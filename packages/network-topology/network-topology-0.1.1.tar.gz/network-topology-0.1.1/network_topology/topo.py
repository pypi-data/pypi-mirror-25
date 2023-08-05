
import networkx as nx
from triangle import triangulate
from shapely.geometry import LineString, Point, Polygon
from shapely.prepared import prep
from shapely.ops import cascaded_union
from itertools import combinations
import numpy as np
import random
from rtree import index
from pprint import pprint


def getNetworkTopology(lineStrings, thickness=14.0, splitAtTeriminals=False,
                       turnThreshold=20.0, minInnerPerimeter=200):
    # Make buffered shape
    big_shape = _makeBufferedShape(lineStrings, thickness, minInnerPerimeter)
    triangles = _triangulate(big_shape, lineStrings, minInnerPerimeter)
    polygons = _polygonize(triangles, big_shape)
    poly_graph = _buildInitialGraph(polygons)
    _tidyIntersections(poly_graph, triangles, polygons)
    skel_graph = _buildSkeletonGraph(poly_graph, triangles, polygons)
    if splitAtTeriminals:
        _splitAtTerminals(skel_graph, lineStrings)
    graph = _findSegmentsAndIntersections(skel_graph, turnThreshold)
    return graph


def _makeBufferedShape(lineStrings, thickness=14.0, minInnerPerimeter=200):
    bufferedShapes = []
    buf = thickness / 2.0
    for ls in lineStrings:
        bufferedShapes.append(ls.buffer(buf, resolution=2, join_style=2))  # cap_style=3
    big_shape = cascaded_union(bufferedShapes)
    filled_shape = Polygon(big_shape.exterior.coords,
                           [ring.coords for ring in big_shape.interiors
                            if ring.length > minInnerPerimeter])
    return filled_shape.simplify(thickness/10.0)  # prep(filled_shape.buffer(-0.1))


def _triangulate(big_shape, lineStrings, minInnerPerimeter=200):
    tri = {
        'vertices': [],
        'segments': []
        }
    lastIndex = 0
    tri['vertices'].append(list(big_shape.exterior.coords[0]))
    for x, y in big_shape.exterior.coords[1:]:
        if [x, y] in tri['vertices']:
            currentIndex = tri['vertices'].index([x, y])
        else:
            currentIndex = len(tri['vertices'])
            tri['vertices'].append([x, y])
        tri['segments'].append([lastIndex, currentIndex])
        lastIndex = currentIndex

    if big_shape.interiors:
        tri['holes'] = []
    for ring in big_shape.interiors:
        if ring.length > minInnerPerimeter:
            x, y = 0, 0
            minx, miny, maxx, maxy = ring.bounds
            while not Polygon(ring).contains(Point(x, y)):
                x = random.uniform(minx, maxx)
                y = random.uniform(miny, maxy)
            tri['holes'].append([x, y])
            lastIndex = len(tri['vertices'])
            tri['vertices'].append(list(ring.coords[0]))
            for x, y in ring.coords[1:]:
                if [x, y] in tri['vertices']:
                    currentIndex = tri['vertices'].index([x, y])
                else:
                    currentIndex = len(tri['vertices'])
                    tri['vertices'].append([x, y])
                tri['segments'].append([lastIndex, currentIndex])
                lastIndex = currentIndex

    for ls in lineStrings:
        for i in [0, -1]:
            coords = list(ls.coords[i])
            if coords not in tri['vertices']:
                tri['vertices'].append(coords)

    return triangulate(tri, 'pq0Da200i')


def _polygonize(res, big_shape):
    prepped_shape = prep(big_shape.buffer(-0.1, cap_style=3, join_style=2))
    polys = [list(vs) for vs in res['triangles']]
    for v, (x, y) in enumerate(res['vertices']):
        # remove any point that is internal to the shape, merging triangles
        if prepped_shape.contains(Point([x, y])):
            shape_graph = nx.Graph()
            affected_polys = []
            for poly, vs in enumerate(polys):
                if v in vs:
                    affected_polys.append(poly)
                    last_pt = vs[0]
                    for pt in vs[1:]:
                        if pt != v and last_pt != v:
                            shape_graph.add_edge(last_pt, pt)
                        last_pt = pt
                    if vs[0] != v and last_pt != v:
                        shape_graph.add_edge(last_pt, vs[0])
            poly = []
            pt = shape_graph.nodes()[0]
            while pt not in poly:
                poly.append(pt)
                neighbours = shape_graph.neighbors(pt)
                if neighbours[0] not in poly:
                    pt = neighbours[0]
                elif neighbours[1] not in poly:
                    pt = neighbours[1]
            polys.append(poly)
            polys = [p for i, p in enumerate(polys) if i not in affected_polys]
    return polys


def _mergeShapes(cluster, TG, polys):
    combined_graph = nx.Graph()
    for shape in cluster:
        for p1, p2 in zip(polys[shape], polys[shape][1:] + [polys[shape][0]]):
            if combined_graph.has_edge(p1, p2):
                combined_graph.remove_edge(p1, p2)
                if not combined_graph[p1]:
                    combined_graph.remove_node(p1)
                if not combined_graph[p2]:
                    combined_graph.remove_node(p2)
            else:
                combined_graph.add_edge(p1, p2)
    poly = []
    pt = combined_graph.nodes()[0]
    while pt not in poly:
        poly.append(pt)
        neighbours = combined_graph.neighbors(pt)
        if neighbours[0] not in poly:
            pt = neighbours[0]
        elif neighbours[1] not in poly:
            pt = neighbours[1]
    cluster = list(cluster)
    base = cluster[0]
    polys[base] = poly
    for shape in cluster[1:]:
        polys[shape] = []
        for n, d in TG[shape].iteritems():
            if n != base:
                TG.add_edge(base, n, **d)
        TG.remove_node(shape)


def _buildInitialGraph(polys):
    edge_tri = {}
    TG = nx.Graph()

    def add_edge(n1, n2, tri, edges, TG):
        n1, n2 = sorted([n1, n2])
        if (n1, n2) not in edges:
            edges[n1, n2] = []
        for other in edges[n1, n2]:
            TG.add_edge(tri, other, v1=n1, v2=n2)
        edges[n1, n2].append(tri)

    for i, t in enumerate(polys):
        for t1, t2 in zip(t[:-1], t[1:]):
            add_edge(t1, t2, i, edge_tri, TG)
        add_edge(t[0], t[-1], i, edge_tri, TG)

    # Collapse internal edges
    central_shapes = [t for t in TG.nodes() if len(TG[t]) > 2]

    for cluster in nx.connected_components(TG.subgraph(central_shapes)):
        _mergeShapes(cluster, TG, polys)

    return TG


def _tidyIntersections(TG, res, polys):
    # 'Tyding T-intersections...'
    toMerge = []
    for node in TG.nodes_iter():
        if TG.degree(node) == 3 and len(polys[node]) == 3:
            points = res['vertices'][polys[node]]
            A = np.array([[p[0]*p[0] + p[1]*p[1], p[0], p[1], 1] for p in points])
            M11 = np.linalg.det(A[:, [1, 2, 3]])
            M12 = np.linalg.det(A[:, [0, 2, 3]])
            M13 = np.linalg.det(A[:, [0, 1, 3]])
            M14 = np.linalg.det(A[:, [0, 1, 2]])
            x = 0.5 * M12/M11
            y = -0.5 * M13/M11
            r2 = M14/M11 + x*x + y*y
            TG.node[node]['centroid'] = [x, y]

            for neighbour, data in TG[node].iteritems():
                points = list(polys[neighbour])
                points.remove(data['v1'])
                points.remove(data['v2'])
                point = res['vertices'][points[0]]
                dx = x - point[0]
                dy = y - point[1]
                if dx*dx + dy*dy < 4*r2:
                    toMerge.append([node, neighbour])

    for cluster in toMerge:
        _mergeShapes(cluster, TG, polys)

    # 'Cleaning up angled crossings...'
    # toMerge = []
    # for node in TG.nodes_iter():
    #     if TG.degree(node) == 2:
    #         sandwiched = True
    #         for neighbour in TG[node]:
    #             if TG.degree(neighbour) == 2:
    #                 sandwiched = False
    #         if sandwiched:
    #             toMerge.append([node] + TG[node].keys())
    #
    # for cluster in toMerge:
    #     _mergeShapes(cluster, TG, polys)


def _makeKey(t1, t2):
    t1, t2 = sorted([t1, t2])
    return int(t1 * 1e9 + t2)


def _insertEdge(G, n1, n2):
    ux = G.node[n1]['x'] - G.node[n2]['x']
    uy = G.node[n1]['y'] - G.node[n2]['y']
    dist = np.sqrt(ux*ux + uy*uy)
    ux /= dist
    uy /= dist
    G.add_edge(n1, n2, ux=ux, uy=uy)


def _buildSkeletonGraph(TG, res, polys):
    node_idx = index.Index()
    G = nx.Graph(index=node_idx)
    for t1, t2, d in TG.edges_iter(data=True):
        x = (res['vertices'][d['v1']][0] + res['vertices'][d['v2']][0])/2.0
        y = (res['vertices'][d['v1']][1] + res['vertices'][d['v2']][1])/2.0
        key = _makeKey(t1, t2)
        node_idx.insert(key, (x, y, x, y))
        G.add_node(key, x=x, y=y)

    for t, d in TG.nodes_iter(data=True):
        if len(TG[t]) == 2:
            pairs = []
            for t2 in TG[t]:
                key = _makeKey(t, t2)
                if key in G:
                    pairs.append(key)
            for e1, e2 in combinations(pairs, 2):
                _insertEdge(G, e1, e2)
        else:  # if len(TG[t]) != 2:
            if 'centroid' in TG.node[t]:
                x, y = TG.node[t]['centroid']
            else:
                # calc centroid & add to graph
                poly = Polygon([list(res['vertices'][v])
                                for v in polys[t]])
                x, y = poly.centroid.coords[0]

            G.add_node(t, x=x, y=y)
            node_idx.insert(t, [x, y, x, y])
            # join all edges to centroid
            for t2 in TG[t]:
                key = _makeKey(t, t2)
                _insertEdge(G, t, key)
    return G


def _splitAtTerminals(G, lineStrings):
    node_idx = G.graph['index']
    for lid, ls in enumerate(lineStrings):
        for i in [0, -1]:
            point = ls.coords[i]
            nearest = list(node_idx.nearest(point + point, num_results=1))[0]
            pid = -float(lid) + 0.1 * i
            G.add_node(pid, x=point[0], y=point[1])
            _insertEdge(G, pid, nearest)


def _findSegmentsAndIntersections(G, turnThreshold=20.0):
    junctions = []
    midpts = []
    threshold = np.cos(turnThreshold/180.0*np.pi)  # np.sqrt(0.5)
    dps = []
    for node in G.nodes_iter():
        if len(G[node]) > 2 or len(G[node]) == 1:
            junctions.append(node)
        elif len(G[node]) == 2:
            ux = []
            uy = []
            for edge, data in G[node].iteritems():
                ux.append(data['ux'])
                uy.append(data['uy'])
            dp = np.abs(ux[0] * ux[1] + uy[0] * uy[1])
            dps.append(dp)
            if dp < threshold:
                junctions.append(node)
            else:
                midpts.append(node)
    segments = list(nx.connected_components(G.subgraph(midpts)))
    BG = nx.blockmodel(G, segments+[[j] for j in junctions])

    lines = []
    ids = []
    to_remove = []
    for node, data in BG.nodes_iter(data=True):
        if data['nnodes'] == 1:
            p = G.node[data['graph'].nodes()[0]]
            data['geom'] = Point(p['x'], p['y'])

    for node, data in BG.nodes_iter(data=True):
        if data['nnodes'] > 1:
            current = data['graph'].nodes()[0]
            successors = nx.dfs_successors(data['graph'], current)
            sequence = [current]
            queue = []
            while current in successors or queue:
                if current in successors:
                    queue += successors[current]
                current = queue[0]
                if current in data['graph'][sequence[-1]]:
                    sequence.append(current)
                else:
                    sequence.insert(0, current)
                queue = queue[1:]

            startNode = None
            endNode = None
            for terminal in BG[node]:
                d = BG.node[terminal]
                if d['graph'].nodes()[0] in G[sequence[0]]:
                    startNode = terminal
                if d['graph'].nodes()[0] in G[sequence[-1]]:
                    endNode = terminal
                    # sequence.insert(0, d['graph'].nodes()[0])
            coords = [[G.node[n]['x'], G.node[n]['y']] for n in sequence]
            line = LineString(coords).simplify(0.1)
            if startNode:
                line = line.difference(BG.node[startNode]['geom'].buffer(1))
            if endNode:
                line = line.difference(BG.node[endNode]['geom'].buffer(1))
            data['geom'] = line
            data['start'] = startNode
            data['end'] = endNode
            if line.length < 7:
                to_remove.append(node)
            else:
                lines.append(line)
                ids.append(node)
    BG.remove_nodes_from(to_remove)

    return BG

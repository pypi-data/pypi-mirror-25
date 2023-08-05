"""Module for map-matching source linestrings back to the topological graph."""

import math
import itertools
import heapq
import networkx as nx
from rtree import index
import numpy as np
import sys


def getMatchedRoutes(lineStrings, DG, increment=100, scope=30):
    """List the segments/edges that best match each linestring."""
    idx = _buildIndex(DG)
    paths = []
    for ls in lineStrings:
        adjacency_list, s, t = _findCandidatePoints(DG, idx, ls,
                                                    increment=increment,
                                                    scope=scope)
        path = _viterbi_search(adjacency_list, s, t, DG)
        paths.append(path)
    return paths


def _buildIndex(DG):
    shapeIdx = index.Index()
    for u, v, i, data in DG.edges(data=True, keys=True):
        shapeIdx.insert(hash((u, v, i)), data['geom'].bounds, obj=(u, v, i))
    return shapeIdx


def _findCandidatePoints(DG, shapeIdx, lineString, increment=100, scope=30):
    adjacency_list = {}
    totalLength = lineString.length
    s = Candidate(DG, start=True)
    t = Candidate(DG, end=True)
    lastRound = [s]
    adjacency_list[t] = []
    for distance in np.linspace(0, totalLength, int(totalLength/increment)+1):
        p = lineString.interpolate(distance)
        nextRound = []
        for item in shapeIdx.intersection((p.x-scope, p.y-scope,
                                           p.x+scope, p.y+scope),
                                          objects=True):
            candidate = Candidate(DG, segment=item.object, measurement=p)
            nextRound.append(candidate)
        if nextRound:
            for prev in lastRound:
                adjacency_list[prev] = list(nextRound)
            lastRound = nextRound
    for prev in lastRound:
        adjacency_list[prev] = [t]
    return adjacency_list, s, t


def _viterbi_search(adjacency_list, s, t, DG):
    # With credit to the "Map Matching in a Programmer's Perspective" guide
    # in Valhalla by Mapzen:
    # https://github.com/valhalla/meili/blob/master/docs/meili/algorithms.md

    # Initialize joint probability for each node
    if 'path_cache' not in DG.graph:
        DG.graph['path_cache'] = {}
    cost = {}
    for u in adjacency_list:
        cost[u] = 1e100
    predecessor = {}
    queue = PriorityQueue()

    cost[s] = s.emission_cost()
    queue.add_or_update(s, cost[s])
    predecessor[s] = None
    while not queue.empty():
        # Extract node u
        u = queue.pop()
        if u == t:
            break
        for v in adjacency_list[u]:
            # Relaxation
            new_cost = (cost[u] +
                        u.transition_cost(v, DG.graph['path_cache']) +
                        v.emission_cost())
            if cost[v] > new_cost:
                cost[v] = new_cost
                predecessor[v] = u
            queue.add_or_update(v, cost[v])
    return _construct_path(predecessor, s, t, DG.graph['path_cache'])


def _construct_path(predecessor, s, t, cache):
    cur = predecessor[t]
    sequence = [cur.segment]
    prev = predecessor[cur]
    while prev is not s:
        if not(prev.segment == cur.segment and prev.offset <= cur.offset):
            if (prev.segment, cur.segment) in cache:
                sequence = cache[prev.segment, cur.segment][1] + sequence
        if sequence[0] != prev.segment:
            sequence.insert(0, prev.segment)
        cur = prev
        prev = predecessor[cur]
    return sequence

SIGMA_Z = 4.07
BETA = 3.0


class Candidate:
    """Class for candidate segment."""

    def __init__(self, DG, segment=None, measurement=None,
                 start=False, end=False):
        """Initialize."""
        self.start = start
        self.end = end
        self.measurement = measurement
        self.segment = segment
        self.DG = DG
        if segment:
            geom = DG.get_edge_data(*segment)['geom']
            self.offset = geom.project(measurement)
            self.distance = geom.distance(measurement)
            self.remaining = geom.length - self.offset
        else:
            self.distance = 0
            self.offset = 0
            self.remaining = 0

    def __hash__(self):
        """Hash for use as dictionary keys."""
        if self.start:
            return hash('start')
        elif self.end:
            return hash('end')
        else:
            return hash((self.segment, self.offset))

    def __str__(self):
        """String representation as segment id and offset."""
        return '{}>{}'.format(self.segment, self.offset)

    def __repr__(self):
        """Just use string representation."""
        return self.__str__()

    def emission_cost(self):
        """Gaussian distribution."""
        c = 1 / (SIGMA_Z * math.sqrt(2 * math.pi))
        prob = c * math.exp(-(self.distance**2))
        return -1 * math.log10(max(prob, sys.float_info.min))

    def transition_cost(self, nextCandidate, cache):
        """Empirical distribution."""
        if self.measurement is None:
            return nextCandidate.offset
        elif nextCandidate.measurement is None:
            return self.remaining
        c = 1 / BETA
        route_distance, crossed = self._route_distance_to(nextCandidate, cache)
        delta = abs(route_distance -
                    self.measurement.distance(nextCandidate.measurement))
        # Apply a small bias against changing edges, to avoid swithcing between
        # opposide edges unnecessarily.
        delta *= 1.000000000001**crossed
        prob = c * math.exp(-delta)
        return -1 * math.log10(max(prob, sys.float_info.min))

    def _route_distance_to(self, nextCandidate, cache):
        if nextCandidate.segment == self.segment and nextCandidate.offset >= self.offset:
            return nextCandidate.offset - self.offset, 0
        if self.segment is None or nextCandidate.segment is None:
            return 0, 0
        terminalDistance = self.remaining + nextCandidate.offset
        if self.segment[1] == nextCandidate.segment[0]:
            return terminalDistance, 1
        sumDistance = 0
        index = (self.segment, nextCandidate.segment)
        if index in cache:
            sumDistance, edgeSequence = cache[index]
        else:
            sequence = nx.dijkstra_path(self.DG, self.segment[1],
                                        nextCandidate.segment[0],
                                        weight='length')
            edgeSequence = []
            for u, v in zip(sequence[:-1], sequence[1:]):
                i = min(self.DG.edge[u][v],
                        key=lambda x: self.DG.edge[u][v][x]['length'])
                edgeSequence.append((u, v, i))
                sumDistance += self.DG.edge[u][v][i]['length']
            cache[index] = sumDistance, edgeSequence
        return sumDistance + terminalDistance, len(edgeSequence) + 1


class PriorityQueue:
    """Priority queue for use in Dijkstra search."""

    REMOVED = '<removed-item>'  # placeholder for a removed item

    def __init__(self):
        """Initialize priority queue."""
        self.pq = []                       # list of entries arranged in a heap
        self.entry_finder = {}             # mapping of items to entries
        self.counter = itertools.count()   # unique sequence count

    def add_or_update(self, item, priority=0):
        """Add a new item or update the priority of an existing item."""
        if item in self.entry_finder:
            self.remove(item)
        count = next(self.counter)
        entry = [priority, count, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.pq, entry)

    def remove(self, item):
        """Mark an existing item as REMOVED.  Raise KeyError if not found."""
        entry = self.entry_finder.pop(item)
        entry[-1] = self.REMOVED

    def pop(self):
        """Remove and return the lowest priority task. Raise error if empty."""
        while self.pq:
            priority, count, item = heapq.heappop(self.pq)
            if item is not self.REMOVED:
                del self.entry_finder[item]
                return item
        raise KeyError('pop from an empty priority queue')

    def empty(self):
        """Return true if the priority queue is empty."""
        return len(self.pq) == 0

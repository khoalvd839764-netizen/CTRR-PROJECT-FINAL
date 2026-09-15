# -*- coding: utf-8 -*-
from core.converter import (
    matrix_to_adj, matrix_to_edges,
    edges_to_matrix, edges_to_adj,
    adj_to_matrix, adj_to_edges
)


class Graph:
    def __init__(self, n=0, directed=False, weighted=False, pos=None, labels=None, curvatures=None, weight_positions=None):
        self.n = n
        self.directed = directed
        self.weighted = weighted
        self.pos = pos
        self.labels = labels
        self.curvatures = curvatures
        self.weight_positions = weight_positions
        
        self.matrix = [[0] * n for _ in range(n)]
        self.adj = {i: [] for i in range(n)}
        self.edges = []

    def from_matrix(self, matrix, pos=None, labels=None, curvatures=None, weight_positions=None):
        self.n = len(matrix)
        self.matrix = matrix
        self.adj = matrix_to_adj(matrix, self.directed)
        self.edges = matrix_to_edges(matrix, self.directed)
        if pos is not None:
            self.pos = pos
        if labels is not None:
            self.labels = labels
        if curvatures is not None:
            self.curvatures = curvatures
        if weight_positions is not None:
            self.weight_positions = weight_positions
        return self

    def from_edges(self, edges, n=None, pos=None, labels=None, curvatures=None, weight_positions=None):
        max_v = -1
        for edge in edges:
            max_v = max(max_v, edge[0], edge[1])
        if n is None or n <= max_v:
            self.n = max_v + 1
        else:
            self.n = n

        self.edges = edges
        self.matrix = edges_to_matrix(edges, self.n, self.directed)
        self.adj = edges_to_adj(edges, self.n, self.directed)
        if pos is not None:
            self.pos = pos
        if labels is not None:
            self.labels = labels
        if curvatures is not None:
            self.curvatures = curvatures
        if weight_positions is not None:
            self.weight_positions = weight_positions
        return self

    def from_text(self, text):
        lines = [l.strip() for l in text.strip().split('\n') if l.strip()] 
        if not lines:
            return self

        first_parts = lines[0].split() 
        if len(first_parts) == 1 and first_parts[0].isdigit():
            n = int(first_parts[0]) 
            mat = []
            for l in lines[1:n + 1]:
                mat.append([float(x) if '.' in x else int(x) for x in l.split()])
            self.from_matrix(mat)
        else:
            edges = []
            for l in lines:
                p = l.split()
                if len(p) >= 2:
                    u = int(p[0])
                    v = int(p[1])
                    w = float(p[2]) if len(p) >= 3 else 1
                    edges.append((u, v, w))
            self.from_edges(edges)
        return self

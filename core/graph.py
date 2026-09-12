# -*- coding: utf-8 -*-
"""Cấu trúc dữ liệu Đồ thị G=(V, E), đồng bộ 3 dạng biểu diễn. Chi tiết: core/chu_thich_thuat_toan/1_graph.md"""
from core.converter import (
    matrix_to_adj, matrix_to_edges,
    edges_to_matrix, edges_to_adj,
    adj_to_matrix, adj_to_edges
)


class Graph:
    """Đối tượng Đồ thị đồng bộ song song ma trận kề, danh sách kề và danh sách cạnh."""
    def __init__(self, n=0, directed=False, weighted=False, pos=None):
        self.n = n
        self.directed = directed
        self.weighted = weighted
        self.pos = pos
        
        self.matrix = [[0] * n for _ in range(n)]
        self.adj = {i: [] for i in range(n)}
        self.edges = []

    def from_matrix(self, matrix, pos=None):
        """Khởi dựng đồ thị từ ma trận kề và đồng bộ sang danh sách kề và cạnh."""
        self.n = len(matrix)
        self.matrix = matrix
        self.adj = matrix_to_adj(matrix, self.directed)
        self.edges = matrix_to_edges(matrix, self.directed)
        if pos is not None:
            self.pos = pos
        return self

    def from_edges(self, edges, n=None, pos=None):
        """Khởi dựng đồ thị từ danh sách cạnh và đồng bộ sang ma trận và danh sách kề."""
        if n is None:
            max_v = -1
            for edge in edges:
                max_v = max(max_v, edge[0], edge[1])
            self.n = max_v + 1
        else:
            self.n = n

        self.edges = edges
        self.matrix = edges_to_matrix(edges, self.n, self.directed)
        self.adj = edges_to_adj(edges, self.n, self.directed)
        if pos is not None:
            self.pos = pos
        return self

    def from_text(self, text):
        """
        Nạp đồ thị từ chuỗi văn bản:
          - Dòng đầu chứa 1 số nguyên n: Nhận diện ma trận kề n x n.
          - Mỗi dòng chứa 2 hoặc 3 số (u, v[, w]): Nhận diện danh sách cạnh.
        """
        lines = [l.strip() for l in text.strip().split('\n') if l.strip()] 
        if not lines:
            return self

        first_parts = lines[0].split() 
        # Nếu dòng đầu chỉ có 1 số nguyên -> Nạp dạng ma trận kề
        if len(first_parts) == 1 and first_parts[0].isdigit():
            n = int(first_parts[0]) 
            mat = []
            for l in lines[1:n + 1]:
                mat.append([float(x) if '.' in x else int(x) for x in l.split()])
            self.from_matrix(mat)
        else:
            # Nạp dạng danh sách cạnh (u, v[, w])
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

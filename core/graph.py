# -*- coding: utf-8 -*-
"""
Module: core/graph.py
Định nghĩa đối tượng trung tâm `Graph` của đề tài CTRR.

Vai trò kiến trúc:
  - Tiếp nhận đồ thị đầu vào dưới bất kỳ hình thức nào (Ma trận kề, Danh sách cạnh, hoặc File văn bản Text).
  - Tự động đồng bộ hóa và duy trì song song cả 3 dạng biểu diễn bằng các hàm converter.
  - Cung cấp giao diện nhất quán cho tất cả các thuật toán giải quyết bài toán:
    + BFS/DFS/Dijkstra cần Danh sách kề để duyệt nhanh các đỉnh lân cận.
    + Kruskal/Bellman-Ford cần Danh sách cạnh để quét toàn bộ cạnh.
    + Ford-Fulkerson cần Ma trận để truy xuất dung lượng capacity[u][v] tức thời.
"""
from core.converter import (
    matrix_to_adj, matrix_to_edges,
    edges_to_matrix, edges_to_adj,
    adj_to_matrix, adj_to_edges
)


class Graph:
    """
    Lớp biểu diễn cấu trúc Đồ thị $G = (V, E)$.
    Tự động đồng bộ hóa giữa 3 cấu trúc dữ liệu nền tảng.
    """
    def __init__(self, n=0, directed=False, weighted=False):
        """
        Khởi tạo đồ thị với:
          - n: Số đỉnh (đánh số từ 0 đến n-1).
          - directed: Đồ thị có hướng (True) hay vô hướng (False).
          - weighted: Đồ thị có trọng số (True) hay không trọng số (False).
        """
        self.n = n
        self.directed = directed
        self.weighted = weighted
        
        # Khởi tạo 3 cấu trúc rỗng
        self.matrix = [[0] * n for _ in range(n)]
        self.adj = {i: [] for i in range(n)}
        self.edges = []

    def from_matrix(self, matrix):
        """
        Khởi dựng đồ thị từ Ma trận kề (Adjacency Matrix).
        Tự động tính toán và cập nhật Danh sách kề (adj) và Danh sách cạnh (edges).
        """
        self.n = len(matrix)
        self.matrix = matrix
        # Đồng bộ hóa sang 2 dạng biểu diễn còn lại
        self.adj = matrix_to_adj(matrix, self.directed)
        self.edges = matrix_to_edges(matrix, self.directed)
        return self

    def from_edges(self, edges, n=None):
        """
        Khởi dựng đồ thị từ Danh sách cạnh (Edge List).
        Nếu không truyền n, tự động suy diễn số lượng đỉnh dựa trên chỉ số đỉnh lớn nhất xuất hiện.
        """
        if n is None:
            # Thuật toán tự động tìm số đỉnh n = max(chỉ số đỉnh) + 1
            max_v = -1
            for edge in edges:
                max_v = max(max_v, edge[0], edge[1])
            self.n = max_v + 1
        else:
            self.n = n

        self.edges = edges
        # Đồng bộ hóa sang Ma trận kề và Danh sách kề
        self.matrix = edges_to_matrix(edges, self.n, self.directed)
        self.adj = edges_to_adj(edges, self.n, self.directed)
        return self

    def from_text(self, text):
        """
        Phân tích chuỗi văn bản (từ file text hoặc nhập bàn phím):
        Hỗ trợ 2 định dạng phổ biến trong đề thi và bài tập:
          1. Định dạng Ma trận: Dòng đầu là số nguyên n (số đỉnh), n dòng sau là ma trận n x n.
          2. Định dạng Danh sách cạnh: Mỗi dòng chứa 2 hoặc 3 số (u, v[, w]).
        """
        lines = [l.strip() for l in text.strip().split('\n') if l.strip()] 
        if not lines:
            return self

        first_parts = lines[0].split() 
        # Nhận diện định dạng: Nếu dòng đầu tiên chỉ có 1 số nguyên duy nhất -> Định dạng Ma trận
        if len(first_parts) == 1 and first_parts[0].isdigit():
            n = int(first_parts[0]) 
            mat = []
            for l in lines[1:n + 1]:
                # Chuyển đổi linh hoạt số thực (float) hoặc số nguyên (int)
                mat.append([float(x) if '.' in x else int(x) for x in l.split()])
            self.from_matrix(mat)
        else:
            # Định dạng Danh sách cạnh: mỗi dòng là một cạnh (u, v, w)
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

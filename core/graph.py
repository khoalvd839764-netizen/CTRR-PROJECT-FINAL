# -*- coding: utf-8 -*-
"""
Module: core/graph.py
Mục đích: Định nghĩa lớp Graph - cấu trúc dữ liệu trung tâm đại diện cho đồ thị trong ứng dụng:
  - Hỗ trợ cả đồ thị có hướng (Directed) và vô hướng (Undirected), có trọng số và không trọng số.
  - Quản lý đồng bộ giữa 3 biểu diễn: Ma trận kề (matrix), Danh sách kề (adj), và Danh sách cạnh (edges).
  - Lưu trữ thông tin tọa độ các đỉnh (pos) và thuộc tính vẽ (labels, curvatures, weight_positions).
  - Hỗ trợ nạp dữ liệu linh hoạt từ Ma trận, Danh sách cạnh, hoặc Chuỗi văn bản thô (Text format).
"""
from core.converter import (
    matrix_to_adj, matrix_to_edges,
    edges_to_matrix, edges_to_adj,
    adj_to_matrix, adj_to_edges
)


class Graph:
    def __init__(self, n=0, directed=False, weighted=False, pos=None, labels=None, curvatures=None, weight_positions=None):
        """
        Khởi tạo đối tượng đồ thị rỗng hoặc với các thuộc tính cơ bản.
        """
        self.n = n                          # Số lượng đỉnh
        self.directed = directed            # True nếu là đồ thị có hướng, False nếu vô hướng
        self.weighted = weighted            # True nếu có trọng số
        self.pos = pos                      # Dict {đỉnh: (x, y)} lưu tọa độ hiển thị đồ họa
        self.labels = labels                # Dict {đỉnh: tên_nhãn} (vd: {0: 'A', 1: 'B'})
        self.curvatures = curvatures        # Dict lưu độ cong khi vẽ các cạnh song song
        self.weight_positions = weight_positions  # Dict lưu vị trí hiển thị số trọng số
        
        # 3 dạng biểu diễn cốt lõi của đồ thị
        self.matrix = [[0] * n for _ in range(n)]  # Ma trận kề (Adjacency Matrix)
        self.adj = {i: [] for i in range(n)}       # Danh sách kề (Adjacency List) dạng {u: [(v, w), ...]}
        self.edges = []                            # Danh sách cạnh (Edge List) dạng [(u, v, w), ...]

    def from_matrix(self, matrix, pos=None, labels=None, curvatures=None, weight_positions=None):
        """
        Nạp đồ thị từ một ma trận kề n x n và tự động đồng bộ sang danh sách kề và danh sách cạnh.
        """
        self.n = len(matrix)
        self.matrix = matrix
        # Chuyển đổi ma trận sang danh sách kề và danh sách cạnh
        self.adj = matrix_to_adj(matrix, self.directed)
        self.edges = matrix_to_edges(matrix, self.directed)
        
        # Cập nhật thông tin bố cục đồ họa nếu có truyền vào
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
        """
        Nạp đồ thị từ danh sách cạnh [(u, v, w), ...] và đồng bộ sang ma trận kề và danh sách kề.
        """
        # Tự động xác định số đỉnh lớn nhất nếu người dùng không truyền n
        max_v = -1
        for edge in edges:
            max_v = max(max_v, edge[0], edge[1])
        if n is None or n <= max_v:
            self.n = max_v + 1
        else:
            self.n = n

        self.edges = edges
        # Chuyển đổi danh sách cạnh sang ma trận và danh sách kề
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
        """
        Phân tích chuỗi văn bản tự do nhập từ giao diện:
        - Dạng 1: Dòng đầu là số nguyên n, tiếp theo là n dòng biểu diễn ma trận kề.
        - Dạng 2: Mỗi dòng là một cạnh gồm 2 hoặc 3 số (u, v [trọng số w]).
        """
        lines = [l.strip() for l in text.strip().split('\n') if l.strip()] 
        if not lines:
            return self

        first_parts = lines[0].split() 
        # Nếu dòng đầu tiên chỉ có 1 số nguyên n -> Định dạng Ma trận kề
        if len(first_parts) == 1 and first_parts[0].isdigit():
            n = int(first_parts[0]) 
            mat = []
            for l in lines[1:n + 1]:
                mat.append([float(x) if '.' in x else int(x) for x in l.split()])
            self.from_matrix(mat)
        else:
            # Ngược lại -> Định dạng Danh sách cạnh từng dòng
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

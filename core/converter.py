# -*- coding: utf-8 -*-
"""
Module: core/converter.py
Cung cấp 6 hàm chuyển đổi hai chiều giữa 3 phương pháp biểu diễn đồ thị chuẩn trong Toán Rời Rạc:
  1. Ma trận kề (Adjacency Matrix)
  2. Danh sách kề (Adjacency List)
  3. Danh sách cạnh (Edge List)

Quy ước toán học:
  - Đồ thị vô hướng: Cạnh (u, v) với trọng số w xuất hiện 2 chiều (u->v và v->u).
    Ma trận kề có tính đối xứng: M[u][v] = M[v][u].
  - Đồ thị có hướng: Cạnh (u, v) chỉ đi 1 chiều từ u sang v.
"""

def matrix_to_adj(matrix, directed=False):
    """
    [HÀM 1]: Chuyển đổi Ma trận kề (Adjacency Matrix) -> Danh sách kề (Adjacency List).
    
    Thuật toán:
      - Duyệt qua từng hàng i (đỉnh nguồn) và cột j (đỉnh đích).
      - Nếu M[i][j] != 0: Tồn tại cạnh từ i đến j với trọng số M[i][j].
      - Thêm cặp (j, weight) vào danh sách các đỉnh kề của đỉnh i: adj[i].
    
    Độ phức tạp: O(V^2).
    """
    n = len(matrix)
    # Khởi tạo dictionary với mỗi đỉnh i từ 0 đến n-1 trỏ đến một list rỗng []
    adj = {i: [] for i in range(n)}
    
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                # Đỉnh j là lân cận của đỉnh i với trọng số matrix[i][j]
                adj[i].append((j, matrix[i][j]))
    return adj


def matrix_to_edges(matrix, directed=False):
    """
    [HÀM 2]: Chuyển đổi Ma trận kề (Adjacency Matrix) -> Danh sách cạnh (Edge List).
    
    Điểm cốt lõi (Tránh trùng lặp cạnh trong đồ thị vô hướng):
      - Đồ thị có hướng (directed=True): Phải duyệt toàn bộ ma trận (j chạy từ 0 đến n-1)
        vì cạnh (i, j) và (j, i) là hai cung có hướng riêng biệt.
      - Đồ thị vô hướng (directed=False): Chỉ cần duyệt nửa trên ma trận (j chạy từ i đến n-1)
        hoặc đường chéo chính trở đi. Cạnh (i, j) và (j, i) đại diện cho cùng một cạnh vô hướng.
    
    Độ phức tạp: O(V^2).
    """
    n = len(matrix)
    edges = []
    
    for i in range(n):
        # Nếu vô hướng: start_j = i (chỉ quét tam giác trên của ma trận kề)
        # Nếu có hướng: start_j = 0 (quét toàn bộ ô)
        start_j = 0 if directed else i
        for j in range(start_j, n):
            if matrix[i][j] != 0:
                # Lưu dưới dạng bộ 3: (đỉnh nguồn u, đỉnh đích v, trọng số w)
                edges.append((i, j, matrix[i][j]))
    return edges


def edges_to_matrix(edges, n, directed=False):
    """
    [HÀM 3]: Chuyển đổi Danh sách cạnh (Edge List) -> Ma trận kề (Adjacency Matrix).
    
    Thuật toán:
      - Khởi tạo ma trận kích thước n x n với toàn bộ giá trị ban đầu là 0.
      - Duyệt từng cạnh (u, v, w):
        + Gán matrix[u][v] = w.
        + Nếu là đồ thị vô hướng: Gán thêm matrix[v][u] = w để đảm bảo tính đối xứng.
    
    Độ phức tạp: O(V^2 + E).
    """
    # Khởi tạo ma trận vuông n x n chứa toàn bộ số 0 (chưa có cạnh nối)
    matrix = [[0] * n for _ in range(n)]
    
    for edge in edges:
        u = edge[0]
        v = edge[1]
        # Nếu bộ dữ liệu cạnh có trọng số thì lấy edge[2], nếu không mặc định w = 1
        weight = edge[2] if len(edge) >= 3 else 1
        
        matrix[u][v] = weight
        if not directed:
            # Đồ thị vô hướng có tính đối xứng qua đường chéo chính
            matrix[v][u] = weight
            
    return matrix


def edges_to_adj(edges, n, directed=False):
    """
    [HÀM 4]: Chuyển đổi Danh sách cạnh (Edge List) -> Danh sách kề (Adjacency List).
    
    Thuật toán:
      - Khởi tạo dict adj với n đỉnh rỗng.
      - Với mỗi cạnh (u, v, w):
        + Đưa (v, w) vào danh sách lân cận của u: adj[u].append((v, w)).
        + Nếu vô hướng: Đưa ngược lại (u, w) vào danh sách lân cận của v: adj[v].append((u, w)).
    
    Độ phức tạp: O(V + E).
    """
    adj = {i: [] for i in range(n)}
    
    for edge in edges:
        u = edge[0]
        v = edge[1]
        weight = edge[2] if len(edge) >= 3 else 1
        
        adj[u].append((v, weight))
        if not directed:
            # Vô hướng: Đường đi 2 chiều giữa u và v
            adj[v].append((u, weight))
            
    return adj


def adj_to_matrix(adj, n):
    """
    [HÀM 5]: Chuyển đổi Danh sách kề (Adjacency List) -> Ma trận kề (Adjacency Matrix).
    
    Thuật toán:
      - Khởi tạo ma trận vuông n x n toàn số 0.
      - Duyệt qua từng đỉnh u và danh sách các đỉnh kề (v, w):
        + Gán ô tương ứng trong ma trận: matrix[u][v] = w.
    
    Độ phức tạp: O(V^2 + E).
    """
    matrix = [[0] * n for _ in range(n)]
    
    for u, neighbors in adj.items():
        for v, weight in neighbors:
            matrix[u][v] = weight
            
    return matrix


def adj_to_edges(adj, directed=False):
    """
    [HÀM 6]: Chuyển đổi Danh sách kề (Adjacency List) -> Danh sách cạnh (Edge List).
    
    Điểm cốt lõi:
      - Với đồ thị vô hướng: Mỗi cạnh được lưu 2 lần trong adj (v trong adj[u] và u trong adj[v]).
      - Để không ghi lặp lại cạnh 2 lần, ta chỉ ghi nhận khi đỉnh nguồn nhỏ hơn hoặc bằng đỉnh đích (u <= v).
    
    Độ phức tạp: O(V + E).
    """
    edges = []
    for u, neighbors in adj.items():
        for v, weight in neighbors:
            # Lọc chống trùng lặp: Nếu có hướng thì lấy hết; nếu vô hướng chỉ lấy khi u <= v
            if directed or u <= v:
                edges.append((u, v, weight))
    return edges

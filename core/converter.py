# -*- coding: utf-8 -*-
"""6 hàm chuyển đổi 2 chiều giữa Ma trận, DS kề và DS cạnh. Chi tiết: core/chu_thich_thuat_toan/2_converter.md"""

def matrix_to_adj(matrix, directed=False):
    """Chuyển đổi Ma trận kề -> Danh sách kề (O(V^2))."""
    n = len(matrix)
    adj = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                adj[i].append((j, matrix[i][j]))
    return adj


def matrix_to_edges(matrix, directed=False):
    """Chuyển đổi Ma trận kề -> Danh sách cạnh (O(V^2)). Vô hướng chỉ quét j >= i."""
    n = len(matrix)
    edges = []
    for i in range(n):
        start_j = 0 if directed else i
        for j in range(start_j, n):
            if matrix[i][j] != 0:
                edges.append((i, j, matrix[i][j]))
    return edges


def edges_to_matrix(edges, n, directed=False):
    """Chuyển đổi Danh sách cạnh -> Ma trận kề. Độ phức tạp: O(V^2 + E)."""
    matrix = [[0] * n for _ in range(n)]
    for edge in edges:
        u, v = edge[0], edge[1]
        weight = edge[2] if len(edge) >= 3 else 1
        matrix[u][v] = weight
        if not directed:
            matrix[v][u] = weight
    return matrix


def edges_to_adj(edges, n, directed=False):
    """Chuyển đổi Danh sách cạnh -> Danh sách kề. Độ phức tạp: O(V + E)."""
    adj = {i: [] for i in range(n)}
    for edge in edges:
        u, v = edge[0], edge[1]
        weight = edge[2] if len(edge) >= 3 else 1
        adj[u].append((v, weight))
        if not directed:
            adj[v].append((u, weight))
    return adj


def adj_to_matrix(adj, n):
    """Chuyển đổi Danh sách kề -> Ma trận kề. Độ phức tạp: O(V^2 + E)."""
    matrix = [[0] * n for _ in range(n)]
    for u, neighbors in adj.items():
        for v, weight in neighbors:
            matrix[u][v] = weight
    return matrix


def adj_to_edges(adj, directed=False):
    """Chuyển đổi Danh sách kề -> Danh sách cạnh (O(V + E)). Vô hướng chỉ lấy u <= v."""
    edges = []
    for u, neighbors in adj.items():
        for v, weight in neighbors:
            if directed or u <= v:
                edges.append((u, v, weight))
    return edges

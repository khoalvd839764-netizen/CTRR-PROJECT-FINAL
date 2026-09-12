# -*- coding: utf-8 -*-
"""Luồng cực đại & Lát cắt hẹp nhất (Edmonds-Karp BFS). Chi tiết: core/chu_thich_thuat_toan/8_max_flow.md"""
from collections import deque


def bfs_augmenting_path(residual, n, source, sink):
    """Tìm đường tăng luồng ngắn nhất trên đồ thị phần dư (residual > 0). Chi tiết: 8_max_flow.md"""
    visited = [False] * n
    parent = [-1] * n
    queue = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()
        if u == sink:
            break
            
        for v in range(n):
            if not visited[v] and residual[u][v] > 0:
                visited[v] = True
                parent[v] = u
                queue.append(v)

    if visited[sink]:
        path = []
        curr = sink
        while curr != -1:
            path.append(curr)
            curr = parent[curr]
        path.reverse()
        return path, parent
        
    return None, None


def ford_fulkerson(edges, n, source, sink):
    """Tìm Max-Flow & Min-Cut S-T bằng Edmonds-Karp (O(V * E^2)). Chi tiết: 8_max_flow.md"""
    # 1. Xây dựng ma trận dung lượng
    capacity = [[0] * n for _ in range(n)]

    if isinstance(edges, list) and len(edges) > 0 and isinstance(edges[0], (list, tuple)) and len(edges[0]) == n:
        for i in range(n):
            for j in range(n):
                capacity[i][j] = edges[i][j]
    else:
        for edge in edges:
            if len(edge) == 3:
                u, v, cap = edge
                capacity[u][v] += cap
            elif len(edge) == 2:
                u, v = edge
                capacity[u][v] += 1

    # 2. Khởi tạo đồ thị phần dư
    residual = [row[:] for row in capacity]
    max_flow = 0
    trace_table = []
    step = 0

    # 3. Vòng lặp tăng luồng (Edmonds-Karp BFS)
    while True:
        path, parent = bfs_augmenting_path(residual, n, source, sink)
        if path is None:
            break

        step += 1

        # Tìm dung lượng thặng dư nhỏ nhất (bottleneck)
        bottleneck = float('inf')
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            bottleneck = min(bottleneck, residual[u][v])

        # Cập nhật đồ thị phần dư: giảm cung thuận, tăng cung nghịch
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck

        max_flow += bottleneck
        trace_table.append({
            "step": step,
            "path": path,
            "bottleneck": bottleneck,
            "current_max_flow": max_flow
        })

    # 4. Tính ma trận luồng thực tế
    flow_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if capacity[i][j] > 0:
                flow_matrix[i][j] = max(0, capacity[i][j] - residual[i][j])

    # 5. Xác định lát cắt hẹp nhất (Min-Cut S-T)
    visited_cut = [False] * n
    queue_cut = deque([source])
    visited_cut[source] = True

    while queue_cut:
        u = queue_cut.popleft()
        for v in range(n):
            if not visited_cut[v] and residual[u][v] > 0:
                visited_cut[v] = True
                queue_cut.append(v)

    S_set = {i for i in range(n) if visited_cut[i]}
    T_set = {i for i in range(n) if not visited_cut[i]}

    min_cut_edges = []
    for u in S_set:
        for v in T_set:
            if capacity[u][v] > 0:
                min_cut_edges.append((u, v, capacity[u][v]))

    return max_flow, flow_matrix, min_cut_edges, (S_set, T_set), trace_table

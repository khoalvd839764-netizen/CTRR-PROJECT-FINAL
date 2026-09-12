# -*- coding: utf-8 -*-
"""Đường đi ngắn nhất: Dijkstra (w >= 0) và Bellman-Ford (w âm, phát hiện chu trình âm). Chi tiết: core/chu_thich_thuat_toan/5_shortest_path.md"""

def dijkstra(adj, n, start, end=None):
    """Tìm đường đi ngắn nhất bằng Dijkstra (Greedy Choice + Relaxation). Chi tiết: 5_shortest_path.md"""
    dist = [float('inf')] * n
    visited = [False] * n
    parent = [-1] * n
    dist[start] = 0
    trace = []

    for step in range(n):
        u = -1
        min_dist = float('inf')
        
        # 1. Lựa chọn tham lam: Tìm đỉnh chưa thăm có khoảng cách nhỏ nhất
        for i in range(n):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i

        if u == -1 or dist[u] == float('inf'):
            break

        visited[u] = True
        trace.append({
            "step": step + 1,
            "u": u,
            "dist": list(dist),
            "parent": list(parent)
        }) 

        if end is not None and u == end:
            break

        # 2. Nới lỏng cạnh (Relaxation)
        for v, w in adj.get(u, []):
            if not visited[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u

    # 3. Truy vết đường đi từ đích về nguồn
    path = None
    if end is not None:
        if dist[end] != float('inf'):
            cur = end
            path = []
            while cur != -1:
                path.append(cur)
                cur = parent[cur]
            path.reverse()

    return {
        "dist": dist,
        "parent": parent,
        "path": path,
        "cost": dist[end] if end is not None and dist[end] != float('inf') else None,
        "trace": trace
    }


def bellman_ford(edges, n, start, directed=False, end=None):
    """Tìm đường ngắn nhất & phát hiện chu trình âm qua n vòng lặp. Chi tiết: 5_shortest_path.md"""
    dist = [float('inf')] * n
    parent = [-1] * n
    dist[start] = 0
    trace = []

    # Chuẩn hóa danh sách cạnh (u, v, w)
    formatted_edges = []
    for e in edges:
        u, v = e[0], e[1]
        w = e[2] if len(e) >= 3 else 1
        formatted_edges.append((u, v, w))
        if not directed:
            formatted_edges.append((v, u, w))

    # 1. Lặp n-1 vòng Relaxation
    for i in range(n - 1):
        changed = False
        for u, v, w in formatted_edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
                
        trace.append(list(dist))
        if not changed:
            break

    # 2. Vòng thứ n: Phát hiện chu trình âm
    has_neg = False
    for u, v, w in formatted_edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            has_neg = True
            break

    # 3. Truy vết đường đi
    path = None
    if end is not None and not has_neg:
        if dist[end] != float('inf'):
            cur = end
            path = []
            while cur != -1:
                path.append(cur)
                cur = parent[cur]
            path.reverse()

    return {
        "dist": dist,
        "parent": parent,
        "path": path,
        "cost": dist[end] if end is not None and dist[end] != float('inf') else None,
        "has_negative_cycle": has_neg,
        "trace": trace
    }

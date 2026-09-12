# -*- coding: utf-8 -*-
"""Thuật toán duyệt BFS và DFS, sinh cây khung và bảng vết. Chi tiết: core/chu_thich_thuat_toan/3_traversal.md"""

def bfs(adj, n, start, record_trace=True):
    """Duyệt theo chiều rộng (BFS). Trả về: (order, tree_edges, trace_table). Chi tiết: 3_traversal.md"""
    visited = [False] * n
    parent = [-1] * n
    queue = [start]
    visited[start] = True

    order = []
    tree_edges = []
    trace_table = []

    while len(queue) > 0:
        u = queue.pop(0)
        order.append(u)
        
        # Duyệt lân cận theo thứ tự chỉ số tăng dần (chuẩn giải tay)
        neighbors = sorted([v for v, w in adj.get(u, [])])
        for v in neighbors:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                queue.append(v)
                tree_edges.append((u, v))

        if record_trace:
            trace_table.append({
                "step": len(order),
                "u": u,
                "queue": list(queue),
                "visited": list(visited)
            })
            
    return order, tree_edges, trace_table


def dfs(adj, n, start):
    """Duyệt theo chiều sâu (DFS). Trả về: (order, tree_edges, trace_table). Chi tiết: 3_traversal.md"""
    visited = [False] * n
    order = []
    tree_edges = []
    trace_table = []

    def dfs_visit(u):
        visited[u] = True
        order.append(u)

        trace_table.append({
            "step": len(order),
            "u": u,
            "queue": [],
            "visited": list(visited)
        })

        # Duyệt lân cận theo thứ tự chỉ số tăng dần
        neighbors = sorted([v for v, w in adj.get(u, [])])
        for v in neighbors:
            if not visited[v]:
                tree_edges.append((u, v))
                dfs_visit(v)

    dfs_visit(start)
    return order, tree_edges, trace_table

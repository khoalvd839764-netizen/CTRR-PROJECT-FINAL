# -*- coding: utf-8 -*-

def bfs(adj, n, start, end=None, record_trace=True):
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

        if end is not None and u == end:
            if record_trace:
                trace_table.append({
                    "step": len(order),
                    "u": u,
                    "queue": list(queue),
                    "visited": list(visited)
                })
            break

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

    if end is not None:
        path = []
        if visited[end]:
            curr = end
            while curr != -1:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
        return order, tree_edges, trace_table, path

    return order, tree_edges, trace_table


def bfs_path(adj, n, start, end, record_trace=True):
    order, tree_edges, trace_table, path = bfs(adj, n, start, end=end, record_trace=record_trace)
    return path, order, tree_edges, trace_table


def dfs(adj, n, start, end=None):
    visited = [False] * n
    parent = [-1] * n
    order = []
    tree_edges = []
    trace_table = []
    found = False

    def dfs_visit(u):
        nonlocal found
        visited[u] = True
        order.append(u)

        trace_table.append({
            "step": len(order),
            "u": u,
            "queue": [],
            "visited": list(visited)
        })

        if end is not None and u == end:
            found = True
            return

        neighbors = sorted([v for v, w in adj.get(u, [])])
        for v in neighbors:
            if not visited[v]:
                parent[v] = u
                tree_edges.append((u, v))
                dfs_visit(v)
                if found:
                    return

    dfs_visit(start)

    if end is not None:
        path = []
        if visited[end]:
            curr = end
            while curr != -1:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
        return order, tree_edges, trace_table, path

    return order, tree_edges, trace_table


def dfs_path(adj, n, start, end):
    order, tree_edges, trace_table, path = dfs(adj, n, start, end=end)
    return path, order, tree_edges, trace_table

# -*- coding: utf-8 -*-

def dijkstra(adj, n, start, end=None):
    dist = [float('inf')] * n
    visited = [False] * n
    parent = [-1] * n
    dist[start] = 0
    trace = []

    for step in range(n):
        u = -1
        min_dist = float('inf')
        
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

        for v, w in adj.get(u, []):
            if not visited[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u

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
    dist = [float('inf')] * n
    parent = [-1] * n
    dist[start] = 0
    trace = []

    formatted_edges = []
    for e in edges:
        u, v = e[0], e[1]
        w = e[2] if len(e) >= 3 else 1
        formatted_edges.append((u, v, w))
        if not directed:
            formatted_edges.append((v, u, w))

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

    has_neg = False
    for u, v, w in formatted_edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            has_neg = True
            break

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

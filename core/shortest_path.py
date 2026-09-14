# -*- coding: utf-8 -*-

def dijkstra(adj, n, start, end=None):
    # dist[i]: khoảng cách ngắn nhất từ start tới i (tạm biết được)
    dist = [float('inf')] * n
    visited = [False] * n   # đỉnh đã chốt (không sửa dist nữa)
    parent = [-1] * n       # để truy lại đường đi
    dist[start] = 0
    trace = []

    for step in range(n):
        # chọn đỉnh chưa chốt có dist nhỏ nhất -> tư tưởng greedy của Dijkstra
        u = -1
        min_dist = float('inf')
        for i in range(n):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i

        if u == -1 or dist[u] == float('inf'):
            break  # không còn đỉnh nào tới được nữa

        visited[u] = True
        trace.append({"step": step + 1, "u": u, "dist": list(dist), "parent": list(parent)})

        if end is not None and u == end:
            break  # chỉ cần tới end thì dừng sớm

        # relax: qua u có rẻ hơn không thì cập nhật
        for v, w in adj.get(u, []):
            if not visited[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u

    # truy ngược parent để dựng đường đi
    path = None
    if end is not None and dist[end] != float('inf'):
        cur, path = end, []
        while cur != -1:
            path.append(cur)
            cur = parent[cur]
        path.reverse()

    return {"dist": dist, "parent": parent, "path": path,
            "cost": dist[end] if end is not None and dist[end] != float('inf') else None,
            "trace": trace}


def bellman_ford(edges, n, start, directed=False, end=None):
    # Không greedy, cứ relax hết mọi cạnh, lặp n-1 lần -> chịu được cạnh âm
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
            formatted_edges.append((v, u, w))  # vô hướng thì thêm chiều ngược

    for i in range(n - 1):
        changed = False
        for u, v, w in formatted_edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
        trace.append(list(dist))
        if not changed:
            break  # ổn định sớm thì dừng luôn

    # relax thêm 1 lần nữa (lần n) mà vẫn giảm được -> có chu trình âm
    has_neg = False
    for u, v, w in formatted_edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            has_neg = True
            break

    path = None
    if end is not None and not has_neg and dist[end] != float('inf'):
        cur, path = end, []
        while cur != -1:
            path.append(cur)
            cur = parent[cur]
        path.reverse()

    return {"dist": dist, "parent": parent, "path": path,
            "cost": dist[end] if end is not None and dist[end] != float('inf') else None,
            "has_negative_cycle": has_neg, "trace": trace}

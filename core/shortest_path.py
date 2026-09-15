# -*- coding: utf-8 -*-

def dijkstra(adj, n, start, end=None):
    dist = [float('inf')] * n      # khoảng cách ngắn nhất từ start tới từng đỉnh
    visited = [False] * n          # đỉnh nào đã chốt xong rồi
    parent = [-1] * n              # để truy vết đường đi sau này
    dist[start] = 0
    trace = []
 
    for step in range(n):
        u = -1
        min_dist = float('inf')
 
        # tìm đỉnh chưa chốt có dist nhỏ nhất
        for i in range(n):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i
 
        # không còn đỉnh nào tới được nữa thì dừng
        if u == -1 or dist[u] == float('inf'):
            break
 
        visited[u] = True  # chốt đỉnh u, từ đây dist[u] không đổi nữa
        trace.append({
            "step": step + 1,
            "u": u,
            "dist": list(dist),      # copy ra, không copy thì các bước trace giống nhau hết
            "parent": list(parent)
        })
 
        if end is not None and u == end:
            break  # đã tới đích thì khỏi làm tiếp
 
        # relax: xem đi qua u tới các đỉnh kề v có ngắn hơn không
        for v, w in adj.get(u, []):
            if not visited[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
 
    # truy vết đường đi từ end ngược về start rồi đảo lại
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
 
    # chuẩn hoá cạnh: thêm trọng số mặc định = 1, nếu vô hướng thì thêm cả 2 chiều
    formatted_edges = []
    for e in edges:
        u, v = e[0], e[1]
        w = e[2] if len(e) >= 3 else 1
        formatted_edges.append((u, v, w))
        if not directed:
            formatted_edges.append((v, u, w))
 
    # lặp n-1 lần vì đường ngắn nhất (không chu trình âm) đi qua tối đa n-1 cạnh
    for i in range(n - 1):
        changed = False
        for u, v, w in formatted_edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
 
        trace.append(list(dist))
        if not changed:
            break  # không đổi gì nữa thì dừng sớm cho nhanh
 
    # lặp thêm 1 lần: nếu vẫn còn relax được nghĩa là có chu trình âm
    has_neg = False
    for u, v, w in formatted_edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            has_neg = True
            break
 
    # có chu trình âm thì không có đường ngắn nhất thật sự nên không truy vết
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
 

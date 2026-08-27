def bfs(adj, n, start):
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

        neighbors = sorted([v for v, w in adj.get(u, [])])
        for v in neighbors:
            if not visited[v]:
                visited [v] = True
                parent [v] = u
                queue.append(v)
                tree_edges.append((u, v))

        trace_table.append({
            "step": len(order),
            "u": u,
            "queue": list(queue),
            "visited": list(visited)
        })
    return order, tree_edges, trace_table

def dfs(adj, n, start):
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

        neighbors = sorted([v for v, w in adj.get(u, [])])
        for v in neighbors:
            if not visited[v]:
                tree_edges.append((u, v))
                dfs_visit(v)

    dfs_visit(start)
    return order, tree_edges, trace_table

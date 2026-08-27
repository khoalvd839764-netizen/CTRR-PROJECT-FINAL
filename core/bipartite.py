def check_bipartite(adj, n):
    color = [0] * n
    parent = [-1] * n

    def extract_odd_cycle(u, v):
        path_u = []
        curr = u
        while curr != -1:
            path_u.append(curr)
            curr = parent[curr]

        path_v = []
        curr = v
        while curr != -1:
            path_v.append(curr)
            curr = parent[curr]

        path_u.reverse()
        path_v.reverse()

        i = 0
        while i < len(path_u) and i < len(path_v) and path_u[i] == path_v[i]:
            i += 1

        odd_cycle = []
        for j in range(len(path_u) - 1, i - 1, -1):
            odd_cycle.append(path_u[j])
        for j in range(len(path_v) - 1, i, -1):
            odd_cycle.append(path_v[j])

        return odd_cycle

    for start in range(n):
        if color[start] == 0:
            color[start] = 1
            queue = [start]

            while queue:
                u = queue.pop(0)

                for v, w in adj.get(u, []):
                    if color[v] == 0:
                        color[v] = -color[u]
                        parent[v] = u
                        queue.append(v)
                    elif color[v] == color[u]:
                        odd_cycle = extract_odd_cycle(u, v)
                        return {"is_bipartite": False, "odd_cycle": odd_cycle}

    v1 = [i for i in range(n) if color[i] == 1]
    v2 = [i for i in range(n) if color[i] == -1]

    colors = {i: ('red' if color[i] == 1 else 'blue') for i in range(n) if color[i] != 0}

    return {"is_bipartite": True, "v1": v1, "v2": v2, "colors": colors}
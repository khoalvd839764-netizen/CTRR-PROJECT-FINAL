# -*- coding: utf-8 -*-

def check_bipartite(adj, n):
    color = [0] * n
    parent = [-1] * n

    for start in range(n):
        if color[start] != 0:
            continue

        color[start] = 1
        queue = [start]
        
        while len(queue) > 0:
            u = queue.pop(0)

            for v, *w in adj.get(u, []):
                if color[v] == 0: 
                    color[v] = -color[u]
                    parent[v] = u 
                    queue.append(v)
                elif color[v] == color[u]:
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

                    lca = -1
                    set_v = set(path_v)
                    for node in path_u:
                        if node in set_v:
                            lca = node
                            break

                    cycle_u = []
                    for node in path_u:
                        cycle_u.append(node)
                        if node == lca:
                            break

                    cycle_v = []
                    for node in path_v:
                        if node == lca:
                            break
                        cycle_v.append(node)

                    odd_cycle = cycle_u + cycle_v[::-1]

                    return {
                        "is_bipartite": False,
                        "odd_cycle": odd_cycle,
                        "colors": None
                    }

    v1 = [i for i in range(n) if color[i] == 1]
    v2 = [i for i in range(n) if color[i] == -1]

    color_map = {i: ("red" if color[i] == 1 else "blue") for i in range(n)}

    return {
        "is_bipartite": True,
        "v1": v1,
        "v2": v2,
        "colors": color_map
    }

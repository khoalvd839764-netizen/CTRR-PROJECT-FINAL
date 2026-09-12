# -*- coding: utf-8 -*-
"""Kiểm tra Đồ thị Hai phía (2-Coloring BFS) & Trích xuất chu trình lẻ. Chi tiết: core/chu_thich_thuat_toan/4_bipartite.md"""

def check_bipartite(adj, n):
    """Kiểm tra đồ thị hai phía bằng tô 2 màu (1 và -1). Chi tiết: 4_bipartite.md"""
    color = [0] * n
    parent = [-1] * n
    # Duyệt qua các thành phần liên thông
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
                    # Xung đột màu: Trích xuất chu trình lẻ thông qua Tổ tiên chung gần nhất (LCA)
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

                    # Tìm điểm giao nhau đầu tiên (LCA)
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

                    # Chu trình lẻ hoàn chỉnh: u -> ... -> LCA -> ... -> v -> u
                    odd_cycle = cycle_u + cycle_v[::-1]

                    return {
                        "is_bipartite": False,
                        "odd_cycle": odd_cycle,
                        "colors": None
                    }

    # Đồ thị hai phía: phân hoạch 2 tập đỉnh V1, V2
    v1 = [i for i in range(n) if color[i] == 1]
    v2 = [i for i in range(n) if color[i] == -1]

    color_map = {i: ("red" if color[i] == 1 else "blue") for i in range(n)}

    return {
        "is_bipartite": True,
        "v1": v1,
        "v2": v2,
        "colors": color_map
    }

def check_bipartite(adj, n): # ta quy định 1 là đỏ -1 là xanh 0 là chưa tô 
    color = [0] * n  # tạo mảng quản lí duyệt 
    parent = [-1] * n # lưu đỉnh vết cha 

    # duyệt các đỉnh nếu có đỉnh chưa tô màu thì tô màu đỏ thêm queue
    for start in range(n):
        if color[start] != 0:
            continue

        color[start] = 1
        queue = [start]
    # nếu queue đang có phần tử thì chạy 
        while len(queue) > 0:
            u = queue.pop(0) # lấy cái vừa được đẩy vào ra

            for v, *w in adj.get(u, []):  # lấy ds cạnh kề với u ra
                if color[v] == 0: # nếu chưa cso màu thì 
                    color[v] = -color[u]  # đổi màu v cha đỏ con xanh cha xanh con đỏ
                    parent[v] = u 
                    queue.append(v)
                elif color[v] == color[u]:
                    # Phát hiện mâu thuẫn màu -> Trích xuất chu trình lẻ
                    path_u = []
                    curr = u
                    while curr != -1:
                        path_u.append(curr)
                        curr = parent[curr]

                    path_v = [] # lưu đỉnh từ u về đỉnh gốc
                    curr = v # tạo con trỏ v 
                    while curr != -1:
                        path_v.append(curr)
                        curr = parent[curr]

                    # Tìm tổ tiên chung gần nhất (LCA)
                    lca = -1
                    set_v = set(path_v)
                    for node in path_u:
                        if node in set_v:
                            lca = node
                            break

                    # Xây dựng chu trình lẻ
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

    color_map = {}
    for i in range(n):
        color_map[i] = "red" if color[i] == 1 else "blue"

    return {
        "is_bipartite": True,
        "v1": v1,
        "v2": v2,
        "colors": color_map
    }

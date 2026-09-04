# =============================================================================
# THUẬT TOÁN ĐỒ THỊ HAI PHÍA (BIPARTITE GRAPH)
# =============================================================================
# Kiểm tra xem đồ thị có phải Bipartite (2-colorable) hay không.
# Ứng dụng: Lập trình phân 2 vùng độc lập (Khô/Ướt) để tránh robot kéo giẻ lau ướt lên sàn gỗ.

def check_bipartite(adj, n):
    """
    Sử dụng BFS để tô màu đỉnh (Coloring).
    Quy định: 1 (Màu đỏ / Khô), -1 (Màu xanh / Ướt), 0 (Chưa tô).
    Trả về True nếu chia được 2 tập độc lập (không mâu thuẫn).
    Nếu False, trả về cả 'chu trình lẻ' (odd cycle) gây ra mâu thuẫn.
    """
    color = [0] * n        # Mảng quản lý trạng thái tô màu
    parent = [-1] * n      # Lưu vết để trích xuất chu trình lẻ khi có lỗi

    # Vòng lặp bên ngoài đảm bảo quét cả các thành phần liên thông rời rạc
    for start in range(n):
        if color[start] != 0:
            continue

        color[start] = 1   # Chọn màu khởi đầu là 1
        queue = [start]
        
        while len(queue) > 0:
            u = queue.pop(0)

            # Duyệt các đỉnh v kề với đỉnh u
            for v, *w in adj.get(u, []):
                if color[v] == 0: 
                    # Nếu chưa tô màu -> Tô màu ĐỐI NGHỊCH với cha nó (1 -> -1 hoặc -1 -> 1)
                    color[v] = -color[u]
                    parent[v] = u 
                    queue.append(v)
                elif color[v] == color[u]:
                    # PHÁT HIỆN LỖI (Mâu thuẫn màu) -> Đồ thị không phải 2 phía
                    # Trích xuất chu trình lẻ bằng thuật toán tìm Tổ tiên chung gần nhất (LCA)
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

                    # Tìm tổ tiên chung gần nhất (Lowest Common Ancestor - LCA)
                    lca = -1
                    set_v = set(path_v)
                    for node in path_u:
                        if node in set_v:
                            lca = node
                            break

                    # Xây dựng chu trình lẻ hoàn chỉnh
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

    # Nếu chạy hết mà không có mâu thuẫn -> Hợp lệ!
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

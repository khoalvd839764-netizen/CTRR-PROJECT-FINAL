# -*- coding: utf-8 -*-
"""
Module: core/bipartite.py
Mục đích: Kiểm tra tính chất 2 phía (Bipartite Graph) của đồ thị vô hướng:
  - Sử dụng thuật toán tô 2 màu (2-Coloring) bằng duyệt BFS.
  - Nếu đồ thị 2 phía: Phân hoạch tập đỉnh thành 2 tập độc lập V1 (màu đỏ) và V2 (màu xanh).
  - Nếu không 2 phía: Tìm và chỉ ra một chu trình có độ dài lẻ (Odd Cycle) làm chứng chỉ bác bỏ.
"""

def check_bipartite(adj, n):
    """
    Kiểm tra đồ thị có phải là đồ thị 2 phía hay không.
    
    Thuật toán:
    - Sử dụng 2 màu đại diện bằng số nguyên: +1 (Đỏ) và -1 (Xanh). 0 nghĩa là chưa tô.
    - Duyệt qua tất cả các thành phần liên thông bằng BFS.
    - Với mỗi đỉnh u đang xét, mọi đỉnh kề v:
        + Nếu chưa tô: tô màu đối lập (color[v] = -color[u]) và đưa vào queue.
        + Nếu đã tô cùng màu (color[v] == color[u]): đồ thị chứa chu trình lẻ -> KHÔNG 2 PHÍA.
        + Thuật toán sẽ tìm tổ tiên chung gần nhất (LCA) của u và v trong cây BFS để dựng chu trình lẻ.
    
    Tham số:
        adj: Danh sách kề dạng dict {u: [(v, w), ...]}
        n: Số lượng đỉnh
        
    Trả về dict:
        - is_bipartite: True / False
        - Nếu True: kèm "v1" (tập đỉnh màu 1), "v2" (tập đỉnh màu -1), "colors" (bản đồ màu để vẽ)
        - Nếu False: kèm "odd_cycle" (danh sách đỉnh tạo chu trình lẻ), "colors": None
    """
    # color[i]: 0 = chưa tô, 1 = nhóm 1 (đỏ), -1 = nhóm 2 (xanh)
    color = [0] * n
    # parent[i]: lưu đỉnh cha trong cây BFS để truy vết chu trình
    parent = [-1] * n

    # Duyệt qua từng đỉnh để xử lý cả đồ thị có nhiều thành phần liên thông
    for start in range(n):
        if color[start] != 0:
            continue  # Đỉnh này đã thuộc thành phần liên thông được xét trước đó

        # Khởi tạo đỉnh bắt đầu của thành phần này với màu 1
        color[start] = 1
        queue = [start]
        
        while len(queue) > 0:
            u = queue.pop(0)

            # Xét tất cả đỉnh kề v của đỉnh u
            for v, *w in adj.get(u, []):
                if color[v] == 0: 
                    # Đỉnh v chưa được tô màu -> tô màu ngược lại với đỉnh u
                    color[v] = -color[u]
                    parent[v] = u 
                    queue.append(v)
                elif color[v] == color[u]:
                    # XUNG ĐỘT MÀU: Hai đỉnh kề nhau có cùng màu -> Không phải đồ thị 2 phía!
                    # Tái tạo chu trình lẻ bằng cách tìm Tổ tiên chung gần nhất (LCA)
                    
                    # 1. Truy vết đường đi từ u ngược về gốc cây BFS
                    path_u = []
                    curr = u
                    while curr != -1:
                        path_u.append(curr)
                        curr = parent[curr]

                    # 2. Truy vết đường đi từ v ngược về gốc cây BFS
                    path_v = []
                    curr = v
                    while curr != -1:
                        path_v.append(curr)
                        curr = parent[curr]

                    # 3. Tìm đỉnh tổ tiên chung đầu tiên (LCA) giữa path_u và path_v
                    lca = -1
                    set_v = set(path_v)
                    for node in path_u:
                        if node in set_v:
                            lca = node
                            break

                    # 4. Trích xuất nhánh từ u lên đến LCA
                    cycle_u = []
                    for node in path_u:
                        cycle_u.append(node)
                        if node == lca:
                            break

                    # 5. Trích xuất nhánh từ v lên đến đỉnh con ngay dưới LCA
                    cycle_v = []
                    for node in path_v:
                        if node == lca:
                            break
                        cycle_v.append(node)

                    # 6. Ghép thành chu trình lẻ hoàn chỉnh: u -> ... -> LCA -> ... -> v -> (cạnh u-v)
                    odd_cycle = cycle_u + cycle_v[::-1]

                    return {
                        "is_bipartite": False,
                        "odd_cycle": odd_cycle,
                        "colors": None
                    }

    # Nếu tô màu thành công tất cả đỉnh mà không có xung đột -> Đồ thị 2 phía
    v1 = [i for i in range(n) if color[i] == 1]
    v2 = [i for i in range(n) if color[i] == -1]

    color_map = {i: ("red" if color[i] == 1 else "blue") for i in range(n)}

    return {
        "is_bipartite": True,
        "v1": v1,
        "v2": v2,
        "colors": color_map
    }

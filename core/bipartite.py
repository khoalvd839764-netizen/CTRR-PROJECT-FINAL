# -*- coding: utf-8 -*-
"""
Module: core/bipartite.py
Kiểm tra Đồ thị Hai phía (Bipartite Graph) bằng Thuật toán Tô 2 màu (2-Coloring BFS).

Nguyên lý Toán học Rời rạc:
  - Định lý König: Một đồ thị là đồ thị hai phía KHI VÀ CHỈ KHI nó KHÔNG chứa chu trình có độ dài lẻ (Odd Cycle).
  - Nếu đồ thị có thể tô bằng 2 màu (Đỏ = 1, Xanh = -1) sao cho không có 2 đỉnh kề nào cùng màu,
    đồ thị đó là hai phía. Hai tập đỉnh V1 và V2 tương ứng với hai màu này.
  - ĐẶC BIỆT (Code khó): Nếu phát hiện 2 đỉnh kề nhau có cùng màu (xung đột màu),
    thuật toán sử dụng phương pháp tìm Tổ tiên chung gần nhất (LCA - Lowest Common Ancestor)
    để trích xuất chính xác Chu trình lẻ (Odd Cycle) làm bằng chứng toán học phản bác.
"""

def check_bipartite(adj, n):
    """
    Kiểm tra đồ thị có phải hai phía hay không bằng phương pháp tô 2 màu (BFS).
    
    Quy ước màu:
      - 0: Đỉnh chưa được xét / chưa tô màu.
      - 1: Màu Đỏ (Tập V1).
      - -1: Màu Xanh (Tập V2).
      
    Trả về Dict:
      - Nếu True: {"is_bipartite": True, "v1": [...], "v2": [...], "colors": {node: 'red'/'blue'}}
      - Nếu False: {"is_bipartite": False, "odd_cycle": [...], "colors": None}
    """
    color = [0] * n        # Mảng lưu trạng thái màu của từng đỉnh: 0, 1, hoặc -1
    parent = [-1] * n      # Mảng lưu đỉnh cha trong cây BFS để phục hồi chu trình lẻ

    # Vòng lặp ngoài duyệt từ 0 đến n-1:
    # Bắt buộc phải có để xử lý các đồ thị không liên thông (gồm nhiều thành phần liên thông rời nhau)
    for start in range(n):
        if color[start] != 0:
            continue

        # Gán màu khởi đầu là 1 cho đỉnh gốc của thành phần liên thông hiện tại
        color[start] = 1
        queue = [start]
        
        while len(queue) > 0:
            u = queue.pop(0)

            # Duyệt qua tất cả các đỉnh v kề với u
            for v, *w in adj.get(u, []):
                if color[v] == 0: 
                    # Đỉnh v chưa được tô màu:
                    # Gán màu NGƯỢC LẠI với đỉnh cha u (nếu u màu 1 thì v màu -1, và ngược lại)
                    color[v] = -color[u]
                    parent[v] = u 
                    queue.append(v)
                elif color[v] == color[u]:
                    # =========================================================================
                    # PHÁT HIỆN XUNG ĐỘT MÀU! (CODE KHÓ: TRÍCH XUẤT CHU TRÌNH LẺ)
                    # Hai đỉnh kề nhau u và v lại có CÙNG MÀU -> Chắc chắn tồn tại chu trình lẻ.
                    # Ta truy ngược từ u và v về gốc cây BFS để tìm Tổ tiên chung gần nhất (LCA).
                    # =========================================================================
                    
                    # Bước A: Lần ngược đường đi từ u về gốc cây BFS
                    path_u = []
                    curr = u
                    while curr != -1:
                        path_u.append(curr)
                        curr = parent[curr]

                    # Bước B: Lần ngược đường đi từ v về gốc cây BFS
                    path_v = []
                    curr = v
                    while curr != -1:
                        path_v.append(curr)
                        curr = parent[curr]

                    # Bước C: Tìm điểm giao nhau đầu tiên giữa 2 đường đi (chính là LCA)
                    lca = -1
                    set_v = set(path_v)
                    for node in path_u:
                        if node in set_v:
                            lca = node
                            break

                    # Bước D: Ghép nhánh từ u lên LCA và nhánh từ LCA xuống v để tạo thành chu trình
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

                    # Chu trình hoàn chỉnh: u -> ... -> LCA -> ... -> v -> u
                    odd_cycle = cycle_u + cycle_v[::-1]

                    return {
                        "is_bipartite": False,
                        "odd_cycle": odd_cycle,
                        "colors": None
                    }

    # Nếu duyệt qua toàn bộ đồ thị mà không phát sinh xung đột màu -> Đồ thị là Hai phía!
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

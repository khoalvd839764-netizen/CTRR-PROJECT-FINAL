# -*- coding: utf-8 -*-
r"""
Module: core/shortest_path.py
Cài đặt 2 thuật toán tìm đường đi ngắn nhất cốt lõi trong Toán Rời Rạc & CTRR:
  1. Thuật toán Dijkstra:
     - Áp dụng cho đồ thị có trọng số KHÔNG ÂM ($w \ge 0$).
     - Chiến lược Tham lam (Greedy Choice) với độ phức tạp $O(V^2)$.
     - Xuất bảng ma trận bước lặp (Bảng vết đối chiếu bài giải tay).
  2. Thuật toán Bellman-Ford:
     - Xử lý được đồ thị có trọng số ÂM ($w < 0$).
     - Lặp Relaxation $n-1$ lần qua toàn bộ cạnh.
     - Lặp lần thứ $n$ để phát hiện Chu trình âm (Negative Cycle Detection).
"""

def dijkstra(adj, n, start, end=None):
    """
    Thuật toán Dijkstra tìm đường đi ngắn nhất từ đỉnh `start`.
    
    Nguyên lý hoạt động (Toán Rời Rạc):
      1. Khởi tạo nhãn khoảng cách dist[start] = 0, tất cả các đỉnh khác = +inf.
      2. Tại mỗi bước, chọn đỉnh u* CHƯA THĂM có dist[u*] nhỏ nhất (Chốt nhãn cố định vĩnh viễn).
      3. Thực hiện thao tác Nới lỏng (Relaxation) cho tất cả các đỉnh kề v của u*:
         Nếu dist[u*] + w(u*, v) < dist[v] thì:
             dist[v] = dist[u*] + w(u*, v)
             parent[v] = u*
      4. Lặp lại cho đến khi chốt đủ n đỉnh hoặc đến được đỉnh đích `end`.
    
    Tham số:
      - adj: Danh sách kề dạng {u: [(v, w), ...]}
      - n: Tổng số đỉnh
      - start: Đỉnh nguồn
      - end: Đỉnh đích (tùy chọn, nếu None sẽ tính khoảng cách tới tất cả các đỉnh)
      
    Trả về Dict:
      - dist: Mảng khoảng cách ngắn nhất từ start
      - parent: Mảng đỉnh cha phục vụ truy vết
      - path: Lộ trình từ start -> end (nếu có end)
      - cost: Chi phí đường đi ngắn nhất
      - trace: Bảng vết từng bước lặp để sinh ma trận giải tay
    """
    dist = [float('inf')] * n   # dist[i]: Khoảng cách ngắn nhất hiện thời từ start đến đỉnh i
    visited = [False] * n       # visited[i] = True nghĩa là nhãn dist[i] đã được chốt tối ưu tuyệt đối
    parent = [-1] * n           # parent[i]: Lưu đỉnh đi trước i trên đường đi ngắn nhất
    dist[start] = 0             # Khoảng cách từ đỉnh xuất phát tới chính nó bằng 0
    trace = []

    for step in range(n):
        u = -1
        min_dist = float('inf')
        
        # ---------------------------------------------------------------------
        # BƯỚC 1: LỰA CHỌN THAM LAM (GREEDY CHOICE)
        # Quét tìm đỉnh u chưa thăm có dist[u] nhỏ nhất
        # ---------------------------------------------------------------------
        for i in range(n):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i

        # Nếu không còn đỉnh nào có thể tới được (đồ thị không liên thông), dừng sớm
        if u == -1 or dist[u] == float('inf'):
            break

        # Chốt đỉnh u (Khoảng cách từ start tới u chính thức đạt giá trị tối ưu)
        visited[u] = True
        
        # Ghi nhận trạng thái bảng vết tại bước lặp hiện tại
        trace.append({
            "step": step + 1,
            "u": u,
            "dist": list(dist),
            "parent": list(parent)
        })

        # Nếu đã chốt xong đỉnh đích end -> Có thể dừng sớm không cần duyệt các đỉnh còn lại
        if end is not None and u == end:
            break

        # ---------------------------------------------------------------------
        # BƯỚC 2: NỚI LỎNG CẠNH (RELAXATION)
        # Quét các đỉnh kề v của u xem đi qua u có rút ngắn quãng đường tới v hay không
        # ---------------------------------------------------------------------
        for v, w in adj.get(u, []):
            if not visited[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w  # Cập nhật nhãn khoảng cách tốt hơn
                parent[v] = u          # Ghi nhớ đường đi ngắn nhất qua u

    # -------------------------------------------------------------------------
    # BƯỚC 3: TRUY VẾT LỘ TRÌNH (PATH RECONSTRUCTION)
    # Lần ngược mảng parent từ đỉnh đích end về đỉnh nguồn start
    # -------------------------------------------------------------------------
    path = None
    if end is not None:
        if dist[end] != float('inf'):
            cur = end
            path = []
            while cur != -1:
                path.append(cur)
                cur = parent[cur]
            path.reverse()  # Đảo ngược danh sách để được thứ tự từ start đến end

    return {
        "dist": dist,
        "parent": parent,
        "path": path,
        "cost": dist[end] if end is not None and dist[end] != float('inf') else None,
        "trace": trace
    }


def bellman_ford(edges, n, start, directed=False, end=None):
    """
    Thuật toán Bellman-Ford tìm đường đi ngắn nhất và phát hiện Chu trình âm.
    
    Nguyên lý Toán học Rời rạc:
      - Trong đồ thị n đỉnh không có chu trình âm, đường đi đơn ngắn nhất qua tối đa n-1 cạnh.
      - Do đó, lặp n-1 vòng qua TẤT CẢ các cạnh chắc chắn sẽ tìm được khoảng cách ngắn nhất.
      - VÒNG LẶP THỨ n (Code khó): Nếu sau n-1 vòng mà vẫn còn bất kỳ cạnh (u, v) nào
        thỏa mãn dist[u] + w < dist[v], điều này CHỨNG MINH đồ thị chứa Chu trình âm!
        (Vì đi vòng quanh chu trình này khoảng cách sẽ giảm vô tận về -inf).
    """
    dist = [float('inf')] * n
    parent = [-1] * n
    dist[start] = 0
    trace = []

    # Chuẩn hóa danh sách cạnh thành bộ ba (u, v, w)
    # Nếu là đồ thị vô hướng, nhân đôi thành 2 cung có hướng (u->v) và (v->u)
    formatted_edges = []
    for e in edges:
        u, v = e[0], e[1]
        w = e[2] if len(e) >= 3 else 1
        formatted_edges.append((u, v, w))
        if not directed:
            formatted_edges.append((v, u, w))

    # -------------------------------------------------------------------------
    # BƯỚC 1: LẶP ĐÚNG n-1 VÒNG RELAXATION TRÊN TOÀN BỘ CẠNH
    # -------------------------------------------------------------------------
    for i in range(n - 1):
        changed = False
        for u, v, w in formatted_edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
                
        trace.append(list(dist))
        # Tối ưu hóa: Nếu qua 1 vòng mà không có khoảng cách nào giảm thêm -> Thuật toán đã hội tụ sớm
        if not changed:
            break

    # -------------------------------------------------------------------------
    # BƯỚC 2: PHÁT HIỆN CHU TRÌNH ÂM (VÒNG THỨ n)
    # -------------------------------------------------------------------------
    has_neg = False
    for u, v, w in formatted_edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            has_neg = True  # Khoảng cách vẫn còn giảm được -> Phát hiện Chu trình âm!
            break

    # -------------------------------------------------------------------------
    # BƯỚC 3: TRUY VẾT ĐƯỜNG ĐI (Nếu không bị chu trình âm làm sai lệch)
    # -------------------------------------------------------------------------
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

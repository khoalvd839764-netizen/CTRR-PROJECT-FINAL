# -*- coding: utf-8 -*-
"""
Module: core/shortest_path.py
Mục đích: Tìm đường đi ngắn nhất trên đồ thị có trọng số:
  - Dijkstra: Thuật toán tham lam cho đồ thị có trọng số không âm (w >= 0).
  - Bellman-Ford: Thuật toán nới lỏng cạnh (Relaxation) cho đồ thị có trọng số bất kỳ (cho phép w < 0),
    có khả năng phát hiện chu trình âm (Negative Cycle).
"""

def dijkstra(adj, n, start, end=None):
    """
    Thuật toán Dijkstra tìm đường đi ngắn nhất từ 1 nguồn (Single Source Shortest Path).
    
    Nguyên lý:
    - Thuật toán tham lam (Greedy): Ở mỗi bước, chọn đỉnh u chưa thăm có khoảng cách ước tính
      nhỏ nhất từ đỉnh start, cố định nhãn khoảng cách này (đã tối ưu).
    - Sau đó duyệt các đỉnh kề v của u để thực hiện phép nới lỏng cạnh (Relaxation):
      Nếu dist[u] + w < dist[v] thì cập nhật dist[v] = dist[u] + w.
      
    Tham số:
        adj: Danh sách kề dạng dict {u: [(v, w), ...]}
        n: Số lượng đỉnh
        start: Đỉnh nguồn
        end: Đỉnh đích (tùy chọn, dừng sớm nếu đã tìm thấy)
        
    Trả về dict:
        - dist: Mảng khoảng cách ngắn nhất từ start đến mọi đỉnh
        - parent: Mảng đỉnh cha phục vụ truy vết đường đi
        - path: Danh sách đỉnh trên đường đi từ start đến end (nếu có end)
        - cost: Chi phí đường đi từ start đến end
        - trace: Bảng lưu vết trạng thái qua từng bước chọn đỉnh
    """
    # Khởi tạo mảng khoảng cách ban đầu: vô cùng (inf), riêng đỉnh start = 0
    dist = [float('inf')] * n
    visited = [False] * n   # Đánh dấu đỉnh đã chốt khoảng cách ngắn nhất
    parent = [-1] * n       # Đỉnh đi trước trong đường đi ngắn nhất
    dist[start] = 0
    trace = []              # Lưu vết các bước thực thi

    for step in range(n):
        u = -1
        min_dist = float('inf')
        
        # BƯỚC THAM LAM: Tìm đỉnh u chưa thăm có khoảng cách nhỏ nhất
        for i in range(n):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i

        # Nếu không tìm thấy đỉnh nào hợp lệ hoặc khoảng cách vô cùng -> các đỉnh còn lại không liên thông
        if u == -1 or dist[u] == float('inf'):
            break

        # Đánh dấu u đã chốt nhãn tối ưu
        visited[u] = True
        trace.append({
            "step": step + 1,
            "u": u,
            "dist": list(dist),
            "parent": list(parent)
        }) 

        # Nếu đã đạt đến đỉnh đích end, có thể dừng thuật toán sớm
        if end is not None and u == end:
            break

        # BƯỚC NỚI LỎNG (RELAXATION): Cập nhật khoảng cách tới các đỉnh kề của u
        for v, w in adj.get(u, []):
            if not visited[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u

    # Truy vết đường đi ngắn nhất từ end về start thông qua mảng parent
    path = None
    if end is not None:
        if dist[end] != float('inf'):
            cur = end
            path = []
            while cur != -1:
                path.append(cur)
                cur = parent[cur]
            path.reverse()  # Đảo ngược để có lộ trình từ start -> end

    return {
        "dist": dist,
        "parent": parent,
        "path": path,
        "cost": dist[end] if end is not None and dist[end] != float('inf') else None,
        "trace": trace
    }


def bellman_ford(edges, n, start, directed=False, end=None):
    """
    Thuật toán Bellman-Ford tìm đường đi ngắn nhất và phát hiện chu trình âm.
    
    Nguyên lý:
    - Lặp lại phép nới lỏng (Relaxation) trên toàn bộ danh sách cạnh (V - 1) lần.
    - Đường đi ngắn nhất không chứa chu trình âm có tối đa (V - 1) cạnh.
    - Tại vòng lặp thứ V, nếu vẫn có cạnh tiếp tục nới lỏng được -> Đồ thị chứa CHU TRÌNH ÂM.
    
    Tham số:
        edges: Danh sách cạnh [(u, v, w), ...] hoặc [(u, v), ...]
        n: Số lượng đỉnh
        start: Đỉnh nguồn
        directed: True nếu là đồ thị có hướng, False nếu vô hướng
        end: Đỉnh đích (tùy chọn)
        
    Trả về dict:
        - dist: Mảng khoảng cách ngắn nhất
        - parent: Mảng đỉnh cha
        - path: Lộ trình đường đi từ start đến end
        - cost: Chi phí tới đỉnh end
        - has_negative_cycle: True nếu phát hiện chu trình âm
        - trace: Lưu lại mảng dist sau mỗi vòng lặp nới lỏng
    """
    dist = [float('inf')] * n
    parent = [-1] * n
    dist[start] = 0
    trace = []

    # Chuẩn hóa danh sách cạnh: chuyển về dạng (u, v, w)
    # Nếu là đồ thị vô hướng, mỗi cạnh (u, v) tương đương 2 cạnh có hướng (u, v) và (v, u)
    formatted_edges = []
    for e in edges:
        u, v = e[0], e[1]
        w = e[2] if len(e) >= 3 else 1
        formatted_edges.append((u, v, w))
        if not directed:
            formatted_edges.append((v, u, w))

    # Lặp n - 1 vòng: Nới lỏng tất cả các cạnh
    for i in range(n - 1):
        changed = False
        for u, v, w in formatted_edges:
            # Nếu u đã tới được và đi qua u đến v cho chi phí nhỏ hơn dist[v] hiện tại
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
                
        trace.append(list(dist))
        # Tối ưu: Nếu một vòng không có cạnh nào được nới lỏng, dừng sớm vì đã tối ưu
        if not changed:
            break

    # KIỂM TRA CHU TRÌNH ÂM: Thực hiện thêm 1 vòng nới lỏng kiểm tra
    # Nếu vẫn còn cạnh nới lỏng được -> Tồn tại chu trình trọng số âm
    has_neg = False
    for u, v, w in formatted_edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            has_neg = True
            break

    # Truy vết đường đi nếu không có chu trình âm và có chỉ định đỉnh đích end
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

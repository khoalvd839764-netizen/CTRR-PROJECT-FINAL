# -*- coding: utf-8 -*-
r"""
Module: core/max_flow.py
Cài đặt Thuật toán Ford-Fulkerson (biến thể Edmonds-Karp) tìm Luồng cực đại và Lát cắt hẹp nhất.

Nguyên lý Toán học Rời rạc:
  - Mạng luồng $G = (V, E)$ là đồ thị có hướng với mỗi cung có dung lượng $c(u, v) \ge 0$,
    có đỉnh Nguồn (Source - S) phát sinh luồng và đỉnh Đích (Sink - T) tiếp nhận luồng.
  - Định lý Max-Flow Min-Cut: Giá trị luồng cực đại từ S đến T BẰNG ĐÚNG dung lượng của lát cắt hẹp nhất phân hoạch (S, T).
  - Biến thể Edmonds-Karp: Sử dụng BFS để luôn tìm đường tăng luồng có ÍT CẠNH NHẤT từ S đến T.
    Điều này giúp thuật toán luôn kết thúc trong thời gian $O(V \cdot E^2)$ và không bị rơi vào vòng lặp vô hạn.
"""
from collections import deque


def bfs_augmenting_path(residual, n, source, sink):
    """
    [CODE KHÓ]: Tìm Đường tăng luồng (Augmenting Path) ngắn nhất từ S đến T trên Đồ thị phần dư (Residual Graph).
    
    Quy tắc:
      - Chỉ đi qua cung (u, v) nếu dung lượng thặng dư residual[u][v] > 0.
      - Sử dụng BFS để tìm đường có ít số cạnh nhất.
      
    Trả về:
      - path: Lộ trình các đỉnh [S, ..., T]
      - parent: Mảng đỉnh cha phục vụ cập nhật luồng
      - (None, None) nếu không còn đường đi nào tới T.
    """
    visited = [False] * n
    parent = [-1] * n
    queue = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()
        if u == sink:
            # Đã tìm thấy đường đi tới đỉnh đích T -> Dừng tìm kiếm
            break
            
        for v in range(n):
            # Điều kiện quan trọng: Cung phải còn dung lượng thặng dư (residual > 0)
            if not visited[v] and residual[u][v] > 0:
                visited[v] = True
                parent[v] = u
                queue.append(v)

    if visited[sink]:
        # Tái tạo đường đi từ Sink về Source thông qua mảng parent
        path = []
        curr = sink
        while curr != -1:
            path.append(curr)
            curr = parent[curr]
        path.reverse()
        return path, parent
        
    return None, None


def ford_fulkerson(edges, n, source, sink):
    """
    Thuật toán Ford-Fulkerson (Edmonds-Karp) tìm Luồng cực đại và Lát cắt hẹp nhất.

    Tham số:
        edges: Danh sách cạnh dạng [(u, v, cap), ...] hoặc ma trận dung lượng n x n
        n: Số lượng đỉnh trong mạng luồng
        source: Đỉnh Nguồn (S)
        sink: Đỉnh Đích (T)

    Trả về:
        max_flow: Giá trị luồng cực đại (int / float)
        flow_matrix: Ma trận luồng thực tế flow[u][v] qua từng cung
        min_cut_edges: Danh sách các cung thuộc lát cắt hẹp nhất [(u, v, cap), ...]
        cut_sets: Phân hoạch hai tập đỉnh (S_set, T_set)
        trace_table: Bảng vết từng bước lặp tăng luồng
    """
    # -------------------------------------------------------------------------
    # 1. XÂY DỰNG MA TRẬN DUNG LƯỢNG (CAPACITY MATRIX)
    # -------------------------------------------------------------------------
    capacity = [[0] * n for _ in range(n)]

    if isinstance(edges, list) and len(edges) > 0 and isinstance(edges[0], (list, tuple)) and len(edges[0]) == n:
        for i in range(n):
            for j in range(n):
                capacity[i][j] = edges[i][j]
    else:
        for edge in edges:
            if len(edge) == 3:
                u, v, cap = edge
                capacity[u][v] += cap
            elif len(edge) == 2:
                u, v = edge
                capacity[u][v] += 1

    # -------------------------------------------------------------------------
    # 2. KHỞI TẠO ĐỒ THỊ PHẦN DƯ (RESIDUAL GRAPH)
    # Ban đầu chưa đẩy luồng, dung lượng thặng dư bằng đúng dung lượng ban đầu
    # -------------------------------------------------------------------------
    residual = [row[:] for row in capacity]
    max_flow = 0
    trace_table = []
    step = 0

    # -------------------------------------------------------------------------
    # 3. VÒNG LẶP TĂNG LUỒNG (EDMONDS-KARP BFS)
    # -------------------------------------------------------------------------
    while True:
        # Tìm đường tăng luồng trên đồ thị phần dư
        path, parent = bfs_augmenting_path(residual, n, source, sink)
        if path is None:
            # Không còn đường tăng luồng nào từ S đến T -> ĐÃ ĐẠT LUỒNG CỰC ĐẠI!
            break

        step += 1

        # [CODE KHÓ - BƯỚC 3.1]: TÌM NGHẼN CỔ CHAI (BOTTLENECK)
        # Dung lượng luồng có thể tăng thêm bị giới hạn bởi cung có dung lượng thặng dư nhỏ nhất trên đường đi
        bottleneck = float('inf')
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            bottleneck = min(bottleneck, residual[u][v])

        # [CODE KHÓ - BƯỚC 3.2]: CẬP NHẬT ĐỒ THỊ THẶNG DƯ (RESIDUAL UPDATE)
        # Điểm mấu chốt: Cung nghịch (v -> u) được tăng thêm lượng 'bottleneck'!
        # Cung nghịch này cho phép các bước sau có thể "hủy luồng" (redirect flow) đã đẩy sai hướng,
        # đảm bảo thuật toán đạt nghiệm tối ưu toàn cục.
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            residual[u][v] -= bottleneck  # Giảm dung lượng còn lại của chiều thuận
            residual[v][u] += bottleneck  # Tăng dung lượng thặng dư của chiều ngược

        max_flow += bottleneck

        trace_table.append({
            "step": step,
            "path": path,
            "bottleneck": bottleneck,
            "current_max_flow": max_flow
        })

    # -------------------------------------------------------------------------
    # 4. TÍNH MA TRẬN LUỒNG THỰC TẾ (FLOW MATRIX)
    # Luồng thực tế trên cung (u, v) = Dung lượng ban đầu - Dung lượng còn lại
    # -------------------------------------------------------------------------
    flow_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if capacity[i][j] > 0:
                flow_matrix[i][j] = max(0, capacity[i][j] - residual[i][j])

    # -------------------------------------------------------------------------
    # 5. [CODE KHÓ]: XÁC ĐỊNH LÁT CẮT HẸP NHẤT (MIN CUT) THEO ĐỊNH LÝ MAX-FLOW MIN-CUT
    # Trên đồ thị phần dư cuối cùng:
    # - Tập S_set: Tập tất cả các đỉnh CÒN ĐẾN ĐƯỢC từ đỉnh Source S (qua các cung có residual > 0).
    # - Tập T_set: Tập tất cả các đỉnh còn lại KHÔNG THỂ đến được từ Source S.
    # - Các cung ban đầu đi từ S_set sang T_set chính là các cung bão hòa thuộc Lát cắt hẹp nhất!
    # -------------------------------------------------------------------------
    visited_cut = [False] * n
    queue_cut = deque([source])
    visited_cut[source] = True

    while queue_cut:
        u = queue_cut.popleft()
        for v in range(n):
            if not visited_cut[v] and residual[u][v] > 0:
                visited_cut[v] = True
                queue_cut.append(v)

    S_set = {i for i in range(n) if visited_cut[i]}
    T_set = {i for i in range(n) if not visited_cut[i]}

    # Tập các cung thuộc lát cắt hẹp nhất: Cung gốc u -> v với u thuộc S_set và v thuộc T_set
    min_cut_edges = []
    min_cut_capacity = 0
    for u in S_set:
        for v in T_set:
            if capacity[u][v] > 0:
                min_cut_edges.append((u, v, capacity[u][v]))
                min_cut_capacity += capacity[u][v]

    return max_flow, flow_matrix, min_cut_edges, (S_set, T_set), trace_table

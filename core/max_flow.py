# -*- coding: utf-8 -*-
"""
Module: core/max_flow.py
Mục đích: Giải bài toán Luồng cực đại trong mạng (Maximum Network Flow)
          và Xác định Lát cắt hẹp nhất (Minimum Cut):
  - Thuật toán Ford-Fulkerson cài đặt biến thể Edmonds-Karp (tìm đường tăng luồng bằng BFS).
  - Tự động dựng Đồ thị thặng dư (Residual Graph), cập nhật luồng thuận và luồng nghịch.
  - Phân hoạch đồ thị thành 2 tập (S, T) của lát cắt nhỏ nhất theo Định lý Max-Flow Min-Cut.
"""
from collections import deque


def bfs_augmenting_path(residual, n, source, sink):
    """
    Tìm một đường tăng luồng (Augmenting Path) từ đỉnh phát (source) đến đỉnh thu (sink)
    trên đồ thị thặng dư bằng BFS (Biến thể Edmonds-Karp).
    
    Tham số:
        residual: Ma trận dung lượng thặng dư n x n
        n: Số lượng đỉnh
        source: Đỉnh phát
        sink: Đỉnh thu
        
    Trả về:
        (path, parent): Đường đi từ source -> sink và mảng truy vết đỉnh cha.
        Nếu không còn đường đi, trả về (None, None).
    """
    visited = [False] * n
    parent = [-1] * n
    queue = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()
        if u == sink:
            break
            
        # Tìm các đỉnh v kề với u mà sức chứa thặng dư còn lại residual[u][v] > 0
        for v in range(n):
            if not visited[v] and residual[u][v] > 0:
                visited[v] = True
                parent[v] = u
                queue.append(v)

    # Nếu đỉnh sink được thăm, truy vết đường đi từ sink ngược về source
    if visited[sink]:
        path = []
        curr = sink
        while curr != -1:
            path.append(curr)
            curr = parent[curr]
        path.reverse()  # Đảo chiều để có thứ tự source -> ... -> sink
        return path, parent
        
    return None, None


def ford_fulkerson(edges, n, source, sink):
    """
    Thuật toán Ford-Fulkerson (Edmonds-Karp) tìm luồng cực đại và lát cắt cực tiểu.
    
    Nguyên lý:
    1. Ban đầu luồng trên mọi cạnh bằng 0, đồ thị thặng dư = đồ thị dung lượng ban đầu.
    2. Lặp lại: Tìm một đường tăng luồng từ source đến sink (bằng BFS).
    3. Tìm giá trị dung lượng thặng dư nhỏ nhất trên đường đó (gọi là bottleneck).
    4. Cập nhật đồ thị thặng dư:
       - Cạnh thuận (u, v): residual[u][v] -= bottleneck
       - Cạnh nghịch (v, u): residual[v][u] += bottleneck (cho phép giảm luồng nếu sau này cần)
    5. Khi không còn đường tăng luồng nào:
       - Luồng hiện tại là Luồng Cực Đại (Max Flow).
       - Các đỉnh còn đến được từ source trên đồ thị thặng dư tạo thành tập S.
       - Các đỉnh còn lại tạo thành tập T.
       - Cặp (S, T) chính là Lát cắt hẹp nhất (Min Cut).
       
    Trả về:
        (max_flow, flow_matrix, min_cut_edges, (S_set, T_set), trace_table)
    """
    # Khởi tạo ma trận dung lượng capacity[u][v]
    capacity = [[0] * n for _ in range(n)]

    # Tiếp nhận dữ liệu đầu vào: dạng ma trận kề n x n hoặc danh sách cạnh (u, v, cap)
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

    # Ma trận dung lượng thặng dư (Residual Graph): ban đầu sao chép từ capacity
    residual = [row[:] for row in capacity]
    max_flow = 0
    trace_table = []
    step = 0

    # VÒNG LẶP CHÍNH: Tăng luồng liên tục cho đến khi không còn đường đi từ source đến sink
    while True:
        path, parent = bfs_augmenting_path(residual, n, source, sink)
        if path is None:
            break  # Không còn đường tăng luồng -> Kết thúc

        step += 1

        # Tìm độ rộng nút thắt cổ chai (bottleneck) trên đường tăng luồng
        bottleneck = float('inf')
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            bottleneck = min(bottleneck, residual[u][v])

        # Cập nhật mạng thặng dư: giảm dung lượng cạnh thuận, tăng dung lượng cạnh nghịch
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck

        # Tích lũy luồng vào tổng luồng cực đại
        max_flow += bottleneck
        trace_table.append({
            "step": step,
            "path": path,
            "bottleneck": bottleneck,
            "current_max_flow": max_flow
        })

    # Tính toán ma trận luồng thực tế qua từng cạnh: flow[u][v] = capacity[u][v] - residual[u][v]
    flow_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if capacity[i][j] > 0:
                flow_matrix[i][j] = max(0, capacity[i][j] - residual[i][j])

    # XÁC ĐỊNH LÁT CẮT HẸP NHẤT (MIN-CUT):
    # Duyệt BFS trên mạng thặng dư cuối cùng từ đỉnh source để tìm tập đỉnh S
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

    # Các cạnh đi từ tập S sang tập T trên đồ thị gốc chính là các cạnh của Min-Cut
    min_cut_edges = []
    for u in S_set:
        for v in T_set:
            if capacity[u][v] > 0:
                min_cut_edges.append((u, v, capacity[u][v]))

    return max_flow, flow_matrix, min_cut_edges, (S_set, T_set), trace_table

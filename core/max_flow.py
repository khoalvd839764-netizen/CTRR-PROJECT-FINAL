# =============================================================================
# THUẬT TOÁN LUỒNG CỰC ĐẠI & LÁT CẮT HẸP NHẤT (MAX FLOW / MIN CUT)
# =============================================================================
# Chứa thuật toán Ford-Fulkerson (dùng BFS - Edmonds-Karp) tìm luồng cực đại.
# Ứng dụng: Tính toán băng thông hút bụi tối đa của mạng lưới ống dẫn (g/min).
# Phát hiện điểm nghẽn (bottleneck) thông qua định lý Min Cut.

from collections import deque


def bfs_augmenting_path(residual, n, source, sink):
    """
    Tìm đường tăng luồng ngắn nhất từ source đến sink bằng BFS.
    Trả về mảng parent lưu vết đường đi, hoặc None nếu không còn đường.
    """
    visited = [False] * n
    parent = [-1] * n
    queue = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()
        if u == sink:
            break
        for v in range(n):
            # Chỉ đi qua cung còn dung lượng thặng dư > 0
            if not visited[v] and residual[u][v] > 0:
                visited[v] = True
                parent[v] = u
                queue.append(v)

    if visited[sink]:
        # Tái tạo đường đi từ source đến sink
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
        edges: danh sách cạnh dạng [(u, v, cap), ...] hoặc ma trận dung lượng n x n
        n: số đỉnh trong mạng luồng
        source: đỉnh Nguồn (S)
        sink: đỉnh Đích (T)

    Trả về:
        max_flow: giá trị luồng cực đại (int / float)
        flow_matrix: ma trận luồng thực tế flow[u][v] (n x n)
        min_cut_edges: danh sách các cung ban đầu thuộc lát cắt hẹp nhất [(u, v, cap), ...]
        cut_sets: tuple (S_set, T_set) phân hoạch 2 tập đỉnh
        trace_table: bảng vết từng bước lặp tăng luồng
    """
    # 1. Xây dựng ma trận dung lượng capacity[n][n]
    capacity = [[0] * n for _ in range(n)]

    if isinstance(edges, list) and len(edges) > 0 and isinstance(edges[0], (list, tuple)) and len(edges[0]) == n:
        # Nếu truyền vào là ma trận dung lượng n x n
        for i in range(n):
            for j in range(n):
                capacity[i][j] = edges[i][j]
    else:
        # Nếu truyền vào là danh sách cung [(u, v, cap), ...]
        for edge in edges:
            if len(edge) == 3:
                u, v, cap = edge
                capacity[u][v] += cap
            elif len(edge) == 2:
                u, v = edge
                capacity[u][v] += 1

    # 2. Khởi tạo ma trận luồng thặng dư residual = capacity
    residual = [row[:] for row in capacity]
    max_flow = 0
    trace_table = []
    step = 0

    # 3. Vòng lặp tăng luồng (Edmonds-Karp BFS)
    while True:
        path, parent = bfs_augmenting_path(residual, n, source, sink)
        if path is None:
            # Không còn đường tăng luồng nào từ source đến sink
            break

        step += 1

        # Tìm lượng tăng luồng nghẽn cổ chai (bottleneck)
        bottleneck = float('inf')
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            bottleneck = min(bottleneck, residual[u][v])

        # Cập nhật đồ thị thặng dư
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            residual[u][v] -= bottleneck  # Giảm dung lượng chiều xuôi
            residual[v][u] += bottleneck  # Tăng dung lượng chiều ngược

        max_flow += bottleneck

        trace_table.append({
            "step": step,
            "path": path,
            "bottleneck": bottleneck,
            "current_max_flow": max_flow
        })

    # 4. Tính ma trận luồng thực tế flow_matrix[u][v]
    flow_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if capacity[i][j] > 0:
                # Luồng thực tế = Dung lượng ban đầu - Dung lượng thặng dư còn lại
                flow_matrix[i][j] = max(0, capacity[i][j] - residual[i][j])

    # 5. Tìm Lát cắt hẹp nhất (Min Cut) qua BFS từ source trên đồ thị thặng dư
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

    # Các cung thuộc lát cắt hẹp nhất: Cung gốc (u -> v) với u in S và v in T
    min_cut_edges = []
    min_cut_capacity = 0
    for u in S_set:
        for v in T_set:
            if capacity[u][v] > 0:
                min_cut_edges.append((u, v, capacity[u][v]))
                min_cut_capacity += capacity[u][v]

    return max_flow, flow_matrix, min_cut_edges, (S_set, T_set), trace_table

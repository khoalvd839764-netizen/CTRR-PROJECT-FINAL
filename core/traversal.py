# =============================================================================
# THUẬT TOÁN DUYỆT ĐỒ THỊ (TRAVERSAL ALGORITHMS)
# =============================================================================
# Chứa các thuật toán nền tảng để duyệt qua các đỉnh của đồ thị:
# 1. BFS (Breadth-First Search - Duyệt theo chiều rộng)
# 2. DFS (Depth-First Search - Duyệt theo chiều sâu)

def bfs(adj, n, start, record_trace=True):
    """
    Duyệt đồ thị theo chiều rộng (BFS).
    Sử dụng hàng đợi (Queue) để duyệt theo từng tầng (level-by-level).
    Ứng dụng trong đồ án: Mô phỏng sóng Lidar quét loang rộng.
    """
    visited = [False] * n  # Mảng đánh dấu các đỉnh đã thăm
    parent = [-1] * n      # Mảng lưu vết đỉnh cha để truy xuất đường đi
    queue = [start]        # Hàng đợi (Queue) khởi tạo với đỉnh nguồn
    visited[start] = True

    order = []             # Danh sách lưu thứ tự các đỉnh đã duyệt
    tree_edges = []        # Danh sách các cạnh tạo thành cây BFS
    trace_table = []       # Bảng lịch sử lưu trạng thái qua từng bước

    while len(queue) > 0:
        u = queue.pop(0)   # Lấy đỉnh đầu tiên ra khỏi hàng đợi (FIFO)
        order.append(u)
        
        # Lấy danh sách các đỉnh kề với u, sắp xếp để duyệt có thứ tự
        neighbors = sorted([v for v, w in adj.get(u, [])])
        for v in neighbors:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                queue.append(v)            # Đẩy đỉnh mới vào cuối hàng đợi
                tree_edges.append((u, v))  # Lưu cạnh vào cây BFS

        if record_trace:
            trace_table.append({
                "step": len(order),
                "u": u,
                "queue": list(queue),
                "visited": list(visited)
            })
    return order, tree_edges, trace_table

def dfs(adj, n, start):
    """
    Duyệt đồ thị theo chiều sâu (DFS).
    Sử dụng Đệ quy (hoặc Stack) để đi sâu nhất có thể trước khi quay lui.
    Ứng dụng trong đồ án: Mô phỏng robot chạy bám tường đi vào ngóc ngách.
    """
    visited = [False] * n  # Mảng đánh dấu các đỉnh đã thăm
    order = []             # Danh sách lưu thứ tự các đỉnh đã duyệt
    tree_edges = []        # Danh sách các cạnh tạo thành cây DFS
    trace_table = []

    def dfs_visit(u):
        visited[u] = True
        order.append(u)

        trace_table.append({
            "step": len(order),
            "u": u,
            "queue": [],
            "visited": list(visited)
        })

        # Lấy các đỉnh kề của u
        neighbors = sorted([v for v, w in adj.get(u, [])])
        for v in neighbors:
            if not visited[v]:
                tree_edges.append((u, v))
                dfs_visit(v) # Gọi đệ quy đi sâu vào đỉnh v

    dfs_visit(start)
    return order, tree_edges, trace_table

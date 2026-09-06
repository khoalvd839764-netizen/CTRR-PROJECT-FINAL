# =============================================================================
# THUẬT TOÁN TÌM ĐƯỜNG ĐI NGẮN NHẤT (SHORTEST PATH ALGORITHMS)
# =============================================================================
# Chứa thuật toán Dijkstra (và Bellman-Ford) để tìm đường đi có chi phí thấp nhất.
# Ứng dụng: Dẫn đường cho Robot từ phòng bất kỳ trở về Trạm sạc an toàn.

def dijkstra(adj, n, start, end=None):
    """
    Thuật toán Dijkstra tìm đường đi ngắn nhất từ đỉnh 'start' đến các đỉnh còn lại.
    Chỉ áp dụng cho đồ thị có trọng số KHÔNG ÂM.
    Độ phức tạp hiện tại: O(V^2) (vì tìm min_dist thủ công, có thể nâng cấp bằng Min-Heap).
    """
    dist = [float('inf')] * n   # Mảng lưu khoảng cách nhỏ nhất từ start đến mỗi đỉnh
    visited = [False] * n       # Đánh dấu đỉnh đã chốt khoảng cách (không thay đổi nữa)
    parent = [-1] * n           # Lưu vết đỉnh cha để truy ngược đường đi
    dist[start] = 0             # Khoảng cách từ start đến chính nó luôn là 0
    trace = []

    for step in range(n):
        u = -1
        min_dist = float('inf')
        
        # Bước 1: Tìm đỉnh u chưa thăm có dist[u] nhỏ nhất (Greedy)
        for i in range(n):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i

        # Nếu không còn đỉnh nào với tới được, dừng sớm
        if u == -1 or dist[u] == float('inf'):
            break

        visited[u] = True       # Chốt đỉnh u (đường đi đến u lúc này đã là tối ưu)
        trace.append({
            "step": step + 1,
            "u": u,
            "dist": list(dist),
            "parent": list(parent)
        })

        # Bước 2: Relaxation (Cập nhật khoảng cách các đỉnh kề v của u)
        for v, w in adj.get(u, []):
            if not visited[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w  # Tìm được đường mới ngắn hơn!
                parent[v] = u          # Ghi nhớ đường đi qua u

    path = None
    if end is not None:
        if dist[end] != float('inf'):
            cur = end
            path = []
            # Truy ngược từ đích (end) về nguồn (start)
            while cur != -1:
                path.append(cur)
                cur = parent[cur]
            path.reverse() # Đảo ngược để có đường đi chuẩn từ start -> end

    return {
        "dist": dist,
        "parent": parent,
        "path": path,
        "cost": dist[end] if end is not None and dist[end] != float('inf') else None,
        "trace": trace
    }


def bellman_ford(edges, n, start, directed=False, end=None):
    """
    Thuật toán Bellman-Ford tìm đường đi ngắn nhất.
    Có khả năng xử lý đồ thị có trọng số ÂM và phát hiện CHU TRÌNH ÂM.
    Độ phức tạp O(V * E).
    """
    dist = [float('inf')] * n
    parent = [-1] * n
    dist[start] = 0
    trace = []

    # Xử lý đồ thị có hướng / vô hướng
    formatted_edges = []
    for e in edges:
        u, v = e[0], e[1]
        w = e[2] if len(e) >= 3 else 1
        formatted_edges.append((u, v, w))
        if not directed:
            formatted_edges.append((v, u, w))

    # Bước 1: Lặp lại quá trình Relaxation n-1 lần cho TẤT CẢ các cạnh
    for i in range(n - 1):
        changed = False
        for u, v, w in formatted_edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
        trace.append(list(dist))
        # Tối ưu: Nếu sau một vòng không có đỉnh nào cập nhật, dừng sớm
        if not changed:
            break

    # Bước 2: Kiểm tra Chu trình Âm (Lặp lần thứ n)
    has_neg = False
    for u, v, w in formatted_edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            has_neg = True  # Nếu vẫn còn cập nhật được -> Có chu trình âm!
            break

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

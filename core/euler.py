# =============================================================================
# THUẬT TOÁN ĐỒ THỊ EULER (EULERIAN PATH & CIRCUIT)
# =============================================================================
# Chứa thuật toán kiểm tra tính Euler, thuật toán Fleury và Hierholzer.
# Ứng dụng: Lập lịch dọn dẹp kỹ (Full Coverage) - Quét 100% các hành lang đúng 1 lần.

"""
Module: core/euler.py
Cài đặt thuật toán kiểm tra tính Euler, thuật toán Fleury (7.1)
và thuật toán Hierholzer (7.2) tìm Chu trình / Đường đi Euler.
"""
from collections import deque
from core.traversal import bfs


def check_eulerian(adj, n, directed=False):
    """
    Kiểm tra điều kiện tồn tại Chu trình Euler hoặc Đường đi Euler.
    """
    if directed:
        # 1. Đồ thị có hướng
        in_deg = [0] * n
        out_deg = [0] * n
        # tính bán bậc vào bật ra
        for u in range(n):
            for v, _ in adj.get(u, []):
                out_deg[u] += 1
                in_deg[v] += 1

        # Đỉnh bắt đầu duyệt liên thông
        start_bfs = next((u for u in range(n) if out_deg[u] > 0 or in_deg[u] > 0), None)
        if start_bfs is None:
            return True, True, 0, "Đồ thị rỗng (không có cạnh)."

        # Kiểm tra liên thông yếu (bỏ qua hướng của cung)
        visited = [False] * n
        queue = deque([start_bfs])
        visited[start_bfs] = True

        undir_adj = {u: set() for u in range(n)}
        for u in range(n):
            for v, _ in adj.get(u, []):
                undir_adj[u].add(v)
                undir_adj[v].add(u)

        while queue:
            u = queue.popleft()
            for v in undir_adj[u]:
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)

        for u in range(n):
            if (out_deg[u] > 0 or in_deg[u] > 0) and not visited[u]:
                return False, False, None, "Đồ thị không liên thông, không có Euler."

        start_nodes = []
        end_nodes = []
        equal_count = 0

        for u in range(n):
            if out_deg[u] == in_deg[u]:
                equal_count += 1
            elif out_deg[u] == in_deg[u] + 1:
                start_nodes.append(u)
            elif in_deg[u] == out_deg[u] + 1:
                end_nodes.append(u)
            else:
                return False, False, None, "Bán bậc vào và bán bậc ra không thỏa mãn Euler."

        if equal_count == n:
            start_node = next((u for u in range(n) if out_deg[u] > 0), 0)
            return True, True, start_node, "Đồ thị có Chu trình Euler (mọi đỉnh có bán bậc vào = bán bậc ra)."
        elif len(start_nodes) == 1 and len(end_nodes) == 1:
            return True, False, start_nodes[0], f"Đồ thị có Đường đi Euler (từ đỉnh {start_nodes[0]} đến đỉnh {end_nodes[0]})."
        else:
            return False, False, None, "Không tồn tại Chu trình hay Đường đi Euler."

    else:
        # 2. Đồ thị vô hướng
        deg = [len(adj.get(u, [])) for u in range(n)]  # lấy ra bậc của các đỉnh

        start_bfs = next((u for u in range(n) if deg[u] > 0), None)  # lấy đỉnh ra nếu bậc lớn 0
        if start_bfs is None:
            return True, True, 0, "Đồ thị rỗng (không có cạnh)."

        # Kiểm tra tính liên thông (tái sử dụng bfs tối ưu, không ghi bảng vết)
        reachable_nodes, _, _ = bfs(adj, n, start_bfs, record_trace=False)
        visited_set = set(reachable_nodes)

        for u in range(n):
            if deg[u] > 0 and u not in visited_set:
                return False, False, None, "Đồ thị không liên thông giữa các đỉnh có cạnh."

        odd_vertices = [u for u in range(n) if deg[u] % 2 != 0]
        odd_count = len(odd_vertices)

        if odd_count == 0:
            start_node = next((u for u in range(n) if deg[u] > 0), 0)
            return True, True, start_node, "Đồ thị có Chu trình Euler (tất cả các đỉnh đều có bậc chẵn)."
        elif odd_count == 2:
            return True, False, odd_vertices[0], f"Đồ thị có Đường đi Euler (xuất phát từ đỉnh bậc lẻ {odd_vertices[0]} hoặc {odd_vertices[1]})."
        else:
            return False, False, None, f"Không tồn tại Euler (đồ thị có {odd_count} đỉnh bậc lẻ, yêu cầu 0 hoặc 2)."


def is_bridge(u, v, adj_copy, n):
    """
    Kiểm tra cạnh (u, v) có phải là Cầu (Bridge) trong đồ thị vô hướng adj_copy hay không.
    Cạnh (u, v) là Cầu nếu sau khi xóa (u, v), v không còn đường đi đến u.
    """
    # Nếu u chỉ còn duy nhất 1 cạnh kề là v thì bắt buộc phải đi (coi như không chặn)
    if len(adj_copy.get(u, [])) <= 1:
        return False

    # 1. Đếm số đỉnh tới được từ u TRƯỚC KHI xóa cạnh (u, v) (tái sử dụng bfs)
    order_before, _, _ = bfs(adj_copy, n, u, record_trace=False)
    count_before = len(order_before)

    # 2. Tạm thời xóa cạnh (u, v)
    adj_copy[u] = [(k, w) for (k, w) in adj_copy[u] if k != v]
    adj_copy[v] = [(k, w) for (k, w) in adj_copy[v] if k != u]

    # 3. Đếm số đỉnh tới được từ u SAU KHI xóa cạnh (u, v) (tái sử dụng bfs)
    order_after, _, _ = bfs(adj_copy, n, u, record_trace=False)
    count_after = len(order_after)

    # 4. Khôi phục lại cạnh (u, v)
    adj_copy[u].append((v, 1))
    adj_copy[v].append((u, 1))

    # Nếu số đỉnh tới được sau khi xóa ít hơn -> (u, v) là Cầu (Bridge)
    return count_after < count_before


def fleury(adj, n, start=None, directed=False):
    """
    Thuật toán Fleury (Mục 7.1) tìm Chu trình / Đường đi Euler.
    Nguyên lý: Tuyệt đối không đi qua Cầu (Bridge) trừ khi không còn lựa chọn nào khác.
    """
    has_euler, is_circuit, default_start, msg = check_eulerian(adj, n, directed)
    if not has_euler:
        return [], [], []

    if start is None:
        start = default_start

    # Tạo bản sao sâu của danh sách kề
    adj_copy = {u: list(adj.get(u, [])) for u in range(n)}

    curr_node = start
    path = [curr_node]
    edges_order = []
    trace_table = []
    step = 0

    while True:
        neighbors = adj_copy.get(curr_node, [])
        if not neighbors:
            break

        # Chọn cạnh đi tiếp
        chosen_v = None
        chosen_w = 1
        reason = ""

        if len(neighbors) == 1:
            chosen_v, chosen_w = neighbors[0]
            reason = "Chỉ còn 1 cạnh duy nhất, bắt buộc đi"
        else:
            # Ưu tiên chọn cạnh KHÔNG phải là Cầu
            for v, w in neighbors:
                if not is_bridge(curr_node, v, adj_copy, n):
                    chosen_v, chosen_w = v, w
                    reason = f"Cạnh ({curr_node}, {v}) không phải là Cầu (Bridge)"
                    break

            if chosen_v is None:
                # Nếu tất cả các cạnh còn lại đều là Cầu -> Bắt buộc chọn cạnh đầu tiên
                chosen_v, chosen_w = neighbors[0]
                reason = "Mọi cạnh còn lại đều là Cầu, bắt buộc phải đi"

        # Xóa cạnh (curr_node, chosen_v) khỏi đồ thị
        adj_copy[curr_node] = [(k, w) for (k, w) in adj_copy[curr_node] if k != chosen_v]
        if not directed:
            adj_copy[chosen_v] = [(k, w) for (k, w) in adj_copy[chosen_v] if k != curr_node]

        step += 1
        edges_order.append((curr_node, chosen_v))
        path.append(chosen_v)

        trace_table.append({
            "step": step,
            "u": curr_node,
            "v": chosen_v,
            "reason": reason,
            "remaining_edges": sum(len(adj_copy[u]) for u in range(n)) // (1 if directed else 2)
        })

        curr_node = chosen_v

    return path, edges_order, trace_table


def hierholzer(adj, n, start=None, directed=False):
    """
    Thuật toán Hierholzer (Mục 7.2) tìm Chu trình / Đường đi Euler hiệu năng cao O(E).
    Nguyên lý: Dùng Stack đi sâu, khi gặp ngõ cụt đưa đỉnh vào kết quả, sau đó đảo ngược.
    """
    has_euler, is_circuit, default_start, msg = check_eulerian(adj, n, directed)
    if not has_euler:
        return [], [], []

    if start is None:
        start = default_start

    # Tạo bản sao danh sách kề
    adj_copy = {u: list(adj.get(u, [])) for u in range(n)}

    curr_path = [start]
    circuit = []
    trace_table = []
    step = 0

    while curr_path:
        u = curr_path[-1]

        if adj_copy.get(u, []):
            # Còn cạnh kề -> Đi tiếp sang đỉnh kề đầu tiên
            v, w = adj_copy[u][0]

            # Xóa cạnh (u, v)
            # Xóa MỘT cạnh (u, v)
            for i, (k, weight) in enumerate(adj_copy[u]):
                if k == v:
                    adj_copy[u].pop(i)
                    break
            if not directed:
                for i, (k, weight) in enumerate(adj_copy[v]):
                    if k == u:
                        adj_copy[v].pop(i)
                        break

            curr_path.append(v)
            step += 1

            trace_table.append({
                "step": step,
                "action": f"Đi từ {u} sang {v}",
                "stack": list(curr_path),
                "circuit": list(circuit)
            })
        else:
            # Ngõ cụt -> Lấy đỉnh ra khỏi Stack và đưa vào kết quả
            dead_end = curr_path.pop()
            circuit.append(dead_end)
            step += 1

            trace_table.append({
                "step": step,
                "action": f"Đỉnh {dead_end} hết cạnh -> Đưa vào Circuit",
                "stack": list(curr_path),
                "circuit": list(circuit)
            })

    # Đảo ngược circuit để được thứ tự đúng
    circuit.reverse()

    edges_order = []
    for i in range(len(circuit) - 1):
        edges_order.append((circuit[i], circuit[i + 1]))

    return circuit, edges_order, trace_table

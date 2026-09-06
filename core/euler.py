# -*- coding: utf-8 -*-
"""
Module: core/euler.py
Cài đặt thuật toán kiểm tra tính Euler, thuật toán Fleury (Mục 7.1)
và thuật toán Hierholzer (Mục 7.2) tìm Chu trình / Đường đi Euler.

Định lý Euler trong Toán Rời Rạc:
  1. Đồ thị vô hướng liên thông:
     - Có Chu trình Euler KHI VÀ CHỈ KHI mọi đỉnh đều có BẬC CHẴN (deg(v) % 2 == 0).
     - Có Đường đi Euler KHI VÀ CHỈ KHI có ĐÚNG 2 đỉnh bậc lẻ (xuất phát ở 1 đỉnh lẻ và kết thúc ở đỉnh lẻ còn lại).
  2. Đồ thị có hướng liên thông yếu:
     - Có Chu trình Euler KHI VÀ CHỈ KHI bán bậc vào = bán bậc ra tại mọi đỉnh (in_deg(v) == out_deg(v)).
     - Có Đường đi Euler KHI VÀ CHỈ KHI có đúng 1 đỉnh có out_deg = in_deg + 1 (đỉnh bắt đầu),
       đúng 1 đỉnh có in_deg = out_deg + 1 (đỉnh kết thúc), và mọi đỉnh khác có in_deg == out_deg.
"""
from collections import deque
from core.traversal import bfs


def check_eulerian(adj, n, directed=False):
    """
    Kiểm tra điều kiện cần và đủ để tồn tại Chu trình Euler hoặc Đường đi Euler.
    
    Trả về Tuple: (has_euler, is_circuit, start_node, message)
      - has_euler: True nếu tồn tại chu trình hoặc đường đi.
      - is_circuit: True nếu là Chu trình (bắt đầu và kết thúc cùng 1 đỉnh), False nếu là Đường đi.
      - start_node: Đỉnh xuất phát hợp lệ.
      - message: Diễn giải chi tiết lý do toán học.
    """
    if directed:
        # =====================================================================
        # 1. ĐỒ THỊ CÓ HƯỚNG
        # =====================================================================
        in_deg = [0] * n
        out_deg = [0] * n
        
        # Đếm bán bậc vào và bán bậc ra cho từng đỉnh
        for u in range(n):
            for v, _ in adj.get(u, []):
                out_deg[u] += 1
                in_deg[v] += 1

        # Tìm đỉnh đầu tiên có cạnh để kiểm tra tính liên thông
        start_bfs = next((u for u in range(n) if out_deg[u] > 0 or in_deg[u] > 0), None)
        if start_bfs is None:
            return True, True, 0, "Đồ thị rỗng (không có cạnh)."

        # Kiểm tra tính liên thông yếu (coi các cung có hướng như cạnh vô hướng)
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

        # Nếu có đỉnh nào có cạnh mà không tới được -> Không liên thông yếu
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
        # =====================================================================
        # 2. ĐỒ THỊ VÔ HƯỚNG
        # =====================================================================
        deg = [len(adj.get(u, [])) for u in range(n)]

        # Tìm đỉnh có bậc > 0 đầu tiên
        start_bfs = next((u for u in range(n) if deg[u] > 0), None)
        if start_bfs is None:
            return True, True, 0, "Đồ thị rỗng (không có cạnh)."

        # Kiểm tra tính liên thông giữa các đỉnh có bậc khác 0
        reachable_nodes, _, _ = bfs(adj, n, start_bfs, record_trace=False)
        visited_set = set(reachable_nodes)

        for u in range(n):
            if deg[u] > 0 and u not in visited_set:
                return False, False, None, "Đồ thị không liên thông giữa các đỉnh có cạnh."

        # Đếm các đỉnh có bậc lẻ
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
    [CODE KHÓ]: Kiểm tra cạnh (u, v) có phải là CẦU (Bridge) trong đồ thị vô hướng hay không.
    
    Định nghĩa Cầu:
      - Cạnh (u, v) là Cầu nếu sau khi bỏ cạnh (u, v), số thành phần liên thông của đồ thị tăng lên
        (tức là số đỉnh có thể đi tới từ u bị giảm đi).
        
    Thuật toán kiểm tra:
      1. Đếm số đỉnh tới được từ u bằng BFS trước khi xóa cạnh: count_before.
      2. Tạm thời loại bỏ cạnh (u, v) khỏi danh sách kề.
      3. Đếm lại số đỉnh tới được từ u bằng BFS sau khi xóa: count_after.
      4. Khôi phục lại cạnh (u, v).
      5. Nếu count_after < count_before -> Cạnh (u, v) là CẦU (Bridge).
    """
    # Nếu đỉnh u chỉ còn đúng 1 cạnh kề duy nhất là v, thì bắt buộc phải đi qua nó (không coi là vi phạm)
    if len(adj_copy.get(u, [])) <= 1:
        return False

    # 1. Đếm số đỉnh tới được từ u TRƯỚC KHI xóa cạnh (u, v)
    order_before, _, _ = bfs(adj_copy, n, u, record_trace=False)
    count_before = len(order_before)

    # 2. Tạm thời xóa cạnh (u, v)
    adj_copy[u] = [(k, w) for (k, w) in adj_copy[u] if k != v]
    adj_copy[v] = [(k, w) for (k, w) in adj_copy[v] if k != u]

    # 3. Đếm số đỉnh tới được từ u SAU KHI xóa cạnh (u, v)
    order_after, _, _ = bfs(adj_copy, n, u, record_trace=False)
    count_after = len(order_after)

    # 4. Khôi phục lại cạnh (u, v)
    adj_copy[u].append((v, 1))
    adj_copy[v].append((u, 1))

    # Nếu số lượng đỉnh liên thông bị sụt giảm -> Đây là Cạnh Cầu!
    return count_after < count_before


def fleury(adj, n, start=None, directed=False):
    """
    Thuật toán Fleury (Mục 7.1) tìm Chu trình / Đường đi Euler.
    
    Nguyên lý cốt lõi:
      - "Không bao giờ đi qua Cầu (Bridge) trừ khi không còn con đường nào khác!"
      - Tại mỗi đỉnh hiện tại:
        + Nếu chỉ có 1 cạnh duy nhất -> Bắt buộc đi.
        + Nếu có nhiều cạnh -> Ưu tiên chọn cạnh KHÔNG phải là Cầu.
        + Xóa cạnh vừa đi khỏi đồ thị và tiếp tục lặp lại.
        
    Độ phức tạp: O(E^2) do mỗi bước kiểm tra Cầu cần duyệt BFS.
    """
    has_euler, is_circuit, default_start, msg = check_eulerian(adj, n, directed)
    if not has_euler:
        return [], [], []

    if start is None:
        start = default_start

    # Tạo bản sao danh sách kề để thao tác xóa cạnh dần dần
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

        chosen_v = None
        chosen_w = 1
        reason = ""

        if len(neighbors) == 1:
            chosen_v, chosen_w = neighbors[0]
            reason = "Chỉ còn 1 cạnh duy nhất, bắt buộc đi"
        else:
            # Ưu tiên tìm cạnh KHÔNG phải là Cầu (Bridge)
            for v, w in neighbors:
                if not is_bridge(curr_node, v, adj_copy, n):
                    chosen_v, chosen_w = v, w
                    reason = f"Cạnh ({curr_node}, {v}) không phải là Cầu (Bridge)"
                    break

            if chosen_v is None:
                # Nếu tất cả các cạnh còn lại đều là Cầu -> Bắt buộc chọn cạnh đầu tiên
                chosen_v, chosen_w = neighbors[0]
                reason = "Mọi cạnh còn lại đều là Cầu, bắt buộc phải đi"

        # Xóa cạnh (curr_node, chosen_v) vừa đi qua khỏi đồ thị
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
    
    Nguyên lý hoạt động (Kỹ thuật ghép chu trình con):
      - Sử dụng cấu trúc Ngăn xếp (Stack) lưu đường đi tạm thời `curr_path`.
      - Từ đỉnh đỉnh stack:
        + Nếu u còn cạnh kề -> Lấy 1 cạnh kề (u, v), xóa cạnh khỏi đồ thị, đẩy v vào Stack.
        + Nếu u HẾT CẠNH KỀ (ngõ cụt của một chu trình con) -> Pop u ra khỏi Stack và đẩy vào `circuit`.
      - Khi Stack rỗng, toàn bộ đồ thị đã được duyệt xong.
      - ĐẢO NGƯỢC danh sách `circuit` để thu được thứ tự đường đi Euler đúng chuẩn.
    
    Độ phức tạp tối ưu: O(E) — Nhanh hơn vượt trội so với Fleury.
    """
    has_euler, is_circuit, default_start, msg = check_eulerian(adj, n, directed)
    if not has_euler:
        return [], [], []

    if start is None:
        start = default_start

    # Tạo bản sao danh sách kề
    adj_copy = {u: list(adj.get(u, [])) for u in range(n)}

    curr_path = [start]   # Stack theo dõi lộ trình hiện thời
    circuit = []          # Danh sách gom kết quả
    trace_table = []
    step = 0

    while curr_path:
        u = curr_path[-1]

        if adj_copy.get(u, []):
            # Còn cạnh kề: Đi tiếp sang đỉnh kề đầu tiên
            v, w = adj_copy[u][0]

            # Xóa 1 cạnh (u, v) khỏi đồ thị
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
            # Ngõ cụt: Đỉnh u đã dùng hết cạnh kề -> Đưa u vào kết quả circuit
            dead_end = curr_path.pop()
            circuit.append(dead_end)
            step += 1

            trace_table.append({
                "step": step,
                "action": f"Đỉnh {dead_end} hết cạnh -> Đưa vào Circuit",
                "stack": list(curr_path),
                "circuit": list(circuit)
            })

    # Đảo ngược danh sách circuit vì các đỉnh hoàn thành sau được đưa vào trước
    circuit.reverse()

    edges_order = []
    for i in range(len(circuit) - 1):
        edges_order.append((circuit[i], circuit[i + 1]))

    return circuit, edges_order, trace_table

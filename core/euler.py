# -*- coding: utf-8 -*-
"""
Module: core/euler.py
Mục đích: Xử lý bài toán Chu trình và Đường đi Euler trên cả đồ thị có hướng và vô hướng:
  - check_eulerian: Kiểm tra điều kiện tồn tại Euler (tính liên thông và tính chẵn/lẻ của bậc đỉnh).
  - is_bridge: Kiểm tra cạnh cầu (Bridge) phục vụ thuật toán Fleury.
  - fleury: Tìm chu trình/đường đi Euler bằng thuật toán Fleury (nguyên tắc không phá cầu).
  - hierholzer: Thuật toán Hierholzer tối ưu O(E) bằng cách ghép các chu trình con qua Stack.
"""
from collections import deque
from core.traversal import bfs


def check_eulerian(adj, n, directed=False):
    """
    Kiểm tra điều kiện cần và đủ để đồ thị có Chu trình hoặc Đường đi Euler.
    
    Điều kiện:
    1. Đồ thị vô hướng:
       - Các đỉnh có bậc > 0 phải thuộc cùng một thành phần liên thông.
       - Chu trình Euler: Tất cả các đỉnh đều có bậc chẵn (0 đỉnh bậc lẻ).
       - Đường đi Euler: Đúng 2 đỉnh có bậc lẻ (xuất phát từ 1 trong 2 đỉnh này).
    2. Đồ thị có hướng:
       - Liên thông yếu giữa các đỉnh có cạnh (bậc > 0).
       - Chu trình Euler: Mọi đỉnh đều có bán bậc vào = bán bậc ra (in_deg == out_deg).
       - Đường đi Euler: Đúng 1 đỉnh có out_deg = in_deg + 1 (đỉnh bắt đầu),
         đúng 1 đỉnh có in_deg = out_deg + 1 (đỉnh kết thúc), và mọi đỉnh khác in_deg == out_deg.
         
    Trả về tuple: (has_euler, is_circuit, start_node, message)
    """
    if directed:
        # --- XỬ LÝ ĐỒ THỊ CÓ HƯỚNG ---
        in_deg = [0] * n   # Bán bậc vào
        out_deg = [0] * n  # Bán bậc ra
        
        for u in range(n):
            for v, _ in adj.get(u, []):
                out_deg[u] += 1
                in_deg[v] += 1

        # Tìm đỉnh đầu tiên có cạnh để bắt đầu kiểm tra liên thông
        start_bfs = next((u for u in range(n) if out_deg[u] > 0 or in_deg[u] > 0), None)
        if start_bfs is None:
            return True, True, 0, "Đồ thị rỗng (không có cạnh)."

        # Kiểm tra tính liên thông yếu (Weakly Connected): bỏ qua hướng mũi tên
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

        # Mọi đỉnh có cạnh đều phải được thăm
        for u in range(n):
            if (out_deg[u] > 0 or in_deg[u] > 0) and not visited[u]:
                return False, False, None, "Đồ thị không liên thông, không có Euler."

        # Đánh giá cân bằng bán bậc vào và ra
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
        # --- XỬ LÝ ĐỒ THỊ VÔ HƯỚNG ---
        deg = [len(adj.get(u, [])) for u in range(n)]

        # Tìm đỉnh có cạnh đầu tiên
        start_bfs = next((u for u in range(n) if deg[u] > 0), None)
        if start_bfs is None:
            return True, True, 0, "Đồ thị rỗng (không có cạnh)."

        # Kiểm tra tính liên thông giữa các đỉnh có bậc > 0
        reachable_nodes, _, _ = bfs(adj, n, start_bfs, record_trace=False)
        visited_set = set(reachable_nodes)

        for u in range(n):
            if deg[u] > 0 and u not in visited_set:
                return False, False, None, "Đồ thị không liên thông giữa các đỉnh có cạnh."

        # Đếm số đỉnh bậc lẻ
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
    Kiểm tra cạnh (u, v) có phải là Cầu (Bridge) trong đồ thị hiện tại hay không.
    
    Nguyên tắc:
    - Một cạnh là Cầu nếu xóa nó đi làm tăng số thành phần liên thông
      (tức là giảm số lượng đỉnh có thể đến được từ đỉnh u).
    """
    if len(adj_copy.get(u, [])) <= 1:
        # Nếu u chỉ còn duy nhất 1 cạnh, bắt buộc phải đi nên không cần coi là cầu cấm đi
        return False

    # Đếm số đỉnh đến được từ u trước khi tạm xóa cạnh (u, v)
    order_before, _, _ = bfs(adj_copy, n, u, record_trace=False)
    count_before = len(order_before)

    # Tạm thời xóa cạnh (u, v)
    adj_copy[u] = [(k, w) for (k, w) in adj_copy[u] if k != v]
    adj_copy[v] = [(k, w) for (k, w) in adj_copy[v] if k != u]

    # Đếm số đỉnh đến được từ u sau khi xóa cạnh
    order_after, _, _ = bfs(adj_copy, n, u, record_trace=False)
    count_after = len(order_after)

    # Hoàn trả lại cạnh (u, v) vào đồ thị
    adj_copy[u].append((v, 1))
    adj_copy[v].append((u, 1))

    # Nếu số lượng đỉnh đến được giảm đi -> Cạnh (u, v) là CẦU
    return count_after < count_before


def fleury(adj, n, start=None, directed=False):
    """
    Thuật toán Fleury tìm Chu trình hoặc Đường đi Euler.
    
    Nguyên lý:
    - Bắt đầu từ đỉnh start hợp lệ (đỉnh bậc lẻ nếu có, hoặc đỉnh bất kỳ có cạnh).
    - Ở mỗi bước từ đỉnh hiện tại u, chọn đi qua cạnh kề (u, v):
      + Ưu tiên cạnh KHÔNG phải là Cầu.
      + Chỉ đi qua Cầu nếu không còn lựa chọn nào khác.
    - Xóa cạnh vừa đi qua và di chuyển đến v cho đến khi không còn cạnh nào.
    
    Trả về: (path, edges_order, trace_table)
    """
    has_euler, is_circuit, default_start, msg = check_eulerian(adj, n, directed)
    if not has_euler:
        return [], [], []

    if start is None:
        start = default_start

    # Bản sao danh sách kề để xóa dần cạnh trong quá trình đi
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

        # Nếu chỉ còn đúng 1 cạnh kề, không còn cách nào khác ngoài việc đi cạnh này
        if len(neighbors) == 1:
            chosen_v, chosen_w = neighbors[0]
            reason = "Chỉ còn 1 cạnh duy nhất, bắt buộc đi"
        else:
            # Tìm cạnh kề không phải là Cầu
            for v, w in neighbors:
                if not is_bridge(curr_node, v, adj_copy, n):
                    chosen_v, chosen_w = v, w
                    reason = f"Cạnh ({curr_node}, {v}) không phải là Cầu (Bridge)"
                    break

            # Nếu tất cả các cạnh kề đều là Cầu, buộc phải chọn 1 cạnh
            if chosen_v is None:
                chosen_v, chosen_w = neighbors[0]
                reason = "Mọi cạnh còn lại đều là Cầu, bắt buộc phải đi"

        # Xóa cạnh đã đi khỏi danh sách kề
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
    Thuật toán Hierholzer tìm Chu trình hoặc Đường đi Euler với độ phức tạp tối ưu O(E).
    
    Nguyên lý:
    - Sử dụng một Ngăn xếp (Stack - curr_path) để theo dõi hành trình:
      1. Từ đỉnh u trên đỉnh Stack, nếu u còn cạnh kề:
         Chọn cạnh (u, v), xóa cạnh khỏi đồ thị và đẩy v vào Stack.
      2. Nếu u không còn cạnh kề nào (đã duyệt hết chu trình con / ngõ cụt):
         Lấy u ra khỏi Stack và đưa vào danh sách kết quả (circuit).
    - Cuối cùng, đảo ngược danh sách circuit ta nhận được lộ trình Euler hoàn chỉnh.
    
    Trả về: (circuit, edges_order, trace_table)
    """
    has_euler, is_circuit, default_start, msg = check_eulerian(adj, n, directed)
    if not has_euler:
        return [], [], []

    if start is None:
        start = default_start

    adj_copy = {u: list(adj.get(u, [])) for u in range(n)}
    curr_path = [start]  # Ngăn xếp chứa hành trình hiện tại
    circuit = []        # Mảng lưu kết quả ngược
    trace_table = []
    step = 0

    while curr_path:
        u = curr_path[-1]

        # Nếu u còn cạnh kề chưa đi
        if adj_copy.get(u, []):
            v, w = adj_copy[u][0]
            # Xóa cạnh (u, v) khỏi danh sách kề của u
            for i, (k, weight) in enumerate(adj_copy[u]):
                if k == v:
                    adj_copy[u].pop(i)
                    break
            # Nếu vô hướng, xóa chiều ngược lại (v, u)
            if not directed:
                for i, (k, weight) in enumerate(adj_copy[v]):
                    if k == u:
                        adj_copy[v].pop(i)
                        break

            # Đẩy đỉnh kế tiếp vào stack
            curr_path.append(v)
            step += 1
            trace_table.append({
                "step": step,
                "action": f"Đi từ {u} sang {v}",
                "stack": list(curr_path),
                "circuit": list(circuit)
            })
        else:
            # Ngõ cụt: u không còn cạnh nào để đi tiếp
            # Pop u ra khỏi stack và ghi nhận vào chu trình hoàn tất
            dead_end = curr_path.pop()
            circuit.append(dead_end)
            step += 1
            trace_table.append({
                "step": step,
                "action": f"Đỉnh {dead_end} hết cạnh -> Đưa vào Circuit",
                "stack": list(curr_path),
                "circuit": list(circuit)
            })

    # Đảo ngược circuit để được thứ tự duyệt từ đỉnh bắt đầu đến kết thúc
    circuit.reverse()
    edges_order = [(circuit[i], circuit[i + 1]) for i in range(len(circuit) - 1)]

    return circuit, edges_order, trace_table

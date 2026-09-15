# -*- coding: utf-8 -*-
"""
Module: core/traversal.py
Mục đích: Cung cấp các thuật toán duyệt đồ thị cơ bản:
  - BFS (Breadth-First Search - Duyệt theo chiều rộng)
  - DFS (Depth-First Search - Duyệt theo chiều sâu)
  - Tìm đường đi ngắn nhất không trọng số và xây dựng cây khung (Spanning Tree).
"""

def bfs(adj, n, start, end=None, record_trace=True):
    """
    Thuật toán duyệt theo chiều rộng (Breadth-First Search).
    - Sử dụng hàng đợi (Queue - FIFO) để mở rộng theo từng lớp/bán kính từ đỉnh start.
    - Tìm đường đi qua ít cạnh nhất giữa 2 đỉnh (với đồ thị không trọng số).
    
    Tham số:
        adj: Danh sách kề dạng dict {u: [(v, w), ...]}
        n: Số lượng đỉnh của đồ thị
        start: Đỉnh xuất phát
        end: Đỉnh đích cần tìm đường đi (None nếu muốn duyệt toàn bộ thành phần liên thông)
        record_trace: Có lưu lại từng bước duyệt để trực quan hóa/vẽ bảng bước không
        
    Trả về:
        Nếu end is None: (order, tree_edges, trace_table)
        Nếu end is not None: (order, tree_edges, trace_table, path)
    """
    # Khởi tạo mảng đánh dấu đỉnh đã thăm và mảng lưu đỉnh cha phục vụ truy vết
    visited = [False] * n
    parent = [-1] * n
    
    # Hàng đợi FIFO: đưa đỉnh xuất phát vào hàng đợi và đánh dấu đã thăm
    queue = [start]
    visited[start] = True

    order = []        # Thứ tự các đỉnh được duyệt qua
    tree_edges = []   # Các cạnh tạo nên cây khung BFS (BFS Spanning Tree)
    trace_table = []  # Bảng lưu vết trạng thái từng bước

    while len(queue) > 0:
        # Lấy đỉnh u ở đầu hàng đợi ra để duyệt
        u = queue.pop(0)
        order.append(u)

        # Nếu đã đến đỉnh đích cần tìm, dừng thuật toán sớm
        if end is not None and u == end:
            if record_trace:
                trace_table.append({
                    "step": len(order),
                    "u": u,
                    "queue": list(queue),
                    "visited": list(visited)
                })
            break

        # Sắp xếp các đỉnh kề theo thứ tự tăng dần để đảm bảo kết quả duyệt xác định
        neighbors = sorted([v for v, w in adj.get(u, [])])
        for v in neighbors:
            if not visited[v]:
                # Đánh dấu đã thăm ngay khi đẩy vào queue để tránh đẩy lặp đỉnh
                visited[v] = True
                parent[v] = u
                queue.append(v)
                tree_edges.append((u, v))  # (u, v) là cạnh thuộc cây khung

        # Ghi nhận trạng thái queue và visited sau bước duyệt đỉnh u
        if record_trace:
            trace_table.append({
                "step": len(order),
                "u": u,
                "queue": list(queue),
                "visited": list(visited)
            })

    # Nếu có chỉ định đỉnh đích end, tiến hành truy vết đường đi từ end ngược về start
    if end is not None:
        path = []
        if visited[end]:
            curr = end
            while curr != -1:
                path.append(curr)
                curr = parent[curr]
            path.reverse()  # Đảo ngược để có đường đi đúng từ start -> end
        return order, tree_edges, trace_table, path

    return order, tree_edges, trace_table


def bfs_path(adj, n, start, end, record_trace=True):
    """
    Tìm đường đi ngắn nhất từ start đến end bằng thuật toán BFS.
    Trả về: (path, order, tree_edges, trace_table)
    """
    order, tree_edges, trace_table, path = bfs(adj, n, start, end=end, record_trace=record_trace)
    return path, order, tree_edges, trace_table


def dfs(adj, n, start, end=None):
    """
    Thuật toán duyệt theo chiều sâu (Depth-First Search).
    - Sử dụng đệ quy (Call Stack - LIFO) để đi sâu nhất có thể theo từng nhánh trước khi quay lui (backtrack).
    
    Tham số:
        adj: Danh sách kề dạng dict {u: [(v, w), ...]}
        n: Số lượng đỉnh của đồ thị
        start: Đỉnh xuất phát
        end: Đỉnh đích (dừng ngay khi gặp nếu chỉ định)
        
    Trả về:
        Nếu end is None: (order, tree_edges, trace_table)
        Nếu end is not None: (order, tree_edges, trace_table, path)
    """
    visited = [False] * n
    parent = [-1] * n
    order = []        # Thứ tự các đỉnh duyệt DFS
    tree_edges = []   # Các cạnh của cây khung DFS
    trace_table = []  # Bảng lưu vết từng bước
    found = False     # Cờ báo hiệu đã tìm thấy đỉnh đích

    def dfs_visit(u):
        nonlocal found
        # Đánh dấu đỉnh u đã thăm và ghi nhận thứ tự
        visited[u] = True
        order.append(u)

        trace_table.append({
            "step": len(order),
            "u": u,
            "queue": [],
            "visited": list(visited)
        })

        # Nếu gặp đỉnh đích thì dừng đệ quy ngay lập tức
        if end is not None and u == end:
            found = True
            return

        # Sắp xếp đỉnh kề tăng dần để thứ tự duyệt luôn xác định
        neighbors = sorted([v for v, w in adj.get(u, [])])
        for v in neighbors:
            if not visited[v]:
                parent[v] = u
                tree_edges.append((u, v))  # Cạnh duyệt cây khung
                dfs_visit(v)               # Đệ quy đi sâu vào đỉnh v
                if found:                  # Nếu đã tìm thấy đích trong nhánh đệ quy, lập tức quay lui
                    return

    # Bắt đầu duyệt DFS từ đỉnh start
    dfs_visit(start)

    # Truy vết đường đi nếu có yêu cầu tìm đến đỉnh end
    if end is not None:
        path = []
        if visited[end]:
            curr = end
            while curr != -1:
                path.append(curr)
                curr = parent[curr]
            path.reverse()  # Đảo chiều để được đường đi start -> end
        return order, tree_edges, trace_table, path

    return order, tree_edges, trace_table


def dfs_path(adj, n, start, end):
    """
    Tìm đường đi từ start đến end bằng DFS.
    Trả về: (path, order, tree_edges, trace_table)
    """
    order, tree_edges, trace_table, path = dfs(adj, n, start, end=end)
    return path, order, tree_edges, trace_table

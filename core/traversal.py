# -*- coding: utf-8 -*-
"""
Module: core/traversal.py
Cài đặt 2 thuật toán duyệt đồ thị kinh điển của Lý thuyết đồ thị:
  1. BFS (Breadth-First Search - Duyệt theo chiều rộng)
  2. DFS (Depth-First Search - Duyệt theo chiều sâu)

Đặc tả đề bài CTRR:
  - Sinh thứ tự duyệt (Order).
  - Trích xuất tập các cạnh của Cây khung duyệt đồ thị (Tree Edges).
  - Tự động ghi nhận Bảng vết từng bước (Trace Table) để đối chiếu chính xác với kết quả giải tay của sinh viên.
  - Quy ước chuẩn mực: Các đỉnh lân cận luôn được duyệt theo thứ tự chỉ số tăng dần.
"""

def bfs(adj, n, start, record_trace=True):
    """
    Duyệt đồ thị theo chiều rộng (Breadth-First Search).
    
    Nguyên lý hoạt động:
      - Sử dụng cấu trúc hàng đợi FIFO (First-In, First-Out).
      - Xuất phát từ đỉnh nguồn `start`, duyệt qua tất cả các đỉnh cách nguồn 1 cạnh (tầng 1),
        sau đó đến các đỉnh cách 2 cạnh (tầng 2), và cứ thế loang dần ra ngoài.
    
    Tham số:
      - adj: Danh sách kề dạng dict {u: [(v, w), ...]}
      - n: Tổng số đỉnh của đồ thị
      - start: Đỉnh bắt đầu duyệt
      - record_trace: Cờ bật/tắt ghi bảng vết (tắt để tăng tốc khi dùng phụ trợ)
      
    Trả về:
      - order: Danh sách thứ tự các đỉnh được duyệt
      - tree_edges: Các cạnh tạo nên Cây khung BFS [(u, v), ...]
      - trace_table: Bảng theo dõi trạng thái hàng đợi và mảng visited tại từng bước
    """
    visited = [False] * n  # Mảng boolean đánh dấu đỉnh đã được khám phá
    parent = [-1] * n      # Mảng lưu đỉnh cha trong cây BFS
    queue = [start]        # Khởi tạo hàng đợi FIFO với đỉnh xuất phát
    visited[start] = True

    order = []             # Lưu chuỗi thứ tự duyệt
    tree_edges = []        # Lưu các cạnh cây duyệt BFS
    trace_table = []       # Bảng vết mô phỏng giải tay

    while len(queue) > 0:
        # Lấy đỉnh u ở đầu hàng đợi ra xử lý (FIFO)
        u = queue.pop(0)
        order.append(u)
        
        # Lấy các đỉnh kề v của u và SẮP XẾP TĂNG DẦN
        # (Lý do: Khi giải tay trên giấy thi, sinh viên luôn chọn đỉnh có số nhỏ trước)
        neighbors = sorted([v for v, w in adj.get(u, [])])
        for v in neighbors:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                queue.append(v)            # Đẩy đỉnh mới chưa thăm vào cuối hàng đợi
                tree_edges.append((u, v))  # Cạnh (u, v) được kết nạp vào cây khung BFS

        if record_trace:
            # Ghi lại trạng thái tại bước lặp hiện tại phục vụ hiển thị bảng vết
            trace_table.append({
                "step": len(order),
                "u": u,
                "queue": list(queue),
                "visited": list(visited)
            })
            
    return order, tree_edges, trace_table


def dfs(adj, n, start):
    """
    Duyệt đồ thị theo chiều sâu (Depth-First Search).
    
    Nguyên lý hoạt động:
      - Sử dụng ngăn xếp Call Stack (Đệ quy).
      - Từ đỉnh hiện tại, đi sâu nhất có thể theo một nhánh cho đến khi gặp ngõ cụt
        (không còn đỉnh kề chưa thăm), sau đó quay lui (Backtracking) để khám phá nhánh khác.
      
    Trả về:
      - order: Danh sách thứ tự các đỉnh được duyệt
      - tree_edges: Các cạnh tạo nên Cây khung DFS [(u, v), ...]
      - trace_table: Bảng vết từng bước duyệt
    """
    visited = [False] * n  # Đánh dấu đỉnh đã thăm
    order = []             # Thứ tự duyệt
    tree_edges = []        # Cạnh cây khung DFS
    trace_table = []

    def dfs_visit(u):
        """Hàm đệ quy duyệt nhánh sâu xuất phát từ đỉnh u."""
        visited[u] = True
        order.append(u)

        trace_table.append({
            "step": len(order),
            "u": u,
            "queue": [],
            "visited": list(visited)
        })

        # Lấy các đỉnh kề và sắp xếp tăng dần để đảm bảo kết quả trùng khớp giải tay
        neighbors = sorted([v for v, w in adj.get(u, [])])
        for v in neighbors:
            if not visited[v]:
                # Ghi nhận cạnh cây khung DFS trước khi đi sâu
                tree_edges.append((u, v))
                # Đi sâu vào đỉnh v bằng đệ quy
                dfs_visit(v)

    # Bắt đầu duyệt từ đỉnh xuất phát
    dfs_visit(start)
    return order, tree_edges, trace_table

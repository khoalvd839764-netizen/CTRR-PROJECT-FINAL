# -*- coding: utf-8 -*-
"""
Module: core/mst.py
Mục đích: Tìm Cây khung nhỏ nhất (Minimum Spanning Tree - MST) cho đồ thị vô hướng liên thông có trọng số:
  - Cấu trúc dữ liệu DSU (Disjoint Set Union) hỗ trợ kiểm tra chu trình O(alpha(V)).
  - Kruskal: Thuật toán tham lam trên tập cạnh (sắp xếp cạnh, dùng DSU tránh chu trình).
  - Prim: Thuật toán tham lam phát triển lát cắt (Cut Property), mở rộng dần cây khung từ 1 đỉnh.
"""

class DSU:
    """
    Cấu trúc dữ liệu các tập hợp rời nhau (Disjoint Set Union / Union-Find).
    - Tối ưu hóa bằng Kỹ thuật nén đường đi (Path Compression) và Hợp nhất theo hạng (Union by Rank).
    - Độ phức tạp thời gian gần như O(1) cho mỗi truy vấn.
    """
    def __init__(self, n):
        self.parent = list(range(n))  # Ban đầu mỗi phần tử là cha của chính nó
        self.rank = [0] * n           # Chiều cao ước tính của cây đại diện

    def find(self, i):
        """
        Tìm gốc đại diện của tập hợp chứa phần tử i.
        Áp dụng nén đường đi (Path Compression) trỏ trực tiếp nút con lên gốc.
        """
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        """
        Hợp nhất 2 tập hợp chứa i và j.
        Trả về True nếu gộp thành công (i và j ở 2 tập khác nhau).
        Trả về False nếu i và j đã cùng thuộc 1 tập (thêm cạnh này sẽ tạo chu trình).
        """
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i == root_j:
            return False  # Cùng gốc -> Đã liên thông -> Không chọn để tránh chu trình

        # Hợp nhất theo hạng: Gốc có rank nhỏ hơn sẽ làm con của gốc có rank lớn hơn
        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1
            
        return True


def kruskal(edges, n):
    """
    Thuật toán Kruskal xây dựng Cây khung nhỏ nhất (MST).
    
    Nguyên lý:
    1. Sắp xếp toàn bộ các cạnh của đồ thị theo thứ tự trọng số tăng dần.
    2. Duyệt qua từng cạnh: nếu cạnh nối 2 đỉnh thuộc 2 thành phần liên thông khác nhau
       (kiểm tra bằng DSU không tạo chu trình) thì kết nạp cạnh đó vào MST.
    3. Dừng lại khi MST đã có đủ (n - 1) cạnh hoặc duyệt hết danh sách cạnh.
    
    Tham số:
        edges: Danh sách cạnh [(u, v, w), ...]
        n: Số lượng đỉnh
        
    Trả về:
        (mst_edges, total_weight, trace_table)
    """
    # Bước 1: Sắp xếp các cạnh tăng dần theo trọng số w
    sorted_edges = sorted(edges, key=lambda x: x[2])
    dsu = DSU(n)
    mst_edges = []
    total_weight = 0
    trace_table = []

    # Bước 2: Lần lượt xét từng cạnh từ nhỏ nhất đến lớn nhất
    for (u, v, w) in sorted_edges:
        # Nếu gộp được (không tạo chu trình) -> CHỌN
        if dsu.union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w
            trace_table.append({
                "edge": (u, v),
                "weight": w,
                "action": "CHỌN",
                "current_mst_edges": len(mst_edges)
            })
        else:
            # Hai đỉnh đã cùng thành phần liên thông -> LOẠI để tránh chu trình
            trace_table.append({
                "edge": (u, v),
                "weight": w,
                "action": "LOẠI (TẠO CHU TRÌNH)"
            })

        # Cây khung luôn có đúng n - 1 cạnh, đủ thì dừng sớm
        if len(mst_edges) == n - 1:
            break
            
    return mst_edges, total_weight, trace_table


def prim(adj, n, start=0):
    """
    Thuật toán Prim xây dựng Cây khung nhỏ nhất (MST).
    
    Nguyên lý:
    - Bắt đầu từ 1 cây khung chỉ gồm đỉnh xuất phát (start).
    - Lặp (n - 1) lần: Tại mỗi bước, tìm cạnh nhẹ nhất nối giữa một đỉnh đã thuộc MST
      với một đỉnh chưa thuộc MST (vượt qua lát cắt / Cut Property).
    - Thêm đỉnh và cạnh đó vào cây khung, tiếp tục mở rộng.
    
    Tham số:
        adj: Danh sách kề {u: [(v, w), ...]}
        n: Số lượng đỉnh
        start: Đỉnh xuất phát (mặc định đỉnh 0)
        
    Trả về:
        (mst_edges, total_weight, trace_table)
    """
    visited = [False] * n
    visited[start] = True  # Đỉnh start bắt đầu trong cây khung

    mst_edges = []
    total_weight = 0
    trace_table = []

    # Cần n - 1 cạnh để kết nối n đỉnh
    for _ in range(n - 1):
        best_u, best_v, best_w = None, None, None

        # Quét tất cả các cạnh (u, v) đi từ đỉnh đã thăm u sang đỉnh chưa thăm v
        for u in range(n):
            if not visited[u]:
                continue
            for (v, w) in adj[u]:
                if not visited[v]:
                    # Tìm cạnh có trọng số w nhỏ nhất băng qua biên cây khung
                    if best_w is None or w < best_w:
                        best_u, best_v, best_w = u, v, w

        # Nếu không tìm thấy cạnh nào hợp lệ -> đồ thị không liên thông
        if best_v is None:
            break

        # Kết nạp đỉnh best_v và cạnh (best_u, best_v) vào MST
        visited[best_v] = True
        mst_edges.append((best_u, best_v, best_w))
        total_weight += best_w

        trace_table.append({
            "edge": (best_u, best_v),
            "weight": best_w,
            "current_mst_edges": len(mst_edges)
        })

    return mst_edges, total_weight, trace_table

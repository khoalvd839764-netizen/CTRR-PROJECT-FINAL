# -*- coding: utf-8 -*-
r"""
Module: core/mst.py
Cài đặt các thuật toán tìm Cây khung nhỏ nhất (Minimum Spanning Tree - MST):
  1. Cấu trúc dữ liệu Disjoint Set Union (DSU) với 2 kỹ thuật tối ưu kinh điển:
     - Nén đường đi (Path Compression)
     - Gộp theo hạng (Union by Rank)
  2. Thuật toán Kruskal (Mục 7.4): Tiếp cận toàn cục trên tập cạnh đã sắp xếp.
  3. Thuật toán Prim (Mục 7.3): Tiếp cận lát cắt (Cut Property) phát triển từ 1 đỉnh.

Nguyên lý Cây khung nhỏ nhất:
  - Cho đồ thị vô hướng liên thông $G = (V, E)$ có trọng số.
  - Cây khung là đồ thị con liên thông chứa TẤT CẢ $n$ đỉnh của $G$ và đúng $n-1$ cạnh, không có chu trình.
  - Cây khung nhỏ nhất là cây khung có tổng trọng số các cạnh là nhỏ nhất.
"""

class DSU:
    """
    Cấu trúc dữ liệu Disjoint Set Union (DSU / Tập hợp rời rạc).
    Phục vụ kiểm tra chu trình và quản lý các thành phần liên thông trong Kruskal.
    """
    def __init__(self, n):
        # Ban đầu mỗi đỉnh i là gốc của chính nó
        self.parent = list(range(n))
        # rank[i]: Chiều cao ước lượng của cây chứa đỉnh i
        self.rank = [0] * n

    def find(self, i):
        """
        [CODE KHÓ]: Tìm gốc (Representative) của tập hợp chứa đỉnh i.
        Áp dụng Kỹ thuật Nén đường đi (Path Compression):
          Gán trực tiếp cha của mọi nút trên đường duyệt trỏ thẳng về gốc!
          Giúp giảm chiều cao cây xuống gần như O(1) trong các lần gọi sau.
        """
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        """
        Hợp nhất 2 tập hợp chứa đỉnh i và j.
        Áp dụng Kỹ thuật Gộp theo hạng (Union by Rank):
          Gắn cây có chiều cao thấp hơn vào dưới gốc của cây có chiều cao lớn hơn,
          ngăn ngừa việc cây biến thành đường thẳng dài.
          
        Trả về:
          - False: Nếu i và j ĐÃ CÙNG một tập hợp (thêm cạnh sẽ TẠO CHU TRÌNH).
          - True: Nếu hợp nhất thành công (không tạo chu trình).
        """
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i == root_j:
            # Hai đỉnh đã cùng chung một thành phần liên thông -> Tạo thành chu trình!
            return False

        # Gộp theo hạng để cây luôn cân bằng
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
    Thuật toán Kruskal tìm Cây khung nhỏ nhất.
    
    Nguyên lý hoạt động:
      1. Sắp xếp tất cả các cạnh theo trọng số tăng dần: w1 <= w2 <= ... <= wE.
      2. Khởi tạo rừng gồm n cây đơn lẻ (mỗi đỉnh là 1 cây) bằng DSU.
      3. Lần lượt xét từng cạnh từ nhẹ nhất đến nặng nhất:
         - Dùng dsu.union(u, v) kiểm tra nếu u và v thuộc 2 cây khác nhau -> Kết nạp cạnh.
         - Nếu u và v đã cùng một cây -> Loại bỏ cạnh vì sẽ tạo chu trình.
      4. Dừng lại ngay khi đã thu nạp đủ đúng n-1 cạnh (Cây khung hoàn thành).
      
    Độ phức tạp: O(E log E) chi phối bởi bước sắp xếp cạnh.
    """
    # Bước 1: Sắp xếp các cạnh tăng dần theo trọng số (edge[2])
    sorted_edges = sorted(edges, key=lambda x: x[2])
    dsu = DSU(n)
    mst_edges = []
    total_weight = 0
    trace_table = []

    # Bước 2: Tham lam chọn các cạnh nhẹ nhất không tạo chu trình
    for (u, v, w) in sorted_edges:
        if dsu.union(u, v):
            # Kết nạp cạnh vào MST
            mst_edges.append((u, v, w))
            total_weight += w
            trace_table.append({
                "edge": (u, v),
                "weight": w,
                "action": "CHỌN",
                "current_mst_edges": len(mst_edges)
            })
        else:
            # Bỏ qua cạnh vì sẽ tạo thành chu trình khép kín
            trace_table.append({
                "edge": (u, v),
                "weight": w,
                "action": "LOẠI (TẠO CHU TRÌNH)"
            })

        # Điều kiện dừng sớm: Cây khung n đỉnh luôn có đúng n-1 cạnh
        if len(mst_edges) == n - 1:
            break
            
    return mst_edges, total_weight, trace_table


def prim(adj, n, start=0):
    r"""
    Thuật toán Prim tìm Cây khung nhỏ nhất.
    
    Nguyên lý hoạt động (Nguyên lý lát cắt - Cut Property):
      1. Bắt đầu với tập đỉnh trong cây S = {start}, tập ngoài cây V \ S.
      2. Tại mỗi bước lặp, tìm cạnh nhẹ nhất (u, v, w) bắc qua lát cắt giữa S và V \ S
         (u thuộc S, v thuộc V \ S).
      3. Kết nạp đỉnh v vào S và thêm cạnh (u, v) vào cây khung.
      4. Lặp lại n-1 lần cho đến khi mọi đỉnh đều được kết nạp.
    """
    visited = [False] * n
    visited[start] = True

    mst_edges = []
    total_weight = 0
    trace_table = []

    for _ in range(n - 1):
        best_u, best_v, best_w = None, None, None

        # Quét tất cả các cạnh bắc qua giữa đỉnh ĐÃ THĂM và CHƯA THĂM
        for u in range(n):
            if not visited[u]:
                continue
            for (v, w) in adj[u]:
                if not visited[v]:
                    if best_w is None or w < best_w:
                        best_u, best_v, best_w = u, v, w

        # Nếu không còn cạnh nào bắc qua (đồ thị không liên thông)
        if best_v is None:
            break

        # Kết nạp đỉnh mới vào cây khung
        visited[best_v] = True
        mst_edges.append((best_u, best_v, best_w))
        total_weight += best_w

        trace_table.append({
            "edge": (best_u, best_v),
            "weight": best_w,
            "current_mst_edges": len(mst_edges)
        })

    return mst_edges, total_weight, trace_table

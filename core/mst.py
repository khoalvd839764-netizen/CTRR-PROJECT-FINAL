# =============================================================================
# THUẬT TOÁN CÂY KHUNG NHỎ NHẤT (MINIMUM SPANNING TREE)
# =============================================================================
# Chứa thuật toán Kruskal và Prim để tìm cây khung có tổng trọng số nhỏ nhất.
# Ứng dụng: Lập lịch dọn dẹp sơ lược (Quick Clean) bao phủ các phòng chính.

class DSU:
    """
    Cấu trúc dữ liệu Disjoint Set Union (Tìm kiếm - Hợp nhất disjoint sets).
    Dùng để phát hiện chu trình cực kỳ hiệu quả trong đồ thị vô hướng.
    """
    def __init__(self, n):
        self.parent = list(range(n))  # Ban đầu mỗi đỉnh là cha của chính nó
        self.rank = [0] * n           # Bậc của cây để gộp tối ưu

    def find(self, i):
        """
        Tìm gốc của tập hợp chứa đỉnh i (Kèm kỹ thuật nén đường Path Compression).
        """
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        """
        Hợp nhất 2 tập hợp chứa i và j. 
        Trả về False nếu i và j đã chung một tập hợp (tạo chu trình).
        """
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i == root_j:
            return False # Tạo thành chu trình!

        # Kỹ thuật gộp theo rank (Union by Rank)
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
    Thuật toán Kruskal tìm cây khung nhỏ nhất.
    Độ phức tạp O(E log E) do phải sắp xếp tất cả các cạnh.
    """
    # Bước 1: Sắp xếp các cạnh tăng dần theo trọng số (độ dài)
    sorted_edges = sorted(edges, key=lambda x: x[2])
    dsu = DSU(n)
    mst_edges = []
    total_weight = 0
    trace_table = []

    # Bước 2: Duyệt từng cạnh, nếu không tạo chu trình thì thêm vào cây
    for (u, v, w) in sorted_edges:
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
            trace_table.append({
                "edge": (u, v),
                "weight": w,
                "action": "LOẠI (TẠO CHU TRÌNH)"
            })

        # Dừng sớm khi cây khung đã đủ n-1 cạnh
        if len(mst_edges) == n - 1:
            break
    return mst_edges, total_weight, trace_table

def prim(adj, n, start=0):
    """
    Thuật toán Prim tìm cây khung nhỏ nhất.
    (Phiên bản đơn giản, không dùng Min Heap)
    """
    visited = [False] * n
    visited[start] = True

    mst_edges = []
    total_weight = 0
    trace_table = []

    for _ in range(n - 1):
        best_u, best_v, best_w = None, None, None

        for u in range(n):
            if not visited[u]:
                continue
            for (v, w) in adj[u]:
                if not visited[v]:
                    if best_w is None or w < best_w:
                        best_u, best_v, best_w = u, v, w

        if best_v is None:
            break

        visited[best_v] = True
        mst_edges.append((best_u, best_v, best_w))
        total_weight += best_w

        trace_table.append({
            "edge": (best_u, best_v),
            "weight": best_w,
            "current_mst_edges": len(mst_edges)
        })

    return mst_edges, total_weight, trace_table

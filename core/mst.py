# -*- coding: utf-8 -*-
"""Cây khung nhỏ nhất (MST) & Cấu trúc DSU: Kruskal và Prim. Chi tiết: core/chu_thich_thuat_toan/7_mst.md"""

class DSU:
    """Disjoint Set Union với Nén đường đi & Gộp theo hạng. Chi tiết: 7_mst.md"""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, i):
        # Nén đường đi (Path Compression)
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        # Gộp theo hạng (Union by Rank)
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i == root_j:
            return False  # Cùng tập hợp -> tạo chu trình

        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1
            
        return True


def kruskal(edges, n):
    """Tìm cây khung nhỏ nhất (MST) bằng Kruskal (O(E log E)). Chi tiết: 7_mst.md"""
    # 1. Sắp xếp cạnh theo trọng số tăng dần
    sorted_edges = sorted(edges, key=lambda x: x[2])
    dsu = DSU(n)
    mst_edges = []
    total_weight = 0
    trace_table = []

    # 2. Tham lam kết nạp các cạnh không tạo chu trình
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

        # Dừng sớm khi đủ n-1 cạnh
        if len(mst_edges) == n - 1:
            break
            
    return mst_edges, total_weight, trace_table


def prim(adj, n, start=0):
    """Tìm cây khung nhỏ nhất (MST) bằng Prim (Cut Property, O(V^2)). Chi tiết: 7_mst.md"""
    visited = [False] * n
    visited[start] = True

    mst_edges = []
    total_weight = 0
    trace_table = []

    for _ in range(n - 1):
        best_u, best_v, best_w = None, None, None

        # Quét cạnh nhẹ nhất bắc qua lát cắt giữa đỉnh đã thăm và chưa thăm
        for u in range(n):
            if not visited[u]:
                continue
            for (v, w) in adj[u]:
                if not visited[v]:
                    if best_w is None or w < best_w:
                        best_u, best_v, best_w = u, v, w

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

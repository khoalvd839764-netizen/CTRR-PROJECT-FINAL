class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i == root_j:
            return False

        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1
        return True

def kruskal(edges, n):
    sorted_edges = sorted(edges, key=lambda x: x[2])
    dsu = DSU(n)
    mst_edges = []
    total_weight = 0
    trace_table = []

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

        if len(mst_edges) == n - 1:
            break
    return mst_edges, total_weight, trace_table

def prim(adj, n, start=0):
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

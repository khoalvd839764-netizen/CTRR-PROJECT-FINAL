import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.graph import Graph
from core.traversal import bfs, dfs, bfs_path, dfs_path

print("🧪 KIỂM TRA PHẦN CỦA ĐỖ THANH (BFS & DFS):")
g = Graph(directed=False).from_edges([(0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1)], n=4)
bfs_order, bfs_tree, bfs_trace = bfs(g.adj, g.n, 0)
dfs_order, dfs_tree, dfs_trace = dfs(g.adj, g.n, 0)

print("   - Thứ tự duyệt BFS:", bfs_order)
print("   - Cây khung BFS   :", bfs_tree)
print("   - Thứ tự duyệt DFS:", dfs_order)
print("   - Cây khung DFS   :", dfs_tree)

# Kiểm tra duyệt từ 1 điểm đến 1 điểm (0 -> 3)
p_bfs, o_bfs, _, _ = bfs_path(g.adj, g.n, 0, 3)
p_dfs, o_dfs, _, _ = dfs_path(g.adj, g.n, 0, 3)
print(f"   - Đường đi BFS (0 -> 3): {p_bfs} ({len(p_bfs) - 1} cạnh)")
print(f"   - Đường đi DFS (0 -> 3): {p_dfs} ({len(p_dfs) - 1} cạnh)")
assert p_bfs in [[0, 1, 3], [0, 2, 3]], "BFS path must be optimal"
assert p_dfs in [[0, 1, 3], [0, 2, 3]], "DFS path must be valid"

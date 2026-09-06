import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.graph import Graph
from core.traversal import bfs, dfs

print("🧪 KIỂM TRA PHẦN CỦA ĐỖ THANH (BFS & DFS):")
g = Graph(directed=False).from_edges([(0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1)], n=4)
bfs_order, bfs_tree, bfs_trace = bfs(g.adj, g.n, 0)
dfs_order, dfs_tree, dfs_trace = dfs(g.adj, g.n, 0)

print("   - Thứ tự duyệt BFS:", bfs_order)
print("   - Cây khung BFS   :", bfs_tree)
print("   - Thứ tự duyệt DFS:", dfs_order)
print("   - Cây khung DFS   :", dfs_tree)

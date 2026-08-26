import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.graph import Graph
from core.shortest_path import dijkstra, bellman_ford

print("🧪 KIỂM TRA PHẦN CỦA LINH (SHORTEST PATH):")
edges = [(0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5), (2, 3, 8), (2, 4, 10), (3, 4, 2)]
g = Graph(directed=False).from_edges(edges, n=5)

d_res = dijkstra(g.adj, g.n, 0, end=4)
b_res = bellman_ford(g.edges, g.n, 0, directed=False, end=4)

print("   - Dijkstra   : Chi phí =", d_res.get("cost"), "| Đường đi =", d_res.get("path"))
print("   - Bellman-Ford: Chi phí =", b_res.get("cost"), "| Đường đi =", b_res.get("path"))

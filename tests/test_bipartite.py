import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.graph import Graph
from core.bipartite import check_bipartite

print("🧪 KIỂM TRA PHẦN CỦA TUẤN (BIPARTITE GRAPH):")
g1 = Graph(directed=False).from_edges([(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 0, 1)], n=4)
res1 = check_bipartite(g1.adj, g1.n)

g2 = Graph(directed=False).from_edges([(0, 1, 1), (1, 2, 1), (2, 0, 1)], n=3)
res2 = check_bipartite(g2.adj, g2.n)

print("   - Test 1 (Hình vuông C4):", res1.get("is_bipartite"), "| V1:", res1.get("v1"), "| V2:", res1.get("v2"))
print("   - Test 2 (Tam giác C3)  :", res2.get("is_bipartite"), "| Chu trình lẻ:", res2.get("odd_cycle"))

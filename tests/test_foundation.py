import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.graph import Graph

def test_graph_and_converter():
    print("=" * 55)
    print("🧪 KIỂM TRA PHẦN NỀN TẢNG (CONVERTER & GRAPH)")
    print("=" * 55)

    # 1. Test nạp từ Danh sách cạnh
    edges = [(0, 1, 4), (1, 2, 2), (0, 2, 5)]
    g1 = Graph(directed=False)
    g1.from_edges(edges, n=3)

    print("\n1. Nạp từ Danh sách cạnh:")
    print("   - Edges :", g1.edges)
    print("   - Matrix:", g1.matrix)
    print("   - Adj   :", g1.adj)

    # 2. Test nạp từ Ma trận kề
    g2 = Graph(directed=False)
    g2.from_matrix(g1.matrix)

    print("\n2. Nạp từ Ma trận kề:")
    print("   - Edges :", g2.edges)
    print("   - Matrix:", g2.matrix)
    print("   - Adj   :", g2.adj)

    # 3. Kiểm tra tính đồng bộ (so sánh nội dung ma trận và tập cạnh)
    assert g1.matrix == g2.matrix, "Lỗi: Ma trận không khớp!"
    assert set(g1.edges) == set(g2.edges), "Lỗi: Danh sách cạnh không khớp!"
    
    # Kiểm tra tập đỉnh kề của từng đỉnh
    for node in range(3):
        assert set(g1.adj[node]) == set(g2.adj[node]), f"Lỗi: Đỉnh kề của node {node} không khớp!"

    print("\n" + "=" * 55)
    print("🎉 TẤT CẢ TEST ĐÃ VƯỢT QUA! NỀN TẢNG HOẠT ĐỘNG 100%")
    print("=" * 55)

if __name__ == "__main__":
    test_graph_and_converter()

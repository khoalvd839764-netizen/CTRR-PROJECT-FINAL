"""
Unit Test: tests/test_mst.py
Kiểm tra tính đúng đắn của Prim và Kruskal (DSU) tìm cây khung nhỏ nhất.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.mst import kruskal, prim


def test_mst():
    print("=======================================================")
    print("🧪 KIỂM TRA PHẦN MST (7.3 PRIM & 7.4 KRUSKAL DSU)")
    print("=======================================================")

    # Đồ thị mẫu 6 đỉnh, 9 cạnh có trọng số
    edges = [
        (0, 1, 4),
        (0, 2, 2),
        (1, 2, 1),
        (1, 3, 5),
        (2, 3, 8),
        (2, 4, 10),
        (3, 4, 2),
        (3, 5, 6),
        (4, 5, 3),
    ]
    n = 6

    # Xây dựng danh sách kề cho Prim
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    # 1. Test Kruskal
    kruskal_edges, kruskal_weight, k_trace = kruskal(edges, n)
    print(f"1. Kruskal MST: Tổng trọng số = {kruskal_weight}")
    print(f"   - Danh sách cạnh MST ({len(kruskal_edges)} cạnh): {kruskal_edges}")
    assert len(kruskal_edges) == n - 1, f"MST phải có đúng {n-1} cạnh"
    assert kruskal_weight == 13, f"Tổng trọng số phải là 13, thực tế: {kruskal_weight}"
    print("   -> Kruskal PASS ✅")

    # 2. Test Prim
    prim_edges, prim_weight, p_trace = prim(adj, n, start=0)
    print(f"2. Prim MST: Tổng trọng số = {prim_weight}")
    print(f"   - Danh sách cạnh MST ({len(prim_edges)} cạnh): {prim_edges}")
    assert len(prim_edges) == n - 1, f"MST phải có đúng {n-1} cạnh"
    assert prim_weight == 13, f"Tổng trọng số phải là 13, thực tế: {prim_weight}"
    print("   -> Prim PASS ✅")

    assert kruskal_weight == prim_weight, "Trọng số Kruskal và Prim phải khớp nhau 100%"

    print("\n🎉 TẤT CẢ TEST CÂY KHUNG MST ĐÃ VƯỢT QUA 100%!")


if __name__ == "__main__":
    test_mst()

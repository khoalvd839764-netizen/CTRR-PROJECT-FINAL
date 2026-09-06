"""
Unit Test: tests/test_euler.py
Kiểm tra tính đúng đắn của check_eulerian, fleury và hierholzer.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.euler import check_eulerian, fleury, hierholzer


def test_euler():
    print("=======================================================")
    print("🧪 KIỂM TRA PHẦN EULER (7.1 FLEURY & 7.2 HIERHOLZER)")
    print("=======================================================")

    # 1. Đồ thị 1: Hình vuông có 2 đường chéo (K4) - Bậc mọi đỉnh = 3 (4 đỉnh lẻ -> Không có Euler)
    k4_adj = {
        0: [(1, 1), (2, 1), (3, 1)],
        1: [(0, 1), (2, 1), (3, 1)],
        2: [(0, 1), (1, 1), (3, 1)],
        3: [(0, 1), (1, 1), (2, 1)],
    }
    has_e, is_circ, start, msg = check_eulerian(k4_adj, 4)
    assert not has_e, "K4 phải không có Euler"
    print(f"1. Test K4 (4 đỉnh bậc 3): {msg} -> PASS ✅")

    # 2. Đồ thị 2: Đồ thị "Ngôi nhà" (House graph) - 2 đỉnh bậc 3 (đỉnh 2 và 3), các đỉnh khác bậc 2
    house_adj = {
        0: [(1, 1), (2, 1)],
        1: [(0, 1), (3, 1)],
        2: [(0, 1), (3, 1), (4, 1)],
        3: [(1, 1), (2, 1), (4, 1)],
        4: [(2, 1), (3, 1)],
    }
    has_e, is_circ, start, msg = check_eulerian(house_adj, 5)
    assert has_e and not is_circ, "House graph phải có Đường đi Euler"
    print(f"2. Test Đồ thị Ngôi nhà (Đường đi Euler): {msg} -> PASS ✅")

    path_fleury, edges_fleury, _ = fleury(house_adj, 5, start=start)
    assert len(edges_fleury) == 6, f"Fleury phải đi đủ 6 cạnh, thực tế: {len(edges_fleury)}"
    print(f"   - Fleury Path: {path_fleury} -> PASS ✅")

    path_hier, edges_hier, _ = hierholzer(house_adj, 5, start=start)
    assert len(edges_hier) == 6, f"Hierholzer phải đi đủ 6 cạnh, thực tế: {len(edges_hier)}"
    print(f"   - Hierholzer Path: {path_hier} -> PASS ✅")

    # 3. Đồ thị 3: Chu trình đơn C5 (5 đỉnh bậc 2) -> Có Chu trình Euler
    c5_adj = {
        0: [(1, 1), (4, 1)],
        1: [(0, 1), (2, 1)],
        2: [(1, 1), (3, 1)],
        3: [(2, 1), (4, 1)],
        4: [(3, 1), (0, 1)],
    }
    has_e, is_circ, start, msg = check_eulerian(c5_adj, 5)
    assert has_e and is_circ, "C5 phải có Chu trình Euler"
    print(f"3. Test Chu trình C5 (Chu trình Euler): {msg} -> PASS ✅")

    p_c5_fleury, e_c5_fleury, _ = fleury(c5_adj, 5)
    assert len(e_c5_fleury) == 5 and p_c5_fleury[0] == p_c5_fleury[-1]
    print(f"   - Fleury Circuit: {p_c5_fleury} -> PASS ✅")

    p_c5_hier, e_c5_hier, _ = hierholzer(c5_adj, 5)
    assert len(e_c5_hier) == 5 and p_c5_hier[0] == p_c5_hier[-1]
    print(f"   - Hierholzer Circuit: {p_c5_hier} -> PASS ✅")

    print("\n🎉 TẤT CẢ TEST EULER ĐÃ VƯỢT QUA 100%!")


if __name__ == "__main__":
    test_euler()

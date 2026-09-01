"""
Unit Test: tests/test_max_flow.py
Kiểm tra tính đúng đắn của thuật toán Ford-Fulkerson (Edmonds-Karp)
và tính Lát cắt hẹp nhất (Min Cut).
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.max_flow import ford_fulkerson


def test_max_flow():
    print("=======================================================")
    print("🧪 KIỂM TRA PHẦN LUỒNG CỰC ĐẠI (7.5 FORD-FULKERSON & MIN CUT)")
    print("=======================================================")

    # Mạng luồng kinh điển 6 đỉnh:
    # 0 (Source S), 5 (Sink T)
    edges = [
        (0, 1, 16),
        (0, 2, 13),
        (1, 2, 10),
        (1, 3, 12),
        (2, 1, 4),
        (2, 4, 14),
        (3, 2, 9),
        (3, 5, 20),
        (4, 3, 7),
        (4, 5, 4),
    ]
    n = 6
    source = 0
    sink = 5

    max_f, flow_mat, min_cut, cut_sets, trace = ford_fulkerson(edges, n, source, sink)
    S_set, T_set = cut_sets

    print(f"1. Luồng cực đại Max Flow = {max_f}")
    print(f"   - Số bước tăng luồng: {len(trace)}")
    for t in trace:
        print(f"     + Bước {t['step']}: Đường {t['path']} tăng {t['bottleneck']} -> Max Flow hiện tại = {t['current_max_flow']}")

    # Kiểm tra Max Flow chuẩn là 23
    assert max_f == 23, f"Max flow phải là 23, thực tế: {max_f}"
    print("   -> Max Flow 23 PASS ✅")

    print("\n2. Lát cắt hẹp nhất (Min Cut):")
    print(f"   - Tập S: {S_set}")
    print(f"   - Tập T: {T_set}")
    print(f"   - Các cung thuộc Min Cut: {min_cut}")

    # Tổng dung lượng của các cung Min Cut phải bằng đúng Max Flow (Định lý Max-Flow Min-Cut)
    min_cut_cap = sum(cap for u, v, cap in min_cut)
    print(f"   - Tổng dung lượng Lát cắt Min Cut = {min_cut_cap}")
    assert min_cut_cap == max_f, f"Min Cut capacity ({min_cut_cap}) phải bằng Max Flow ({max_f})"
    print("   -> Định lý Max-Flow Min-Cut (23 == 23) PASS ✅")

    print("\n🎉 TẤT CẢ TEST LUỒNG CỰC ĐẠI & LÁT CẮT ĐÃ VƯỢT QUA 100%!")


if __name__ == "__main__":
    test_max_flow()

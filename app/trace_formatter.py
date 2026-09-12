# -*- coding: utf-8 -*-
"""
Module: app/trace_formatter.py
Tập hợp các hàm tự do độc lập (pure functions) để định dạng và in bảng vết
(Trace Tables) đối chiếu giải tay từng bước cho các thuật toán CTRR.
"""


def print_bfs_trace(trace):
    """In bảng vết từng bước duyệt BFS (đối chiếu giải tay hàng đợi Queue)."""
    if not trace:
        return
    print("\n📊 BẢNG VẾT TỪNG BƯỚC BFS (ĐỐI CHIẾU GIẢI TAY):")
    print(f"{'Bước':<6} | {'Đỉnh u':<8} | {'Hàng đợi (Queue)':<35} | {'Mảng Visited'}")
    print("-" * 75)
    for row in trace:
        print(f"{row['step']:<6} | {row['u']:<8} | {str(row['queue']):<35} | {row['visited']}")


def print_dfs_trace(trace):
    """In bảng vết từng bước duyệt DFS (đối chiếu giải tay mảng Visited)."""
    if not trace:
        return
    print("\n📊 BẢNG VẾT TỪNG BƯỚC DFS (ĐỐI CHIẾU GIẢI TAY):")
    print(f"{'Bước':<6} | {'Đỉnh u':<8} | {'Mảng Visited'}")
    print("-" * 55)
    for row in trace:
        print(f"{row['step']:<6} | {row['u']:<8} | {row['visited']}")


def print_dijkstra_trace(trace):
    """In bảng ma trận bước lặp nới lỏng đỉnh và mảng khoảng cách dist của Dijkstra."""
    if not trace:
        return
    print("\n📊 BẢNG MA TRẬN BƯỚC LẶP DIJKSTRA (ĐỐI CHIẾU GIẢI TAY):")
    print(f"{'Bước':<6} | {'Đỉnh chốt':<10} | {'Mảng khoảng cách dist'}")
    print("-" * 65)
    for row in trace:
        print(f"{row['step']:<6} | {str(row['u']):<10} | {row['dist']}")


def print_fleury_trace(trace):
    """In bảng vết chọn từng cạnh theo quy tắc tránh cạnh Cầu của Fleury."""
    if not trace:
        return
    print("\n📊 BẢNG VẾT TỪNG BƯỚC FLEURY:")
    print(f"{'Bước':<6} | {'Cạnh chọn':<12} | {'Lý do chọn'}")
    print("-" * 55)
    for r in trace:
        print(f"{r['step']:<6} | ({r['u']} -> {r['v']}){'':<4} | {r['reason']}")


def print_hierholzer_trace(trace):
    """In bảng vết hành động mở rộng / quay lui và trạng thái Stack của Hierholzer."""
    if not trace:
        return
    print("\n📊 BẢNG VẾT TỪNG BƯỚC HIERHOLZER:")
    print(f"{'Bước':<6} | {'Hành động':<40} | {'Ngăn xếp Stack'}")
    print("-" * 75)
    for r in trace:
        print(f"{r['step']:<6} | {r['action']:<40} | {r['stack']}")


def print_prim_trace(trace):
    """In bảng vết kết nạp cạnh có trọng số nhỏ nhất của Prim."""
    if not trace:
        return
    print("\n📊 BẢNG VẾT TỪNG BƯỚC KẾT NẠP CẠNH PRIM:")
    print(f"{'Bước':<6} | {'Cạnh kết nạp':<15} | {'Trọng số w':<12} | {'Tổng cạnh MST'}")
    print("-" * 55)
    for i, r in enumerate(trace, 1):
        print(f"{i:<6} | {str(r['edge']):<15} | {r['weight']:<12} | {r['current_mst_edges']}")


def print_kruskal_trace(trace):
    """In bảng vết xét cạnh theo thứ tự trọng số tăng dần & DSU Union-Find của Kruskal."""
    if not trace:
        return
    print("\n📊 BẢNG VẾT XÉT CẠNH KRUSKAL (ĐỐI CHIẾU GIẢI TAY):")
    print(f"{'Cạnh xét':<15} | {'Trọng số w':<12} | {'Hành động':<25}")
    print("-" * 55)
    for r in trace:
        print(f"{str(r['edge']):<15} | {r['weight']:<12} | {r['action']}")


def print_max_flow_trace(trace):
    """In bảng vết từng bước tìm đường tăng luồng và dung lượng nghẽn của Edmonds-Karp."""
    if not trace:
        return
    print("\n📊 BẢNG VẾT TỪNG BƯỚC TĂNG LUỒNG (AUGMENTING PATHS):")
    print(f"{'Bước':<6} | {'Đường tăng luồng':<30} | {'Độ nghẽn (Δf)':<15} | {'Tổng luồng Max Flow'}")
    print("-" * 75)
    for r in trace:
        path_str = " -> ".join(map(str, r['path']))
        print(f"{r['step']:<6} | {path_str:<30} | {r['bottleneck']:<15} | {r['current_max_flow']}")

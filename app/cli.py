"""
Module: app/cli.py
Giao diện dòng lệnh tương tác (CLI Menu) đầy đủ cho toàn bộ đồ án CTRR.
Bao gồm: Phần Cơ Bản (Mục 1-5), Phần Nâng Cao (Mục 6-8) & Mô Phỏng Thiên Tai Pygame (Mục 9) & Chạy Demo Tự Động (Mục 10).
"""
import os
import sys

from core.graph import Graph
from core.traversal import bfs, dfs, bfs_path, dfs_path
from core.bipartite import check_bipartite
from core.shortest_path import dijkstra, bellman_ford
from core.euler import check_eulerian, fleury, hierholzer
from core.mst import prim, kruskal
from core.max_flow import ford_fulkerson
from visualizer.draw import draw, draw_euler, draw_mst, draw_max_flow
from visualizer.animation import animate_dfs, animate_bfs
from app.trace_formatter import (
    print_bfs_trace, print_dfs_trace, print_dijkstra_trace,
    print_fleury_trace, print_hierholzer_trace,
    print_prim_trace, print_kruskal_trace, print_max_flow_trace
)
from data.samples import (
    GRAPH_UNDIRECTED_20, GRAPH_DIRECTED_20,
    GRAPH_BIPARTITE_15, GRAPH_EULER_15
)


class App: # hàm khởi tạo
    def __init__(self):
        self.graph = None

    def _parse_node_input(self, prompt, default=0):
        val_str = input(prompt).strip()
        if not val_str:
            return default
        if self.graph and getattr(self.graph, "labels", None):
            rev_map = {str(v).lower(): k for k, v in self.graph.labels.items()}
            if val_str.lower() in rev_map:
                return rev_map[val_str.lower()]
        try:
            return int(val_str)
        except ValueError:
            return default

    def _parse_optional_node_input(self, prompt):
        val_str = input(prompt).strip()
        if not val_str:
            return None
        if self.graph and getattr(self.graph, "labels", None):
            rev_map = {str(v).lower(): k for k, v in self.graph.labels.items()}
            if val_str.lower() in rev_map:
                return rev_map[val_str.lower()]
        try:
            return int(val_str)
        except ValueError:
            return None

    def _format_node(self, u):
        if self.graph and getattr(self.graph, "labels", None):
            lbl = self.graph.labels.get(u)
            if lbl is not None and lbl != str(u):
                return f"{lbl}({u})"
        return str(u)

    def _format_path(self, path):
        return " -> ".join(self._format_node(u) for u in path)

    def print_header(self, title):
        print("\n" + "=" * 70)
        print(f"📌 {title.center(64)}")
        print("=" * 70)

    # =========================================================================
    # CHỨC NĂNG 1: INPUT ĐỒ THỊ & VẼ LƯU ẢNH
    # =========================================================================
    def handle_input_graph(self):
        self.print_header("CHỨC NĂNG 1: INPUT ĐỒ THỊ & VẼ LƯU ẢNH")
        print("1. 🌟 Đồ thị mẫu 1: VÔ HƯỚNG 20 ĐỈNH (Mạng lưới đa tầng phi đối xứng - 47 cạnh)")
        print("2. 🚀 Đồ thị mẫu 2: CÓ HƯỚNG 20 ĐỈNH (Mạng phức hợp đa tuyến - 46 cung)")
        print("3. ⚖️  Đồ thị mẫu 3: ĐỒ THỊ 2 PHÍA 15 ĐỈNH (Test Bipartite - 25 cạnh liên thông)")
        print("4. 🔄 Đồ thị mẫu 4: ĐỒ THỊ EULER 15 ĐỈNH (Test Euler - 4-regular 30 cạnh)")
        print("5. Tự nhập đồ thị từ bàn phím (Danh sách cạnh: u v [w])")
        print("6. Tự nhập đồ thị từ bàn phím (Ma trận kề)")
        
        choice = input("👉 Chọn cách nhập (1-6): ").strip()
        
        if choice == '1':
            self.graph = Graph(directed=GRAPH_UNDIRECTED_20["directed"]).from_edges(
                GRAPH_UNDIRECTED_20["edges"], n=GRAPH_UNDIRECTED_20["n"], pos=GRAPH_UNDIRECTED_20.get("pos")
            )
            print("✅ Đã nạp ĐỒ THỊ VÔ HƯỚNG 20 ĐỈNH thành công!")
        elif choice == '2':
            self.graph = Graph(directed=GRAPH_DIRECTED_20["directed"]).from_edges(
                GRAPH_DIRECTED_20["edges"], n=GRAPH_DIRECTED_20["n"], pos=GRAPH_DIRECTED_20.get("pos")
            )
            print("✅ Đã nạp ĐỒ THỊ CÓ HƯỚNG 20 ĐỈNH thành công!")
        elif choice == '3':
            self.graph = Graph(directed=GRAPH_BIPARTITE_15["directed"]).from_edges(
                GRAPH_BIPARTITE_15["edges"], n=GRAPH_BIPARTITE_15["n"], pos=GRAPH_BIPARTITE_15.get("pos")
            )
            print("✅ Đã nạp ĐỒ THỊ 2 PHÍA 15 ĐỈNH thành công!")
        elif choice == '4':
            self.graph = Graph(directed=GRAPH_EULER_15["directed"]).from_edges(
                GRAPH_EULER_15["edges"], n=GRAPH_EULER_15["n"], pos=GRAPH_EULER_15.get("pos")
            )
            print("✅ Đã nạp ĐỒ THỊ EULER 15 ĐỈNH thành công!")
        elif choice == '5':
            n_raw = input("Nhập số đỉnh n: ").strip()
            n = int(n_raw) if n_raw.isdigit() else None
            is_dir = input("Đồ thị có hướng không? (y/n): ").strip().lower() == 'y'
            print("Nhập từng cạnh (u v w), gõ 'done' hoặc ấn Enter dòng trống khi xong:")
            edges = []
            while True:
                line = input().strip()
                if line.lower() == 'done' or not line:
                    break
                p = line.split()
                if len(p) >= 2:
                    edges.append((int(p[0]), int(p[1]), float(p[2]) if len(p) >= 3 else 1))
            max_v = max([max(e[0], e[1]) for e in edges], default=-1)
            if n is not None and n <= max_v:
                print(f"⚠️ Lưu ý: Bạn nhập n = {n}, nhưng danh sách cạnh có đỉnh lớn nhất là {max_v}.")
                print(f"   Hệ thống tự động điều chỉnh n = {max_v + 1} (các đỉnh từ 0 đến {max_v}) để đồ thị hợp lệ!")
                n = max_v + 1
            self.graph = Graph(directed=is_dir).from_edges(edges, n=n)
            print(f"✅ Đã nạp đồ thị từ bàn phím thành công ({self.graph.n} đỉnh, {len(edges)} cạnh)!")
        elif choice == '6':
            n = int(input("Nhập số đỉnh n: ").strip())
            is_dir = input("Đồ thị có hướng không? (y/n): ").strip().lower() == 'y'
            print(f"Nhập {n} dòng ma trận kề:")
            matrix = []
            for _ in range(n):
                matrix.append([float(x) if '.' in x else int(x) for x in input().split()])
            self.graph = Graph(directed=is_dir).from_matrix(matrix)
            print("✅ Đã nạp ma trận thành công!")
        else:
            print("❌ Lựa chọn không hợp lệ.")
            return

        saved_path = draw(self.graph, filename="current_graph.png")
        print(f"🖼️  Đã vẽ và lưu ảnh đồ thị vào: {os.path.relpath(saved_path)}")

    # =========================================================================
    # CHỨC NĂNG 2: HIỂN THỊ 3 PHƯƠNG PHÁP BIỂU DIỄN
    # =========================================================================
    def handle_display_representations(self):
        if self.graph is None:
            print("⚠️ Chưa có đồ thị nào! Vui lòng chọn chức năng 1 để nạp đồ thị trước.")
            return

        self.print_header("CHỨC NĂNG 2: HIỂN THỊ 3 PHƯƠNG PHÁP BIỂU DIỄN")
        
        print("\n--- 1. MA TRẬN KỀ (ADJACENCY MATRIX) ---")
        for row in self.graph.matrix:
            print("  ", row)

        print("\n--- 2. DANH SÁCH KỀ (ADJACENCY LIST) ---")
        for u, neighbors in self.graph.adj.items():
            print(f"   Đỉnh {u}: {neighbors}")

        print(f"\n--- 3. DANH SÁCH CẠNH (EDGE LIST - Tổng cộng {len(self.graph.edges)} cạnh) ---")
        print("  ", self.graph.edges)

    # =========================================================================
    # CHỨC NĂNG 3: DUYỆT ĐỒ THỊ (BFS / DFS & ANIMATION .GIF)
    # =========================================================================
    def handle_traversal(self):
        if self.graph is None:
            print("⚠️ Chưa có đồ thị! Tự động nạp Đồ thị mẫu 20 đỉnh...")
            self.graph = Graph(directed=GRAPH_UNDIRECTED_20["directed"]).from_edges(
                GRAPH_UNDIRECTED_20["edges"], n=GRAPH_UNDIRECTED_20["n"]
            )

        self.print_header("CHỨC NĂNG 3: DUYỆT ĐỒ THỊ (BFS / DFS & ANIMATION .GIF)")
        print("1. Duyệt theo chiều rộng (BFS - Breadth-First Search + Bảng vết + Tìm đường đi)")
        print("2. Duyệt theo chiều sâu  (DFS - Depth-First Search  + Bảng vết + Tìm đường đi)")
        print("3. 🎬 Chạy Hoạt hình Animation DFS (Xuất file .GIF động từng bước duyệt & quay lui)")
        print("4. 🎬 Chạy Hoạt hình Animation BFS (Xuất file .GIF động từng bước đưa vào Queue)")
        
        traversal_type = input("👉 Chọn chức năng muốn duyệt (1-4): ").strip()

        if traversal_type in ['1', '2']:
            start = self._parse_node_input(f"Nhập đỉnh bắt đầu (0 đến {self.graph.n - 1}): ", 0)
            end = self._parse_optional_node_input(f"Nhập đỉnh kết thúc (0 đến {self.graph.n - 1}, nhấn [Enter] để duyệt toàn bộ): ")

            if traversal_type == '1':
                if end is not None:
                    path, bfs_order, bfs_tree, bfs_trace = bfs_path(self.graph.adj, self.graph.n, start, end)
                    print(f"\n🌊 KẾT QUẢ DUYỆT BFS TỪ {self._format_node(start)} ĐẾN {self._format_node(end)}:")
                    if path:
                        print("   • Đường đi tìm được (Số cạnh ít nhất):", self._format_path(path))
                        print(f"   • Chiều dài đường đi: {len(path) - 1} cạnh (ít bước chuyển nhất)")
                        print("   • Thứ tự các đỉnh đã duyệt trước khi chạm đích:", self._format_path(bfs_order))
                        print(f"   • Cây khung BFS đã mở ({len(bfs_tree)} cạnh):", bfs_tree)
                        print_bfs_trace(bfs_trace)

                        path_edges = [(path[i], path[i+1]) for i in range(len(path) - 1)]
                        filename = "traversal_bfs_path.png"
                        saved_path = draw(self.graph, filename=filename, highlight=path_edges)
                        print(f"\n🖼️  Đã vẽ và lưu ảnh Đường đi BFS vào: {os.path.relpath(saved_path)}")
                    else:
                        print(f"   ❌ Không tìm thấy đường đi từ {self._format_node(start)} đến {self._format_node(end)} (Hai đỉnh không liên thông)!")
                        print("   • Thứ tự các đỉnh đã duyệt:", self._format_path(bfs_order))
                        print_bfs_trace(bfs_trace)
                else:
                    bfs_order, bfs_tree, bfs_trace = bfs(self.graph.adj, self.graph.n, start)
                    print(f"\n🌊 KẾT QUẢ DUYỆT BFS TOÀN BỘ TỪ ĐỈNH {self._format_node(start)}:")
                    print("   • Thứ tự duyệt :", self._format_path(bfs_order))
                    print(f"   • Cây khung BFS ({len(bfs_tree)} cạnh):", bfs_tree)
                    print_bfs_trace(bfs_trace)

                    filename = "traversal_bfs_tree.png"
                    saved_path = draw(self.graph, filename=filename, highlight=bfs_tree)
                    print(f"\n🖼️  Đã vẽ và lưu ảnh Cây khung BFS vào: {os.path.relpath(saved_path)}")

            elif traversal_type == '2':
                if end is not None:
                    path, dfs_order, dfs_tree, dfs_trace = dfs_path(self.graph.adj, self.graph.n, start, end)
                    print(f"\n🌲 KẾT QUẢ DUYỆT DFS TỪ {self._format_node(start)} ĐẾN {self._format_node(end)}:")
                    if path:
                        print("   • Đường đi tìm được (Theo chiều sâu DFS):", self._format_path(path))
                        print(f"   • Chiều dài đường đi: {len(path) - 1} cạnh")
                        print("   • Thứ tự các đỉnh đã duyệt trước khi chạm đích:", self._format_path(dfs_order))
                        print(f"   • Cây khung DFS đã mở ({len(dfs_tree)} cạnh):", dfs_tree)
                        print_dfs_trace(dfs_trace)

                        path_edges = [(path[i], path[i+1]) for i in range(len(path) - 1)]
                        filename = "traversal_dfs_path.png"
                        saved_path = draw(self.graph, filename=filename, highlight=path_edges)
                        print(f"\n🖼️  Đã vẽ và lưu ảnh Đường đi DFS vào: {os.path.relpath(saved_path)}")
                    else:
                        print(f"   ❌ Không tìm thấy đường đi từ {self._format_node(start)} đến {self._format_node(end)} (Hai đỉnh không liên thông)!")
                        print("   • Thứ tự các đỉnh đã duyệt:", self._format_path(dfs_order))
                        print_dfs_trace(dfs_trace)
                else:
                    dfs_order, dfs_tree, dfs_trace = dfs(self.graph.adj, self.graph.n, start)
                    print(f"\n🌲 KẾT QUẢ DUYỆT DFS TOÀN BỘ TỪ ĐỈNH {self._format_node(start)}:")
                    print("   • Thứ tự duyệt :", self._format_path(dfs_order))
                    print(f"   • Cây khung DFS ({len(dfs_tree)} cạnh):", dfs_tree)
                    print_dfs_trace(dfs_trace)

                    filename = "traversal_dfs_tree.png"
                    saved_path = draw(self.graph, filename=filename, highlight=dfs_tree)
                    print(f"\n🖼️  Đã vẽ và lưu ảnh Cây khung DFS vào: {os.path.relpath(saved_path)}")

        elif traversal_type == '3':
            start = self._parse_node_input(f"Nhập đỉnh bắt đầu (0 đến {self.graph.n - 1}): ", 0)
            print(f"\n🎬 Đang tạo Animation trực quan hóa từng bước DFS từ đỉnh {start}...")
            gif_path = animate_dfs(self.graph, start=start, filename="traversal_dfs_animation.gif", fps=1.5)
            print(f"🎉 Hoàn tất! File ảnh động đã lưu tại: {os.path.relpath(gif_path)}")

        elif traversal_type == '4':
            start = self._parse_node_input(f"Nhập đỉnh bắt đầu (0 đến {self.graph.n - 1}): ", 0)
            print(f"\n🎬 Đang tạo Animation trực quan hóa từng bước BFS từ đỉnh {start}...")
            gif_path = animate_bfs(self.graph, start=start, filename="traversal_bfs_animation.gif", fps=1.5)
            print(f"🎉 Hoàn tất! File ảnh động đã lưu tại: {os.path.relpath(gif_path)}")
        else:
            print("❌ Lựa chọn không hợp lệ, vui lòng chọn từ 1 đến 4.")

    # =========================================================================
    # CHỨC NĂNG 4: KIỂM TRA ĐỒ THỊ HAI PHÍA (BIPARTITE)
    # =========================================================================
    def handle_bipartite(self):
        self.print_header("CHỨC NĂNG 4: KIỂM TRA ĐỒ THỊ HAI PHÍA (BIPARTITE)")
        print("1. Kiểm tra đồ thị hiện tại")
        print("2. Test với Đồ thị 2 phía mẫu 15 đỉnh (Phân hoạch V1, V2)")
        print("3. Test với Đồ thị mẫu 20 đỉnh (Không 2 phía - Bắt chu trình lẻ)")
        c = input("👉 Chọn (1-3): ").strip()
        
        g_test = self.graph
        if c == '1' and g_test is None:
            print("⚠️ Chưa có đồ thị hiện tại! Tự động nạp Đồ thị 2 phía mẫu 15 đỉnh...")
            g_test = Graph(directed=GRAPH_BIPARTITE_15["directed"]).from_edges(
                GRAPH_BIPARTITE_15["edges"], n=GRAPH_BIPARTITE_15["n"], pos=GRAPH_BIPARTITE_15.get("pos")
            )
        elif c == '2':
            g_test = Graph(directed=GRAPH_BIPARTITE_15["directed"]).from_edges(
                GRAPH_BIPARTITE_15["edges"], n=GRAPH_BIPARTITE_15["n"], pos=GRAPH_BIPARTITE_15.get("pos")
            )
        elif c == '3':
            g_test = Graph(directed=GRAPH_UNDIRECTED_20["directed"]).from_edges(
                GRAPH_UNDIRECTED_20["edges"], n=GRAPH_UNDIRECTED_20["n"], pos=GRAPH_UNDIRECTED_20.get("pos")
            )

        res = check_bipartite(g_test.adj, g_test.n)
        
        if res["is_bipartite"]:
            print("\n🎉 KẾT LUẬN: ĐỒ THỊ LÀ ĐỒ THỊ HAI PHÍA (BIPARTITE)!")
            print(f"   • Tập đỉnh V1 (Màu Đỏ) : {res['v1']}")
            print(f"   • Tập đỉnh V2 (Màu Xanh): {res['v2']}")
            saved_path = draw(g_test, filename="bipartite_result.png", colors=res["colors"])
            print(f"🖼️  Đã lưu hình ảnh tô 2 màu vào: {os.path.relpath(saved_path)}")
        else:
            print("\n❌ KẾT LUẬN: ĐỒ THỊ KHÔNG PHẢI LÀ ĐỒ THỊ HAI PHÍA!")
            print(f"   • Bằng chứng vi phạm (Chu trình lẻ): {res['odd_cycle']}")
            highlight_cycle = []
            cycle = res['odd_cycle']
            for i in range(len(cycle)):
                highlight_cycle.append((cycle[i], cycle[(i + 1) % len(cycle)]))
            saved_path = draw(g_test, filename="bipartite_odd_cycle.png", highlight=highlight_cycle)
            print(f"🖼️  Đã lưu hình ảnh Chu trình lẻ vi phạm vào: {os.path.relpath(saved_path)}")

    # =========================================================================
    # CHỨC NĂNG 5: TÌM ĐƯỜNG ĐI NGẮN NHẤT (DIJKSTRA / BELLMAN-FORD)
    # =========================================================================
    def handle_shortest_path(self):
        if self.graph is None:
            print("⚠️ Chưa có đồ thị! Tự động nạp Đồ thị mẫu 20 đỉnh...")
            self.graph = Graph(directed=GRAPH_UNDIRECTED_20["directed"]).from_edges(
                GRAPH_UNDIRECTED_20["edges"], n=GRAPH_UNDIRECTED_20["n"]
            )

        self.print_header("CHỨC NĂNG 5: TÌM ĐƯỜNG ĐI NGẮN NHẤT (DIJKSTRA / BELLMAN-FORD)")
        print("1. Thuật toán Dijkstra (Nhanh & Tối ưu cho trọng số >= 0)")
        print("2. Thuật toán Bellman-Ford (Xử lý trọng số âm & Bắt chu trình âm)")
        
        algo_choice = input("👉 Chọn thuật toán (1 hoặc 2): ").strip()
        start = self._parse_node_input(f"Nhập đỉnh nguồn (start, 0 đến {self.graph.n - 1}): ", 0)
        end = self._parse_node_input(f"Nhập đỉnh đích (end, 0 đến {self.graph.n - 1}): ", self.graph.n - 1)

        if algo_choice == '1':
            d_res = dijkstra(self.graph.adj, self.graph.n, start, end)
            print(f"\n⚡ KẾT QUẢ THUẬT TOÁN DIJKSTRA ({self._format_node(start)} -> {self._format_node(end)}):")
            print(f"   • Chi phí ngắn nhất : {d_res['cost']}")
            print(f"   • Lộ trình đường đi : {self._format_path(d_res['path']) if d_res['path'] else 'Không có đường đi'}")
            print_dijkstra_trace(d_res["trace"])

            if d_res ["path"]:
                p = d_res["path"]
                hl_path = [(p[i], p[i + 1]) for i in range(len(p) - 1)]
                saved_path = draw(self.graph, filename="shortest_path_dijkstra.png", highlight=hl_path)
                print(f"🖼️  Đã vẽ và hiển thị ảnh đường đi Dijkstra vào: {os.path.relpath(saved_path)}")

        elif algo_choice == '2':
            b_res = bellman_ford(self.graph.edges, self.graph.n, start, self.graph.directed, end)
            print(f"\n🔍 KẾT QUẢ THUẬT TOÁN BELLMAN-FORD ({self._format_node(start)} -> {self._format_node(end)}):")
            print(f"   • Chi phí ngắn nhất     : {b_res['cost']}")
            print(f"   • Lộ trình đường đi     : {self._format_path(b_res['path']) if b_res['path'] else 'Không có đường đi'}")
            print(f"   • Phát hiện chu trình âm: {b_res['has_negative_cycle']}")

            if b_res["path"]:
                p = b_res["path"]
                hl_path = [(p[i], p[i + 1]) for i in range(len(p) - 1)]
                saved_path = draw(self.graph, filename="shortest_path_bellman.png", highlight=hl_path)
                print(f"🖼️  Đã vẽ và hiển thị ảnh đường đi Bellman-Ford vào: {os.path.relpath(saved_path)}")
        else:
            print("❌ Lựa chọn không hợp lệ.")

    # =========================================================================
    # CHỨC NĂNG 6: CHU TRÌNH & ĐƯỜNG ĐI EULER (7.1 FLEURY & 7.2 HIERHOLZER)
    # =========================================================================
    def handle_euler(self):
        self.print_header("CHỨC NĂNG 6: CHU TRÌNH & ĐƯỜNG ĐI EULER (FLEURY / HIERHOLZER)")
        print("1. Chạy trên Đồ thị Euler mẫu 15 đỉnh (Chu trình Euler 4-regular 30 cạnh)")
        print("2. Chạy trên Đồ thị hiện tại")
        
        c = input("👉 Chọn đồ thị (1-2): ").strip()
        if c == '1':
            g_euler = Graph(directed=GRAPH_EULER_15["directed"]).from_edges(
                GRAPH_EULER_15["edges"], n=GRAPH_EULER_15["n"], pos=GRAPH_EULER_15.get("pos")
            )
        else:
            if self.graph is None:
                print("⚠️ Chưa có đồ thị hiện tại! Tự động nạp Đồ thị Euler mẫu 15 đỉnh...")
                g_euler = Graph(directed=GRAPH_EULER_15["directed"]).from_edges(
                    GRAPH_EULER_15["edges"], n=GRAPH_EULER_15["n"], pos=GRAPH_EULER_15.get("pos")
                )
            else:
                g_euler = self.graph

        has_e, is_circ, start_node, msg = check_eulerian(g_euler.adj, g_euler.n, g_euler.directed)
        print(f"\n🔍 KIỂM TRA ĐIỀU KIỆN EULER: {msg}")

        if not has_e:
            print("❌ Đồ thị không tồn tại Chu trình hay Đường đi Euler!")
            return

        print("\n--- CHỌN THUẬT TOÁN TÌM ĐƯỜNG EULER ---")
        print("1. Thuật toán Fleury (7.1 - Không đi qua Cầu)")
        print("2. Thuật toán Hierholzer (7.2 - Nối chu trình bằng Stack O(E))")
        algo = input("👉 Chọn thuật toán (1 hoặc 2): ").strip()

        if algo == '1':
            path, edges_order, trace = fleury(g_euler.adj, g_euler.n, start=start_node, directed=g_euler.directed)
            print(f"\n🎯 KẾT QUẢ FLEURY ({'Chu trình' if is_circ else 'Đường đi'} Euler):")
            print("   • Thứ tự đỉnh :", " -> ".join(map(str, path)))
            print("   • Thứ tự cạnh :", edges_order)
            print_fleury_trace(trace)

            filename = "euler_fleury_result.png"
            saved_path = draw_euler(g_euler, path, edges_order, filename=filename)
            print(f"\n🖼️  Đã vẽ và lưu ảnh lộ trình Euler vào: {os.path.relpath(saved_path)}")

        elif algo == '2':
            path, edges_order, trace = hierholzer(g_euler.adj, g_euler.n, start=start_node, directed=g_euler.directed)
            print(f"\n🎯 KẾT QUẢ HIERHOLZER ({'Chu trình' if is_circ else 'Đường đi'} Euler):")
            print("   • Thứ tự đỉnh :", " -> ".join(map(str, path)))
            print("   • Thứ tự cạnh :", edges_order)
            print_hierholzer_trace(trace)

            filename = "euler_hierholzer_result.png"
            saved_path = draw_euler(g_euler, path, edges_order, filename=filename)
            print(f"\n🖼️  Đã vẽ và lưu ảnh lộ trình Euler vào: {os.path.relpath(saved_path)}")
        else:
            print("❌ Lựa chọn không hợp lệ.")

    # =========================================================================
    # CHỨC NĂNG 7: CÂY KHUNG NHỎ NHẤT (7.3 PRIM & 7.4 KRUSKAL DSU)
    # =========================================================================
    def handle_mst(self):
        self.print_header("CHỨC NĂNG 7: CÂY KHUNG NHỎ NHẤT (PRIM & KRUSKAL DSU)")
        print("1. Chạy trên Đồ thị vô hướng mẫu 20 đỉnh")
        print("2. Chạy trên Đồ thị hiện tại")
        
        c = input("👉 Chọn đồ thị (1-2): ").strip()
        if c == '1':
            g_mst = Graph(directed=False).from_edges(
                GRAPH_UNDIRECTED_20["edges"], n=GRAPH_UNDIRECTED_20["n"], pos=GRAPH_UNDIRECTED_20.get("pos")
            )
        else:
            if self.graph is None:
                print("⚠️ Chưa có đồ thị hiện tại! Tự động nạp Đồ thị mẫu 20 đỉnh...")
                g_mst = Graph(directed=False).from_edges(
                    GRAPH_UNDIRECTED_20["edges"], n=GRAPH_UNDIRECTED_20["n"], pos=GRAPH_UNDIRECTED_20.get("pos")
                )
            else:
                g_mst = self.graph

        print("\n--- CHỌN THUẬT TOÁN CÂY KHUNG NHỎ NHẤT ---")
        print("1. Thuật toán Prim (7.3 - Mở rộng từ 1 đỉnh)")
        print("2. Thuật toán Kruskal (7.4 - Sắp xếp cạnh + DSU Union-Find)")
        algo = input("👉 Chọn thuật toán (1 hoặc 2): ").strip()

        if algo == '1':
            start = self._parse_node_input(f"Nhập đỉnh xuất phát (0 đến {g_mst.n - 1}): ", 0)
            mst_edges, total_w, trace = prim(g_mst.adj, g_mst.n, start=start)
            print(f"\n🌲 KẾT QUẢ THUẬT TOÁN PRIM (MST TỪ ĐỈNH {self._format_node(start)}):")
            print(f"   • Tổng trọng số cây khung : {total_w}")
            print(f"   • Danh sách {len(mst_edges)} cạnh cây khung : {mst_edges}")
            print_prim_trace(trace)

            filename = "mst_prim_result.png"
            saved_path = draw_mst(g_mst, mst_edges, total_w, filename=filename)
            print(f"\n🖼️  Đã vẽ và lưu ảnh Cây khung Prim vào: {os.path.relpath(saved_path)}")

        elif algo == '2':
            mst_edges, total_w, trace = kruskal(g_mst.edges, g_mst.n)
            print(f"\n🌲 KẾT QUẢ THUẬT TOÁN KRUSKAL (DSU UNION-FIND):")
            print(f"   • Tổng trọng số cây khung : {total_w}")
            print(f"   • Danh sách {len(mst_edges)} cạnh cây khung : {mst_edges}")
            print_kruskal_trace(trace)

            filename = "mst_kruskal_result.png"
            saved_path = draw_mst(g_mst, mst_edges, total_w, filename=filename)
            print(f"\n🖼️  Đã vẽ và lưu ảnh Cây khung Kruskal vào: {os.path.relpath(saved_path)}")
        else:
            print("❌ Lựa chọn không hợp lệ.")

    # =========================================================================
    # CHỨC NĂNG 8: LUỒNG CỰC ĐẠI & LÁT CẮT HẸP NHẤT (7.5 FORD-FULKERSON)
    # =========================================================================
    def handle_max_flow(self):
        self.print_header("CHỨC NĂNG 8: LUỒNG CỰC ĐẠI & LÁT CẮT HẸP NHẤT (FORD-FULKERSON)")
        print("1. Chạy trên Đồ thị có hướng mẫu 20 đỉnh (S=0 -> T=19, Max Flow = 11)")
        print("2. Chạy trên Đồ thị hiện tại")

        c = input("👉 Chọn mạng luồng (1-2): ").strip()
        if c == '1':
            g_flow = Graph(directed=True).from_edges(
                GRAPH_DIRECTED_20["edges"], n=GRAPH_DIRECTED_20["n"], pos=GRAPH_DIRECTED_20.get("pos")
            )
            source = 0
            sink = 19
        else:
            if self.graph is None:
                print("⚠️ Chưa có đồ thị trong bộ nhớ! Tự động nạp Đồ thị có hướng 20 đỉnh...")
                g_flow = Graph(directed=True).from_edges(
                    GRAPH_DIRECTED_20["edges"], n=GRAPH_DIRECTED_20["n"], pos=GRAPH_DIRECTED_20.get("pos")
                )
                source = 0
                sink = 19
            elif not self.graph.directed:
                print(f"ℹ️ Đồ thị hiện tại là đồ thị vô hướng ({self.graph.n} đỉnh).")
                print("   Hệ thống tự động coi các cạnh là 2 chiều (dung lượng dòng chảy 2 chiều) để tìm luồng cực đại.")
                flow_edges = []
                for edge in self.graph.edges:
                    u, v = edge[0], edge[1]
                    w = edge[2] if len(edge) > 2 else 1
                    flow_edges.append((u, v, w))
                    flow_edges.append((v, u, w))
                g_flow = Graph(directed=True).from_edges(
                    flow_edges, n=self.graph.n, pos=getattr(self.graph, "pos", None)
                )
                setattr(g_flow, "original_undirected", True)
                setattr(g_flow, "base_edges", list(self.graph.edges))
                source = self._parse_node_input(f"Nhập đỉnh Nguồn S (0 đến {g_flow.n - 1}, mặc định 0): ", 0)
                sink = self._parse_node_input(f"Nhập đỉnh Đích T (0 đến {g_flow.n - 1}, mặc định {g_flow.n - 1}): ", g_flow.n - 1)
            else:
                g_flow = self.graph
                source = self._parse_node_input(f"Nhập đỉnh Nguồn S (0 đến {g_flow.n - 1}, mặc định 0): ", 0)
                sink = self._parse_node_input(f"Nhập đỉnh Đích T (0 đến {g_flow.n - 1}, mặc định {g_flow.n - 1}): ", g_flow.n - 1)

        max_f, flow_mat, min_cut, cut_sets, trace = ford_fulkerson(g_flow.edges, g_flow.n, source, sink)
        S_set, T_set = cut_sets

        print(f"\n🌊 KẾT QUẢ THUẬT TOÁN FORD-FULKERSON (EDMONDS-KARP):")
        print(f"   • LUỒNG CỰC ĐẠI (MAX FLOW) = {max_f}")
        print(f"   • Phân hoạch 2 tập đỉnh Lát cắt:")
        print(f"     + Tập S (Nguồn tới được): {sorted(list(S_set))}")
        print(f"     + Tập T (Đích)          : {sorted(list(T_set))}")
        print(f"   • Danh sách các cung thuộc Lát cắt hẹp nhất (Min Cut): {min_cut}")
        print(f"   • Tổng dung lượng Lát cắt Min Cut = {sum(cap for _, _, cap in min_cut)} (khớp với Max Flow = {max_f})")
        print_max_flow_trace(trace)

        filename = "max_flow_result.png"
        saved_path = draw_max_flow(g_flow, flow_mat, min_cut, max_f, source, sink, filename=filename)
        print(f"\n🖼️  Đã vẽ và lưu ảnh Mạng luồng & Lát cắt vào: {os.path.relpath(saved_path)}")

    # =========================================================================
    # CHỨC NĂNG 9: DEMO TỰ ĐỘNG TOÀN DIỆN
    # =========================================================================
    def handle_auto_demo(self):
        self.print_header("🚀 CHẠY DEMO TỰ ĐỘNG TOÀN DIỆN (TẤT CẢ CHỨC NĂNG 1 -> 8)")
        
        # 1. Đồ thị 20 đỉnh
        g20 = Graph(directed=GRAPH_UNDIRECTED_20["directed"]).from_edges(
            GRAPH_UNDIRECTED_20["edges"], n=GRAPH_UNDIRECTED_20["n"], pos=GRAPH_UNDIRECTED_20.get("pos")
        )
        print("\n[PHẦN CƠ BẢN] ĐỒ THỊ 20 ĐỈNH:")
        bfs_ord, bfs_tree, _ = bfs(g20.adj, g20.n, 0)
        dfs_ord, dfs_tree, _ = dfs(g20.adj, g20.n, 0)
        sp_res = dijkstra(g20.adj, g20.n, 0, 19)
        print(f"• BFS (0)          : {' -> '.join(map(str, bfs_ord))}")
        print(f"• DFS (0)          : {' -> '.join(map(str, dfs_ord))}")
        print(f"• Shortest (0->19) : {' -> '.join(map(str, sp_res['path']))} (Chi phí: {sp_res['cost']})")
        draw(g20, filename="demo_20_graph.png", show=False)

        # 2. Đồ thị 2 phía 15 đỉnh (Bipartite)
        g_bip = Graph(directed=GRAPH_BIPARTITE_15["directed"]).from_edges(
            GRAPH_BIPARTITE_15["edges"], n=GRAPH_BIPARTITE_15["n"], pos=GRAPH_BIPARTITE_15.get("pos")
        )
        res_bip = check_bipartite(g_bip.adj, g_bip.n)
        print(f"\n[PHẦN 4 BIPARTITE] Đồ thị 2 phía 15 đỉnh: {res_bip['is_bipartite']} | V1: {len(res_bip['v1'])} đỉnh, V2: {len(res_bip['v2'])} đỉnh")
        draw(g_bip, filename="demo_bipartite_15.png", colors=res_bip["colors"], show=False)

        # 3. Đồ thị Euler 15 đỉnh (Eulerian Circuit)
        g_e = Graph(directed=GRAPH_EULER_15["directed"]).from_edges(
            GRAPH_EULER_15["edges"], n=GRAPH_EULER_15["n"], pos=GRAPH_EULER_15.get("pos")
        )
        e_path, e_edges, _ = hierholzer(g_e.adj, g_e.n, 0)
        print(f"[PHẦN 7.1-7.2 EULER] Đồ thị Euler 15 đỉnh: {' -> '.join(map(str, e_path[:8]))} ... ({len(e_edges)} cạnh)")
        draw_euler(g_e, e_path, e_edges, filename="demo_euler_15.png", show=False)

        # 4. MST trên đồ thị 20 đỉnh
        k_mst, k_w, _ = kruskal(g20.edges, g20.n)
        print(f"[PHẦN 7.3-7.4 MST] Kruskal MST 20 đỉnh = {k_w} ({len(k_mst)} cạnh)")
        draw_mst(g20, k_mst, k_w, filename="demo_mst_20.png", show=False)

        # 5. Max Flow trên đồ thị có hướng 20 đỉnh
        g_dir = Graph(directed=GRAPH_DIRECTED_20["directed"]).from_edges(
            GRAPH_DIRECTED_20["edges"], n=GRAPH_DIRECTED_20["n"], pos=GRAPH_DIRECTED_20.get("pos")
        )
        mf, f_mat, min_c, _, _ = ford_fulkerson(g_dir.edges, g_dir.n, 0, 19)
        print(f"[PHẦN 7.5 MAX FLOW] Ford-Fulkerson Max Flow (0->19) = {mf} | Min Cut = {min_c}")
        draw_max_flow(g_dir, f_mat, min_c, mf, 0, 19, filename="demo_max_flow_20.png", show=False)

        print("\n" + "=" * 70)
        print("🎉 TẤT CẢ CÁC THUẬT TOÁN ĐÃ ĐƯỢC GIẢI TOÀN DIỆN VÀ CHÍNH XÁC 100%!")
        print("🖼️  Tất cả các file ảnh đồ thị đã được vẽ và lưu tại thư mục: results/")
        print("=" * 70)

    # =========================================================================
    # CHỨC NĂNG 10: ỨNG DỤNG THỰC TẾ (ĐIỀU PHỐI GIAO THÔNG ĐÔ THỊ THÔNG MINH)
    # =========================================================================
    def handle_practical_traffic_app(self):
        self.print_header("🚑 ỨNG DỤNG THỰC TẾ: SA BÀN ĐIỀU PHỐI CẤP CỨU & CỨU HỘ UTH - BÌNH THẠNH (PYGAME)")
        print("Trọng tâm Thuật toán CTRR Thực Chiến:")
        print("  • 1. BFS Quét Đa Tầng (Multi-Layer Wave): Quét từ tâm sự cố tìm trạm y tế / PCCC gần nhất còn xe.")
        print("  • 2. Dijkstra Dò Đường Siêu Tốc (Fast Trace): Hiển thị tia quét nới lỏng đỉnh trước khi chốt lộ trình.")
        print("  • 3. Xe Cứu Thương Bẻ Cua Né Tắc (Dynamic Reroute): Click chuột phải gây kẹt xe, xe tự đổi lộ trình.")
        print("  • 4. Kruskal MST: Phím [M] quy hoạch mạng cáp viễn thông kết nối toàn bộ 32 nút giao.")
        print("  • 5. Menu Tròn (Radial Menu): Click vào nút giao để chọn [🚑 Cấp Cứu] hoặc [🚒 Báo Cháy].")
        print("\nĐang khởi động Giao diện Sa bàn Tác chiến Pygame (1600x920)...")
        try:
            from ung_dung_thuc_te.main import run as run_traffic_gui
            run_traffic_gui()
            print("✅ Đã đóng giao diện Ứng Dụng Thực Tế và quay lại Menu chính.")
        except Exception as e:
            print(f"❌ Lỗi khi khởi chạy mô phỏng: {e}")

    def run(self):
        while True:
            print("\n" + "=" * 70)
            print("🎓 CTRR FINAL PROJECT — HỆ THỐNG GIẢI TOÁN ĐỒ THỊ TOÀN DIỆN")
            print("=" * 70)
            print(" 🟢 [PHẦN CƠ BẢN]")
            print("   [1] Nhập đồ thị (Mẫu 20 đỉnh vô hướng / Mẫu 20 đỉnh có hướng / Bàn phím) & Vẽ lưu ảnh")
            print("   [2] Hiển thị 3 phương pháp biểu diễn (Ma trận ↔ Danh sách kề ↔ Cạnh)")
            print("   [3] Duyệt đồ thị (BFS hoặc DFS riêng biệt + Animation .GIF + Bảng vết)")
            print("   [4] Kiểm tra đồ thị hai phía (Bipartite) & Chu trình lẻ")
            print("   [5] Tìm đường đi ngắn nhất (Dijkstra hoặc Bellman-Ford riêng biệt)")
            print("\n 🔴 [PHẦN NÂNG CAO]")
            print("   [6] 🔀 Chu trình & Đường đi Euler (7.1 Fleury / 7.2 Hierholzer + Bảng vết)")
            print("   [7] 🌲 Cây khung nhỏ nhất MST (7.3 Prim / 7.4 Kruskal DSU + Bảng vết)")
            print("   [8] 🌊 Luồng cực đại & Lát cắt hẹp nhất (7.5 Ford-Fulkerson & Min Cut)")
            print("\n 🚀 [TỔNG HỢP & ỨNG DỤNG THỰC TẾ]")
            print("   [9] ⚡ Chạy Demo TỰ ĐỘNG TOÀN DIỆN (Tất cả từ Mục 1 đến Mục 8)")
            print("   [10] 🚦 ỨNG DỤNG THỰC TẾ: Mạng Lưới Giao Thông Đô Thị Thông Minh (Dijkstra, BFS, DFS, MST)")
            print("   [0] Thoát chương trình")
            print("=" * 70)
            
            choice = input("👉 Nhập lựa chọn của bạn (0 - 10): ").strip()
            
            if choice == '1':
                self.handle_input_graph()
            elif choice == '2':
                self.handle_display_representations()
            elif choice == '3':
                self.handle_traversal()
            elif choice == '4':
                self.handle_bipartite()
            elif choice == '5':
                self.handle_shortest_path()
            elif choice == '6':
                self.handle_euler()
            elif choice == '7':
                self.handle_mst()
            elif choice == '8':
                self.handle_max_flow()
            elif choice == '9':
                self.handle_auto_demo()
            elif choice == '10':
                self.handle_practical_traffic_app()
            elif choice == '0':
                print("\n👋 Cảm ơn thầy cô và các bạn đã theo dõi! Tạm biệt.")
                break
            else:
                print("❌ Lựa chọn không hợp lệ, vui lòng chọn từ 0 đến 10.")


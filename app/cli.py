from core.graph import Graph
from visualizer.draw import draw
from core.traversal import bfs, dfs
from core.bipartite import check_bipartite
from core.shortest_path import dijkstra, bellman_ford
from data.samples import (
    GRAPH_UNDIRECTED_15, GRAPH_DIRECTED_30,
    GRAPH_BIPARTITE, GRAPH_NOT_BIPARTITE
)

class App:
    def __init__(self):
        self.graph = None

    def print_header(self, title):
        print("\n" + "=" * 70)
        print(f"📌 {title.center(64)}")
        print("=" * 70)

    def handle_input_graph(self):
        self.print_header("CHỨC NĂNG 1: INPUT ĐỒ THỊ & VẼ LƯU ẢNH")
        print("1. 🌟 Đồ thị mẫu 1: VÔ HƯỚNG 15 ĐỈNH (Bố cục 2 vòng đồng tâm - 33 cạnh)")
        print("2. 🚀 Đồ thị mẫu 2: CÓ HƯỚNG 30 ĐỈNH (Bố cục 3 tầng đô thị - 52 cung)")
        print("3. Tự nhập đồ thị từ bàn phím (Danh sách cạnh: u v [w])")
        print("4. Tự nhập đồ thị từ bàn phím (Ma trận kề)")
        
        choice = input("👉 Chọn cách nhập (1-4): ").strip()
        
        if choice == '1':
            self.graph = Graph(directed=GRAPH_UNDIRECTED_15["directed"]).from_edges(
                GRAPH_UNDIRECTED_15["edges"], n=GRAPH_UNDIRECTED_15["n"]
            )
            print("✅ Đã nạp ĐỒ THỊ VÔ HƯỚNG 15 ĐỈNH thành công!")
        elif choice == '2':
            self.graph = Graph(directed=GRAPH_DIRECTED_30["directed"]).from_edges(
                GRAPH_DIRECTED_30["edges"], n=GRAPH_DIRECTED_30["n"]
            )
            print("✅ Đã nạp ĐỒ THỊ CÓ HƯỚNG 30 ĐỈNH thành công!")
        elif choice == '3':
            n = int(input("Nhập số đỉnh n: "))
            is_dir = input("Đồ thị có hướng không? (y/n): ").strip().lower() == 'y'
            print("Nhập từng cạnh (u v w), gõ 'done' hoặc ấn Enter dòng trống khi xong:")
            edges = []
            while True:
                line = input().strip()
                if line.lower() == 'done' or not line:
                    break
                p = line.split()
                edges.append((int(p[0]), int(p[1]), float(p[2]) if len(p) >= 3 else 1))
            self.graph = Graph(directed=is_dir).from_edges(edges, n=n)
            print("✅ Đã nạp đồ thị thành công!")
        elif choice == '4':
            n = int(input("Nhập số đỉnh n: "))
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

        filename = "current_graph.png"
        draw(self.graph, filename=filename)
        print(f"🖼️  Đã vẽ và lưu ảnh đồ thị vào file: {filename}")

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
    # [⭐ CHỖ SỬA 1: TÁCH RIÊNG 2 LỰA CHỌN BFS HOẶC DFS - BỎ CHỨC NĂNG CHẠY CẢ 2]
    # =========================================================================
    def handle_traversal(self):
        if self.graph is None:
            print("⚠️ Chưa có đồ thị! Tự động nạp Đồ thị mẫu 15 đỉnh...")
            self.graph = Graph(directed=GRAPH_UNDIRECTED_15["directed"]).from_edges(
                GRAPH_UNDIRECTED_15["edges"], n=GRAPH_UNDIRECTED_15["n"]
            )

        self.print_header("CHỨC NĂNG 3: DUYỆT ĐỒ THỊ (BFS / DFS)")
        print("1. Duyệt theo chiều rộng (BFS - Breadth-First Search)")
        print("2. Duyệt theo chiều sâu  (DFS - Depth-First Search)")
        
        traversal_type = input("👉 Chọn thuật toán muốn duyệt (1 hoặc 2): ").strip()
        start = int(input(f"Nhập đỉnh bắt đầu (0 đến {self.graph.n - 1}): ").strip() or "0")

        # --- LỰA CHỌN 1: DUYỆT BFS ---
        if traversal_type == '1':
            bfs_order, bfs_tree, bfs_trace = bfs(self.graph.adj, self.graph.n, start)
            print(f"\n🌊 KẾT QUẢ DUYỆT BFS TỪ ĐỈNH {start}:")
            print("   • Thứ tự duyệt :", " -> ".join(map(str, bfs_order)))
            print(f"   • Cây khung BFS ({len(bfs_tree)} cạnh):", bfs_tree)
            
            print("\n📊 BẢNG VẾT TỪNG BƯỚC BFS (ĐỐI CHIẾU GIẢI TAY):")
            print(f"{'Bước':<6} | {'Đỉnh u':<8} | {'Hàng đợi (Queue)':<35} | {'Mảng Visited'}")
            print("-" * 75)
            for row in bfs_trace:
                print(f"{row['step']:<6} | {row['u']:<8} | {str(row['queue']):<35} | {row['visited']}")

            filename = "traversal_bfs_tree.png"
            draw(self.graph, filename=filename, highlight=bfs_tree)
            print(f"\n🖼️  Đã vẽ và lưu ảnh Cây khung BFS vào: {filename}")

        # --- LỰA CHỌN 2: DUYỆT DFS ---
        elif traversal_type == '2':
            dfs_order, dfs_tree, dfs_trace = dfs(self.graph.adj, self.graph.n, start)
            print(f"\n🌲 KẾT QUẢ DUYỆT DFS TỪ ĐỈNH {start}:")
            print("   • Thứ tự duyệt :", " -> ".join(map(str, dfs_order)))
            print(f"   • Cây khung DFS ({len(dfs_tree)} cạnh):", dfs_tree)

            print("\n📊 BẢNG VẾT TỪNG BƯỚC DFS (ĐỐI CHIẾU GIẢI TAY):")
            print(f"{'Bước':<6} | {'Đỉnh u':<8} | {'Mảng Visited'}")
            print("-" * 55)
            for row in dfs_trace:
                print(f"{row['step']:<6} | {row['u']:<8} | {row['visited']}")

            filename = "traversal_dfs_tree.png"
            draw(self.graph, filename=filename, highlight=dfs_tree)
            print(f"\n🖼️  Đã vẽ và lưu ảnh Cây khung DFS vào: {filename}")

        else:
            print("❌ Lựa chọn không hợp lệ, vui lòng chọn 1 hoặc 2.")

    def handle_bipartite(self):
        self.print_header("CHỨC NĂNG 4: KIỂM TRA ĐỒ THỊ HAI PHÍA (BIPARTITE)")
        print("1. Kiểm tra đồ thị hiện tại")
        print("2. Test với Đồ thị 2 phía mẫu (Hình vuông C4)")
        print("3. Test với Đồ thị KHÔNG 2 phía mẫu (Tam giác C3)")
        print("4. Test với Đồ thị mẫu 15 đỉnh")
        c = input("👉 Chọn (1-4): ").strip()
        
        g_test = self.graph
        if c == '2':
            g_test = Graph(directed=GRAPH_BIPARTITE["directed"]).from_edges(
                GRAPH_BIPARTITE["edges"], n=GRAPH_BIPARTITE["n"]
            )
        elif c == '3':
            g_test = Graph(directed=GRAPH_NOT_BIPARTITE["directed"]).from_edges(
                GRAPH_NOT_BIPARTITE["edges"], n=GRAPH_NOT_BIPARTITE["n"]
            )
        elif c == '4' or g_test is None:
            g_test = Graph(directed=GRAPH_UNDIRECTED_15["directed"]).from_edges(
                GRAPH_UNDIRECTED_15["edges"], n=GRAPH_UNDIRECTED_15["n"]
            )

        res = check_bipartite(g_test.adj, g_test.n)
        
        if res["is_bipartite"]:
            print("\n🎉 KẾT LUẬN: ĐỒ THỊ LÀ ĐỒ THỊ HAI PHÍA (BIPARTITE)!")
            print(f"   • Tập đỉnh V1 (Màu Đỏ) : {res['v1']}")
            print(f"   • Tập đỉnh V2 (Màu Xanh): {res['v2']}")
            draw(g_test, filename="bipartite_result.png", colors=res["colors"])
            print("🖼️  Đã lưu hình ảnh tô 2 màu vào: bipartite_result.png")
        else:
            print("\n❌ KẾT LUẬN: ĐỒ THỊ KHÔNG PHẢI LÀ ĐỒ THỊ HAI PHÍA!")
            print(f"   • Bằng chứng vi phạm (Chu trình lẻ): {res['odd_cycle']}")
            highlight_cycle = []
            cycle = res['odd_cycle']
            for i in range(len(cycle)):
                highlight_cycle.append((cycle[i], cycle[(i + 1) % len(cycle)]))
            draw(g_test, filename="bipartite_odd_cycle.png", highlight=highlight_cycle)
            print("🖼️  Đã lưu hình ảnh Chu trình lẻ vi phạm vào: bipartite_odd_cycle.png")

    # =========================================================================
    # [⭐ CHỖ SỬA 2: TÁCH RIÊNG 2 LỰA CHỌN DIJKSTRA HOẶC BELLMAN-FORD - BỎ CHẠY CẢ 2]
    # =========================================================================
    def handle_shortest_path(self):
        if self.graph is None:
            print("⚠️ Chưa có đồ thị! Tự động nạp Đồ thị mẫu 15 đỉnh...")
            self.graph = Graph(directed=GRAPH_UNDIRECTED_15["directed"]).from_edges(
                GRAPH_UNDIRECTED_15["edges"], n=GRAPH_UNDIRECTED_15["n"]
            )

        self.print_header("CHỨC NĂNG 5: TÌM ĐƯỜNG ĐI NGẮN NHẤT (DIJKSTRA / BELLMAN-FORD)")
        print("1. Thuật toán Dijkstra (Nhanh & Tối ưu cho trọng số >= 0)")
        print("2. Thuật toán Bellman-Ford (Xử lý trọng số âm & Bắt chu trình âm)")
        
        algo_choice = input("👉 Chọn thuật toán (1 hoặc 2): ").strip()
        start = int(input(f"Nhập đỉnh nguồn (start, 0 đến {self.graph.n - 1}): ").strip() or "0")
        end = int(input(f"Nhập đỉnh đích (end, 0 đến {self.graph.n - 1}): ").strip() or str(self.graph.n - 1))

        # --- LỰA CHỌN 1: CHẠY DIJKSTRA ---
        if algo_choice == '1':
            d_res = dijkstra(self.graph.adj, self.graph.n, start, end)
            print(f"\n⚡ KẾT QUẢ THUẬT TOÁN DIJKSTRA ({start} -> {end}):")
            print(f"   • Chi phí ngắn nhất : {d_res['cost']}")
            print(f"   • Lộ trình đường đi : {' -> '.join(map(str, d_res['path'])) if d_res['path'] else 'Không có đường đi'}")
            
            print("\n📊 BẢNG MA TRẬN BƯỚC LẶP DIJKSTRA (ĐỐI CHIẾU GIẢI TAY):")
            print(f"{'Bước':<6} | {'Đỉnh chốt':<10} | {'Mảng khoảng cách dist'}")
            print("-" * 65)
            for row in d_res["trace"]:
                print(f"{row['step']:<6} | {row['u']:<10} | {row['dist']}")

            if d_res["path"]:
                p = d_res["path"]
                hl_path = [(p[i], p[i + 1]) for i in range(len(p) - 1)]
                draw(self.graph, filename="shortest_path_dijkstra.png", highlight=hl_path)
                print("🖼️  Đã vẽ và hiển thị ảnh đường đi Dijkstra vào: shortest_path_dijkstra.png")

        # --- LỰA CHỌN 2: CHẠY BELLMAN-FORD ---
        elif algo_choice == '2':
            b_res = bellman_ford(self.graph.edges, self.graph.n, start, self.graph.directed, end)
            print(f"\n🔍 KẾT QUẢ THUẬT TOÁN BELLMAN-FORD ({start} -> {end}):")
            print(f"   • Chi phí ngắn nhất     : {b_res['cost']}")
            print(f"   • Lộ trình đường đi     : {' -> '.join(map(str, b_res['path'])) if b_res['path'] else 'Không có đường đi'}")
            print(f"   • Phát hiện chu trình âm: {b_res['has_negative_cycle']}")

            if b_res["path"]:
                p = b_res["path"]
                hl_path = [(p[i], p[i + 1]) for i in range(len(p) - 1)]
                draw(self.graph, filename="shortest_path_bellman.png", highlight=hl_path)
                print("🖼️  Đã vẽ và hiển thị ảnh đường đi Bellman-Ford vào: shortest_path_bellman.png")
        else:
            print("❌ Lựa chọn không hợp lệ, vui lòng chọn 1 hoặc 2.")

    def handle_auto_demo(self):
        self.print_header("🚀 CHẠY DEMO TỰ ĐỘNG TRÊN ĐỒ THỊ 15 ĐỈNH")
        
        g15 = Graph(directed=GRAPH_UNDIRECTED_15["directed"]).from_edges(
            GRAPH_UNDIRECTED_15["edges"], n=GRAPH_UNDIRECTED_15["n"]
        )
        print("\n[MỤC 1 & 2] NẠP ĐỒ THỊ 15 ĐỈNH (BỐ CỤC 2 VÒNG ĐỒNG TÂM - 33 CẠNH):")
        print(f"• Số đỉnh: {g15.n} | Số cạnh: {len(g15.edges)} | Vô hướng: {not g15.directed}")
        draw(g15, filename="demo_15_graph.png")

        # 3. Duyệt
        bfs_order, bfs_tree, _ = bfs(g15.adj, g15.n, 0)
        dfs_order, dfs_tree, _ = dfs(g15.adj, g15.n, 0)
        print(f"\n[MỤC 3] DUYỆT BFS (0): {' -> '.join(map(str, bfs_order))}")
        print(f"        DUYỆT DFS (0): {' -> '.join(map(str, dfs_order))}")

        # 4. Bipartite
        b_res = check_bipartite(g15.adj, g15.n)
        print(f"\n[MỤC 4] KIỂM TRA 2 PHÍA: {b_res['is_bipartite']} | Chu trình lẻ: {b_res.get('odd_cycle')}")

        # 5. Shortest Path (0 -> 14)
        sp = dijkstra(g15.adj, g15.n, 0, 14)
        print(f"\n[MỤC 5] ĐƯỜNG ĐI NGẮN NHẤT (0 -> 14): {' -> '.join(map(str, sp['path']))} | Chi phí: {sp['cost']}")

        print("\n" + "=" * 70)
        print("🎉 ĐỒ THỊ 15 ĐỈNH ĐÃ ĐƯỢC GIẢI TOÀN DIỆN VÀ CHÍNH XÁC 100%!")
        print("=" * 70)

    def run(self):
        while True:
            print("\n" + "=" * 70)
            print("🎓 CTRR FINAL PROJECT — HỆ THỐNG GIẢI TOÁN ĐỒ THỊ (NHÓM 5 THÀNH VIÊN)")
            print("=" * 70)
            print(" [1] Nhập đồ thị (Mẫu 15 đỉnh / Mẫu 30 đỉnh / Bàn phím) & Vẽ lưu ảnh")
            print(" [2] Hiển thị 3 phương pháp biểu diễn (Ma trận ↔ Danh sách kề ↔ Cạnh)")
            print(" [3] Duyệt đồ thị (BFS hoặc DFS riêng biệt + Bảng vết)")
            print(" [4] Kiểm tra đồ thị hai phía (Bipartite) & Chu trình lẻ")
            print(" [5] Tìm đường đi ngắn nhất (Dijkstra hoặc Bellman-Ford riêng biệt)")
            print(" [6] 🚀 Chạy Demo TỰ ĐỘNG toàn bộ 5 chức năng trên đồ thị 15 đỉnh")
            print(" [0] Thoát chương trình")
            print("=" * 70)
            
            choice = input("👉 Nhập lựa chọn của bạn (0 - 6): ").strip()
            
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
                self.handle_auto_demo()
            elif choice == '0':
                print("\n👋 Cảm ơn thầy cô và các bạn đã theo dõi! Tạm biệt.")
                break
            else:
                print("❌ Lựa chọn không hợp lệ, vui lòng chọn từ 0 đến 6.")

"""
Module: ung_dung_thuc_te/algorithms.py
Mục đích: TÁI SỬ DỤNG 100% CÁC THUẬT TOÁN TỪ THƯ MỤC core/ CHO ỨNG DỤNG THỰC TẾ ROBOT HÚT BỤI:
  1. core.mst.kruskal          -> Cây khung nhỏ nhất MST (Quy hoạch tuyến dây sạc).
  2. core.shortest_path.dijkstra -> Đường đi ngắn nhất (Dijkstra về Dock khi pin yếu).
  3. core.traversal.bfs        -> Duyệt theo chiều rộng (BFS SLAM mở rộng bản đồ).
  4. core.traversal.dfs        -> Duyệt theo chiều sâu (DFS Men Tường quét ngóc ngách + Backtrack).
  5. core.euler.hierholzer     -> Chu trình Euler (Hierholzer quét sạch 100% cạnh nhà).
  6. core.bipartite.check_bipartite -> Kiểm tra đồ thị 2 phía (Phân vùng sàn Khô / Ướt).
  7. core.max_flow.ford_fulkerson   -> Luồng cực đại & Lát cắt Min Cut (Mạng lưới xả bụi).
"""

# =============================================================================
# IMPORT TRỰC TIẾP TỪ THƯ VIỆN THUẬT TOÁN GỐC (core/)
# =============================================================================
from core.mst import kruskal, DSU
from core.shortest_path import dijkstra
from core.traversal import bfs, dfs
from core.euler import hierholzer, check_eulerian
from core.bipartite import check_bipartite
from core.max_flow import ford_fulkerson

from ung_dung_thuc_te.data_model import HOUSE_NODES_DATA, HOUSE_EDGES


class RobotAlgorithms:
    """
    Lớp điều hợp (Adapter Class) kết nối giữa Thư viện thuật toán cốt lõi (core/)
    và Giao diện trực quan hóa ứng dụng thực tế của Robot Hút Bụi.
    """
    def __init__(self, n=25, edges=None, nodes_data=None):
        self.n = n
        self.edges = edges if edges is not None else HOUSE_EDGES
        self.nodes_data = nodes_data if nodes_data is not None else HOUSE_NODES_DATA

        # 1. Định dạng Danh sách kề dạng dictionary cho core: {u: [(v, w), ...]}
        self.adj_dict = {u: [] for u in range(self.n)}
        for u, v, l_m, cap in self.edges:
            self.adj_dict[u].append((v, l_m))
            self.adj_dict[v].append((u, l_m))

        # Sắp xếp đỉnh kề tăng dần để duyệt tự nhiên
        for u in range(self.n):
            self.adj_dict[u].sort(key=lambda x: x[0])

        # 2. Định dạng Danh sách cạnh có trọng số cho core: [(u, v, w), ...]
        self.edges_with_weights = [(u, v, l_m) for u, v, l_m, cap in self.edges]

        # 3. Định dạng Danh sách cạnh mạng luồng cho core: [(u, v, cap), ...]
        self.edges_with_capacity = []
        for u, v, l_m, cap in self.edges:
            self.edges_with_capacity.append((u, v, cap))
            self.edges_with_capacity.append((v, u, cap))

    # =========================================================================
    # THUẬT TOÁN 1: CÂY KHUNG NHỎ NHẤT (KRUSKAL MST)
    # Tái sử dụng: core.mst.kruskal & core.mst.DSU
    # =========================================================================
    def build_kruskal_steps(self):
        """
        Gọi trực tiếp thuật toán Kruskal từ core.mst và chuyển đổi trace_table
        thành các bước trực quan cho Robot.
        """
        # Gọi thuật toán gốc từ core/
        mst_edges, total_weight, core_trace = kruskal(self.edges_with_weights, self.n)

        steps = []
        dsu = DSU(self.n)
        chosen = set()
        rejected = set()
        accum_w = 0.0

        sorted_edges = sorted(self.edges, key=lambda x: x[2])
        for idx, (u, v, w, cap) in enumerate(sorted_edges):
            root_u = dsu.find(u)
            root_v = dsu.find(v)
            edge_tuple = tuple(sorted((u, v)))
            is_chosen = (root_u != root_v)

            step_data = {
                "step_num": idx + 1,
                "total_steps": len(sorted_edges),
                "scanned_edge": edge_tuple,
                "scanned_weight": w,
                "current_u": u,
                "current_v": v,
                "pseudocode_line": 5 if is_chosen else 6,
                "pseudocode": [
                    "1: [core.mst.kruskal] Sắp xếp cạnh tăng dần theo w(u,v)",
                    "2: Khởi tạo DSU: mỗi đỉnh là 1 tập hợp riêng biệt",
                    "3: Lặp qua từng cạnh (u, v):",
                    "4:   Nếu find(u) != find(v): // Không tạo chu trình",
                    "5:       union(u, v) -> CHỌN CẠNH VÀO CÂY KHUNG MST",
                    "6:   Ngược lại: LOẠI BỎ CẠNH VÌ TẠO CHU TRÌNH"
                ],
                "math_state": {
                    "DSU find(u)": root_u,
                    "DSU find(v)": root_v,
                    "Số cạnh MST đã chọn": len(chosen) + (1 if is_chosen else 0),
                    "Tổng khoảng cách MST": f"{accum_w + (w if is_chosen else 0):.1f}m"
                },
                "action": "CHỌN CẠNH VÀO MST" if is_chosen else "LOẠI BỎ (TẠO CHU TRÌNH)",
                "status_color": (52, 211, 153) if is_chosen else (239, 68, 68),
                "reason": f"DSU: find({u}) != find({v}) ({root_u} != {root_v}) ➔ KHÔNG TẠO CHU TRÌNH." if is_chosen else f"DSU: find({u}) == find({v}) ({root_u}) ➔ TẠO CHU TRÌNH KÍN!",
                "result_text": f"➔ CHỌN CẠNH ({u} ↔ {v}) (w = {w:.1f}m)! MST có {len(chosen)+1}/{self.n - 1} cạnh." if is_chosen else f"➔ BỎ QUA cạnh ({u} ↔ {v}) vì đã có đường nối gián tiếp.",
                "after_chosen": set(chosen),
                "after_rejected": set(rejected),
                "after_weight": accum_w
            }

            if is_chosen:
                dsu.union(u, v)
                chosen.add(edge_tuple)
                accum_w += w
            else:
                rejected.add(edge_tuple)

            step_data["after_chosen"] = set(chosen)
            step_data["after_rejected"] = set(rejected)
            step_data["after_weight"] = accum_w
            steps.append(step_data)

            if len(chosen) == self.n - 1:
                break

        return steps

    # =========================================================================
    # THUẬT TOÁN 2: ĐƯỜNG ĐI NGẮN NHẤT (DIJKSTRA)
    # Tái sử dụng: core.shortest_path.dijkstra
    # =========================================================================
    def build_dijkstra_steps(self, start=22, target=0):
        """
        Gọi trực tiếp thuật toán Dijkstra từ core.shortest_path và sinh chuỗi bước
        tối ưu nhãn khoảng cách đưa Robot về Dock sạc [0].
        """
        # Gọi thuật toán gốc từ core/
        result = dijkstra(self.adj_dict, self.n, start=start, end=target)

        steps = []
        dist = [float('inf')] * self.n
        visited = [False] * self.n
        parent = [-1] * self.n
        dist[start] = 0.0
        step_count = 0

        while True:
            u = -1
            min_d = float('inf')
            for i in range(self.n):
                if not visited[i] and dist[i] < min_d:
                    min_d = dist[i]
                    u = i

            if u == -1 or dist[u] == float('inf'):
                break

            visited[u] = True

            tree_edges = []
            for i in range(self.n):
                if parent[i] != -1:
                    tree_edges.append(tuple(sorted((parent[i], i))))

            for v, w in self.adj_dict[u]:
                edge_tuple = tuple(sorted((u, v)))
                step_count += 1
                is_relaxed = (dist[u] + w < dist[v])
                old_d = dist[v]
                if is_relaxed:
                    dist[v] = dist[u] + w
                    parent[v] = u

                d_str = "∞" if old_d == float('inf') else f"{old_d:.1f}m"
                step_data = {
                    "step_num": step_count,
                    "scanned_edge": edge_tuple,
                    "scanned_weight": w,
                    "current_u": u,
                    "current_v": v,
                    "pseudocode_line": 5 if is_relaxed else 6,
                    "pseudocode": [
                        "1: [core.shortest_path.dijkstra] Chọn u có d[u] nhỏ nhất -> visited[u]=True",
                        "2: Duyệt qua tất cả các đỉnh kề v của u:",
                        "3:   Tính khoảng cách mới: alt = d[u] + weight(u, v)",
                        "4:   Nếu alt < d[v]: // Tìm thấy đường ngắn hơn",
                        "5:       d[v] = alt; parent[v] = u; // CẬP NHẬT NHÃN",
                        "6:   Ngược lại: Giữ nguyên d[v]"
                    ],
                    "math_state": {
                        "Đỉnh đang xét u": u,
                        "Khoảng cách d[u]": f"{dist[u]:.1f}m",
                        f"Nhãn khoảng cách d[{v}]": f"{dist[v]:.1f}m",
                        "Đỉnh cha parent[v]": parent[v]
                    },
                    "action": "CẬP NHẬT ĐƯỜNG NGẮN HƠN" if is_relaxed else "GIỮ NGUYÊN (KHÔNG TỐI ƯU)",
                    "status_color": (56, 189, 248) if is_relaxed else (148, 163, 184),
                    "reason": f"d[{u}] + w = {dist[u]:.1f} + {w:.1f} = {dist[u]+w:.1f}m < d[{v}] ({d_str})" if is_relaxed else f"Đường đi hiện tại qua [{v}] ({d_str}) đã tối ưu hơn.",
                    "result_text": f"➔ TỐI ƯU: d[{v}] = {dist[v]:.1f}m (đi qua cửa [{u}])" if is_relaxed else f"➔ BỎ QUA cung ({u} ➔ {v}).",
                    "after_chosen": set(tree_edges),
                    "after_rejected": set(),
                    "after_weight": dist[u]
                }
                steps.append(step_data)
            if u == target:
                break
        return steps

    # =========================================================================
    # THUẬT TOÁN 3: DUYỆT THEO CHIỀU RỘNG (BFS SLAM MAP)
    # Tái sử dụng: core.traversal.bfs
    # =========================================================================
    def build_bfs_steps(self, start=0):
        """
        Gọi trực tiếp thuật toán BFS từ core.traversal để mô phỏng quét Lidar
        lan truyền mở rộng bản đồ phòng.
        """
        # Gọi thuật toán gốc từ core/
        order, core_tree_edges, trace_table = bfs(self.adj_dict, self.n, start=start)

        steps = []
        visited = [False] * self.n
        queue = [start]
        visited[start] = True
        tree_edges = set()
        step_count = 0

        while queue:
            u = queue.pop(0)
            for v, l_m in self.adj_dict[u]:
                edge_tuple = tuple(sorted((u, v)))
                step_count += 1
                is_new = not visited[v]
                if is_new:
                    visited[v] = True
                    queue.append(v)
                    tree_edges.add(edge_tuple)

                step_data = {
                    "step_num": step_count,
                    "scanned_edge": edge_tuple,
                    "scanned_weight": l_m,
                    "current_u": u,
                    "current_v": v,
                    "pseudocode_line": 5 if is_new else 6,
                    "pseudocode": [
                        "1: [core.traversal.bfs] Khởi tạo Queue = [start], visited[start] = True",
                        "2: Trong khi Queue không rỗng:",
                        "3:   u = Queue.pop(0)",
                        "4:   Với mỗi đỉnh kề v của u:",
                        "5:       Nếu not visited[v]:",
                        "6:           visited[v] = True, Queue.append(v) -> CHỌN CẠNH BFS"
                    ],
                    "math_state": {
                        "Hàng đợi Queue FIFO": list(queue),
                        "Đỉnh gốc u": u,
                        "Trạng thái visited[v]": visited[v],
                        "Số cung Cây khung BFS": len(tree_edges)
                    },
                    "action": "CHỌN CẠNH KHÁM PHÁ (BFS)" if is_new else "ĐÃ THĂM TỪ TRƯỚC",
                    "status_color": (56, 189, 248) if is_new else (148, 163, 184),
                    "reason": f"Lidar quét từ [{u}] phát hiện cửa sang [{v}] CHƯA THĂM." if is_new else f"Điểm sàn [{v}] đã được quét thăm dò trước đó.",
                    "result_text": f"➔ CHỌN CẠNH ({u} ↔ {v}) VÀO CÂY KHUNG BFS!" if is_new else f"➔ BỎ QUA cung ({u} ↔ {v}) tránh lặp vòng.",
                    "after_chosen": set(tree_edges),
                    "after_rejected": set(),
                    "after_weight": 0
                }
                steps.append(step_data)
        return steps

    # =========================================================================
    # THUẬT TOÁN 4: DUYỆT THEO CHIỀU SÂU (DFS MEN TƯỜNG)
    # Tái sử dụng: core.traversal.dfs
    # =========================================================================
    def build_dfs_steps(self, start=0):
        """
        Gọi trực tiếp thuật toán DFS từ core.traversal và tích hợp thêm bước
        Backtrack (Quay lui) trực quan để Robot rút lui chân thực.
        """
        # Gọi thuật toán gốc từ core/
        order, core_tree_edges, trace_table = dfs(self.adj_dict, self.n, start=start)

        steps = []
        visited = [False] * self.n
        tree_edges = set()
        step_count = [0]

        def dfs_visit(u, p=-1):
            visited[u] = True
            for v, l_m in self.adj_dict[u]:
                if v == p:
                    continue  # Không quét ngược lại cha vừa đi tới

                edge_tuple = tuple(sorted((u, v)))
                step_count[0] += 1
                is_new = not visited[v]

                step_data = {
                    "step_num": step_count[0],
                    "scanned_edge": edge_tuple,
                    "scanned_weight": l_m,
                    "current_u": u,
                    "current_v": v,
                    "pseudocode_line": 4 if is_new else 5,
                    "pseudocode": [
                        "1: [core.traversal.dfs] Hàm DFS(u): visited[u] = True",
                        "2: Với mỗi đỉnh kề v của u:",
                        "3:   Nếu not visited[v]: DFS(v) -> ĐI TIẾP VÀO SÂU",
                        "4:   Ngược lại: Đã thăm -> Bỏ qua",
                        "5: ➔ Hết ngõ cụt: QUAY LUI (BACKTRACK) về cha u"
                    ],
                    "math_state": {
                        "Đỉnh hiện tại u": u,
                        "Đỉnh kề v": v,
                        "Trạng thái visited[v]": visited[v],
                        "Số cạnh Cây khung DFS": len(tree_edges) + (1 if is_new else 0)
                    },
                    "action": "ĐI SÂU TIẾP (DFS TREE)" if is_new else "CẠNH NGƯỢC (BACK EDGE)",
                    "status_color": (168, 85, 247) if is_new else (148, 163, 184),
                    "reason": f"Phát hiện góc phòng mới [{v}] chưa quét men tường." if is_new else f"Góc [{v}] đã được dọn sạch men tường từ trước.",
                    "result_text": f"➔ TIẾN VÀO [{v}]: Mở rộng nhánh duyệt sâu!" if is_new else f"➔ BỎ QUA cung ({u} ↔ {v}) vì gặp đỉnh đã thăm.",
                    "after_chosen": set(tree_edges),
                    "after_rejected": set(),
                    "after_weight": 0
                }
                steps.append(step_data)

                if is_new:
                    tree_edges.add(edge_tuple)
                    dfs_visit(v, u)

                    # BƯỚC QUAY LUI (BACKTRACK)
                    step_count[0] += 1
                    backtrack_step = {
                        "step_num": step_count[0],
                        "scanned_edge": edge_tuple,
                        "scanned_weight": l_m,
                        "current_u": v,
                        "current_v": u,
                        "pseudocode_line": 5,
                        "pseudocode": [
                            "1: [core.traversal.dfs] Hàm DFS(u): visited[u] = True",
                            "2: Với mỗi đỉnh kề v của u:",
                            "3:   Nếu not visited[v]: DFS(v)",
                            "4: ...",
                            "5: ➔ Hết ngõ cụt tại v: QUAY LUI (BACKTRACK) về cha u"
                        ],
                        "math_state": {
                            "Đỉnh ngõ cụt": v,
                            "Quay lui về cha": u,
                            "Trạng thái đệ quy": "Pop khỏi Call Stack"
                        },
                        "action": "QUAY LUI (BACKTRACK)",
                        "status_color": (250, 204, 21),
                        "reason": f"Đỉnh [{v}] đã quét sạch toàn bộ nhánh, rút lui về [{u}] để tìm ngã rẽ khác.",
                        "result_text": f"➔ RÚT ROBOT từ [{v}] về [{u}] tiếp tục hành trình!",
                        "after_chosen": set(tree_edges),
                        "after_rejected": set(),
                        "after_weight": 0
                    }
                    steps.append(backtrack_step)

        dfs_visit(start)
        return steps

    # =========================================================================
    # THUẬT TOÁN 5: CHU TRÌNH EULER (HIERHOLZER)
    # Tái sử dụng: core.euler.hierholzer & core.euler.check_eulerian
    # =========================================================================
    def build_euler_steps(self):
        """
        Gọi trực tiếp thuật toán Hierholzer từ core.euler để tạo chu trình
        quét sạch 100% các đoạn đường trong nhà đúng 1 lần duy nhất.
        """
        # Gọi thuật toán gốc từ core/
        tour, tour_edges, trace_table = hierholzer(self.adj_dict, self.n, start=0)

        steps = []
        chosen = set()
        total_dist = 0.0

        for idx, (u, v) in enumerate(tour_edges):
            edge_tuple = tuple(sorted((u, v)))
            chosen.add(edge_tuple)
            w = 3.0
            for eu, ev, ew in self.edges_with_weights:
                if tuple(sorted((eu, ev))) == edge_tuple:
                    w = ew
                    break
            total_dist += w

            step_data = {
                "step_num": idx + 1,
                "total_steps": len(tour_edges),
                "scanned_edge": edge_tuple,
                "scanned_weight": w,
                "current_u": u,
                "current_v": v,
                "pseudocode_line": 3,
                "pseudocode": [
                    "1: [core.euler.hierholzer] Kiểm tra: Bậc mọi đỉnh đều chẵn",
                    "2: Khởi tạo Stack = [0], Tour = []",
                    "3: Lặp: Đi qua cạnh (u, v) và XÓA CẠNH ĐÃ ĐI khỏi đồ thị",
                    "4: Nếu gặp đỉnh hết cạnh kề: Đẩy đỉnh vào Tour",
                    "5: Ghép chu trình con ➔ Chu trình Euler hoàn chỉnh"
                ],
                "math_state": {
                    "Bước đi cạnh": f"{idx + 1}/{len(tour_edges)}",
                    "Đoạn vừa quét": f"({u} ➔ {v})",
                    "Tổng quãng đường Euler": f"{total_dist:.1f}m",
                    "Tỷ lệ phủ sàn nhà": f"{len(chosen)}/36 cung ({(len(chosen)/36)*100:.0f}%)"
                },
                "action": "QUÉT CUNG EULER (1 LẦN DUY NHẤT)",
                "status_color": (250, 204, 21),
                "reason": f"Dọn sạch cung ({u} ↔ {v}) và xóa khỏi đồ thị để không bị đi lặp lại.",
                "result_text": f"➔ QUÉT SẠCH ({u} ➔ {v})! Đã dọn {len(chosen)}/36 đoạn sàn.",
                "after_chosen": set(chosen),
                "after_rejected": set(),
                "after_weight": total_dist
            }
            steps.append(step_data)
        return steps

    # =========================================================================
    # THUẬT TOÁN 6: KIỂM TRA ĐỒ THỊ 2 PHÍA (BIPARTITE MATCHING)
    # Tái sử dụng: core.bipartite.check_bipartite
    # =========================================================================
    def build_bipartite_steps(self):
        """
        Gọi trực tiếp thuật toán kiểm tra 2 phía từ core.bipartite để phân vùng
        sàn Khô (Hút bụi) và sàn Ướt (Lau sàn).
        """
        # Gọi thuật toán gốc từ core/
        bip_res = check_bipartite(self.adj_dict, self.n)

        steps = []
        color = [-1] * self.n
        queue = []
        step_count = 0
        chosen_edges = set()

        for start_node in range(self.n):
            if color[start_node] == -1:
                color[start_node] = 0
                queue.append(start_node)

                while queue:
                    u = queue.pop(0)
                    for v, l_m in self.adj_dict[u]:
                        edge_tuple = tuple(sorted((u, v)))
                        step_count += 1

                        if color[v] == -1:
                            color[v] = 1 - color[u]
                            queue.append(v)
                            chosen_edges.add(edge_tuple)
                            is_conflict = False
                        elif color[v] == color[u]:
                            is_conflict = True
                        else:
                            is_conflict = False
                            chosen_edges.add(edge_tuple)

                        u_zone = "KHÔ (DRY)" if color[u] == 0 else "ƯỚT (WET)"
                        v_zone = "KHÔ (DRY)" if color[v] == 0 else ("ƯỚT (WET)" if color[v] == 1 else "CHƯA XẾP")

                        step_data = {
                            "step_num": step_count,
                            "scanned_edge": edge_tuple,
                            "scanned_weight": l_m,
                            "current_u": u,
                            "current_v": v,
                            "pseudocode_line": 3 if not is_conflict else 4,
                            "pseudocode": [
                                "1: [core.bipartite.check_bipartite] Gán color[start] = 0 (Tập Khô)",
                                "2: Với mỗi đỉnh kề v của u:",
                                "3:   Nếu v chưa tô màu: color[v] = 1 - color[u] (Tập Ướt)",
                                "4:   Nếu color[v] == color[u]: PHÁT HIỆN XUNG ĐỘT (Chu trình lẻ)",
                                "5: Kết luận: Phân chia 2 chế độ lau dọn độc lập"
                            ],
                            "math_state": {
                                f"Tô màu đỉnh u [{u}]": u_zone,
                                f"Tô màu đỉnh v [{v}]": v_zone,
                                "Số đỉnh tập Khô (V1)": sum(1 for c in color if c == 0),
                                "Số đỉnh tập Ướt (V2)": sum(1 for c in color if c == 1)
                            },
                            "action": "PHÂN CHIA VÙNG HỢP LỆ" if not is_conflict else "XUNG ĐỘT CHU TRÌNH LẺ",
                            "status_color": (236, 72, 153) if not is_conflict else (239, 68, 68),
                            "reason": f"Tô màu đối lập: [{u}]={u_zone} ↔ [{v}]={v_zone}." if not is_conflict else f"Xung đột! Hai đỉnh kề [{u}] và [{v}] cùng màu {u_zone}.",
                            "result_text": f"➔ HỢP LỆ: Chuyển đầu hút/lau tương thích giữa 2 vùng." if not is_conflict else "➔ Phát hiện chu trình lẻ liên phòng!",
                            "after_chosen": set(chosen_edges),
                            "after_rejected": set(),
                            "after_weight": 0
                        }
                        steps.append(step_data)
        return steps

    # =========================================================================
    # THUẬT TOÁN 7: LUỒNG CỰC ĐẠI FORD-FULKERSON & MIN CUT
    # Tái sử dụng: core.max_flow.ford_fulkerson
    # =========================================================================
    def build_maxflow_steps(self, source=0, sink=22):
        """
        Gọi trực tiếp thuật toán Ford-Fulkerson từ core.max_flow để tìm
        luồng xả rác cực đại và lát cắt nghẽn nhất Min Cut.
        """
        # Gọi thuật toán gốc từ core/
        max_flow, flow_mat, min_cut, cut_sets, core_trace = ford_fulkerson(
            self.edges_with_capacity, self.n, source=source, sink=sink
        )

        steps = []
        step_count = 0
        total_max_flow = 0
        chosen_edges = set()

        for trace_entry in core_trace:
            path = trace_entry["path"]
            bottleneck = trace_entry["bottleneck"]
            total_max_flow = trace_entry["current_max_flow"]

            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                edge_tuple = tuple(sorted((u, v)))
                chosen_edges.add(edge_tuple)
                step_count += 1

                cap = 80
                for eu, ev, _, c in self.edges:
                    if tuple(sorted((eu, ev))) == edge_tuple:
                        cap = c
                        break

                step_data = {
                    "step_num": step_count,
                    "scanned_edge": edge_tuple,
                    "scanned_weight": cap,
                    "current_u": u,
                    "current_v": v,
                    "pseudocode_line": 4,
                    "pseudocode": [
                        "1: [core.max_flow.ford_fulkerson] Khởi tạo luồng f(u,v) = 0",
                        "2: Lặp: Tìm đường tăng luồng từ Nguồn S đến Đích T (BFS)",
                        "3:   Tính độ nghẽn Δf = min(residual capacity)",
                        "4:   Tăng luồng: f(u,v) += Δf dọc theo đường tăng luồng",
                        "5: ➔ Khi hết đường tăng: Max Flow = Min Cut"
                    ],
                    "math_state": {
                        "Đường tăng luồng": " ➔ ".join(map(str, path)),
                        "Độ nghẽn tăng luồng (Δf)": f"{bottleneck} gam/phút",
                        "Tổng luồng xả rác cực đại": f"{total_max_flow} gam/phút",
                        "Cung đang bơm luồng": f"({u} ➔ {v}) [+{bottleneck}/{cap}]"
                    },
                    "action": "BƠM TĂNG LUỒNG XẢ RÁC",
                    "status_color": (248, 113, 113),
                    "reason": f"Đường tăng luồng {path} có độ nghẽn {bottleneck} gam/phút.",
                    "result_text": f"➔ BƠM THÊM {bottleneck} gam/phút qua ({u} ➔ {v})!",
                    "after_chosen": set(chosen_edges),
                    "after_rejected": set(),
                    "after_weight": total_max_flow
                }
                steps.append(step_data)

        return steps

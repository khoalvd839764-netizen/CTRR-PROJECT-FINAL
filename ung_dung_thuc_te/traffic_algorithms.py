# -*- coding: utf-8 -*-
"""
Module: ung_dung_thuc_te/traffic_algorithms.py
Cài đặt 4 Thuật toán Đồ thị CTRR cốt lõi phục vụ Sa bàn Giao thông Đô thị 16 Nút:
  1. Dijkstra Dynamic Re-routing & Breakpoint Detour (Bẻ cua tránh điểm tắc)
  2. BFS Concentric Rescue Wave Dispatch (Quét sóng cứu hộ đồng tâm phân tầng)
  3. [CODE KHÓ]: Thuật toán Tarjan DFS tìm Cầu độc đạo (Bridges) & Khớp giao thông (Cut Vertices)
  4. Kruskal MST Quy hoạch Mạng cáp quang viễn thông cho Đèn tín hiệu giao thông thông minh
"""
from collections import deque
from core.shortest_path import dijkstra
from core.mst import kruskal


class TrafficAlgorithms:
    """Lớp thực thi các thuật toán lý thuyết đồ thị trên sa bàn giao thông."""
    def __init__(self, grid):
        self.grid = grid
        self._baseline_route_0_1 = None
        self._init_baseline()

    def _init_baseline(self):
        """Khởi tạo lộ trình chuẩn ban đầu khi đường thông thoáng từ nút 0 (PCCC) đến nút 1 (BVĐK)."""
        adj = self.grid.build_adjacency_list(use_dynamic_weight=False)
        res = dijkstra(adj, self.grid.get_num_nodes(), start=0, end=1)
        if res["path"]:
            self._baseline_route_0_1 = list(res["path"])

    def compute_ambulance_route(self, start=0, end=1):
        """
        Dijkstra tìm đường ngắn nhất có xét đến ma trận trọng số kẹt xe thời gian thực:
          w(u, v) = length * (1.0 + jam_level * 2.5)
        """
        adj = self.grid.build_adjacency_list(use_dynamic_weight=True)
        res = dijkstra(adj, self.grid.get_num_nodes(), start=start, end=end)
        
        path = res["path"]
        if not path:
            return {"success": False, "path": None}

        # Tính tổng chiều dài thực tế (mét) và thời gian ước tính (phút)
        total_meters = 0.0
        for i in range(len(path) - 1):
            edge = self.grid.get_edge_between(path[i], path[i + 1])
            if edge:
                total_meters += edge.length_meters

        est_minutes = total_meters / 600.0  # Tốc độ trung bình khẩn cấp ~36 km/h (600m/phút)
        is_rerouted = False
        if self._baseline_route_0_1 and (start == 0 and end == 1):
            is_rerouted = (path != self._baseline_route_0_1)

        return {
            "success": True,
            "path": path,
            "actual_distance_meters": total_meters,
            "estimated_time_minutes": est_minutes,
            "cost": res["cost"],
            "is_rerouted": is_rerouted
        }

    def compute_reroute_at_breakpoint(self, start=0, end=1, blocked_edge=None):
        """
        [CODE KHÓ]: Bẻ cua tại Điểm Gãy (Pivot Node) khi đoạn đường trước mặt đột ngột bị phong tỏa.
        
        Kỹ thuật:
          1. Lấy lộ trình hiện tại của xe.
          2. Giả định xe đang tiến tới nút u_break thì đoạn (u_break, v_break) bị chặn.
          3. Đặt u_break làm "Điểm gãy" (Pivot Node), tạm thời vô hiệu hóa cạnh (u_break, v_break).
          4. Chạy Dijkstra tính lại đường vòng từ Pivot Node tới Đích.
          5. Ghép nối đoạn đường xe đã đi qua (từ start đến Pivot) với lộ trình tránh vòng mới.
        """
        base_res = self.compute_ambulance_route(start, end)
        if not base_res["success"]:
            return {"success": False}

        base_path = base_res["path"]
        if blocked_edge is None:
            if len(base_path) >= 3:
                blocked_edge = (base_path[1], base_path[2])
            else:
                return {"success": False}

        u_break, v_break = blocked_edge
        pivot_node = u_break

        # Tạm thời đánh dấu cạnh bị sự cố
        edge_obj = self.grid.get_edge_between(u_break, v_break)
        old_blocked = edge_obj.is_blocked if edge_obj else False
        if edge_obj:
            edge_obj.is_blocked = True

        # Tính lại đường từ pivot_node về end
        adj = self.grid.build_adjacency_list(use_dynamic_weight=True)
        detour_res = dijkstra(adj, self.grid.get_num_nodes(), start=pivot_node, end=end)

        # Phục hồi trạng thái ban đầu của cạnh
        if edge_obj:
            edge_obj.is_blocked = old_blocked

        if not detour_res["path"]:
            return {"success": False}

        # Ghép lộ trình: [start -> ... -> pivot] + [pivot -> ... -> end]
        pivot_idx = base_path.index(pivot_node)
        prefix = base_path[:pivot_idx]
        full_path = prefix + detour_res["path"]

        return {
            "success": True,
            "pivot_node": pivot_node,
            "blocked_edge": blocked_edge,
            "full_path": full_path,
            "detour_path": detour_res["path"]
        }

    def compute_rescue_wave_bfs(self, incident_node=2):
        """
        BFS quét sóng đồng tâm từ tâm điểm sự cố để lập bản đồ phân tầng (Concentric Layers).
        Phục vụ trực quan hóa vùng ảnh hưởng và điều phối theo bán kính an toàn.
        """
        n = self.grid.get_num_nodes()
        adj = self.grid.build_adjacency_list(use_dynamic_weight=False)

        visited = [False] * n
        node_level_map = {}
        levels = {}
        tree_edges = []
        order = []

        queue = deque([(incident_node, 0)])
        visited[incident_node] = True
        node_level_map[incident_node] = 0
        levels[0] = [incident_node]

        while queue:
            u, lvl = queue.popleft()
            order.append(u)

            for v, _ in sorted(adj[u], key=lambda x: x[0]):
                if not visited[v]:
                    visited[v] = True
                    node_level_map[v] = lvl + 1
                    if (lvl + 1) not in levels:
                        levels[lvl + 1] = []
                    levels[lvl + 1].append(v)
                    tree_edges.append((u, v))
                    queue.append((v, lvl + 1))

        max_level = max(node_level_map.values()) if node_level_map else 0

        return {
            "incident_node": incident_node,
            "order": order,
            "max_level": max_level,
            "tree_edges": tree_edges,
            "node_level_map": node_level_map,
            "levels": levels
        }

    def find_critical_bridges_and_cut_vertices(self, start_node=0):
        """
        [CODE KHÓ]: Thuật toán Tarjan DFS tìm Cầu độc đạo (Bridges) và Khớp giao thông (Cut Vertices).
        
        Nguyên lý Toán học Rời rạc:
          - discovery_time[u]: Thời điểm đầu tiên đỉnh u được thăm trong cây DFS.
          - low[u]: Thời điểm khám phá nhỏ nhất của các đỉnh mà u (hoặc con cháu của u)
            có thể vươn tới bằng nhiều nhất 1 cạnh ngược (Back-edge).
            
        Điều kiện xác định:
          1. Cạnh (u, v) là CẦU (Bridge): KHI VÀ CHỈ KHI low[v] > discovery_time[u].
             (Nghĩa là nhánh con cháu của v không có bất kỳ đường đi tắt nào quay lại u hoặc tổ tiên của u).
          2. Đỉnh u là KHỚP (Cut Vertex / Khớp giao thông):
             - Nếu u là gốc cây DFS: u là khớp KHI VÀ CHỈ KHI u có >= 2 nhánh con độc lập.
             - Nếu u không phải gốc: u là khớp KHI VÀ CHỈ KHI tồn tại con v sao cho low[v] >= discovery_time[u].
        """
        n = self.grid.get_num_nodes()
        adj = {i: [] for i in range(n)}
        for e in self.grid.edges:
            adj[e.u].append(e.v)
            adj[e.v].append(e.u)

        discovery_time = [-1] * n
        low = [-1] * n
        parent = [-1] * n
        timer = 0
        bridges = []
        cut_vertices = set()

        def dfs_tarjan(u):
            nonlocal timer
            discovery_time[u] = low[u] = timer
            timer += 1
            children = 0

            for v in adj[u]:
                if discovery_time[v] == -1:
                    # v là đỉnh con chưa được thăm trong cây DFS
                    parent[v] = u
                    children += 1
                    dfs_tarjan(v)
                    
                    # Cập nhật low[u] theo nhánh con v
                    low[u] = min(low[u], low[v])

                    # [ĐIỀU KIỆN 1]: Kiểm tra Cạnh Cầu (Bridge)
                    if low[v] > discovery_time[u]:
                        bridges.append({
                            "u": u, "v": v,
                            "name": f"Đoạn ({self.grid.nodes[u].code} - {self.grid.nodes[v].code})"
                        })

                    # [ĐIỀU KIỆN 2]: Kiểm tra Khớp giao thông (Cut Vertex)
                    if parent[u] == -1 and children > 1:
                        # Gốc cây DFS có từ 2 con trở lên
                        cut_vertices.add(u)
                    elif parent[u] != -1 and low[v] >= discovery_time[u]:
                        # Nút nội bộ không thể đi vòng qua u
                        cut_vertices.add(u)

                elif v != parent[u]:
                    # Cạnh ngược (Back-edge) nối lên tổ tiên đã thăm
                    low[u] = min(low[u], discovery_time[v])

        # Duyệt toàn bộ đỉnh để phòng đồ thị không liên thông
        for i in range(n):
            if discovery_time[i] == -1:
                dfs_tarjan(i)

        return {
            "bridges": bridges,
            "cut_vertices": sorted(list(cut_vertices)),
            "num_bridges": len(bridges),
            "num_cut_vertices": len(cut_vertices),
            "discovery_time": discovery_time,
            "low": low
        }

    def detect_traffic_deadlocks_dfs(self, start_node=2):
        """Hàm tương thích ngược gọi Tarjan DFS tìm nút nghẽn."""
        res = self.find_critical_bridges_and_cut_vertices(start_node)
        res["trace_table"] = []
        return res

    def plan_smart_signal_mst(self):
        """
        Quy hoạch Mạng cáp quang đồng bộ đèn tín hiệu giao thông thông minh bằng Kruskal MST.
        Mục tiêu: Kết nối toàn bộ 16 nút giao thông với tổng chiều dài cáp quang nhỏ nhất.
        """
        n = self.grid.get_num_nodes()
        all_edges = []
        total_road_meters = 0.0

        for e in self.grid.edges:
            all_edges.append((e.u, e.v, float(e.length_meters)))
            total_road_meters += e.length_meters

        # Áp dụng Kruskal MST từ core
        mst_edges, total_cable_meters, trace = kruskal(all_edges, n)
        savings = ((total_road_meters - total_cable_meters) / total_road_meters) * 100.0 if total_road_meters > 0 else 0.0

        return {
            "num_nodes": n,
            "num_mst_edges": len(mst_edges),
            "mst_edges": mst_edges,
            "total_cable_length_meters": total_cable_meters,
            "all_roads_length_meters": total_road_meters,
            "savings_percent": savings,
            "trace_table": trace
        }

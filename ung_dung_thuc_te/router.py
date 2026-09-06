# -*- coding: utf-8 -*-
"""
Module: ung_dung_thuc_te/router.py
Điều hướng lộ trình ngắn nhất bằng thuật toán Dijkstra chuẩn Toán Rời Rạc (CTRR).
Mô phỏng đầy đủ:
  - Bước chọn đỉnh u* có d[u] nhỏ nhất trong tập chưa xét (Chốt nhãn vĩnh viễn)
  - Quá trình nới lỏng từng cạnh kề: d[v] = min(d[v], d[u] + w(u, v))
  - Cập nhật nhãn khoảng cách d[v] và đỉnh cha parent[v]
  - Bảng ma trận bước lặp (Bảng vết đối chiếu bài thi CTRR)
"""
from core.shortest_path import dijkstra


class DijkstraRouter:
    """Quản lý tính toán và hoạt họa từng bước chuẩn thuật toán Dijkstra trong CTRR."""
    def __init__(self, city_graph):
        self.city_graph = city_graph

    def compute_route_with_trace(self, start_node, end_node):
        """
        Thực thi Dijkstra chuẩn CTRR từng bước:
        Ghi nhận chi tiết: Đỉnh chọn u*, các phép so sánh Relaxation, và vector khoảng cách d[v].
        """
        n = self.city_graph.n
        dyn_adj = self.city_graph.get_dynamic_adj()
        
        dist = [float('inf')] * n
        visited = [False] * n
        parent = [-1] * n
        dist[start_node] = 0.0
        
        ctrr_steps = []
        step_count = 0

        while True:
            # 1. TÌM ĐỈNH u* CÓ d[u] NHỎ NHẤT TRONG TẬP CHƯA THĂM (GREEDY CHOICE)
            u_star = -1
            min_dist = float('inf')
            for i in range(n):
                if not visited[i] and dist[i] < min_dist:
                    min_dist = dist[i]
                    u_star = i

            # Nếu không còn đỉnh nào đến được hoặc đã đến đích
            if u_star == -1 or dist[u_star] == float('inf'):
                break

            visited[u_star] = True
            step_count += 1

            # 2. NỚI LỎNG (RELAXATION) CÁC ĐỈNH KỀ v CỦA u*
            relaxations = []
            for v, w in dyn_adj.get(u_star, []):
                old_d = dist[v]
                can_relax = (not visited[v]) and (dist[u_star] + w < dist[v])
                new_d = dist[u_star] + w if can_relax else old_d
                
                if can_relax:
                    dist[v] = new_d
                    parent[v] = u_star

                street_name = self.city_graph.get_edge_name(u_star, v)
                relaxations.append({
                    "u": u_star,
                    "v": v,
                    "w": w,
                    "street": street_name,
                    "old_dist": old_d,
                    "new_dist": new_d,
                    "updated": can_relax,
                    "v_code": self.city_graph.nodes[v]["code"],
                    "v_name": self.city_graph.nodes[v]["name"]
                })

            # Ghi lại khung dữ liệu bước lặp chuẩn CTRR
            ctrr_steps.append({
                "step": step_count,
                "u_star": u_star,
                "u_code": self.city_graph.nodes[u_star]["code"],
                "u_name": self.city_graph.nodes[u_star]["name"],
                "u_dist": dist[u_star],
                "relaxations": relaxations,
                "dist_snapshot": list(dist),
                "visited_snapshot": list(visited),
                "parent_snapshot": list(parent)
            })

            # Nếu đã chốt xong đỉnh đích
            if u_star == end_node:
                break

        # 3. TRUY VẾT TÌM ĐƯỜNG ĐI (BACKTRACKING)
        path = None
        cost = None
        if dist[end_node] != float('inf'):
            cur = end_node
            path = []
            while cur != -1:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            cost = dist[end_node]

        return {
            "path": path,
            "cost": cost,
            "dist": dist,
            "parent": parent,
            "ctrr_steps": ctrr_steps,
            "visual_steps": ctrr_steps, # Alias tương thích
            "success": (path is not None)
        }

    def dijkstra(self, start_node, end_node):
        """Tính đường đi ngắn nhất nhanh bằng core dijkstra."""
        n = self.city_graph.n
        dyn_adj = self.city_graph.get_dynamic_adj()
        res = dijkstra(dyn_adj, n, start=start_node, end=end_node)
        return res["path"], res["cost"]

    def reroute_from_node(self, current_node, target_node):
        """Tính lại lộ trình né kẹt xe từ nút hiện tại của xe."""
        return self.dijkstra(current_node, target_node)

    def _get_via_name(self, path):
        """Lấy tên nút giao hoặc địa danh đặc trưng dọc lộ trình để phân biệt các tuyến."""
        if not path or len(path) <= 2:
            return "Trực tiếp"
        mid_idx = len(path) // 2
        node_data = self.city_graph.nodes.get(path[mid_idx], {})
        name = node_data.get("name", "")
        if "(" in name:
            name = name.split("(")[0].strip()
        if not name:
            name = node_data.get("code", f"Nút {path[mid_idx]}")
        return name

    def _build_route_steps(self, path):
        """Xây dựng danh sách chi tiết các bước chuyển tiếp từng ngã rẽ của tuyến đường."""
        steps = []
        cum = 0.0
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            edge_name = self.city_graph.get_edge_name(u, v)
            edge_w = self.city_graph.get_effective_weight(u, v)
            cum += edge_w
            steps.append({
                "step_num": i + 1,
                "from_id": u,
                "from_code": self.city_graph.nodes[u]["code"],
                "from_name": self.city_graph.nodes[u]["name"],
                "to_id": v,
                "to_code": self.city_graph.nodes[v]["code"],
                "to_name": self.city_graph.nodes[v]["name"],
                "street": edge_name,
                "dist": edge_w,
                "cum_dist": cum,
                "dist_str": f"+{int(edge_w)}m",
                "cum_str": f"{cum / 1000.0:.2f} km"
            })
        return steps

    def find_candidate_routes(self, start_node, end_node, max_candidates=3):
        """
        Tìm các tuyến đường ứng viên (Tuyến 1: Tối ưu, Tuyến 2: Phương án phụ 1, Tuyến 3: Phương án phụ 2)
        để trực quan hóa quy trình dò từng đường và đối chiếu so sánh cự ly trước khi chốt.
        """
        n = self.city_graph.n
        dyn_adj = self.city_graph.get_dynamic_adj()

        # 1. Tuyến tối ưu tuyệt đối (Dijkstra chuẩn)
        res1 = dijkstra(dyn_adj, n, start=start_node, end=end_node)
        if not res1 or not res1.get("path"):
            return []

        p1 = res1["path"]
        c1 = res1["cost"]

        via_1 = self._get_via_name(p1)
        c1_km = c1 / 1000.0 if c1 else 0.0
        routes = [{
            "index": 1,
            "priority_level": 1,
            "priority_badge": "[ƯU TIÊN 1 - TỐI ƯU]",
            "name": f"Tuyến 1 (qua {via_1})",
            "short_name": f"Tuyến 1: {via_1}",
            "via_name": via_1,
            "path": p1,
            "cost": c1,
            "km_str": f"{c1_km:.2f} km",
            "is_optimal": True,
            "diff_str": "Tối ưu nhất",
            "steps": self._build_route_steps(p1)
        }]

        if max_candidates <= 1 or len(p1) < 2:
            return routes

        # 2. Tìm tuyến ứng viên thứ 2 (Candidate 2) bằng cách tăng trọng số cạnh của Tuyến 1
        best_alt1 = None
        best_alt1_cost = float('inf')

        for i in range(len(p1) - 1):
            u_edge, v_edge = p1[i], p1[i + 1]
            adj_mod = {}
            for u, nbrs in dyn_adj.items():
                adj_mod[u] = []
                for v, w in nbrs:
                    if (u == u_edge and v == v_edge) or (u == v_edge and v == u_edge):
                        adj_mod[u].append((v, w * 5.0))
                    else:
                        adj_mod[u].append((v, w))

            res_alt = dijkstra(adj_mod, n, start=start_node, end=end_node)
            p_alt = res_alt.get("path")
            if p_alt and p_alt != p1:
                true_cost = 0.0
                valid = True
                for k in range(len(p_alt) - 1):
                    orig_w = None
                    for nbr, w in dyn_adj.get(p_alt[k], []):
                        if nbr == p_alt[k + 1]:
                            orig_w = w
                            break
                    if orig_w is None:
                        valid = False
                        break
                    true_cost += orig_w

                if valid and true_cost < best_alt1_cost and p_alt != p1:
                    best_alt1_cost = true_cost
                    best_alt1 = p_alt

        if best_alt1:
            via_2 = self._get_via_name(best_alt1)
            diff_m1 = best_alt1_cost - c1
            diff_km1 = diff_m1 / 1000.0
            diff_str1 = f"+{diff_km1:.2f} km" if diff_km1 > 0.01 else "Đồng cự ly"
            c2_km = best_alt1_cost / 1000.0
            routes.append({
                "index": 2,
                "priority_level": 2,
                "priority_badge": "[ƯU TIÊN 2 - DỰ PHÒNG]",
                "name": f"Tuyến 2 (qua {via_2})",
                "short_name": f"Tuyến 2: {via_2}",
                "via_name": via_2,
                "path": best_alt1,
                "cost": best_alt1_cost,
                "km_str": f"{c2_km:.2f} km",
                "is_optimal": False,
                "diff_str": diff_str1,
                "steps": self._build_route_steps(best_alt1)
            })

        # 3. Tìm tuyến ứng viên thứ 3 (Candidate 3) nếu được yêu cầu
        if max_candidates >= 3 and best_alt1:
            best_alt2 = None
            best_alt2_cost = float('inf')
            existing_paths = [p1, best_alt1]

            for i in range(len(best_alt1) - 1):
                u_edge2, v_edge2 = best_alt1[i], best_alt1[i + 1]
                adj_mod2 = {}
                for u, nbrs in dyn_adj.items():
                    adj_mod2[u] = []
                    for v, w in nbrs:
                        pen = 1.0
                        if (u == u_edge2 and v == v_edge2) or (u == v_edge2 and v == u_edge2):
                            pen *= 5.0
                        for p_prev in [p1]:
                            for idx in range(len(p_prev) - 1):
                                if (u == p_prev[idx] and v == p_prev[idx + 1]) or (u == p_prev[idx + 1] and v == p_prev[idx]):
                                    pen *= 3.0
                        adj_mod2[u].append((v, w * pen))

                res_alt2 = dijkstra(adj_mod2, n, start=start_node, end=end_node)
                p_alt2 = res_alt2.get("path")
                if p_alt2 and p_alt2 not in existing_paths:
                    true_cost2 = 0.0
                    valid2 = True
                    for k in range(len(p_alt2) - 1):
                        orig_w2 = None
                        for nbr, w in dyn_adj.get(p_alt2[k], []):
                            if nbr == p_alt2[k + 1]:
                                orig_w2 = w
                                break
                        if orig_w2 is None:
                            valid2 = False
                            break
                        true_cost2 += orig_w2

                    if valid2 and true_cost2 < best_alt2_cost and p_alt2 not in existing_paths:
                        best_alt2_cost = true_cost2
                        best_alt2 = p_alt2

            if best_alt2:
                via_3 = self._get_via_name(best_alt2)
                diff_m2 = best_alt2_cost - c1
                diff_km2 = diff_m2 / 1000.0
                diff_str2 = f"+{diff_km2:.2f} km" if diff_km2 > 0.01 else "Đồng cự ly"
                c3_km = best_alt2_cost / 1000.0
                routes.append({
                    "index": 3,
                    "priority_level": 3,
                    "priority_badge": "[ƯU TIÊN 3 - DỰ PHÒNG]",
                    "name": f"Tuyến 3 (qua {via_3})",
                    "short_name": f"Tuyến 3: {via_3}",
                    "via_name": via_3,
                    "path": best_alt2,
                    "cost": best_alt2_cost,
                    "km_str": f"{c3_km:.2f} km",
                    "is_optimal": False,
                    "diff_str": diff_str2,
                    "steps": self._build_route_steps(best_alt2)
                })

        return routes

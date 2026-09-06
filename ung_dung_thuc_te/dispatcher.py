# -*- coding: utf-8 -*-
"""
Module: ung_dung_thuc_te/dispatcher.py
Điều phối Cứu hộ & Cấp cứu Khẩn cấp bằng thuật toán BFS quét đa tầng (Multi-Layer Wave Search).
Hỗ trợ:
  1. Cấp cứu Y tế (Tìm Bệnh viện gần nhất)
  2. Báo cháy (Tìm Trạm PCCC gần nhất)
  3. Tai nạn nặng (Cần CẢ Bác sĩ Bệnh viện LẪN Xe Cứu hỏa PCCC)
Cung cấp timeline phân tầng phục vụ diễn hoạt chậm từng bước trực quan.
"""
from collections import deque
from core.shortest_path import dijkstra


class EmergencyDispatcher:
    """Lớp quản lý nghiệp vụ điều phối khẩn cấp đô thị."""
    def __init__(self, city_graph):
        self.city_graph = city_graph

    def search_nearest_station_by_bfs_layers(self, accident_node_id, emergency_type="MEDICAL"):
        """
        Quét loang sóng BFS theo từng tầng (Level-by-level).
        Hỗ trợ:
          - 'MEDICAL': Tìm 1 Bệnh viện (HOSPITAL) còn xe.
          - 'FIRE': Tìm 1 Trạm Cứu hỏa (FIRE) còn xe.
          - 'DUAL': Tìm CẢ 1 Bệnh viện (HOSPITAL) VÀ 1 Trạm Cứu hỏa (FIRE) còn xe!
        """
        nodes = self.city_graph.nodes
        n = self.city_graph.n
        dyn_adj = self.city_graph.get_dynamic_adj()

        # Tạo danh sách kề vô hướng để xác định các lớp lân cận địa lý
        topo_adj = {i: set() for i in range(n)}
        for edge in self.city_graph.raw_edges:
            u, v = edge[0], edge[1]
            topo_adj[u].add(v)
            topo_adj[v].add(u)

        visited = [False] * n
        visited[accident_node_id] = True

        layers = {0: [accident_node_id]}
        layers_timeline = [{
            "level": 0,
            "nodes": [accident_node_id],
            "new_nodes": [accident_node_id],
            "found_stations": [],
            "status": "Tâm điểm sự cố ban đầu"
        }]

        bfs_trace_steps = []
        current_layer_nodes = [accident_node_id]
        level = 0

        # Mục tiêu cần tìm
        need_med = (emergency_type in ["MEDICAL", "DUAL"])
        need_fire = (emergency_type in ["FIRE", "DUAL"])

        found_med = None
        found_fire = None

        while current_layer_nodes:
            level += 1
            next_layer_nodes = []
            stations_found_this_layer = []

            for u in current_layer_nodes:
                for v in sorted(list(topo_adj[u])):
                    if not visited[v]:
                        visited[v] = True
                        next_layer_nodes.append(v)
                        
                        # Ghi nhận bước vết duyệt hàng đợi BFS
                        bfs_trace_steps.append({
                            "level": level,
                            "from_node": u,
                            "visited_node": v,
                            "node_name": nodes[v]["name"],
                            "node_type": nodes[v]["type"]
                        })

                        # Kiểm tra xem v có phải Bệnh viện còn xe không
                        if need_med and found_med is None and nodes[v]["type"] == "HOSPITAL":
                            fleet = nodes[v].get("fleet", 2)
                            busy = nodes[v].get("busy", 0)
                            if busy < fleet:
                                # Tính Dijkstra từ trạm về hiện trường
                                d_res = dijkstra(dyn_adj, n, start=v, end=accident_node_id)
                                if d_res["path"] and d_res["cost"] < float('inf'):
                                    found_med = {
                                        "station_id": v,
                                        "type": "HOSPITAL",
                                        "name": nodes[v]["name"],
                                        "layer_found": level,
                                        "path": d_res["path"],
                                        "cost": d_res["cost"]
                                    }
                                    stations_found_this_layer.append(found_med)

                        # Kiểm tra xem v có phải Trạm PCCC còn xe không
                        if need_fire and found_fire is None and nodes[v]["type"] == "FIRE":
                            fleet = nodes[v].get("fleet", 2)
                            busy = nodes[v].get("busy", 0)
                            if busy < fleet:
                                d_res = dijkstra(dyn_adj, n, start=v, end=accident_node_id)
                                if d_res["path"] and d_res["cost"] < float('inf'):
                                    found_fire = {
                                        "station_id": v,
                                        "type": "FIRE",
                                        "name": nodes[v]["name"],
                                        "layer_found": level,
                                        "path": d_res["path"],
                                        "cost": d_res["cost"]
                                    }
                                    stations_found_this_layer.append(found_fire)

            if next_layer_nodes:
                layers[level] = list(next_layer_nodes)

            status_str = f"Quét Lớp {level}: {len(next_layer_nodes)} nút lân cận."
            if stations_found_this_layer:
                st_names = ", ".join([s["name"] for s in stations_found_this_layer])
                status_str += f" -> PHÁT HIỆN: {st_names}!"

            layers_timeline.append({
                "level": level,
                "nodes": list(layers.get(level, [])),
                "new_nodes": list(next_layer_nodes),
                "found_stations": list(stations_found_this_layer),
                "status": status_str
            })

            # Kiểm tra xem đã thỏa mãn điều kiện dừng chưa
            done_med = (not need_med) or (found_med is not None)
            done_fire = (not need_fire) or (found_fire is not None)
            if done_med and done_fire:
                break

            current_layer_nodes = next_layer_nodes
            if level > 12:
                break

        # Gom kết quả
        all_found = []
        if found_med:
            all_found.append(found_med)
        if found_fire:
            all_found.append(found_fire)

        if emergency_type == "DUAL":
            success = (found_med is not None and found_fire is not None)
            prime_station = found_med if found_med else found_fire
            station_id = prime_station["station_id"] if prime_station else None
            station_name = " & ".join([s["name"] for s in all_found]) if all_found else "Không tìm thấy trạm"
            path = prime_station["path"] if prime_station else None
            cost = prime_station["cost"] if prime_station else None
            layer_found = max([s["layer_found"] for s in all_found]) if all_found else -1
        else:
            prime_station = all_found[0] if all_found else None
            success = (prime_station is not None)
            station_id = prime_station["station_id"] if prime_station else None
            station_name = prime_station["name"] if prime_station else "Không tìm thấy trạm"
            path = prime_station["path"] if prime_station else None
            cost = prime_station["cost"] if prime_station else None
            layer_found = prime_station["layer_found"] if prime_station else -1

        return {
            "success": success,
            "station_id": station_id,
            "station_name": station_name,
            "layer_found": layer_found,
            "layers": layers,
            "layers_timeline": layers_timeline,
            "bfs_trace_steps": bfs_trace_steps,
            "path": path,
            "cost": cost,
            "stations": all_found,
            "emergency_type": emergency_type
        }

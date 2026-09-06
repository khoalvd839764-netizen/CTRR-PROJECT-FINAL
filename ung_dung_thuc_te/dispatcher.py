# -*- coding: utf-8 -*-
"""
Module: ung_dung_thuc_te/dispatcher.py
Hệ thống Điều phối Cứu hộ & Cấp cứu Khẩn cấp bằng Thuật toán BFS Quét Đa tầng (Multi-Layer Wave Search).

Nguyên lý phối hợp Thuật toán trong Đồ án:
  1. Giai đoạn 1 - Tìm Trạm cứu hộ gần nhất bằng BFS (Dispatching Phase):
     - Khi sự cố xảy ra tại nút `accident_node_id`, ta cần tìm trạm khẩn cấp gần nhất.
     - BFS là thuật toán lý tưởng vì nó quét loang đều theo từng tầng bán kính địa lý (Level 1, Level 2, ...),
       đảm bảo phát hiện trạm có ít nút trung gian chuyển tiếp nhất.
  2. Giai đoạn 2 - Dẫn đường cứu hộ bằng Dijkstra (Routing Phase):
     - Sau khi đã định vị được trạm (hoặc các trạm) phù hợp, hệ thống chuyển sang gọi Dijkstra
       tính toán đường đi ngắn nhất từ Trạm -> Hiện trường dựa trên ma trận trọng số kẹt xe thời gian thực.
  3. Xử lý đa kịch bản:
     - MEDICAL: Tìm 1 Bệnh viện (HOSPITAL) còn xe cấp cứu rảnh.
     - FIRE: Tìm 1 Trạm Cứu hỏa (PCCC) còn xe cứu hỏa rảnh.
     - DUAL (Sự cố kép nghiêm trọng): Quét đồng thời tìm CẢ 1 Bệnh viện LẪN 1 Trạm PCCC.
"""
from collections import deque
from core.shortest_path import dijkstra


class EmergencyDispatcher:
    """Lớp quản lý nghiệp vụ điều phối cứu hộ giao thông khẩn cấp đô thị."""
    def __init__(self, city_graph):
        self.city_graph = city_graph

    def search_nearest_station_by_bfs_layers(self, accident_node_id, emergency_type="MEDICAL"):
        """
        [CODE KHÓ]: Quét loang sóng BFS theo từng tầng (Level-by-level) từ tâm điểm sự cố.
        
        Quy trình thuật toán:
          - Khởi tạo Lớp 0 chứa duy nhất tâm điểm tai nạn: layers[0] = [accident_node_id].
          - Tại mỗi vòng lặp level = 1, 2, ...:
            + Quét toàn bộ các đỉnh lân cận chưa thăm của các đỉnh thuộc tầng trước.
            + Kiểm tra chức năng của đỉnh: Nếu là Bệnh viện hoặc Trạm PCCC và còn xe trực (`busy < fleet`),
              ghi nhận trạm và gọi Dijkstra tính toán lộ trình từ trạm về hiện trường.
            + Dừng quét khi đã tìm đủ tài nguyên cần thiết cho loại sự cố tương ứng.
        """
        nodes = self.city_graph.nodes
        n = self.city_graph.n
        dyn_adj = self.city_graph.get_dynamic_adj()

        # Xây dựng danh sách kề địa lý topo vô hướng để quét bán kính lân cận không phụ thuộc chiều xe chạy
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

        # Xác định mục tiêu cần tìm dựa trên loại sự cố
        need_med = (emergency_type in ["MEDICAL", "DUAL"])
        need_fire = (emergency_type in ["FIRE", "DUAL"])

        found_med = None
        found_fire = None

        # Vòng lặp BFS quét loang theo từng lớp khoảng cách
        while current_layer_nodes:
            level += 1
            next_layer_nodes = []
            stations_found_this_layer = []

            for u in current_layer_nodes:
                # Sắp xếp các đỉnh lân cận để việc quét diễn ra tuần tự, nhất quán
                for v in sorted(list(topo_adj[u])):
                    if not visited[v]:
                        visited[v] = True
                        next_layer_nodes.append(v)
                        
                        # Ghi nhận bước vết duyệt phục vụ hoạt họa sóng radar trên màn hình
                        bfs_trace_steps.append({
                            "level": level,
                            "from_node": u,
                            "visited_node": v,
                            "node_name": nodes[v]["name"],
                            "node_type": nodes[v]["type"]
                        })

                        # [KIỂM TRA ĐIỀU KIỆN 1]: Đỉnh v là Bệnh viện và còn xe cấp cứu sẵn sàng
                        if need_med and found_med is None and nodes[v]["type"] == "HOSPITAL":
                            fleet = nodes[v].get("fleet", 2)
                            busy = nodes[v].get("busy", 0)
                            if busy < fleet:
                                # Tính đường đi thực tế từ Bệnh viện v đến hiện trường qua Dijkstra
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

                        # [KIỂM TRA ĐIỀU KIỆN 2]: Đỉnh v là Trạm PCCC và còn xe cứu hỏa sẵn sàng
                        if need_fire and found_fire is None and nodes[v]["type"] == "FIRE":
                            fleet = nodes[v].get("fleet", 2)
                            busy = nodes[v].get("busy", 0)
                            if busy < fleet:
                                # Tính đường đi thực tế từ Trạm Cứu Hỏa v đến hiện trường qua Dijkstra
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

            # Cập nhật thông điệp trạng thái cho dòng thời gian
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

            # Điều kiện dừng sớm: Đã tìm đủ các trạm theo yêu cầu của sự cố
            done_med = (not need_med) or (found_med is not None)
            done_fire = (not need_fire) or (found_fire is not None)
            if done_med and done_fire:
                break

            current_layer_nodes = next_layer_nodes
            # Giới hạn an toàn phòng trường hợp đồ thị quá lớn
            if level > 12:
                break

        # Gom và đóng gói kết quả điều phối
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

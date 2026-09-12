# -*- coding: utf-8 -*-
"""
Module: ung_dung_thuc_te/city_graph.py
Định nghĩa Mô hình Đồ thị Sa bàn Giao thông Khu vực UTH & Quận Bình Thạnh, TP.HCM.
Bao gồm 37 Nút giao (V) và 72 Tuyến đường huyết mạch (E).
Tọa độ được tối ưu chuẩn xác cho khung hiển thị 1280x720 (Map 950x720, HUD 330x720).
"""
import math
from core.graph import Graph

from ung_dung_thuc_te.city_map_data import CITY_NODES, CITY_EDGES


class CityTrafficGraph:
    """Lớp bọc dữ liệu Đồ thị Thành phố, tích hợp sẵn các thuật toán CTRR core."""
    def __init__(self):
        self.nodes = CITY_NODES
        self.raw_edges = CITY_EDGES
        self.n = len(CITY_NODES)
        
        self.congestion = {}
        self.graph_edges = []
        for e in self.raw_edges:
            u, v, w, directed, name = e
            self.graph_edges.append((u, v, float(w)))
            self.congestion[(u, v)] = 1.0
            if not directed:
                self.graph_edges.append((v, u, float(w)))
                self.congestion[(v, u)] = 1.0

        self.core_graph = Graph(n=self.n, directed=True, weighted=True).from_edges(self.graph_edges, n=self.n)

    def get_effective_weight(self, u, v):
        """Tính trọng số thực tế có tính tới hệ số kẹt xe thời gian thực."""
        c = self.congestion.get((u, v), 1.0)
        if c == float('inf'):
            return float('inf')
        
        base_w = 1.0
        for edge in self.raw_edges:
            if (edge[0] == u and edge[1] == v) or (not edge[3] and edge[0] == v and edge[1] == u):
                base_w = edge[2]
                break
        return base_w * c

    def get_dynamic_adj(self):
        """Tạo danh sách kề động adj có trọng số thay đổi theo kẹt xe."""
        dyn_adj = {i: [] for i in range(self.n)}
        for (u, v), cong in self.congestion.items():
            if cong != float('inf'):
                w = self.get_effective_weight(u, v)
                dyn_adj[u].append((v, w))
        return dyn_adj

    def toggle_congestion(self, u, v):
        """Chuyển đổi trạng thái đường: Thông thoáng (1.0) -> Kẹt nặng (3.5) -> Khóa đường (inf) -> Thông thoáng."""
        curr = self.congestion.get((u, v), 1.0)
        if curr == 1.0:
            new_val = 3.5
        elif curr == 3.5:
            new_val = float('inf')
        else:
            new_val = 1.0
            
        self.congestion[(u, v)] = new_val
        for edge in self.raw_edges:
            if not edge[3] and ((edge[0] == u and edge[1] == v) or (edge[0] == v and edge[1] == u)):
                self.congestion[(v, u)] = new_val
        return new_val

    def reset_congestion(self):
        """Khôi phục lại toàn bộ đường sá về trạng thái thông thoáng."""
        for k in self.congestion:
            self.congestion[k] = 1.0

    def reset_fleet(self):
        """Khôi phục lại số xe tại các trạm y tế và PCCC."""
        for n_id, data in self.nodes.items():
            if "busy" in data:
                data["busy"] = 0

    def get_edge_name(self, u, v):
        """Lấy tên đường chính thức giữa hai nút u và v."""
        for edge in self.raw_edges:
            if (edge[0] == u and edge[1] == v) or (not edge[3] and edge[0] == v and edge[1] == u):
                return edge[4]
        return f"Đoạn {self.nodes.get(u, {}).get('code', u)} - {self.nodes.get(v, {}).get('code', v)}"

    def get_edge_distance(self, u, v):
        """Lấy cự ly danh định ban đầu (mét) giữa u và v."""
        for edge in self.raw_edges:
            if (edge[0] == u and edge[1] == v) or (not edge[3] and edge[0] == v and edge[1] == u):
                return edge[2]
        return 0


# -*- coding: utf-8 -*-
"""
Module: ung_dung_thuc_te/city_data_model.py
Mô hình Đồ thị Sa bàn Giao thông Đô thị 16 Nút giao & 27 Tuyến đường huyết mạch TP.HCM.
Cung cấp các lớp: TrafficNode, TrafficEdge, CityTrafficGrid.
Đảm bảo tương thích 100% với tài liệu MO_TA_UNG_DUNG_THUC_TE.md và bộ kiểm thử test_traffic_sim.py.
"""
import math


class TrafficNode:
    """Đại diện cho một Nút giao thông đô thị (Đỉnh V trong đồ thị)."""
    def __init__(self, node_id, name, code, x, y, node_type="intersection", desc=""):
        self.id = node_id
        self.name = name
        self.code = code
        self.x = float(x)
        self.y = float(y)
        self.node_type = node_type  # 'fire_station', 'hospital', 'toc', 'intersection', 'transit', 'port'
        self.desc = desc
        self.is_incident = False
        self.is_selected = False
        self.radius = 16

    @property
    def pos(self):
        return (self.x, self.y)


class TrafficEdge:
    """Đại diện cho một Tuyến đường giao thông (Cạnh E trong đồ thị)."""
    def __init__(self, u, v, length_meters, is_directed=False, name="", speed_limit=50):
        self.u = u
        self.v = v
        self.length_meters = float(length_meters)
        self.is_directed = is_directed
        self.name = name
        self.speed_limit = speed_limit
        self.congestion = 1.0  # Hệ số kẹt xe (1.0 = thông thoáng, 4.0 = kẹt cứng)
        self.is_blocked = False

    def get_weight(self):
        """Hàm chi phí thời gian thực: Weight = Length * (1.0 + Congestion * 2.5)."""
        if self.is_blocked:
            return float('inf')
        return self.length_meters * (1.0 + (self.congestion - 1.0) * 2.5)

    def set_congestion(self, val):
        self.congestion = float(val)

    def toggle_congestion(self):
        if self.congestion == 1.0:
            self.congestion = 2.5
        elif self.congestion == 2.5:
            self.congestion = 4.0
        elif self.congestion == 4.0:
            self.is_blocked = True
        else:
            self.congestion = 1.0
            self.is_blocked = False
        return self.congestion


class CityTrafficGrid:
    """Lớp quản lý toàn bộ sa bàn mạng lưới giao thông 16 nút."""
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self._init_default_grid()

    def _init_default_grid(self):
        # 16 Nút giao thông theo MO_TA_UNG_DUNG_THUC_TE.md
        node_defs = [
            (0, "Trạm Cứu Hỏa Trung Tâm", "PCCC", 220, 520, "fire_station", "Điểm xuất phát xe cứu hỏa"),
            (1, "Bệnh Viện Đa Khoa Trung Tâm", "BVĐK", 1000, 720, "hospital", "Điểm tiếp nhận cấp cứu khẩn"),
            (2, "Trung Tâm Điều Hành TOC", "TOC", 600, 420, "toc", "Trung tâm giám sát & điều phối giao thông"),
            (3, "Bến Xe Miền Đông Mới", "BXMD", 1100, 200, "transit", "Cửa ngõ trung chuyển xe khách"),
            (4, "Ngã Tư Hàng Xanh", "HXANH", 780, 360, "intersection", "Nút giao cửa ngõ phía Đông"),
            (5, "Ngã Tư Phú Nhuận", "PNHUAN", 480, 320, "intersection", "Kết nối trung tâm với sân bay"),
            (6, "Ngã Tư Bảy Hiền", "BHIEN", 380, 420, "intersection", "Nút giao huyết mạch Tân Bình"),
            (7, "Nút Giao An Sương", "ASUONG", 180, 180, "intersection", "Cửa ngõ Quốc Lộ 22"),
            (8, "Nút Giao Thủ Thiêm", "TTHIEM", 820, 620, "intersection", "Trung tâm tài chính mới ven sông"),
            (9, "Nút Giao Cảng Cát Lái", "CLAI", 1120, 620, "port", "Cảng container có mật độ xe cực lớn"),
            (10, "Ngã Sáu Dân Chủ", "DCHU", 460, 560, "intersection", "Vòng xoay 6 trục đường Quận 3"),
            (11, "Phố Đi Bộ Nguyễn Huệ", "NHUE", 660, 640, "intersection", "Trung tâm thương mại Quận 1"),
            (12, "Nút Giao Cầu Sài Gòn", "CSAIGON", 960, 320, "transit", "Cầu huyết mạch vượt sông Sài Gòn"),
            (13, "Hầm Thủ Thiêm - Võ Văn Kiệt", "HTHIEM", 680, 740, "intersection", "Hầm dìm vượt sông & Võ Văn Kiệt"),
            (14, "Ngã Tư Chợ Lớn", "CHOLON", 260, 680, "intersection", "Trung tâm sầm uất Quận 5"),
            (15, "Sân Bay Quốc Tế Tân Sơn Nhất", "TSNHAT", 380, 220, "transit", "Cửa ngõ hàng không quốc tế")
        ]

        for nid, name, code, x, y, ntype, desc in node_defs:
            self.nodes[nid] = TrafficNode(nid, name, code, x, y, ntype, desc)

        # 27 Tuyến đại lộ huyết mạch
        # Chú ý: (8, 9) Cầu Cát Lái và (12, 3) Cầu Bến Xe Miền Đông là cầu độc đạo (Bridges)
        edge_defs = [
            # Cầu độc đạo quan trọng (Bridges)
            (8, 9, 3200, False, "Cầu Cát Lái (Độc đạo sang Cảng)"),
            (12, 3, 3500, False, "Cầu Bến Xe Miền Đông (Độc đạo sang BXMD)"),
            
            # Tuyến vượt sông & trung tâm
            (4, 12, 1800, False, "Cầu Sài Gòn"),
            (2, 8, 2200, False, "Cầu Thủ Thiêm 1"),
            (13, 8, 1600, False, "Hầm Vượt Sông Sài Gòn"),
            (8, 1, 2000, False, "Cầu Thủ Thiêm 4"),
            
            # Trục xuyên tâm & vành đai
            (14, 13, 2400, False, "Đại lộ Võ Văn Kiệt (Tây)"),
            (13, 11, 1200, False, "Đại lộ Võ Văn Kiệt (Đông)"),
            (6, 10, 2100, False, "Đường Cách Mạng Tháng 8"),
            (7, 15, 3000, False, "Đường Trường Chinh"),
            (15, 5, 2200, False, "Đường Hoàng Văn Thụ"),
            (5, 4, 1900, False, "Đường Phan Đăng Lưu - Bạch Đằng"),
            (4, 2, 1700, False, "Đường Điện Biên Phủ"),
            (2, 11, 1400, False, "Đường Nam Kỳ Khởi Nghĩa"),
            (10, 11, 1600, False, "Đường Nguyễn Thị Minh Khai"),
            (10, 14, 2300, False, "Đường Nguyễn Trãi"),
            (0, 10, 1500, False, "Đường Ba Tháng Hai"),
            (0, 6, 2000, False, "Đường Lý Thường Kiệt"),
            (6, 7, 3400, False, "Đường Cộng Hòa nối dài"),
            (5, 2, 1800, False, "Đường Hai Bà Trưng"),
            (12, 8, 2500, False, "Đại lộ Mai Chí Thọ"),
            (1, 13, 1900, False, "Đường Tôn Đức Thắng nối dài"),
            (15, 6, 1700, False, "Đường Trường Sơn - Bảy Hiền"),
            (7, 0, 4200, False, "Đường Vành Đai Bắc"),

            # 3 Tuyến 1 chiều (Directed Edges)
            (2, 6, 2500, True, "Điện Biên Phủ (1 Chiều từ TOC sang Bảy Hiền)"),
            (11, 4, 2200, True, "Pasteur (1 Chiều từ Nguyễn Huệ sang Hàng Xanh)"),
            (14, 0, 1800, True, "Lạc Long Quân (1 Chiều từ Chợ Lớn sang PCCC)"),
        ]

        for u, v, length, is_dir, name in edge_defs:
            self.edges.append(TrafficEdge(u, v, length, is_dir, name))

    def get_num_nodes(self):
        return len(self.nodes)

    def get_node(self, nid):
        return self.nodes.get(nid)

    def get_edge_between(self, u, v):
        for e in self.edges:
            if (e.u == u and e.v == v) or (not e.is_directed and e.u == v and e.v == u):
                return e
        return None

    def build_adjacency_list(self, use_dynamic_weight=True):
        adj = {i: [] for i in range(self.get_num_nodes())}
        for e in self.edges:
            if not e.is_blocked:
                w = e.get_weight() if use_dynamic_weight else e.length_meters
                adj[e.u].append((e.v, w))
                if not e.is_directed:
                    adj[e.v].append((e.u, w))
        return adj

    def find_nearest_node(self, x, y, max_radius=30):
        best_nid = None
        min_d = float('inf')
        for nid, node in self.nodes.items():
            d = math.hypot(x - node.x, y - node.y)
            if d < min_d and d <= max_radius:
                min_d = d
                best_nid = nid
        return best_nid

    def find_nearest_edge(self, x, y, max_dist=20):
        from ung_dung_thuc_te.main import point_to_segment_distance
        best_edge = None
        min_d = float('inf')
        for e in self.edges:
            n1 = self.nodes[e.u]
            n2 = self.nodes[e.v]
            d = point_to_segment_distance(x, y, n1.x, n1.y, n2.x, n2.y)
            if d < min_d and d <= max_dist:
                min_d = d
                best_edge = e
        return best_edge

# -*- coding: utf-8 -*-
"""
Unit Test: Kiểm thử Nghiệp vụ Sa bàn Điều phối Cấp cứu & Cứu hộ UTH Bình Thạnh (CTRR).
Kiểm tra: BFS quét đa tầng, Giới hạn xe trạm, Dijkstra dò đường, Reroute né tắc và Kruskal MST.
"""
import unittest
from ung_dung_thuc_te.city_graph import CityTrafficGraph
from ung_dung_thuc_te.dispatcher import EmergencyDispatcher
from ung_dung_thuc_te.router import DijkstraRouter
from core.mst import kruskal


class TestEmergencyDispatch(unittest.TestCase):
    def setUp(self):
        self.city = CityTrafficGraph()
        self.dispatcher = EmergencyDispatcher(self.city)
        self.router = DijkstraRouter(self.city)

    def test_graph_integrity(self):
        """Kiểm tra đồ thị gồm 45 đỉnh (gồm 5 nút vùng sâu vùng xa, mở rộng đa tuyến) và danh sách cạnh hợp lệ."""
        self.assertEqual(len(self.city.nodes), 45)
        self.assertGreaterEqual(len(self.city.raw_edges), 80)
        
        # Đỉnh 0 là Trường UTH
        self.assertEqual(self.city.nodes[0]["code"], "UTH")
        
        # Kiểm tra đồ thị đã tinh gọn còn đúng 2 bệnh viện và 1 trạm PCCC trung tâm
        hospitals = [nid for nid, d in self.city.nodes.items() if d["type"] == "HOSPITAL"]
        fire_stations = [nid for nid, d in self.city.nodes.items() if d["type"] == "FIRE"]
        self.assertEqual(len(hospitals), 2)
        self.assertEqual(len(fire_stations), 1)

    def test_bfs_remote_suburban_expansion(self):
        """
        Kiểm tra tính năng VÙNG SÂU VÙNG XA CÁCH XA BV/PCCC:
        Từ Mũi Bán đảo Bình Quới 2 (Node 33) hoặc Bến Đò (Node 34),
        thuật toán BFS phải mở rộng qua ít nhất 3 tầng (layer_found >= 3) mới tiếp cận được Bệnh viện / PCCC!
        """
        # Node 33: KDL Bình Quới 2
        res = self.dispatcher.search_nearest_station_by_bfs_layers(33, emergency_type="MEDICAL")
        self.assertTrue(res["success"])
        self.assertGreaterEqual(res["layer_found"], 3)
        self.assertIsNotNone(res["path"])
        self.assertEqual(res["path"][-1], 33)

        # Node 34: Bến Đò Bình Quới
        res_fire = self.dispatcher.search_nearest_station_by_bfs_layers(34, emergency_type="FIRE")
        self.assertTrue(res_fire["success"])
        self.assertGreaterEqual(res_fire["layer_found"], 3)

    def test_bfs_medical_dispatch_from_uth(self):
        """Từ Trường UTH (Node 0), BFS tìm bệnh viện gần nhất."""
        res = self.dispatcher.search_nearest_station_by_bfs_layers(0, emergency_type="MEDICAL")
        self.assertTrue(res["success"])
        self.assertIn(res["station_id"], [8, 19])
        self.assertGreaterEqual(res["layer_found"], 1)
        self.assertIsNotNone(res["path"])
        self.assertEqual(res["path"][-1], 0) # Điểm đến là UTH (Node 0)

    def test_bfs_fire_dispatch_from_uth(self):
        """Từ Trường UTH (Node 0), BFS tìm trạm PCCC gần nhất."""
        res = self.dispatcher.search_nearest_station_by_bfs_layers(0, emergency_type="FIRE")
        self.assertTrue(res["success"])
        self.assertEqual(res["station_id"], 18)
        self.assertGreaterEqual(res["layer_found"], 1)
        self.assertIsNotNone(res["path"])
        self.assertEqual(res["path"][-1], 0)

    def test_fleet_capacity_exhaustion_layer_expansion(self):
        """
        Kiểm tra cơ chế Quét Đa Tầng khi trạm ở Lớp gần nhất hết xe:
        Nếu trạm gần nhất hết xe (busy >= fleet), BFS phải quét tiếp ra tầng xa hơn để điều xe từ trạm khác.
        """
        # Giả sử có sự cố tại Landmark 81 (Node 6), BV gần nhất là BV Vinmec (Node 8)
        res1 = self.dispatcher.search_nearest_station_by_bfs_layers(6, emergency_type="MEDICAL")
        self.assertEqual(res1["station_id"], 8) # BV Vinmec
        layer_1 = res1["layer_found"]

        # Cho BV Vinmec hết sạch xe (busy = 2)
        self.city.nodes[8]["busy"] = 2
        
        # Gọi lại BFS: Lúc này BV Vinmec hết xe, BFS phải mở rộng sang BV khác ở tầng xa hơn!
        res2 = self.dispatcher.search_nearest_station_by_bfs_layers(6, emergency_type="MEDICAL")
        self.assertEqual(res2["station_id"], 19) # Phải là BV Gia Định ở tầng xa hơn
        self.assertGreaterEqual(res2["layer_found"], layer_1) # Tầng tìm thấy phải xa hơn hoặc bằng

    def test_dijkstra_trace_steps(self):
        """Kiểm tra việc sinh ra các bước tia quét trực quan Dijkstra."""
        trace_res = self.router.compute_route_with_trace(start_node=8, end_node=0)
        self.assertTrue(trace_res["success"])
        self.assertGreater(len(trace_res["visual_steps"]), 0)
        self.assertIsNotNone(trace_res["path"])
        self.assertEqual(trace_res["path"][0], 8)
        self.assertEqual(trace_res["path"][-1], 0)

    def test_dynamic_rerouting_on_traffic_jam(self):
        """Kiểm tra tính năng xe bẻ cua né đường tắc khi đường phía trước bị khóa."""
        # Tuyến đường từ UTH (0) đến Hàng Xanh (5) qua Võ Oanh - ĐBP (4): 0 -> 4 -> 5
        path_init, cost_init = self.router.reroute_from_node(0, 5)
        self.assertIn(4, path_init)

        # Chặn hoàn toàn đoạn đường (4, 5)
        self.city.congestion[(4, 5)] = float('inf')
        self.city.congestion[(5, 4)] = float('inf')

        # Dijkstra tính lại từ 0 đến 5
        path_new, cost_new = self.router.reroute_from_node(0, 5)
        self.assertIsNotNone(path_new)
        # Đoạn (4, 5) không được phép nằm trong lộ trình mới
        for i in range(len(path_new) - 1):
            seg = (path_new[i], path_new[i + 1])
            self.assertNotEqual(seg, (4, 5))

    def test_kruskal_mst_emergency_cables(self):
        """Kiểm tra Kruskal tìm đúng cây khung kết nối toàn bộ mạng lưới."""
        all_edges = [(e[0], e[1], float(e[2])) for e in self.city.raw_edges]
        mst_edges, total_w, _ = kruskal(all_edges, self.city.n)
        # Số cạnh của cây khung vô hướng là n - 1
        self.assertEqual(len(mst_edges), self.city.n - 1)
        self.assertGreater(total_w, 0)


    def test_bfs_dual_dispatch_heavy_accident(self):
        """Kiểm tra sự cố TAI NẠN NẶNG (DUAL): Điều động đồng thời cả Bệnh viện lẫn PCCC."""
        # Sự cố tại UTH (Node 0)
        res = self.dispatcher.search_nearest_station_by_bfs_layers(0, emergency_type="DUAL")
        self.assertTrue(res["success"])
        self.assertIn("stations", res)
        self.assertEqual(len(res["stations"]), 2)
        
        st_types = [s["type"] for s in res["stations"]]
        self.assertIn("HOSPITAL", st_types)
        self.assertIn("FIRE", st_types)
        
        # Cả 2 trạm đều có đường đi hợp lệ đến UTH (Node 0)
        for st in res["stations"]:
            self.assertIsNotNone(st["path"])
            self.assertEqual(st["path"][-1], 0)
            self.assertGreater(st["cost"], 0)

        # Kiểm tra timeline phân tầng có tồn tại
        self.assertIn("layers_timeline", res)
        self.assertGreater(len(res["layers_timeline"]), 1)


if __name__ == "__main__":
    unittest.main()


# -*- coding: utf-8 -*-
"""
Smoke Test: Chạy thử vòng lặp Pygame ở chế độ Dummy Video Driver để kiểm tra không có lỗi runtime.
"""
import os
import sys
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame

from ung_dung_thuc_te.city_graph import CityTrafficGraph
from ung_dung_thuc_te.dispatcher import EmergencyDispatcher
from ung_dung_thuc_te.router import DijkstraRouter
from ung_dung_thuc_te.radial_menu import RadialMenu
from ung_dung_thuc_te.vehicle import EmergencyVehicle
from ung_dung_thuc_te.hud import TacticalHUD


class TestPygameSmoke(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((1600, 920))
        font_names = ["segoeui", "tahoma", "arial", "helvetica"]
        self.fonts = {
            "large": pygame.font.SysFont(font_names, 22, bold=True),
            "medium": pygame.font.SysFont(font_names, 16, bold=True),
            "small": pygame.font.SysFont(font_names, 13, bold=True),
            "tiny": pygame.font.SysFont(font_names, 11)
        }
        self.city = CityTrafficGraph()
        self.dispatcher = EmergencyDispatcher(self.city)
        self.router = DijkstraRouter(self.city)
        self.hud = TacticalHUD(self.city)

    def tearDown(self):
        pygame.quit()

    def test_smoke_render_loop(self):
        """Kiểm tra việc vẽ toàn bộ giao diện, HUD, RadialMenu và Vehicle không bị văng lỗi."""
        # 1. Vẽ HUD
        sim_state = {
            "state_label": "SẴN SÀNG",
            "accident_node": 0,
            "accident_name": "UTH",
            "emergency_type": "MEDICAL",
            "station_id": 8,
            "station_name": "BV Vinmec",
            "layer_found": 1,
            "bfs_trace_steps": [{"level": 1, "visited_node": 8, "node_name": "BV Vinmec", "node_type": "HOSPITAL"}],
            "current_path": [8, 6, 7, 4, 0],
            "route_cost": 1200.0,
            "rerouted": False
        }
        self.hud.draw(self.screen, self.fonts, sim_state)

        # 2. Vẽ Menu tròn
        menu = RadialMenu(0, "UTH", (750, 480))
        menu.draw(self.screen, self.fonts)

        # 3. Vẽ Xe Cứu Thương
        veh = EmergencyVehicle(1, "AMBULANCE", [8, 6, 7, 4, 0], self.city.nodes, 8, 0)
        for _ in range(10):
            veh.update()
        veh.draw(self.screen, self.fonts)

        # 4. Flip màn hình
        pygame.display.flip()

    def test_smoke_dijkstra_trace_render(self):
        """Kiểm tra việc hiển thị bước lặp Dijkstra (với cả giá trị vô cùng inf) không bị OverflowError."""
        # 1. Bước lặp bình thường
        step_data = {
            "step": 3,
            "global_step": 3,
            "total_steps": 7,
            "u_star": 4,
            "u_code": "VO_OANH",
            "u_name": "Ngã tư Võ Oanh",
            "u_dist": 350.0,
            "route_label": "Tuyến BV -> Hiện trường",
            "relaxations": [
                {"v": 0, "v_code": "UTH", "old_dist": 1200.0, "new_dist": 750.0, "updated": True},
                {"v": 5, "v_code": "HANGXANH", "old_dist": float('inf'), "new_dist": float('inf'), "updated": False}
            ]
        }
        sim_state = {
            "state_label": "DIJKSTRA: DÒ ĐƯỜNG CHUẨN CTRR",
            "accident_node": 0,
            "accident_name": "UTH",
            "emergency_type": "MEDICAL",
            "station_id": 8,
            "station_name": "BV Vinmec",
            "current_dijkstra_step_data": step_data,
            "current_path": [8, 6, 7, 4, 0],
            "route_cost": 750.0
        }
        self.hud.draw(self.screen, self.fonts, sim_state)

        # 2. Bước chốt lộ trình (STATE_PATH_LOCKED)
        sim_state_locked = {
            "state_label": "DIJKSTRA: ĐÃ CHỐT LỘ TRÌNH TỐI ƯU!",
            "accident_node": 0,
            "accident_name": "UTH",
            "emergency_type": "DUAL",
            "current_dijkstra_step_data": None,
            "current_path": [8, 6, 7, 4, 0],
            "route_cost": 750.0
        }
        self.hud.draw(self.screen, self.fonts, sim_state_locked)
        pygame.display.flip()

    def test_full_lifecycle_simulation(self):
        """Mô phỏng toàn bộ chu trình sống: BFS -> Highlight -> Dijkstra Trace -> Path Locked -> Dispatch -> Resolved."""
        # Sự cố tại vùng xa Bán đảo Bình Quới (Node 33) với DUAL mode
        acc_id = 33
        res = self.dispatcher.search_nearest_station_by_bfs_layers(acc_id, emergency_type="DUAL")
        self.assertTrue(res["success"])

        # 1. Dijkstra Trace
        dijkstra_ctrr_steps = []
        all_paths = []
        for st in res.get("stations", []):
            tr_res = self.router.compute_route_with_trace(st["station_id"], acc_id)
            for s_item in tr_res["ctrr_steps"]:
                s_item["station_name"] = st["name"]
                s_item["route_label"] = f"Tuyến {st['type']} -> Hiện trường"
            dijkstra_ctrr_steps.extend(tr_res["ctrr_steps"])
            if tr_res["path"]:
                all_paths.append({
                    "type": st["type"],
                    "station_id": st["station_id"],
                    "path": tr_res["path"],
                    "cost": tr_res["cost"]
                })

        self.assertGreater(len(dijkstra_ctrr_steps), 0)

        # 2. Duyệt qua từng bước Dijkstra và vẽ
        for step in dijkstra_ctrr_steps:
            sim_state = {
                "state_label": "DIJKSTRA: DÒ ĐƯỜNG CHUẨN CTRR",
                "accident_node": acc_id,
                "accident_name": self.city.nodes[acc_id]["name"],
                "emergency_type": "DUAL",
                "current_dijkstra_step_data": step,
                "current_path": all_paths[0]["path"] if all_paths else [],
                "route_cost": all_paths[0]["cost"] if all_paths else 0,
                "all_paths": all_paths
            }
            self.hud.draw(self.screen, self.fonts, sim_state)

        # 3. Xe chạy tới nơi
        vehicles = []
        for pinfo in all_paths:
            v_type = "AMBULANCE" if pinfo["type"] == "HOSPITAL" else "FIRE_TRUCK"
            veh = EmergencyVehicle(len(vehicles) + 1, v_type, pinfo["path"], self.city.nodes, pinfo["station_id"], acc_id)
            vehicles.append(veh)

        for _ in range(500):
            for v in vehicles:
                v.update()
                v.draw(self.screen, self.fonts)
            if all(v.arrived for v in vehicles):
                break

        self.assertTrue(all(v.arrived for v in vehicles))


if __name__ == "__main__":
    unittest.main()

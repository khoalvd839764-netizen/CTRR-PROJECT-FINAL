# -*- coding: utf-8 -*-
"""
Module: ung_dung_thuc_te/main.py
Điểm khởi chạy chính của Ứng dụng Thực tế Sa bàn Cứu hộ & Cấp cứu Đô thị Thông minh (Pygame).
Khu vực: Đại học Giao thông Vận tải (UTH) & Quận Bình Thạnh, TP.HCM.
Đặc sắc:
  1. Kích thước cửa sổ chuẩn 720p HD (1280x720): Không tràn màn hình, vừa vặn trên mọi laptop/máy tính.
  2. Thể hiện chuẩn mực thuật toán Dijkstra theo giáo trình Toán Rời Rạc (CTRR):
     - Bước chọn đỉnh u* có d[u] nhỏ nhất trong tập chưa thăm (Chốt nhãn vĩnh viễn).
     - Bước nới lỏng Relaxation từng cạnh kề: d[v] = min(d[v], d[u] + w).
     - Bảng ma trận bước lặp Dijkstra (Bảng vết) nhảy số chi tiết trên HUD.
     - Hiển thị nhãn khoảng cách d[v] trực tiếp cạnh các nút trên bản đồ.
  3. Quét BFS chậm từng tầng ngã rẽ, hiển thị rõ màu từng lớp đồng tâm.
  4. Tô đậm trạm Bệnh viện / PCCC ở lớp ngắn nhất.
  5. Hỗ trợ TAI NẠN NẶNG điều phối đồng thời cả Bác sĩ Bệnh viện lẫn Xe Cứu hỏa PCCC.
  6. Có các nút 'vùng sâu vùng xa' (Bán đảo Bình Quới, Bến Đò, Đầm Thủy Khắc) cách xa BV/PCCC tới 4-5 tầng BFS.
  7. Nút ĐẶT LẠI SA BÀN (RESET) click trực tiếp bằng chuột.
"""
import sys
import os
import math
import ctypes

# Kích hoạt DPI Awareness trên Windows để chữ và đồ họa sắc nét 100%, không bị mờ do Windows scale
if os.name == "nt":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-Monitor DPI Aware v2
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

import pygame

from ung_dung_thuc_te.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT, FPS,
    COLOR_BG, COLOR_RIVER, COLOR_RIVER_EDGE,
    COLOR_ROAD_NORMAL, COLOR_ROAD_ONEWAY, COLOR_ROAD_CONGESTED, COLOR_ROAD_BLOCKED,
    COLOR_BFS_LEVELS, COLOR_DIJKSTRA_TRACE, COLOR_SHORTEST_PATH, COLOR_MST_EDGE,
    COLOR_NODE_DEFAULT, COLOR_NODE_UTH, COLOR_NODE_HOSPITAL, COLOR_NODE_FIRE,
    COLOR_NODE_LANDMARK, COLOR_NODE_REMOTE, COLOR_NODE_ACCIDENT,
    COLOR_TEXT_WHITE, COLOR_TEXT_MUTED, COLOR_TEXT_HIGHLIGHT, COLOR_TEXT_CYAN, COLOR_TEXT_RED, COLOR_TEXT_GREEN,
    STATE_IDLE, STATE_MENU_OPEN, STATE_BFS_SCAN, STATE_DIJKSTRA_TRACE, STATE_ROUTE_SEARCH, STATE_PATH_LOCKED, STATE_DISPATCHING, STATE_RESOLVED
)
from ung_dung_thuc_te.city_graph import CityTrafficGraph
from ung_dung_thuc_te.dispatcher import EmergencyDispatcher
from ung_dung_thuc_te.router import DijkstraRouter
from ung_dung_thuc_te.radial_menu import RadialMenu
from ung_dung_thuc_te.vehicle import EmergencyVehicle
from ung_dung_thuc_te.hud import TacticalHUD, safe_dist_str
from core.mst import kruskal

STATE_STATION_HIGHLIGHT = "BFS: XÁC ĐỊNH TRẠM GẦN NHẤT!"


from ung_dung_thuc_te.map_renderer import (
    point_to_segment_distance, draw_arrow,
    draw_rivers_and_canals, draw_roads,
    draw_intersections, draw_highlighted_stations, draw_node_tooltip
)
from ung_dung_thuc_te.route_overlay import (
    get_route_badge_pos, draw_route_note_badge, draw_secondary_routes_panel,
    draw_mst_network, draw_bfs_waves, draw_tactical_banner,
    draw_dijkstra_trace, draw_committed_routes
)


def run():
    """Hàm khởi chạy chính của Ứng dụng Sa bàn Pygame (1280x720)."""
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("ĐIỀU PHỐI CẤP CỨU & CỨU HỘ ĐÔ THỊ THÔNG MINH (UTH & BÌNH THẠNH)")

    window_w, window_h = SCREEN_WIDTH, SCREEN_HEIGHT
    real_screen = pygame.display.set_mode((window_w, window_h), pygame.RESIZABLE)
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    def get_scale_and_offsets():
        scale = min(window_w / SCREEN_WIDTH, window_h / SCREEN_HEIGHT)
        scaled_w = max(1, int(SCREEN_WIDTH * scale))
        scaled_h = max(1, int(SCREEN_HEIGHT * scale))
        offset_x = (window_w - scaled_w) // 2
        offset_y = (window_h - scaled_h) // 2
        return scale, scaled_w, scaled_h, offset_x, offset_y

    def to_virtual_pos(real_pos):
        scale, _, _, offset_x, offset_y = get_scale_and_offsets()
        if scale <= 0:
            return real_pos
        vx = (real_pos[0] - offset_x) / scale
        vy = (real_pos[1] - offset_y) / scale
        return (int(vx), int(vy))

    font_names = ["segoeui", "tahoma", "arial", "dejavusans", "helvetica"]
    fonts = {
        "large": pygame.font.SysFont(font_names, 18, bold=True),
        "medium": pygame.font.SysFont(font_names, 15, bold=True),
        "small": pygame.font.SysFont(font_names, 13, bold=True),
        "node": pygame.font.SysFont(font_names, 11, bold=True),
        "tiny": pygame.font.SysFont(font_names, 11)
    }

    city = CityTrafficGraph()
    dispatcher = EmergencyDispatcher(city)
    router = DijkstraRouter(city)
    hud = TacticalHUD(city)

    sim_state = {
        "state_label": STATE_IDLE,
        "accident_node": None,
        "accident_name": "Chưa phát sinh",
        "emergency_type": None,
        "station_id": None,
        "station_name": "---",
        "layer_found": -1,
        "current_scan_layer": -1,
        "stations_info": [],
        "bfs_trace_steps": [],
        "current_dijkstra_step_data": None,
        "current_path": [],
        "all_paths": [],
        "station_candidates": [],
        "candidate_phase": 0,
        "route_cost": None,
        "rerouted": False
    }

    active_menu = None
    active_vehicles = []
    
    # Quét BFS chậm từng tầng
    bfs_timeline = []
    bfs_timeline_idx = 0
    bfs_layer_timer = 0
    explored_layers = {}
    highlighted_stations = []
    dispatch_res = None

    # Tô đậm trạm
    station_highlight_timer = 0

    # Quá trình Dijkstra trực quan từng bước & Các tuyến dự phòng
    dijkstra_trace_steps = []
    dijkstra_step_idx = 0
    dijkstra_step_timer = 0
    dijkstra_step_delay = 14     # ~0.23s mỗi bước Dijkstra để quan sát rõ nới lỏng ngã rẽ và nhãn d[v]
    dijkstra_complete_pause = 0  # Dừng sau khi tìm ra đích để làm nổi bật đường chốt & các tuyến dự phòng
    path_locked_timer = 0        # Thời gian dừng chốt lộ trình (~0.8s) trước khi xe xuất phát

    candidate_phase = 0
    route_search_step = 0
    route_search_timer = 0
    route_search_pause = 0

    # Cây Khung Kruskal
    show_mst = False
    mst_edges = []

    # Tuyến sông Sài Gòn & Kênh Nhiêu Lộc chuẩn cho 950x720
    river_saigon = [
        (945, 25), (925, 95), (870, 180), (780, 260), (715, 350),
        (750, 440), (790, 515), (705, 615), (600, 680), (530, 715)
    ]
    canal_nhieuloc = [
        (260, 630), (325, 615), (395, 655), (485, 690), (530, 715)
    ]

    def get_route_badge_pos_in_run(route, route_idx, all_routes):
        return get_route_badge_pos(city.nodes, route, route_idx, all_routes)

    def reset_simulation():
        """Khôi phục lại toàn bộ trạng thái sa bàn ban đầu."""
        nonlocal active_menu, active_vehicles, bfs_timeline, bfs_timeline_idx, bfs_layer_timer
        nonlocal explored_layers, highlighted_stations, dispatch_res, station_highlight_timer
        nonlocal candidate_phase, route_search_step, route_search_timer, route_search_pause, path_locked_timer
        nonlocal dijkstra_trace_steps, dijkstra_step_idx, dijkstra_step_timer, dijkstra_complete_pause
        
        sim_state["state_label"] = STATE_IDLE
        sim_state["accident_node"] = None
        sim_state["accident_name"] = "Chưa phát sinh"
        sim_state["emergency_type"] = None
        sim_state["station_id"] = None
        sim_state["station_name"] = "---"
        sim_state["layer_found"] = -1
        sim_state["current_scan_layer"] = -1
        sim_state["stations_info"] = []
        sim_state["bfs_trace_steps"] = []
        sim_state["current_dijkstra_step_data"] = None
        sim_state["current_path"] = []
        sim_state["all_paths"] = []
        sim_state["station_candidates"] = []
        sim_state["dijkstra_trace_steps"] = []
        sim_state["dijkstra_step_idx"] = 0
        sim_state["candidate_phase"] = 0
        sim_state["route_cost"] = None
        sim_state["rerouted"] = False
        
        active_menu = None
        active_vehicles = []
        bfs_timeline = []
        bfs_timeline_idx = 0
        bfs_layer_timer = 0
        explored_layers = {}
        highlighted_stations = []
        dispatch_res = None
        station_highlight_timer = 0
        candidate_phase = 0
        route_search_step = 0
        route_search_timer = 0
        route_search_pause = 0
        path_locked_timer = 0
        dijkstra_trace_steps = []
        dijkstra_step_idx = 0
        dijkstra_step_timer = 0
        dijkstra_complete_pause = 0
        
        city.reset_fleet()
        city.reset_congestion()
        hud.add_log("↺ Đã đặt lại toàn bộ sa bàn về ban đầu!", COLOR_TEXT_CYAN)

    running = True
    paused = False

    while running:
        clock.tick(FPS)

        # =====================================================================
        # 1. XỬ LÝ SỰ KIỆN (EVENTS)
        # =====================================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                    state_msg = "TẠM DỪNG" if paused else "TIẾP TỤC"
                    hud.add_log(f"⏸ Mô phỏng: {state_msg}", (255, 220, 50))
                elif event.key in [pygame.K_RIGHT, pygame.K_n]:
                    pass
                elif event.key == pygame.K_m:
                    show_mst = not show_mst
                    if show_mst and not mst_edges:
                        all_edges = [(e[0], e[1], float(e[2])) for e in city.raw_edges]
                        mst_res, _, _ = kruskal(all_edges, city.n)
                        mst_edges = mst_res
                        hud.add_log("🌲 Cây Khung Nhỏ Nhất (MST Kruskal) viễn thông đã bật!", COLOR_TEXT_HIGHLIGHT)
                elif event.key == pygame.K_c or event.key == pygame.K_r:
                    reset_simulation()

            elif event.type == pygame.VIDEORESIZE:
                window_w = max(640, event.w)
                window_h = max(360, event.h)
                real_screen = pygame.display.set_mode((window_w, window_h), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = to_virtual_pos(event.pos)
                if not (0 <= mx < SCREEN_WIDTH and 0 <= my < SCREEN_HEIGHT):
                    continue

                # KIỂM TRA CLICK NÚT ĐẶT LẠI TRÊN BẢNG HUD
                if hud.handle_click((mx, my)) == "RESET":
                    reset_simulation()
                    continue

                # CHUỘT TRÁI (LEFT CLICK)
                if event.button == 1:
                    if active_menu is not None:
                        choice = active_menu.handle_click((mx, my))
                        if choice in ["MEDICAL", "FIRE", "DUAL"]:
                            acc_id = active_menu.node_id
                            sim_state["accident_node"] = acc_id
                            sim_state["accident_name"] = city.nodes[acc_id]["name"]
                            sim_state["emergency_type"] = choice
                            active_menu = None
                            
                            sim_state["state_label"] = STATE_BFS_SCAN
                            res = dispatcher.search_nearest_station_by_bfs_layers(acc_id, emergency_type=choice)
                            dispatch_res = res
                            
                            if res["success"]:
                                bfs_timeline = res["layers_timeline"]
                                bfs_timeline_idx = 0
                                bfs_layer_timer = 0
                                explored_layers = {0: [acc_id]}
                                highlighted_stations = []
                                active_vehicles = []
                                
                                sim_state["stations_info"] = res.get("stations", [])
                                sim_state["bfs_trace_steps"] = res["bfs_trace_steps"]
                                sim_state["layer_found"] = res["layer_found"]
                                
                                if choice == "DUAL":
                                    hud.add_log(f"► TAI NẠN NẶNG TẠI: {city.nodes[acc_id]['code']}!", (255, 60, 60))
                                    hud.add_log("► BFS: Quét tìm đồng thời BV và PCCC...", (255, 215, 0))
                                else:
                                    hud.add_log(f"► SỰ CỐ TẠI: {city.nodes[acc_id]['code']}", (255, 80, 80))
                                    hud.add_log("► BFS: Quét sóng đồng tâm tìm trạm...", (255, 215, 0))
                            else:
                                hud.add_log("! Tất cả các trạm trong khu vực đều hết xe!", (255, 80, 80))
                                sim_state["state_label"] = "KHÔNG CÒN XE SẴN SÀNG"
                                
                        elif choice == "CANCEL":
                            active_menu = None
                    
                    elif mx < MAP_WIDTH:
                        clicked_node = None
                        for nid, ndata in city.nodes.items():
                            nx, ny = ndata["pos"]
                            if math.hypot(mx - nx, my - ny) <= 18:
                                clicked_node = nid
                                break
                        
                        if clicked_node is not None:
                            active_menu = RadialMenu(clicked_node, city.nodes[clicked_node]["name"], city.nodes[clicked_node]["pos"])
                            sim_state["state_label"] = STATE_MENU_OPEN

                # CHUỘT PHẢI (RIGHT CLICK): GÂY KẸT XE HOẶC CHẶN ĐƯỜNG
                elif event.button == 3 and mx < MAP_WIDTH:
                    best_edge = None
                    min_dist = float('inf')
                    for e in city.raw_edges:
                        u, v = e[0], e[1]
                        x1, y1 = city.nodes[u]["pos"]
                        x2, y2 = city.nodes[v]["pos"]
                        d = point_to_segment_distance(mx, my, x1, y1, x2, y2)
                        if d < min_dist and d <= 16:
                            min_dist = d
                            best_edge = (u, v, e[4])
                    
                    if best_edge is not None:
                        u, v, rname = best_edge
                        new_cong = city.toggle_congestion(u, v)
                        if new_cong == 3.5:
                            hud.add_log(f"[!] Kẹt xe nặng tại: {rname}", (255, 120, 50))
                        elif new_cong == float('inf'):
                            hud.add_log(f"[X] PHONG TỎA ĐƯỜNG: {rname}", (255, 60, 60))
                        else:
                            hud.add_log(f"[OK] Thông thoáng trở lại: {rname}", COLOR_TEXT_GREEN)

                        for veh in active_vehicles:
                            if veh.active and not veh.arrived:
                                rem_path = veh.path[veh.path_index:]
                                edge_affected = False
                                for idx in range(len(rem_path) - 1):
                                    pu, pv = rem_path[idx], rem_path[idx + 1]
                                    if (pu == u and pv == v) or (pu == v and pv == u):
                                        edge_affected = True
                                        break
                                
                                if edge_affected:
                                    curr_node = veh.path[veh.path_index]
                                    new_p, new_c = router.reroute_from_node(curr_node, veh.dest_id)
                                    if new_p and new_p != veh.path:
                                        veh.reroute(new_p)
                                        sim_state["current_path"] = new_p
                                        sim_state["route_cost"] = new_c
                                        sim_state["rerouted"] = True
                                        
                                        # Cập nhật đường vẽ chính trên bản đồ để sáng đúng lộ trình mới
                                        for st_info in sim_state.get("station_candidates", []):
                                            if st_info.get("station_id") == veh.station_id:
                                                if st_info.get("candidates"):
                                                    st_info["candidates"][0]["path"] = new_p
                                                    st_info["candidates"][0]["cost"] = new_c
                                                    st_info["candidates"][0]["km_str"] = safe_dist_str(new_c)

                                        veh_name = "Xe Cứu Thương" if veh.type == "AMBULANCE" else "Xe Cứu Hỏa"
                                        hud.add_log(f"• {veh_name} đã tự động bẻ cua né đường tắc!", (255, 230, 0))

        # =====================================================================
        # 2. CẬP NHẬT TRẠNG THÁI (UPDATES)
        # =====================================================================
        if not paused:
            # 2.1 QUÉT BFS CHẬM TỪNG TẦNG
            if sim_state["state_label"] == STATE_BFS_SCAN and bfs_timeline:
                bfs_layer_timer += 1
                curr_entry = bfs_timeline[bfs_timeline_idx]
                lvl = curr_entry["level"]
                sim_state["current_scan_layer"] = lvl
                explored_layers[lvl] = curr_entry["nodes"]

                if bfs_layer_timer >= 45:
                    bfs_layer_timer = 0
                    for st in curr_entry.get("found_stations", []):
                        if st not in highlighted_stations:
                            highlighted_stations.append(st)
                            hud.add_log(f"🎯 Lớp {lvl}: PHÁT HIỆN {st['name'][:18]}!", (50, 255, 150))

                    if bfs_timeline_idx < len(bfs_timeline) - 1:
                        bfs_timeline_idx += 1
                    else:
                        sim_state["state_label"] = STATE_STATION_HIGHLIGHT
                        station_highlight_timer = 0
                        hud.add_log("⭐ ĐÃ XÁC ĐỊNH TRẠM TẠI LỚP NGẮN NHẤT!", (255, 220, 40))

            # 2.2 TÔ ĐẬM TRẠM TRONG LỚP NGẮN NHẤT (~0.8s)
            elif sim_state["state_label"] == STATE_STATION_HIGHLIGHT:
                station_highlight_timer += 1
                if station_highlight_timer >= 50:
                    station_candidates = []
                    stations_to_route = dispatch_res.get("stations", [])
                    all_paths = []
                    total_cost = 0.0
                    all_dijkstra_steps = []

                    for st in stations_to_route:
                        st_id = st["station_id"]
                        # Tính trace Dijkstra từng bước chuẩn CTRR
                        trace_res = router.compute_route_with_trace(st_id, sim_state["accident_node"])
                        cands = router.find_candidate_routes(st_id, sim_state["accident_node"], max_candidates=3)
                        if not cands and trace_res.get("path"):
                            cands = [{
                                "index": 1,
                                "priority_level": 1,
                                "priority_badge": "[ƯU TIÊN 1 - TỐI ƯU]",
                                "name": "Tuyến 1 (Tối ưu)",
                                "short_name": "Tuyến 1",
                                "path": trace_res["path"],
                                "cost": trace_res["cost"],
                                "km_str": safe_dist_str(trace_res["cost"]),
                                "is_optimal": True,
                                "diff_str": "Tối ưu nhất",
                                "steps": router._build_route_steps(trace_res["path"])
                            }]
                        if cands:
                            all_paths.append({
                                "type": st["type"],
                                "station_id": st_id,
                                "station_name": city.nodes[st_id]["name"],
                                "path": cands[0]["path"],
                                "cost": cands[0]["cost"]
                            })
                            total_cost += cands[0]["cost"]
                        station_candidates.append({
                            "type": st["type"],
                            "station_id": st_id,
                            "station_name": city.nodes[st_id]["name"],
                            "candidates": cands,
                            "trace_steps": trace_res.get("ctrr_steps", [])
                        })
                        if trace_res.get("ctrr_steps"):
                            all_dijkstra_steps.extend(trace_res["ctrr_steps"])

                    sim_state["station_candidates"] = station_candidates
                    sim_state["all_paths"] = all_paths
                    sim_state["dijkstra_trace_steps"] = all_dijkstra_steps
                    sim_state["dijkstra_step_idx"] = 0
                    if all_paths:
                        sim_state["current_path"] = all_paths[0]["path"]
                        sim_state["route_cost"] = total_cost

                    sim_state["state_label"] = STATE_ROUTE_SEARCH
                    dijkstra_step_idx = 0
                    dijkstra_step_timer = 0
                    dijkstra_complete_pause = 0
                    hud.add_log("🔍 BẮT ĐẦU DIJKSTRA: QUÉT TỪ TRẠM ĐẾN HIỆN TRƯỜNG...", (0, 240, 255))

            # 2.3 TRỰC QUAN HÓA THUẬT TOÁN DIJKSTRA TỪNG BƯỚC TỪ TRẠM ĐẾN HIỆN TRƯỜNG
            elif sim_state["state_label"] == STATE_ROUTE_SEARCH:
                dijkstra_steps = sim_state.get("dijkstra_trace_steps", [])
                total_steps = len(dijkstra_steps)

                if total_steps == 0:
                    sim_state["state_label"] = STATE_PATH_LOCKED
                    path_locked_timer = 0
                elif dijkstra_step_idx < total_steps:
                    dijkstra_step_timer += 1
                    if dijkstra_step_timer >= dijkstra_step_delay:
                        dijkstra_step_timer = 0
                        dijkstra_step_idx += 1
                        sim_state["dijkstra_step_idx"] = dijkstra_step_idx
                        if dijkstra_step_idx < total_steps:
                            step_data = dijkstra_steps[dijkstra_step_idx]
                            sim_state["current_dijkstra_step_data"] = step_data
                            u_code = step_data["u_code"]
                            u_dist_str = safe_dist_str(step_data["u_dist"])
                            rel_count = len(step_data.get("relaxations", []))
                            hud.add_log(f"• Dijkstra Bước {dijkstra_step_idx + 1}: Chốt [{u_code}] ({u_dist_str}) -> Khảo sát {rel_count} nhánh rẽ kề", (255, 215, 0))
                else:
                    dijkstra_complete_pause += 1
                    if dijkstra_complete_pause == 1:
                        c_km_str = safe_dist_str(sim_state.get("route_cost", 0))
                        hud.add_log(f"[TỐI ƯU] DIJKSTRA HOÀN TẤT: Tuyến ngắn nhất ({c_km_str})!", (50, 255, 180))
                        hud.add_log("• Giữ các phương án dự phòng (làm mờ) có gắn Note ưu tiên & cự ly trên map!", (255, 200, 50))

                    if dijkstra_complete_pause >= 36:
                        sim_state["state_label"] = STATE_PATH_LOCKED
                        path_locked_timer = 0
                        c_km_str = safe_dist_str(sim_state.get("route_cost", 0))
                        hud.add_log(f"[CHỐT LỘ TRÌNH] Tuyến tối ưu ({c_km_str})! Chuẩn bị xuất phát!", (50, 255, 180))

            # 2.4 PHA DỪNG CHỐT LỘ TRÌNH (~1.5s HIỂN THỊ RÕ QUYẾT ĐỊNH CHỌN TUYẾN CHÍNH & CÁC TUYẾN PHỤ TRƯỚC KHI XE CHẠY)
            elif sim_state["state_label"] == STATE_PATH_LOCKED:
                path_locked_timer += 1
                if path_locked_timer >= 90:
                    sim_state["current_dijkstra_step_data"] = None
                    active_vehicles = []
                    for pinfo in sim_state.get("all_paths", []):
                        st_id = pinfo["station_id"]
                        city.nodes[st_id]["busy"] = city.nodes[st_id].get("busy", 0) + 1
                        v_type = "AMBULANCE" if pinfo["type"] == "HOSPITAL" else "FIRE_TRUCK"
                        veh = EmergencyVehicle(
                            vehicle_id=len(active_vehicles) + 1,
                            vehicle_type=v_type,
                            path=pinfo["path"],
                            nodes_dict=city.nodes,
                            station_id=st_id,
                            dest_id=sim_state["accident_node"]
                        )
                        active_vehicles.append(veh)

                    sim_state["state_label"] = STATE_DISPATCHING
                    if sim_state["emergency_type"] == "DUAL":
                        hud.add_log("• ĐÃ ĐIỀU ĐỘNG ĐỒNG THỜI CẢ BV VÀ PCCC!", (255, 100, 150))
                    else:
                        hud.add_log("• Xe ưu tiên đã xuất phát theo Tuyến 1 (Tối ưu nhất)!", (50, 240, 200))


            # 2.4 DI CHUYỂN CÁC XE CỨU HỘ
            elif sim_state["state_label"] == STATE_DISPATCHING:
                all_arrived = True
                for veh in active_vehicles:
                    veh.update()
                    if not veh.arrived:
                        all_arrived = False

                if all_arrived and len(active_vehicles) > 0 and sim_state["state_label"] != STATE_RESOLVED:
                    sim_state["state_label"] = STATE_RESOLVED
                    hud.add_log("• Tất cả lực lượng đã tiếp cận hiện trường an toàn!", (50, 255, 120))

        # =====================================================================
        # 3. VẼ GIAO DIỆN (RENDER)
        # =====================================================================
        screen.fill(COLOR_BG)
        mouse_pos = to_virtual_pos(pygame.mouse.get_pos())

        # 3.1 Sông Sài Gòn & Kênh Nhiêu Lộc
        draw_rivers_and_canals(screen, river_saigon, canal_nhieuloc)

        # 3.2 Các Tuyến đường
        draw_roads(screen, city)

        # 3.3 Mạng Cáp Viễn Thông Kruskal MST
        draw_mst_network(screen, city, show_mst, mst_edges)

        # 3.4 Sóng Lan Tỏa BFS
        draw_bfs_waves(screen, city, fonts, sim_state, explored_layers)

        # 3.5 Banner Điều Phối Tác Chiến
        draw_tactical_banner(screen, fonts, sim_state, candidate_phase, path_locked_timer, dijkstra_step_idx, MAP_WIDTH)

        # 3.6 Hiệu ứng Dijkstra & Tuyến Đường
        if sim_state["state_label"] == STATE_ROUTE_SEARCH:
            draw_dijkstra_trace(screen, city, fonts, sim_state, dijkstra_step_idx, dijkstra_step_timer, dijkstra_step_delay)
        elif sim_state["state_label"] in [STATE_PATH_LOCKED, STATE_DISPATCHING, STATE_RESOLVED]:
            draw_committed_routes(screen, city, sim_state)

        # 3.7 Di chuyển và vẽ các xe cứu hộ
        for veh in active_vehicles:
            veh.draw(screen, fonts)

        # 3.8 Nút Giao & Trạm Cứu Hộ
        hovered_node = draw_intersections(screen, city, fonts, mouse_pos, explored_layers, sim_state["accident_node"], MAP_WIDTH)

        # 3.9 Tô đậm trạm tại lớp ngắn nhất
        draw_highlighted_stations(screen, city, fonts, highlighted_stations)

        # 3.10 Tooltip khi rê chuột
        if active_menu is None:
            draw_node_tooltip(screen, fonts, hovered_node, mouse_pos, MAP_WIDTH)

        # 3.11 Menu Tròn
        if active_menu is not None:
            active_menu.draw(screen, fonts, mouse_pos=mouse_pos)

        # 3.11.1 Hiển thị trạng thái tạm dừng nếu paused
        if paused:
            pause_lbl = fonts["small"].render("[TẠM DỪNG] BẤM [SPACE] ĐỂ TIẾP TỤC", True, (255, 230, 80))
            px = (MAP_WIDTH - pause_lbl.get_width()) // 2
            p_box = pygame.Rect(px - 12, 12, pause_lbl.get_width() + 24, 26)
            pygame.draw.rect(screen, (16, 22, 35), p_box, border_radius=4)
            pygame.draw.rect(screen, (255, 215, 0), p_box, 1, border_radius=4)
            screen.blit(pause_lbl, (px, 17))

        # 3.12 Bảng HUD bên phải
        hud.draw(screen, fonts, sim_state, mouse_pos=mouse_pos)

        # 3.13 Co giãn bề mặt ảo lên cửa sổ thực tế (Scale & Letterbox bảo toàn tỷ lệ và sắc nét)
        scale, scaled_w, scaled_h, offset_x, offset_y = get_scale_and_offsets()
        if scaled_w == window_w and scaled_h == window_h:
            real_screen.blit(screen, (0, 0))
        else:
            scaled_surf = pygame.transform.smoothscale(screen, (scaled_w, scaled_h))
            real_screen.fill((10, 14, 22))  # Viền đệm letterbox sang trọng
            real_screen.blit(scaled_surf, (offset_x, offset_y))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()

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


def point_to_segment_distance(px, py, x1, y1, x2, y2):
    """Tính khoảng cách từ điểm (px, py) tới đoạn thẳng (x1, y1)-(x2, y2)."""
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    return math.hypot(px - proj_x, py - proj_y)


def draw_arrow(surface, color, start, end, width=2):
    """Vẽ mũi tên chỉ hướng cho đường 1 chiều."""
    pygame.draw.line(surface, color, start, end, width)
    mid_x = (start[0] + end[0]) / 2
    mid_y = (start[1] + end[1]) / 2
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    arrow_len = 8
    arrow_angle = math.pi / 6
    
    p1 = (mid_x - arrow_len * math.cos(angle - arrow_angle),
          mid_y - arrow_len * math.sin(angle - arrow_angle))
    p2 = (mid_x - arrow_len * math.cos(angle + arrow_angle),
          mid_y - arrow_len * math.sin(angle + arrow_angle))
    pygame.draw.polygon(surface, color, [(mid_x, mid_y), p1, p2])


def get_route_badge_pos(nodes_dict, route, route_idx, all_routes):
    """Xác định vị trí ghim Note Badge trên map tại điểm đặc trưng của tuyến."""
    pth = route.get("path", [])
    if not pth:
        return (200, 200)
    p1 = all_routes[0].get("path", []) if all_routes else []
    if route_idx == 0:
        mid_node = pth[len(pth) // 2]
        base_pos = nodes_dict[mid_node]["pos"]
        return (base_pos[0], base_pos[1] - 40)
    elif route_idx == 1:
        diff_nodes = [n for n in pth if n not in p1]
        if diff_nodes:
            pick_node = diff_nodes[len(diff_nodes) // 2]
        else:
            pick_node = pth[max(1, len(pth) // 3)]
        base_pos = nodes_dict[pick_node]["pos"]
        return (base_pos[0] + 32, base_pos[1] - 40)
    else:
        p2 = all_routes[1].get("path", []) if len(all_routes) > 1 else []
        diff_nodes = [n for n in pth if n not in p1 and n not in p2]
        if not diff_nodes:
            diff_nodes = [n for n in pth if n not in p1]
        if diff_nodes:
            pick_node = diff_nodes[len(diff_nodes) // 2]
        else:
            pick_node = pth[min(len(pth) - 2, max(1, 2 * len(pth) // 3))]
        base_pos = nodes_dict[pick_node]["pos"]
        return (base_pos[0] - 32, base_pos[1] + 36)


def draw_route_note_badge(target_surface, fonts_dict, cand, route_idx, pos, is_locked=False, avoid_rects=None):
    """Vẽ thẻ ghi chú chiến thuật (Tactical Card) sắc nét 3 dòng, nổi bật thông tin cho từng phương án."""
    p_lvl = cand.get("priority_level", route_idx + 1)
    km_str = cand.get("km_str", "")
    diff_str = cand.get("diff_str", "")
    via_name = cand.get("via_name", "")
    if not via_name:
        via_name = cand.get("short_name", "").split(":")[-1].strip()

    if p_lvl == 1:
        title_text = "[1] TUYẾN 1 - ĐÃ CHỌN (TỐI ƯU NHẤT)"
        sub_text = f"Cự ly: {km_str} • Lộ trình qua: {via_name}"
        desc_text = "-> Phương án tối ưu tuyệt đối (Ngắn nhất)"
        title_col = (0, 255, 240)
        sub_col = (235, 250, 255)
        desc_col = (100, 245, 220)
        border_col = (0, 255, 240)
        bg_col = (8, 26, 40, 245)
        border_w = 2
    elif p_lvl == 2:
        title_text = "[2] ĐƯỜNG PHỤ 1 (DỰ PHÒNG NÉ TẮC)"
        sub_text = f"Cự ly: {km_str} ({diff_str}) • Lộ trình qua: {via_name}"
        desc_text = "-> Tự động bẻ cua né kẹt xe khi trục chính ùn tắc"
        title_col = (255, 205, 60)
        sub_col = (255, 235, 205)
        desc_col = (255, 195, 110)
        border_col = (255, 185, 45)
        bg_col = (34, 22, 10, 245)
        border_w = 2
    else:
        title_text = "[3] ĐƯỜNG PHỤ 2 (HÀNH LANG VÒNG NGOÀI)"
        sub_text = f"Cự ly: {km_str} ({diff_str}) • Lộ trình qua: {via_name}"
        desc_text = "-> Hành lang bao bọc dự bị vòng ngoài"
        title_col = (60, 240, 190)
        sub_col = (215, 255, 240)
        desc_col = (130, 235, 205)
        border_col = (50, 225, 175)
        bg_col = (14, 30, 26, 245)
        border_w = 2

    font_t = fonts_dict["small"]
    font_s = fonts_dict["small"]
    font_d = fonts_dict["tiny"]
    surf_t = font_t.render(title_text, True, title_col)
    surf_s = font_s.render(sub_text, True, sub_col)
    surf_d = font_d.render(desc_text, True, desc_col)

    pad_x = 10
    pad_y = 6
    w = max(surf_t.get_width(), surf_s.get_width(), surf_d.get_width()) + pad_x * 2
    h = surf_t.get_height() + surf_s.get_height() + surf_d.get_height() + pad_y * 2 + 4

    rx = max(18, min(MAP_WIDTH - w - 18, pos[0] - w // 2))
    ry = max(88, min(MAP_HEIGHT - h - 18, pos[1] - h // 2))
    card_rect = pygame.Rect(rx, ry, w, h)

    if avoid_rects:
        for prev_r in avoid_rects:
            if card_rect.colliderect(prev_r):
                if card_rect.centery >= prev_r.centery:
                    card_rect.top = prev_r.bottom + 8
                else:
                    card_rect.bottom = prev_r.top - 8
                card_rect.y = max(88, min(MAP_HEIGHT - h - 18, card_rect.y))
        rx = card_rect.x
        ry = card_rect.y

    # Đổ bóng (Drop shadow)
    shadow_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    shadow_surf.fill((0, 0, 0, 155))
    target_surface.blit(shadow_surf, (rx + 3, ry + 3))

    # Nền card
    bg_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    bg_surf.fill(bg_col)
    target_surface.blit(bg_surf, (rx, ry))

    # Viền card
    pygame.draw.rect(target_surface, border_col, card_rect, border_w, border_radius=5)

    # Nếu là Tuyến 1 trong pha chốt: thêm viền hào quang phát quang nhịp nhàng
    if p_lvl == 1 and is_locked:
        pulse_px = int(math.sin(pygame.time.get_ticks() * 0.015) * 2)
        glow_r = pygame.Rect(rx - 2 - pulse_px, ry - 2 - pulse_px, w + 4 + pulse_px * 2, h + 4 + pulse_px * 2)
        pygame.draw.rect(target_surface, (0, 255, 240), glow_r, 1, border_radius=7)

    # Chân ghim (Pin marker) nhỏ liên kết xuống mặt đường
    pygame.draw.circle(target_surface, border_col, pos, 3)

    # Chữ 3 dòng
    line1_y = ry + pad_y
    line2_y = line1_y + surf_t.get_height() + 2
    line3_y = line2_y + surf_s.get_height() + 2
    target_surface.blit(surf_t, (rx + pad_x, line1_y))
    target_surface.blit(surf_s, (rx + pad_x, line2_y))
    target_surface.blit(surf_d, (rx + pad_x, line3_y))
    return card_rect


def draw_secondary_routes_panel(target_surface, fonts_dict, cands, mouse_pos=None):
    """Vẽ bảng thông tin chiến thuật các tuyến đường phụ nổi bật đè trực tiếp lên góc bản đồ."""
    if not cands or len(cands) <= 1:
        return None, None
    sec_cands = cands[1:3]
    n_sec = len(sec_cands)
    panel_w = 490
    panel_h = 36 + n_sec * 44
    panel_x = 18
    panel_y = MAP_HEIGHT - panel_h - 14
    panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

    # 1. Đổ bóng (Drop shadow)
    shadow_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    shadow_surf.fill((0, 0, 0, 160))
    target_surface.blit(shadow_surf, (panel_x + 4, panel_y + 4))

    # 2. Nền kính mờ công nghệ cao (Glassmorphism dark background)
    bg_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    bg_surf.fill((10, 18, 30, 245))
    target_surface.blit(bg_surf, (panel_x, panel_y))

    # 3. Viền bảng chỉ huy phát quang
    pygame.draw.rect(target_surface, (255, 195, 60), panel_rect, 2, border_radius=6)

    # 4. Tiêu đề bảng
    header_surf = fonts_dict["small"].render("THÔNG TIN CÁC PHƯƠNG ÁN DỰ PHÒNG (ĐƯỜNG PHỤ NÉ TẮC)", True, (255, 215, 70))
    target_surface.blit(header_surf, (panel_x + 12, panel_y + 7))
    pygame.draw.line(target_surface, (55, 75, 100), (panel_x + 10, panel_y + 26), (panel_x + panel_w - 10, panel_y + 26), 1)

    hovered_route_idx = None

    # 5. Render từng tuyến phụ
    curr_y = panel_y + 32
    for idx, cand in enumerate(sec_cands):
        p_lvl = cand.get("priority_level", idx + 2)
        km_str = cand.get("km_str", "")
        diff_str = cand.get("diff_str", "")
        via = cand.get("via_name", "")
        if not via:
            via = cand.get("short_name", "").split(":")[-1].strip()

        row_rect = pygame.Rect(panel_x + 8, curr_y, panel_w - 16, 38)
        is_hover = mouse_pos and row_rect.collidepoint(mouse_pos)
        if is_hover:
            hovered_route_idx = idx + 1

        if p_lvl == 2:
            tag_title = f"[2] [ĐƯỜNG PHỤ 1] {km_str} ({diff_str}) • Qua {via}"
            tag_desc = "-> Vai trò: Dự phòng né tắc • Sẵn sàng tự động bẻ cua né kẹt xe Tuyến 1"
            title_col = (255, 220, 70) if is_hover else (255, 205, 50)
            desc_col = (255, 245, 215) if is_hover else (255, 235, 195)
            box_border = (255, 220, 80) if is_hover else (255, 185, 45)
            box_bg = (50, 36, 16, 240) if is_hover else (38, 26, 12, 230)
        else:
            tag_title = f"[3] [ĐƯỜNG PHỤ 2] {km_str} ({diff_str}) • Qua {via}"
            tag_desc = "-> Vai trò: Hành lang dự bị • Thoát hiểm vòng ngoài khi trục chính ngập/tắc"
            title_col = (70, 255, 205) if is_hover else (50, 235, 185)
            desc_col = (230, 255, 245) if is_hover else (210, 255, 240)
            box_border = (70, 245, 195) if is_hover else (50, 225, 175)
            box_bg = (18, 45, 38, 240) if is_hover else (14, 34, 30, 230)

        row_surf = pygame.Surface((panel_w - 16, 38), pygame.SRCALPHA)
        row_surf.fill(box_bg)
        target_surface.blit(row_surf, (row_rect.x, row_rect.y))
        pygame.draw.rect(target_surface, box_border, row_rect, 2 if is_hover else 1, border_radius=4)

        target_surface.blit(fonts_dict["small"].render(tag_title, True, title_col), (row_rect.x + 8, row_rect.y + 4))
        target_surface.blit(fonts_dict["tiny"].render(tag_desc, True, desc_col), (row_rect.x + 8, row_rect.y + 20))

        curr_y += 44

    return panel_rect, hovered_route_idx


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
        if len(river_saigon) >= 2:
            pygame.draw.lines(screen, COLOR_RIVER_EDGE, False, river_saigon, 34)
            pygame.draw.lines(screen, COLOR_RIVER, False, river_saigon, 28)
        if len(canal_nhieuloc) >= 2:
            pygame.draw.lines(screen, COLOR_RIVER_EDGE, False, canal_nhieuloc, 18)
            pygame.draw.lines(screen, COLOR_RIVER, False, canal_nhieuloc, 14)

        # 3.2 Các Tuyến đường
        for e in city.raw_edges:
            u, v, dist_m, directed, name = e
            p1 = city.nodes[u]["pos"]
            p2 = city.nodes[v]["pos"]
            cong = city.congestion.get((u, v), 1.0)

            if cong == float('inf'):
                road_col = COLOR_ROAD_BLOCKED
                width = 3
            elif cong > 2.0:
                road_col = COLOR_ROAD_CONGESTED
                width = 3
            elif directed:
                road_col = COLOR_ROAD_ONEWAY
                width = 2
            else:
                road_col = COLOR_ROAD_NORMAL
                width = 2

            if directed:
                draw_arrow(screen, road_col, p1, p2, width)
            else:
                pygame.draw.line(screen, road_col, p1, p2, width)

        # 3.3 Lớp Cáp Viễn Thông Kruskal MST
        if show_mst and mst_edges:
            for (mu, mv, mw) in mst_edges:
                mp1 = city.nodes[mu]["pos"]
                mp2 = city.nodes[mv]["pos"]
                pygame.draw.line(screen, COLOR_MST_EDGE, mp1, mp2, 3)

        # 3.4 VẼ CÁC VÒNG TRÒN SÓNG LAN TỎA THEO TỪNG TẦNG BFS
        if sim_state["accident_node"] is not None and explored_layers:
            acc_pos = city.nodes[sim_state["accident_node"]]["pos"]
            for lvl, n_list in explored_layers.items():
                if lvl == 0:
                    continue
                col_idx = min(lvl, len(COLOR_BFS_LEVELS) - 1)
                ring_color = COLOR_BFS_LEVELS[col_idx]
                r_dist = lvl * 52  # Tỷ lệ bán kính vừa vặn 720p

                wave_surf = pygame.Surface((r_dist * 2 + 6, r_dist * 2 + 6), pygame.SRCALPHA)
                pygame.draw.circle(wave_surf, (*ring_color, 85), (r_dist + 3, r_dist + 3), r_dist, 2)
                screen.blit(wave_surf, (acc_pos[0] - r_dist - 3, acc_pos[1] - r_dist - 3))

                lvl_tag = fonts["tiny"].render(f"LỚP {lvl}", True, ring_color)
                screen.blit(lvl_tag, (acc_pos[0] + r_dist - 18, acc_pos[1] - 7))

        # 3.5 BANNER ĐIỀU PHỐI TÁC CHIẾN Ở ĐẦU BẢN ĐỒ (CÁCH BIỆT HOÀN TOÀN KHỎI CÁC NÚT GIAO)
        if sim_state["state_label"] in [STATE_ROUTE_SEARCH, STATE_PATH_LOCKED, STATE_DISPATCHING, STATE_RESOLVED]:
            b_w = MAP_WIDTH - 28
            is_locked_phase = (sim_state["state_label"] == STATE_PATH_LOCKED)
            b_h = 58 if is_locked_phase else 44
            banner_rect = pygame.Rect(14, 8, b_w, b_h)
            
            b_surf = pygame.Surface((b_w, b_h), pygame.SRCALPHA)
            b_surf.fill((14, 22, 38, 245))
            screen.blit(b_surf, (14, 8))
            
            if sim_state["state_label"] == STATE_ROUTE_SEARCH:
                b_border_col = (255, 225, 50) if candidate_phase == 0 else (255, 195, 45)
            elif sim_state["state_label"] == STATE_PATH_LOCKED:
                b_border_col = (50, 255, 180)
            elif sim_state["state_label"] == STATE_RESOLVED:
                b_border_col = (50, 255, 140)
            else:
                b_border_col = (0, 240, 220)
            pygame.draw.rect(screen, b_border_col, banner_rect, 2 if is_locked_phase else 1, border_radius=6)

            cost_val = sim_state.get("route_cost", 0)
            km_str = safe_dist_str(cost_val)
            eta_mins = (cost_val / 300.0) if cost_val else 0.0

            if is_locked_phase:
                station_cands = sim_state.get("station_candidates", [])
                cands = station_cands[0].get("candidates", []) if station_cands else []
                n_c = min(3, len(cands))
                t_head = fonts["small"].render(
                    f"⭐ QUYẾT ĐỊNH ĐIỀU PHỐI: CHỌN TUYẾN 1 (TỐI ƯU NHẤT) TRONG {n_c} PHƯƠNG ÁN KHẢ THI", 
                    True, (50, 255, 180)
                )
                screen.blit(t_head, (24, 11))

                if cands:
                    spacing = 8
                    chip_w = (b_w - 20 - spacing * (n_c - 1)) // n_c
                    chip_h = 24
                    chip_y = 28

                    for idx in range(n_c):
                        c = cands[idx]
                        cx = 24 + idx * (chip_w + spacing)
                        c_rect = pygame.Rect(cx, chip_y, chip_w, chip_h)
                        
                        p_lvl = c.get("priority_level", idx + 1)
                        via = c.get("via_name", "")
                        if not via:
                            via = c.get("short_name", "").split(":")[-1].strip()
                        if len(via) > 15:
                            via = via[:14] + ".."

                        if p_lvl == 1:
                            chip_bg = (12, 45, 38, 235)
                            chip_border = (50, 255, 140)
                            chip_title = f"[1] T.1 (CHỌN): {c['km_str']}"
                            chip_sub = f" • Qua {via} (Tối ưu)"
                            t_col = (50, 255, 140)
                            border_w = 2
                        elif p_lvl == 2:
                            chip_bg = (38, 28, 12, 230)
                            chip_border = (255, 190, 50)
                            chip_title = f"[2] PHỤ 1: {c['km_str']}"
                            chip_sub = f" • Qua {via} ({c['diff_str']})"
                            t_col = (255, 205, 60)
                            border_w = 1
                        else:
                            chip_bg = (14, 34, 30, 230)
                            chip_border = (50, 225, 175)
                            chip_title = f"[3] PHỤ 2: {c['km_str']}"
                            chip_sub = f" • Qua {via} ({c['diff_str']})"
                            t_col = (60, 240, 190)
                            border_w = 1

                        c_surf = pygame.Surface((chip_w, chip_h), pygame.SRCALPHA)
                        c_surf.fill(chip_bg)
                        screen.blit(c_surf, (cx, chip_y))
                        pygame.draw.rect(screen, chip_border, c_rect, border_w, border_radius=4)

                        screen.blit(fonts["tiny"].render(chip_title + chip_sub, True, t_col), (cx + 6, chip_y + 4))

                # Thanh đếm ngược điều xe ở đáy banner
                bar_y = banner_rect.bottom - 4
                prog = min(1.0, path_locked_timer / 90.0)
                pygame.draw.rect(screen, (30, 45, 60), (16, bar_y, b_w - 4, 3), border_radius=2)
                pygame.draw.rect(screen, (50, 255, 180), (16, bar_y, int((b_w - 4) * prog), 3), border_radius=2)

            else:
                if sim_state["state_label"] == STATE_ROUTE_SEARCH:
                    dijkstra_steps = sim_state.get("dijkstra_trace_steps", [])
                    total_steps = max(1, len(dijkstra_steps))
                    curr_idx = min(dijkstra_step_idx, total_steps - 1)
                    if dijkstra_steps and curr_idx < len(dijkstra_steps):
                        step_data = dijkstra_steps[curr_idx]
                        u_code = step_data["u_code"]
                        u_dist_str = safe_dist_str(step_data["u_dist"])
                        rel_count = len(step_data.get("relaxations", []))
                        t_head = fonts["small"].render(
                            f"DIJKSTRA BƯỚC [{curr_idx+1}/{total_steps}]: Chốt đỉnh [{u_code}] (d = {u_dist_str}) -> Khảo sát {rel_count} nhánh rẽ kề", 
                            True, (255, 225, 50)
                        )
                        t_sub = fonts["tiny"].render(
                            f"• Đang nới lỏng cạnh kề & cập nhật nhãn d[v] ngắn nhất về hướng {sim_state['accident_name'][:22]}",
                            True, (215, 235, 255)
                        )
                    else:
                        t_head = fonts["small"].render(
                            f"DIJKSTRA HOÀN TẤT: ĐÃ TÌM RA TUYẾN TỐI ƯU ({km_str})!", 
                            True, (50, 255, 180)
                        )
                        t_sub = fonts["tiny"].render(
                            "• Đang kích hoạt các phương án dự phòng làm mờ trên bản đồ...",
                            True, (200, 255, 230)
                        )
                elif sim_state["state_label"] == STATE_RESOLVED:
                    t_head = fonts["small"].render(
                        "LỰC LƯỢNG CỨU HỘ ĐÃ TIẾP CẬN HIỆN TRƯỜNG AN TOÀN!", 
                        True, (50, 255, 140)
                    )
                    t_sub = fonts["tiny"].render(
                        f"Hiện trường: {sim_state['accident_name']} | Đang xử lý sự cố | Bấm [[C] Đặt lại sa bàn] trên thanh điều khiển để tạo ca mới",
                        True, (200, 235, 255)
                    )
                elif sim_state["emergency_type"] == "DUAL":
                    t_head = fonts["small"].render(
                        f"ĐIỀU ĐỘNG LIÊN BỘ (BV + PCCC) -> {sim_state['accident_name'][:26]}", 
                        True, (255, 100, 160)
                    )
                    t_sub = fonts["tiny"].render(
                        f"Tổng cự ly: {km_str} | Dự kiến tiếp cận (ETA): ~{eta_mins:.1f} phút | Tốc độ khẩn cấp, ưu tiên còi đèn",
                        True, (220, 240, 255)
                    )
                else:
                    veh_title = "XE CẤP CỨU BV" if sim_state["emergency_type"] == "MEDICAL" else "XE CỨU HỎA PCCC"
                    t_head = fonts["small"].render(
                        f"ĐÃ ĐIỀU ĐỘNG {veh_title} -> {sim_state['accident_name'][:26]}", 
                        True, (50, 255, 200)
                    )
                    t_sub = fonts["tiny"].render(
                        f"Tổng cự ly: {km_str} | Dự kiến tiếp cận (ETA): ~{eta_mins:.1f} phút | Phương tiện đang chạy theo đường ngắn nhất",
                        True, (215, 240, 255)
                    )
                screen.blit(t_head, (24, 12))
                screen.blit(t_sub, (24, 27))

        # 3.6 DIỄN HOẠT THUẬT TOÁN DIJKSTRA TRỰC QUAN TRÊN BẢN ĐỒ
        if sim_state["state_label"] == STATE_ROUTE_SEARCH:
            dijkstra_steps = sim_state.get("dijkstra_trace_steps", [])
            total_steps = len(dijkstra_steps)
            curr_idx = min(dijkstra_step_idx, max(0, total_steps - 1))

            if dijkstra_steps and curr_idx < total_steps:
                step_data = dijkstra_steps[curr_idx]
                u_star = step_data["u_star"]
                u_pos = city.nodes[u_star]["pos"]
                u_dist = step_data["u_dist"]

                # 1. Vẽ cây đường đi đã chốt tới các nút đã duyệt (Settled tree)
                parent_snap = step_data.get("parent_snapshot", [])
                visited_snap = step_data.get("visited_snapshot", [])
                for i in range(city.n):
                    if visited_snap and i < len(visited_snap) and visited_snap[i]:
                        if parent_snap and i < len(parent_snap) and parent_snap[i] != -1:
                            p_node = parent_snap[i]
                            pt1 = city.nodes[p_node]["pos"]
                            pt2 = city.nodes[i]["pos"]
                            pygame.draw.line(screen, (10, 50, 70), pt1, pt2, 6)
                            pygame.draw.line(screen, (0, 220, 255), pt1, pt2, 3)

                # 2. Phóng tia quét nới lỏng (Relaxation rays) từ u* tới các đỉnh kề v
                relaxations = step_data.get("relaxations", [])
                prog = min(1.0, dijkstra_step_timer / float(dijkstra_step_delay))

                for rel in relaxations:
                    v = rel["v"]
                    v_pos = city.nodes[v]["pos"]
                    w = rel["w"]
                    updated = rel["updated"]

                    rx = int(u_pos[0] + (v_pos[0] - u_pos[0]) * prog)
                    ry = int(u_pos[1] + (v_pos[1] - u_pos[1]) * prog)

                    ray_col = (255, 225, 60) if updated else (120, 165, 210)
                    pygame.draw.line(screen, ray_col, u_pos, (rx, ry), 3 if updated else 1)
                    pygame.draw.circle(screen, (255, 255, 255), (rx, ry), 4)

                    mid_x = (u_pos[0] + v_pos[0]) // 2
                    mid_y = (u_pos[1] + v_pos[1]) // 2
                    w_tag = fonts["tiny"].render(f"+{int(w)}m", True, (255, 240, 180) if updated else (180, 200, 225))
                    w_box = pygame.Rect(mid_x - w_tag.get_width() // 2 - 3, mid_y - 8, w_tag.get_width() + 6, 14)
                    pygame.draw.rect(screen, (12, 18, 30), w_box, border_radius=3)
                    pygame.draw.rect(screen, ray_col, w_box, 1, border_radius=3)
                    screen.blit(w_tag, (w_box.x + 3, w_box.y + 1))

                    if updated:
                        v_pulse = 12 + int(math.sin(pygame.time.get_ticks() * 0.02) * 3)
                        pygame.draw.circle(screen, (50, 255, 140), v_pos, v_pulse, 2)
                        d_tag = fonts["tiny"].render(f"d={safe_dist_str(rel['new_dist'])}", True, (50, 255, 140))
                        d_box = pygame.Rect(v_pos[0] - d_tag.get_width() // 2 - 3, v_pos[1] - 22, d_tag.get_width() + 6, 14)
                        pygame.draw.rect(screen, (10, 20, 32), d_box, border_radius=3)
                        pygame.draw.rect(screen, (50, 255, 140), d_box, 1, border_radius=3)
                        screen.blit(d_tag, (d_box.x + 3, d_box.y + 1))

                # 3. Beacon vàng nhấp nháy tại nút u* đang xét
                u_pulse = 16 + int(math.sin(pygame.time.get_ticks() * 0.02) * 4)
                pygame.draw.circle(screen, (255, 215, 0), u_pos, u_pulse, 2)
                u_tag = fonts["tiny"].render(f"📍 Chốt [{step_data['u_code']}] (d={safe_dist_str(u_dist)})", True, (255, 255, 255))
                u_box = pygame.Rect(u_pos[0] - u_tag.get_width() // 2 - 4, u_pos[1] + 14, u_tag.get_width() + 8, 16)
                pygame.draw.rect(screen, (14, 20, 35), u_box, border_radius=3)
                pygame.draw.rect(screen, (255, 215, 0), u_box, 1, border_radius=3)
                screen.blit(u_tag, (u_box.x + 4, u_box.y + 2))

            # 4. Khi toàn bộ bước Dijkstra đã xong: Vẽ trước lộ trình chốt và các tuyến dự phòng mờ
            if dijkstra_step_idx >= total_steps:
                station_cands = sim_state.get("station_candidates", [])
                for st_info in station_cands:
                    cands = st_info.get("candidates", [])
                    st_type = st_info.get("type", "HOSPITAL")
                    # Vẽ các tuyến dự phòng (Đường phụ 1, Đường phụ 2) tô mờ dịu nhẹ
                    for c_idx in range(len(cands) - 1, 0, -1):
                        cand = cands[c_idx]
                        pth = cand["path"]
                        p_lvl = cand.get("priority_level", c_idx + 1)
                        if p_lvl == 2:
                            sec_col = (235, 170, 50)       # Vàng hổ phách dịu mờ cho Tuyến phụ 1
                            halo_col = (35, 25, 14)
                        else:
                            sec_col = (50, 190, 150)       # Xanh ngọc lục bảo dịu mờ cho Tuyến phụ 2
                            halo_col = (14, 32, 26)
                        for i in range(len(pth) - 1):
                            pt1 = city.nodes[pth[i]]["pos"]
                            pt2 = city.nodes[pth[i + 1]]["pos"]
                            pygame.draw.line(screen, halo_col, pt1, pt2, 6)
                            pygame.draw.line(screen, sec_col, pt1, pt2, 3)

                    # Vẽ Tuyến 1 sáng rực neon và tim sáng
                    if cands:
                        pth1 = cands[0]["path"]
                        halo_p = (10, 70, 95) if st_type == "HOSPITAL" else (75, 40, 10)
                        primary_col = COLOR_SHORTEST_PATH if st_type == "HOSPITAL" else (255, 140, 20)
                        for i in range(len(pth1) - 1):
                            pt1 = city.nodes[pth1[i]]["pos"]
                            pt2 = city.nodes[pth1[i + 1]]["pos"]
                            pygame.draw.line(screen, halo_p, pt1, pt2, 12)
                            pygame.draw.line(screen, primary_col, pt1, pt2, 6)
                            pygame.draw.line(screen, (240, 255, 255), pt1, pt2, 2)

        # 3.6.1 KHI ĐÃ CHỐT ĐƯỜNG HOẶC XE ĐANG CHẠY / ĐÃ ĐẾN NƠI:
        # VẼ CÁC TUYẾN DỰ PHÒNG TÔ MỜ Ở LỚP DƯỚI, TUYẾN CHÍNH SÁNG RỰC RỠ Ở LỚP TRÊN (BẢN ĐỒ THOÁNG ĐÃNG)
        elif sim_state["state_label"] in [STATE_PATH_LOCKED, STATE_DISPATCHING, STATE_RESOLVED]:
            station_cands = sim_state.get("station_candidates", [])
            for st_info in station_cands:
                cands = st_info.get("candidates", [])
                st_type = st_info.get("type", "HOSPITAL")

                # 1. Vẽ các tuyến dự phòng (Đường phụ 1, Đường phụ 2) TÔ MỜ DỊU NHẸ, ĐỂ BẢN ĐỒ THOÁNG ĐÃNG
                for c_idx in range(len(cands) - 1, 0, -1):
                    cand = cands[c_idx]
                    pth = cand["path"]
                    p_lvl = cand.get("priority_level", c_idx + 1)
                    if p_lvl == 2:
                        sec_col = (235, 170, 50)       # Vàng hổ phách dịu mờ cho Tuyến phụ 1
                        halo_col = (35, 25, 14)        # Viền bóng mờ nhẹ
                        line_w = 3.5
                        halo_w = 6.5
                    else:
                        sec_col = (50, 190, 150)       # Xanh ngọc lục bảo dịu mờ cho Tuyến phụ 2
                        halo_col = (14, 32, 26)        # Viền bóng mờ nhẹ
                        line_w = 3.5
                        halo_w = 6.5

                    for i in range(len(pth) - 1):
                        pt1 = city.nodes[pth[i]]["pos"]
                        pt2 = city.nodes[pth[i + 1]]["pos"]
                        pygame.draw.line(screen, halo_col, pt1, pt2, int(halo_w))
                        pygame.draw.line(screen, sec_col, pt1, pt2, int(line_w))

                # 2. Vẽ Tuyến 1 (Ưu tiên 1 - Tối ưu) RỰC RỠ NEON VÀ TIM SÁNG
                if cands:
                    pth1 = cands[0]["path"]
                    halo_p = (10, 70, 95) if st_type == "HOSPITAL" else (75, 40, 10)
                    pulse_val = int(210 + math.sin(pygame.time.get_ticks() * 0.015) * 45)
                    glow_p = (0, pulse_val, 255) if st_type == "HOSPITAL" else (255, pulse_val, 30)

                    for i in range(len(pth1) - 1):
                        pt1 = city.nodes[pth1[i]]["pos"]
                        pt2 = city.nodes[pth1[i + 1]]["pos"]
                        pygame.draw.line(screen, halo_p, pt1, pt2, 12)
                        pygame.draw.line(screen, glow_p, pt1, pt2, 6)
                        pygame.draw.line(screen, (240, 255, 255), pt1, pt2, 2)

                    # 2.1 Hiệu ứng luồng sóng điện xung kích chạy dọc Tuyến 1 trong pha chốt quyết định
                    if sim_state["state_label"] == STATE_PATH_LOCKED and len(pth1) >= 2:
                        total_segs = len(pth1) - 1
                        surge_phase = (pygame.time.get_ticks() % 900) / 900.0
                        seg_pos = surge_phase * total_segs
                        cur_seg_idx = min(total_segs - 1, int(seg_pos))
                        seg_frac = seg_pos - cur_seg_idx
                        p_a = city.nodes[pth1[cur_seg_idx]]["pos"]
                        p_b = city.nodes[pth1[cur_seg_idx + 1]]["pos"]
                        pulse_x = int(p_a[0] + (p_b[0] - p_a[0]) * seg_frac)
                        pulse_y = int(p_a[1] + (p_b[1] - p_a[1]) * seg_frac)

                        # Vòng năng lượng điện quét từ trạm tới đích
                        pygame.draw.circle(screen, (0, 255, 255), (pulse_x, pulse_y), 11, 2)
                        pygame.draw.circle(screen, (255, 255, 255), (pulse_x, pulse_y), 5)

        # 3.7 VẼ CÁC XE CỨU HỘ
        for veh in active_vehicles:
            veh.draw(screen, fonts)

        # 3.8 VẼ CÁC NÚT GIAO (KÍCH THƯỚC CHUẨN 720P GỌN GÀNG)
        hovered_node = None

        node_layer_map = {}
        for lvl, n_list in explored_layers.items():
            for nid in n_list:
                node_layer_map[nid] = lvl

        for nid, ndata in city.nodes.items():
            nx, ny = ndata["pos"]
            ntype = ndata["type"]
            dist_to_mouse = math.hypot(mouse_pos[0] - nx, mouse_pos[1] - ny)
            is_hover = (dist_to_mouse <= 14)
            if is_hover and mouse_pos[0] < MAP_WIDTH:
                hovered_node = ndata

            # Kích thước nút chuẩn đẹp
            if nid == sim_state["accident_node"]:
                base_color = COLOR_NODE_ACCIDENT
                node_radius = 12 + int(math.sin(pygame.time.get_ticks() * 0.008) * 3)
            elif ntype == "UTH":
                base_color = COLOR_NODE_UTH
                node_radius = 11
            elif ntype == "HOSPITAL":
                base_color = COLOR_NODE_HOSPITAL
                node_radius = 10
            elif ntype == "FIRE":
                base_color = COLOR_NODE_FIRE
                node_radius = 10
            elif ntype == "LANDMARK":
                base_color = COLOR_NODE_LANDMARK
                node_radius = 9
            elif ntype == "REMOTE":
                base_color = COLOR_NODE_REMOTE
                node_radius = 7
            else:
                base_color = COLOR_NODE_DEFAULT
                node_radius = 7

            if is_hover:
                node_radius += 2

            # Viền phân lớp BFS
            border_color = (230, 240, 250)
            border_width = 2
            if nid in node_layer_map:
                nlvl = node_layer_map[nid]
                border_color = COLOR_BFS_LEVELS[min(nlvl, len(COLOR_BFS_LEVELS) - 1)]
                border_width = 2

            pygame.draw.circle(screen, (15, 20, 32), (nx, ny), node_radius + 2)
            pygame.draw.circle(screen, base_color, (nx, ny), node_radius)
            pygame.draw.circle(screen, border_color, (nx, ny), node_radius, border_width)

            # Mã code nút - Thiết kế dạng badge/pill sắc nét chống mờ
            code_surf = fonts["node"].render(ndata["code"], True, (245, 250, 255))
            pw = code_surf.get_width() + 8
            ph = code_surf.get_height() + 2
            px = nx - pw // 2
            py = ny + node_radius + 3
            pill_rect = pygame.Rect(px, py, pw, ph)
            
            pill_bg = (10, 15, 26)
            pill_border = (45, 65, 95)
            if nid == sim_state["accident_node"]:
                pill_border = (255, 60, 60)
            elif ntype == "HOSPITAL":
                pill_border = (40, 220, 130)
            elif ntype == "FIRE":
                pill_border = (255, 120, 30)
            elif ntype == "UTH":
                pill_border = (30, 160, 255)
            elif ntype == "LANDMARK":
                pill_border = (230, 190, 50)
                
            pygame.draw.rect(screen, pill_bg, pill_rect, border_radius=3)
            pygame.draw.rect(screen, pill_border, pill_rect, 1, border_radius=3)
            screen.blit(code_surf, (px + 4, py + 1))

        # 3.9 TÔ ĐẬM RỰC RỠ CÁC TRẠM ĐƯỢC CHỌN TẠI LỚP NGẮN NHẤT
        for st in highlighted_stations:
            st_id = st["station_id"]
            sx, sy = city.nodes[st_id]["pos"]
            pulse_r = 18 + int(math.sin(pygame.time.get_ticks() * 0.012) * 4)
            glow_col = (50, 255, 140) if st["type"] == "HOSPITAL" else (255, 150, 30)
            
            pygame.draw.circle(screen, glow_col, (sx, sy), pulse_r, 3)
            
            badge_text = f"• {st['name'][:16]} (LỚP {st['layer_found']}) •"
            badge_surf = fonts["tiny"].render(badge_text, True, (255, 255, 255))
            b_w, b_h = badge_surf.get_width() + 8, 16
            b_rect = pygame.Rect(sx - b_w // 2, sy - pulse_r - 20, b_w, b_h)
            pygame.draw.rect(screen, (15, 25, 40), b_rect, border_radius=3)
            pygame.draw.rect(screen, glow_col, b_rect, 1, border_radius=3)
            screen.blit(badge_surf, (b_rect.x + 4, b_rect.y + 1))

        # 3.10 Tooltip khi rê chuột
        if hovered_node is not None and active_menu is None:
            tip_title = hovered_node["name"]
            tip_desc = hovered_node.get("desc", "")
            if "fleet" in hovered_node:
                avail = hovered_node["fleet"] - hovered_node.get("busy", 0)
                tip_desc += f" [Sẵn sàng: {avail}/{hovered_node['fleet']}]"
                
            t_surf1 = fonts["small"].render(tip_title, True, COLOR_TEXT_HIGHLIGHT)
            t_surf2 = fonts["tiny"].render(tip_desc, True, (210, 225, 245))
            
            box_w = max(t_surf1.get_width(), t_surf2.get_width()) + 14
            box_h = 38
            bx = min(mouse_pos[0] + 10, MAP_WIDTH - box_w - 10)
            by = max(mouse_pos[1] - 42, 10)
            
            tip_rect = pygame.Rect(bx, by, box_w, box_h)
            pygame.draw.rect(screen, (15, 20, 32), tip_rect, border_radius=4)
            pygame.draw.rect(screen, (70, 95, 135), tip_rect, 1, border_radius=4)
            screen.blit(t_surf1, (bx + 7, by + 3))
            screen.blit(t_surf2, (bx + 7, by + 20))

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

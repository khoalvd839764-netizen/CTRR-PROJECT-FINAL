# -*- coding: utf-8 -*-
"""
Module: ung_dung_thuc_te/route_overlay.py
Đảm nhận toàn bộ các lớp phủ trực quan hóa thuật toán lên bản đồ:
- Cây khung nhỏ nhất viễn thông (Kruskal MST).
- Sóng lan tỏa đồng tâm theo từng tầng tìm kiếm trạm (BFS Multi-Layer Waves).
- Banner điều phối chiến thuật ở đầu bản đồ.
- Diễn hoạt từng bước nới lỏng ngã rẽ và nhãn khoảng cách d[v] (Dijkstra Tracing Rays).
- Vệt sáng Neon lộ trình chốt và các tuyến đường phụ né tắc (Primary & Secondary Routes).
- Thẻ Tactical Card và Bảng thông tin tuyến phụ.
"""
import math
import pygame

from ung_dung_thuc_te.config import (
    MAP_WIDTH, MAP_HEIGHT,
    COLOR_BFS_LEVELS, COLOR_MST_EDGE, COLOR_SHORTEST_PATH,
    STATE_ROUTE_SEARCH, STATE_PATH_LOCKED, STATE_DISPATCHING, STATE_RESOLVED
)
from ung_dung_thuc_te.hud import safe_dist_str


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
    """Vẽ thẻ ghi chú chiến thuật (Tactical Card) sắc nét 3 dòng."""
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

    shadow_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    shadow_surf.fill((0, 0, 0, 155))
    target_surface.blit(shadow_surf, (rx + 3, ry + 3))

    bg_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    bg_surf.fill(bg_col)
    target_surface.blit(bg_surf, (rx, ry))

    pygame.draw.rect(target_surface, border_col, card_rect, border_w, border_radius=5)

    if p_lvl == 1 and is_locked:
        pulse_px = int(math.sin(pygame.time.get_ticks() * 0.015) * 2)
        glow_r = pygame.Rect(rx - 2 - pulse_px, ry - 2 - pulse_px, w + 4 + pulse_px * 2, h + 4 + pulse_px * 2)
        pygame.draw.rect(target_surface, (0, 255, 240), glow_r, 1, border_radius=7)

    pygame.draw.circle(target_surface, border_col, pos, 3)

    line1_y = ry + pad_y
    line2_y = line1_y + surf_t.get_height() + 2
    line3_y = line2_y + surf_s.get_height() + 2
    target_surface.blit(surf_t, (rx + pad_x, line1_y))
    target_surface.blit(surf_s, (rx + pad_x, line2_y))
    target_surface.blit(surf_d, (rx + pad_x, line3_y))
    return card_rect


def draw_secondary_routes_panel(target_surface, fonts_dict, cands, mouse_pos=None):
    """Vẽ bảng thông tin chiến thuật các tuyến đường phụ nổi bật ở góc bản đồ."""
    if not cands or len(cands) <= 1:
        return None, None
    sec_cands = cands[1:3]
    n_sec = len(sec_cands)
    panel_w = 490
    panel_h = 36 + n_sec * 44
    panel_x = 18
    panel_y = MAP_HEIGHT - panel_h - 14
    panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

    shadow_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    shadow_surf.fill((0, 0, 0, 160))
    target_surface.blit(shadow_surf, (panel_x + 4, panel_y + 4))

    bg_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    bg_surf.fill((10, 18, 30, 245))
    target_surface.blit(bg_surf, (panel_x, panel_y))

    pygame.draw.rect(target_surface, (255, 195, 60), panel_rect, 2, border_radius=6)

    header_surf = fonts_dict["small"].render("THÔNG TIN CÁC PHƯƠNG ÁN DỰ PHÒNG (ĐƯỜNG PHỤ NÉ TẮC)", True, (255, 215, 70))
    target_surface.blit(header_surf, (panel_x + 12, panel_y + 7))
    pygame.draw.line(target_surface, (55, 75, 100), (panel_x + 10, panel_y + 26), (panel_x + panel_w - 10, panel_y + 26), 1)

    hovered_route_idx = None
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


def draw_mst_network(screen, city, show_mst, mst_edges):
    """Vẽ mạng cáp quang viễn thông tối ưu bằng cây khung nhỏ nhất (Kruskal MST)."""
    if show_mst and mst_edges:
        for (mu, mv, mw) in mst_edges:
            mp1 = city.nodes[mu]["pos"]
            mp2 = city.nodes[mv]["pos"]
            pygame.draw.line(screen, COLOR_MST_EDGE, mp1, mp2, 3)


def draw_bfs_waves(screen, city, fonts, sim_state, explored_layers):
    """Vẽ các vòng tròn sóng lan tỏa theo từng tầng BFS từ tâm sự cố."""
    if sim_state["accident_node"] is not None and explored_layers:
        acc_pos = city.nodes[sim_state["accident_node"]]["pos"]
        for lvl, n_list in explored_layers.items():
            if lvl == 0:
                continue
            col_idx = min(lvl, len(COLOR_BFS_LEVELS) - 1)
            ring_color = COLOR_BFS_LEVELS[col_idx]
            r_dist = lvl * 52

            wave_surf = pygame.Surface((r_dist * 2 + 6, r_dist * 2 + 6), pygame.SRCALPHA)
            pygame.draw.circle(wave_surf, (*ring_color, 85), (r_dist + 3, r_dist + 3), r_dist, 2)
            screen.blit(wave_surf, (acc_pos[0] - r_dist - 3, acc_pos[1] - r_dist - 3))

            lvl_tag = fonts["tiny"].render(f"LỚP {lvl}", True, ring_color)
            screen.blit(lvl_tag, (acc_pos[0] + r_dist - 18, acc_pos[1] - 7))


def draw_tactical_banner(screen, fonts, sim_state, candidate_phase, path_locked_timer, dijkstra_step_idx, map_width):
    """Vẽ banner điều phối tác chiến ở đầu bản đồ."""
    if sim_state["state_label"] not in [STATE_ROUTE_SEARCH, STATE_PATH_LOCKED, STATE_DISPATCHING, STATE_RESOLVED]:
        return

    b_w = map_width - 28
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


def draw_dijkstra_trace(screen, city, fonts, sim_state, dijkstra_step_idx, dijkstra_step_timer, dijkstra_step_delay):
    """Diễn hoạt thuật toán Dijkstra trực quan từng bước: cây chốt, tia quét nới lỏng, beacon vàng."""
    dijkstra_steps = sim_state.get("dijkstra_trace_steps", [])
    total_steps = len(dijkstra_steps)
    curr_idx = min(dijkstra_step_idx, max(0, total_steps - 1))

    if dijkstra_steps and curr_idx < total_steps:
        step_data = dijkstra_steps[curr_idx]
        u_star = step_data["u_star"]
        u_pos = city.nodes[u_star]["pos"]
        u_dist = step_data["u_dist"]

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

        u_pulse = 16 + int(math.sin(pygame.time.get_ticks() * 0.02) * 4)
        pygame.draw.circle(screen, (255, 215, 0), u_pos, u_pulse, 2)
        u_tag = fonts["tiny"].render(f"📍 Chốt [{step_data['u_code']}] (d={safe_dist_str(u_dist)})", True, (255, 255, 255))
        u_box = pygame.Rect(u_pos[0] - u_tag.get_width() // 2 - 4, u_pos[1] + 14, u_tag.get_width() + 8, 16)
        pygame.draw.rect(screen, (14, 20, 35), u_box, border_radius=3)
        pygame.draw.rect(screen, (255, 215, 0), u_box, 1, border_radius=3)
        screen.blit(u_tag, (u_box.x + 4, u_box.y + 2))

    if dijkstra_step_idx >= total_steps:
        station_cands = sim_state.get("station_candidates", [])
        for st_info in station_cands:
            cands = st_info.get("candidates", [])
            st_type = st_info.get("type", "HOSPITAL")
            for c_idx in range(len(cands) - 1, 0, -1):
                cand = cands[c_idx]
                pth = cand["path"]
                p_lvl = cand.get("priority_level", c_idx + 1)
                if p_lvl == 2:
                    sec_col = (235, 170, 50)
                    halo_col = (35, 25, 14)
                else:
                    sec_col = (50, 190, 150)
                    halo_col = (14, 32, 26)
                for i in range(len(pth) - 1):
                    pt1 = city.nodes[pth[i]]["pos"]
                    pt2 = city.nodes[pth[i + 1]]["pos"]
                    pygame.draw.line(screen, halo_col, pt1, pt2, 6)
                    pygame.draw.line(screen, sec_col, pt1, pt2, 3)

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


def draw_committed_routes(screen, city, sim_state):
    """Vẽ tuyến 1 rực rỡ neon, luồng xung kích và các tuyến phụ mờ trong pha chốt/di chuyển/hoàn tất."""
    station_cands = sim_state.get("station_candidates", [])
    for st_info in station_cands:
        cands = st_info.get("candidates", [])
        st_type = st_info.get("type", "HOSPITAL")

        for c_idx in range(len(cands) - 1, 0, -1):
            cand = cands[c_idx]
            pth = cand["path"]
            p_lvl = cand.get("priority_level", c_idx + 1)
            if p_lvl == 2:
                sec_col = (235, 170, 50)
                halo_col = (35, 25, 14)
                line_w = 3.5
                halo_w = 6.5
            else:
                sec_col = (50, 190, 150)
                halo_col = (14, 32, 26)
                line_w = 3.5
                halo_w = 6.5

            for i in range(len(pth) - 1):
                pt1 = city.nodes[pth[i]]["pos"]
                pt2 = city.nodes[pth[i + 1]]["pos"]
                pygame.draw.line(screen, halo_col, pt1, pt2, int(halo_w))
                pygame.draw.line(screen, sec_col, pt1, pt2, int(line_w))

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

                pygame.draw.circle(screen, (0, 255, 255), (pulse_x, pulse_y), 11, 2)
                pygame.draw.circle(screen, (255, 255, 255), (pulse_x, pulse_y), 5)

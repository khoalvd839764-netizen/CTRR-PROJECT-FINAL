# -*- coding: utf-8 -*-
"""
Module: ung_dung_thuc_te/hud.py
Bảng điều khiển tác chiến HUD (Tactical Operations Center Dashboard) hiển thị bên phải màn hình.
Thiết kế vừa vặn hoàn hảo chuẩn màn hình 720p HD (Chiều cao 720px, Chiều rộng 330px).
Trình bày chuẩn thuật toán Toán Rời Rạc (CTRR):
  - Bảng ma trận bước lặp Dijkstra (Chốt u* nhỏ nhất & Nới lỏng Relaxation d[v] = min(d[v], d[u] + w))
  - Xử lý an toàn tuyệt đối với giá trị vô cùng (float('inf')), không bị crash OverflowError
  - Nút ĐẶT LẠI SA BÀN (RESET) click chuột trực tiếp
"""
import math
import pygame
from ung_dung_thuc_te.config import (
    HUD_X, HUD_WIDTH, HUD_HEIGHT,
    COLOR_PANEL_BG, COLOR_PANEL_BORDER, COLOR_PANEL_HEADER,
    COLOR_TEXT_WHITE, COLOR_TEXT_MUTED, COLOR_TEXT_HIGHLIGHT,
    COLOR_TEXT_CYAN, COLOR_TEXT_RED, COLOR_TEXT_GREEN
)


def safe_dist_str(val):
    """Định dạng khoảng cách thành km rõ ràng cho người dùng thực tế."""
    if val is None or math.isinf(val):
        return "---"
    km = val / 1000.0
    if km >= 10.0:
        return f"{km:.1f} km"
    return f"{km:.2f} km"


class TacticalHUD:
    """Quản lý hiển thị toàn bộ giao diện bảng điều khiển tác chiến bên phải."""
    def __init__(self, city_graph):
        self.city_graph = city_graph
        self.log_messages = []
        self.reset_btn_rect = pygame.Rect(HUD_X + 12, 60, HUD_WIDTH - 24, 28)

    def add_log(self, text, color=COLOR_TEXT_WHITE):
        """Thêm tin nhắn vào nhật ký tác chiến."""
        self.log_messages.append({"text": text, "color": color})
        if len(self.log_messages) > 6:
            self.log_messages.pop(0)

    def handle_click(self, mouse_pos):
        """Kiểm tra xem người dùng có click vào các nút trên HUD không."""
        if self.reset_btn_rect.collidepoint(mouse_pos):
            return "RESET"
        return None

    def draw(self, surface, fonts, sim_state, mouse_pos=None):
        """Vẽ toàn bộ HUD lên bề mặt Pygame (hỗ trợ mouse_pos ảo khi phóng to)."""
        font_sm = fonts["small"]
        font_xs = fonts["tiny"]
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()

        # 1. Nền Panel HUD bên phải
        panel_rect = pygame.Rect(HUD_X, 0, HUD_WIDTH, HUD_HEIGHT)
        pygame.draw.rect(surface, COLOR_PANEL_BG, panel_rect)
        pygame.draw.line(surface, COLOR_PANEL_BORDER, (HUD_X, 0), (HUD_X, HUD_HEIGHT), 2)

        # 2. Header: SỞ CHỈ HUY KHẨN CẤP ĐÔ THỊ
        header_rect = pygame.Rect(HUD_X, 0, HUD_WIDTH, 52)
        pygame.draw.rect(surface, COLOR_PANEL_HEADER, header_rect)
        pygame.draw.line(surface, COLOR_PANEL_BORDER, (HUD_X, 52), (HUD_X + HUD_WIDTH, 52), 1)

        t1 = font_sm.render("SỞ CHỈ HUY ĐIỀU PHỐI (EOC)", True, COLOR_TEXT_HIGHLIGHT)
        t2 = font_xs.render("MẠNG LƯỚI GIAO THÔNG UTH - BÌNH THẠNH", True, COLOR_TEXT_CYAN)
        surface.blit(t1, (HUD_X + 14, 8))
        surface.blit(t2, (HUD_X + 14, 28))

        # 3. NÚT BẤM TRỰC QUAN [ ↺ ĐẶT LẠI SA BÀN / RESET ]
        is_hover_reset = self.reset_btn_rect.collidepoint(mouse_pos)
        btn_bg = (60, 30, 40) if is_hover_reset else (40, 24, 34)
        btn_border = (255, 80, 80) if is_hover_reset else (190, 60, 60)
        pygame.draw.rect(surface, btn_bg, self.reset_btn_rect, border_radius=4)
        pygame.draw.rect(surface, btn_border, self.reset_btn_rect, 1, border_radius=4)
        
        btn_txt = font_xs.render("[C] ĐẶT LẠI SA BÀN (RESET)", True, (255, 230, 230) if is_hover_reset else (220, 190, 190))
        surface.blit(btn_txt, (self.reset_btn_rect.x + (self.reset_btn_rect.width - btn_txt.get_width()) // 2,
                               self.reset_btn_rect.y + 7))

        curr_y = 92

        # 4. HỘP TRẠNG THÁI TÁC CHIẾN (CURRENT INCIDENT STATUS)
        status_box = pygame.Rect(HUD_X + 10, curr_y, HUD_WIDTH - 20, 114)
        pygame.draw.rect(surface, (24, 32, 48), status_box, border_radius=5)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, status_box, 1, border_radius=5)

        st_title = font_xs.render("THÔNG TIN ĐIỀU PHỐI HIỆN TRƯỜNG", True, COLOR_TEXT_WHITE)
        surface.blit(st_title, (HUD_X + 16, curr_y + 6))
        pygame.draw.line(surface, (40, 55, 80), (HUD_X + 14, curr_y + 22), (HUD_X + HUD_WIDTH - 14, curr_y + 22), 1)

        state_str = sim_state.get("state_label", "SẴN SÀNG")
        state_col = COLOR_TEXT_GREEN if "SẴN SÀNG" in state_str else COLOR_TEXT_HIGHLIGHT
        if "ĐIỀU XE" in state_str or "ĐIỀU ĐỘNG" in state_str:
            state_col = (255, 100, 100)
        elif "BFS" in state_str:
            state_col = (255, 215, 0)
        elif "DIJKSTRA" in state_str:
            state_col = (0, 240, 220)

        s_lbl = font_xs.render(f"Trạng thái: {state_str[:28]}", True, state_col)
        surface.blit(s_lbl, (HUD_X + 16, curr_y + 27))

        acc_name = sim_state.get("accident_name", "Chưa phát sinh")
        em_type = sim_state.get("emergency_type", "")
        type_str = ""
        type_col = COLOR_TEXT_WHITE
        if em_type == "MEDICAL":
            type_str = "[CẤP CỨU]"
            type_col = (60, 255, 160)
        elif em_type == "FIRE":
            type_str = "[BÁO CHÁY]"
            type_col = (255, 140, 40)
        elif em_type == "DUAL":
            type_str = "[SỰ CỐ NẶNG]"
            type_col = (255, 100, 140)

        acc_lbl = font_xs.render(f"Hiện trường: {acc_name[:17]}", True, COLOR_TEXT_WHITE)
        surface.blit(acc_lbl, (HUD_X + 16, curr_y + 44))
        if type_str:
            t_badge = font_xs.render(type_str, True, type_col)
            surface.blit(t_badge, (HUD_X + HUD_WIDTH - t_badge.get_width() - 16, curr_y + 44))

        # Đơn vị tiếp nhận
        stations_info = sim_state.get("stations_info", [])
        if stations_info:
            info_str = " & ".join([f"{s['name'][:10]} (L{s['layer_found']})" for s in stations_info])
            stat_lbl = font_xs.render(f"Đơn vị: {info_str}", True, COLOR_TEXT_CYAN)
        else:
            station_name = sim_state.get("station_name", "---")
            layer_found = sim_state.get("layer_found", -1)
            layer_str = f"Lớp {layer_found}" if layer_found > 0 else "---"
            stat_lbl = font_xs.render(f"Đơn vị: {station_name[:18]} [{layer_str}]", True, COLOR_TEXT_CYAN)
        surface.blit(stat_lbl, (HUD_X + 16, curr_y + 61))

        cost_val = sim_state.get("route_cost", None)
        if cost_val is not None and not math.isinf(cost_val) and sim_state.get("state_label") in [
            "DIJKSTRA: ĐÃ CHỐT LỘ TRÌNH TỐI ƯU!", "ĐIỀU XE ĐẾN HIỆN TRƯỜNG", "ĐÃ TIẾP CẬN HIỆN TRƯỜNG",
            "ĐIỀU PHỐI XE CỨU HỘ", "XÁC NHẬN LỘ TRÌNH TỐI ƯU"
        ]:
            cost_str = f"{safe_dist_str(cost_val)} (~{cost_val / 300.0:.1f} phút)"
        elif "DÒ ĐƯỜNG" in sim_state.get("state_label", ""):
            cost_str = "Đang dò đường từ trạm..."
        elif "DIJKSTRA" in sim_state.get("state_label", ""):
            cost_str = "Đang tối ưu lộ trình..."
        elif "BFS" in sim_state.get("state_label", ""):
            cost_str = "Đang quét tìm trạm gần nhất..."
        elif "ĐIỀU" in sim_state.get("state_label", ""):
            cost_str = f"{safe_dist_str(cost_val)} (~{cost_val / 300.0:.1f} phút)" if cost_val else "---"
        else:
            cost_str = "---"
        cost_lbl = font_xs.render(f"Tổng cự ly & Thời gian (ETA): {cost_str}", True, COLOR_TEXT_HIGHLIGHT)
        surface.blit(cost_lbl, (HUD_X + 16, curr_y + 78))

        current_scan_layer = sim_state.get("current_scan_layer", -1)
        if current_scan_layer >= 0 and "BFS" in state_str:
            badge_str = f"► Tiến trình: Đang quét ngã rẽ Lớp {current_scan_layer}..."
            surface.blit(font_xs.render(badge_str, True, (255, 140, 50)), (HUD_X + 16, curr_y + 95))

        curr_y += 120

        # 5. KHU VỰC CHÚ THÍCH CÁC TUYẾN ĐƯỜNG & DỰ PHÒNG NÉ TẮC (THAY THẾ HỘP NĂNG LỰC CŨ)
        # Thiết kế chuẩn vừa vặn chiều cao màn hình 720p: từ curr_y = 212 đến y = 588 (chiều cao 376px)
        state_str = sim_state.get("state_label", "")
        station_cands = sim_state.get("station_candidates", [])
        has_active_routes = bool(station_cands or sim_state.get("all_paths") or sim_state.get("current_path"))

        # TRƯỜNG HỢP 1: THUẬT TOÁN DIJKSTRA ĐANG DÒ TỪNG BƯỚC (CHƯA CHỐT)
        if ("DÒ ĐƯỜNG" in state_str or "DIJKSTRA" in state_str) and ("CHỐT" not in state_str and "TỐI ƯU!" not in state_str):
            algo_box = pygame.Rect(HUD_X + 10, curr_y, HUD_WIDTH - 20, 374)
            pygame.draw.rect(surface, (18, 26, 42), algo_box, border_radius=5)
            pygame.draw.rect(surface, (0, 220, 200), algo_box, 1, border_radius=5)

            algo_title = font_xs.render("🔍 DIJKSTRA: TIẾN TRÌNH DÒ TUYẾN TỐI ƯU", True, (255, 220, 50))
            surface.blit(algo_title, (HUD_X + 16, curr_y + 8))
            pygame.draw.line(surface, (40, 65, 95), (HUD_X + 14, curr_y + 26), (HUD_X + HUD_WIDTH - 14, curr_y + 26), 1)

            dijkstra_steps = sim_state.get("dijkstra_trace_steps", [])
            d_idx = sim_state.get("dijkstra_step_idx", 0)
            sub_y = curr_y + 36

            step_data = None
            if dijkstra_steps and d_idx < len(dijkstra_steps):
                step_data = dijkstra_steps[d_idx]
            elif sim_state.get("current_dijkstra_step_data"):
                step_data = sim_state.get("current_dijkstra_step_data")

            if step_data:
                u_code = step_data.get("u_code", "")
                u_name = step_data.get("u_name", "")[:20]
                u_dist_str = safe_dist_str(step_data.get("u_dist", 0))
                total_s = len(dijkstra_steps) if dijkstra_steps else step_data.get("total_steps", 1)
                cur_s = d_idx + 1 if dijkstra_steps else step_data.get("step", 1)

                surface.blit(font_xs.render(f"• Bước [{cur_s}/{total_s}]: Chốt đỉnh u* = [{u_code}]", True, (200, 240, 255)), (HUD_X + 16, sub_y))
                sub_y += 18
                surface.blit(font_xs.render(f"  Vị trí: {u_name}", True, (160, 195, 230)), (HUD_X + 16, sub_y))
                sub_y += 18
                surface.blit(font_xs.render(f"  Khoảng cách chốt d[u*]: {u_dist_str}", True, (50, 255, 140)), (HUD_X + 16, sub_y))
                sub_y += 24

                surface.blit(font_xs.render("• Nới lỏng các ngã rẽ kề (Relaxation):", True, (255, 215, 0)), (HUD_X + 16, sub_y))
                sub_y += 18
                for rel in step_data.get("relaxations", [])[:4]:
                    v_code = rel.get("v_code", "")
                    w_m = int(rel.get("w", 0)) if "w" in rel else int(rel.get("new_dist", 0) - rel.get("old_dist", 0)) if not math.isinf(rel.get("new_dist", 0)) else 0
                    if rel.get("updated"):
                        stat_t = "CẬP NHẬT [OK]"
                        stat_col = (60, 255, 140)
                    else:
                        stat_t = "BỎ QUA"
                        stat_col = (150, 175, 205)
                    surface.blit(font_xs.render(f"  -> [{v_code}] (+{abs(w_m)}m): {stat_t}", True, stat_col), (HUD_X + 16, sub_y))
                    sub_y += 17

                sub_y += 10
                surface.blit(font_xs.render("• Thuật toán Dijkstra tìm đường ngắn nhất", True, (255, 200, 50)), (HUD_X + 16, sub_y))
                sub_y += 18
                surface.blit(font_xs.render("• Lan truyền nhãn khoảng cách d[v] từ trạm", True, (180, 220, 255)), (HUD_X + 16, sub_y))
                sub_y += 18
                surface.blit(font_xs.render("• Nới lỏng cạnh kề & khóa đỉnh cự ly cực tiểu", True, (150, 200, 240)), (HUD_X + 16, sub_y))
            else:
                surface.blit(font_xs.render("• Thuật toán BFS tìm trạm gần nhất", True, (50, 255, 180)), (HUD_X + 16, sub_y))
                sub_y += 18
                surface.blit(font_xs.render("• Quét loang đồng tâm qua từng tầng giao lộ", True, (180, 220, 255)), (HUD_X + 16, sub_y))
                sub_y += 18
                surface.blit(font_xs.render("• Tìm trạm trực có ít ngã rẽ cản trở nhất", True, (150, 200, 240)), (HUD_X + 16, sub_y))

        # TRƯỜNG HỢP 2: THUẬT TOÁN BFS ĐANG QUÉT TÌM TRẠM
        elif "BFS" in state_str:
            bfs_box = pygame.Rect(HUD_X + 10, curr_y, HUD_WIDTH - 20, 374)
            pygame.draw.rect(surface, (18, 26, 42), bfs_box, border_radius=5)
            pygame.draw.rect(surface, (255, 200, 50), bfs_box, 1, border_radius=5)

            surface.blit(font_xs.render("BFS: QUÉT TÌM TRẠM CỨU HỘ GẦN NHẤT", True, (255, 215, 0)), (HUD_X + 16, curr_y + 8))
            pygame.draw.line(surface, (55, 50, 25), (HUD_X + 14, curr_y + 26), (HUD_X + HUD_WIDTH - 14, curr_y + 26), 1)

            bfs_steps = sim_state.get("bfs_trace_steps", [])
            c_layer = sim_state.get("current_scan_layer", 1)
            b_y = curr_y + 38
            surface.blit(font_xs.render("• Thuật toán: Breadth-First Search (BFS)", True, (200, 235, 255)), (HUD_X + 16, b_y))
            b_y += 22
            surface.blit(font_xs.render(f"• Tiến trình: Đang lan tỏa tầng sóng Lớp {c_layer}...", True, (255, 160, 60)), (HUD_X + 16, b_y))
            b_y += 22
            surface.blit(font_xs.render(f"• Số nút đã rà soát: {len(bfs_steps)} ngã rẽ xung quanh", True, (180, 215, 245)), (HUD_X + 16, b_y))
            b_y += 22
            surface.blit(font_xs.render("• Mục tiêu: Bệnh viện / PCCC gần nhất còn xe", True, (255, 225, 120)), (HUD_X + 16, b_y))
            b_y += 26
            surface.blit(font_xs.render("• Chạm trạm: Chuyển giao sang Dijkstra", True, (50, 255, 140)), (HUD_X + 16, b_y))
            b_y += 18
            surface.blit(font_xs.render("   để dò 3 phương án (1 chính + 2 phụ né tắc).", True, (160, 210, 200)), (HUD_X + 16, b_y))

        # TRƯỜNG HỢP 3: CÓ DỮ LIỆU TUYẾN ĐƯỜNG (CHỐT / ĐIỀU XE / ĐÃ ĐẾN HIỆN TRƯỜNG)
        elif has_active_routes:
            # 3A. NẾU CÓ TỪ 2 XE / 2 TRẠM TRỞ LÊN (VÍ DỤ TAI NẠN NẶNG DUAL: BV + PCCC):
            # CHIA LÀM 2 KHÚC RÕ RÀNG TRONG THANH BÊN CẠNH THEO YÊU CẦU CỦA NGƯỜI DÙNG
            if len(station_cands) >= 2:
                card_h = 184
                gap_y = 8

                for s_idx, st_info in enumerate(station_cands[:2]):
                    card_y = curr_y + s_idx * (card_h + gap_y)
                    st_type = st_info.get("type", "HOSPITAL")
                    st_name = st_info.get("station_name", f"Trạm {s_idx+1}")
                    st_cands = st_info.get("candidates", [])

                    if st_type == "HOSPITAL":
                        theme_border = (0, 200, 220)
                        theme_bg = (16, 26, 40)
                        hdr_bg = (14, 38, 58)
                        khuc_title = f"KHÚC {s_idx+1}: CẤP CỨU ({st_name[:10]})"
                    else:
                        theme_border = (255, 140, 40)
                        theme_bg = (38, 22, 18)
                        hdr_bg = (56, 28, 20)
                        khuc_title = f"KHÚC {s_idx+1}: PCCC ({st_name[:10]})"

                    box_r = pygame.Rect(HUD_X + 10, card_y, HUD_WIDTH - 20, card_h)
                    pygame.draw.rect(surface, theme_bg, box_r, border_radius=5)
                    pygame.draw.rect(surface, theme_border, box_r, 1, border_radius=5)

                    hdr_r = pygame.Rect(HUD_X + 10, card_y, HUD_WIDTH - 20, 23)
                    pygame.draw.rect(surface, hdr_bg, hdr_r, border_top_left_radius=5, border_top_right_radius=5)
                    pygame.draw.line(surface, theme_border, (HUD_X + 10, card_y + 23), (HUD_X + HUD_WIDTH - 10, card_y + 23), 1)

                    surface.blit(font_xs.render(khuc_title, True, (255, 255, 255)), (HUD_X + 16, card_y + 4))
                    sub_tag = font_xs.render("[3 TUYẾN]", True, (180, 220, 255))
                    surface.blit(sub_tag, (HUD_X + HUD_WIDTH - sub_tag.get_width() - 16, card_y + 4))

                    # 3 Dòng chú thích chi tiết cho từng tuyến
                    r_y = card_y + 28
                    if st_cands:
                        # Tuyến 1 (Chính)
                        c1 = st_cands[0]
                        v1 = c1.get("via_name", "")
                        v1_str = f" • {v1[:14]}" if v1 else ""
                        surface.blit(font_xs.render(f"[1] T.1 (CHÍNH): {c1['km_str']}{v1_str}", True, (50, 255, 140)), (HUD_X + 16, r_y))
                        r_y += 15
                        surface.blit(font_xs.render("   -> Tối ưu: Ngắn nhất, phản ứng nhanh", True, (170, 225, 210)), (HUD_X + 16, r_y))
                        r_y += 18

                        # Đường Phụ 1
                        if len(st_cands) > 1:
                            c2 = st_cands[1]
                            v2 = c2.get("via_name", "")
                            v2_str = f" • {v2[:13]}" if v2 else ""
                            surface.blit(font_xs.render(f"[2] PHỤ 1: {c2['km_str']} ({c2.get('diff_str', '')}){v2_str}", True, (255, 205, 50)), (HUD_X + 16, r_y))
                            r_y += 15
                            surface.blit(font_xs.render("   -> Dự phòng 1: Tự bẻ cua nếu Tuyến 1 kẹt", True, (255, 230, 180)), (HUD_X + 16, r_y))
                            r_y += 18
                        else:
                            surface.blit(font_xs.render("[2] PHỤ 1: Sẵn sàng trực gác hành lang", True, (255, 205, 50)), (HUD_X + 16, r_y))
                            r_y += 33

                        # Đường Phụ 2
                        if len(st_cands) > 2:
                            c3 = st_cands[2]
                            v3 = c3.get("via_name", "")
                            v3_str = f" • {v3[:13]}" if v3 else ""
                            surface.blit(font_xs.render(f"[3] PHỤ 2: {c3['km_str']} ({c3.get('diff_str', '')}){v3_str}", True, (60, 240, 190)), (HUD_X + 16, r_y))
                            r_y += 15
                            surface.blit(font_xs.render("   -> Dự phòng 2: Hành lang thoát hiểm vòng ngoài", True, (170, 235, 215)), (HUD_X + 16, r_y))
                            r_y += 18
                        else:
                            surface.blit(font_xs.render("[3] PHỤ 2: Hành lang bao bọc an toàn", True, (60, 240, 190)), (HUD_X + 16, r_y))
                            r_y += 33

                        # Chip trạng thái ở đáy mỗi khúc
                        is_rerouted = sim_state.get("rerouted", False)
                        if is_rerouted:
                            st_msg = "• ĐÃ TỰ BẺ CUA NÉ KẸT XE (ĐƯỜNG PHỤ)!"
                            st_c = (255, 110, 90)
                        else:
                            st_msg = "• Tuyến thông suốt • Còi ưu tiên mở đường"
                            st_c = (60, 255, 160)
                        surface.blit(font_xs.render(st_msg, True, st_c), (HUD_X + 16, card_y + 164))

            # 3B. NẾU CHỈ CÓ 1 XE / 1 TRẠM (CẤP CỨU HOẶC CỨU HỎA ĐƠN LẺ):
            # HIỂN THỊ 1 HỘP LỚN TOÀN DIỆN VỀ ĐƯỜNG CHÍNH VÀ CÁC ĐƯỜNG PHỤ
            else:
                one_box = pygame.Rect(HUD_X + 10, curr_y, HUD_WIDTH - 20, 374)
                pygame.draw.rect(surface, (18, 26, 42), one_box, border_radius=5)
                pygame.draw.rect(surface, (50, 160, 220), one_box, 1, border_radius=5)

                st_info = station_cands[0] if station_cands else {}
                st_name = st_info.get("station_name", sim_state.get("station_name", "Trạm điều phối"))

                hdr_r = pygame.Rect(HUD_X + 10, curr_y, HUD_WIDTH - 20, 24)
                pygame.draw.rect(surface, (14, 34, 54), hdr_r, border_top_left_radius=5, border_top_right_radius=5)
                pygame.draw.line(surface, (50, 160, 220), (HUD_X + 10, curr_y + 24), (HUD_X + HUD_WIDTH - 10, curr_y + 24), 1)

                surface.blit(font_xs.render("CHÚ THÍCH CÁC TUYẾN ĐƯỜNG", True, (255, 255, 255)), (HUD_X + 16, curr_y + 5))
                sub_tag = font_xs.render("[1 CHÍNH + 2 PHỤ]", True, (50, 255, 180))
                surface.blit(sub_tag, (HUD_X + HUD_WIDTH - sub_tag.get_width() - 16, curr_y + 5))

                cands = st_info.get("candidates", [])
                p_y = curr_y + 29
                surface.blit(font_xs.render(f"Đơn vị: {st_name[:24]}", True, COLOR_TEXT_CYAN), (HUD_X + 16, p_y))
                p_y += 18

                if cands:
                    c1 = cands[0]
                    v1 = c1.get("via_name", "")
                    v1_str = f" qua {v1}" if v1 else ""
                    c1_cost = c1.get("cost", 0)
                    eta1 = c1_cost / 300.0 if c1_cost else 0.0

                    # 1. TUYẾN 1 (CHÍNH)
                    surface.blit(font_xs.render("[1] TUYẾN 1: CHÍNH (ĐANG CHẠY - TỐI ƯU)", True, (50, 255, 140)), (HUD_X + 16, p_y))
                    p_y += 16
                    surface.blit(font_xs.render(f"• Cự ly: {c1['km_str']} | ETA dự kiến: ~{eta1:.1f} phút", True, (220, 245, 255)), (HUD_X + 16, p_y))
                    p_y += 16
                    surface.blit(font_xs.render(f"• Lộ trình: Trục chính{v1_str}", True, (170, 220, 240)), (HUD_X + 16, p_y))
                    p_y += 16
                    surface.blit(font_xs.render("• Đánh giá: Quãng đường ngắn nhất, ưu tiên tuyệt đối", True, (140, 200, 230)), (HUD_X + 16, p_y))
                    p_y += 22

                    pygame.draw.line(surface, (30, 48, 70), (HUD_X + 16, p_y - 4), (HUD_X + HUD_WIDTH - 16, p_y - 4), 1)

                    # 2. ĐƯỜNG PHỤ 1 (DỰ PHÒNG NÉ TẮC)
                    if len(cands) > 1:
                        c2 = cands[1]
                        v2 = c2.get("via_name", "")
                        v2_str = f" qua {v2}" if v2 else ""
                        surface.blit(font_xs.render("[2] ĐƯỜNG PHỤ 1: DỰ PHÒNG BẺ CUA NÉ TẮC", True, (255, 205, 50)), (HUD_X + 16, p_y))
                        p_y += 16
                        surface.blit(font_xs.render(f"• Cự ly: {c2['km_str']} ({c2.get('diff_str', '')}){v2_str}", True, (255, 235, 190)), (HUD_X + 16, p_y))
                        p_y += 16
                        surface.blit(font_xs.render("• Vai trò: Sẵn sàng tự động bẻ cua né tắc Tuyến 1", True, (220, 200, 150)), (HUD_X + 16, p_y))
                        p_y += 16
                        surface.blit(font_xs.render("• Tình trạng: [TỰ ĐỘNG KÍCH HOẠT KHI TẮC ĐƯỜNG]", True, (255, 180, 70)), (HUD_X + 16, p_y))
                        p_y += 22
                    else:
                        surface.blit(font_xs.render("[2] ĐƯỜNG PHỤ 1: Không có đường tránh song song", True, (255, 205, 50)), (HUD_X + 16, p_y))
                        p_y += 40

                    pygame.draw.line(surface, (30, 48, 70), (HUD_X + 16, p_y - 4), (HUD_X + HUD_WIDTH - 16, p_y - 4), 1)

                    # 3. ĐƯỜNG PHỤ 2 (HÀNH LANG DỰ BỊ VÒNG NGOÀI)
                    if len(cands) > 2:
                        c3 = cands[2]
                        v3 = c3.get("via_name", "")
                        v3_str = f" qua {v3}" if v3 else ""
                        surface.blit(font_xs.render("[3] ĐƯỜNG PHỤ 2: HÀNH LANG DỰ BỊ VÒNG NGOÀI", True, (60, 240, 190)), (HUD_X + 16, p_y))
                        p_y += 16
                        surface.blit(font_xs.render(f"• Cự ly: {c3['km_str']} ({c3.get('diff_str', '')}){v3_str}", True, (200, 245, 235)), (HUD_X + 16, p_y))
                        p_y += 16
                        surface.blit(font_xs.render("• Vai trò: Lối thoát hiểm vòng ngoài khi giao lộ nghẽn", True, (160, 225, 210)), (HUD_X + 16, p_y))
                        p_y += 16
                        surface.blit(font_xs.render("• Tình trạng: [HÀNH LANG BAO BỌC AN TOÀN]", True, (40, 220, 170)), (HUD_X + 16, p_y))
                        p_y += 24
                    else:
                        surface.blit(font_xs.render("[3] ĐƯỜNG PHỤ 2: Hành lang bao bọc dự bị", True, (60, 240, 190)), (HUD_X + 16, p_y))
                        p_y += 40

                    # Tình trạng vận hành
                    is_rerouted = sim_state.get("rerouted", False)
                    if is_rerouted:
                        st_box_col = (55, 25, 20)
                        st_border_col = (255, 90, 70)
                        st_txt1 = "• TÌNH HUỐNG: ĐÃ TỰ BẺ CUA NÉ KẸT XE THÀNH CÔNG!"
                        st_txt2 = "   Phương tiện đã chuyển sang Đường Phụ 1 an toàn."
                        txt_col = (255, 120, 100)
                    else:
                        st_box_col = (14, 30, 25)
                        st_border_col = (40, 180, 120)
                        st_txt1 = "• VẬN HÀNH: Tuyến thông suốt • Còi ưu tiên mở đường"
                        st_txt2 = "   Hệ thống sẵn sàng tự bẻ cua nếu Tuyến 1 bị nghẽn."
                        txt_col = (60, 255, 160)

                    bot_r = pygame.Rect(HUD_X + 16, curr_y + 318, HUD_WIDTH - 32, 44)
                    pygame.draw.rect(surface, st_box_col, bot_r, border_radius=4)
                    pygame.draw.rect(surface, st_border_col, bot_r, 1, border_radius=4)
                    surface.blit(font_xs.render(st_txt1, True, txt_col), (HUD_X + 22, curr_y + 322))
                    surface.blit(font_xs.render(st_txt2, True, (200, 230, 220)), (HUD_X + 22, curr_y + 340))
                else:
                    # Fallback nếu chỉ có current_path hoặc all_paths
                    c_val = sim_state.get("route_cost", 0)
                    c_km_str = safe_dist_str(c_val)
                    eta_mins = c_val / 300.0 if c_val else 0.0
                    surface.blit(font_xs.render(f"📍 TỔNG CỰ LY LỘ TRÌNH: {c_km_str}", True, (0, 255, 200)), (HUD_X + 16, p_y))
                    p_y += 18
                    surface.blit(font_xs.render(f"⏱ Thời gian dự kiến (ETA): ~{eta_mins:.1f} phút", True, COLOR_TEXT_HIGHLIGHT), (HUD_X + 16, p_y))
                    p_y += 24
                    all_paths = sim_state.get("all_paths", [])
                    if all_paths:
                        p_nodes = all_paths[0].get("path", [])
                        seq_str = " > ".join([self.city_graph.nodes[n]["code"] for n in p_nodes])
                        if len(seq_str) > 34:
                            seq_str = seq_str[:34] + "..."
                        surface.blit(font_xs.render(f"• Các chặng: {seq_str}", True, (150, 175, 205)), (HUD_X + 16, p_y))

        # TRƯỜNG HỢP 4: TRẠNG THÁI SẴN SÀNG / NGHỈ (IDLE)
        else:
            idle_box = pygame.Rect(HUD_X + 10, curr_y, HUD_WIDTH - 20, 374)
            pygame.draw.rect(surface, (18, 26, 42), idle_box, border_radius=5)
            pygame.draw.rect(surface, COLOR_PANEL_BORDER, idle_box, 1, border_radius=5)

            surface.blit(font_xs.render("CƠ CHẾ DÒ 3 ĐƯỜNG & DỰ PHÒNG NÉ TẮC", True, (50, 255, 180)), (HUD_X + 16, curr_y + 8))
            pygame.draw.line(surface, (40, 55, 80), (HUD_X + 14, curr_y + 26), (HUD_X + HUD_WIDTH - 14, curr_y + 26), 1)

            i_y = curr_y + 36
            surface.blit(font_xs.render("• Thuật toán cốt lõi: Dijkstra + BFS đa tầng", True, (200, 230, 255)), (HUD_X + 16, i_y))
            i_y += 22
            surface.blit(font_xs.render("• 1 Tuyến chính (T.1): Ngắn nhất theo Dijkstra", True, (60, 255, 140)), (HUD_X + 16, i_y))
            i_y += 22
            surface.blit(font_xs.render("• Đường Phụ 1: Dự phòng né tắc, tự bẻ cua", True, (255, 205, 50)), (HUD_X + 16, i_y))
            i_y += 22
            surface.blit(font_xs.render("• Đường Phụ 2: Hành lang an toàn bao bọc", True, (60, 240, 190)), (HUD_X + 16, i_y))
            i_y += 22
            surface.blit(font_xs.render("• Đa phương tiện: Điều động song song BV + PCCC", True, COLOR_TEXT_CYAN), (HUD_X + 16, i_y))
            i_y += 26
            surface.blit(font_xs.render("• Thao tác nhanh: Click chuột trái ngã tư trên sa bàn", True, (255, 200, 50)), (HUD_X + 16, i_y))
            i_y += 18
            surface.blit(font_xs.render("  để phát lệnh điều xe [CẤP CỨU], [CỨU HỎA] hoặc [LIÊN BỘ].", True, (160, 185, 215)), (HUD_X + 16, i_y))
            i_y += 24
            surface.blit(font_xs.render("• Thử thách né tắc: Chuột phải vào đường đang chạy", True, (255, 140, 70)), (HUD_X + 16, i_y))
            i_y += 18
            surface.blit(font_xs.render("  để bơm kẹt xe và xem thuật toán tự bẻ cua!", True, (255, 180, 120)), (HUD_X + 16, i_y))

        # 6. HỘP HƯỚNG DẪN TƯƠNG TÁC ĐIỀU KHIỂN (GỌN GÀNG Ở ĐÁY MÀN HÌNH 720P)
        guide_box = pygame.Rect(HUD_X + 10, 594, HUD_WIDTH - 20, 118)
        pygame.draw.rect(surface, (16, 22, 34), guide_box, border_radius=5)
        pygame.draw.rect(surface, (35, 50, 75), guide_box, 1, border_radius=5)

        g_title = font_xs.render("HƯỚNG DẪN TƯƠNG TÁC ĐIỀU KHIỂN", True, (255, 215, 0))
        surface.blit(g_title, (HUD_X + 16, 600))
        pygame.draw.line(surface, (40, 55, 80), (HUD_X + 14, 616), (HUD_X + HUD_WIDTH - 14, 616), 1)

        guides = [
            ("• Chuột Trái Node:", "Mở Menu điều [CẤP CỨU], [PCCC] hoặc [LIÊN BỘ]"),
            ("• Chuột Phải Tuyến:", "Bơm kẹt xe (Dijkstra bẻ cua né tắc)"),
            ("• Nút Đặt Lại / [C]:", "Xóa sạch hiện trường, hồi sinh đội xe"),
            ("• Phím [M]:", "Bật/Tắt Cây khung Kruskal cáp quang"),
            ("• Phím [Space]:", "Tạm dừng / Tiếp tục mô phỏng"),
        ]

        g_y = 622
        for key_t, desc_t in guides:
            surface.blit(font_xs.render(f"{key_t} {desc_t}", True, (170, 190, 215)), (HUD_X + 16, g_y))
            g_y += 18


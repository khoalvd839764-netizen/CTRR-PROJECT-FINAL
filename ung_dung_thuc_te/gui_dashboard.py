"""
Module: ung_dung_thuc_te/gui_dashboard.py
Mục đích: Giao diện trực quan hóa Đa góc nhìn (Multi-view Dashboard) 3 Cột cho Ứng Dụng Thực Tế Robot Hút Bụi:
  - CỘT 1 (Trái): Sa Bàn Căn Hộ 3D Isometric (Xoay 360°, Zoom 40%-300%, Nội thất 3D né vật cản, Robot phát quang).
  - CỘT 2 (Giữa): Đồ Thị Toán Học G = (V, E) (25 đỉnh, 36 cung cong Bézier không đè nét, quả cầu năng lượng).
  - CỘT 3 (Phải): Bộ Soi Mã Giả & Biến Trực Tiếp (Pseudocode Line Highlight, Live DSU/Queue/Stack/Flow, Bảng điều khiển).
"""

import sys
import math
import pygame
import os

from ung_dung_thuc_te.data_model import (
    HOUSE_NODES_DATA, HOUSE_BASE_COORDS, HOUSE_EDGES,
    EDGE_CURVATURE, ROOMS_LAYOUT_3D, FURNITURE_3D_BLOCKS
)
from ung_dung_thuc_te.algorithms import RobotAlgorithms

# =============================================================================
# CẤU HÌNH KÍCH THƯỚC VÀ MÀU SẮC GIAO DIỆN CHUẨN DASHBOARD
# =============================================================================
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60

# Kích thước 3 Cột
COL_Y = 56
COL_HEIGHT = 804

COL1_X = 16
COL1_WIDTH = 510

COL2_X = 540
COL2_WIDTH = 680

COL3_X = 1234
COL3_WIDTH = 520

# Bảng màu Dark Cyber UI cao cấp
COLOR_APP_BG = (10, 15, 29)
COLOR_CARD_BG = (17, 24, 39)
COLOR_CARD_BORDER = (31, 41, 55)
COLOR_CARD_BORDER_GLOW = (56, 189, 248)

COLOR_TEXT_WHITE = (248, 250, 252)
COLOR_TEXT_CYAN = (56, 189, 248)
COLOR_TEXT_GOLD = (250, 204, 21)
COLOR_TEXT_GREEN = (52, 211, 153)
COLOR_TEXT_RED = (248, 113, 113)
COLOR_TEXT_MUTED = (148, 163, 184)


def get_vietnamese_font(size, bold=False):
    """Tải font hỗ trợ đầy đủ dấu tiếng Việt Unicode chuẩn UTF-8."""
    candidates = [
        "dejavusans", "liberationsans", "notosans", "arial", "segoeui", "tahoma"
    ]
    for font_name in candidates:
        try:
            f = pygame.font.SysFont(font_name, size, bold=bold)
            if f:
                return f
        except Exception:
            continue
    return pygame.font.Font(None, size)


class SmartRobotSimulationApp:
    """
    Lớp điều phối toàn bộ Ứng Dụng Thực Tế Robot Hút Bụi Thông Minh.
    """
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("ROBOT HÚT BỤI THÔNG MINH — ỨNG DỤNG THỰC TẾ CTRR 100%")

        self.is_fullscreen = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
        self.clock = pygame.time.Clock()

        # Hệ thống Font chữ phân cấp
        self.font_title = get_vietnamese_font(15, bold=True)
        self.font_main = get_vietnamese_font(13, bold=True)
        self.font_body = get_vietnamese_font(11, bold=False)
        self.font_code = get_vietnamese_font(11, bold=True)
        self.font_tag = get_vietnamese_font(10, bold=True)
        self.font_small = get_vietnamese_font(10, bold=False)

        # Mô hình Dữ liệu căn hộ
        self.nodes_data = dict(HOUSE_NODES_DATA)
        self.base_coords = dict(HOUSE_BASE_COORDS)
        self.edges = list(HOUSE_EDGES)
        self.n = len(self.nodes_data)
        self.curvatures = {tuple(sorted(k)): v for k, v in EDGE_CURVATURE.items()}

        # Khởi tạo Bộ sinh thuật toán
        self.algo_engine = RobotAlgorithms(n=self.n, edges=self.edges, nodes_data=self.nodes_data)

        # Camera 3D & Điều khiển Zoom / Pan
        self.is_3d_mode = True
        self.cam_yaw = 45.0
        self.cam_pitch = 38.0
        self.cam_zoom = 0.95
        self.cam_pan_x = 0
        self.cam_pan_y = 0
        self.is_dragging_3d = False
        self.is_panning_3d = False
        self.last_mouse_pos = (0, 0)

        # Trạng thái Mô phỏng
        self.active_mode = "MST"
        self.steps = []
        self.current_step_idx = 0
        self.is_auto_playing = False
        self.auto_timer = 0
        self.pulse_val = 0.0
        self.lidar_angle = 0.0

        # Animation lướt mượt mà giữa các điểm (0.0 -> 1.0)
        self.anim_t = 1.0
        self.anim_speed = 0.035

        # Danh sách Nút Menu Chế độ
        self.top_buttons = []
        self.init_top_buttons()

        # Nút điều khiển Zoom / Pan / 3D ở Cột 1
        self.btn_zoom_out_rect = pygame.Rect(COL1_X + 288, COL_Y + 10, 26, 26)
        self.btn_zoom_badge_rect = pygame.Rect(COL1_X + 318, COL_Y + 10, 56, 26)
        self.btn_zoom_in_rect = pygame.Rect(COL1_X + 378, COL_Y + 10, 26, 26)
        self.btn_view_3d_rect = pygame.Rect(COL1_X + 410, COL_Y + 10, 88, 26)

        # Nút điều khiển Bước ở Cột 3
        btn_y = COL_Y + COL_HEIGHT - 44
        self.btn_prev_rect = pygame.Rect(COL3_X + 16, btn_y, 90, 32)
        self.btn_next_rect = pygame.Rect(COL3_X + 114, btn_y, 110, 32)
        self.btn_auto_rect = pygame.Rect(COL3_X + 232, btn_y, 150, 32)
        self.btn_reset_rect = pygame.Rect(COL3_X + 390, btn_y, 80, 32)
        self.btn_fullscreen_rect = pygame.Rect(COL3_X + 478, btn_y, (COL3_WIDTH - 32) - 462, 32)

        # Khởi động thuật toán mặc định
        self.switch_mode("MST")

    def init_top_buttons(self):
        """Khởi tạo 7 nút chọn nhanh thuật toán trên thanh Top Bar."""
        modes = [
            ("[1] Kruskal MST", "MST", (52, 211, 153)),
            ("[2] Dijkstra Về Sạc", "DIJKSTRA", (56, 189, 248)),
            ("[3] BFS SLAM Map", "BFS", (14, 165, 233)),
            ("[4] DFS Quét Sâu", "DFS", (168, 85, 247)),
            ("[5] Euler Toàn Nhà", "EULER", (250, 204, 21)),
            ("[6] Đồ Thị 2 Phía", "BIPARTITE", (236, 72, 153)),
            ("[7] Max-Flow Hộp Rác", "MAXFLOW", (248, 113, 113))
        ]
        buttons = []
        btn_w = (SCREEN_WIDTH - 32 - 6 * 8) // 7
        btn_h = 34
        for i, (label, mode_id, color) in enumerate(modes):
            bx = 16 + i * (btn_w + 8)
            rect = pygame.Rect(bx, 10, btn_w, btn_h)
            buttons.append((rect, label, mode_id, color))
        self.top_buttons = buttons

    def get_column1_pos(self, node_id, z=0):
        """Chiếu điểm (x, y, z) của Căn hộ sang tọa độ màn hình ở Cột 1 (3D Isometric hoặc 2D)."""
        base_x, base_y = self.base_coords[node_id]
        center_x, center_y = 290, 410
        cx = COL1_WIDTH // 2 + self.cam_pan_x
        cy = COL_HEIGHT // 2 + 10 + self.cam_pan_y

        if not self.is_3d_mode:
            sx = cx + (base_x + 15 - center_x) * self.cam_zoom
            sy = cy + (base_y + 15 - center_y) * self.cam_zoom
            return int(sx), int(sy)

        return self.get_3d_point(base_x, base_y, z, cx, cy)

    def get_3d_point(self, x, y, z, cx, cy):
        """Công thức phép chiếu 3D Isometric chuẩn: Xoay quanh trục Yaw và nghiêng Pitch."""
        rel_x = x - 290
        rel_y = y - 410

        rad_yaw = math.radians(self.cam_yaw)
        x1 = rel_x * math.cos(rad_yaw) - rel_y * math.sin(rad_yaw)
        y1 = rel_x * math.sin(rad_yaw) + rel_y * math.cos(rad_yaw)
        z1 = z

        rad_pitch = math.radians(self.cam_pitch)
        x2 = x1
        y2 = y1 * math.cos(rad_pitch) - z1 * math.sin(rad_pitch)

        sx = cx + x2 * self.cam_zoom
        sy = cy + y2 * self.cam_zoom
        return int(sx), int(sy)

    def get_column2_graph_pos(self, node_id):
        """Tính tọa độ 2D thông thoáng ở Cột 2 (Đồ thị Toán học)."""
        base_x, base_y = self.base_coords[node_id]
        scale_x = (COL2_WIDTH - 90) / 440.0
        scale_y = (COL_HEIGHT - 140) / 600.0
        gx = int((base_x - 60) * scale_x + 45)
        gy = int((base_y - 100) * scale_y + 75)
        return gx, gy

    def get_arc_points(self, p1, p2, edge_tuple, num_segments=10):
        """Tạo chuỗi điểm theo đường cong Bézier bậc 2 (Quadratic Bézier) chống đè nét."""
        offset = self.curvatures.get(edge_tuple, 0)
        if offset == 0:
            return [p1, p2], ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)

        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        dist = math.hypot(dx, dy)
        if dist == 0:
            return [p1, p2], p1

        nx = -dy / dist
        ny = dx / dist
        cx = (x1 + x2) / 2.0 + nx * offset
        cy = (y1 + y2) / 2.0 + ny * offset

        pts = []
        for i in range(num_segments + 1):
            t = i / float(num_segments)
            bx = (1.0 - t)**2 * x1 + 2.0 * (1.0 - t) * t * cx + t**2 * x2
            by = (1.0 - t)**2 * y1 + 2.0 * (1.0 - t) * t * cy + t**2 * y2
            pts.append((int(bx), int(by)))

        mid_pt = pts[num_segments // 2]
        return pts, mid_pt

    def get_interpolated_arc_pos(self, p1, p2, edge_tuple, t):
        """Tính vị trí robot mượt mà dọc theo đường cong Bézier tại thời điểm t in [0.0, 1.0]."""
        offset = self.curvatures.get(edge_tuple, 0)
        if offset == 0:
            return int((1.0 - t) * p1[0] + t * p2[0]), int((1.0 - t) * p1[1] + t * p2[1])

        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        dist = math.hypot(dx, dy)
        if dist == 0:
            return p1

        nx = -dy / dist
        ny = dx / dist
        cx = (x1 + x2) / 2.0 + nx * offset
        cy = (y1 + y2) / 2.0 + ny * offset

        bx = (1.0 - t)**2 * x1 + 2.0 * (1.0 - t) * t * cx + t**2 * x2
        by = (1.0 - t)**2 * y1 + 2.0 * (1.0 - t) * t * cy + t**2 * y2
        return int(bx), int(by)

    def draw_3d_quad(self, surf, p1, p2, p3, p4, fill_col, border_col=None):
        """Vẽ mặt tứ giác 3D với thuật toán Back-face Culling loại bỏ mặt khuất."""
        pts = [p1, p2, p3, p4]
        cross = (p2[0] - p1[0]) * (p3[1] - p2[1]) - (p2[1] - p1[1]) * (p3[0] - p2[0])
        if cross > 0:
            pygame.draw.polygon(surf, fill_col, pts)
            if border_col:
                pygame.draw.polygon(surf, border_col, pts, 1)

    def draw_3d_box(self, surf, x, y, z, w, d, h, col_top, col_side_x, col_side_y, border_col=None):
        """Vẽ khối hộp 3D nội thất đặc hoàn chỉnh (Đáy, Thân và Nắp) chuẩn Isometric."""
        cx = COL1_WIDTH // 2 + self.cam_pan_x
        cy = COL_HEIGHT // 2 + 10 + self.cam_pan_y

        b0 = self.get_3d_point(x, y, z, cx, cy)
        b1 = self.get_3d_point(x + w, y, z, cx, cy)
        b2 = self.get_3d_point(x + w, y + d, z, cx, cy)
        b3 = self.get_3d_point(x, y + d, z, cx, cy)

        t0 = self.get_3d_point(x, y, z + h, cx, cy)
        t1 = self.get_3d_point(x + w, y, z + h, cx, cy)
        t2 = self.get_3d_point(x + w, y + d, z + h, cx, cy)
        t3 = self.get_3d_point(x, y + d, z + h, cx, cy)

        sh_s = pygame.Surface((COL1_WIDTH, COL_HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(sh_s, (0, 0, 0, 70), [b0, b1, b2, b3])
        surf.blit(sh_s, (0, 0))

        self.draw_3d_quad(surf, b0, b1, t1, t0, col_side_y, border_col)
        self.draw_3d_quad(surf, b1, b2, t2, t1, col_side_x, border_col)
        self.draw_3d_quad(surf, b2, b3, t3, t2, col_side_y, border_col)
        self.draw_3d_quad(surf, b3, b0, t0, t3, col_side_x, border_col)
        self.draw_3d_quad(surf, t0, t1, t2, t3, col_top, border_col)

    # =========================================================================
    # RENDER CỘT 1: SA BÀN CĂN HỘ 3D ISOMETRIC
    # =========================================================================
    def draw_column_1_floorplan(self, cur_step):
        surf = pygame.Surface((COL1_WIDTH, COL_HEIGHT))
        surf.fill(COLOR_CARD_BG)

        mode_str = "3D ISOMETRIC" if self.is_3d_mode else "2D TOP-DOWN"
        t_col1 = self.font_main.render(f"🏠 CỘT 1: CĂN HỘ ({mode_str})", True, COLOR_TEXT_CYAN)
        surf.blit(t_col1, (16, 12))

        zoom_pct = int(round(self.cam_zoom * 100))
        surf.blit(self.font_small.render(f"Cuộn chuột / Phím [+/-] Zoom: {zoom_pct}% • Trái: Xoay 360° • Phải: Dời", True, COLOR_TEXT_MUTED), (16, 32))

        # Nút Zoom Out [-]
        pygame.draw.rect(surf, (30, 41, 59), (288, 10, 26, 26), border_radius=4)
        pygame.draw.rect(surf, (71, 85, 105), (288, 10, 26, 26), width=1, border_radius=4)
        z_out_t = self.font_main.render("-", True, COLOR_TEXT_WHITE)
        surf.blit(z_out_t, (288 + 13 - z_out_t.get_width()//2, 10 + 13 - z_out_t.get_height()//2 - 1))

        # Badge Zoom % / Reset
        pygame.draw.rect(surf, (15, 23, 42), (318, 10, 56, 26), border_radius=4)
        z_border_c = COLOR_TEXT_CYAN if zoom_pct != 95 else (71, 85, 105)
        pygame.draw.rect(surf, z_border_c, (318, 10, 56, 26), width=1, border_radius=4)
        z_pct_t = self.font_tag.render(f"{zoom_pct}%", True, COLOR_TEXT_CYAN if zoom_pct != 95 else COLOR_TEXT_MUTED)
        surf.blit(z_pct_t, (318 + 28 - z_pct_t.get_width()//2, 10 + 13 - z_pct_t.get_height()//2))

        # Nút Zoom In [+]
        pygame.draw.rect(surf, (30, 41, 59), (378, 10, 26, 26), border_radius=4)
        pygame.draw.rect(surf, (71, 85, 105), (378, 10, 26, 26), width=1, border_radius=4)
        z_in_t = self.font_main.render("+", True, COLOR_TEXT_WHITE)
        surf.blit(z_in_t, (378 + 13 - z_in_t.get_width()//2, 10 + 13 - z_in_t.get_height()//2 - 1))

        # Nút Đổi 3D / 2D
        b3d_bg = (14, 116, 144) if self.is_3d_mode else (30, 41, 59)
        pygame.draw.rect(surf, b3d_bg, (410, 10, 88, 26), border_radius=4)
        pygame.draw.rect(surf, COLOR_TEXT_CYAN, (410, 10, 88, 26), width=1, border_radius=4)
        b3d_lbl = "🎮 3D" if self.is_3d_mode else "📐 2D"
        b3d_t = self.font_tag.render(b3d_lbl, True, (255, 255, 255))
        surf.blit(b3d_t, (410 + 44 - b3d_t.get_width()//2, 10 + 13 - b3d_t.get_height()//2))

        scanned_edge = cur_step.get("scanned_edge") if cur_step else None
        chosen_edges = cur_step.get("after_chosen", set()) if cur_step else set()

        # 1. Vẽ Mặt sàn kiến trúc 5 phòng
        cx, cy = COL1_WIDTH // 2 + self.cam_pan_x, COL_HEIGHT // 2 + 10 + self.cam_pan_y
        for rx, ry, rw, rh, rname, rcol, grid_col in ROOMS_LAYOUT_3D:
            if self.is_3d_mode:
                p0 = self.get_3d_point(rx, ry, 0, cx, cy)
                p1 = self.get_3d_point(rx + rw, ry, 0, cx, cy)
                p2 = self.get_3d_point(rx + rw, ry + rh, 0, cx, cy)
                p3 = self.get_3d_point(rx, ry + rh, 0, cx, cy)

                floor_surf = pygame.Surface((COL1_WIDTH, COL_HEIGHT), pygame.SRCALPHA)
                pygame.draw.polygon(floor_surf, rcol, [p0, p1, p2, p3])
                pygame.draw.polygon(floor_surf, (51, 65, 85), [p0, p1, p2, p3], 1)

                grid_spacing = 45
                for gx in range(rx + grid_spacing, rx + rw, grid_spacing):
                    gp0 = self.get_3d_point(gx, ry, 0, cx, cy)
                    gp1 = self.get_3d_point(gx, ry + rh, 0, cx, cy)
                    pygame.draw.line(floor_surf, grid_col, gp0, gp1, 1)
                for gy in range(ry + grid_spacing, ry + rh, grid_spacing):
                    gp0 = self.get_3d_point(rx, gy, 0, cx, cy)
                    gp1 = self.get_3d_point(rx + rw, gy, 0, cx, cy)
                    pygame.draw.line(floor_surf, grid_col, gp0, gp1, 1)

                surf.blit(floor_surf, (0, 0))
                surf.blit(self.font_tag.render(rname, True, (148, 163, 184)), (p0[0] - 10, p0[1] - 8))
            else:
                center_x, center_y = 290, 410
                sx = int(cx + (rx - center_x) * self.cam_zoom)
                sy = int(cy + (ry - center_y) * self.cam_zoom)
                sw = max(1, int(rw * self.cam_zoom))
                sh = max(1, int(rh * self.cam_zoom))
                r_surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
                pygame.draw.rect(r_surf, rcol, (0, 0, sw, sh), border_radius=max(1, int(6 * self.cam_zoom)))
                pygame.draw.rect(r_surf, (51, 65, 85), (0, 0, sw, sh), width=1, border_radius=max(1, int(6 * self.cam_zoom)))
                surf.blit(r_surf, (sx, sy))
                surf.blit(self.font_tag.render(rname, True, (148, 163, 184)), (sx + 8, sy + 6))

        # 2. Vẽ Đồ nội thất 3D đặc né vật cản với Painter's Depth Sorting
        if self.is_3d_mode:
            rad_yaw = math.radians(self.cam_yaw)
            def get_depth(item):
                cx_item = item["x"] + item["w"] / 2.0 - 290
                cy_item = item["y"] + item["d"] / 2.0 - 410
                return cx_item * math.sin(rad_yaw) + cy_item * math.cos(rad_yaw)

            sorted_furniture = sorted(FURNITURE_3D_BLOCKS, key=get_depth)
            for item in sorted_furniture:
                self.draw_3d_box(surf, item["x"], item["y"], item["z"], item["w"], item["d"], item["h"], item["top"], item["sx"], item["sy"], (30, 41, 59))

            # Tường 3D kiến trúc
            for rx, ry, rw, rh, _, _, _ in ROOMS_LAYOUT_3D:
                p0 = self.get_3d_point(rx, ry, 0, cx, cy)
                p1 = self.get_3d_point(rx + rw, ry, 0, cx, cy)
                p2 = self.get_3d_point(rx + rw, ry + rh, 0, cx, cy)
                p3 = self.get_3d_point(rx, ry + rh, 0, cx, cy)

                p0_t = self.get_3d_point(rx, ry, 26, cx, cy)
                p1_t = self.get_3d_point(rx + rw, ry, 26, cx, cy)
                p2_t = self.get_3d_point(rx + rw, ry + rh, 26, cx, cy)
                p3_t = self.get_3d_point(rx, ry + rh, 26, cx, cy)

                for b, t in [(p0, p0_t), (p1, p1_t), (p2, p2_t), (p3, p3_t)]:
                    pygame.draw.line(surf, (100, 116, 139), b, t, 2)
                pygame.draw.polygon(surf, (71, 85, 105, 120), [p0_t, p1_t, p2_t, p3_t], 2)

        # 3. Vẽ Cung đường cong Bézier né vật cản
        seen = set()
        for u, v, l_m, cap in self.edges:
            edge_tuple = tuple(sorted((u, v)))
            if edge_tuple in seen:
                continue
            seen.add(edge_tuple)

            p1 = self.get_column1_pos(u, z=4)
            p2 = self.get_column1_pos(v, z=4)
            pts, mid_pt = self.get_arc_points(p1, p2, edge_tuple)

            if edge_tuple == scanned_edge:
                pygame.draw.lines(surf, COLOR_TEXT_GOLD, False, pts, 5)
            elif edge_tuple in chosen_edges:
                col = COLOR_TEXT_GREEN if self.active_mode != "DIJKSTRA" else COLOR_TEXT_CYAN
                pygame.draw.lines(surf, col, False, pts, 4)
            else:
                pygame.draw.lines(surf, (56, 189, 248, 160) if self.is_3d_mode else (51, 65, 85), False, pts, 2)

        # 4. Vẽ 25 Đỉnh quét bụi
        for i, d in self.nodes_data.items():
            p_node = self.get_column1_pos(i, z=8)
            p_ground = self.get_column1_pos(i, z=0)

            ntype = d["room"]
            is_dock = (ntype == "DOCK" and i == 0)
            is_cur = (cur_step and (i == cur_step.get("current_u") or i == cur_step.get("current_v")))

            color = (236, 72, 153) if is_dock else ((59, 130, 246) if d["zone"] == "DRY" else (245, 158, 11))
            
            if self.is_3d_mode:
                pygame.draw.line(surf, (148, 163, 184, 160), p_ground, p_node, 1)

            if is_cur:
                pygame.draw.circle(surf, COLOR_TEXT_GOLD, p_node, 18, 2)

            r = 11 if is_dock else 9
            pygame.draw.circle(surf, color, p_node, r)
            pygame.draw.circle(surf, (255, 255, 255), p_node, r, 1)

            id_txt = self.font_tag.render(str(i), True, (255, 255, 255))
            surf.blit(id_txt, (p_node[0] - id_txt.get_width() // 2, p_node[1] - id_txt.get_height() // 2))

        # 5. Vẽ Robot Roomba 3D phát quang di chuyển đồng bộ
        if cur_step:
            u = cur_step.get("current_u", 0)
            v = cur_step.get("current_v", 0)
            u_p = self.get_column1_pos(u, z=0)
            v_p = self.get_column1_pos(v, z=0)

            edge_tuple = tuple(sorted((u, v)))
            rx, ry = self.get_interpolated_arc_pos(u_p, v_p, edge_tuple, self.anim_t)

            scale = max(0.6, min(2.5, self.cam_zoom))
            bot_base = (rx, ry)
            bot_top = (rx, int(ry - 14 * scale))
            bot_lidar = (rx, int(ry - 20 * scale))

            bw = int(16 * scale)
            bh = int(8 * scale)

            sh_s = pygame.Surface((COL1_WIDTH, COL_HEIGHT), pygame.SRCALPHA)
            pygame.draw.ellipse(sh_s, (0, 0, 0, 110), (bot_base[0] - bw - 2, bot_base[1] - bh - 1, (bw + 2) * 2, (bh + 1) * 2))
            pygame.draw.ellipse(sh_s, (56, 189, 248, 60), (bot_base[0] - bw - 8, bot_base[1] - bh - 5, (bw + 8) * 2, (bh + 5) * 2))
            surf.blit(sh_s, (0, 0))

            pygame.draw.ellipse(surf, (30, 41, 59), (bot_base[0] - bw, bot_base[1] - bh, bw * 2, bh * 2))
            pygame.draw.line(surf, (148, 163, 184), (bot_base[0] - int(14 * scale), bot_base[1]), (bot_top[0] - int(14 * scale), bot_top[1]), max(1, int(2 * scale)))
            pygame.draw.line(surf, (148, 163, 184), (bot_base[0] + int(14 * scale), bot_base[1]), (bot_top[0] + int(14 * scale), bot_top[1]), max(1, int(2 * scale)))
            pygame.draw.ellipse(surf, (241, 245, 249), (bot_top[0] - int(14 * scale), bot_top[1] - int(7 * scale), int(28 * scale), int(14 * scale)))
            pygame.draw.ellipse(surf, (56, 189, 248), (bot_top[0] - int(10 * scale), bot_top[1] - int(5 * scale), int(20 * scale), int(10 * scale)), 1)

            pygame.draw.circle(surf, (239, 68, 68), bot_lidar, max(2, int(4 * scale)))

            for b in range(6):
                rad = math.radians(self.lidar_angle + b * 60)
                bx = rx + int(30 * scale * math.cos(rad))
                by = ry + int(15 * scale * math.sin(rad))
                pygame.draw.line(surf, (56, 189, 248, 160), bot_lidar, (bx, by), 1)

        self.screen.blit(surf, (COL1_X, COL_Y))
        pygame.draw.rect(self.screen, COLOR_CARD_BORDER, (COL1_X, COL_Y, COL1_WIDTH, COL_HEIGHT), 2)

    # =========================================================================
    # RENDER CỘT 2: ĐỒ THỊ TOÁN HỌC G = (V, E)
    # =========================================================================
    def draw_column_2_graph(self, cur_step):
        surf = pygame.Surface((COL2_WIDTH, COL_HEIGHT))
        surf.fill(COLOR_CARD_BG)

        t_col2 = self.font_main.render("📐 CỘT 2: ĐỒ THỊ TOÁN HỌC G = (V, E)", True, COLOR_TEXT_GOLD)
        surf.blit(t_col2, (16, 12))

        surf.blit(self.font_small.render("Cung cong Bézier tách biệt 100%: Dễ nhìn, không đè lên nhau", True, COLOR_TEXT_MUTED), (16, 30))

        graph_bg = pygame.Rect(16, 52, COL2_WIDTH - 32, COL_HEIGHT - 68)
        pygame.draw.rect(surf, (15, 23, 42), graph_bg, border_radius=6)
        pygame.draw.rect(surf, (31, 41, 55), graph_bg, width=1, border_radius=6)

        scanned_edge = cur_step.get("scanned_edge") if cur_step else None
        chosen_edges = cur_step.get("after_chosen", set()) if cur_step else set()
        rejected_edges = cur_step.get("after_rejected", set()) if cur_step else set()

        self.pulse_val = (self.pulse_val + 0.12) % (math.pi * 2)
        glow_w = int(5 + 2 * math.sin(self.pulse_val))

        # 1. Vẽ 36 cung Bézier không đè nét
        seen = set()
        for u, v, l_m, cap in self.edges:
            edge_tuple = tuple(sorted((u, v)))
            if edge_tuple in seen:
                continue
            seen.add(edge_tuple)

            p1 = self.get_column2_graph_pos(u)
            p2 = self.get_column2_graph_pos(v)
            pts, mid_pt = self.get_arc_points(p1, p2, edge_tuple)

            is_scan = (edge_tuple == scanned_edge)
            is_pick = (edge_tuple in chosen_edges)
            is_rej = (edge_tuple in rejected_edges)

            if is_scan:
                pygame.draw.lines(surf, COLOR_TEXT_GOLD, False, pts, glow_w)
            elif is_pick:
                col = COLOR_TEXT_GREEN if self.active_mode != "DIJKSTRA" else COLOR_TEXT_CYAN
                pygame.draw.lines(surf, col, False, pts, 4)
            elif is_rej:
                pygame.draw.lines(surf, (239, 68, 68, 120), False, pts, 2)
            else:
                pygame.draw.lines(surf, (51, 65, 85), False, pts, 2)

            mx, my = mid_pt
            tag_col = COLOR_TEXT_GOLD if is_scan else (COLOR_TEXT_GREEN if is_pick else (COLOR_TEXT_RED if is_rej else (148, 163, 184)))
            bg_col = (55, 48, 163) if is_scan else ((6, 78, 59) if is_pick else ((127, 29, 29) if is_rej else (15, 23, 42)))
            
            tag_surf = self.font_tag.render(f"{l_m:.1f}m", True, tag_col)
            t_rect = pygame.Rect(mx - tag_surf.get_width()//2 - 2, my - tag_surf.get_height()//2 - 1, tag_surf.get_width() + 4, tag_surf.get_height() + 2)
            pygame.draw.rect(surf, bg_col, t_rect, border_radius=3)
            pygame.draw.rect(surf, tag_col if (is_scan or is_pick) else (51, 65, 85), t_rect, width=1, border_radius=3)
            surf.blit(tag_surf, (mx - tag_surf.get_width()//2, my - tag_surf.get_height()//2))

        # 2. Quả cầu năng lượng di chuyển đồng bộ
        if cur_step:
            u = cur_step.get("current_u", 0)
            v = cur_step.get("current_v", 0)
            u_p = self.get_column2_graph_pos(u)
            v_p = self.get_column2_graph_pos(v)

            edge_tuple = tuple(sorted((u, v)))
            ox, oy = self.get_interpolated_arc_pos(u_p, v_p, edge_tuple, self.anim_t)

            pygame.draw.circle(surf, (56, 189, 248, 60), (ox, oy), 16)
            pygame.draw.circle(surf, COLOR_TEXT_CYAN, (ox, oy), 8)
            pygame.draw.circle(surf, (255, 255, 255), (ox, oy), 4)

        # 3. Vẽ 25 Đỉnh toán học
        for i, d in self.nodes_data.items():
            gx, gy = self.get_column2_graph_pos(i)
            is_cur = (cur_step and (i == cur_step.get("current_u") or i == cur_step.get("current_v")))
            is_dock = (i == 0)

            color = (236, 72, 153) if is_dock else ((59, 130, 246) if d["zone"] == "DRY" else (245, 158, 11))
            r = 14 if is_dock else 12

            if is_cur:
                pygame.draw.circle(surf, COLOR_TEXT_GOLD, (gx, gy), 22, 2)
                pygame.draw.circle(surf, (250, 204, 21, 60), (gx, gy), 28, 1)

            pygame.draw.circle(surf, color, (gx, gy), r)
            pygame.draw.circle(surf, (255, 255, 255), (gx, gy), r, 2)

            id_txt = self.font_tag.render(str(i), True, (255, 255, 255))
            surf.blit(id_txt, (gx - id_txt.get_width()//2, gy - id_txt.get_height()//2))

            name_txt = self.font_small.render(d["name"], True, COLOR_TEXT_WHITE if is_cur else (203, 213, 225))
            surf.blit(name_txt, (gx - name_txt.get_width()//2, gy + r + 4))

        self.screen.blit(surf, (COL2_X, COL_Y))
        pygame.draw.rect(self.screen, COLOR_CARD_BORDER, (COL2_X, COL_Y, COL2_WIDTH, COL_HEIGHT), 2)

    # =========================================================================
    # RENDER CỘT 3: BỘ SOI MÃ GIẢ & BIẾN TOÁN HỌC LIVE
    # =========================================================================
    def draw_column_3_inspector(self, cur_step):
        surf = pygame.Surface((COL3_WIDTH, COL_HEIGHT))
        surf.fill(COLOR_CARD_BG)

        t_col3 = self.font_main.render("🔍 CỘT 3: BỘ SOI MÃ GIẢ & BIẾN TOÁN HỌC", True, (244, 114, 182))
        surf.blit(t_col3, (16, 12))

        step_txt = f"Bước: {self.current_step_idx + 1}/{len(self.steps)}" if self.steps else "Sẵn sàng"
        surf.blit(self.font_small.render(f"Đang chạy: {self.active_mode} ALGORITHM | {step_txt}", True, COLOR_TEXT_MUTED), (16, 30))

        py = 52

        # 1. BẢNG MÃ GIẢ PSEUDOCODE
        box1 = pygame.Rect(16, py, COL3_WIDTH - 32, 170)
        pygame.draw.rect(surf, (15, 23, 42), box1, border_radius=6)
        pygame.draw.rect(surf, (31, 41, 55), box1, width=1, border_radius=6)

        surf.blit(self.font_tag.render("MÃ GIẢ THUẬT TOÁN ĐANG THỰC THI (PSEUDOCODE):", True, COLOR_TEXT_CYAN), (24, py + 8))

        if cur_step and "pseudocode" in cur_step:
            active_line = cur_step.get("pseudocode_line", 1)
            line_y = py + 26
            for idx, pline in enumerate(cur_step["pseudocode"]):
                is_cur_line = (idx + 1 == active_line)
                if is_cur_line:
                    hl_rect = pygame.Rect(20, line_y - 2, COL3_WIDTH - 40, 18)
                    pygame.draw.rect(surf, (55, 48, 163), hl_rect, border_radius=3)
                    surf.blit(self.font_code.render(f"▶ {pline}", True, COLOR_TEXT_GOLD), (24, line_y))
                else:
                    surf.blit(self.font_code.render(f"  {pline}", True, (203, 213, 225)), (24, line_y))
                line_y += 20

        py += 180

        # 2. HỘP GIẢI THÍCH CHI TIẾT TỪNG BƯỚC
        box2 = pygame.Rect(16, py, COL3_WIDTH - 32, 195)
        pygame.draw.rect(surf, (15, 23, 42), box2, border_radius=6)
        pygame.draw.rect(surf, COLOR_CARD_BORDER_GLOW, box2, width=1, border_radius=6)

        if cur_step:
            u = cur_step.get("current_u", 0)
            v = cur_step.get("current_v", 0)
            u_name = self.nodes_data.get(u, {}).get("name", f"Đỉnh {u}")
            v_name = self.nodes_data.get(v, {}).get("name", f"Đỉnh {v}")
            w = cur_step.get("scanned_weight", 0.0)

            surf.blit(self.font_main.render(f"BƯỚC {self.current_step_idx + 1}/{len(self.steps)}: ĐÁNH GIÁ CẠNH ({u} ↔ {v})", True, COLOR_TEXT_GOLD), (24, py + 8))
            surf.blit(self.font_body.render(f"• Quét lối đi: [{u}] {u_name} ➔ [{v}] {v_name} (w = {w:.1f}m)", True, COLOR_TEXT_WHITE), (24, py + 30))

            surf.blit(self.font_main.render("• Điều kiện toán học:", True, (244, 114, 182)), (24, py + 52))
            surf.blit(self.font_body.render(cur_step.get("reason", ""), True, (226, 232, 240)), (28, py + 70))

            surf.blit(self.font_main.render("• Hành động:", True, COLOR_TEXT_GREEN), (24, py + 95))
            surf.blit(self.font_main.render(cur_step.get("result_text", ""), True, cur_step.get("status_color", COLOR_TEXT_CYAN)), (28, py + 115))

        py += 205

        # 3. BẢNG TRẠNG THÁI BIẾN TOÁN HỌC LIVE
        box3 = pygame.Rect(16, py, COL3_WIDTH - 32, 195)
        pygame.draw.rect(surf, (15, 23, 42), box3, border_radius=6)
        pygame.draw.rect(surf, (31, 41, 55), box3, width=1, border_radius=6)

        surf.blit(self.font_tag.render("BẢNG TRẠNG THÁI BIẾN TOÁN HỌC (LIVE VARIABLES):", True, COLOR_TEXT_CYAN), (24, py + 8))

        if cur_step and "math_state" in cur_step:
            var_y = py + 28
            for k, val in cur_step["math_state"].items():
                surf.blit(self.font_body.render(f"• {k}:", True, (148, 163, 184)), (24, var_y))
                surf.blit(self.font_main.render(str(val), True, COLOR_TEXT_GOLD), (240, var_y))
                var_y += 20

            py += 150

            chosen_list = list(cur_step["after_chosen"])
            chosen_str = ", ".join([f"({cu}↔{cv})" for cu, cv in chosen_list[:8]])
            surf.blit(self.font_small.render(f"Tập cạnh đã chọn ({len(chosen_list)}): {chosen_str}", True, (226, 232, 240)), (20, py))
            if len(chosen_list) > 8:
                chosen_str2 = ", ".join([f"({cu}↔{cv})" for cu, cv in chosen_list[8:16]])
                surf.blit(self.font_small.render(f"                         {chosen_str2}", True, (226, 232, 240)), (20, py + 15))

        # 4. NÚT ĐIỀU KHIỂN BƯỚC
        mouse_pos = pygame.mouse.get_pos()
        btn_y = COL_HEIGHT - 44

        is_h_p = self.btn_prev_rect.collidepoint(mouse_pos)
        pygame.draw.rect(surf, (51, 65, 85) if is_h_p else (30, 41, 59), (16, btn_y, 90, 32), border_radius=5)
        pygame.draw.rect(surf, COLOR_TEXT_CYAN, (16, btn_y, 90, 32), width=1, border_radius=5)
        surf.blit(self.font_body.render("◀ LÙI [B]", True, (255, 255, 255)), (28, btn_y + 8))

        is_h_n = self.btn_next_rect.collidepoint(mouse_pos)
        pygame.draw.rect(surf, (14, 116, 144) if is_h_n else (8, 145, 178), (114, btn_y, 110, 32), border_radius=5)
        pygame.draw.rect(surf, (255, 255, 255) if is_h_n else COLOR_TEXT_CYAN, (114, btn_y, 110, 32), width=1, border_radius=5)
        surf.blit(self.font_main.render("TIẾP [S] ▶", True, (255, 255, 255)), (128, btn_y + 7))

        auto_bg = (5, 150, 105) if self.is_auto_playing else (51, 65, 85)
        pygame.draw.rect(surf, auto_bg, (232, btn_y, 150, 32), border_radius=5)
        pygame.draw.rect(surf, COLOR_TEXT_GREEN if self.is_auto_playing else (148, 163, 184), (232, btn_y, 150, 32), width=1, border_radius=5)
        auto_lbl = "⏸️ DỪNG [SPACE]" if self.is_auto_playing else "▶️ PHÁT TỰ ĐỘNG"
        surf.blit(self.font_body.render(auto_lbl, True, (255, 255, 255)), (244, btn_y + 8))

        pygame.draw.rect(surf, (51, 65, 85), (390, btn_y, 80, 32), border_radius=5)
        pygame.draw.rect(surf, (148, 163, 184), (390, btn_y, 80, 32), width=1, border_radius=5)
        surf.blit(self.font_body.render("🔄 ĐẶT LẠI", True, (255, 255, 255)), (398, btn_y + 8))

        is_h_fs = self.btn_fullscreen_rect.collidepoint(mouse_pos)
        pygame.draw.rect(surf, (14, 165, 233) if is_h_fs else (3, 105, 161), (478, btn_y, (COL3_WIDTH - 32) - 462, 32), border_radius=5)
        surf.blit(self.font_tag.render("⛶ F11", True, (255, 255, 255)), (490, btn_y + 9))

        self.screen.blit(surf, (COL3_X, COL_Y))
        pygame.draw.rect(self.screen, COLOR_CARD_BORDER, (COL3_X, COL_Y, COL3_WIDTH, COL_HEIGHT), 2)

    def draw_top_bar(self):
        """Vẽ thanh Menu 7 Thuật Toán trên cùng."""
        mouse_pos = pygame.mouse.get_pos()
        for rect, label, mode_id, color in self.top_buttons:
            is_act = (self.active_mode == mode_id)
            is_hov = rect.collidepoint(mouse_pos)

            bg_c = (color[0]//2, color[1]//2, color[2]//2) if is_act else ((51, 65, 85) if is_hov else (17, 24, 39))
            border_c = color if is_act else ((148, 163, 184) if is_hov else (31, 41, 55))

            pygame.draw.rect(self.screen, bg_c, rect, border_radius=6)
            pygame.draw.rect(self.screen, border_c, rect, width=2 if is_act else 1, border_radius=6)

            txt_c = (255, 255, 255) if is_act else (226, 232, 240)
            btn_t = self.font_main.render(label, True, txt_c)
            self.screen.blit(btn_t, (rect.centerx - btn_t.get_width()//2, rect.centery - btn_t.get_height()//2))

    def switch_mode(self, mode_id):
        """Chuyển đổi tức thì sang thuật toán mới."""
        self.active_mode = mode_id
        self.is_auto_playing = False
        self.auto_timer = 0
        
        if mode_id == "MST":
            self.steps = self.algo_engine.build_kruskal_steps()
        elif mode_id == "DIJKSTRA":
            self.steps = self.algo_engine.build_dijkstra_steps(start=22, target=0)
        elif mode_id == "BFS":
            self.steps = self.algo_engine.build_bfs_steps(start=0)
        elif mode_id == "DFS":
            self.steps = self.algo_engine.build_dfs_steps(start=0)
        elif mode_id == "EULER":
            self.steps = self.algo_engine.build_euler_steps()
        elif mode_id == "BIPARTITE":
            self.steps = self.algo_engine.build_bipartite_steps()
        else:
            self.steps = self.algo_engine.build_maxflow_steps()

        self.current_step_idx = 0
        self.anim_t = 0.0

    def step_next(self):
        """Tiến 1 bước thuật toán."""
        if self.current_step_idx < len(self.steps) - 1:
            self.current_step_idx += 1
            self.anim_t = 0.0

    def step_prev(self):
        """Lùi 1 bước thuật toán."""
        if self.current_step_idx > 0:
            self.current_step_idx -= 1
            self.anim_t = 0.0

    def toggle_fullscreen(self):
        """Bật / Tắt chế độ toàn màn hình."""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)

    def run(self):
        """Vòng lặp chính xử lý sự kiện và vẽ khung hình."""
        running = True
        while running:
            self.clock.tick(FPS)
            mx, my = pygame.mouse.get_pos()
            self.lidar_angle = (self.lidar_angle + 5.0) % 360.0

            if self.anim_t < 1.0:
                self.anim_t = min(1.0, self.anim_t + self.anim_speed)

            if self.is_auto_playing:
                self.auto_timer += 1
                if self.auto_timer >= 55:
                    self.auto_timer = 0
                    if self.current_step_idx < len(self.steps) - 1:
                        self.current_step_idx += 1
                        self.anim_t = 0.0
                    else:
                        self.is_auto_playing = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEWHEEL:
                    if mx <= COL1_X + COL1_WIDTH:
                        self.cam_zoom = max(0.4, min(3.0, self.cam_zoom + event.y * 0.08))

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Kiểm tra click Top Buttons
                        for rect, _, mode_id, _ in self.top_buttons:
                            if rect.collidepoint(mx, my):
                                self.switch_mode(mode_id)
                                break

                        # Kiểm tra nút Zoom / 3D ở Cột 1
                        if self.btn_zoom_out_rect.collidepoint(mx, my):
                            self.cam_zoom = max(0.4, self.cam_zoom - 0.15)
                        elif self.btn_zoom_in_rect.collidepoint(mx, my):
                            self.cam_zoom = min(3.0, self.cam_zoom + 0.15)
                        elif self.btn_zoom_badge_rect.collidepoint(mx, my):
                            self.cam_zoom = 0.95
                            self.cam_pan_x = 0
                            self.cam_pan_y = 0
                        elif self.btn_view_3d_rect.collidepoint(mx, my):
                            self.is_3d_mode = not self.is_3d_mode

                        # Kiểm tra nút điều khiển ở Cột 3
                        elif self.btn_prev_rect.collidepoint(mx, my):
                            self.step_prev()
                        elif self.btn_next_rect.collidepoint(mx, my):
                            self.step_next()
                        elif self.btn_auto_rect.collidepoint(mx, my):
                            self.is_auto_playing = not self.is_auto_playing
                        elif self.btn_reset_rect.collidepoint(mx, my):
                            self.current_step_idx = 0
                            self.is_auto_playing = False
                            self.anim_t = 0.0
                        elif self.btn_fullscreen_rect.collidepoint(mx, my):
                            self.toggle_fullscreen()

                        elif mx < COL1_X + COL1_WIDTH and my > COL_Y:
                            self.is_dragging_3d = True
                            self.last_mouse_pos = (mx, my)

                    elif event.button == 3:
                        if mx < COL1_X + COL1_WIDTH and my > COL_Y:
                            self.is_panning_3d = True
                            self.last_mouse_pos = (mx, my)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.is_dragging_3d = False
                    elif event.button == 3:
                        self.is_panning_3d = False

                elif event.type == pygame.MOUSEMOTION:
                    if self.is_dragging_3d and self.is_3d_mode:
                        dx = mx - self.last_mouse_pos[0]
                        dy = my - self.last_mouse_pos[1]
                        self.cam_yaw = (self.cam_yaw + dx * 0.5) % 360.0
                        self.cam_pitch = max(10.0, min(85.0, self.cam_pitch - dy * 0.5))
                        self.last_mouse_pos = (mx, my)
                    elif self.is_panning_3d:
                        dx = mx - self.last_mouse_pos[0]
                        dy = my - self.last_mouse_pos[1]
                        self.cam_pan_x += dx
                        self.cam_pan_y += dy
                        self.last_mouse_pos = (mx, my)

                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RIGHT, pygame.K_s]:
                        self.step_next()
                    elif event.key in [pygame.K_LEFT, pygame.K_b]:
                        self.step_prev()
                    elif event.key == pygame.K_SPACE:
                        self.is_auto_playing = not self.is_auto_playing
                    elif event.key == pygame.K_r:
                        self.current_step_idx = 0
                        self.is_auto_playing = False
                        self.anim_t = 0.0
                    elif event.key in [pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS]:
                        self.cam_zoom = min(3.0, self.cam_zoom + 0.15)
                    elif event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]:
                        self.cam_zoom = max(0.4, self.cam_zoom - 0.15)
                    elif event.key in [pygame.K_0, pygame.K_KP0]:
                        self.cam_zoom = 0.95
                        self.cam_pan_x = 0
                        self.cam_pan_y = 0
                    elif event.key == pygame.K_v:
                        self.is_3d_mode = not self.is_3d_mode
                    elif event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                    elif event.key in [pygame.K_1, pygame.K_KP1]:
                        self.switch_mode("MST")
                    elif event.key in [pygame.K_2, pygame.K_KP2]:
                        self.switch_mode("DIJKSTRA")
                    elif event.key in [pygame.K_3, pygame.K_KP3]:
                        self.switch_mode("BFS")
                    elif event.key in [pygame.K_4, pygame.K_KP4]:
                        self.switch_mode("DFS")
                    elif event.key in [pygame.K_5, pygame.K_KP5]:
                        self.switch_mode("EULER")
                    elif event.key in [pygame.K_6, pygame.K_KP6]:
                        self.switch_mode("BIPARTITE")
                    elif event.key in [pygame.K_7, pygame.K_KP7]:
                        self.switch_mode("MAXFLOW")

            # Vẽ nền và 3 cột giao diện
            self.screen.fill(COLOR_APP_BG)
            self.draw_top_bar()

            cur_step = self.steps[self.current_step_idx] if self.steps else None
            self.draw_column_1_floorplan(cur_step)
            self.draw_column_2_graph(cur_step)
            self.draw_column_3_inspector(cur_step)

            pygame.display.flip()

        pygame.quit()

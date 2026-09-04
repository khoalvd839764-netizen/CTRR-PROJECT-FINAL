"""
Module: ung_dung_thuc_te/gui_dashboard.py
Purpose: Cross-Platform Multi-View Dashboard for the Smart Vacuum Robot Simulation.
Engineered for Windows, macOS, and Linux:
  - 100% Crisp Typography (Universal cross-platform fonts, zero tofu/broken glyphs).
  - Hardware-accelerated Linear Scaling (os.environ["SDL_RENDER_SCALE_QUALITY"] = "linear").
  - Seamless Fullscreen F11 & Window Resizing without resolution stretching or blur.
  - Pixel-perfect Mouse Hit Detection in any window/display configuration.
"""

import sys
import math
import os

# 1. Hardware Linear Texture Filtering: Eliminates pixelation and jaggedness when scaling
os.environ["SDL_RENDER_SCALE_QUALITY"] = "linear"

# 2. Windows Per-Monitor DPI Awareness: Prevents OS DWM coordinate distortion
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

import pygame

from ung_dung_thuc_te.data_model import (
    HOUSE_NODES_DATA, HOUSE_BASE_COORDS, HOUSE_EDGES,
    EDGE_CURVATURE, ROOMS_LAYOUT_3D, FURNITURE_3D_BLOCKS
)
from ung_dung_thuc_te.algorithms import RobotAlgorithms

# =============================================================================
# CANVAS AND UI LAYOUT CONFIGURATION
# =============================================================================
CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080
FPS = 60

# 3-Column Layout
COL_Y = 52
COL_HEIGHT = 1014

COL1_X = 14
COL1_WIDTH = 570

COL2_X = 596
COL2_WIDTH = 730

COL3_X = 1338
COL3_WIDTH = 568

# Dark Cyber UI Palette
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


def get_ui_font(size, bold=False):
    """
    Loads cross-platform typography font supporting clean rendering across Windows, macOS, Linux.
    Tries modern system fonts in order of platform priority, with universal fallback.
    """
    candidates = [
        "segoeui",          # Windows modern default
        "sfpro",            # macOS modern default
        "helveticaneue",    # macOS standard
        "helvetica",        # macOS standard
        "arial",            # Universal cross-platform
        "dejavusans",       # Linux standard
        "liberationsans",   # Linux standard
        "notosans",         # Linux / Android standard
        "tahoma",           # Windows fallback
        "freesans"          # Linux fallback
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
    Coordinator class for the Smart Vacuum Robot Simulation Dashboard.
    Uses Virtual Canvas 1920x1080 with Hardware Linear Scaling for pristine visual quality.
    """
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SMART VACUUM ROBOT - REAL-WORLD GRAPH THEORY DASHBOARD")

        self.is_fullscreen = False
        self.screen = pygame.display.set_mode(
            (CANVAS_WIDTH, CANVAS_HEIGHT), pygame.RESIZABLE | pygame.SCALED
        )
        self.clock = pygame.time.Clock()

        # Upgraded Typography Hierarchy (Crisp & Legible at 1080p, 1440p, 4K, and Scaled Displays)
        self.font_title = get_ui_font(16, bold=True)  # Column headers
        self.font_main = get_ui_font(14, bold=True)   # Buttons, key variables
        self.font_body = get_ui_font(12, bold=False)  # Descriptions & status
        self.font_code = get_ui_font(12, bold=True)   # Pseudocode monospace
        self.font_tag = get_ui_font(11, bold=True)    # Badges & node IDs
        self.font_small = get_ui_font(11, bold=False) # Hints & legends

        # Apartment Data Model
        self.nodes_data = dict(HOUSE_NODES_DATA)
        self.base_coords = dict(HOUSE_BASE_COORDS)
        self.edges = list(HOUSE_EDGES)
        self.n = len(self.nodes_data)
        self.curvatures = {tuple(sorted(k)): v for k, v in EDGE_CURVATURE.items()}

        # Core Algorithm Engine
        self.algo_engine = RobotAlgorithms(self.n, self.edges, self.nodes_data)

        # Active Mode & Step Tracker
        self.active_mode = "MST"
        self.steps = []
        self.current_step_idx = 0
        self.is_auto_playing = False
        self.auto_timer = 0

        # Camera & 3D Isometric Projection
        self.is_3d_mode = True
        self.cam_zoom = 1.15
        self.cam_yaw = 38.0
        self.cam_pitch = 38.0
        self.cam_pan_x = 0
        self.cam_pan_y = 0

        # Interactive state
        self.is_dragging_3d = False
        self.is_panning_3d = False
        self.last_mouse_pos = (0, 0)
        self.lidar_angle = 0.0

        # Animation interpolation (0.0 -> 1.0)
        self.anim_t = 1.0
        self.anim_speed = 0.035

        # Top Bar Algorithm Menu Buttons
        self.top_buttons = []
        self.init_top_buttons()

        # Column 1 Zoom / View Controls
        top_btn_y = COL_Y + 8
        self.btn_view_3d_rect = pygame.Rect(COL1_X + COL1_WIDTH - 76, top_btn_y, 66, 26)
        self.btn_zoom_in_rect = pygame.Rect(COL1_X + COL1_WIDTH - 106, top_btn_y, 26, 26)
        self.btn_zoom_badge_rect = pygame.Rect(COL1_X + COL1_WIDTH - 162, top_btn_y, 52, 26)
        self.btn_zoom_out_rect = pygame.Rect(COL1_X + COL1_WIDTH - 192, top_btn_y, 26, 26)

        # Column 3 Step Controls
        ctrl_btn_y = COL_Y + COL_HEIGHT - 46
        self.btn_prev_rect = pygame.Rect(COL3_X + 12, ctrl_btn_y, 90, 36)
        self.btn_next_rect = pygame.Rect(COL3_X + 108, ctrl_btn_y, 110, 36)
        self.btn_auto_rect = pygame.Rect(COL3_X + 224, ctrl_btn_y, 140, 36)
        self.btn_reset_rect = pygame.Rect(COL3_X + 370, ctrl_btn_y, 80, 36)
        self.btn_fullscreen_rect = pygame.Rect(COL3_X + 456, ctrl_btn_y, COL3_WIDTH - 12 - 456, 36)

        # Start default mode
        self.switch_mode("MST")

    def init_top_buttons(self):
        """Initializes 7 quick-access algorithm buttons on the Top Bar."""
        modes = [
            ("[1] Kruskal MST", "MST", (52, 211, 153)),
            ("[2] Dijkstra Return", "DIJKSTRA", (56, 189, 248)),
            ("[3] BFS SLAM Map", "BFS", (14, 165, 233)),
            ("[4] DFS Wall-Follow", "DFS", (168, 85, 247)),
            ("[5] Euler Full House", "EULER", (250, 204, 21)),
            ("[6] Bipartite Zones", "BIPARTITE", (236, 72, 153)),
            ("[7] Max-Flow Dust", "MAXFLOW", (248, 113, 113))
        ]
        btn_gap = 8
        btn_w = (CANVAS_WIDTH - 28 - 6 * btn_gap) // 7
        btn_h = 38
        buttons = []
        for i, (label, mode_id, color) in enumerate(modes):
            bx = 14 + i * (btn_w + btn_gap)
            rect = pygame.Rect(bx, 6, btn_w, btn_h)
            buttons.append((rect, label, mode_id, color))
        self.top_buttons = buttons

    def is_top_button_hit(self, rect, pos):
        """
        Precise hit detection for top buttons.
        Expands vertically by 8px (y from 2 to 48) for easy clicking,
        with ZERO horizontal overlap so each button is exclusively triggered.
        """
        if pos is None:
            return False
        return rect.inflate(0, 8).collidepoint(pos)

    def get_column1_pos(self, node_id, z=0):
        """Projects (x, y, z) apartment coordinates to Column 1 screen space."""
        base_x, base_y = self.base_coords[node_id]
        cx = COL1_WIDTH // 2 + self.cam_pan_x
        cy = COL_HEIGHT // 2 + self.cam_pan_y

        if not self.is_3d_mode:
            center_x, center_y = 290, 410
            sx = cx + (base_x + 15 - center_x) * self.cam_zoom
            sy = cy + (base_y + 15 - center_y) * self.cam_zoom
            return (int(sx), int(sy))

        rel_x = (base_x + 15) - 290
        rel_y = (base_y + 15) - 410
        rel_z = z

        rad_yaw = math.radians(self.cam_yaw)
        rad_pitch = math.radians(self.cam_pitch)

        rx = rel_x * math.cos(rad_yaw) - rel_y * math.sin(rad_yaw)
        ry = rel_x * math.sin(rad_yaw) + rel_y * math.cos(rad_yaw)
        rz = rel_z

        iso_x = rx
        iso_y = ry * math.sin(rad_pitch) - rz * math.cos(rad_pitch)

        sx = cx + iso_x * self.cam_zoom
        sy = cy + iso_y * self.cam_zoom
        return (int(sx), int(sy))

    def project_3d_point(self, x, y, z):
        """Projects generic 3D points to Column 1 space."""
        cx = COL1_WIDTH // 2 + self.cam_pan_x
        cy = COL_HEIGHT // 2 + self.cam_pan_y

        if not self.is_3d_mode:
            center_x, center_y = 290, 410
            sx = cx + (x - center_x) * self.cam_zoom
            sy = cy + (y - center_y) * self.cam_zoom
            return (int(sx), int(sy))

        rel_x = x - 290
        rel_y = y - 410
        rel_z = z

        rad_yaw = math.radians(self.cam_yaw)
        rad_pitch = math.radians(self.cam_pitch)

        rx = rel_x * math.cos(rad_yaw) - rel_y * math.sin(rad_yaw)
        ry = rel_x * math.sin(rad_yaw) + rel_y * math.cos(rad_yaw)
        rz = rel_z

        iso_x = rx
        iso_y = ry * math.sin(rad_pitch) - rz * math.cos(rad_pitch)

        sx = cx + iso_x * self.cam_zoom
        sy = cy + iso_y * self.cam_zoom
        return (int(sx), int(sy))

    def get_column2_graph_pos(self, node_id):
        """Computes balanced mathematical graph layout in Column 2."""
        bx, by = self.base_coords[node_id]
        scale_x = (COL2_WIDTH - 120) / 480.0
        scale_y = (COL_HEIGHT - 160) / 680.0
        gx = 60 + int((bx - 40) * scale_x)
        gy = 90 + int((by - 80) * scale_y)
        return (gx, gy)

    def get_arc_points(self, p1, p2, edge_tuple, num_segments=16):
        """Generates quadratic Bézier curve points to avoid overlapping edges."""
        curvature = self.curvatures.get(edge_tuple, 0)
        x1, y1 = p1
        x2, y2 = p2

        mx = (x1 + x2) / 2.0
        my = (y1 + y2) / 2.0

        if curvature == 0:
            return [p1, p2], (int(mx), int(my))

        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        if length == 0:
            return [p1, p2], (int(mx), int(my))

        nx = -dy / length
        ny = dx / length

        ctrl_x = mx + nx * curvature * 1.5
        ctrl_y = my + ny * curvature * 1.5

        pts = []
        for i in range(num_segments + 1):
            t = i / float(num_segments)
            inv = 1.0 - t
            bx = inv * inv * x1 + 2 * inv * t * ctrl_x + t * t * x2
            by = inv * inv * y1 + 2 * inv * t * ctrl_y + t * t * y2
            pts.append((int(bx), int(by)))

        mid_x = 0.25 * x1 + 0.5 * ctrl_x + 0.25 * x2
        mid_y = 0.25 * y1 + 0.5 * ctrl_y + 0.25 * y2
        return pts, (int(mid_x), int(mid_y))

    def get_interpolated_arc_pos(self, p1, p2, edge_tuple, t):
        """Interpolates position along the Bézier curve for smooth pulse animation."""
        curvature = self.curvatures.get(edge_tuple, 0)
        x1, y1 = p1
        x2, y2 = p2
        if curvature == 0:
            return (int(x1 + (x2 - x1) * t), int(y1 + (y2 - y1) * t))

        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        nx = -dy / length
        ny = dx / length

        mx = (x1 + x2) / 2.0
        my = (y1 + y2) / 2.0
        ctrl_x = mx + nx * curvature * 1.5
        ctrl_y = my + ny * curvature * 1.5

        inv = 1.0 - t
        bx = inv * inv * x1 + 2 * inv * t * ctrl_x + t * t * x2
        by = inv * inv * y1 + 2 * inv * t * ctrl_y + t * t * y2
        return (int(bx), int(by))

    # =========================================================================
    # RENDER COLUMN 1: 3D ISOMETRIC APARTMENT FLOORPLAN
    # =========================================================================
    # =========================================================================
    # COLUMN 1: 3D FLOORPLAN & ROBOT SIMULATION (GIAO DIỆN MÔ PHỎNG VẬT LÝ)
    # =========================================================================
    # Đây là giao diện chính hiển thị căn hộ dưới dạng 3D Isometric.
    # Nhiệm vụ:
    # 1. Vẽ sơ đồ phòng (Phòng khách, bếp, ngủ...)
    # 2. Vẽ nội thất (Sofa, giường, tủ...)
    # 3. Vẽ vị trí thực tế của Robot và các hiệu ứng Laser Lidar
    def draw_column_1_floorplan(self, cur_step):
        surf = pygame.Surface((COL1_WIDTH, COL_HEIGHT))
        surf.fill(COLOR_CARD_BG)

        mode_tag = "3D VIEW" if self.is_3d_mode else "2D TOP"
        t_col1 = self.font_title.render(f"COL 1: FLOORPLAN ({mode_tag})", True, COLOR_TEXT_CYAN)
        surf.blit(t_col1, (16, 10))

        zoom_pct = int(round(self.cam_zoom * 100))
        surf.blit(self.font_small.render(f"Scroll / Keys [+/-] Zoom: {zoom_pct}% | Left-Drag: Rotate | Right-Drag: Pan", True, COLOR_TEXT_MUTED), (16, 30))

        # Zoom Out [-]
        z_out_rx = COL1_WIDTH - 192
        pygame.draw.rect(surf, (30, 41, 59), (z_out_rx, 8, 26, 26), border_radius=4)
        pygame.draw.rect(surf, (71, 85, 105), (z_out_rx, 8, 26, 26), width=1, border_radius=4)
        z_out_t = self.font_main.render("-", True, COLOR_TEXT_WHITE)
        surf.blit(z_out_t, (z_out_rx + 13 - z_out_t.get_width()//2, 8 + 13 - z_out_t.get_height()//2 - 1))

        # Zoom % Badge
        z_badge_rx = COL1_WIDTH - 162
        pygame.draw.rect(surf, (15, 23, 42), (z_badge_rx, 8, 52, 26), border_radius=4)
        z_border_c = COLOR_TEXT_CYAN if zoom_pct != 115 else (71, 85, 105)
        pygame.draw.rect(surf, z_border_c, (z_badge_rx, 8, 52, 26), width=1, border_radius=4)
        z_pct_t = self.font_tag.render(f"{zoom_pct}%", True, COLOR_TEXT_CYAN if zoom_pct != 115 else COLOR_TEXT_MUTED)
        surf.blit(z_pct_t, (z_badge_rx + 26 - z_pct_t.get_width()//2, 8 + 13 - z_pct_t.get_height()//2))

        # Zoom In [+]
        z_in_rx = COL1_WIDTH - 106
        pygame.draw.rect(surf, (30, 41, 59), (z_in_rx, 8, 26, 26), border_radius=4)
        pygame.draw.rect(surf, (71, 85, 105), (z_in_rx, 8, 26, 26), width=1, border_radius=4)
        z_in_t = self.font_main.render("+", True, COLOR_TEXT_WHITE)
        surf.blit(z_in_t, (z_in_rx + 13 - z_in_t.get_width()//2, 8 + 13 - z_in_t.get_height()//2 - 1))

        # 3D / 2D Toggle Button
        v3d_rx = COL1_WIDTH - 76
        v3d_bg = (14, 165, 233) if self.is_3d_mode else (30, 41, 59)
        pygame.draw.rect(surf, v3d_bg, (v3d_rx, 8, 66, 26), border_radius=4)
        pygame.draw.rect(surf, (255, 255, 255) if self.is_3d_mode else (71, 85, 105), (v3d_rx, 8, 66, 26), width=1, border_radius=4)
        v3d_t = self.font_tag.render("3D VIEW" if self.is_3d_mode else "2D TOP", True, (255, 255, 255))
        surf.blit(v3d_t, (v3d_rx + 33 - v3d_t.get_width()//2, 8 + 13 - v3d_t.get_height()//2))

        # 1. Draw 5 Room Floor Boundaries
        for rx, ry, rw, rd, label, fl_col, gr_col in ROOMS_LAYOUT_3D:
            p_tl = self.project_3d_point(rx, ry, 0)
            p_tr = self.project_3d_point(rx + rw, ry, 0)
            p_br = self.project_3d_point(rx + rw, ry + rd, 0)
            p_bl = self.project_3d_point(rx, ry + rd, 0)

            poly_surf = pygame.Surface((COL1_WIDTH, COL_HEIGHT), pygame.SRCALPHA)
            pygame.draw.polygon(poly_surf, fl_col, [p_tl, p_tr, p_br, p_bl])
            pygame.draw.polygon(poly_surf, (gr_col[0], gr_col[1], gr_col[2], 180), [p_tl, p_tr, p_br, p_bl], 1)
            surf.blit(poly_surf, (0, 0))

            p_mid = self.project_3d_point(rx + rw // 2, ry + rd // 2, 0)
            tag_s = self.font_tag.render(label, True, (gr_col[0] + 50, gr_col[1] + 50, min(255, gr_col[2] + 80)))
            surf.blit(tag_s, (p_mid[0] - tag_s.get_width() // 2, p_mid[1] - tag_s.get_height() // 2))

        # 2. Draw 3D Architectural Furniture Blocks
        for fb in FURNITURE_3D_BLOCKS:
            fx, fy, fz = fb["x"], fb["y"], fb["z"]
            fw, fd, fh = fb["w"], fb["d"], fb["h"]

            b_tl = self.project_3d_point(fx, fy, fz)
            b_tr = self.project_3d_point(fx + fw, fy, fz)
            b_br = self.project_3d_point(fx + fw, fy + fd, fz)
            b_bl = self.project_3d_point(fx, fy + fd, fz)

            t_tl = self.project_3d_point(fx, fy, fz + fh)
            t_tr = self.project_3d_point(fx + fw, fy, fz + fh)
            t_br = self.project_3d_point(fx + fw, fy + fd, fz + fh)
            t_bl = self.project_3d_point(fx, fy + fd, fz + fh)

            if self.is_3d_mode:
                pygame.draw.polygon(surf, fb["sx"], [b_bl, b_br, t_br, t_bl])
                pygame.draw.polygon(surf, fb["sy"], [b_br, b_tr, t_tr, t_br])

            pygame.draw.polygon(surf, fb["top"], [t_tl, t_tr, t_br, t_bl])
            pygame.draw.polygon(surf, (255, 255, 255), [t_tl, t_tr, t_br, t_bl], 1)

        # 3. Draw 36 Clean Paths
        scanned_edge = cur_step.get("scanned_edge", (-1, -1)) if cur_step else (-1, -1)
        chosen_edges = cur_step.get("after_chosen", set()) if cur_step else set()
        rejected_edges = cur_step.get("after_rejected", set()) if cur_step else set()
        shortest_path_edges = cur_step.get("shortest_path_edges", set()) if cur_step else set()
        is_path_found = cur_step.get("is_path_found", False) if cur_step else False

        seen_edges = set()
        t_ticks = pygame.time.get_ticks()
        pulse = (math.sin(t_ticks * 0.008) + 1.0) / 2.0
        glow_w = int(3 + pulse * 4)

        # High-visibility pulsing oscillation for Dijkstra shortest path (~1.5 Hz)
        blink = (math.sin(t_ticks * 0.012) + 1.0) / 2.0  # 0.0 to 1.0
        sp_pulse_w = int(5 + blink * 5)
        neon_g = int(180 + blink * 75)
        sp_neon_col = (16, neon_g, 220) if blink > 0.4 else (52, 255, 160)

        for u, v, l_m, cap in self.edges:
            edge_tuple = tuple(sorted((u, v)))
            if edge_tuple in seen_edges:
                continue
            seen_edges.add(edge_tuple)

            p1 = self.get_column1_pos(u, z=0)
            p2 = self.get_column1_pos(v, z=0)

            is_sp = (is_path_found and self.active_mode == "DIJKSTRA" and edge_tuple in shortest_path_edges)
            is_scan = (edge_tuple == scanned_edge)
            is_pick = (edge_tuple in chosen_edges)
            is_rej = (edge_tuple in rejected_edges)

            if is_sp:
                # Flashing/pulsing multi-layer neon laser line
                aura_c = (5, 150, 105) if blink < 0.5 else (6, 182, 212)
                pygame.draw.line(surf, aura_c, p1, p2, sp_pulse_w + 6)
                pygame.draw.line(surf, sp_neon_col, p1, p2, sp_pulse_w)
                pygame.draw.line(surf, (255, 255, 255), p1, p2, max(2, sp_pulse_w - 4))
            elif is_scan:
                pygame.draw.line(surf, COLOR_TEXT_GOLD, p1, p2, glow_w)
            elif is_pick:
                col = COLOR_TEXT_GREEN if self.active_mode != "DIJKSTRA" else COLOR_TEXT_CYAN
                pygame.draw.line(surf, col, p1, p2, 4)
            elif is_rej:
                pygame.draw.line(surf, (239, 68, 68, 120), p1, p2, 1)
            else:
                pygame.draw.line(surf, (51, 65, 85, 140), p1, p2, 1)

        # 4. Draw 25 Cleaning Waypoints
        sp_nodes = cur_step.get("shortest_path_nodes", []) if (cur_step and is_path_found and self.active_mode == "DIJKSTRA") else []
        for i, d in self.nodes_data.items():
            p_node = self.get_column1_pos(i, z=8)
            p_ground = self.get_column1_pos(i, z=0)

            ntype = d["room"]
            is_dock = (ntype == "DOCK" and i == 0)
            is_cur = (cur_step and (i == cur_step.get("current_u") or i == cur_step.get("current_v")))
            is_sp_node = (i in sp_nodes)

            color = (236, 72, 153) if is_dock else ((59, 130, 246) if d["zone"] == "DRY" else (245, 158, 11))
            
            if self.is_3d_mode:
                pygame.draw.line(surf, (148, 163, 184, 160), p_ground, p_node, 1)

            # Pulsing beacon ring for nodes along the shortest path
            if is_sp_node:
                beacon_r = int(14 + blink * 7)
                pygame.draw.circle(surf, (52, 255, 160), p_node, beacon_r, 2)
                pygame.draw.circle(surf, (16, 185, 129, 80), p_node, beacon_r + 4, 1)

            if is_cur:
                pygame.draw.circle(surf, COLOR_TEXT_GOLD, p_node, 18, 2)

            r = 11 if is_dock else 9
            pygame.draw.circle(surf, color, p_node, r)
            pygame.draw.circle(surf, (255, 255, 255), p_node, r, 1)

            id_txt = self.font_tag.render(str(i), True, (255, 255, 255))
            surf.blit(id_txt, (p_node[0] - id_txt.get_width() // 2, p_node[1] - id_txt.get_height() // 2))

        # 5. Draw Glowing 3D Roomba Robot with Lidar Scanner (Zero-Teleportation Physical Logic)
        if cur_step:
            mode = self.active_mode
            if mode == "DIJKSTRA":
                phase = cur_step.get("phase", "")
                if phase in ("SCAN", "LOCKED"):
                    # Robot is stationary at starting corner [22] running Dijkstra in memory
                    bot_u, bot_v = 22, 22
                elif phase == "DOCKED":
                    # Robot is safely docked at Charging Base [0]
                    bot_u, bot_v = 0, 0
                else:  # "TRAVELING" -> Physically rolls along the shortest path
                    bot_u = cur_step.get("current_u", 0)
                    bot_v = cur_step.get("current_v", 0)

            elif mode in ("MST", "MAXFLOW"):
                # Kruskal (infrastructure cabling) and Max Flow (pipe evacuation):
                # Robot is resting at Dock Base [0], monitoring network flow
                bot_u, bot_v = 0, 0

            else:  # BFS, DFS, EULER, BIPARTITE -> 100% continuous physical travel
                bot_u = cur_step.get("current_u", 0)
                bot_v = cur_step.get("current_v", 0)

            u_p = self.get_column1_pos(bot_u, z=0)
            v_p = self.get_column1_pos(bot_v, z=0)

            rx = int(u_p[0] + (v_p[0] - u_p[0]) * self.anim_t)
            ry = int(u_p[1] + (v_p[1] - u_p[1]) * self.anim_t)

            scale = max(0.5, min(2.0, self.cam_zoom))
            bot_base = (rx, ry)
            bot_top = (rx, ry - int(10 * scale)) if self.is_3d_mode else (rx, ry)
            bot_lidar = (rx, ry - int(14 * scale)) if self.is_3d_mode else (rx, ry)

            pygame.draw.ellipse(surf, (15, 23, 42), (bot_base[0] - int(16 * scale), bot_base[1] - int(8 * scale), int(32 * scale), int(16 * scale)))
            pygame.draw.line(surf, (148, 163, 184), (bot_base[0] - int(14 * scale), bot_base[1]), (bot_top[0] - int(14 * scale), bot_top[1]), max(1, int(2 * scale)))
            pygame.draw.line(surf, (148, 163, 184), (bot_base[0] + int(14 * scale), bot_base[1]), (bot_top[0] + int(14 * scale), bot_top[1]), max(1, int(2 * scale)))
            pygame.draw.ellipse(surf, (241, 245, 249), (bot_top[0] - int(14 * scale), bot_top[1] - int(7 * scale), int(28 * scale), int(14 * scale)))
            pygame.draw.ellipse(surf, (56, 189, 248), (bot_top[0] - int(10 * scale), bot_top[1] - int(5 * scale), int(20 * scale), int(10 * scale)), 1)

            # =================================================================
            # 6. HIGH-TECH SCI-FI LIDAR SCANNER & VOLUMETRIC LASER BEAM
            # =================================================================
            laser_overlay = pygame.Surface((COL1_WIDTH, COL_HEIGHT), pygame.SRCALPHA)
            t_ticks = pygame.time.get_ticks()
            pulse_wave = (math.sin(t_ticks * 0.018) + 1.0) / 2.0

            # 6.1 Cyber Radar Range Rings around Roomba Base
            for r_ring in [int(18 * scale), int(34 * scale)]:
                pygame.draw.ellipse(laser_overlay, (56, 189, 248, 38), 
                                    (rx - r_ring, ry - r_ring // 2, r_ring * 2, r_ring), 1)

            # 6.2 Sweeping 360° Phosphor Radar Fan
            sweep_rad = math.radians(self.lidar_angle)
            fan_len = int(32 * scale)
            for trail_i in range(12):
                trail_rad = sweep_rad - math.radians(trail_i * 3.6)
                alpha_trail = max(0, 160 - trail_i * 13)
                tx = rx + int(fan_len * math.cos(trail_rad))
                ty = ry + int((fan_len * 0.5) * math.sin(trail_rad))
                pygame.draw.line(laser_overlay, (56, 189, 248, alpha_trail), bot_lidar, (tx, ty), max(1, int(1.5 * scale)))

            # 6.3 Pulsing Ruby / Cyan Laser Diode Lens on Lidar Dome
            core_pulse = (math.sin(t_ticks * 0.015) + 1.0) / 2.0
            core_r = max(2, int((3.5 + core_pulse * 1.5) * scale))
            pygame.draw.circle(laser_overlay, (239, 68, 68, 160), bot_lidar, core_r + 3)
            pygame.draw.circle(surf, (255, 90, 90), bot_lidar, core_r)
            pygame.draw.circle(surf, (255, 255, 255), bot_lidar, max(1, core_r - 2))

            # 6.4 VOLUMETRIC TACTICAL LASER BEAM (When surveying/scanning waypoints)
            inspect_t = cur_step.get("inspect_target")
            if inspect_t is not None and inspect_t != bot_u:
                target_node = inspect_t
            elif mode == "DIJKSTRA" and cur_step.get("phase") == "SCAN":
                target_node = cur_step.get("current_v", cur_step.get("current_u"))
            elif bot_u == bot_v and cur_step.get("scanned_edge", (-1, -1)) != (-1, -1):
                se = cur_step.get("scanned_edge", (-1, -1))
                target_node = se[1] if se[0] == bot_u else (se[0] if se[1] == bot_u else None)
            else:
                target_node = None

            if target_node is not None and target_node != bot_u:
                tp_node = self.get_column1_pos(target_node, z=8)

                lx1, ly1 = bot_lidar
                lx2, ly2 = tp_node
                dist_l = math.hypot(lx2 - lx1, ly2 - ly1)

                if dist_l > 8:
                    # Adaptive Laser Color Matrix based on active algorithm
                    if mode == "DIJKSTRA":
                        beam_c = (56, 189, 248)       # Electric Cyan
                        halo_rgba = (14, 165, 233, 65)
                    elif mode == "DFS":
                        beam_c = (168, 85, 247)      # Neon Violet
                        halo_rgba = (147, 51, 234, 65)
                    elif cur_step.get("action") == "ODD CYCLE CONFLICT":
                        beam_c = (239, 68, 68)       # Alert Red
                        halo_rgba = (220, 38, 38, 80)
                    else:
                        beam_c = (250, 204, 21)      # High-Power Gold
                        halo_rgba = (234, 179, 8, 65)

                    # Layer 1: Wide Atmospheric Glow Halo
                    glow_thick = int(9 + pulse_wave * 6)
                    pygame.draw.line(laser_overlay, halo_rgba, (lx1, ly1), (lx2, ly2), glow_thick)

                    # Layer 2: Main High-Energy Laser Beam
                    main_thick = max(2, int(3.5 + pulse_wave * 2))
                    pygame.draw.line(laser_overlay, (*beam_c, 230), (lx1, ly1), (lx2, ly2), main_thick)

                    # Layer 3: Ultra-Intense White Laser Plasma Core
                    core_thick = max(1, int(1.5 * scale))
                    pygame.draw.line(laser_overlay, (255, 255, 255, 245), (lx1, ly1), (lx2, ly2), core_thick)

                    # Layer 4: Dual Paraxial Telemetry Tracer Lines
                    nx = -(ly2 - ly1) / dist_l * 3.5
                    ny = (lx2 - lx1) / dist_l * 3.5
                    pygame.draw.line(laser_overlay, (*beam_c, 80), (lx1 + nx, ly1 + ny), (lx2, ly2), 1)
                    pygame.draw.line(laser_overlay, (*beam_c, 80), (lx1 - nx, ly1 - ny), (lx2, ly2), 1)

                    # Layer 5: Dynamic High-Speed Photon Energy Packets (Streaming Particles)
                    for p_i in range(3):
                        p_t = (t_ticks * 0.0035 + p_i * 0.33) % 1.0
                        px = int(lx1 + (lx2 - lx1) * p_t)
                        py = int(ly1 + (ly2 - ly1) * p_t)
                        pygame.draw.circle(laser_overlay, (255, 255, 255, 240), (px, py), int(2.5 + pulse_wave * 1.5))
                        pygame.draw.circle(laser_overlay, (*beam_c, 160), (px, py), int(5 + pulse_wave * 2.5))

                    # Layer 6: Tactical HUD Target Lock Reticle at Destination
                    # Expanding radar shockwave ring
                    ripple_r = int(8 + ((t_ticks * 0.045) % 18))
                    ripple_alpha = max(0, int(210 * (1.0 - ripple_r / 26.0)))
                    pygame.draw.circle(laser_overlay, (*beam_c, ripple_alpha), (lx2, ly2), ripple_r, 2)

                    # Rotating Sci-Fi HUD Crosshair Brackets
                    ret_r = int(14 + pulse_wave * 4)
                    pygame.draw.circle(laser_overlay, (*beam_c, 210), (lx2, ly2), ret_r, 1)
                    for angle_deg in [0, 90, 180, 270]:
                        c_rad = math.radians(angle_deg + (t_ticks * 0.09) % 360)
                        cx1 = lx2 + int((ret_r - 3) * math.cos(c_rad))
                        cy1 = ly2 + int((ret_r - 3) * math.sin(c_rad))
                        cx2 = lx2 + int((ret_r + 5) * math.cos(c_rad))
                        cy2 = ly2 + int((ret_r + 5) * math.sin(c_rad))
                        pygame.draw.line(laser_overlay, (255, 255, 255, 230), (cx1, cy1), (cx2, cy2), 2)

                    # Super-bright Laser Impact Spark
                    pygame.draw.circle(laser_overlay, (255, 255, 255, 255), (lx2, ly2), 4)
                    pygame.draw.circle(laser_overlay, (*beam_c, 190), (lx2, ly2), 8)

            # Composite Laser Overlay onto Column 1 Surface
            surf.blit(laser_overlay, (0, 0))

        self.screen.blit(surf, (COL1_X, COL_Y))
        pygame.draw.rect(self.screen, COLOR_CARD_BORDER, (COL1_X, COL_Y, COL1_WIDTH, COL_HEIGHT), 2)

    # =========================================================================
    # RENDER COLUMN 2: MATHEMATICAL GRAPH G = (V, E)
    # =========================================================================
    # =========================================================================
    # COLUMN 2: MATHEMATICAL GRAPH G = (V, E) (ĐỒ THỊ TOÁN HỌC)
    # =========================================================================
    # Giao diện này hiển thị cấu trúc đồ thị trừu tượng song song với sơ đồ vật lý.
    # Đỉnh = Các điểm mốc trong nhà.
    # Cạnh = Hành lang di chuyển an toàn giữa các mốc.
    def draw_column_2_graph(self, cur_step):
        surf = pygame.Surface((COL2_WIDTH, COL_HEIGHT))
        surf.fill(COLOR_CARD_BG)

        t_col2 = self.font_title.render("COL 2: MATHEMATICAL GRAPH G = (V, E)", True, COLOR_TEXT_GOLD)
        surf.blit(t_col2, (16, 10))

        surf.blit(self.font_small.render("Non-overlapping Bezier Curved Edges | Clear Planar Topology", True, COLOR_TEXT_MUTED), (16, 30))

        graph_bg = pygame.Rect(12, 48, COL2_WIDTH - 24, COL_HEIGHT - 62)
        pygame.draw.rect(surf, (15, 23, 42), graph_bg, border_radius=6)
        pygame.draw.rect(surf, (31, 41, 55), graph_bg, width=1, border_radius=6)

        scanned_edge = cur_step.get("scanned_edge", (-1, -1)) if cur_step else (-1, -1)
        chosen_edges = cur_step.get("after_chosen", set()) if cur_step else set()
        rejected_edges = cur_step.get("after_rejected", set()) if cur_step else set()
        shortest_path_edges = cur_step.get("shortest_path_edges", set()) if cur_step else set()
        is_path_found = cur_step.get("is_path_found", False) if cur_step else False

        seen = set()
        t_ticks = pygame.time.get_ticks()
        pulse = (math.sin(t_ticks * 0.008) + 1.0) / 2.0
        glow_w = int(3 + pulse * 4)

        blink = (math.sin(t_ticks * 0.012) + 1.0) / 2.0
        sp_pulse_w = int(5 + blink * 5)
        neon_g = int(180 + blink * 75)
        sp_neon_col = (16, neon_g, 220) if blink > 0.4 else (52, 255, 160)

        # 1. Draw 36 Bézier Curved Edges
        for u, v, l_m, cap in self.edges:
            edge_tuple = tuple(sorted((u, v)))
            if edge_tuple in seen:
                continue
            seen.add(edge_tuple)

            p1 = self.get_column2_graph_pos(u)
            p2 = self.get_column2_graph_pos(v)
            pts, mid_pt = self.get_arc_points(p1, p2, edge_tuple)

            is_sp = (is_path_found and self.active_mode == "DIJKSTRA" and edge_tuple in shortest_path_edges)
            is_scan = (edge_tuple == scanned_edge)
            is_pick = (edge_tuple in chosen_edges)
            is_rej = (edge_tuple in rejected_edges)

            if is_sp:
                aura_c = (5, 150, 105) if blink < 0.5 else (6, 182, 212)
                pygame.draw.lines(surf, aura_c, False, pts, sp_pulse_w + 6)
                pygame.draw.lines(surf, sp_neon_col, False, pts, sp_pulse_w)
                pygame.draw.lines(surf, (255, 255, 255), False, pts, max(2, sp_pulse_w - 4))
            elif is_scan:
                pygame.draw.lines(surf, COLOR_TEXT_GOLD, False, pts, glow_w)
            elif is_pick:
                col = COLOR_TEXT_GREEN if self.active_mode != "DIJKSTRA" else COLOR_TEXT_CYAN
                pygame.draw.lines(surf, col, False, pts, 4)
            elif is_rej:
                pygame.draw.lines(surf, (239, 68, 68, 120), False, pts, 2)
            else:
                pygame.draw.lines(surf, (51, 65, 85), False, pts, 2)

            mx, my = mid_pt
            if is_sp:
                tag_surf = self.font_tag.render(f"★ {l_m:.1f}m", True, (255, 255, 255))
                t_rect = pygame.Rect(mx - tag_surf.get_width()//2 - 3, my - tag_surf.get_height()//2 - 2, tag_surf.get_width() + 6, tag_surf.get_height() + 4)
                pygame.draw.rect(surf, (5, 150, 105), t_rect, border_radius=4)
                pygame.draw.rect(surf, (52, 255, 160), t_rect, width=2, border_radius=4)
                surf.blit(tag_surf, (mx - tag_surf.get_width()//2, my - tag_surf.get_height()//2))
            else:
                tag_col = COLOR_TEXT_GOLD if is_scan else (COLOR_TEXT_GREEN if is_pick else (COLOR_TEXT_RED if is_rej else (148, 163, 184)))
                bg_col = (55, 48, 163) if is_scan else ((6, 78, 59) if is_pick else ((127, 29, 29) if is_rej else (15, 23, 42)))
                
                tag_surf = self.font_tag.render(f"{l_m:.1f}m", True, tag_col)
                t_rect = pygame.Rect(mx - tag_surf.get_width()//2 - 2, my - tag_surf.get_height()//2 - 1, tag_surf.get_width() + 4, tag_surf.get_height() + 2)
                pygame.draw.rect(surf, bg_col, t_rect, border_radius=3)
                pygame.draw.rect(surf, tag_col if (is_scan or is_pick) else (51, 65, 85), t_rect, width=1, border_radius=3)
                surf.blit(tag_surf, (mx - tag_surf.get_width()//2, my - tag_surf.get_height()//2))

        # 2. Moving Energy Pulse
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

        # 3. Draw 25 Mathematical Nodes
        sp_nodes = cur_step.get("shortest_path_nodes", []) if (cur_step and is_path_found and self.active_mode == "DIJKSTRA") else []
        for i, d in self.nodes_data.items():
            gx, gy = self.get_column2_graph_pos(i)
            is_cur = (cur_step and (i == cur_step.get("current_u") or i == cur_step.get("current_v")))
            is_dock = (i == 0)
            is_sp_node = (i in sp_nodes)

            color = (236, 72, 153) if is_dock else ((59, 130, 246) if d["zone"] == "DRY" else (245, 158, 11))
            r = 14 if is_dock else 12

            if is_sp_node:
                pygame.draw.circle(surf, (52, 255, 160), (gx, gy), int(16 + blink * 8), 2)
                pygame.draw.circle(surf, (16, 185, 129, 90), (gx, gy), int(22 + blink * 8), 1)

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
    # RENDER COLUMN 3: LIVE PSEUDOCODE & MATHEMATICAL VARIABLES INSPECTOR
    # =========================================================================
    # =========================================================================
    # COLUMN 3: ALGORITHM INSPECTOR (BẢNG ĐIỀU KHIỂN & TRẠNG THÁI TOÁN HỌC)
    # =========================================================================
    # Bảng này hiển thị từng bước chạy (Step-by-step) của thuật toán:
    # 1. Mã giả (Pseudocode) đang chạy tới dòng nào.
    # 2. Trạng thái các biến toán học (Queue, Stack, Array...)
    # 3. Log hành động của Robot.
    def draw_column_3_inspector(self, cur_step):
        surf = pygame.Surface((COL3_WIDTH, COL_HEIGHT))
        surf.fill(COLOR_CARD_BG)

        t_col3 = self.font_title.render("COL 3: PSEUDOCODE & LIVE MATH INSPECTOR", True, (244, 114, 182))
        surf.blit(t_col3, (16, 10))

        step_txt = f"Step: {self.current_step_idx + 1}/{len(self.steps)}" if self.steps else "Ready"
        surf.blit(self.font_small.render(f"Active Mode: {self.active_mode} ALGORITHM | {step_txt}", True, COLOR_TEXT_MUTED), (16, 30))

        py = 50

        # 1. PSEUDOCODE BOX (210px)
        h1 = 210
        box1 = pygame.Rect(14, py, COL3_WIDTH - 28, h1)
        pygame.draw.rect(surf, (15, 23, 42), box1, border_radius=6)
        pygame.draw.rect(surf, (31, 41, 55), box1, width=1, border_radius=6)

        surf.blit(self.font_tag.render("ACTIVE ALGORITHM PSEUDOCODE:", True, COLOR_TEXT_CYAN), (22, py + 8))

        if cur_step and "pseudocode" in cur_step:
            active_line = cur_step.get("pseudocode_line", 1)
            line_y = py + 28
            for idx, pline in enumerate(cur_step["pseudocode"]):
                is_cur_line = (idx + 1 == active_line)
                if is_cur_line:
                    hl_rect = pygame.Rect(18, line_y - 2, COL3_WIDTH - 36, 19)
                    pygame.draw.rect(surf, (55, 48, 163), hl_rect, border_radius=3)
                    surf.blit(self.font_code.render(f"> {pline}", True, COLOR_TEXT_GOLD), (22, line_y))
                else:
                    surf.blit(self.font_code.render(f"  {pline}", True, (203, 213, 225)), (22, line_y))
                line_y += 20

        py += h1 + 10

        # 2. STEP REASONING & ROBOT ACTION BOX (245px)
        h2 = 245
        box2 = pygame.Rect(14, py, COL3_WIDTH - 28, h2)
        pygame.draw.rect(surf, (15, 23, 42), box2, border_radius=6)
        pygame.draw.rect(surf, COLOR_CARD_BORDER_GLOW, box2, width=1, border_radius=6)

        if cur_step:
            u = cur_step.get("current_u", 0)
            v = cur_step.get("current_v", 0)
            u_name = self.nodes_data.get(u, {}).get("name", f"Node {u}")
            v_name = self.nodes_data.get(v, {}).get("name", f"Node {v}")
            w = cur_step.get("scanned_weight", 0.0)

            title = cur_step.get("step_title", f"EVALUATING EDGE ({u} <-> {v})")
            surf.blit(self.font_main.render(f"STEP {self.current_step_idx + 1}/{len(self.steps)}: {title}", True, COLOR_TEXT_GOLD), (22, py + 8))

            phase = cur_step.get("phase", "")
            if phase == "LOCKED":
                surf.blit(self.font_body.render(f"> Path locked: [22] Plants -> ... -> [0] Charging Dock (w = {w:.1f}m)", True, COLOR_TEXT_WHITE), (22, py + 30))
            elif phase == "TRAVELING":
                surf.blit(self.font_body.render(f"> Autonomous motion: [{u}] {u_name} -> [{v}] {v_name} (Segment: {w:.1f}m)", True, COLOR_TEXT_WHITE), (22, py + 30))
            elif phase == "DOCKED":
                surf.blit(self.font_body.render("> Robot coupling: Secured at [0] Charging Dock Base", True, COLOR_TEXT_WHITE), (22, py + 30))
            else:
                surf.blit(self.font_body.render(f"> Scanning path: [{u}] {u_name} -> [{v}] {v_name} (w = {w:.1f}m)", True, COLOR_TEXT_WHITE), (22, py + 30))

            surf.blit(self.font_main.render("> Mathematical Condition:", True, (244, 114, 182)), (22, py + 52))
            surf.blit(self.font_body.render(cur_step.get("reason", ""), True, (226, 232, 240)), (26, py + 72))

            surf.blit(self.font_main.render("> Action:", True, COLOR_TEXT_GREEN), (22, py + 96))
            surf.blit(self.font_main.render(cur_step.get("result_text", ""), True, cur_step.get("status_color", COLOR_TEXT_CYAN)), (26, py + 118))

        py += h2 + 10

        # 3. LIVE VARIABLES BOX (435px)
        h3 = 435
        box3 = pygame.Rect(14, py, COL3_WIDTH - 28, h3)
        pygame.draw.rect(surf, (15, 23, 42), box3, border_radius=6)
        pygame.draw.rect(surf, (31, 41, 55), box3, width=1, border_radius=6)

        surf.blit(self.font_tag.render("LIVE MATHEMATICAL VARIABLES STATE:", True, COLOR_TEXT_CYAN), (22, py + 8))

        if cur_step and "math_state" in cur_step:
            var_y = py + 30
            for k, val in cur_step["math_state"].items():
                surf.blit(self.font_body.render(f"> {k}:", True, (148, 163, 184)), (22, var_y))
                surf.blit(self.font_main.render(str(val), True, COLOR_TEXT_GOLD), (220, var_y))
                var_y += 20

            chosen_list = list(cur_step["after_chosen"])
            c_y = var_y + 10
            chosen_str = ", ".join([f"({cu}<->{cv})" for cu, cv in chosen_list[:10]])
            surf.blit(self.font_small.render(f"Selected Edges ({len(chosen_list)}): {chosen_str}", True, (226, 232, 240)), (22, c_y))
            if len(chosen_list) > 10:
                chosen_str2 = ", ".join([f"({cu}<->{cv})" for cu, cv in chosen_list[10:20]])
                surf.blit(self.font_small.render(f"                         {chosen_str2}", True, (226, 232, 240)), (22, c_y + 18))

        # 4. STEP CONTROLLER BUTTONS
        btn_y = COL_HEIGHT - 46
        mouse_pos = pygame.mouse.get_pos()

        is_h_p = self.btn_prev_rect.collidepoint(mouse_pos)
        pygame.draw.rect(surf, (51, 65, 85) if is_h_p else (30, 41, 59), (12, btn_y, 90, 36), border_radius=5)
        pygame.draw.rect(surf, COLOR_TEXT_CYAN, (12, btn_y, 90, 36), width=1, border_radius=5)
        surf.blit(self.font_main.render("< PREV [B]", True, (255, 255, 255)), (18, btn_y + 9))

        is_h_n = self.btn_next_rect.collidepoint(mouse_pos)
        pygame.draw.rect(surf, (14, 116, 144) if is_h_n else (8, 145, 178), (108, btn_y, 110, 36), border_radius=5)
        pygame.draw.rect(surf, (255, 255, 255) if is_h_n else COLOR_TEXT_CYAN, (108, btn_y, 110, 36), width=1, border_radius=5)
        surf.blit(self.font_main.render("NEXT [S] >", True, (255, 255, 255)), (120, btn_y + 9))

        auto_bg = (5, 150, 105) if self.is_auto_playing else (51, 65, 85)
        pygame.draw.rect(surf, auto_bg, (224, btn_y, 140, 36), border_radius=5)
        pygame.draw.rect(surf, COLOR_TEXT_GREEN if self.is_auto_playing else (148, 163, 184), (224, btn_y, 140, 36), width=1, border_radius=5)
        auto_lbl = "PAUSE [SPACE]" if self.is_auto_playing else "AUTO PLAY"
        surf.blit(self.font_main.render(auto_lbl, True, (255, 255, 255)), (234, btn_y + 9))

        is_h_r = self.btn_reset_rect.collidepoint(mouse_pos)
        pygame.draw.rect(surf, (71, 85, 105) if is_h_r else (51, 65, 85), (370, btn_y, 80, 36), border_radius=5)
        pygame.draw.rect(surf, (148, 163, 184), (370, btn_y, 80, 36), width=1, border_radius=5)
        surf.blit(self.font_main.render("RESET [R]", True, (255, 255, 255)), (374, btn_y + 9))

        fs_w = max(40, COL3_WIDTH - 12 - 456)
        is_h_fs = self.btn_fullscreen_rect.collidepoint(mouse_pos)
        pygame.draw.rect(surf, (14, 165, 233) if is_h_fs else (3, 105, 161), (456, btn_y, fs_w, 36), border_radius=5)
        surf.blit(self.font_tag.render("[F11] FULL", True, (255, 255, 255)), (464, btn_y + 10))

        self.screen.blit(surf, (COL3_X, COL_Y))
        pygame.draw.rect(self.screen, COLOR_CARD_BORDER, (COL3_X, COL_Y, COL3_WIDTH, COL_HEIGHT), 2)

    def draw_top_bar(self):
        """Renders the top algorithm navigation bar."""
        mouse_pos = pygame.mouse.get_pos()
        for rect, label, mode_id, color in self.top_buttons:
            is_act = (self.active_mode == mode_id)
            is_hov = self.is_top_button_hit(rect, mouse_pos)

            bg_c = (color[0]//2, color[1]//2, color[2]//2) if is_act else ((51, 65, 85) if is_hov else (17, 24, 39))
            border_c = color if is_act else ((148, 163, 184) if is_hov else (31, 41, 55))

            pygame.draw.rect(self.screen, bg_c, rect, border_radius=6)
            pygame.draw.rect(self.screen, border_c, rect, width=2 if is_act else 1, border_radius=6)

            txt_c = (255, 255, 255) if is_act else (226, 232, 240)
            btn_t = self.font_main.render(label, True, txt_c)
            self.screen.blit(btn_t, (rect.centerx - btn_t.get_width()//2, rect.centery - btn_t.get_height()//2))

    def switch_mode(self, mode_id):
        """Switches dynamically to a different graph algorithm."""
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
            self.steps = self.algo_engine.build_maxflow_steps(source=0, sink=22)

        self.current_step_idx = 0
        self.anim_t = 1.0

    def step_next(self):
        """Advances one algorithm step."""
        if self.current_step_idx < len(self.steps) - 1:
            self.current_step_idx += 1
            self.anim_t = 0.0

    def step_prev(self):
        """Reverses one algorithm step."""
        if self.current_step_idx > 0:
            self.current_step_idx -= 1
            self.anim_t = 0.0

    def toggle_fullscreen(self):
        """
        Toggles fullscreen cleanly while preserving 16:9 aspect ratio and visual fidelity.
        Uses native desktop resolution to avoid stretching or pixel distortion on Windows, Mac, Linux.
        """
        self.is_fullscreen = not self.is_fullscreen
        try:
            # Pygame 2 / SDL2 native toggle (fast and maintains context)
            if pygame.display.toggle_fullscreen():
                return
        except Exception:
            pass

        # Fallback method if display driver does not support dynamic toggle
        flags = pygame.SCALED
        if self.is_fullscreen:
            flags |= pygame.FULLSCREEN
        else:
            flags |= pygame.RESIZABLE

        self.screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT), flags)

    def run(self):
        """Main game loop handling events, simulation state, and rendering."""
        running = True
        while running:
            self.clock.tick(FPS)
            raw_mx, raw_my = pygame.mouse.get_pos()

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

                elif event.type == pygame.VIDEORESIZE:
                    # Pygame SCALED automatically scales viewport
                    pass

                elif event.type == pygame.MOUSEWHEEL:
                    mx, my = pygame.mouse.get_pos()
                    if mx <= COL1_X + COL1_WIDTH:
                        self.cam_zoom = max(0.4, min(3.0, self.cam_zoom + event.y * 0.08))

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click_pos = event.pos

                        # 1. Check Top Algorithm Navigation Buttons (100% precise in any window size)
                        top_clicked = False
                        for rect, _, mode_id, _ in self.top_buttons:
                            if self.is_top_button_hit(rect, click_pos):
                                self.switch_mode(mode_id)
                                top_clicked = True
                                break

                        if top_clicked:
                            continue

                        # 2. Check Column 1 Zoom / 3D Mode Buttons
                        if self.btn_zoom_out_rect.inflate(4, 4).collidepoint(click_pos):
                            self.cam_zoom = max(0.4, self.cam_zoom - 0.15)
                        elif self.btn_zoom_in_rect.inflate(4, 4).collidepoint(click_pos):
                            self.cam_zoom = min(3.0, self.cam_zoom + 0.15)
                        elif self.btn_zoom_badge_rect.inflate(4, 4).collidepoint(click_pos):
                            self.cam_zoom = 1.15
                            self.cam_pan_x = 0
                            self.cam_pan_y = 0
                        elif self.btn_view_3d_rect.inflate(4, 4).collidepoint(click_pos):
                            self.is_3d_mode = not self.is_3d_mode

                        # 3. Check Column 3 Step Controller Buttons
                        elif self.btn_prev_rect.inflate(4, 4).collidepoint(click_pos):
                            self.step_prev()
                        elif self.btn_next_rect.inflate(4, 4).collidepoint(click_pos):
                            self.step_next()
                        elif self.btn_auto_rect.inflate(4, 4).collidepoint(click_pos):
                            self.is_auto_playing = not self.is_auto_playing
                        elif self.btn_reset_rect.inflate(4, 4).collidepoint(click_pos):
                            self.current_step_idx = 0
                            self.is_auto_playing = False
                            self.anim_t = 0.0
                        elif self.btn_fullscreen_rect.inflate(4, 4).collidepoint(click_pos):
                            self.toggle_fullscreen()

                        # 4. Canvas Dragging for 3D Camera Rotation
                        elif click_pos[0] < COL1_X + COL1_WIDTH and click_pos[1] > COL_Y:
                            self.is_dragging_3d = True
                            self.last_mouse_pos = click_pos

                    elif event.button == 3:
                        click_pos = event.pos
                        if click_pos[0] < COL1_X + COL1_WIDTH and click_pos[1] > COL_Y:
                            self.is_panning_3d = True
                            self.last_mouse_pos = click_pos

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.is_dragging_3d = False
                    elif event.button == 3:
                        self.is_panning_3d = False

                elif event.type == pygame.MOUSEMOTION:
                    cur_pos = event.pos
                    if self.is_dragging_3d and self.is_3d_mode:
                        dx = cur_pos[0] - self.last_mouse_pos[0]
                        dy = cur_pos[1] - self.last_mouse_pos[1]
                        self.cam_yaw = (self.cam_yaw + dx * 0.5) % 360.0
                        self.cam_pitch = max(10.0, min(85.0, self.cam_pitch - dy * 0.5))
                        self.last_mouse_pos = cur_pos
                    elif self.is_panning_3d:
                        dx = cur_pos[0] - self.last_mouse_pos[0]
                        dy = cur_pos[1] - self.last_mouse_pos[1]
                        self.cam_pan_x += dx
                        self.cam_pan_y += dy
                        self.last_mouse_pos = cur_pos

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
                        self.cam_zoom = 1.15
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

            # Render background and the 3 distinct dashboard columns
            self.screen.fill(COLOR_APP_BG)
            self.draw_top_bar()

            cur_step = self.steps[self.current_step_idx] if self.steps else None
            self.draw_column_1_floorplan(cur_step)
            self.draw_column_2_graph(cur_step)
            self.draw_column_3_inspector(cur_step)

            pygame.display.flip()

        pygame.quit()

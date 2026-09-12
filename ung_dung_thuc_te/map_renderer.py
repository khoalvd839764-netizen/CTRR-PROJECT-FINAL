# -*- coding: utf-8 -*-
"""
Module: ung_dung_thuc_te/map_renderer.py
Đảm nhận toàn bộ việc vẽ các thành phần địa hình bản đồ sa bàn:
- Sông ngòi, kênh rạch (Sông Sài Gòn, Kênh Nhiêu Lộc - Thị Nghè).
- Mạng lưới tuyến đường, độ rộng, tình trạng kẹt xe/phong tỏa, mũi tên 1 chiều.
- Các nút giao thông, trạm y tế, trạm cứu hỏa, trường ĐH GTVT (UTH), địa danh.
- Hiển thị tooltip thông tin khi rê chuột vào nút giao.
"""
import math
import pygame

from ung_dung_thuc_te.config import (
    COLOR_RIVER, COLOR_RIVER_EDGE,
    COLOR_ROAD_NORMAL, COLOR_ROAD_ONEWAY, COLOR_ROAD_CONGESTED, COLOR_ROAD_BLOCKED,
    COLOR_NODE_DEFAULT, COLOR_NODE_UTH, COLOR_NODE_HOSPITAL, COLOR_NODE_FIRE,
    COLOR_NODE_LANDMARK, COLOR_NODE_REMOTE, COLOR_NODE_ACCIDENT,
    COLOR_BFS_LEVELS, COLOR_TEXT_HIGHLIGHT
)


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


def draw_rivers_and_canals(screen, river_saigon, canal_nhieuloc):
    """Vẽ Sông Sài Gòn và Kênh Nhiêu Lộc - Thị Nghè."""
    if len(river_saigon) >= 2:
        pygame.draw.lines(screen, COLOR_RIVER_EDGE, False, river_saigon, 34)
        pygame.draw.lines(screen, COLOR_RIVER, False, river_saigon, 28)
    if len(canal_nhieuloc) >= 2:
        pygame.draw.lines(screen, COLOR_RIVER_EDGE, False, canal_nhieuloc, 18)
        pygame.draw.lines(screen, COLOR_RIVER, False, canal_nhieuloc, 14)


def draw_roads(screen, city):
    """Vẽ toàn bộ mạng lưới đường sá giao thông theo trạng thái thực tế."""
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


def draw_intersections(screen, city, fonts, mouse_pos, explored_layers, accident_node, map_width):
    """Vẽ 37/45 nút giao, trạm xe, trường học với viền phân lớp BFS sắc nét."""
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
        if is_hover and mouse_pos[0] < map_width:
            hovered_node = ndata

        if nid == accident_node:
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

        # Mã code nút - Dạng badge/pill sắc nét
        code_surf = fonts["node"].render(ndata["code"], True, (245, 250, 255))
        pw = code_surf.get_width() + 8
        ph = code_surf.get_height() + 2
        px = nx - pw // 2
        py = ny + node_radius + 3
        pill_rect = pygame.Rect(px, py, pw, ph)

        pill_bg = (10, 15, 26)
        pill_border = (45, 65, 95)
        if nid == accident_node:
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

    return hovered_node


def draw_highlighted_stations(screen, city, fonts, highlighted_stations):
    """Tô đậm rực rỡ các trạm cứu hộ được chọn tại lớp ngắn nhất."""
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


def draw_node_tooltip(screen, fonts, hovered_node, mouse_pos, map_width):
    """Vẽ tooltip thông tin chi tiết nút giao / số xe sẵn sàng khi rê chuột."""
    if hovered_node is None:
        return

    tip_title = hovered_node["name"]
    tip_desc = hovered_node.get("desc", "")
    if "fleet" in hovered_node:
        avail = hovered_node["fleet"] - hovered_node.get("busy", 0)
        tip_desc += f" [Sẵn sàng: {avail}/{hovered_node['fleet']}]"

    t_surf1 = fonts["small"].render(tip_title, True, COLOR_TEXT_HIGHLIGHT)
    t_surf2 = fonts["tiny"].render(tip_desc, True, (210, 225, 245))

    box_w = max(t_surf1.get_width(), t_surf2.get_width()) + 14
    box_h = 38
    bx = min(mouse_pos[0] + 10, map_width - box_w - 10)
    by = max(mouse_pos[1] - 42, 10)

    tip_rect = pygame.Rect(bx, by, box_w, box_h)
    pygame.draw.rect(screen, (15, 20, 32), tip_rect, border_radius=4)
    pygame.draw.rect(screen, (70, 95, 135), tip_rect, 1, border_radius=4)
    screen.blit(t_surf1, (bx + 7, by + 3))
    screen.blit(t_surf2, (bx + 7, by + 20))

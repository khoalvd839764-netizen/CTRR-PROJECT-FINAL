# -*- coding: utf-8 -*-
"""
Module: ung_dung_thuc_te/radial_menu.py
Menu tròn tương tác động hiển thị tại vị trí nút được click.
Thiết kế thích ứng thông minh (Adaptive Bounds):
  - Tự động xoay chùm nút xuống dưới nếu nút ở sát mép trên màn hình (không bao giờ bị mất lựa chọn bên trên).
  - Tự động xoay chùm nút sang bên đối diện nếu nút ở sát mép trái hoặc mép phải (bờ HUD).
  - Giới hạn cứng tọa độ mọi nút bấm luôn nằm hoàn toàn bên trong khung hiển thị bản đồ.
"""
import math
import pygame
from ung_dung_thuc_te.config import (
    MAP_WIDTH, MAP_HEIGHT,
    COLOR_PANEL_BG, COLOR_TEXT_WHITE,
    COLOR_NODE_HOSPITAL, COLOR_NODE_FIRE
)


class RadialMenu:
    """Menu tròn tương tác động với thuật toán định vị không bị tràn viền màn hình."""
    def __init__(self, node_id, node_name, center_pos):
        self.node_id = node_id
        self.node_name = node_name
        self.center_x, self.center_y = center_pos
        self.active = True
        self.radius = 76
        self.btn_radius = 26
        
        # 1. Thuật toán định hướng góc bấm thích ứng theo tọa độ nút
        # Mép trên: y < 135 -> Toàn bộ các lựa chọn xòe xuống dưới (không có nút nào bay lên trên)
        if self.center_y < 135:
            self.title_below = True
            if self.center_x > MAP_WIDTH - 150:
                angle_dual = 100
                angle_med = 125
                angle_fire = 150
                angle_cancel = 175
            elif self.center_x < 150:
                angle_dual = 80
                angle_med = 55
                angle_fire = 30
                angle_cancel = 5
            else:
                angle_dual = 70
                angle_med = 30
                angle_fire = 110
                angle_cancel = 150
        elif self.center_y > 590:
            angle_dual = -70
            angle_med = -30
            angle_fire = -110
            angle_cancel = -150
            self.title_below = False
        elif self.center_x < 125:
            angle_dual = -15
            angle_med = -55
            angle_fire = 25
            angle_cancel = 65
            self.title_below = False
        elif self.center_x > MAP_WIDTH - 125:
            angle_dual = -165
            angle_med = -125
            angle_fire = 155
            angle_cancel = 115
            self.title_below = False
        else:
            angle_dual = -90
            angle_med = -25
            angle_fire = -155
            angle_cancel = 90
            self.title_below = False

        self.buttons = [
            {
                "type": "MEDICAL",
                "label": "CẤP CỨU",
                "sub": "Gọi BV",
                "angle": angle_med,
                "color": COLOR_NODE_HOSPITAL,
                "hover_color": (30, 255, 160)
            },
            {
                "type": "FIRE",
                "label": "BÁO CHÁY",
                "sub": "Gọi PCCC",
                "angle": angle_fire,
                "color": COLOR_NODE_FIRE,
                "hover_color": (255, 140, 40)
            },
            {
                "type": "DUAL",
                "label": "T.NẠN NẶNG",
                "sub": "BV + PCCC",
                "angle": angle_dual,
                "color": (235, 45, 120),
                "hover_color": (255, 90, 180)
            },
            {
                "type": "CANCEL",
                "label": "HỦY",
                "sub": "Đóng",
                "angle": angle_cancel,
                "color": (80, 95, 125),
                "hover_color": (240, 70, 70)
            }
        ]

        # 2. Tính toán và KẸP TỌA ĐỘ BẢO VỆ CHỐNG TRÀN VIỀN
        margin = self.btn_radius + 8
        for btn in self.buttons:
            rad = math.radians(btn["angle"])
            bx = self.center_x + int(self.radius * math.cos(rad))
            by = self.center_y + int(self.radius * math.sin(rad))

            # Giới hạn cứng trong vùng hiển thị an toàn của bản đồ
            btn["x"] = max(margin, min(bx, MAP_WIDTH - margin))
            btn["y"] = max(margin, min(by, MAP_HEIGHT - margin))

    def handle_click(self, mouse_pos):
        """Xử lý sự kiện click chuột, trả về loại sự cố được chọn hoặc None."""
        mx, my = mouse_pos
        for btn in self.buttons:
            dist = math.hypot(mx - btn["x"], my - btn["y"])
            if dist <= self.btn_radius + 4:
                return btn["type"]
        
        # Click ra ngoài vùng bán kính menu -> Hủy
        dist_center = math.hypot(mx - self.center_x, my - self.center_y)
        if dist_center > self.radius + self.btn_radius + 35:
            return "CANCEL"
        return None

    def draw(self, surface, fonts, mouse_pos=None):
        """Vẽ menu tròn cùng các nhãn định vị an toàn lên màn hình (hỗ trợ mouse_pos ảo)."""
        font_sm = fonts["small"]
        font_xs = fonts["tiny"]
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()

        # 1. Vòng hào quang mờ nối các nút
        pygame.draw.circle(surface, (40, 55, 80), (self.center_x, self.center_y), self.radius, 2)

        # 2. Đường nan hoa từ tâm sự cố đến từng nút lựa chọn
        for btn in self.buttons:
            pygame.draw.line(surface, (60, 80, 115), (self.center_x, self.center_y), (btn["x"], btn["y"]), 2)

        # 3. Tâm điểm sự cố
        pygame.draw.circle(surface, (255, 50, 50), (self.center_x, self.center_y), 16)
        pygame.draw.circle(surface, (255, 255, 255), (self.center_x, self.center_y), 16, 2)
        
        # 4. Vẽ từng nút lựa chọn tròn
        for btn in self.buttons:
            dist = math.hypot(mouse_pos[0] - btn["x"], mouse_pos[1] - btn["y"])
            is_hover = (dist <= self.btn_radius + 4)
            r = self.btn_radius + (3 if is_hover else 0)
            col = btn["hover_color"] if is_hover else btn["color"]

            # Nền nút tròn với viền nổi bật
            pygame.draw.circle(surface, (14, 20, 32), (btn["x"], btn["y"]), r + 2)
            pygame.draw.circle(surface, COLOR_PANEL_BG, (btn["x"], btn["y"]), r)
            pygame.draw.circle(surface, col, (btn["x"], btn["y"]), r, 3 if is_hover else 2)

            # Chữ tiêu đề trên nút
            lbl_surf = font_xs.render(btn["label"], True, COLOR_TEXT_WHITE if not is_hover else col)
            sub_surf = font_xs.render(btn["sub"], True, (215, 230, 245))
            
            surface.blit(lbl_surf, (btn["x"] - lbl_surf.get_width() // 2, btn["y"] - 10))
            surface.blit(sub_surf, (btn["x"] - sub_surf.get_width() // 2, btn["y"] + 3))

        # 5. Hộp tiêu đề thông báo vị trí sự cố (Tự động canh lề chống tràn màn hình)
        title_surf = font_sm.render(f"SỰ CỐ TẠI: {self.node_name}", True, (255, 220, 50))
        t_w = title_surf.get_width() + 16
        tx = max(10, min(self.center_x - t_w // 2, MAP_WIDTH - t_w - 10))
        
        if self.title_below:
            max_btn_y = max(btn["y"] for btn in self.buttons)
            ty = min(max_btn_y + self.btn_radius + 8, MAP_HEIGHT - 32)
        else:
            min_btn_y = min(btn["y"] for btn in self.buttons)
            ty = max(min_btn_y - self.btn_radius - 28, 10)

        bg_rect = pygame.Rect(tx, ty, t_w, 24)
        pygame.draw.rect(surface, (15, 22, 35), bg_rect, border_radius=4)
        pygame.draw.rect(surface, (255, 220, 50), bg_rect, 1, border_radius=4)
        surface.blit(title_surf, (tx + 8, ty + 3))

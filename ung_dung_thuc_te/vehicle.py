# -*- coding: utf-8 -*-
"""
Module: ung_dung_thuc_te/vehicle.py
Quản lý hoạt họa di chuyển của Phương tiện Cứu hộ (Xe Cứu Thương / Xe Cứu Hỏa).
Bao gồm: Chuyển động mượt mà (lerp), xoay góc theo hướng đi, đèn còi ưu tiên nhấp nháy,
vệt sáng đuôi xe (light trail), và hỗ trợ tự động bẻ cua né đường tắc (Dynamic Reroute).
"""
import math
import pygame


class EmergencyVehicle:
    """Lớp đối tượng xe cứu hộ khẩn cấp."""
    def __init__(self, vehicle_id, vehicle_type, path, nodes_dict, station_id, dest_id):
        self.id = vehicle_id
        self.type = vehicle_type  # 'AMBULANCE' hoặc 'FIRE_TRUCK'
        self.path = list(path)
        self.nodes = nodes_dict
        self.station_id = station_id
        self.dest_id = dest_id
        
        self.path_index = 0
        start_pos = self.nodes[self.path[0]]["pos"]
        self.x = float(start_pos[0])
        self.y = float(start_pos[1])
        
        self.speed = 3.8  # Tốc độ di chuyển (pixel/frame)
        self.angle = 0.0
        self.active = True
        self.arrived = False
        
        self.siren_tick = 0
        self.trail = []   # Lưu vết vệt sáng đuôi xe

    def update(self):
        """Cập nhật vị trí di chuyển theo lộ trình từng frame."""
        if not self.active or self.arrived:
            return

        self.siren_tick += 1

        # Lưu lại vị trí để vẽ trail đuôi xe
        self.trail.append((self.x, self.y))
        if len(self.trail) > 12:
            self.trail.pop(0)

        # Kiểm tra mục tiêu tiếp theo trên lộ trình
        if self.path_index < len(self.path) - 1:
            next_node_id = self.path[self.path_index + 1]
            target_x, target_y = self.nodes[next_node_id]["pos"]
            
            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.hypot(dx, dy)

            # Tính góc xoay của xe
            self.angle = math.degrees(math.atan2(-dy, dx))

            if dist <= self.speed:
                # Đã tới nút tiếp theo
                self.x = float(target_x)
                self.y = float(target_y)
                self.path_index += 1
                
                # Nếu đã tới điểm cuối của lộ trình
                if self.path_index >= len(self.path) - 1:
                    self.arrived = True
            else:
                # Di chuyển tịnh tiến mượt mà
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed

    def reroute(self, new_path):
        """Cập nhật lộ trình mới khi phát hiện sự cố kẹt xe phía trước."""
        if new_path and len(new_path) >= 2:
            self.path = list(new_path)
            self.path_index = 0

    def get_current_segment(self):
        """Trả về cặp (u, v) đoạn đường xe đang di chuyển."""
        if self.path_index < len(self.path) - 1:
            return self.path[self.path_index], self.path[self.path_index + 1]
        return None

    def draw(self, surface, fonts):
        """Vẽ xe cứu hộ cùng hiệu ứng đèn còi, vệt sáng và đèn pha chiếu sáng."""
        if not self.active:
            return

        # 1. Vẽ vệt sáng đuôi xe (Trail)
        trail_len = len(self.trail)
        trail_color = (0, 240, 255) if self.type == "AMBULANCE" else (255, 120, 20)
        for i, (tx, ty) in enumerate(self.trail):
            alpha_ratio = (i + 1) / (trail_len + 1)
            r = int(5 * alpha_ratio)
            if r > 0:
                pygame.draw.circle(surface, trail_color, (int(tx), int(ty)), r)

        # 2. Vẽ đèn pha chiếu sáng phía trước
        rad = math.radians(-self.angle)
        dir_x = math.cos(rad)
        dir_y = math.sin(rad)
        perp_x = -dir_y
        perp_y = dir_x

        beam_len = 35
        beam_spread = 16
        head_x = self.x + dir_x * 12
        head_y = self.y + dir_y * 12

        p1 = (head_x + dir_x * beam_len + perp_x * beam_spread, head_y + dir_y * beam_len + perp_y * beam_spread)
        p2 = (head_x + dir_x * beam_len - perp_x * beam_spread, head_y + dir_y * beam_len - perp_y * beam_spread)
        
        # Tam giác đèn pha bán trong suốt
        light_surf = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        pygame.draw.polygon(light_surf, (255, 255, 200, 35), [(head_x, head_y), p1, p2])
        surface.blit(light_surf, (0, 0))

        # 3. Thân xe hình chữ nhật xoay theo hướng
        veh_w, veh_h = 24, 14
        veh_surf = pygame.Surface((veh_w, veh_h), pygame.SRCALPHA)
        
        body_color = (245, 250, 255) if self.type == "AMBULANCE" else (220, 45, 30)
        border_color = (30, 80, 180) if self.type == "AMBULANCE" else (255, 220, 0)
        
        pygame.draw.rect(veh_surf, body_color, (0, 0, veh_w, veh_h), border_radius=3)
        pygame.draw.rect(veh_surf, border_color, (0, 0, veh_w, veh_h), 2, border_radius=3)

        # Kính xe
        pygame.draw.rect(veh_surf, (40, 60, 90), (veh_w - 7, 2, 5, veh_h - 4), border_radius=1)

        # Đèn còi ưu tiên nhấp nháy (Xanh - Đỏ luân phiên)
        siren_flash = (self.siren_tick // 6) % 2
        col_left = (255, 30, 30) if siren_flash == 0 else (30, 120, 255)
        col_right = (30, 120, 255) if siren_flash == 0 else (255, 30, 30)
        
        pygame.draw.circle(veh_surf, col_left, (veh_w // 2 - 3, veh_h // 2), 3)
        pygame.draw.circle(veh_surf, col_right, (veh_w // 2 + 3, veh_h // 2), 3)

        # Xoay surface theo góc angle
        rotated_surf = pygame.transform.rotate(veh_surf, self.angle)
        rect = rotated_surf.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated_surf, rect)

        # 4. Hào quang đèn còi lan tỏa
        glow_radius = 18 + int(math.sin(self.siren_tick * 0.3) * 4)
        glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        glow_color = (255, 40, 40, 50) if siren_flash == 0 else (30, 140, 255, 50)
        pygame.draw.circle(glow_surf, glow_color, (glow_radius, glow_radius), glow_radius)
        surface.blit(glow_surf, (int(self.x) - glow_radius, int(self.y) - glow_radius))

        # 5. Nhãn loại xe phía trên
        label_text = "BV 115" if self.type == "AMBULANCE" else "PCCC"
        font_xs = fonts["tiny"]
        lbl_surf = font_xs.render(label_text, True, (255, 255, 255))
        lbl_bg = pygame.Rect(int(self.x) - lbl_surf.get_width() // 2 - 3, int(self.y) - 22, lbl_surf.get_width() + 6, 14)
        pygame.draw.rect(surface, (10, 15, 25), lbl_bg, border_radius=2)
        pygame.draw.rect(surface, (255, 200, 0), lbl_bg, 1, border_radius=2)
        surface.blit(lbl_surf, (lbl_bg.x + 3, lbl_bg.y + 1))

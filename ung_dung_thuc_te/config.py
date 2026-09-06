# -*- coding: utf-8 -*-
"""
Module: ung_dung_thuc_te/config.py
Thiết lập hằng số cấu hình, bảng màu Tactical Cyberpunk, độ phân giải và font chữ cho Sa bàn Pygame.
Độ phân giải chuẩn màn hình 720p HD (1280x720): Không bị tràn màn hình trên mọi dòng máy tính.
"""

# Kích thước cửa sổ chuẩn 720p HD (Vừa vặn trên mọi màn hình máy tính)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Phân chia khu vực
MAP_WIDTH = 950
MAP_HEIGHT = 720
HUD_X = 950
HUD_WIDTH = 330
HUD_HEIGHT = 720

# Tần số quét (Frame rate)
FPS = 60

# BẢNG MÀU TACTICAL CYBERPUNK
COLOR_BG = (12, 17, 27)               # Nền đen xanh thẫm
COLOR_PANEL_BG = (18, 24, 38)         # Nền panel HUD
COLOR_PANEL_BORDER = (42, 58, 86)     # Viền panel
COLOR_PANEL_HEADER = (28, 38, 60)

# Sông Sài Gòn & Kênh Nhiêu Lộc - Thị Nghè
COLOR_RIVER = (20, 35, 54)
COLOR_RIVER_EDGE = (32, 58, 88)

# Tuyến đường
COLOR_ROAD_NORMAL = (55, 72, 100)     # Đường 2 chiều thông thoáng
COLOR_ROAD_ONEWAY = (70, 92, 128)     # Đường 1 chiều
COLOR_ROAD_CONGESTED = (225, 75, 45)  # Đường kẹt xe nặng
COLOR_ROAD_BLOCKED = (180, 25, 25)    # Đường bị phong tỏa / sập cầu

# Thuật toán trực quan hóa phân tầng BFS
COLOR_BFS_LEVELS = [
    (255, 60, 60),    # Lớp 0: Tâm điểm sự cố (Đỏ)
    (255, 200, 20),   # Lớp 1: Vàng chanh
    (0, 220, 255),    # Lớp 2: Xanh lam ngọc (Cyan)
    (180, 100, 255),  # Lớp 3: Tím Neon
    (50, 230, 130),   # Lớp 4: Xanh lục bảo
    (255, 120, 200),  # Lớp 5: Hồng phấn Neon
    (255, 140, 40),   # Lớp 6+: Cam rực rỡ
]

COLOR_DIJKSTRA_TRACE = (255, 220, 40) # Tia quét vàng dò đường ngắn nhất
COLOR_SHORTEST_PATH = (0, 240, 190)   # Đường ngắn nhất chốt (Neon Aqua/Teal)
COLOR_MST_EDGE = (255, 170, 0)        # Cáp viễn thông Kruskal (Vàng cam)

# Nút giao
COLOR_NODE_DEFAULT = (110, 130, 165)
COLOR_NODE_UTH = (30, 144, 255)       # Trường UTH (Xanh dương đặc trưng)
COLOR_NODE_HOSPITAL = (0, 210, 125)   # Bệnh viện (Xanh y tế)
COLOR_NODE_FIRE = (255, 100, 20)      # PCCC (Cam cứu hỏa)
COLOR_NODE_LANDMARK = (230, 190, 50)  # Landmark 81 / Điểm nhấn
COLOR_NODE_REMOTE = (140, 160, 190)   # Khu vực vùng sâu vùng xa
COLOR_NODE_ACCIDENT = (255, 40, 40)   # Điểm xảy ra sự cố

# Màu chữ & giao diện
COLOR_TEXT_WHITE = (240, 245, 250)
COLOR_TEXT_MUTED = (130, 150, 180)
COLOR_TEXT_HIGHLIGHT = (255, 215, 0)
COLOR_TEXT_CYAN = (0, 230, 220)
COLOR_TEXT_RED = (255, 80, 80)
COLOR_TEXT_GREEN = (60, 230, 120)

# Trạng thái điều phối
STATE_IDLE = "SẴN SÀNG (IDLE)"
STATE_MENU_OPEN = "CHỌN LOẠI SỰ CỐ"
STATE_BFS_SCAN = "BFS: QUÉT TỪNG TẦNG ĐỒNG TÂM..."
STATE_DIJKSTRA_TRACE = "DIJKSTRA: DÒ ĐƯỜNG CHUẨN CTRR"
STATE_ROUTE_SEARCH = "DÒ ĐƯỜNG TỪ TRUNG TÂM ĐẾN HIỆN TRƯỜNG"
STATE_PATH_LOCKED = "DIJKSTRA: ĐÃ CHỐT LỘ TRÌNH TỐI ƯU!"
STATE_DISPATCHING = "ĐIỀU XE ĐẾN HIỆN TRƯỜNG"
STATE_RESOLVED = "ĐÃ TIẾP CẬN HIỆN TRƯỜNG"

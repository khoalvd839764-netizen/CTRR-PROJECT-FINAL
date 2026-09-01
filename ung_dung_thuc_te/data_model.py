"""
Module: ung_dung_thuc_te/data_model.py
Mục đích: Định nghĩa toàn bộ mô hình dữ liệu căn hộ thực tế phục vụ Robot Hút Bụi Thông Minh.
Bao gồm:
  1. 25 Đỉnh (Nodes) phân bổ tại 5 phòng và hành lang (kèm phân vùng sàn Khô / Ướt).
  2. 36 Cung (Edges) kết nối lối đi thực tế (chiều dài mét và dung lượng luồng bụi).
  3. Tọa độ thực tế né vật cản 100% (Obstacle-Free Coordinates).
  4. Bảng độ cong Bézier chống đè nét (Anti-overlapping Curvatures).
  5. Mô hình nội thất 3D (Solid 3D Furniture Blocks) và mặt sàn 5 phòng.
"""

# =============================================================================
# 1. DỮ LIỆU 25 ĐỈNH (NODES) CĂN HỘ THỰC TẾ
# =============================================================================
# Mỗi đỉnh đại diện cho một vị trí quét bụi chiến lược trong nhà:
# - name: Tên mô tả vị trí thực tế
# - room: Tên phòng chứa đỉnh (DOCK, LIVING, KITCHEN, CORRIDOR, MASTER, KIDS, BALCONY)
# - zone: Phân vùng sàn (DRY: Sàn gỗ/gạch khô, WET: Sàn nước/ban công/bếp)
# - dust: Khối lượng bụi tích tụ ban đầu (gam)
HOUSE_NODES_DATA = {
    # Khu vực Sảnh & Trạm Sạc (Foyer & Dock)
    0: {"name": "Dock Sạc Base", "room": "DOCK", "zone": "DRY", "dust": 0},
    1: {"name": "Tủ Giày Foyer", "room": "DOCK", "zone": "DRY", "dust": 30},

    # Khu vực Phòng Khách (Living Room)
    2: {"name": "Sofa Trái", "room": "LIVING", "zone": "DRY", "dust": 60},
    3: {"name": "Sofa Phải", "room": "LIVING", "zone": "DRY", "dust": 65},
    4: {"name": "Cửa Khách", "room": "LIVING", "zone": "DRY", "dust": 70},
    5: {"name": "Bàn Trà", "room": "LIVING", "zone": "DRY", "dust": 80},

    # Khu vực Phòng Bếp & Bàn Ăn (Kitchen & Dining)
    6: {"name": "Cửa Bếp", "room": "KITCHEN", "zone": "WET", "dust": 90},
    7: {"name": "Bàn Ăn", "room": "KITCHEN", "zone": "WET", "dust": 110},
    8: {"name": "Bồn Rửa", "room": "KITCHEN", "zone": "WET", "dust": 95},
    9: {"name": "Bếp Nấu", "room": "KITCHEN", "zone": "WET", "dust": 120},

    # Khu vực Hành Lang Trung Tâm (Central Corridor)
    10: {"name": "Hành Lang Bắc", "room": "CORRIDOR", "zone": "DRY", "dust": 40},
    11: {"name": "Hành Lang Đông", "room": "CORRIDOR", "zone": "DRY", "dust": 45},
    12: {"name": "Hành Lang Nam", "room": "CORRIDOR", "zone": "DRY", "dust": 50},

    # Khu vực Phòng Ngủ Master (Master Bedroom)
    13: {"name": "Cửa Master", "room": "MASTER", "zone": "DRY", "dust": 55},
    14: {"name": "Giường Lớn", "room": "MASTER", "zone": "DRY", "dust": 50},
    15: {"name": "Bàn Phấn", "room": "MASTER", "zone": "DRY", "dust": 40},
    16: {"name": "Tủ Áo", "room": "MASTER", "zone": "DRY", "dust": 45},

    # Khu vực Phòng Ngủ Trẻ Em (Kids Bedroom)
    17: {"name": "Cửa Trẻ Em", "room": "KIDS", "zone": "DRY", "dust": 65},
    18: {"name": "Bàn Học", "room": "KIDS", "zone": "DRY", "dust": 85},
    19: {"name": "Giường Tầng", "room": "KIDS", "zone": "DRY", "dust": 90},
    20: {"name": "Góc Đồ Chơi", "room": "KIDS", "zone": "DRY", "dust": 130},

    # Khu vực Ban Công & Nhà Vệ Sinh (Balcony & Restroom)
    21: {"name": "Cửa Ban Công", "room": "BALCONY", "zone": "WET", "dust": 100},
    22: {"name": "Cây Cảnh", "room": "BALCONY", "zone": "WET", "dust": 140},
    23: {"name": "Máy Giặt", "room": "BALCONY", "zone": "WET", "dust": 70},
    24: {"name": "Góc WC", "room": "BALCONY", "zone": "WET", "dust": 60}
}


# =============================================================================
# 2. TỌA ĐỘ SÀN 2D NÉ VẬT CẢN 100% (FREE SPACE COORDINATES)
# =============================================================================
# Tọa độ (x, y) trên mặt phẳng mặt bằng căn hộ (kích thước chuẩn 560 x 780 px).
# Tất cả 25 đỉnh đều nằm tại các lối đi thông thoáng, cách xa mép đồ nội thất ít nhất 15-20px.
HOUSE_BASE_COORDS = {
    # Foyer & Dock
    0: (60, 115),    # [0] Dock Sạc Base (Sàn trống trước trạm sạc)
    1: (130, 115),   # [1] Tủ Giày Foyer (Lối đi sảnh vào)

    # Phòng Khách
    2: (200, 130),   # [2] Sofa Trái (Lối đi trước ghế sofa)
    3: (285, 130),   # [3] Sofa Phải (Lối đi trước ghế sofa)
    4: (185, 235),   # [4] Cửa Khách (Sàn thoáng trước cửa ra hành lang)
    5: (290, 235),   # [5] Bàn Trà (Sàn thoáng bên bàn trà)

    # Phòng Bếp
    6: (150, 345),   # [6] Cửa Bếp (Lối vào cửa bếp)
    7: (60, 395),    # [7] Bàn Ăn (Lối đi cạnh bàn ăn)
    8: (60, 510),    # [8] Bồn Rửa (Sàn đứng trước bồn rửa chén)
    9: (150, 510),   # [9] Bếp Nấu (Sàn đứng trước bếp nấu)

    # Hành Lang Trung Tâm
    10: (230, 345),  # [10] Hành Lang Bắc (Giao điểm Khách - Bếp)
    11: (310, 345),  # [11] Hành Lang Đông (Giao điểm Master - Trẻ Em)
    12: (310, 510),  # [12] Hành Lang Nam (Giao điểm Trẻ Em - Ban Công)

    # Phòng Ngủ Master
    13: (380, 115),  # [13] Cửa Master (Lối vào phòng ngủ chính)
    14: (470, 115),  # [14] Giường Lớn (Lối đi cạnh giường ngủ)
    15: (380, 235),  # [15] Bàn Phấn (Sàn trước bàn trang điểm)
    16: (470, 235),  # [16] Tủ Áo (Lối đi trước tủ quần áo)

    # Phòng Trẻ Em
    17: (380, 355),  # [17] Cửa Trẻ Em (Lối vào phòng ngủ trẻ em)
    18: (470, 355),  # [18] Bàn Học (Sàn trước bàn học sinh)
    19: (380, 510),  # [19] Giường Tầng (Lối đi cạnh giường tầng)
    20: (470, 510),  # [20] Góc Đồ Chơi (Thảm chơi trẻ em)

    # Ban Công & WC (Bố cục Vòng Nhẫn Kim Cương - Không Đè Nét)
    21: (180, 675),  # [21] Cửa Ban Công (Lối ra hiên ban công)
    22: (80, 725),   # [22] Cây Cảnh (Sàn hiên trước chậu cây cảnh)
    23: (310, 675),  # [23] Máy Giặt (Sàn trước máy giặt & phơi đồ)
    24: (440, 725)   # [24] Góc WC (Sàn trước cửa phòng vệ sinh)
}


# =============================================================================
# 3. 36 CUNG ĐỒ THỊ CHUẨN XÁC (HOUSE EDGES)
# =============================================================================
# Cấu trúc: (u, v, length_in_meters, capacity_in_grams)
# - u, v: 2 đỉnh kết nối lối đi
# - length: Khoảng cách di chuyển thực tế của Robot (mét)
# - capacity: Dung lượng luồng bụi / khả năng lưu thông (gam/phút)
HOUSE_EDGES = [
    # 1. Khu vực Dock & Foyer (4 cung)
    (0, 1, 2.0, 50),
    (1, 2, 2.5, 60),
    (2, 4, 3.0, 80),
    (4, 0, 4.0, 70),

    # 2. Khu vực Phòng Khách (5 cung)
    (2, 3, 3.0, 80),
    (3, 5, 3.0, 80),
    (5, 4, 3.0, 80),
    (4, 10, 2.5, 90),
    (10, 2, 3.5, 90),

    # 3. Khu vực Phòng Bếp (7 cung)
    (6, 7, 2.5, 90),
    (7, 8, 3.0, 100),
    (8, 9, 2.5, 90),
    (9, 6, 3.0, 80),
    (6, 8, 3.5, 90),
    (6, 10, 2.0, 90),
    (8, 10, 3.5, 90),

    # 4. Khu vực Hành Lang Trung Tâm (3 cung)
    (10, 11, 3.5, 120),
    (11, 12, 3.5, 120),
    (12, 10, 3.5, 120),

    # 5. Khu vực Phòng Ngủ Master (5 cung)
    (13, 14, 2.5, 70),
    (14, 16, 3.0, 70),
    (16, 15, 2.5, 70),
    (11, 13, 2.5, 80),
    (15, 11, 3.0, 80),

    # 6. Khu vực Phòng Trẻ Em (5 cung)
    (17, 18, 2.5, 75),
    (18, 20, 3.0, 75),
    (20, 19, 2.5, 75),
    (12, 17, 2.5, 80),
    (19, 12, 3.0, 80),

    # 7. Khu vực Ban Công & WC (7 cung)
    (21, 22, 3.5, 90),
    (22, 23, 3.0, 70),
    (23, 24, 3.5, 70),
    (24, 21, 4.0, 90),
    (21, 23, 4.0, 90),
    (12, 21, 3.5, 100),
    (23, 12, 4.0, 100)
]


# =============================================================================
# 4. ĐỘ CONG BÉZIER CHỐNG ĐÈ NÉT (ANTI-OVERLAPPING CURVATURES)
# =============================================================================
# Độ lệch pháp tuyến (pixel) để uốn cong các cung song song hoặc giao nhau:
# - Giá trị dương (+): Uốn cong sang phải của vector hướng
# - Giá trị âm (-): Uốn cong sang trái của vector hướng
EDGE_CURVATURE = {
    # Lối đi Cửa Khách & Foyer
    (4, 10): 22,
    (2, 10): -22,
    (0, 4): -18,
    (2, 4): 16,
    (4, 5): 14,

    # Lối đi Khu Bếp & Bàn Ăn
    (6, 10): 18,
    (8, 10): -24,
    (6, 8): 18,
    (9, 6): -14,

    # Hành Lang Trung Tâm
    (12, 10): 16,

    # Phòng Ngủ Master
    (11, 13): 18,
    (11, 15): -18,
    (14, 16): 14,

    # Phòng Trẻ Em
    (12, 17): 18,
    (12, 19): -18,
    (18, 20): 14,

    # Ban Công & WC
    (12, 21): 20,
    (12, 23): -20,
    (21, 23): 18,
    (22, 23): -18,
    (21, 24): 26
}


# =============================================================================
# 5. MÔ HÌNH MẶT SÀN & NỘI THẤT 3D (ARCHITECTURAL 3D BLOCKS)
# =============================================================================
# Cấu trúc phòng: (x, y, width, depth, label, floor_color, grid_color)
ROOMS_LAYOUT_3D = [
    (20, 50, 310, 240, "🛋️ PHÒNG KHÁCH (LIVING)", (23, 37, 84, 50), (30, 58, 138, 40)),
    (20, 310, 170, 310, "🍳 BẾP & ĂN (KITCHEN)", (69, 26, 3, 45), (146, 64, 14, 35)),
    (350, 50, 190, 240, "🛏️ PN MASTER (BEDROOM)", (59, 7, 100, 45), (107, 33, 168, 35)),
    (350, 310, 190, 310, "🧸 TRẺ EM (KIDS ROOM)", (30, 41, 59, 50), (71, 85, 105, 35)),
    (20, 640, 520, 120, "🌿 BAN CÔNG & WC (BALCONY)", (6, 78, 59, 45), (4, 120, 87, 35))
]

# Danh sách các khối hộp 3D nội thất kiến trúc (kê sát tường, không cản lối đi đồ thị)
FURNITURE_3D_BLOCKS = [
    # 1. Khu Sảnh Foyer & Dock Sạc
    {"x": 45, "y": 55, "z": 0, "w": 30, "d": 25, "h": 8, "top": (14, 165, 233), "sx": (2, 132, 199), "sy": (3, 105, 161)},
    {"x": 115, "y": 55, "z": 0, "w": 35, "d": 25, "h": 22, "top": (100, 116, 139), "sx": (71, 85, 105), "sy": (51, 65, 85)},

    # 2. Khu Phòng Khách
    {"x": 235, "y": 55, "z": 0, "w": 85, "d": 20, "h": 26, "top": (37, 99, 235), "sx": (29, 78, 216), "sy": (30, 64, 175)},
    {"x": 235, "y": 75, "z": 0, "w": 85, "d": 35, "h": 14, "top": (59, 130, 246), "sx": (37, 99, 235), "sy": (29, 78, 216)},
    {"x": 235, "y": 175, "z": 0, "w": 35, "d": 30, "h": 12, "top": (217, 119, 6), "sx": (180, 83, 9), "sy": (146, 64, 14)},
    {"x": 25, "y": 165, "z": 0, "w": 20, "d": 55, "h": 12, "top": (30, 41, 59), "sx": (15, 23, 42), "sy": (15, 23, 42)},
    {"x": 27, "y": 170, "z": 12, "w": 5, "d": 45, "h": 24, "top": (14, 165, 233), "sx": (2, 132, 199), "sy": (3, 105, 161)},

    # 3. Khu Bếp & Bàn Ăn
    {"x": 25, "y": 315, "z": 0, "w": 35, "d": 35, "h": 46, "top": (148, 163, 184), "sx": (100, 116, 139), "sy": (71, 85, 105)},
    {"x": 25, "y": 390, "z": 0, "w": 50, "d": 55, "h": 18, "top": (180, 83, 9), "sx": (146, 64, 14), "sy": (120, 53, 15)},
    {"x": 25, "y": 555, "z": 0, "w": 140, "d": 45, "h": 20, "top": (100, 116, 139), "sx": (71, 85, 105), "sy": (51, 65, 85)},
    {"x": 60, "y": 560, "z": 20, "w": 28, "d": 22, "h": 2, "top": (226, 232, 240), "sx": (203, 213, 225), "sy": (148, 163, 184)},
    {"x": 120, "y": 560, "z": 20, "w": 26, "d": 22, "h": 2, "top": (239, 68, 68), "sx": (185, 28, 28), "sy": (153, 27, 27)},

    # 4. Khu Phòng Ngủ Master
    {"x": 435, "y": 55, "z": 0, "w": 90, "d": 16, "h": 32, "top": (107, 33, 168), "sx": (88, 28, 135), "sy": (59, 7, 100)},
    {"x": 440, "y": 71, "z": 0, "w": 80, "d": 65, "h": 16, "top": (248, 250, 252), "sx": (203, 213, 225), "sy": (148, 163, 184)},
    {"x": 490, "y": 175, "z": 0, "w": 40, "d": 95, "h": 44, "top": (63, 63, 70), "sx": (39, 39, 42), "sy": (24, 24, 27)},
    {"x": 360, "y": 55, "z": 0, "w": 40, "d": 25, "h": 18, "top": (147, 51, 234), "sx": (126, 34, 206), "sy": (107, 33, 168)},

    # 5. Khu Phòng Trẻ Em
    {"x": 455, "y": 320, "z": 0, "w": 70, "d": 42, "h": 18, "top": (14, 165, 233), "sx": (2, 132, 199), "sy": (3, 105, 161)},
    {"x": 480, "y": 475, "z": 0, "w": 50, "d": 110, "h": 32, "top": (59, 130, 246), "sx": (37, 99, 235), "sy": (29, 78, 216)},
    {"x": 360, "y": 555, "z": 0, "w": 40, "d": 40, "h": 14, "top": (245, 158, 11), "sx": (217, 119, 6), "sy": (180, 83, 9)},

    # 6. Khu Ban Công & WC
    {"x": 35, "y": 650, "z": 0, "w": 30, "d": 30, "h": 26, "top": (16, 185, 129), "sx": (5, 150, 105), "sy": (4, 120, 87)},
    {"x": 290, "y": 705, "z": 0, "w": 40, "d": 38, "h": 26, "top": (226, 232, 240), "sx": (203, 213, 225), "sy": (148, 163, 184)},
    {"x": 485, "y": 705, "z": 0, "w": 35, "d": 38, "h": 22, "top": (248, 250, 252), "sx": (203, 213, 225), "sy": (148, 163, 184)}
]

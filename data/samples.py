# ==============================================================================
# BỘ DỮ LIỆU ĐỒ THỊ MẪU CHÍNH THỨC (SAMPLE GRAPHS)
# ==============================================================================

# TỌA ĐỘ BỐ CỤC KHÔNG GIAN 20 ĐỈNH (MẠNG LƯỚI ĐA TẦNG PHI ĐỐI XỨNG - ORGANIC MESH)
# Thiết kế đảm bảo 0 va chạm cạnh xuyên đỉnh (0 collinear collisions), các cạnh phân tán độc lập
POS_20 = {
    0: (-16.0, 5.0),  1: (-16.0, -5.0),
    2: (-10.5, 12.0), 3: (-10.0, 4.0),  4: (-10.0, -4.0),  5: (-10.5, -12.0),
    6: (-3.5, 14.5),  7: (-3.0, 6.5),   8: (-3.0, -1.5),   9: (-3.0, -8.5),  10: (-3.5, -15.0),
    11: (4.0, 13.5),  12: (4.0, 5.5),   13: (4.0, -2.5),   14: (4.0, -9.5),  15: (4.0, -15.5),
    16: (11.0, 9.5),  17: (11.0, 1.0),  18: (11.0, -8.0),
    19: (17.0, 0.0)
}

# 1. BÀI MẪU 1: ĐỒ THỊ VÔ HƯỚNG 20 ĐỈNH (MẠNG LƯỚI ĐA TẦNG PHI ĐỐI XỨNG - 47 CẠNH ĐỘC LẬP)
GRAPH_UNDIRECTED_20 = { 
    "n": 20,
    "directed": False,
    "pos": POS_20,
    "edges": [
        # Cột 1 (0, 1) và tuyến nối Cột 1 -> Cột 2
        (0, 1, 4), (0, 2, 6), (0, 3, 3), (0, 4, 7),
        (1, 3, 6), (1, 4, 3), (1, 5, 5),

        # Cột 2 nội bộ
        (2, 3, 4), (3, 4, 5), (4, 5, 4),

        # Tuyến nối Cột 2 -> Cột 3
        (2, 6, 5), (2, 7, 6), (3, 7, 3), (3, 8, 4),
        (4, 8, 5), (4, 9, 3), (5, 9, 6), (5, 10, 4),

        # Cột 3 nội bộ
        (6, 7, 3), (7, 8, 4), (8, 9, 4), (9, 10, 3),

        # Tuyến nối Cột 3 -> Cột 4
        (6, 11, 4), (7, 11, 6), (7, 12, 3), (8, 12, 4),
        (8, 13, 3), (9, 13, 5), (9, 14, 3), (10, 14, 6), (10, 15, 4),

        # Cột 4 nội bộ
        (11, 12, 3), (12, 13, 4), (13, 14, 3), (14, 15, 4),

        # Tuyến nối Cột 4 -> Cột 5
        (11, 16, 5), (12, 16, 4), (12, 17, 3), (13, 17, 4),
        (13, 18, 5), (14, 18, 4), (15, 18, 6),

        # Cột 5 nội bộ
        (16, 17, 3), (17, 18, 4),

        # Tuyến nối Cột 5 -> Cột 6 (Đích 19)
        (16, 19, 5), (17, 19, 3), (18, 19, 4)
    ]
}
GRAPH_UNDIRECTED_15 = GRAPH_UNDIRECTED_20  # Alias tương thích ngược

# 2. BÀI MẪU 2: ĐỒ THỊ CÓ HƯỚNG 20 ĐỈNH (MẠNG PHỨC HỢP ĐA TUYẾN - 46 CUNG ĐỘC LẬP)
GRAPH_DIRECTED_20 = {
    "n": 20,
    "directed": True,
    "pos": POS_20,
    "edges": [
        # Tuyến luồng từ Cột 1 -> Cột 2
        (0, 1, 4), (0, 2, 5), (0, 3, 3), (0, 4, 6), (1, 4, 3), (1, 5, 5),

        # Cột 2 điều phối
        (2, 3, 3), (4, 3, 3), (4, 5, 3),

        # Tuyến chuyển tiếp Cột 2 -> Cột 3
        (2, 6, 4), (3, 7, 3), (4, 8, 4), (5, 10, 4),

        # Cột 3 liên kết
        (6, 7, 3), (7, 8, 3), (9, 8, 3), (9, 10, 3),

        # Chu trình hồi lưu cục bộ Cột 3 -> Cột 2 (tạo độ phức tạp cao, cung độc lập không đè nét)
        (7, 2, 5), (9, 4, 4), (10, 4, 5),

        # Tuyến chuyển tiếp Cột 3 -> Cột 4
        (6, 11, 4), (7, 12, 3), (8, 13, 3), (9, 14, 3), (10, 15, 4),

        # Cột 4 liên kết
        (11, 12, 3), (12, 13, 3), (14, 13, 3), (14, 15, 3),

        # Chu trình hồi lưu cục bộ Cột 4 -> Cột 3
        (11, 7, 5), (12, 8, 4), (13, 9, 4), (15, 9, 5),

        # Tuyến chuyển tiếp Cột 4 -> Cột 5
        (11, 16, 4), (12, 17, 3), (13, 17, 4), (14, 18, 3), (15, 18, 5),

        # Cột 5 liên kết
        (16, 17, 3), (18, 17, 3),

        # Tuyến lùi đường vòng Cột 5 -> Cột 4 / Cột 3 (độ phức tạp cao cho thuật toán đường đi ngắn nhất)
        (16, 12, 5), (17, 8, 5), (18, 13, 4),

        # Tuyến hội tụ Cột 5 -> Cột 6 (Đích 19)
        (16, 19, 4), (17, 19, 3), (18, 19, 4)
    ]
}
GRAPH_DIRECTED_30 = GRAPH_DIRECTED_20  # Alias tương thích ngược

# 3. ĐỒ THỊ MẪU KIỂM TRA 2 PHÍA (BIPARTITE C4)
GRAPH_BIPARTITE = {
    "n": 4,
    "directed": False,
    "edges": [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 0, 1)]
}

# 4. ĐỒ THỊ MẪU KHÔNG 2 PHÍA (TAM GIÁC C3)
GRAPH_NOT_BIPARTITE = {
    "n": 3,
    "directed": False,
    "edges": [(0, 1, 1), (1, 2, 1), (2, 0, 1)]
}

# 5. ĐỒ THỊ MẪU EULER (ĐỒ THỊ NGÔI NHÀ - CÓ ĐƯỜNG ĐI EULER)
GRAPH_EULER_HOUSE = {
    "n": 5,
    "directed": False,
    "edges": [
        (0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1), (2, 4, 1), (3, 4, 1)
    ]
}

# 6. ĐỒ THỊ MẪU CHU TRÌNH EULER (C5 + SAO 5 CÁNH)
GRAPH_EULER_CIRCUIT = {
    "n": 5,
    "directed": False,
    "edges": [
        (0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 0, 1),
        (0, 2, 1), (2, 4, 1), (4, 1, 1), (1, 3, 1), (3, 0, 1)
    ]
}

# 7. ĐỒ THỊ MẪU CÂY KHUNG NHỎ NHẤT (MST 6 ĐỈNH)
GRAPH_MST_6 = {
    "n": 6,
    "directed": False,
    "edges": [
        (0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5), (2, 3, 8),
        (2, 4, 10), (3, 4, 2), (3, 5, 6), (4, 5, 3)
    ]
}

# 8. MẠNG LUỒNG MẪU FORD-FULKERSON (MAX FLOW 6 ĐỈNH: S=0 -> T=5)
GRAPH_MAX_FLOW_6 = {
    "n": 6,
    "directed": True,
    "source": 0,
    "sink": 5,
    "edges": [
        (0, 1, 16), (0, 2, 13), (1, 2, 10), (1, 3, 12), (2, 1, 4),
        (2, 4, 14), (3, 2, 9), (3, 5, 20), (4, 3, 7), (4, 5, 4)
    ]
}



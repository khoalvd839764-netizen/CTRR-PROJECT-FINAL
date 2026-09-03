# ==============================================================================
# BỘ DỮ LIỆU ĐỒ THỊ MẪU CHÍNH THỨC (SAMPLE GRAPHS)
# ==============================================================================

# 1. BÀI MẪU 1: ĐỒ THỊ VÔ HƯỚNG 20 ĐỈNH (BỐ CỤC 3 TẦNG ĐỒNG TÂM - 38 CẠNH)
GRAPH_UNDIRECTED_20 = { 
    "n": 20,
    "directed": False,
    "edges": [
        # Tầng 1: Vòng ngoài cùng 10 đỉnh (0 -> 9: 10 cạnh)
        (0, 1, 3), (1, 2, 4), (2, 3, 2), (3, 4, 5), (4, 5, 3),
        (5, 6, 6), (6, 7, 4), (7, 8, 5), (8, 9, 3), (9, 0, 4),

        # Tuyến nan hoa nối Tầng 1 <-> Tầng 2 (10 cạnh hướng kính)
        (0, 10, 4), (1, 10, 3), (2, 11, 5), (3, 11, 2), (4, 12, 6),
        (5, 13, 3), (6, 13, 5), (7, 14, 4), (8, 14, 3), (9, 15, 5),

        # Tầng 2: Vòng giữa 6 đỉnh (10 -> 15: 6 cạnh)
        (10, 11, 3), (11, 12, 4), (12, 13, 2), (13, 14, 5), (14, 15, 3), (15, 10, 4),

        # Tuyến nan hoa nối Tầng 2 <-> Tầng 3 (6 cạnh hướng kính)
        (10, 16, 3), (11, 17, 4), (12, 17, 2), (13, 18, 5), (14, 18, 3), (15, 19, 4),

        # Tầng 3: Cụm Lõi trung tâm 4 đỉnh (16 -> 19: 4 cạnh vòng + 2 cạnh chéo)
        (16, 17, 2), (17, 18, 3), (18, 19, 2), (19, 16, 4),
        (16, 18, 5), (17, 19, 4)
    ]
}
GRAPH_UNDIRECTED_15 = GRAPH_UNDIRECTED_20  # Alias tương thích ngược

# 2. BÀI MẪU 2: ĐỒ THỊ CÓ HƯỚNG 20 ĐỈNH (BỐ CỤC 3 TẦNG ĐÔ THỊ - 42 CUNG)
GRAPH_DIRECTED_20 = {
    "n": 20,
    "directed": True,
    "edges": [
        # Tầng 1: Vòng ngoài (Đỉnh 0 -> 9: 10 cung theo chiều kim đồng hồ)
        (0, 1, 3), (1, 2, 4), (2, 3, 2), (3, 4, 5), (4, 5, 3),
        (5, 6, 4), (6, 7, 5), (7, 8, 2), (8, 9, 4), (9, 0, 3),

        # Tuyến 1 chiều từ Tầng 1 -> Tầng 2 (Đỉnh 10 -> 15: 8 cung hướng tâm)
        (0, 10, 4), (1, 10, 3), (2, 11, 5), (4, 12, 2),
        (5, 13, 4), (7, 14, 3), (8, 14, 5), (9, 15, 4),

        # Tầng 2: Vòng giữa (Đỉnh 10 -> 15: 6 cung theo chiều kim đồng hồ)
        (10, 11, 3), (11, 12, 4), (12, 13, 2), (13, 14, 5), (14, 15, 3), (15, 10, 4),

        # Tuyến 1 chiều từ Tầng 2 -> Tầng 3 (Cụm Lõi Trung Tâm 16 -> 19: 6 cung hướng tâm)
        (10, 16, 3), (11, 17, 4), (12, 17, 2), (13, 18, 5), (14, 18, 3), (15, 19, 4),

        # Tầng 3: Lõi trung tâm (Đỉnh 16 -> 19: 4 cung khép kín + 2 cung chéo)
        (16, 17, 2), (17, 18, 3), (18, 19, 2), (19, 16, 4),
        (16, 18, 3), (17, 19, 2),

        # Tuyến thoát ly từ Lõi / Vòng giữa ra Vành đai ngoài (6 cung tránh nghẽn)
        (16, 0, 5), (17, 3, 6), (18, 6, 4), (19, 9, 5),
        (11, 2, 4), (14, 7, 3)
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



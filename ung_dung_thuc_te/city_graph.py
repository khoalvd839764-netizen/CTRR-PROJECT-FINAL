# -*- coding: utf-8 -*-
"""
Module: ung_dung_thuc_te/city_graph.py
Định nghĩa Mô hình Đồ thị Sa bàn Giao thông Khu vực UTH & Quận Bình Thạnh, TP.HCM.
Bao gồm 37 Nút giao (V) và 72 Tuyến đường huyết mạch (E).
Tọa độ được tối ưu chuẩn xác cho khung hiển thị 1280x720 (Map 950x720, HUD 330x720).
"""
import math
from core.graph import Graph

# Danh mục 37 Đỉnh (Nodes) - Tọa độ rescaled chuẩn cho 950x720
CITY_NODES = {
    0: {
        "id": 0, "code": "UTH", "name": "ĐH GTVT CS1 (Võ Oanh - D2)",
        "pos": (542, 429), "type": "UTH", "desc": "Trường ĐH Giao Thông Vận Tải TP.HCM"
    },
    1: {
        "id": 1, "code": "FTU2", "name": "ĐH Ngoại Thương CS2 (D5)",
        "pos": (627, 366), "type": "LANDMARK", "desc": "ĐH Ngoại Thương Cơ Sở 2"
    },
    2: {
        "id": 2, "code": "UVK_D2", "name": "Ngã 3 Ung Văn Khiêm - D2",
        "pos": (542, 327), "type": "INTERSECTION", "desc": "Điểm đen ngập nước & kẹt xe giờ cao điểm"
    },
    3: {
        "id": 3, "code": "UVK_D5", "name": "Ngã 3 Ung Văn Khiêm - D5",
        "pos": (635, 274), "type": "INTERSECTION", "desc": "Cửa ngõ ra sông Sài Gòn"
    },
    4: {
        "id": 4, "code": "VO_DBP", "name": "Giao lộ Võ Oanh - Điện Biên Phủ",
        "pos": (542, 529), "type": "INTERSECTION", "desc": "Nối trục trường học ra Đại lộ Điện Biên Phủ"
    },
    5: {
        "id": 5, "code": "HXANH", "name": "Vòng Xoay Hàng Xanh",
        "pos": (389, 529), "type": "TRANSIT", "desc": "Cửa ngõ huyết mạch Đông Bắc thành phố"
    },
    6: {
        "id": 6, "code": "LM81", "name": "Landmark 81 / Vinhomes",
        "pos": (712, 552), "type": "LANDMARK", "desc": "Tòa tháp cao nhất Việt Nam - Central Park"
    },
    7: {
        "id": 7, "code": "CSAIGON", "name": "Nút Chân Cầu Sài Gòn",
        "pos": (703, 475), "type": "TRANSIT", "desc": "Trục vượt sông sang TP. Thủ Đức"
    },
    8: {
        "id": 8, "code": "BV_VINMEC", "name": "BV Đa Khoa Quốc Tế Vinmec",
        "pos": (763, 614), "type": "HOSPITAL", "desc": "Bệnh viện ĐKQT hiện đại bờ sông Sài Gòn",
        "fleet": 2, "busy": 0
    },
    9: {
        "id": 9, "code": "TANCANG", "name": "Khu Đô Thị Tân Cảng",
        "pos": (627, 591), "type": "INTERSECTION", "desc": "Cửa ngõ vào Vinhomes & Cầu Sài Gòn"
    },
    10: {
        "id": 10, "code": "CTHINGHE", "name": "Cầu Thị Nghè (Sang Q.1)",
        "pos": (295, 668), "type": "TRANSIT", "desc": "Kết nối Thảo Cầm Viên Q.1 sang Bình Thạnh"
    },
    11: {
        "id": 11, "code": "NHCANH", "name": "Ngã 3 Nguyễn Hữu Cảnh - Ngô Tất Tố",
        "pos": (482, 645), "type": "INTERSECTION", "desc": "Trục 'rốn ngập' ven sông Sài Gòn"
    },
    12: {
        "id": 12, "code": "UBND_BT", "name": "UBND Quận Bình Thạnh",
        "pos": (261, 506), "type": "LANDMARK", "desc": "Trung tâm hành chính công Quận Bình Thạnh"
    },
    13: {
        "id": 13, "code": "BACHIEU", "name": "Chợ Bà Chiểu / Lăng Ông",
        "pos": (210, 443), "type": "LANDMARK", "desc": "Trung tâm thương mại truyền thống lâu đời"
    },
    14: {
        "id": 14, "code": "BD_DBL", "name": "Ngã Tư Bạch Đằng - Đinh Bộ Lĩnh",
        "pos": (363, 429), "type": "INTERSECTION", "desc": "Giao lộ trọng điểm phân luồng ngập úng"
    },
    15: {
        "id": 15, "code": "BXMD", "name": "Bến Xe Miền Đông Cũ",
        "pos": (457, 258), "type": "TRANSIT", "desc": "Cửa ngõ xe khách Quốc Lộ 13"
    },
    16: {
        "id": 16, "code": "CBTRIEU", "name": "Nút Chân Cầu Bình Triệu",
        "pos": (457, 158), "type": "TRANSIT", "desc": "Vượt sông Sài Gòn sang Hiệp Bình Chánh"
    },
    17: {
        "id": 17, "code": "CSGT_HX", "name": "Chốt CSGT Hàng Xanh",
        "pos": (389, 606), "type": "TRANSIT", "desc": "Chốt điều tiết phân luồng giao thông Hàng Xanh"
    },
    18: {
        "id": 18, "code": "PCCC_BT", "name": "Đội PCCC & CNCH CA Bình Thạnh",
        "pos": (83, 397), "type": "FIRE", "desc": "Sở chỉ huy PCCC trung tâm quận Bình Thạnh",
        "fleet": 3, "busy": 0
    },
    19: {
        "id": 19, "code": "BV_GIADINH", "name": "Bệnh Viện Nhân Dân Gia Định",
        "pos": (36, 323), "type": "HOSPITAL", "desc": "Bệnh viện tuyến cuối cấp cứu lớn nhất quận",
        "fleet": 3, "busy": 0
    },
    20: {
        "id": 20, "code": "CS_UNGBUOU", "name": "Cơ Sở Y Tế Nơ Trang Long",
        "pos": (126, 333), "type": "LANDMARK", "desc": "Khu liên cơ y tế chuyên khoa Nơ Trang Long"
    },
    21: {
        "id": 21, "code": "NTL_PDL", "name": "Ngã Tư Nơ Trang Long - Phan Đăng Lưu",
        "pos": (83, 258), "type": "INTERSECTION", "desc": "Giao cắt trục y tế lớn của thành phố"
    },
    22: {
        "id": 22, "code": "LQD_BD", "name": "Ngã Tư Lê Quang Định - Bạch Đằng",
        "pos": (159, 374), "type": "INTERSECTION", "desc": "Cửa ngõ từ Gò Vấp sang Bình Thạnh"
    },
    23: {
        "id": 23, "code": "NXI_DBL", "name": "Ngã Tư Nguyễn Xí - Đinh Bộ Lĩnh",
        "pos": (372, 327), "type": "INTERSECTION", "desc": "Trục kết nối BX Miền Đông sang Nơ Trang Long"
    },
    24: {
        "id": 24, "code": "NXI_NTL", "name": "Ngã Tư Nguyễn Xí - Nơ Trang Long",
        "pos": (236, 250), "type": "INTERSECTION", "desc": "Cầu Đỏ & cụm dân cư Nguyễn Xí"
    },
    25: {
        "id": 25, "code": "CHUVANAN", "name": "Khu Đô Thị Chu Văn An",
        "pos": (270, 336), "type": "INTERSECTION", "desc": "Khu dân cư đông đúc & Học viện Cán Bộ"
    },
    26: {
        "id": 26, "code": "PVT_NTL", "name": "Ngã 3 Phan Văn Trị - Nơ Trang Long",
        "pos": (151, 188), "type": "INTERSECTION", "desc": "Đường huyết mạch nối Gò Vấp - Bình Thạnh"
    },
    27: {
        "id": 27, "code": "PVD_NTL", "name": "Nút Phạm Văn Đồng - Nơ Trang Long",
        "pos": (151, 119), "type": "TRANSIT", "desc": "Đại lộ nội đô đẹp nhất TP.HCM"
    },
    28: {
        "id": 28, "code": "PVD_BLO", "name": "Phạm Văn Đồng - Chân Cầu Bình Lợi",
        "pos": (304, 119), "type": "TRANSIT", "desc": "Cầu đường bộ vượt sông sang Thủ Đức"
    },
    29: {
        "id": 29, "code": "CAUKINH", "name": "Cầu Kinh (Cửa Ngõ Thanh Đa)",
        "pos": (729, 266), "type": "TRANSIT", "desc": "Cây cầu độc đạo kết nối bán đảo Thanh Đa"
    },
    30: {
        "id": 30, "code": "BINHQUOI", "name": "Bán Đảo Du Lịch Bình Quới",
        "pos": (797, 211), "type": "LANDMARK", "desc": "Vùng sinh thái sông nước bán đảo"
    },
    31: {
        "id": 31, "code": "CDBP", "name": "Cầu Điện Biên Phủ (Ranh Q.1)",
        "pos": (210, 614), "type": "TRANSIT", "desc": "Cầu vượt Kênh Nhiêu Lộc sang Quận 1"
    },
    32: {
        "id": 32, "code": "BQ1", "name": "KDL Bình Quới 1 (Vùng Sâu Bán Đảo)",
        "pos": (831, 258), "type": "REMOTE", "desc": "Khu nghỉ dưỡng sâu trong bán đảo, cách xa BV/PCCC"
    },
    33: {
        "id": 33, "code": "BQ2", "name": "KDL Bình Quới 2 (Mũi Bán Đảo Xa Nhất)",
        "pos": (890, 181), "type": "REMOTE", "desc": "Mũi cực đông bán đảo, cần 4-5 tầng BFS mới tiếp cận"
    },
    34: {
        "id": 34, "code": "BENDO", "name": "Bến Đò Bình Quới (Cực Đông Bắc)",
        "pos": (882, 104), "type": "REMOTE", "desc": "Bến đò vượt sông sang Linh Đông, Thủ Đức"
    },
    35: {
        "id": 35, "code": "DAMTHUY", "name": "Khu Sinh Thái Đầm Thủy Khắc",
        "pos": (780, 119), "type": "REMOTE", "desc": "Vùng đầm lầy ao sen cách biệt sâu trong Thanh Đa"
    },
    36: {
        "id": 36, "code": "HIEPBINH", "name": "KDC Hiệp Bình Chánh (Bắc Cầu B.Triệu)",
        "pos": (457, 88), "type": "REMOTE", "desc": "Vùng ngoại vi bờ bắc sông Sài Gòn"
    },
    37: {
        "id": 37, "code": "D1_DBP", "name": "Ngã 3 Nguyễn Văn Thương (D1) - ĐBP",
        "pos": (600, 498), "type": "INTERSECTION", "desc": "Cửa ngõ D1 sầm uất song song D2 ra Điện Biên Phủ"
    },
    38: {
        "id": 38, "code": "D1_UVK", "name": "Ngã 3 Nguyễn Văn Thương (D1) - Ung Văn Khiêm",
        "pos": (590, 309), "type": "INTERSECTION", "desc": "Nối trục D1 ra Ung Văn Khiêm song song D2"
    },
    39: {
        "id": 39, "code": "BUIDINHTUY", "name": "Ngã 4 Bùi Đình Túy - Chu Văn An",
        "pos": (285, 295), "type": "INTERSECTION", "desc": "Trục xuyên tâm đông đúc nối Bạch Đằng và Nơ Trang Long"
    },
    40: {
        "id": 40, "code": "BDT_LQD", "name": "Ngã 3 Bùi Đình Túy - Lê Quang Định",
        "pos": (205, 309), "type": "INTERSECTION", "desc": "Cửa ngõ Bùi Đình Túy phía Chợ Bà Chiểu"
    },
    41: {
        "id": 41, "code": "NGCUUVAN", "name": "Ngã 3 Nguyễn Cửu Vân - Điện Biên Phủ",
        "pos": (330, 571), "type": "INTERSECTION", "desc": "Trục đường tắt né kẹt xe giữa Hàng Xanh và Thị Nghè"
    },
    42: {
        "id": 42, "code": "PHVIETCHANH", "name": "Phố Ẩm Thực Phạm Viết Chánh (Thị Nghè)",
        "pos": (370, 650), "type": "LANDMARK", "desc": "Khu ẩm thực & kết nối cầu Thị Nghè sang Nguyễn Hữu Cảnh"
    },
    43: {
        "id": 43, "code": "CX_THANHDA", "name": "Cư Xá Thanh Đa (Bờ Bán Đảo)",
        "pos": (692, 331), "type": "LANDMARK", "desc": "Khu dân cư lâu đời ven bờ sông Thanh Đa"
    },
    44: {
        "id": 44, "code": "BEN_THANHDA", "name": "Bến Waterbus Thanh Đa",
        "pos": (785, 345), "type": "TRANSIT", "desc": "Bến buýt đường sông kết nối Bán đảo và KDL Bình Quới"
    }
}

# Danh mục Tuyến đường (Cạnh / Cung)
CITY_EDGES = [
    # --- KHU VỰC ĐẠI HỌC GIAO THÔNG VẬN TẢI (UTH - D2) ---
    (0, 4, 350, False, "Đường Võ Oanh (D2 Nam)"),
    (0, 2, 380, False, "Đường Võ Oanh (D2 Bắc)"),
    (0, 1, 300, False, "Đường D3 - D5"),
    (1, 3, 350, False, "Đường D5 (Đoạn FTU ra sông)"),
    (2, 3, 420, False, "Đường Ung Văn Khiêm (Đoạn 1)"),
    (3, 29, 450, False, "Đường Ung Văn Khiêm (Ra Cầu Kinh)"),
    (2, 15, 520, False, "Đường Ung Văn Khiêm (Về BX Miền Đông)"),
    (4, 7, 650, False, "Đại lộ Điện Biên Phủ (Hướng Cầu Sài Gòn)"),
    (4, 5, 500, False, "Đại lộ Điện Biên Phủ (Hướng Hàng Xanh)"),
    (0, 9, 700, False, "Đường Ven Sông Sài Gòn"),

    # --- TRỤC ĐIỆN BIÊN PHỦ & CẦU SÀI GÒN & LANDMARK 81 ---
    (7, 6, 400, False, "Đường Nguyễn Hữu Cảnh (Đoạn Landmark 81)"),
    (6, 8, 300, False, "Đường Nội Bộ Vinhomes -> BV Vinmec"),
    (6, 9, 320, False, "Trục Cửa Ngõ Tân Cảng"),
    (9, 11, 480, False, "Đường Nguyễn Hữu Cảnh (Đoạn Tân Cảng)"),
    (11, 10, 600, False, "Đường Nguyễn Hữu Cảnh (Về Cầu Thị Nghè)"),
    (5, 4, 500, False, "Đại lộ Điện Biên Phủ"),
    (5, 31, 750, False, "Đại lộ Điện Biên Phủ (Về Cầu ĐBP Q1)"),
    (31, 10, 450, False, "Đường Hoàng Sa bờ kè Nhiêu Lộc"),

    # --- KHU VỰC HÀNG XANH & ĐINH BỘ LĨNH & BẠCH ĐẰNG ---
    (5, 10, 650, True, "Đường Xô Viết Nghệ Tĩnh (1 CHIỀU vào Q1)"),
    (5, 17, 250, False, "Trục Xô Viết Nghệ Tĩnh -> PCCC Hàng Xanh"),
    (17, 11, 450, False, "Hẻm Liên Phường Hàng Xanh - Ngô Tất Tố"),
    (5, 14, 400, False, "Đường Xô Viết Nghệ Tĩnh (Đoạn Đài Liệt Sĩ)"),
    
    (14, 23, 420, True, "Đường Đinh Bộ Lĩnh (1 CHIỀU lên Bắc)"),
    (23, 15, 380, True, "Đường Đinh Bộ Lĩnh (1 CHIỀU ra BXMD)"),
    (15, 16, 450, True, "Quốc Lộ 13 (1 CHIỀU ra Cầu Bình Triệu)"),
    
    (13, 22, 280, False, "Đường Phan Đăng Lưu (Chợ Bà Chiểu)"),
    (22, 14, 600, True, "Đường Bạch Đằng (1 CHIỀU về Hàng Xanh)"),
    (14, 5, 400, True, "Đường Bạch Đằng (1 CHIỀU nhập Vòng Xoay Hàng Xanh)"),
    
    (5, 12, 550, False, "Đường Vũ Tùng nối Hàng Xanh - BV Bình Thạnh"),
    (12, 13, 300, False, "Đường Vũ Tùng - Chợ Bà Chiểu"),
    (12, 10, 650, False, "Đường Phan Văn Hân"),

    # --- KHU Y TẾ TRỌNG ĐIỂM: GIA ĐỊNH - UNG BƯỚU - PCCC BÌNH THẠNH ---
    (18, 19, 320, False, "Phan Đăng Lưu (PCCC -> BV Gia Định)"),
    (19, 20, 150, False, "Nơ Trang Long (BV Gia Định <-> BV Ung Bướu)"),
    (18, 21, 350, False, "Phan Đăng Lưu (Đoạn PCCC -> Ngã tư NTL)"),
    (20, 21, 220, False, "Nơ Trang Long (BV Ung Bướu -> Ngã tư NTL)"),
    (21, 13, 400, False, "Phan Đăng Lưu (Ngã tư NTL -> Chợ Bà Chiểu)"),
    (21, 24, 450, False, "Đường Nơ Trang Long (Đoạn Cầu Đỏ)"),
    (24, 26, 420, False, "Đường Nơ Trang Long (Đoạn Phan Văn Trị)"),
    (26, 27, 450, False, "Đường Nơ Trang Long (Ra Phạm Văn Đồng)"),
    (22, 26, 650, False, "Đường Phan Văn Trị"),
    (22, 18, 400, False, "Đường Lê Quang Định"),

    # --- KHU VỰC NGUYỄN XÍ - CHU VĂN AN - BẾN XE MIỀN ĐÔNG ---
    (23, 24, 520, False, "Đường Nguyễn Xí"),
    (23, 25, 360, False, "Đường Chu Văn An (Nhánh Đông)"),
    (25, 24, 400, False, "Đường Chu Văn An (Nhánh Bắc)"),
    (25, 14, 420, False, "Đường Chu Văn An (Nhánh Nam về Bạch Đằng)"),
    (24, 15, 550, False, "Đường Đinh Bộ Lĩnh nhánh phụ"),

    # --- TRỤC ĐẠI LỘ VÀNH ĐAI PHẠM VĂN ĐỒNG & CẦU VƯỢT SÔNG ---
    (27, 28, 600, False, "Đại lộ Phạm Văn Đồng (Đoạn 1)"),
    (28, 16, 550, False, "Đại lộ Phạm Văn Đồng (Đoạn Cầu Bình Lợi)"),
    (16, 28, 550, False, "Nhánh quay đầu Chân Cầu Bình Triệu"),
    (28, 23, 800, False, "Đường Nguyễn Xí kéo dài ra Phạm Văn Đồng"),

    # --- BÁN ĐẢO THANH ĐA & BÌNH QUỚI ---
    (29, 30, 850, False, "Đường Bình Quới (Trục cửa ngõ Bán Đảo)"),
    (29, 15, 850, False, "Đường Xô Viết Nghệ Tĩnh (Đoạn Cầu Kinh -> BXMD)"),

    # --- CÁC TUYẾN KẾT NỐI VÙNG SÂU VÙNG XA (REMOTE NETWORK) ---
    (30, 32, 700, False, "Đường Bình Quới nhánh KDL 1"),
    (32, 33, 650, False, "Đường đê bao Mũi Bán Đảo BQ2"),
    (33, 34, 550, False, "Đường ven sông ra Bến Đò"),
    (34, 35, 600, False, "Đường nội bộ Đầm Thủy Khắc"),
    (35, 30, 500, False, "Nhánh liên khu bán đảo về trục chính"),
    (16, 36, 600, False, "Quốc Lộ 13 vượt sông sang Hiệp Bình Chánh"),
    (28, 36, 750, False, "Nhánh Vành đai ven sông Hiệp Bình Chánh"),

    # --- MỞ RỘNG MẠNG LƯỚI ĐA TUYẾN DÒ ĐƯỜNG (EXPANDED ROUTES) ---
    # 1. Trục D1 (Nguyễn Văn Thương) song song D2 (Võ Oanh)
    (37, 38, 380, False, "Đường Nguyễn Văn Thương (D1)"),
    (4, 37, 320, False, "Điện Biên Phủ (Đoạn Võ Oanh -> D1)"),
    (37, 7, 450, False, "Điện Biên Phủ (Đoạn D1 -> Cầu Sài Gòn)"),
    (2, 38, 260, False, "Ung Văn Khiêm (Đoạn D2 -> D1)"),
    (38, 3, 270, False, "Ung Văn Khiêm (Đoạn D1 -> D5)"),
    (0, 37, 340, False, "Hẻm 48 Võ Oanh thông sang D1"),
    (0, 38, 330, False, "Hẻm nội bộ sinh viên UTH sang D1"),
    (1, 38, 280, False, "Đường D5 nối D1"),
    (9, 37, 390, False, "Đường Tân Cảng nối sang Nguyễn Văn Thương"),

    # 2. Trục Bùi Đình Túy & Chu Văn An xuyên tâm
    (40, 39, 360, False, "Đường Bùi Đình Túy (Đoạn Cầu Bùi Đình Túy)"),
    (40, 22, 280, False, "Bùi Đình Túy nối Lê Quang Định"),
    (40, 13, 310, False, "Bùi Đình Túy về Chợ Bà Chiểu"),
    (39, 25, 230, False, "Đường Bùi Đình Túy cắt Chu Văn An"),
    (39, 24, 370, False, "Đường Bùi Đình Túy nối Nơ Trang Long"),
    (39, 14, 420, False, "Hẻm liên cư Bùi Đình Túy ra Bạch Đằng"),
    (18, 40, 350, False, "Phan Đăng Lưu rẽ vào Bùi Đình Túy"),
    (25, 12, 480, False, "Chu Văn An nối UBND Quận Bình Thạnh"),
    (23, 38, 650, False, "Đường Đinh Bộ Lĩnh nối Ung Văn Khiêm D1"),

    # 3. Trục Nguyễn Cửu Vân & Phạm Viết Chánh né kẹt Hàng Xanh
    (5, 41, 350, False, "Đường Nguyễn Cửu Vân (Đầu Hàng Xanh)"),
    (41, 31, 370, False, "Nguyễn Cửu Vân nối Cầu Điện Biên Phủ"),
    (41, 42, 360, False, "Đường Nguyễn Cửu Vân nối Phạm Viết Chánh"),
    (17, 41, 290, False, "Hẻm CSGT Hàng Xanh ra Nguyễn Cửu Vân"),
    (42, 10, 330, False, "Phạm Viết Chánh nối Cầu Thị Nghè"),
    (42, 11, 370, False, "Phạm Viết Chánh ra Nguyễn Hữu Cảnh"),
    (12, 41, 460, False, "Đường Huỳnh Mẫn Đạt nối Nguyễn Cửu Vân"),

    # 4. Trục Bán đảo Thanh Đa & Bến Waterbus đường sông
    (29, 43, 390, False, "Đường Thanh Đa (Đoạn Cư Xá)"),
    (43, 44, 330, False, "Đường ven sông ra Bến Waterbus"),
    (44, 30, 470, False, "Trục Bán Đảo Thanh Đa nối KDL Bình Quới"),
    (43, 3, 440, False, "Tuyến đò ngang qua sông D5 sang Thanh Đa"),
    (44, 32, 520, False, "Đường ven sông Thanh Đa nối Bình Quới 1"),

    # 5. Các nhánh liên thông khác khu vực Cầu Đỏ, Phan Văn Trị, Tân Cảng
    (4, 9, 480, False, "Đường ven rạch Văn Thánh nối ĐBP và Tân Cảng"),
    (7, 0, 580, False, "Hẻm nhánh Chân Cầu Sài Gòn rẽ vào UTH"),
    (2, 23, 510, False, "Đường nhánh Ung Văn Khiêm sang Nguyễn Xí"),
    (20, 26, 430, False, "Đường liên viện Ung Bướu sang Phan Văn Trị"),
    (28, 24, 620, False, "Đường ven rạch Lăng nối Cầu Đỏ - Bình Lợi"),
]


class CityTrafficGraph:
    """Lớp bọc dữ liệu Đồ thị Thành phố, tích hợp sẵn các thuật toán CTRR core."""
    def __init__(self):
        self.nodes = CITY_NODES
        self.raw_edges = CITY_EDGES
        self.n = len(CITY_NODES)
        
        self.congestion = {}
        self.graph_edges = []
        for e in self.raw_edges:
            u, v, w, directed, name = e
            self.graph_edges.append((u, v, float(w)))
            self.congestion[(u, v)] = 1.0
            if not directed:
                self.graph_edges.append((v, u, float(w)))
                self.congestion[(v, u)] = 1.0

        self.core_graph = Graph(n=self.n, directed=True, weighted=True).from_edges(self.graph_edges, n=self.n)

    def get_effective_weight(self, u, v):
        """Tính trọng số thực tế có tính tới hệ số kẹt xe thời gian thực."""
        c = self.congestion.get((u, v), 1.0)
        if c == float('inf'):
            return float('inf')
        
        base_w = 1.0
        for edge in self.raw_edges:
            if (edge[0] == u and edge[1] == v) or (not edge[3] and edge[0] == v and edge[1] == u):
                base_w = edge[2]
                break
        return base_w * c

    def get_dynamic_adj(self):
        """Tạo danh sách kề động adj có trọng số thay đổi theo kẹt xe."""
        dyn_adj = {i: [] for i in range(self.n)}
        for (u, v), cong in self.congestion.items():
            if cong != float('inf'):
                w = self.get_effective_weight(u, v)
                dyn_adj[u].append((v, w))
        return dyn_adj

    def toggle_congestion(self, u, v):
        """Chuyển đổi trạng thái đường: Thông thoáng (1.0) -> Kẹt nặng (3.5) -> Khóa đường (inf) -> Thông thoáng."""
        curr = self.congestion.get((u, v), 1.0)
        if curr == 1.0:
            new_val = 3.5
        elif curr == 3.5:
            new_val = float('inf')
        else:
            new_val = 1.0
            
        self.congestion[(u, v)] = new_val
        for edge in self.raw_edges:
            if not edge[3] and ((edge[0] == u and edge[1] == v) or (edge[0] == v and edge[1] == u)):
                self.congestion[(v, u)] = new_val
        return new_val

    def reset_congestion(self):
        """Khôi phục lại toàn bộ đường sá về trạng thái thông thoáng."""
        for k in self.congestion:
            self.congestion[k] = 1.0

    def reset_fleet(self):
        """Khôi phục lại số xe tại các trạm y tế và PCCC."""
        for n_id, data in self.nodes.items():
            if "busy" in data:
                data["busy"] = 0

    def get_edge_name(self, u, v):
        """Lấy tên đường chính thức giữa hai nút u và v."""
        for edge in self.raw_edges:
            if (edge[0] == u and edge[1] == v) or (not edge[3] and edge[0] == v and edge[1] == u):
                return edge[4]
        return f"Đoạn {self.nodes.get(u, {}).get('code', u)} - {self.nodes.get(v, {}).get('code', v)}"

    def get_edge_distance(self, u, v):
        """Lấy cự ly danh định ban đầu (mét) giữa u và v."""
        for edge in self.raw_edges:
            if (edge[0] == u and edge[1] == v) or (not edge[3] and edge[0] == v and edge[1] == u):
                return edge[2]
        return 0


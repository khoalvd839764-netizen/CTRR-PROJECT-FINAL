# MỤC LỤC BÁO CÁO ĐỒ ÁN CTRR
**ĐỀ TÀI: HỆ THỐNG GIẢI TOÁN ĐỒ THỊ TOÀN DIỆN VÀ ỨNG DỤNG THỰC TẾ ROBOT HÚT BỤI THÔNG MINH**

---

### PHẦN MỞ ĐẦU
- **LỜI CẢM ƠN** .............................................................................................................. Trang i
- **NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN** ............................................................. Trang ii
- **MỤC LỤC** ................................................................................................................... Trang iii
- **DANH MỤC CÁC KÝ HIỆU VÀ TỪ VIẾT TẮT** ........................................................... Trang v
- **DANH MỤC HÌNH VẼ** ................................................................................................. Trang vi
- **DANH MỤC BẢNG BIỂU** ............................................................................................. Trang vii

---

### CHƯƠNG 1: TỔNG QUAN & KIẾN THỨC CHUYÊN NGÀNH
- **1.1. CÁC KHÁI NIỆM CỐT LÕI CÓ TRONG DỰ ÁN** ................................................... Trang 1
  - 1.1.1. Khái niệm và các dạng đồ thị (Vô hướng, có hướng, trọng số) .......................... Trang 1
  - 1.1.2. Ba phương pháp biểu diễn đồ thị (Ma trận kề, Danh sách kề, Cạnh) .................. Trang 3
  - 1.1.3. Tổng quan 7 bài toán lý thuyết đồ thị được giải quyết ......................................... Trang 5
    - *a. Duyệt đồ thị (BFS & DFS)* ................................................................................. Trang 5
    - *b. Đồ thị hai phía (Bipartite Graph & Chu trình lẻ)* ................................................... Trang 7
    - *c. Đường đi ngắn nhất (Dijkstra & Bellman-Ford)* .................................................... Trang 9
    - *d. Đường đi và Chu trình Euler (Fleury & Hierholzer)* ............................................... Trang 12
    - *e. Cây khung nhỏ nhất MST (Kruskal & Prim)* ......................................................... Trang 15
    - *f. Luồng cực đại & Lát cắt hẹp nhất (Ford-Fulkerson & Min-Cut)* .............................. Trang 18
- **1.2. MÔI TRƯỜNG, CÔNG NGHỆ VÀ THƯ VIỆN SỬ DỤNG** ....................................... Trang 21
  - 1.2.1. Ngôn ngữ lập trình Python 3 .............................................................................. Trang 21
  - 1.2.2. Thư viện trực quan hóa Matplotlib và NetworkX ................................................. Trang 22
  - 1.2.3. Thư viện mô phỏng tương tác thời gian thực Pygame .......................................... Trang 23
- **1.3. PHẠM VI GIẢI BÀI TOÁN THỰC TẾ** ..................................................................... Trang 24

---

### CHƯƠNG 2: THIẾT KẾ DỰ ÁN & TỐI ƯU HÓA HỆ THỐNG
- **2.1. KIẾN TRÚC PHÂN TẦNG CỦA HỆ THỐNG (MODULAR ARCHITECTURE)** ........... Trang 26
  - 2.1.1. Mô hình phân tầng luồng dữ liệu ........................................................................ Trang 26
  - 2.1.2. Thiết kế lớp dữ liệu Graph và bộ chuyển đổi Converter ...................................... Trang 28
  - 2.1.3. Thiết kế giao diện điều khiển dòng lệnh (CLI Application) .................................... Trang 31
- **2.2. CÁC KỸ THUẬT VÀ GIẢI THUẬT TỐI ƯU MÃ NGUỒN** ....................................... Trang 33
  - 2.2.1. Tối ưu lọc trùng lặp cạnh đối xứng vô hướng với điều kiện `u <= v` ................... Trang 33
  - 2.2.2. Giải thuật Tổ tiên chung gần nhất (LCA) trích xuất chính xác Chu trình lẻ vi phạm .. Trang 35
  - 2.2.3. Tối ưu hóa bộ nhớ: Tái sử dụng BFS với cơ chế cờ `record_trace=False` .......... Trang 38
  - 2.2.4. Cấu trúc dữ liệu Disjoint Set Union (DSU) nén đường đi trong thuật toán Kruskal ... Trang 41
- **2.3. MODULE TRỰC QUAN HÓA (VISUALIZER)** ........................................................... Trang 44
  - 2.3.1. Thuật toán bố cục vật lý lực lò xo (Force-directed / Spring Layout) .................... Trang 44
  - 2.3.2. Cơ chế ghi nhận từng bước duyệt và trích xuất hoạt ảnh động (.GIF) ................. Trang 47

---

### CHƯƠNG 3: ỨNG DỤNG THỰC TẾ — MÔ PHỎNG ROBOT HÚT BỤI THÔNG MINH
- **3.1. BỐI CẢNH BÀI TOÁN THỰC TẾ** ........................................................................... Trang 50
  - 3.1.1. Mô hình không gian sa bàn căn hộ thông minh .................................................. Trang 50
  - 3.1.2. Ánh xạ bản đồ dạng lưới (Grid Map) sang mô hình Đồ thị trọng số ..................... Trang 52
- **3.2. THUẬT TOÁN ỨNG DỤNG VÀ TÁC DỤNG ĐỐI VỚI HÀNH VI ROBOT** ................. Trang 54
  - 3.2.1. Tìm đường tối ưu né vật cản về trạm sạc (Dijkstra / Bellman-Ford) ...................... Trang 54
  - 3.2.2. Quét sạch mọi hành lang không trùng lặp với thuật toán Euler ........................... Trang 57
  - 3.2.3. Tối ưu hóa mạng lưới dây nối giữa các dock sạc với Cây khung nhỏ nhất MST .... Trang 60
  - 3.2.4. Khám phá và lập bản đồ không gian phòng mới với BFS/DFS ............................. Trang 62
- **3.3. Ý NGHĨA THỰC TIỄN CỦA ĐỀ TÀI** ........................................................................ Trang 64

---

### CHƯƠNG 4: THỰC NGHIỆM, KẾT LUẬN & TỔNG KẾT
- **4.1. SO SÁNH KẾT QUẢ GIẢI TAY VÀ CHẠY MÁY** ..................................................... Trang 66
  - 4.1.1. Đối chiếu Bảng ma trận bước lặp thuật toán Dijkstra (20 đỉnh) ............................ Trang 66
  - 4.1.2. Đối chiếu thứ tự chọn cạnh và tổng trọng số Cây khung Kruskal (MST = 53) ..... Trang 69
  - 4.1.3. Đối chiếu kiểm tra đồ thị hai phía và chu trình lẻ vi phạm (Tam giác 0-1-10) ........ Trang 72
  - 4.1.4. Đánh giá bộ kiểm thử tự động toàn diện (Unit Test Suite PASS 100%) ................ Trang 74
- **4.2. KẾT QUẢ ĐẠT ĐƯỢC CỦA DỰ ÁN** ........................................................................ Trang 76
- **4.3. HẠN CHẾ VÀ HƯỚNG PHÁT TRIỂN** ..................................................................... Trang 78
  - 4.3.1. Những hạn chế còn tồn tại ................................................................................ Trang 78
  - 4.3.2. Hướng nghiên cứu và mở rộng đề tài ................................................................ Trang 79

---

### PHẦN KẾT THÚC
- **TÀI LIỆU THAM KHẢO** ................................................................................................. Trang 81
- **PHỤ LỤC: HƯỚNG DẪN KHỞI CHẠY VÀ SỬ DỤNG HỆ THỐNG** ............................... Trang 83

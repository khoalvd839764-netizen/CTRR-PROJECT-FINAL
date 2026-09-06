# 🎓 ĐỒ ÁN MÔN HỌC: CẤU TRÚC RỜI RẠC & LÝ THUYẾT ĐỒ THỊ
## HỆ THỐNG GIẢI TOÁN ĐỒ THỊ TOÀN DIỆN & MÔ PHỎNG ĐIỀU PHỐI GIAO THÔNG ĐÔ THỊ THÔNG MINH
> **Trường Đại học Giao thông vận tải TP.HCM (UTH)**  
> **Khoa Công Nghệ Thông Tin**  
> **Giảng viên hướng dẫn:** Thầy Tăng Lê Ngọc Gia Huy  
> **Điểm khởi chạy duy nhất:** `python main.py`

---

## 🌟 LỜI CẢM ƠN
Trong suốt quá trình học tập môn Cấu trúc rời rạc, được sự giảng dạy và hướng dẫn tận tình của **thầy Tăng Lê Ngọc Gia Huy**, nhóm chúng em đã tiếp thu được nền tảng kiến thức vững chắc về Lý thuyết đồ thị và hoàn thành xuất sắc đồ án cuối kỳ này.

Nhóm xin chân thành cảm ơn Thầy đã tạo điều kiện thuận lợi, định hướng phương pháp tư duy toán học rời rạc và ứng dụng thực tiễn để nhóm có thể hoàn thiện đề tài một cách trọn vẹn nhất!

---

## 📌 TỔNG QUAN DỰ ÁN

Dự án được xây dựng với mục tiêu kép:
1. **Bộ công cụ Thuật toán Đồ thị chuẩn mực (Core Library - 100% tự viết, không phụ thuộc networkx):**
   - Đầy đủ các thuật toán nền tảng: Duyệt đồ thị (BFS, DFS), Kiểm tra đồ thị 2 phía (Bipartite 2-coloring), Tìm đường đi ngắn nhất (Dijkstra, Bellman-Ford với phát hiện chu trình âm), Chu trình Euler (Fleury, Hierholzer), Cây khung nhỏ nhất MST (Prim, Kruskal kèm cấu trúc Disjoint Set Union nén đường đi), Luồng cực đại & Lát cắt hẹp nhất (Ford-Fulkerson / Edmonds-Karp).
   - Tự động sinh **bảng vết từng bước (trace table)** chi tiết, khớp 100% với phương pháp giải tay trên giấy của sinh viên, kèm trực quan hóa và xuất file ảnh kết quả độ phân giải cao (`matplotlib`).
2. **Ứng dụng Thực tế Đột phá (Real-world Simulation Engine - Pygame GUI):**
   - **Sa bàn Mạng lưới Giao thông Đô thị Thông minh (Smart City Traffic Grid):** Sa bàn 16 nút giao trọng điểm, 27 tuyến huyết mạch hai chiều/một chiều.
   - **Trung tâm Điều phối Cứu hộ Khẩn cấp (Emergency Dispatch):** Tích hợp BFS tìm trạm gần nhất (PCCC, Cấp cứu 115, CSGT) và Dijkstra dẫn đường theo ma trận trọng số kẹt xe thay đổi theo thời gian thực ($W = L \times [1.0 + \text{Jam} \times 2.5]$).
   - **Đa lộ trình tối ưu:** Sinh đồng thời 1 Tuyến chính (Main Route) + 2 Tuyến dự phòng (Backup Routes) bằng phương pháp phạt trọng số cạnh (Penalty Method).

---

## 📂 CẤU TRÚC THƯ MỤC DỰ ÁN

```
CTRR-PROJECT-FINAL/
│
├── main.py                     # Điểm khởi chạy duy nhất của toàn bộ dự án
├── requirements.txt            # Thư viện phụ thuộc (matplotlib, pygame, pytest)
├── README.md                   # Báo cáo và tài liệu giới thiệu dự án
│
├── core/                       # 100% THUẬT TOÁN THUẦN (TỰ CÀI ĐẶT TỪ ĐẦU)
│   ├── graph.py                # Class Graph: quản lý ma trận kề, DS kề, DS cạnh
│   ├── converter.py            # 6 hàm chuyển đổi 2 chiều giữa 3 dạng biểu diễn đồ thị
│   ├── traversal.py            # BFS, DFS (sinh thứ tự duyệt, cây khung & bảng vết)
│   ├── bipartite.py            # Kiểm tra đồ thị 2 phía (tô 2 màu & trích xuất chu trình lẻ)
│   ├── shortest_path.py        # Dijkstra & Bellman-Ford (phát hiện chu trình âm, bảng vết)
│   ├── euler.py                # Fleury & Hierholzer (chu trình & đường đi Euler)
│   ├── mst.py                  # Prim & Kruskal (kèm class DSU nén đường đi + rank)
│   └── max_flow.py             # Ford-Fulkerson / Edmonds-Karp (Max Flow & Min-Cut)
│
├── visualizer/                 # CÔNG CỤ TRỰC QUAN HÓA & LƯU ẢNH
│   ├── draw.py                 # Vẽ đồ thị Matplotlib, highlight đường đi, cây khung, lát cắt
│   └── animation.py            # Trích xuất hoạt ảnh từng bước (GIF)
│
├── app/                        # GIAO DIỆN DÒNG LỆNH MENU TƯƠNG TÁC
│   └── cli.py                  # Menu tương tác 10 chức năng chuẩn đề bài
│
├── ung_dung_thuc_te/           # SA BÀN ĐIỀU PHỐI GIAO THÔNG THÔNG MINH (PYGAME GUI)
│   ├── main.py                 # Giao diện sa bàn đồ họa độ phân giải cao
│   ├── city_graph.py           # Dữ liệu 16 nút giao, 27 đại lộ, đường 1 chiều/2 chiều
│   ├── city_data_model.py      # Mô hình trạng thái nút, cạnh, mật độ giao thông
│   ├── dispatcher.py           # BFS tìm trạm cứu hỏa/cấp cứu gần nhất
│   ├── router.py               # Dijkstra trọng số kẹt xe động & 3 tuyến đường thay thế
│   ├── traffic_algorithms.py   # Kruskal phân vùng cứu hộ, Ford-Fulkerson lưu lượng
│   ├── vehicle.py              # Động lực học xe di chuyển mượt mà trên đồ thị
│   ├── hud.py                  # Bảng điều khiển, biểu đồ radar, timeline sự cố
│   └── radial_menu.py          # Menu tròn điều khiển nhanh tại từng nút giao
│
├── data/                       # DỮ LIỆU ĐỒ THỊ MẪU
│   └── samples.py              # Các bộ đồ thị mẫu kinh điển cho từng thuật toán
│
├── tests/                      # BỘ KIỂM THỬ TỰ ĐỘNG (UNIT TESTS)
│   ├── test_foundation.py      # Kiểm thử cấu trúc đồ thị & 6 hàm converter
│   ├── test_euler.py           # Kiểm thử Fleury & Hierholzer
│   ├── test_mst.py             # Kiểm thử Prim, Kruskal & DSU
│   ├── test_max_flow.py        # Kiểm thử Ford-Fulkerson & Min-Cut
│   ├── test_traffic_sim.py     # Kiểm thử thuật toán sa bàn giao thông
│   ├── test_emergency_dispatch.py # Kiểm thử BFS Dispatcher & Dijkstra Router
│   ├── test_robot_storyline.py # Kiểm thử mô hình liên phòng robot hút bụi
│   └── test_pygame_smoke.py    # Kiểm thử không vỡ giao diện Pygame
│
└── results/                    # KẾT QUẢ XUẤT ẢNH & HOẠT ẢNH TỰ ĐỘNG
```

---

## ⚡ 10 CHỨC NĂNG THUẬT TOÁN CỐT LÕI (MENU CHÍNH)

Khi chạy `python main.py`, hệ thống cung cấp Menu tương tác toàn diện:

| Mục | Chức năng | Thuật toán & Đặc tả kỹ thuật |
| :---: | :--- | :--- |
| **1** | **Nhập xuất đồ thị** | Hỗ trợ đồ thị vô hướng, có hướng, có trọng số. Nhập từ ma trận, danh sách cạnh hoặc text file. Tự động vẽ và xuất file ảnh PNG. |
| **2** | **Chuyển đổi biểu diễn** | Chuyển đổi 2 chiều giữa 3 cấu trúc: `Adjacency Matrix` $\leftrightarrow$ `Adjacency List` $\leftrightarrow$ `Edge List`. |
| **3** | **Duyệt đồ thị (BFS & DFS)** | Duyệt theo thứ tự đỉnh ưu tiên tăng dần, sinh cây khung và bảng vết (trace table) từng bước khớp bài giải tay. |
| **4** | **Kiểm tra đồ thị 2 phía** | Sử dụng thuật toán tô 2 màu (2-Coloring BFS). Nếu không thỏa mãn, tự động trích xuất chu trình độ dài lẻ (Odd Cycle) để chứng minh. |
| **5** | **Tìm đường đi ngắn nhất** | **Dijkstra** (trọng số không âm) và **Bellman-Ford** (xử lý trọng số âm, phát hiện chu trình âm). Sinh ma trận bảng vết từng bước lặp. |
| **6** | **Ứng dụng thực tế** | Khởi chạy Sa bàn Giao thông Đô thị Thông minh & Điều phối Cứu hộ Khẩn cấp thời gian thực (Pygame GUI). |
| **7.1** | **Chu trình Euler (Fleury)** | Kiểm tra điều kiện Euler, kiểm tra cạnh cầu (Bridge detection) qua DFS, tìm chu trình/đường đi Euler. |
| **7.2** | **Chu trình Euler (Hierholzer)**| Thuật toán ghép chu trình con tối ưu độ phức tạp $O(E)$, xuất trình tự các bước ghép. |
| **7.3** | **Cây khung nhỏ nhất (Prim)** | Phát triển cây khung từ 1 đỉnh theo nguyên lý lát cắt (Cut Property), tính tổng trọng số nhỏ nhất. |
| **7.4** | **Cây khung nhỏ nhất (Kruskal)**| Sắp xếp cạnh tăng dần, kết hợp cấu trúc `Disjoint Set Union (DSU)` có nén đường đi (Path Compression) và gộp theo hạng (Union by Rank). |
| **7.5** | **Luồng cực đại & Lát cắt hẹp nhất** | Thuật toán **Edmonds-Karp** (BFS tìm đường tăng luồng trên đồ thị phần dư), xác định giá trị Max-Flow và tập đỉnh lát cắt hẹp nhất (Min-Cut $S - T$). |

---

## 🚦 ĐIỂM NHẤN ỨNG DỤNG THỰC TẾ: SA BÀN ĐIỀU PHỐI GIAO THÔNG & CỨU HỘ KHẨN CẤP

Ứng dụng thực tế được thiết kế bám sát 100% kiến thức môn học CTRR với tính chân thực cao:

### 1. Không gian đồ thị $G = (V, E)$:
- **16 Nút giao trọng điểm:** Trạm PCCC Trung tâm, Bệnh viện Đa khoa, Trung tâm TOC, Bến xe Miền Đông, Ngã tư Hàng Xanh, Sân bay Tân Sơn Nhất, Cảng Cát Lái, Hầm Thủ Thiêm...
- **27 Tuyến đại lộ:** Bao gồm các trục xuyên tâm, cầu vượt sông và các tuyến đường 1 chiều thực tế (Điện Biên Phủ, Pasteur, Lạc Long Quân...).

### 2. Thuật toán điều phối thời gian thực:
- **Bước 1 (BFS Dispatcher):** Khi xảy ra sự cố (cháy nổ / tai nạn), thuật toán BFS quét loang từng tầng để xác định ngay trạm cứu hộ/xe cấp cứu có khoảng cách số nút giao ít nhất.
- **Bước 2 (Dynamic Dijkstra Router):** Tính toán lộ trình nhanh nhất dựa trên trọng số biến thiên theo tình trạng ùn tắc thời gian thực:
  $$\text{Weight}(u, v) = \text{Length}(u, v) \times (1.0 + \text{JamLevel} \times 2.5)$$
- **Bước 3 (3 Candidate Routes):** Áp dụng kỹ thuật phạt trọng số cạnh (Penalty Method) để tạo đồng thời **1 Tuyến chính + 2 Tuyến dự phòng độc lập** giúp tài xế linh hoạt chuyển hướng khi gặp sự cố đột xuất.
- **Bước 4 (Kruskal & Max-Flow):** Ứng dụng Kruskal để thiết lập mạng lưới liên lạc xương sống tối thiểu giữa các trạm khẩn cấp và Max-Flow để đánh giá năng lực giải tỏa giao thông đô thị.

---

## 🛠️ HƯỚNG DẪN CÀI ĐẶT & CHẠY CHƯƠNG TRÌNH

### 1. Yêu cầu môi trường:
- Python 3.9 trở lên (đã kiểm thử tương thích tốt trên Python 3.10, 3.11, 3.12, 3.13, 3.14).

### 2. Cài đặt thư viện:
```bash
pip install -r requirements.txt
```

### 3. Khởi chạy chương trình:
- **Cách 1: Chạy Menu chính (Hỗ trợ toàn bộ 10 chức năng):**
  ```bash
  python main.py
  ```
- **Cách 2: Chạy trực tiếp Sa bàn Giao thông Đô thị Thông minh (GUI):**
  ```bash
  python main.py --gui
  # hoặc:
  python main.py --traffic
  ```

### 4. Chạy bộ kiểm thử tự động (Unit Tests):
```bash
pytest
# hoặc:
python -m pytest -v
```
*(Hiện tại 37/37 test cases đều vượt qua thành công 100%).*

---

## 👥 THÀNH VIÊN NHÓM THỰC HIỆN
- Sinh viên Khoa Công Nghệ Thông Tin - Trường Đại học Giao thông vận tải TP.HCM (UTH).
- Đồ án hoàn thành với sự nỗ lực, nghiêm túc và tinh thần đồng đội cao.

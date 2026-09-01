# 🤖 BÁO CÁO MÔ TẢ ỨNG DỤNG THỰC TẾ: ROBOT HÚT BỤI & LAU NHÀ THÔNG MINH (SMART VACUUM ROBOT SIMULATION)

> **Môn học**: Cấu Trúc Rời Rạc (Discrete Mathematics / Graph Theory)  
> **Đề tài**: Vận dụng toàn diện 7 Thuật toán Đồ thị cốt lõi vào Bài toán Điều hướng và Tối ưu hóa Robot Hút Bụi Thông Minh trong Căn hộ Hiện đại.  
> **Framework**: Python 3, Pygame, Matplotlib.  
> **Mã nguồn**: Thư mục [`ung_dung_thuc_te/`](./ung_dung_thuc_te/)  

---

## 📌 I. BỐI CẢNH THỰC TẾ & ĐẶT VẤN ĐỀ

Trong kỷ nguyên nhà thông minh (*Smart Home*), các thiết bị Robot hút bụi lau nhà tự động (như Roborock, Ecovacs, Dreame, Roomba) phải đối mặt với nhiều bài toán tối ưu hóa phức tạp:
1. **Tiết kiệm pin & Năng lượng**: Phải tìm đường ngắn nhất để đưa robot quay về trạm sạc (*Dock*) khi pin yếu.
2. **Quy hoạch mạng lưới di chuyển**: Cần kết nối toàn bộ các điểm trọng yếu trong nhà với tổng chiều dài đường đi là nhỏ nhất.
3. **Lập bản đồ tự động (SLAM)**: Khi vào nhà mới, robot cần quét Lidar theo từng tầng sóng để lập bản đồ địa hình.
4. **Dọn dẹp chân tường & ngóc ngách**: Cần bám sát tường và các góc phòng sâu, tự biết quay lui (*Backtracking*) khi gặp ngõ cụt.
5. **Dọn sạch 100% không lặp đường**: Đi qua toàn bộ các lối đi trong nhà đúng 1 lần duy nhất để tiết kiệm thời gian và chổi quét.
6. **Phân vùng làm việc thông minh**: Tự động nhận diện vùng Sàn Khô (*Dry Zone* - phòng khách, phòng ngủ) để hút bụi và vùng Sàn Ướt (*Wet Zone* - bếp, ban công, toilet) để tự động hạ giẻ lau sàn.
7. **Tối ưu hóa xả bụi & chống nghẽn**: Mạng lưới thu gom bụi từ các phòng dồn về hộp rác trung tâm với dung lượng luồng tối đa mà không gây nghẽn đường ống.

Dự án này đã **mô hình hóa toàn bộ căn hộ thực tế thành Đồ thị Toán học $G=(V, E)$** và áp dụng **đầy đủ 7 Thuật toán Cấu trúc rời rạc** để giải quyết triệt để các bài toán trên.

---

## 🏠 II. MÔ HÌNH HÓA ĐỒ THỊ CĂN HỘ $G = (V, E)$

```
                            [0] DOCK SẠC BASE
                                    |
                            [1] TỦ GIÀY FOYER
                                    |
     [PHÒNG KHÁCH]          [PHÒNG MASTER]          [PHÒNG TRẺ EM]
   (Đỉnh 2, 3, 4, 5)       (Đỉnh 13, 14, 15, 16)   (Đỉnh 17, 18, 19, 20)
           \                       |                       /
            \                      |                      /
             -----> [10] HÀNH LANG BẮC --- [11] HÀNH LANG ĐÔNG <-----
                           |                      |
                           |                      |
                    [PHÒNG BẾP & ĂN]       [12] HÀNH LANG NAM
                    (Đỉnh 6, 7, 8, 9)             |
                           |                      |
                           -------------------> [BAN CÔNG & WC]
                                               (Đỉnh 21, 22, 23, 24)
```

### 1. Tập 25 Đỉnh ($V$ - Waypoints)
Mỗi đỉnh đại diện cho một vị trí quét dọn chiến lược, được đặt tại **vùng không gian thoáng (Free Space)**, cách xa mép vật cản ít nhất 15-20px:
* **Khu vực Sảnh & Trạm sạc (Foyer & Dock)**:
  * `[0] Dock Sạc Base`: Trạm sạc nguồn trung tâm (gốc tọa độ xuất phát).
  * `[1] Tủ Giày Foyer`: Lối vào sảnh chính.
* **Khu vực Phòng Khách (Living Room)**:
  * `[2] Sofa Trái`, `[3] Sofa Phải`, `[4] Cửa Khách`, `[5] Bàn Trà`.
* **Khu vực Phòng Bếp & Bàn Ăn (Kitchen & Dining)**:
  * `[6] Cửa Bếp`, `[7] Bàn Ăn`, `[8] Bồn Rửa`, `[9] Bếp Nấu`.
* **Khu vực Hành Lang Trung Tâm (Corridor Hub)**:
  * `[10] Hành Lang Bắc` (kết nối Khách - Bếp).
  * `[11] Hành Lang Đông` (kết nối Master - Trẻ Em).
  * `[12] Hành Lang Nam` (kết nối Trẻ Em - Ban Công).
* **Khu vực Phòng Ngủ Master (Master Bedroom)**:
  * `[13] Cửa Master`, `[14] Giường Lớn`, `[15] Bàn Phấn`, `[16] Tủ Áo`.
* **Khu vực Phòng Ngủ Trẻ Em (Kids Bedroom)**:
  * `[17] Cửa Trẻ Em`, `[18] Bàn Học`, `[19] Giường Tầng`, `[20] Góc Đồ Chơi`.
* **Khu vực Ban Công & WC (Balcony & Restroom)**:
  * `[21] Cửa Ban Công`, `[22] Cây Cảnh`, `[23] Máy Giặt`, `[24] Góc WC`.

### 2. Tập 36 Cung ($E$ - Lối đi thực tế)
* Mỗi cung $(u, v)$ có trọng số $w(u, v)$ là khoảng cách di chuyển thực tế (mét) và dung lượng $cap(u, v)$ là sức chứa luồng bụi (gam/phút).
* **Độ cong Bézier bậc 2**: Áp dụng vector pháp tuyến uốn cong các cung song song và giao nhau, đảm bảo **100% không bị đè nét, không thẳng hàng che khuất nhau**.
* **Né vật cản 100%**: Mọi cung đường đi đều chạy vòng qua các khoảng trống giữa bàn trà, ghế sofa, tủ lạnh và giường ngủ.

---

## 🧮 III. VẬN DỤNG CHI TIẾT 7 THUẬT TOÁN CẤU TRÚC RỜI RẠC

Toàn bộ 7 thuật toán đều được **tái sử dụng trực tiếp từ thư viện cốt lõi `core/`** (`core.mst`, `core.shortest_path`, `core.traversal`, `core.euler`, `core.bipartite`, `core.max_flow`):

```
+-----------------------------------------------------------------------------------+
|                           HỆ THỐNG 7 THUẬT TOÁN CTRR                              |
+-------------------+--------------------------------+------------------------------+
| Thuật Toán        | Hàm Tái Sử Dụng Từ core/       | Ứng Dụng Thực Tế             |
+-------------------+--------------------------------+------------------------------+
| 1. Kruskal MST    | core.mst.kruskal (DSU)         | Quy hoạch tuyến dây sạc      |
| 2. Dijkstra       | core.shortest_path.dijkstra    | Đường ngắn nhất về Dock sạc  |
| 3. BFS SLAM       | core.traversal.bfs             | Quét Lidar mở rộng bản đồ    |
| 4. DFS Men Tường  | core.traversal.dfs             | Quét sâu góc khuất + Quay lui|
| 5. Euler Circuit  | core.euler.hierholzer          | Dọn sạch 100% cạnh đúng 1 lần|
| 6. Bipartite 2 Phía| core.bipartite.check_bipartite | Phân chia sàn Khô / Ướt      |
| 7. Max Flow & Cut | core.max_flow.ford_fulkerson   | Tối ưu hóa lưu lượng xả bụi  |
+-------------------+--------------------------------+------------------------------+
```

### 1. Thuật toán Kruskal MST (Cây Khung Nhỏ Nhất)
* **Ý nghĩa thực tế**: Quy hoạch mạng lưới đường trục chính liên kết trọn vẹn 25 điểm trong toàn bộ căn hộ sao cho **tổng khoảng cách dây dẫn sạc ngầm là ngắn nhất**.
* **Bản chất toán học**:
  * Sắp xếp 36 cạnh theo thứ tự trọng số tăng dần $w(u, v)$.
  * Sử dụng cấu trúc dữ liệu **Disjoint Set Union (DSU)** với kỹ thuật nén đường đi (*Path Compression*) để kiểm tra xem 2 đỉnh $u, v$ đã cùng một tập hợp liên thông hay chưa.
  * Nếu $find(u) \neq find(v)$, hợp nhất $union(u, v)$ và chọn cạnh vào cây khung. Ngược lại, loại bỏ vì tạo chu trình kín.
* **Kết quả**: Chọn đúng $24$ cạnh kết nối $25$ đỉnh với tổng khoảng cách tối ưu nhất.

### 2. Thuật toán Dijkstra (Tìm Đường Ngắn Nhất Về Sạc)
* **Ý nghĩa thực tế**: Khi robot đang làm việc ở góc xa nhất của căn hộ (`[22] Cây Cảnh Ban Công`) và nhận cảnh báo pin yếu ($< 15\%$), thuật toán sẽ tính toán hành trình ngắn nhất để đưa robot quay về `[0] Dock Sạc Base`.
* **Bản chất toán học**:
  * Khởi tạo mảng khoảng cách $d[start] = 0$, các đỉnh khác bằng $\infty$.
  * Duyệt chọn đỉnh $u$ chưa thăm có $d[u]$ nhỏ nhất, cập nhật nhãn khoảng cách cho các đỉnh kề $v$:
    $$\text{Nếu } d[u] + w(u, v) < d[v] \implies d[v] = d[u] + w(u, v), \quad parent[v] = u$$
* **Kết quả**: Tìm ra đường đi ngắn nhất: `[22] Cây Cảnh` ➔ `[21] Cửa Ban Công` ➔ `[12] Hành Lang Nam` ➔ `[10] Hành Lang Bắc` ➔ `[4] Cửa Khách` ➔ `[0] Dock Sạc`.

### 3. Thuật toán BFS SLAM Map (Khám Phá Bản Đồ Mở Rộng)
* **Ý nghĩa thực tế**: Mô phỏng cảm biến Lidar quay 360° quét phát hiện phòng mới. Sóng cảm biến lan truyền từ trạm sạc ra các phòng lân cận theo từng tầng khoảng cách.
* **Bản chất toán học**:
  * Sử dụng cấu trúc **Hàng đợi FIFO (Queue)**. Đỉnh nào được phát hiện trước sẽ được mở rộng trước.
  * Đảm bảo mọi điểm trong phòng khách được lập bản đồ trước khi tiến sâu vào các phòng ngủ và ban công.

### 4. Thuật toán DFS Men Tường (Dọn Dẹp Góc Khuất & Quay Lui)
* **Ý nghĩa thực tế**: Robot bám sát mép tường để quét sạch bụi ở các góc phòng sâu. Khi đi hết một nhánh ngõ cụt (ví dụ góc tủ áo hoặc gầm giường), robot sẽ thực hiện **quay lui (Backtracking)** về ngã ba trước đó để tìm đường rẽ khác.
* **Bản chất toán học**:
  * Sử dụng giải thuật đệ quy tương đương cấu trúc **Ngăn xếp (Call Stack)**.
  * Tích hợp bước trực quan hóa Backtracking: Robot di chuyển lùi ngược lại đỉnh cha $u$ thay vì dịch chuyển tức thời (*teleport*).

### 5. Chu trình Euler Hierholzer (Quét Sạch 100% Cung Đường Đúng 1 Lần)
* **Ý nghĩa thực tế**: Chế độ "Dọn dẹp tổng thể" (*Deep Clean*). Robot phải đi qua toàn bộ 36 cung đường trong nhà **đúng 1 lần duy nhất**, không bỏ sót đoạn nào và không đi lặp lại đoạn đã quét để tiết kiệm chổi than.
* **Bản chất toán học**:
  * Kiểm tra điều kiện Euler: Toàn bộ 25 đỉnh trong đồ thị đều có **bậc chẵn** ($deg(v) \in \{2, 4, 6\}$).
  * Thuật toán **Hierholzer**: Bắt đầu từ `[0] Dock Sạc`, đi qua từng cạnh và xóa cạnh đã đi khỏi đồ thị, sau đó nối các chu trình con lại thành một chu trình Euler khép kín hoàn chỉnh gồm 36 bước.

### 6. Đồ thị 2 Phía Bipartite (Phân Vùng Sàn Khô / Ướt)
* **Ý nghĩa thực tế**: Robot tự động nhận diện mặt sàn để kích hoạt tính năng:
  * **Tập V1 (Sàn Khô - DRY)**: Phòng Khách, Phòng Ngủ Master, Phòng Trẻ Em $\implies$ Chỉ bật động cơ Hút Bụi, nâng giẻ lau lên để không làm ướt thảm/sàn gỗ.
  * **Tập V2 (Sàn Ướt - WET)**: Bếp, Ban Công, Nhà Vệ Sinh $\implies$ Hạ giẻ lau ướt và tăng công suất bơm nước.
* **Bản chất toán học**:
  * Tô màu 2 tập $0$ và $1$ bằng BFS. Nếu hai đỉnh kề nhau có cùng màu $\implies$ Phát hiện xung đột và trích xuất chu trình lẻ (*Odd Cycle*).

### 7. Luồng Cực Đại Ford-Fulkerson & Lát Cắt Min Cut (Tối Ưu Xả Rác)
* **Ý nghĩa thực tế**: Mạng lưới các họng xả bụi tự động từ các phòng gom về Hộp rác trung tâm (`[22]`). Xác định đoạn ống nghẽn nhất (*Bottleneck / Min Cut*) để cảnh báo người dùng vệ sinh ống dẫn.
* **Bản chất toán học**:
  * Thuật toán **Edmonds-Karp**: Tìm đường tăng luồng từ Nguồn $S=0$ đến Đích $T=22$ bằng BFS.
  * Tìm dung lượng thặng dư nhỏ nhất $\Delta f = \min(c_f(u, v))$, tăng luồng dọc theo đường đi cho đến khi không còn đường tăng luồng.
  * Xác định Lát cắt hẹp nhất $\text{Min Cut} = (S, T)$ có tổng dung lượng bằng đúng giá trị luồng cực đại $\text{Max Flow}$.

---

## 🖥️ IV. GIAO DIỆN ĐA GÓC NHÌN (MULTI-VIEW DASHBOARD 3 CỘT)

Giao diện được xây dựng trên nền tảng **Pygame** với độ phân giải chuẩn $1920 \times 1080$, chia làm 3 cột đồng bộ hóa thời gian thực:

```
+-----------------------------------------------------------------------------------------------------------+
| [1] Kruskal MST | [2] Dijkstra | [3] BFS SLAM | [4] DFS Men Tường | [5] Euler | [6] 2 Phía | [7] Max-Flow |
+------------------------------------+---------------------------------------+------------------------------+
| 🏠 CỘT 1: SA BÀN 3D ISOMETRIC      | 📐 CỘT 2: ĐỒ THỊ TOÁN HỌC G = (V, E)  | 🔍 CỘT 3: BỘ SOI MÃ GIẢ      |
|                                    |                                       |                              |
| - Phối cảnh 3D căn hộ 5 phòng      | - 25 Đỉnh & 36 Cung Bézier cong       | - Pseudocode Highlight dòng  |
| - Nội thất 3D né vật cản 100%      | - Quả cầu năng lượng lướt đồng bộ     | - Live Variables: DSU, Queue,|
| - Robot Roomba phát quang xoay 360°| - Nhãn mét lơ lửng không đè nét       |   Stack, Min-Cut, Khoảng cách|
| - Phím điều khiển: Zoom, Pan, Xoay | - Màu sắc phân biệt Chấp nhận / Loại  | - Nút: [LÙI] [TIẾP] [TỰ ĐỘNG]|
+------------------------------------+---------------------------------------+------------------------------+
```

---

## 🎮 V. HƯỚNG DẪN ĐIỀU KHIỂN & PHÍM TẮT

| Phím Tắt / Thao Tác | Chức Năng |
| :--- | :--- |
| **`Phím Số 1 .. 7`** | Chuyển đổi tức thì giữa 7 Thuật toán CTRR |
| **`Phím Space`** | Bật / Tắt chế độ **Phát Tự Động (Auto-Play)** |
| **`Phím S` hoặc `Mũi tên Phải`** | Tiến **1 Bước** thuật toán (*Step Next*) |
| **`Phím B` hoặc `Mũi tên Trái`** | Lùi **1 Bước** thuật toán (*Step Previous*) |
| **`Phím R`** | **Đặt lại (Reset)** thuật toán về bước 0 ban đầu |
| **`Cuộn Chuột` / Phím `+` `-`** | Phóng to / Thu nhỏ Sa bàn 3D (Zoom 40% đến 300%) |
| **`Phím 0`** | Đặt lại góc nhìn và Zoom chuẩn 95% |
| **`Kéo Chuột Trái`** | Xoay góc nhìn 3D căn hộ 360° (*Orbit Yaw / Pitch*) |
| **`Kéo Chuột Phải`** | Dời vị trí camera 3D (*Pan Camera*) |
| **`Phím V`** | Chuyển đổi qua lại giữa chế độ **3D Isometric** và **2D Mặt bằng** |
| **`Phím F11`** | Bật / Tắt chế độ **Toàn màn hình (Fullscreen)** |

---

## 🚀 VI. HƯỚNG DẪN KHỞI CHẠY CHƯƠNG TRÌNH

Dự án sử dụng file **[`main.py`](file:///home/jackie-khoa/Downloads/course/CTRR%20FINAL%20PROJECT/main.py)** làm điểm khởi chạy duy nhất cho toàn bộ hệ thống:

### 1. Mở Menu CLI Tổng Hợp (Đầy đủ 10 Chức năng)
```bash
python3 main.py
```
*(Tại Menu chính, chọn mục `10` để mở giao diện Robot Hút Bụi, hoặc chọn `1`..`9` để giải các bài toán đồ thị cơ bản & nâng cao)*

### 2. Mở trực tiếp Giao diện Robot Hút Bụi 3D (Khuyên dùng khi thuyết trình)
```bash
python3 main.py --robot
```
*(Hoặc: `python3 main.py --gui`)*

---
*Báo cáo được hoàn thiện chuẩn cấu trúc đồ án Cấu Trúc Rời Rạc.*

# 🤖 BÁO CÁO ĐỒ ÁN: ĐIỀU HƯỚNG & LẬP LỊCH ROBOT HÚT BỤI BẰNG ĐỒ THỊ LIÊN PHÒNG (TOPOLOGICAL ROOM GRAPH)

> **Môn học**: Cấu Trúc Rời Rạc (Discrete Mathematics / Graph Theory - CTRR Final Project)  
> **Đề tài**: Mô hình hóa Căn hộ thành Đồ thị Liên phòng $G=(V, E)$ và Ứng dụng Thuật toán Đồ thị vào Điều hướng, Lập lịch Robot Hút Bụi Thông Minh.  
> **Mã nguồn**: Thư mục [`ung_dung_thuc_te/`](./ung_dung_thuc_te/)  

---

## 📌 I. TẠI SAO MÔ HÌNH NÀY THỰC TẾ 100% VÀ CHUẨN CTRR 100%?

### 1. Phản ánh đúng thực tế của Robot Hút Bụi Thông Minh (Mi Home, Roborock, Ecovacs):
Trong các ứng dụng điều khiển robot hút bụi thương mại ngày nay:
* Bản đồ căn hộ được quản lý ở **cấp độ vĩ mô theo từng PHÒNG chức năng (Room Segmentation)**.
* Các tính năng cốt lõi người dùng thao tác hằng ngày:
  1. **Điều hướng chuyển phòng**: Đang dọn ở Bếp, người dùng chọn sang dọn Phòng Ngủ Master. Robot phải tìm đường ngắn nhất qua các hành lang để đến đúng cửa phòng đích.
  2. **Lập lịch dọn nhiều phòng**: Chọn dọn 4 phòng liên tiếp sao cho tổng quãng đường di chuyển ít nhất, tự động ưu tiên Bếp nhiều dầu mỡ dọn sau cùng để không làm bẩn sàn phòng khách và phòng ngủ.
  3. **Khẩn cấp pin yếu về sạc**: Từ bất kỳ phòng nào, tìm đường ngắn nhất né các cửa phòng đang đóng để phi về Trạm sạc Base.
  4. **Né cửa phòng bị đóng**: Khi lối đi chính bị khóa, robot tự động tìm đường vòng phụ.

---

## 🏠 II. MÔ HÌNH HÓA ĐỒ THỊ TOÁN HỌC $G = (V, E)$

```
                            [0] TRẠM SẠC BASE (DOCK)
                                       │ (2.5m)
                            [1] SẢNH CHÍNH & TỦ GIÀY
                                  /         \
                           (3.0m)/           \(3.5m)
                                /             \
                 [2] PHÒNG KHÁCH ───────── [3] HÀNH LANG BẮC ───────── [4] PHÒNG BẾP & ĂN
                   (Sàn Gỗ 28m²)   (3.5m)      │ (4.0m)       (3.0m)     (Gạch Nhám 18m²)
                                               │                           │
                                               │                           │ (4.5m)
                                      [5] HÀNH LANG ĐÔNG                   │
                                         /            \                    │
                                  (3.0m)/              \(4.0m)             │
                                       /                \                  │
                        [6] NGỦ MASTER ──(4.0m)── [7] NGỦ TRẺ EM           │
                        (Sàn Gỗ Sồi 22m²)         (Thảm Chơi 16m²)         │
                                                       │ (3.0m)            │
                                                       │                   │
                                              [8] HÀNH LANG NAM <──────────┘
                                                       │
                                                       │ (3.5m)
                                                       │
                                              [9] BAN CÔNG & GIẶT
                                                (Đá Hoa Cương 12m²)
```

### 1. Tập 10 Đỉnh ($V$ - Các Phòng & Cửa Ra Vào):
* `[0] Trạm Sạc Base (Dock)`: Vị trí xuất phát và nạp điện 45W.
* `[1] Sảnh Chính & Tủ Giày (Foyer)`: Khu vực tiếp đón, sàn gạch men 8m².
* `[2] Phòng Khách (Living Room)`: Sàn gỗ cao cấp 28m², sofa và bàn trà.
* `[3] Hành Lang Bắc (North Hub)`: Nút giao thông huyết mạch giữa Khách và Bếp.
* `[4] Phòng Bếp & Bàn Ăn (Kitchen)`: Sàn gạch nhám 18m², nhiều dầu mỡ.
* `[5] Hành Lang Đông (East Hub)`: Nút giao thông dẫn vào khu phòng ngủ.
* `[6] Phòng Ngủ Master`: Sàn gỗ sồi 22m², giường lớn và bàn phấn.
* `[7] Phòng Ngủ Trẻ Em (Kids)`: Sàn gỗ & thảm chơi 16m², đồ chơi lego.
* `[8] Hành Lang Nam (South Hub)`: Lối thông ra khu giặt phơi và ban công.
* `[9] Ban Công & Giặt Phơi (Balcony)`: Sàn đá sỏi ngoài trời 12m², máy giặt.

### 2. Tập 13 Cạnh ($E$ - Lối Đi Hành Lang):
* Mỗi cạnh $(u, v)$ có trọng số $w(u, v)$ là khoảng cách di chuyển thực tế (mét) giữa các cửa phòng.
* Ma trận kề $A$ đối xứng cấp 10, danh sách kề chuẩn mực môn Cấu Trúc Rời Rạc.

---

## 🧮 III. 8 CHỨC NĂNG THỰC TẾ KẾT HỢP THUẬT TOÁN ĐỒ THỊ CTRR

```
+-----------------------------------------------------------------------------------------------+
|                            HỆ THỐNG 8 CHỨC NĂNG ĐỒ THỊ LIÊN PHÒNG                             |
+-----+-------------------------------+------------------------------+--------------------------+
| Phím| Chức Năng Trên App            | Thuật Toán CTRR Tái Sử Dụng  | Ý Nghĩa Thực Tế          |
+-----+-------------------------------+------------------------------+--------------------------+
| [1] | Chuyển Phòng Dọn Dẹp          | core.shortest_path.dijkstra  | Tìm đường ngắn nhất qua  |
|     | (Ví dụ: Bếp [4] -> Master [6])|                              | các hành lang thông phòng|
| [2] | Lập Lịch Dọn Đa Phòng         | core.mst.kruskal (DSU)       | Quy hoạch mạng lưới trục |
|     |                               |                              | hành lang cự ly tối thiểu|
| [3] | Pin Yếu Về Sạc Khẩn Cấp       | core.shortest_path.dijkstra  | Pin < 15%, khóa vệt Neon |
|     | (Từ Ban Công [9] về Dock [0]) |                              | phi thẳng về Dock sạc    |
| [4] | Né Cửa Phòng Bị Khóa          | core.shortest_path.dijkstra  | Re-routing tức thời khi  |
|     | (Cửa Hành Lang Đông bị đóng)  | (Đồ thị thặng dư)            | lối đi chính bị chặn     |
| [5] | Khám Phá Danh Sách Phòng SLAM | core.traversal.bfs           | Quét Lidar theo tầng bậc |
|     | (Khi mới unbox đặt tại Dock)  |                              | loang rộng phát hiện phòng|
| [6] | Tuần Tra Sâu & Quay Lui       | core.traversal.dfs           | Đi sâu vào từng phòng, tự|
|     |                               | (Call Stack Backtracking)    | lùi xe khi gặp ngõ cụt   |
| [7] | Kiểm Chứng Cấu Trúc Căn Hộ    | core.bipartite.check_bipartite| Chứng minh phản chứng    |
|     |                               |                              | căn hộ có chu trình lẻ   |
| [8] | Tuần Tra Khử Khuẩn UV Hành Lang| core.euler.hierholzer        | Đi qua toàn bộ hành lang |
|     |                               | (Chinese Postman Augment)    | đúng 1 lần bằng Euler    |
+-----+-------------------------------+------------------------------+--------------------------+
```

---

## 🖥️ IV. GIAO DIỆN SA BÀN MULTI-VIEW 3 CỘT

1. **Cột 1: Sa bàn Căn hộ Phân phòng**:
   - Vẽ rõ 6 khu vực phòng lớn.
   - **Tính năng độc đáo**: Khi Robot hoàn tất chặng đường đến phòng nào, **phòng đó sáng rực đèn màu xanh lá kèm nhãn `[✓ ĐÃ DỌN]`**, mô phỏng chính xác tiến trình làm sạch thực tế!
   - Robot Roomba 3D xoay mượt mà, phát tia quét Lidar 360°.
2. **Cột 2: Đồ thị Toán học $G=(V, E)$**:
   - 10 Đỉnh cửa phòng và 13 Cung hành lang uốn cong Bézier không đè nét.
   - Trọng số mét hiển thị rõ ràng trên từng cung.
   - Vệt sáng Neon xanh lá rực rỡ khi khóa lộ trình Dijkstra.
3. **Cột 3: Bảng Thuyết Minh Kịch Bản & Mã Giả**:
   - Hộp phụ đề tiếng Việt tự động giải thích chi tiết cho sinh viên đọc khi thuyết trình.
   - Mã giả Pseudocode chạy sáng từng dòng.
   - Bảng biến toán học: $d[u]$, `parent`, danh sách phòng đã dọn xong.

---

## 🎤 V. KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN 3 PHÚT

### ⏱️ Phần 1: Mở đầu (30 giây)
> *"Kính thưa quý Thầy Cô, trong thực tế các hãng robot hàng đầu như Roborock hay Mi Home, bản đồ căn hộ được mô hình hóa ở cấp độ vĩ mô thành **Đồ thị Topological các Phòng và Cửa ra vào**. Nhóm đã xây dựng mô hình đồ thị 10 đỉnh đại diện cho các phòng và 13 cung hành lang có trọng số mét thực tế để giải quyết trọn vẹn bài toán điều hướng và lập lịch dọn dẹp:"*

### ⏱️ Phần 2: Trình diễn Demo (2 phút)
> * **Bấm phím 1**: *"Thưa Thầy Cô, khi người dùng yêu cầu robot chuyển từ Phòng Bếp [4] sang dọn Phòng Master [6], thuật toán **Dijkstra** tìm ngay ra hành lang ngắn nhất né các phòng khác với tổng cự ly chỉ 8.5m. Khi robot đến nơi, phòng Master sáng đèn [✓ ĐÃ DỌN]!"*
> * **Bấm phím 2**: *"Để dọn dẹp toàn bộ căn hộ với cự ly di chuyển tối thiểu, thuật toán **Kruskal MST** sử dụng cấu trúc DSU để quy hoạch đúng 9 hành lang trục chính kết nối 10 phòng, loại bỏ hoàn toàn các chu trình đi vòng lặp đường."*
> * **Bấm phím 3**: *"Khi robot đang ở góc xa nhất là Ban công [9] và pin giảm xuống dưới 15%, **Dijkstra** khóa lộ trình Neon khẩn cấp đưa robot phi thẳng về Dock sạc [0] nạp điện 45W."*
> * **Bấm phím 4**: *"Nếu cửa hành lang chính (3, 5) bất ngờ bị đóng, hệ thống tức thời gán trọng số bằng vô cùng và kích hoạt Dijkstra Re-routing tìm đường vòng phụ an toàn."*
> * **Bấm phím 5 & 6**: *"Thuật toán **BFS** quét Lidar loang rộng khám phá danh sách phòng khi mới về nhà mới, còn **DFS** tuần tra sâu từng phòng và tự động quay lui (Backtracking) khi gặp ngõ cụt."*

### ⏱️ Phần 3: Kết luận (30 giây)
> *"Mô hình Đồ thị các Phòng này vừa đáp ứng 100% chuẩn mực toán học của môn Cấu Trúc Rời Rạc, vừa phản ánh chân thực cách các kỹ sư Robotics thiết kế hệ điều hành robot thông minh ngoài đời thực. Em xin cảm ơn Thầy Cô đã lắng nghe!"*

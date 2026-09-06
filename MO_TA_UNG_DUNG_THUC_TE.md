# 🚦 BÁO CÁO ĐỒ ÁN: HỆ THỐNG MÔ PHỎNG & ĐIỀU PHỐI MẠNG LƯỚI GIAO THÔNG ĐÔ THỊ THÔNG MINH
## (SMART CITY TRAFFIC GRID SIMULATOR & REAL-TIME ROUTING ENGINE)

> **Môn học**: Cấu Trúc Rời Rạc & Lý Thuyết Đồ Thị (CTRR)  
> **Khoa**: Công Nghệ Thông Tin  
> **Thành viên thực hiện**: Đỗ Thanh, Tuấn, Linh, Nhật Trường  
> **Giao diện sa bàn**: Pygame High-Resolution GUI (1600x920)  
> **Mã nguồn thực thi**: `python run_traffic_sim.py` hoặc `python main.py` (Mục 10)  

---

## 🌟 I. TẠI SAO ĐỀ TÀI NÀY VỪA THỰC TẾ 100%, VỪA CHUẨN TOÁN RỜI RẠC?

Trong thực tế giao thông của các đô thị lớn (như TP.HCM, Hà Nội), mọi trục đường và ngã tư đều cấu thành **Đồ thị không gian (Spatial Graph)** rõ ràng nhất mà ai cũng nhìn thấy ngoài đời:
1. **Tính trực quan không thể phản biện**: 
   - Ngã tư, vòng xoay, bến xe, bệnh viện chính là **Đỉnh ($V$)**.
   - Tuyến đường, đại lộ, cầu vượt sông, hầm chui chính là **Cạnh ($E$)**.
   - Chiều giao thông (đường 1 chiều / 2 chiều) thể hiện trực tiếp **Đồ thị có hướng (Directed Graph) và Vô hướng (Undirected Graph)**.
2. **Trọng số thay đổi theo thời gian thực (Dynamic Edge Weight)**:
   - Một đoạn đường dài 2 km nếu vắng xe thì đi mất 3 phút. Nhưng vào giờ cao điểm, kẹt xe làm chi phí di chuyển tăng gấp 3-4 lần.
   - Công thức tính trọng số cạnh:
     $$Weight(u, v) = \text{Độ\_dài\_mét} \times (1.0 + \text{Hệ\_số\_kẹt\_xe} \times 2.5)$$
3. **Bám sát 100% giáo trình CTRR (Tuyệt đối không dùng A\*)**:
   - Chỉ sử dụng đúng các thuật toán nền tảng sinh viên học trên lớp: **Dijkstra**, **BFS**, **DFS**, **MST Kruskal**.

---

## 🗺️ II. MÔ HÌNH DỮ LIỆU ĐỒ THỊ THÀNH PHỐ $G = (V, E)$

Hệ thống mô phỏng sa bàn giao thông gồm **16 Nút giao thông trọng điểm** và **27 Tuyến đại lộ huyết mạch**:

### 1. Danh mục 16 Đỉnh ($V$):
| ID | Tên Nút Giao Thông | Mã Code | Chức năng đô thị |
| :---: | :--- | :---: | :--- |
| **0** | **Trạm Cứu Hỏa Trung Tâm** | `PCCC` | Điểm xuất phát xe cứu hỏa, ứng cứu sự cố cháy nổ |
| **1** | **Bệnh Viện Đa Khoa Trung Tâm** | `BVĐK` | Điểm tiếp nhận cấp cứu người bệnh khẩn |
| **2** | **Trung Tâm Điều Hành TOC** | `TOC` | Trung tâm giám sát & điều phối giao thông thông minh toàn thành phố |
| **3** | **Bến Xe Miền Đông Mới** | `BXMD` | Cửa ngõ trung chuyển xe khách liên tỉnh |
| **4** | **Ngã Tư Hàng Xanh** | `HXANH` | Nút giao trọng điểm cửa ngõ phía Đông |
| **5** | **Ngã Tư Phú Nhuận** | `PNHUAN` | Giao điểm kết nối trung tâm với sân bay |
| **6** | **Ngã Tư Bảy Hiền** | `BHIEN` | Nút giao huyết mạch quận Tân Bình |
| **7** | **Nút Giao An Sương** | `ASUONG` | Cửa ngõ Quốc Lộ 22 kết nối Tây Ninh & Campuchia |
| **8** | **Nút Giao Thủ Thiêm** | `TTHIEM` | Trung tâm tài chính mới ven sông Sài Gòn |
| **9** | **Nút Giao Cảng Cát Lái** | `CLAI` | Cảng container có mật độ xe đầu kéo cực lớn |
| **10** | **Ngã Sáu Dân Chủ** | `DCHU` | Vòng xoay kết nối 6 trục đường Quận 3 |
| **11** | **Phố Đi Bộ Nguyễn Huệ** | `NHUE` | Trung tâm tài chính - thương mại Quận 1 |
| **12** | **Nút Giao Cầu Sài Gòn** | `CSAIGON`| Cầu huyết mạch vượt sông Sài Gòn sang TP. Thủ Đức |
| **13** | **Hầm Thủ Thiêm - Võ Văn Kiệt** | `HTHIEM` | Hầm dìm vượt sông và trục đại lộ Đông Tây |
| **14** | **Ngã Tư Chợ Lớn** | `CHOLON` | Trung tâm thương mại sầm uất Quận 5 |
| **15** | **Sân Bay Quốc Tế Tân Sơn Nhất**| `TSNHAT` | Cửa ngõ hàng không quốc tế |

### 2. Danh mục Tuyến đường ($E$):
* **Trục vượt sông**: Cầu Sài Gòn (đoạn 4-12), Cầu Thủ Thiêm 1 (2-8), Hầm Vượt Sông Sài Gòn (13-8), Cầu Thủ Thiêm 4 (8-1).
* **Trục vành đai & xuyên tâm**: Võ Văn Kiệt (14-13-11), Cách Mạng Tháng 8 (6-10), Trường Chinh (7-15), Mai Chí Thọ (12-3, 8-9).
* **Các tuyến 1 chiều (Directed Edges)**: Điện Biên Phủ (2 $\to$ 6), Pasteur (11 $\to$ 4), Lạc Long Quân (14 $\to$ 0).

---

## ⚡ III. 4 THUẬT TOÁN CỐT LÕI VÀ CÁCH VẬN HÀNH TRÊN SA BÀN

### 1. Thuật toán Dijkstra: Điều hướng Xe Cứu Thương Né Tắc Đường (Dynamic Re-routing)
* **Bài toán thực tế**: Xe cứu thương chở bệnh nhân nguy kịch từ Hiện trường về Bệnh Viện Đa Khoa [1] hoặc xuất phát từ Trạm Cứu Hỏa [0].
* **Cơ chế hoạt động**:
  - Dựa trên hàm chi phí thời gian thực $Weight = \text{Length} \times (1 + 2.5 \times Congestion)$.
  - **Tương tác trực tiếp**: Người dùng click chuột phải lên tuyến đường đang đi để "Bơm kẹt xe" (đèn đỏ tắc cứng) $\to$ Thuật toán Dijkstra phát hiện chi phí đoạn này vọt lên cao, ngay lập tức kích hoạt tính năng **Tự Động Re-Route** sang lộ trình vòng khác vắng hơn!
  - Xe cứu thương hoạt họa mượt mà, chớp đèn còi ưu tiên xanh đỏ di chuyển theo đúng các nút giao được chọn.

### 2. Thuật toán BFS: Đội Cứu Hộ Khẩn Cấp Quét Sóng Đồng Tâm (Wave Level Dispatch)
* **Bài toán thực tế**: Khi xảy ra sự cố lớn (cháy lớn, vỡ đường ống nước, ngập lụt) tại một nút giao, Sở Chỉ Huy cần điều động lực lượng phong tỏa và phân luồng từ tâm sự cố theo các vòng tròn đồng tâm.
* **Cơ chế hoạt động**:
  - Khởi tạo hàng đợi FIFO từ tâm sự cố $u$.
  - Mở rộng theo từng cấp độ:
    - **Cấp 1 (1-hop)**: Các nút giao trực tiếp tiếp giáp tâm sự cố $\to$ Đóng đường khẩn cấp.
    - **Cấp 2 (2-hops)**: Các nút giao trung gian $\to$ Đặt biển báo chuyển hướng từ xa.
### 1. Thuật toán Dijkstra: Điều hướng Xe Cứu Thương & Bẻ Cua Tại Điểm Gãy (Breakpoint Re-routing)
* **Bài toán thực tế**: Xe cứu thương đang di chuyển trên lộ trình ngắn nhất. Bất ngờ, một đoạn đường phía trước gặp sự cố nghiêm trọng (sập cầu, tai nạn liên hoàn, ngập nặng) biến thành **Điểm Gãy (Break Point)** hoàn toàn bị cô lập!
* **Cơ chế hoạt động**:
  - Không chỉ tính lại từ đầu, hệ thống nhận diện **Nút giao ngay trước Điểm Gãy (Pivot Node)**.
  - Thuật toán Dijkstra tức thì kích hoạt tại nút Pivot để tìm **Nhánh Rẽ Mới (Detour Branch)** đưa xe đến đích B an toàn.
  - **Trên màn hình Pygame**:
    - Đoạn đường gặp sự cố nhấp nháy đỏ chói kèm biểu tượng ⛔ `[ĐIỂM GÃY KHÓA ĐƯỜNG]`.
    - Nút giao trước điểm gãy phát sáng hào quang vàng ⚡ `[ĐIỂM BẺ CUA]`.
    - Lộ trình thay thế phát sáng rực rỡ màu vàng Neon, xe cứu thương bẻ lái mượt mà sang lộ trình mới!
    - Bấm phím **`[B]`** để kích hoạt kịch bản mẫu này chỉ trong 1 giây!

### 2. Thuật toán BFS: Đội Cứu Hộ Khẩn Cấp Tô Màu Từng Lớp Sóng Đồng Tâm (Multi-Layer Wave)
* **Bài toán thực tế**: Sự cố khẩn cấp (cháy lớn, nổ đường ống) tại một nút giao. Lực lượng cứu hộ cần khoanh vùng theo bán kính ngã rẽ ít nhất (FIFO Queue).
* **Cơ chế hoạt động & Phân tầng màu sắc**:
  - **Cấp 0 (Đỏ rực)**: Tâm sự cố ban đầu (Epicenter) $\to$ Khoanh vùng nguy hiểm.
  - **Cấp 1 (Vàng chanh - 1 ngã rẽ)**: Vành đai 1 $\to$ Đóng đường khẩn cấp, sơ tán dân.
  - **Cấp 2 (Xanh lam ngọc - 2 ngã rẽ)**: Vành đai 2 $\to$ Đặt chốt chặn điều tiết giao thông.
  - **Cấp 3+ (Xanh lục bảo & Tím - 3+ ngã rẽ)**: Vành đai 3 $\to$ Cảnh báo phân luồng từ xa toàn đô thị.
  - **Trên màn hình Pygame**:
    - Mỗi lớp có màu sắc riêng biệt hiển thị trên cả nút giao và các nhánh cây khung BFS.
    - Góc trái bản đồ có **Bảng Chú Giải Các Lớp Sóng BFS** trực quan 100%.

### 3. Thuật toán DFS: Kiểm Tra Luồng 1 Chiều, Phát Hiện Bẫy Ngõ Cụt & Deadlock
* **Bản chất đời thực**:
  - Bạn đi vào khu phố cổ có các biển báo 1 chiều. Bạn rẽ phải theo biển 1 chiều, lại gặp biển 1 chiều bắt rẽ trái, rồi lại rẽ tiếp... cuối cùng **quay trở lại đúng chỗ cũ mà không có đường nào thoát ra đại lộ**! Đó chính là **BẪY KẸT XE VÒNG LẶP (Deadlock Cycle)**!
  - Hoặc xe đi vào một đoạn 1 chiều mà đầu kia bị rào chắn không có đường rẽ $\to$ **NGÕ CỤT 1 CHIỀU (Dead-end)**!
* **Bản chất Toán học CTRR**:
  - DFS duyệt sâu theo từng nhánh và phân loại cung thành: Cung cây (Tree Edge) và **Cung ngược (Back Edge)**.
  - **Định lý CTRR**: Đồ thị có hướng tồn tại chu trình bế tắc **KHI VÀ CHỈ KHI DFS GẶP CUNG NGƯỢC (Back Edge)** nối về một đỉnh tổ tiên đang duyệt dở (Màu Xám).
  - **Trên màn hình Pygame**:
    - Chu trình bế tắc được viền đỏ phát sáng, có các mũi tên trắng xoay tròn nhấp nháy cảnh báo: `[⚠️ BẪY KẸT XE VÒNG LẶP (DEADLOCK)]`.
    - Ngõ cụt hiển thị biển báo ⛔ `[NGÕ CỤT 1 CHIỀU]`.

### 4. Thuật toán MST (Kruskal): Quy Hoạch Cáp Quang Đèn Tín Hiệu Thông Minh
* **Bài toán thực tế**: Sở GTVT cần đào đường đặt cáp viễn thông nối toàn bộ 16 cột đèn tín hiệu về Trung Tâm TOC [2].
* **Cơ chế hoạt động**:
  - Sắp xếp các đoạn đường tăng dần, dùng cấu trúc dữ liệu **DSU** chọn đúng $V - 1 = 15$ đoạn cáp ngắn nhất, không tạo vòng dư thừa.
  - Tiết kiệm hơn 40% chi phí đào đường so với phủ kín toàn bộ các tuyến.

---

## 🎤 IV. KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN TRƯỚC HỘI ĐỒNG (3 PHÚT)

> *(Khởi chạy sa bàn: `python run_traffic_sim.py` hoặc chọn `[10]` trong `python main.py`)*

* **Mở đầu (30 giây)**:  
  *"Kính thưa quý Thầy Cô, nhóm chúng em ứng dụng Lý thuyết Đồ thị vào bài toán thực tế: **Hệ thống Mô phỏng & Điều phối Mạng lưới Giao thông Đô thị Thông minh**.  
  Bản đồ gồm 16 nút giao ($V$) và 27 tuyến đường ($E$). Trọng số cạnh là hàm chi phí thay đổi theo thời gian thực phụ thuộc vào mức độ kẹt xe."*

* **Demo 1 - Dijkstra Bẻ Cua Tại Điểm Gãy (45 giây)**:  
  *(Bấm phím `[1]`, rồi bấm phím `[B]`)*  
  *"Thưa Thầy Cô, xe cứu thương đang đi trên lộ trình ngắn nhất. Em bấm phím `[B]` mô phỏng sự cố sập cầu gây **Điểm Gãy** tại đoạn trước mặt xe. Thuật toán **Dijkstra** lập tức phát hiện nút bẻ cua ngay trước điểm gãy và **tự động vẽ nhánh rẽ mới màu vàng** đưa xe cứu thương vòng qua đại lộ khác đến bệnh viện an toàn!"*

* **Demo 2 - BFS Sóng Tô Màu Từng Lớp (30 giây)**:  
  *(Bấm phím `[2]`)*  
  *"Khi xảy ra sự cố, thuật toán **BFS** dùng hàng đợi FIFO quét theo từng lớp đồng tâm có **màu sắc riêng biệt**: Đỏ là tâm sự cố, Vàng là Vành đai 1 cần đóng đường khẩn, Xanh lam là Vành đai 2 đặt chốt chặn, và Xanh lá là Vành đai 3 cảnh báo từ xa."*

* **Demo 3 - DFS Bẫy Kẹt Xe 1 Chiều & Deadlock (45 giây - ĂN ĐIỂM CAO)**:  
  *(Bấm phím `[3]`)*  
  *"Thưa Thầy Cô, trong quy hoạch luồng 1 chiều, nếu phân luồng sai sẽ tạo ra **vòng lặp kẹt xe kín (Deadlock)** khiến các xe chạy lòng vòng không thoát ra được.  
  Nhóm ứng dụng thuật toán **DFS** với kỹ thuật tô màu 3 trạng thái. Định lý toán rời rạc chỉ rõ: khi DFS gặp **Cung ngược (Back Edge)**, nó lập tức bắt trọn chu trình khép kín này và báo động đỏ trên màn hình để chuyên viên giao thông cắm lại biển báo!"*

* **Demo 4 - MST Kruskal (30 giây)**:  
  *(Bấm phím `[4]`)*  
  *"Để kết nối 16 nút đèn tín hiệu về Trung tâm TOC, thuật toán **Kruskal cùng cấu trúc DSU** tìm ra Cây Khung gồm đúng 15 đoạn cáp màu vàng ánh kim, tiết kiệm hơn 40% chi phí đào đường."*

* **Kết luận (10 giây)**:  
  *"Hệ thống vừa phản ánh đúng 100% bản chất toán học của môn Cấu Trúc Rời Rạc, vừa mang tính ứng dụng thực tế cao. Nhóm em xin cảm ơn Thầy Cô!"*


# 📊 BÁO CÁO TIẾN ĐỘ THỰC HIỆN DỰ ÁN CTRR FINAL PROJECT

* **Môn học**: Cấu trúc rời rạc (Discrete Mathematics & Graph Theory)
* **Nhóm**: 5 thành viên
* **Nhóm trưởng**: Jackie Khoa
* **Cập nhật lần cuối**: 27/08/2026

---

# 🏆 1. TỔNG QUAN TIẾN ĐỘ TOÀN DỰ ÁN

```
[GIAI ĐOẠN 1: PHẦN CƠ BẢN (MỤC 1 -> 5)]     ████████████████████  100% (HOÀN THÀNH)
[GIAI ĐOẠN 2: PHẦN NÂNG CAO (MỤC 7 & 8)]    ░░░░░░░░░░░░░░░░░░░░    0% (SẴN SÀNG TRIỂN KHAI)
```

---

# 🟢 2. CHI TIẾT CÁC PHẦN ĐÃ HOÀN THÀNH (PHẦN CƠ BẢN)

| STT | Mục đề bài | File mã nguồn | Thành viên | Trạng thái | Đánh giá |
|:---:|:---|:---|:---|:---:|:---:|
| **1** | Input đồ thị & Vẽ lưu hình PNG | `core/graph.py`<br>`visualizer/draw.py` | **Jackie Khoa**<br>**Nhật Trường** | ✅ XONG | Bố cục đa tầng đồng tâm, xuất ảnh cực nét. |
| **2** | Chuyển đổi 6 chiều giữa 3 dạng | `core/converter.py` | **Jackie Khoa** | ✅ XONG | Chuyển đổi chính xác Matrix ↔ Adj List ↔ Edge List. |
| **3** | Duyệt BFS & DFS riêng biệt | `core/traversal.py` | **Đỗ Thanh** | ✅ XONG | Thứ tự `sorted` khớp 100% giải tay + Bảng vết Queue/Đệ quy. |
| **4** | Đồ thị 2 phía & Chu trình lẻ | `core/bipartite.py` | **Tuấn** (Nhóm hỗ trợ) | ✅ XONG | Tô 2 màu, chia 2 tập V1, V2 hoặc vạch chu trình lẻ. |
| **5** | Dijkstra & Bellman-Ford | `core/shortest_path.py` | **Linh** | ✅ XONG | Tìm đường tối ưu, xuất bảng ma trận lặp, bắt chu trình âm. |
| **CLI**| Menu điều khiển OOP | `app/cli.py`<br>`run_demo.py` | **Jackie Khoa** | ✅ XONG | Menu Console CLI tương tác linh hoạt, phân tách rõ ràng. |

---

# 🔴 3. KẾ HOẠCH PHẦN NÂNG CAO & BÀI TOÁN THỰC TẾ

| Mục | Thuật toán / Bài toán | File dự kiến | Nhiệm vụ kỹ thuật | Trạng thái |
|:---:|:---|:---|:---|:---:|
| **7.1** | Thuật toán Fleury | `core/euler.py` | Tìm chu trình / đường đi Euler bằng cách tránh đi qua cầu | ⏳ Chưa làm |
| **7.2** | Thuật toán Hierholzer | `core/euler.py` | Tìm Euler bằng cách nối chu trình con bằng Stack | ⏳ Chưa làm |
| **7.3** | Thuật toán Prim | `core/mst.py` | Tìm Cây khung nhỏ nhất (MST) mở rộng từ 1 đỉnh | ⏳ Chưa làm |
| **7.4** | Thuật toán Kruskal | `core/mst.py` | Tìm Cây khung nhỏ nhất (MST) kết hợp cấu trúc DSU | ⏳ Chưa làm |
| **7.5** | Thuật toán Ford-Fulkerson | `core/max_flow.py` | Tìm Luồng cực đại (Max Flow) & Lát cắt hẹp nhất (Min Cut) | ⏳ Chưa làm |
| **8** | Ứng dụng Bài toán thực tế | `app/real_world.py` | Lựa chọn đề tài thực tế độc đáo và ấn tượng | ⏳ Đang chọn đề tài |

---

# 🚀 4. LỆNH CHẠY HỆ THỐNG HIỆN TẠI

```bash
# Chạy Menu tương tác chính (Phần cơ bản 1 -> 5):
python3 run_demo.py
```

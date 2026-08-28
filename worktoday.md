# 📋 KẾ HOẠCH TRIỂN KHAI PHẦN NÂNG CAO — CTRR FINAL PROJECT

Tài liệu chi tiết các đầu việc, thứ tự thực hiện và phân công cho **Phần Nâng Cao (Mục 7 & Mục 8)**.

---

## 📊 SƠ ĐỒ PHỤ THUỘC & THỨ TỰ THỰC HIỆN

```
┌─────────────────────────────────────────────────────────────────────────┐
│              GIAI ĐOẠN 1: TRIỂN KHAI CÁC MODULE CORE ĐỘC LẬP            │
│                     (LÀM SONG SONG 100% CÙNG LÚC)                       │
│                                                                         │
│  [Nhánh A: Euler]       [Nhánh B: MST]       [Nhánh C: Max Flow]       │
│   • Fleury (7.1)         • Prim (7.3)         • Ford-Fulkerson (7.5)    │
│   • Hierholzer (7.2)     • Kruskal DSU (7.4)  • Min Cut (7.5)           │
│   • test_euler.py        • test_mst.py        • test_max_flow.py        │
│                                                                         │
│             [Nhánh D: Kịch bản & Dữ liệu Bài toán thực tế Mục 8]        │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              GIAI ĐOẠN 2: TÍCH HỢP TRỰC QUAN HÓA & MENU CLI             │
│                 (BẮT BUỘC SAU KHI HOÀN TẤT GIAI ĐOẠN 1)                 │
│                                                                         │
│   • visualizer/draw.py: Thêm hàm vẽ Euler, MST, Mạng Luồng & Lát Cắt   │
│   • app/cli.py: Ghép Menu chọn 7.1 -> 7.5 và Mục 8, xuất Bảng vết       │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│             GIAI ĐOẠN 3: NGHIỆM THU & BÁO CÁO TOÀN DIỆN CUỐI CÙNG       │
│                                                                         │
│   • Chạy kịch bản Bài toán thực tế Mục 8 trực tiếp từ Menu CLI          │
│   • Chạy toàn bộ Test Suite tự động (pytest tests/) đảm bảo pass 100%   │
│   • Cập nhật báo cáo tiến độ nộp bài (TIEN_DO.md / README.md)           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📝 CHECKLIST CHI TIẾT TỪNG GIAI ĐOẠN

### 🟢 GIAI ĐOẠN 1: CÁC MODULE CORE ĐỘC LẬP (LÀM SONG SONG ĐƯỢC)

| # | Hạng mục công việc | File đảm nhận | Nhiệm vụ cụ thể | Trạng thái |
|:---:|:---|:---|:---|:---:|
| **1.1** | **Chu trình & Đường đi Euler** | `core/euler.py`<br>`tests/test_euler.py` | • Kiểm tra điều kiện tồn tại Euler (tính liên thông & bậc đỉnh).<br>• Cài đặt **7.1 Fleury** (tìm cầu và duyệt).<br>• Cài đặt **7.2 Hierholzer** (dùng Stack nối chu trình con). | ⏳ Chưa làm |
| **1.2** | **Cây khung nhỏ nhất (MST)** | `core/mst.py`<br>`tests/test_mst.py` | • Cài đặt **7.3 Prim** (mở rộng cây khung từ 1 đỉnh).<br>• Cài đặt class **DSU** (Find có Path Compression + Union by Rank).<br>• Cài đặt **7.4 Kruskal** (sắp xếp cạnh + DSU). | ⏳ Chưa làm |
| **1.3** | **Luồng cực đại & Lát cắt** | `core/max_flow.py`<br>`tests/test_max_flow.py` | • Cài đặt **7.5 Ford-Fulkerson (Edmonds-Karp)** dùng BFS tìm đường tăng luồng.<br>• Tìm tập lát cắt hẹp nhất **Min Cut** $(S, T)$ trên đồ thị thặng dư. | ⏳ Chưa làm |
| **1.4** | **Thiết kế Bài toán thực tế (Mục 8)** | `data/sample_real_world.py`<br>`docs/real_world_spec.md` | • Xác định bài toán thực tế (ví dụ: Mạng cấp nước đô thị / Thu gom rác / Điều phối vận tải).<br>• Định nghĩa rõ: Node là gì, Edge là gì, Trọng số là gì, Mục tiêu là gì.<br>• Chuẩn bị dataset đồ thị thực tế. | ⏳ Chưa làm |

---

### 🟡 GIAI ĐOẠN 2: TÍCH HỢP TRỰC QUAN HÓA & MENU CLI (LÀM SAU KHI CÓ CORE)

| # | Hạng mục công việc | File đảm nhận | Nhiệm vụ cụ thể | Trạng thái |
|:---:|:---|:---|:---|:---:|
| **2.1** | **Mở rộng Trực quan hóa đồ thị** | `visualizer/draw.py` | • `draw_euler_path()`: Vẽ chu trình Euler có đánh số thứ tự từng bước.<br>• `draw_mst()`: Tô màu nổi bật các cạnh thuộc cây khung MST.<br>• `draw_max_flow()`: Vẽ mạng luồng hiển thị `flow/capacity` và vạch cắt Min-Cut. | ⏳ Chưa làm |
| **2.2** | **Tích hợp Menu CLI & Bảng vết** | `app/cli.py` | • Thêm các lựa chọn 7.1, 7.2, 7.3, 7.4, 7.5 vào Menu chính.<br>• Xuất Bảng vết bước lặp chi tiết để đối chiếu bài làm tay.<br>• Tự động gọi hàm vẽ hình và lưu file ảnh kết quả. | ⏳ Chưa làm |

---

### 🔴 GIAI ĐOẠN 3: NGHIỆM THU & BÁO CÁO (LÀM CUỐI CÙNG)

| # | Hạng mục công việc | File đảm nhận | Nhiệm vụ cụ thể | Trạng thái |
|:---:|:---|:---|:---|:---:|
| **3.1** | **Chạy thử nghiệm Bài toán thực tế** | `app/cli.py`<br>`run_demo.py` | • Nạp dữ liệu thực tế Mục 8 và chạy trực tiếp từ giao diện CLI.<br>• Xuất file ảnh kết quả phân tích thực tế. | ⏳ Chưa làm |
| **3.2** | **Kiểm thử toàn bộ hệ thống (Unit Tests)** | `tests/` | • Chạy `pytest tests/` đảm bảo 100% test cases (Cơ bản + Nâng cao) đều pass. | ⏳ Chưa làm |
| **3.3** | **Cập nhật Báo cáo & Tài liệu** | `TIEN_DO.md`<br>`README.md` | • Cập nhật bảng phân công, tiến độ hoàn thành và hướng dẫn sử dụng. | ⏳ Chưa làm |

---

## 🎯 CÁC LỆNH CHẠY KIỂM THỬ KHI HOÀN THÀNH

```bash
# 1. Chạy ứng dụng Menu chính:
python3 run_demo.py

# 2. Chạy kiểm thử từng module nâng cao:
python3 tests/test_euler.py
python3 tests/test_mst.py
python3 tests/test_max_flow.py

# 3. Chạy toàn bộ test suite:
pytest tests/
```

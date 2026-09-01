# BẢNG PHÂN CÔNG & TIẾN ĐỘ THỰC HIỆN DỰ ÁN CTRR

Tài liệu quản lý tiến độ và phân công công việc của nhóm 5 người.

---

# 📊 BẢNG CHECKLIST TIẾN ĐỘ TOÀN DỰ ÁN

## 🟢 GIAI ĐOẠN 1: PHẦN CƠ BẢN (HOÀN THÀNH 100% ✅)

| Mục | Chức năng theo đề bài | File code đảm nhận | Thành viên | Trạng thái |
|:---:|:---|:---|:---|:---:|
| **1** | Input đồ thị & Vẽ lưu hình đồ thị | `core/graph.py`<br>`visualizer/draw.py` | **Jackie Khoa**<br>**Nhật Trường** | ✅ **XONG 100%** |
| **2** | Chuyển đổi 3 dạng biểu diễn (Matrix ↔ List ↔ Edge) | `core/converter.py` | **Jackie Khoa** | ✅ **XONG 100%** |
| **3** | Duyệt BFS & DFS + Bảng vết đối chiếu + Animation .GIF | `core/traversal.py`<br>`visualizer/animation.py` | **Đỗ Thanh**<br>**Jackie Khoa** | ✅ **XONG 100%** |
| **4** | Kiểm tra Đồ thị 2 phía (Bipartite) & Chu trình lẻ | `core/bipartite.py` | **Tuấn** | ✅ **XONG 100%** |
| **5** | Đường đi ngắn nhất (Dijkstra & Bellman-Ford) | `core/shortest_path.py` | **Linh** | ✅ **XONG 100%** |
| **Menu** | Ứng dụng CLI Menu điều khiển tương tác | `run_demo.py` | **Jackie Khoa** | ✅ **XONG 100%** |

---

## 🔴 GIAI ĐOẠN 2: PHẦN NÂNG CAO & BÀI TOÁN THỰC TẾ (HOÀN THÀNH 100% ✅)

| Mục | Thuật toán / Nhiệm vụ theo đề bài | File đảm nhận | Phân công ban đầu | Người thực hiện thực tế | Trạng thái |
|:---:|:---|:---|:---|:---|:---:|
| **7.1** | Fleury (Chu trình / Đường đi Euler) | `core/euler.py` | **Đỗ Thanh** | **Đỗ Thanh** + **Jackie Khoa** (fix bug) | ✅ **XONG 100%** |
| **7.2** | Hierholzer (Chu trình / Đường đi Euler) | `core/euler.py` | **Đỗ Thanh** | **Đỗ Thanh** + **Jackie Khoa** (fix bug) | ✅ **XONG 100%** |
| **7.3** | Prim (Cây khung nhỏ nhất - MST) | `core/mst.py` | **Linh** | **Linh** | ✅ **XONG 100%** |
| **7.4** | Kruskal (Cây khung nhỏ nhất - MST) | `core/mst.py` | **Linh** | **Linh** | ✅ **XONG 100%** |
| **7.5** | Ford-Fulkerson (Max Flow & Min Cut) | `core/max_flow.py` | **Tuấn** | ❌ **Tuấn không hợp tác, không làm**<br>👑 **Jackie Khoa tiếp quản & làm toàn bộ** | ✅ **XONG 100%** |
| **Vẽ** | Trực quan hóa nâng cao (Euler, MST, Flow, Animation) | `visualizer/draw.py`<br>`visualizer/animation.py` | **Nhật Trường** | **Nhật Trường** + **Jackie Khoa** | ✅ **XONG 100%** |
| **8 & Demo** | **Menu CLI Tương Tác & Chạy Demo Tự Động Toàn Diện** + **TEST TOÀN BỘ** | `app/cli.py`<br>`run_demo.py`<br>`tests/` | **Jackie Khoa** | **Jackie Khoa** | ✅ **XONG 100%** |

---

# 👤 1. ĐỖ THANH — CHU TRÌNH & ĐƯỜNG ĐI EULER (`core/euler.py`) — ✅ XONG 100%

> **File**: `core/euler.py`  
> **Trạng thái**: Đã cài đặt `check_eulerian()`, `fleury()`, `hierholzer()`. Nhóm trưởng Jackie Khoa đã review và fix toàn bộ cú pháp/logic.

---

# 👤 2. LINH — CÂY KHUNG NHỎ NHẤT (MST) (`core/mst.py`) — ✅ XONG 100%

> **File**: `core/mst.py`  
> **Trạng thái**: Đã hoàn thành `class DSU`, `kruskal()`, và `prim()`. Đã test pass 100%.

---

# 👤 3. TUẤN ❌ (KHÔNG HỢP TÁC, KHÔNG LÀM) $\to$ 👑 JACKIE KHOA TIẾP QUẢN (`core/max_flow.py`) — ✅ XONG 100%

> **File**: `core/max_flow.py`  
> **Ghi chú**: **Tuấn không hợp tác, không làm nhiệm vụ được phân công.** Nhóm trưởng **Jackie Khoa** đã tiếp quản và hoàn thành toàn bộ thuật toán Ford-Fulkerson (Edmonds-Karp) và Lát cắt hẹp nhất (Min Cut). Đã test pass 100%.

---

# 👤 4. NHẬT TRƯỜNG — TRỰC QUAN HÓA NÂNG CAO (`visualizer/draw.py` & `visualizer/animation.py`) — ✅ XONG 100%

> **File**: `visualizer/draw.py`, `visualizer/animation.py`  
> **Đã hoàn thành**: Bổ sung `draw_euler()`, `draw_mst()`, `draw_max_flow()`, `compute_smart_layout()`, và xuất file ảnh động `animate_dfs()`, `animate_bfs()` (.GIF).

---

# 👤 5. JACKIE KHOA (LEADER) — MENU CLI & TEST TOÀN BỘ — ✅ XONG 100%

> **File đảm nhận**: `app/cli.py`, `run_demo.py`, `tests/`  
> **Đã hoàn thành**:
> * Cài đặt xong toàn bộ `core/max_flow.py` (thay Tuấn: Ford-Fulkerson và Min Cut).
> * Review và fix xong toàn bộ `core/euler.py` và `core/mst.py`.
> * Hoàn thiện Menu CLI tương tác 9 chức năng toàn diện trong `app/cli.py`.
> * Viết và chạy toàn bộ test suite: tất cả đều PASS 100%.

---

# 🚀 CÁCH CHẠY VÀ TRẢI NGHIỆM HỆ THỐNG

```bash
# 1. Chạy Hệ Thống Giải Toán CTRR Menu CLI:
python3 run_demo.py

# 2. Chạy Toàn Bộ Bộ Kiểm Thử Tự Động:
python3 tests/test_foundation.py
python3 tests/test_traversal.py
python3 tests/test_bipartite.py
python3 tests/test_shortest_path.py
python3 tests/test_euler.py
python3 tests/test_mst.py
python3 tests/test_max_flow.py
```

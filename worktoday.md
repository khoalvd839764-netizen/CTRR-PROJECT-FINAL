# BẢNG PHÂN CÔNG & TIẾN ĐỘ THỰC HIỆN DỰ ÁN CTRR

Tài liệu quản lý tiến độ và phân công công việc của nhóm 5 người.

---

# 📊 BẢNG CHECKLIST TIẾN ĐỘ TOÀN DỰ ÁN

## 🟢 GIAI ĐOẠN 1: PHẦN CƠ BẢN (HOÀN THÀNH 100% ✅)

| Mục | Chức năng theo đề bài | File code đảm nhận | Thành viên | Trạng thái |
|:---:|:---|:---|:---|:---:|
| **1** | Input đồ thị & Vẽ lưu hình đồ thị | `core/graph.py`<br>`visualizer/draw.py` | **Jackie Khoa**<br>**Nhật Trường** | ✅ **XONG 100%** |
| **2** | Chuyển đổi 3 dạng biểu diễn (Matrix ↔ List ↔ Edge) | `core/converter.py` | **Jackie Khoa** | ✅ **XONG 100%** |
| **3** | Duyệt BFS & DFS + Bảng vết đối chiếu | `core/traversal.py` | **Đỗ Thanh** | ✅ **XONG 100%** |
| **4** | Kiểm tra Đồ thị 2 phía (Bipartite) & Chu trình lẻ | `core/bipartite.py` | **Tuấn** | ✅ **XONG 100%** |
| **5** | Đường đi ngắn nhất (Dijkstra & Bellman-Ford) | `core/shortest_path.py` | **Linh** | ✅ **XONG 100%** |
| **Menu** | Ứng dụng CLI Menu điều khiển tương tác | `run_demo.py` | **Jackie Khoa** | ✅ **XONG 100%** |

---

## 🔴 GIAI ĐOẠN 2: PHẦN NÂNG CAO & BÀI TOÁN THỰC TẾ

| Mục | Thuật toán / Nhiệm vụ theo đề bài | File đảm nhận | Thành viên | Trọng tâm giải quyết | Trạng thái |
|:---:|:---|:---|:---|:---|:---:|
| **7.1** | Fleury (Chu trình / Đường đi Euler) | `core/euler.py` | **Đỗ Thanh** | Kiểm tra cầu (Bridge) và đi qua mỗi cạnh đúng 1 lần | ⏳ Đang làm |
| **7.2** | Hierholzer (Chu trình / Đường đi Euler) | `core/euler.py` | **Đỗ Thanh** | Dùng Stack nối các chu trình con $O(E)$ | ⏳ Đang làm |
| **7.3** | Prim (Cây khung nhỏ nhất - MST) | `core/mst.py` | **Linh** | Mở rộng cây khung từ 1 đỉnh xuất phát | ⏳ Đang làm |
| **7.4** | Kruskal (Cây khung nhỏ nhất - MST) | `core/mst.py` | **Linh** | Sắp xếp cạnh + Cấu trúc DSU (Union-Find) | ⏳ Đang làm |
| **7.5** | Ford-Fulkerson (Max Flow & Min Cut) | `core/max_flow.py` | **Tuấn** | Tìm luồng cực đại (Edmonds-Karp) và lát cắt hẹp nhất | ⏳ Đang làm |
| **Vẽ** | Trực quan hóa nâng cao (Euler, MST, Flow) | `visualizer/draw.py` | **Nhật Trường** | Vẽ đường Euler đánh số, tô màu MST, vẽ lát cắt Min Cut | ⏳ Đang làm |
| **8 & Test** | Bài toán thực tế + Menu CLI + **TEST TOÀN BỘ** | `data/sample_real_world.py`<br>`app/cli.py`<br>`tests/` | **Jackie Khoa** | Bài toán thực tế, Menu CLI và **kiểm thử toàn bộ hệ thống** | ⏳ Đang làm |

---

# 👤 1. ĐỖ THANH — CHU TRÌNH & ĐƯỜNG ĐI EULER (`core/euler.py`)

> **File cần mở**: `core/euler.py`  
> **Nhiệm vụ**: Cài đặt kiểm tra Euler, thuật toán Fleury (7.1) và Hierholzer (7.2).

### 🎯 Hướng dẫn thực hiện:
1. **Hàm `check_eulerian(adj, n)`**:
   * Kiểm tra tính liên thông.
   * Đếm đỉnh bậc lẻ: 0 đỉnh lẻ $\to$ Chu trình Euler; 2 đỉnh lẻ $\to$ Đường đi Euler; $>2$ đỉnh lẻ $\to$ Không có Euler.
2. **Hàm `fleury(adj, n, start)` (Mục 7.1)**:
   * Đi qua các cạnh, kiểm tra cạnh có phải là Cầu (Bridge) hay không bằng DFS.
   * Không bao giờ đi qua cầu trừ khi không còn cạnh nào khác.
3. **Hàm `hierholzer(adj, n, start)` (Mục 7.2)**:
   * Dùng Stack `curr_path`, đi sâu khi gặp ngõ cụt thì đưa vào `circuit`.
   * Đảo ngược `circuit` để có chu trình Euler tối ưu $O(E)$.

---

# 👤 2. LINH — CÂY KHUNG NHỎ NHẤT (MST) (`core/mst.py`)

> **File cần mở**: `core/mst.py`  
> **Nhiệm vụ**: Cài đặt class DSU, thuật toán Prim (7.3) và Kruskal (7.4).

### 🎯 Hướng dẫn thực hiện:
1. **Class `DSU`**:
   * Cài hàm `find(i)` có Path Compression.
   * Cài hàm `union(i, j)` theo Rank (trả về True nếu gộp được, False nếu cùng tập).
2. **Hàm `kruskal(edges, n)` (Mục 7.4)**:
   * Sắp xếp `edges` theo trọng số tăng dần.
   * Lần lượt duyệt từng cạnh, dùng DSU để thêm vào MST nếu không tạo chu trình cho đủ $n-1$ cạnh.
3. **Hàm `prim(adj, n, start)` (Mục 7.3)**:
   * Bắt đầu từ đỉnh `start`, dùng mảng `visited` liên tục chọn cạnh nhẹ nhất nối giữa tập đã thăm và chưa thăm.

---

# 👤 3. TUẤN — LUỒNG CỰC ĐẠI & LÁT CẮT HẸP NHẤT (`core/max_flow.py`)

> **File cần mở**: `core/max_flow.py`  
> **Nhiệm vụ**: Cài đặt thuật toán Ford-Fulkerson (Edmonds-Karp) và tìm Min Cut (7.5).

### 🎯 Hướng dẫn thực hiện:
1. **Hàm `ford_fulkerson(edges, n, source, sink)`**:
   * Dựng ma trận luồng thặng dư `residual[n][n]`.
   * Dùng BFS tìm đường tăng luồng ngắn nhất từ `source` đến `sink`.
   * Tăng luồng $\Delta f = \min(\text{residual})$ và cập nhật đồ thị thặng dư.
2. **Tìm Lát cắt hẹp nhất (Min Cut)**:
   * Dùng BFS/DFS từ `source` trên `residual` để chia thành 2 tập $(S, T)$.
   * Lấy các cạnh gốc nối từ $S \to T$.

---

# 👤 4. NHẬT TRƯỜNG — TRỰC QUAN HÓA NÂNG CAO (`visualizer/draw.py`)

> **File cần mở**: `visualizer/draw.py`  
> **Nhiệm vụ**: Viết các hàm vẽ hình đồ thị cho Euler, MST, và Mạng luồng Max Flow.

### 🎯 Hướng dẫn thực hiện:
1. **Hàm `draw_euler(g, path, edges_order, filename)`**: Vẽ đồ thị và đánh số thứ tự từng bước đi $1, 2, 3...$ trên các cạnh.
2. **Hàm `draw_mst(g, mst_edges, total_weight, filename)`**: Tô màu xanh đậm nét to các cạnh thuộc MST, các cạnh bị loại vẽ nét đứt mờ.
3. **Hàm `draw_max_flow(g, flow_matrix, min_cut_edges, max_flow, source, sink, filename)`**: Hiển thị nhãn `flow/capacity` trên mỗi cạnh và vạch cắt Min-Cut.

---

# 👤 5. JACKIE KHOA (LEADER) — BÀI TOÁN THỰC TẾ, MENU CLI & TEST TOÀN BỘ

> **File đảm nhận**: `data/sample_real_world.py`, `app/cli.py`, `run_demo.py`, `tests/`  
> **Trách nhiệm**: Nhóm trưởng chịu trách nhiệm **kiểm thử toàn bộ hệ thống**, tích hợp và giải quyết bài toán thực tế.

### 🎯 Nhiệm vụ cụ thể của Nhóm trưởng:
1. **Bài toán thực tế (Mục 8)**: Xây dựng dữ liệu và giải quyết bài toán *Tối ưu lộ trình xe quét đường / gom rác đô thị* (hoặc mạng cấp nước).
2. **Ghép Menu CLI (`app/cli.py`)**: Tích hợp các lựa chọn 7.1 $\to$ 7.5 và Mục 8 vào Menu chính, xuất Bảng vết bước lặp.
3. **Kiểm thử toàn diện (`tests/`)**:
   * Viết và chạy test kiểm tra thuật toán Euler của Thanh (`tests/test_euler.py`).
   * Viết và chạy test kiểm tra thuật toán MST của Linh (`tests/test_mst.py`).
   * Viết và chạy test kiểm tra thuật toán Max Flow của Tuấn (`tests/test_max_flow.py`).
   * Viết và chạy test kiểm tra hàm vẽ hình của Nhật Trường (`tests/test_draw.py`).
   * Chạy kiểm thử tự động toàn bộ test suite (`pytest tests/`) nghiệm thu dự án.

---

# 🚀 CÁCH CHẠY VÀ KIỂM THỬ HỆ THỐNG (DÀNH CHO NHÓM TRƯỞNG)

1. **Chạy Menu tương tác**:
   ```bash
   .venv/bin/python3 run_demo.py
   ```

2. **Chạy kiểm thử toàn bộ các bài test**:
   ```bash
   .venv/bin/python3 tests/test_foundation.py
   .venv/bin/python3 tests/test_traversal.py
   .venv/bin/python3 tests/test_bipartite.py
   .venv/bin/python3 tests/test_shortest_path.py
   .venv/bin/python3 tests/test_euler.py
   .venv/bin/python3 tests/test_mst.py
   .venv/bin/python3 tests/test_max_flow.py
   .venv/bin/python3 tests/test_draw.py
   ```

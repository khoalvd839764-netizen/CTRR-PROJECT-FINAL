# 📋 BẢNG PHÂN CÔNG & HƯỚNG DẪN CHI TIẾT PHẦN NÂNG CAO (NHÓM 5 THÀNH VIÊN)

Dự án: **CẤU TRÚC RỜI RẠC — CTRR FINAL PROJECT**  
Nhóm trưởng: **Lê Võ Đăng Khoa (Jackie Khoa)**

---

## 👥 BẢNG PHÂN CHIA NHIỆM VỤ

| STT | Thành viên | Nhiệm vụ đảm nhận | File code chính | Mục đề bài |
|:---:|:---|:---|:---|:---:|
| **1** | **Đỗ Thanh** | Chu trình & Đường đi Euler (Fleury + Hierholzer) | `core/euler.py`<br>`tests/test_euler.py` | **Mục 7.1 & 7.2** |
| **2** | **Linh** | Cây khung nhỏ nhất (Prim + Kruskal với DSU) | `core/mst.py`<br>`tests/test_mst.py` | **Mục 7.3 & 7.4** |
| **3** | **Tuấn** | Luồng cực đại & Lát cắt hẹp nhất (Ford-Fulkerson) | `core/max_flow.py`<br>`tests/test_max_flow.py` | **Mục 7.5** |
| **4** | **Nhật Trường** | Trực quan hóa nâng cao (Vẽ Euler, MST, Mạng Luồng) | `visualizer/draw.py`<br>`tests/test_draw.py` | **Mục 7 (Vẽ hình)** |
| **5** | **Đăng Khoa (Leader)** | Thiết kế Bài toán thực tế + Tích hợp Menu CLI + Test Suite | `data/sample_real_world.py`<br>`app/cli.py`<br>`run_demo.py` | **Mục 8 & Ghép nối** |

---

# 👤 1. ĐỖ THANH — CHU TRÌNH & ĐƯỜNG ĐI EULER (`core/euler.py`)

> **Mục tiêu**: Tìm Chu trình Euler (đi qua mỗi cạnh đúng 1 lần rồi về gốc) hoặc Đường đi Euler (đi qua mỗi cạnh đúng 1 lần).

### 🎯 Các hàm cần cài đặt trong `core/euler.py`:

#### 1.1 Hàm bổ trợ: `check_eulerian(adj, n, directed=False)`
* **Mục đích**: Kiểm tra xem đồ thị có Euler hay không trước khi tìm đường.
* **Quy tắc toán học (Vô hướng)**:
  * Đồ thị phải liên thông (các đỉnh bậc $>0$ thuộc cùng 1 thành phần liên thông).
  * **Chu trình Euler**: $0$ đỉnh bậc lẻ (tất cả đỉnh đều bậc chẵn).
  * **Đường đi Euler**: đúng $2$ đỉnh bậc lẻ (bắt đầu từ 1 trong 2 đỉnh lẻ này).
  * **Không có Euler**: nếu có $>2$ đỉnh bậc lẻ.
* **Trả về**: `(has_euler, is_circuit, start_node)`

#### 1.2 Hàm `fleury(adj, n, start=None, directed=False)` (Mục 7.1)
* **Ý tưởng**: Đi từ đỉnh hiện tại sang đỉnh kề sao cho **không đi qua cầu (Bridge)** trừ khi không còn lựa chọn nào khác.
* **Các bước cài đặt**:
  1. Tạo bản sao danh sách kề `adj_copy` để xóa cạnh dần khi đi qua.
  2. Bắt đầu từ đỉnh `u = start`.
  3. Duyệt các đỉnh kề $v$ của $u$:
     * Kiểm tra cạnh $(u, v)$ có phải là **Cầu** hay không (dùng DFS đếm số đỉnh liên thông trước và sau khi tạm xóa cạnh $(u, v)$).
     * Nếu không phải cầu $\implies$ Chọn đi cạnh $(u, v)$.
     * Nếu tất cả đều là cầu $\implies$ Bắt buộc đi cạnh duy nhất còn lại.
  4. Xóa cạnh $(u, v)$ khỏi `adj_copy` và đặt $u = v$, thêm $(u, v)$ vào lộ trình.
  5. Lặp lại cho đến khi hết cạnh.
* **Trả về**: `path` (danh sách đỉnh), `edges_order` (danh sách cạnh theo thứ tự đi), `trace_table` (bảng vết bước lặp).

#### 1.3 Hàm `hierholzer(adj, n, start=None, directed=False)` (Mục 7.2)
* **Ý tưởng**: Tìm chu trình bằng cách đi sâu, khi gặp ngõ cụt thì đưa vào Stack, sau đó ghép chu trình con $\implies$ độ phức tạp tối ưu $O(E)$.
* **Các bước cài đặt**:
  1. Tạo `curr_path = [start]` (Stack) và `circuit = []`.
  2. Vòng lặp `while len(curr_path) > 0:`
     * Lấy `u = curr_path[-1]`.
     * Nếu $u$ còn cạnh kề: lấy đỉnh $v$ kề tiếp theo, xóa cạnh $(u, v)$ khỏi đồ thị, đẩy $v$ vào `curr_path.append(v)`.
     * Nếu $u$ hết cạnh kề (ngõ cụt): bốc ra `circuit.append(curr_path.pop())`.
  3. Đảo ngược `circuit.reverse()` ta được Chu trình/Đường đi Euler hoàn chỉnh!
* **Trả về**: `path`, `edges_order`, `trace_table`.

### 🧪 Lệnh test cho Đỗ Thanh:
```bash
.venv/bin/python3 tests/test_euler.py
```

---

# 👤 2. LINH — CÂY KHUNG NHỎ NHẤT (MST) (`core/mst.py`)

> **Mục tiêu**: Tìm cây khung có tổng trọng số các cạnh là nhỏ nhất trên đồ thị vô hướng liên thông có trọng số.

### 🎯 Các hàm cần cài đặt trong `core/mst.py`:

#### 2.1 Cấu trúc dữ liệu DSU: `class DSU`
* **Nhiệm vụ**: Quản lý các tập hợp rời nhau phục vụ thuật toán Kruskal.
* **Phương thức**:
  * `__init__(self, n)`: Khởi tạo `parent = [i for i in range(n)]`, `rank = [0] * n`.
  * `find(self, i)`: Tìm gốc của phần tử $i$ với **Nén đường đi (Path Compression)**:
    ```python
    if self.parent[i] != i:
        self.parent[i] = self.find(self.parent[i])
    return self.parent[i]
    ```
  * `union(self, i, j)`: Hợp nhất 2 tập chứa $i$ và $j$ theo **Hạng (Union by Rank)**. Trả về `True` nếu gộp thành công, `False` nếu đã cùng tập (tránh tạo chu trình).

#### 2.2 Hàm `kruskal(edges, n)` (Mục 7.4)
* **Ý tưởng**: Sắp xếp cạnh tăng dần $\to$ Lần lượt thêm cạnh vào cây nếu không tạo chu trình (dùng DSU).
* **Các bước cài đặt**:
  1. Sắp xếp `edges` theo trọng số $w$ tăng dần: `sorted_edges = sorted(edges, key=lambda x: x[2])`.
  2. Khởi tạo `dsu = DSU(n)`, `mst_edges = []`, `total_weight = 0`, `trace_table = []`.
  3. Lần lượt duyệt từng cạnh $(u, v, w)$ trong `sorted_edges`:
     * Nếu `dsu.union(u, v) == True`:
       * Thêm $(u, v, w)$ vào `mst_edges`.
       * `total_weight += w`.
       * Ghi vết: `{"edge": (u, v), "weight": w, "action": "CHỌN", "mst_count": len(mst_edges)}`.
     * Ngược lại (`find(u) == find(v)`):
       * Ghi vết: `{"edge": (u, v), "weight": w, "action": "LOẠI (TẠO CHU TRÌNH)"}`.
     * Nếu `len(mst_edges) == n - 1` $\implies$ Đã đủ $N-1$ cạnh, dừng sớm!
* **Trả về**: `mst_edges`, `total_weight`, `trace_table`.

#### 2.3 Hàm `prim(adj, n, start=0)` (Mục 7.3)
* **Ý tưởng**: Mở rộng cây khung từ 1 đỉnh xuất phát, luôn chọn cạnh nhẹ nhất nối giữa tập đã thăm ($S$) và tập chưa thăm ($V \setminus S$).
* **Các bước cài đặt**:
  1. Khởi tạo `visited = [False] * n`, `visited[start] = True`.
  2. `mst_edges = []`, `total_weight = 0`, `trace_table = []`.
  3. Lặp $N - 1$ bước (mỗi bước kết nạp thêm 1 đỉnh mới):
     * Tìm cạnh $(u, v, w)$ có $w$ nhỏ nhất sao cho `visited[u] == True` và `visited[v] == False`.
     * Đánh dấu `visited[v] = True`.
     * Thêm $(u, v, w)$ vào `mst_edges`, `total_weight += w`.
     * Ghi vết từng bước vào `trace_table`.
* **Trả về**: `mst_edges`, `total_weight`, `trace_table`.

### 🧪 Lệnh test cho Linh:
```bash
.venv/bin/python3 tests/test_mst.py
```

---

# 👤 3. TUẤN — LUỒNG CỰC ĐẠI & LÁT CẮT HẸP NHẤT (`core/max_flow.py`)

> **Mục tiêu**: Tìm lưu lượng vận chuyển lớn nhất từ đỉnh Nguồn ($S$) đến đỉnh Đích ($T$) trên mạng có sức chứa (Capacity), và chỉ ra Lát cắt hẹp nhất (Min Cut).

### 🎯 Các hàm cần cài đặt trong `core/max_flow.py`:

#### 3.1 Hàm `ford_fulkerson(edges, n, source, sink)` (Thuật toán Edmonds-Karp)
* **Ý tưởng**: Dùng **BFS** tìm đường tăng luồng ngắn nhất trên đồ thị thặng dư (Residual Graph), tăng luồng cho đến khi không còn đường đi từ $S \to T$.
* **Các bước cài đặt**:
  1. Xây dựng ma trận dung lượng `capacity[n][n]` và ma trận luồng thặng dư `residual[n][n] = capacity[n][n]`.
  2. Khởi tạo `max_flow = 0`, `trace_table = []`.
  3. **Vòng lặp tăng luồng**:
     * Dùng BFS tìm đường đi từ `source` đến `sink` trên `residual`:
       * Nếu tìm thấy đường đi $P$ qua mảng `parent`:
         * Tính lượng luồng có thể tăng thêm: $\Delta f = \min_{(u, v) \in P} \text{residual}[u][v]$.
         * Cập nhật đồ thị thặng dư với mọi cạnh $(u, v) \in P$:
           * $\text{residual}[u][v] -= \Delta f$ (giảm chiều xuôi).
           * $\text{residual}[v][u] += \Delta f$ (tăng chiều ngược).
         * `max_flow += Δf`.
         * Ghi vết: `{"step": k, "augmenting_path": P, "bottleneck": Δf, "current_flow": max_flow}`.
       * Nếu không còn đường đi nào từ `source` tới `sink` $\implies$ Dừng vòng lặp!
  4. **Tìm Lát cắt hẹp nhất (Min Cut)**:
     * Dùng BFS/DFS từ `source` trên đồ thị thặng dư `residual`:
       * Tập $S$: Tất cả các đỉnh mà `source` có thể đi tới được.
       * Tập $T$: Các đỉnh còn lại ($V \setminus S$).
       * Cạnh thuộc lát cắt hẹp nhất: Các cạnh gốc $(u, v)$ có $u \in S$ và $v \in T$.
* **Trả về**: `max_flow`, `flow_matrix`, `min_cut_edges`, `cut_sets (S, T)`, `trace_table`.

### 🧪 Lệnh test cho Tuấn:
```bash
.venv/bin/python3 tests/test_max_flow.py
```

---

# 👤 4. NHẬT TRƯỜNG — TRỰC QUAN HÓA NÂNG CAO (`visualizer/draw.py`)

> **Mục tiêu**: Mở rộng các hàm vẽ hình đồ thị chuyên biệt cho các thuật toán nâng cao và lưu ra file ảnh PNG chất lượng cao.

### 🎯 Các hàm cần bổ sung trong `visualizer/draw.py`:

#### 4.1 Hàm `draw_euler(g, path, edges_order, filename="euler_path.png")`
* Vẽ đồ thị gốc màu xám mờ.
* Tô màu nổi bật các cạnh theo thứ tự đi Euler (có đánh số thứ tự chặng bay/bước đi $1, 2, 3...$ trên cạnh).
* Đỉnh xuất phát tô màu Xanh Lá, đỉnh kết thúc tô màu Đỏ.

#### 4.2 Hàm `draw_mst(g, mst_edges, total_weight, filename="mst_result.png")`
* Các cạnh thuộc cây khung MST tô màu **Xanh Dương Đậm nét to** (lineWidth = 2.5) và ghi rõ trọng số $w$.
* Các cạnh bị loại (không thuộc MST) vẽ nét đứt mờ màu xám.
* Hiển thị dòng tiêu đề: `Cây khung nhỏ nhất MST — Tổng trọng số = total_weight`.

#### 4.3 Hàm `draw_max_flow(g, flow_matrix, min_cut_edges, max_flow, source, sink, filename="max_flow.png")`
* Hiển thị nhãn trên mỗi cạnh dạng `flow / capacity` (ví dụ: `8/10`).
* Đỉnh Nguồn ($S$) tô màu Xanh Dương, Đỉnh Đích ($T$) tô màu Đỏ Cam.
* Các cạnh thuộc Lát cắt hẹp nhất (**Min Cut**) tô màu ĐỎ nét đậm hoặc nét đứt phân cách 2 tập đỉnh.

### 🧪 Lệnh test cho Nhật Trường:
```bash
.venv/bin/python3 tests/test_draw.py
```

---

# 👤 5. ĐĂNG KHOA (NHÓM TRƯỞNG) — BÀI TOÁN THỰC TẾ & TÍCH HỢP HỆ THỐNG

### 🎯 Nhiệm vụ của Nhóm trưởng:

#### 5.1 Thiết kế Bài toán Thực tế (Mục 8 Đề bài)
* **Chủ đề**: **Tối ưu hóa Tuyến Xe Gom Rác & Quét Đường Đô Thị (Urban Sanitation Vehicle Routing)** dùng **Thuật toán Euler (Hierholzer/Fleury)**.
  * Hoặc **Tối ưu mạng lưới cấp nước đô thị** dùng **MST (Kruskal/Prim)**.
* **Xây dựng file dữ liệu**: `data/sample_real_world.py` (Bản đồ các tuyến phố thực tế có tọa độ, tên đường, độ dài).
* **Mô tả 4 yếu tố bắt buộc**:
  1. *Bài toán đặt ra là gì?* (Xe quét đường cần đi qua tất cả các tuyến phố đúng 1 lần để tiết kiệm xăng dầu và thời gian).
  2. *Đỉnh (Node) là gì?* (Các ngã ba, ngã tư giao lộ).
  3. *Cạnh (Edge) là gì?* (Các đoạn đường phố).
  4. *Trọng số (Weight) là gì?* (Chiều dài đoạn đường tính bằng mét).
  5. *Kết quả*: Tìm ra lộ trình hoàn hảo không lặp lại tuyến đường nào.

#### 5.2 Tích hợp toàn bộ vào Menu CLI (`app/cli.py`)
* Ghép các lựa chọn Menu nâng cao:
  * `[7.1]` Tìm chu trình / đường đi Euler bằng Fleury
  * `[7.2]` Tìm chu trình / đường đi Euler bằng Hierholzer
  * `[7.3]` Tìm cây khung nhỏ nhất bằng Prim
  * `[7.4]` Tìm cây khung nhỏ nhất bằng Kruskal (DSU)
  * `[7.5]` Tìm luồng cực đại & Lát cắt hẹp nhất bằng Ford-Fulkerson
  * `[8]` Chạy kịch bản Bài toán thực tế
* In Bảng ma trận / Bảng vết bước lặp chuẩn chỉ để sinh viên đối chiếu khi làm bài thi trên giấy.

#### 5.3 Quản lý bộ Unit Tests tự động (`tests/`)
* Viết đầy đủ assertion cho `test_euler.py`, `test_mst.py`, `test_max_flow.py`.
* Chạy kiểm thử tổng thể `pytest tests/` đảm bảo 100% test pass.

---

## 🚀 QUY TRÌNH PHỐI HỢP GIT CHO CẢ NHÓM:
Mỗi bạn tạo 1 nhánh riêng để code, sau khi test xong thì tạo Pull Request gộp vào `main`:
* Đỗ Thanh: `git checkout -b feature/euler-dothanh`
* Linh: `git checkout -b feature/mst-linh`
* Tuấn: `git checkout -b feature/maxflow-tuan`
* Nhật Trường: `git checkout -b feature/draw-advanced-nhattuong`
* Đăng Khoa: `git checkout -b feature/real-world-cli-dangkhoa`

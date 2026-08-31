# 📚 CẨM NANG CHI TIẾT & PHÂN CÔNG CÔNG VIỆC DỰ ÁN CTRR (NHÓM 5 NGƯỜI)

> **Tài liệu hướng dẫn "cầm tay chỉ việc"** cho từng thành viên trong nhóm. Mọi thành viên đọc kỹ phần của mình để hiểu rõ bản chất toán học, cấu trúc Input/Output và từng bước viết code.

---

# 📊 BẢNG TỔNG KẾT PHÂN CÔNG TOÀN DỰ ÁN

## 🟢 GIAI ĐOẠN 1: PHẦN CƠ BẢN (ĐÃ HOÀN THÀNH 100% ✅)

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

# 👤 1. ĐỖ THANH — CHU TRÌNH & ĐƯỜNG ĐI EULER

* **File cần mở**: `core/euler.py`
* **Ý nghĩa toán học**: Bài toán 7 cây cầu Konigsberg nổi tiếng của Euler. Tìm một đường đi qua **tất cả các cạnh** của đồ thị, mỗi cạnh đi qua **đúng 1 lần**.
  * Nếu điểm đầu trùng điểm cuối $\implies$ **Chu trình Euler (Eulerian Circuit)**.
  * Nếu điểm đầu khác điểm cuối $\implies$ **Đường đi Euler (Eulerian Path)**.

---

### 📌 CÁC HÀM THANH CẦN VIẾT:

#### 🔹 1.1 Hàm `check_eulerian(adj, n, directed=False)`
* **Mục đích**: Kiểm tra trước xem đồ thị có tồn tại Euler hay không.
* **Input**: `adj` (danh sách kề dạng `{0: [(1, 1), (2, 1)], ...}`), `n` (số đỉnh).
* **Quy tắc kiểm tra (Đồ thị vô hướng)**:
  1. Tính bậc (degree) của từng đỉnh: `deg[u] = len(adj.get(u, []))`.
  2. Kiểm tra tính liên thông: Tất cả các đỉnh có bậc $> 0$ phải thuộc cùng một thành phần liên thông (dùng BFS/DFS từ 1 đỉnh có bậc $>0$).
  3. Đếm số đỉnh có bậc lẻ:
     * Nếu **$0$ đỉnh bậc lẻ**: Có **Chu trình Euler** $\implies$ đỉnh xuất phát có thể là bất kỳ đỉnh nào có bậc $>0$.
     * Nếu **đúng $2$ đỉnh bậc lẻ**: Có **Đường đi Euler** $\implies$ đỉnh xuất phát **bắt buộc** phải là 1 trong 2 đỉnh bậc lẻ này.
     * Nếu **khác 0 và 2**: **Không tồn tại Euler**!
* **Output trả về**: `(has_euler: bool, is_circuit: bool, start_node: int or None, message: str)`

---

#### 🔹 1.2 Hàm `fleury(adj, n, start=None, directed=False)` (Mục 7.1)
* **Ý tưởng Fleury**: Đi qua các cạnh tự do, nhưng **TUYỆT ĐỐI KHÔNG ĐI QUA CẦU (Bridge)** trừ khi không còn cạnh nào khác để đi.
  *(Cầu là cạnh mà nếu xóa nó đi thì đồ thị bị đứt làm 2 mảnh không liên thông)*.
* **Từng bước thực hiện**:
  1. Gọi `check_eulerian` kiểm tra trước. Nếu không có Euler thì return rỗng.
  2. Tạo bản sao danh sách kề `adj_copy` để xóa cạnh dần khi duyệt.
  3. Đặt đỉnh hiện tại `u = start` (nếu `start is None` thì lấy start từ `check_eulerian`).
  4. Lặp cho đến khi không còn cạnh nào trong đồ thị:
     * Lấy danh sách các đỉnh kề $v$ của $u$.
     * Nếu chỉ có 1 đỉnh kề duy nhất: Bắt buộc chọn đi cạnh $(u, v)$.
     * Nếu có nhiều đỉnh kề: Dùng hàm bổ trợ `is_bridge(u, v, adj_copy)` để kiểm tra. Chọn cạnh $(u, v)$ đầu tiên **không phải là cầu**.
     * Xóa cạnh $(u, v)$ khỏi `adj_copy` (xóa cả $u \to v$ và $v \to u$).
     * Thêm đỉnh $v$ vào lộ trình `path` và thêm cạnh `(u, v)` vào `edges_order`.
     * Cập nhật `u = v`.
* **Output trả về**: `path` (list các đỉnh `[0, 1, 2, 0]`), `edges_order` (list các cạnh `[(0, 1), (1, 2), (2, 0)]`), `trace_table` (bảng vết từng bước).

---

#### 🔹 1.3 Hàm `hierholzer(adj, n, start=None, directed=False)` (Mục 7.2)
* **Ý tưởng Hierholzer**: Thuật toán cực nhanh $O(E)$ dùng ngăn xếp (Stack). Cứ đi sâu tạo chu trình con, khi gặp ngõ cụt thì lùi lại đưa đỉnh vào chu trình chính.
* **Từng bước thực hiện**:
  1. Tạo Stack `curr_path = [start]` và danh sách kết quả `circuit = []`.
  2. Tạo bản sao `adj_copy`.
  3. Vòng lặp `while len(curr_path) > 0:`
     * Lấy đỉnh đầu ngăn xếp `u = curr_path[-1]`.
     * Nếu $u$ còn cạnh kề:
       * Chọn đỉnh kề $v = adj\_copy[u][0][0]$.
       * Xóa cạnh $(u, v)$ khỏi `adj_copy`.
       * Đẩy $v$ vào ngăn xếp: `curr_path.append(v)`.
     * Nếu $u$ đã hết sạch cạnh kề (ngõ cụt):
       * Lấy $u$ ra khỏi Stack và đưa vào kết quả: `circuit.append(curr_path.pop())`.
  4. Đảo ngược mảng `circuit.reverse()` $\implies$ Thu được đường đi Euler hoàn chỉnh!
* **Output trả về**: `path`, `edges_order`, `trace_table`.

---

# 👤 2. LINH — CÂY KHUNG NHỎ NHẤT (MST - MINIMUM SPANNING TREE)

* **File cần mở**: `core/mst.py`
* **Ý nghĩa toán học**: Cho đồ thị vô hướng liên thông có trọng số gồm $N$ đỉnh. Cây khung nhỏ nhất là một tập hợp gồm đúng $N - 1$ cạnh kết nối tất cả các đỉnh lại với nhau sao cho **tổng trọng số các cạnh là nhỏ nhất** (không chứa chu trình).

---

### 📌 CÁC HÀM LINH CẦN VIẾT:

#### 🔹 2.1 Cấu trúc DSU: `class DSU`
* **Mục đích**: Quản lý các tập hợp rời nhau để kiểm tra 2 đỉnh có thuộc cùng một chu trình hay không với độ phức tạp $O(\alpha(N)) \approx O(1)$.
* **Cài đặt**:
  ```python
  class DSU:
      def __init__(self, n):
          self.parent = list(range(n))
          self.rank = [0] * n

      def find(self, i):
          # Nén đường đi (Path Compression)
          if self.parent[i] != i:
              self.parent[i] = self.find(self.parent[i])
          return self.parent[i]

      def union(self, i, j):
          # Hợp nhất theo hạng (Union by Rank)
          root_i = self.find(i)
          root_j = self.find(j)
          if root_i == root_j:
              return False # Đã cùng tập hợp -> Thêm cạnh này sẽ tạo chu trình!
          if self.rank[root_i] < self.rank[root_j]:
              self.parent[root_i] = root_j
          elif self.rank[root_i] > self.rank[root_j]:
              self.parent[root_j] = root_i
          else:
              self.parent[root_j] = root_i
              self.rank[root_i] += 1
          return True # Gộp thành công -> Không tạo chu trình
  ```

---

#### 🔹 2.2 Hàm `kruskal(edges, n)` (Mục 7.4)
* **Ý tưởng Kruskal**: Thuật toán tham lam (Greedy). Luôn ưu tiên chọn cạnh nhẹ nhất trước.
* **Từng bước thực hiện**:
  1. Sắp xếp toàn bộ danh sách cạnh `edges` theo trọng số $w$ tăng dần: `sorted_edges = sorted(edges, key=lambda x: x[2])`.
  2. Khởi tạo `dsu = DSU(n)`, `mst_edges = []`, `total_weight = 0`, `trace_table = []`.
  3. Lần lượt duyệt từng cạnh $(u, v, w)$ trong `sorted_edges`:
     * Thử gọi `dsu.union(u, v)`:
       * Nếu trả về `True` (hợp lệ):
         * Thêm $(u, v, w)$ vào `mst_edges`.
         * `total_weight += w`.
         * Ghi vết: `{"edge": (u, v), "weight": w, "action": "CHỌN", "current_mst_edges": len(mst_edges)}`.
       * Nếu trả về `False` (tạo chu trình):
         * Bỏ qua cạnh này.
         * Ghi vết: `{"edge": (u, v), "weight": w, "action": "LOẠI (TẠO CHU TRÌNH)"}`.
     * Nếu `len(mst_edges) == n - 1`: Đã đủ $N-1$ cạnh của cây khung $\implies$ `break` dừng sớm!
* **Output trả về**: `mst_edges` (list các cạnh `[(0, 1, 3), ...]`), `total_weight: int/float`, `trace_table`.

---

#### 🔹 2.3 Hàm `prim(adj, n, start=0)` (Mục 7.3)
* **Ý tưởng Prim**: Mở rộng vết dầu loang từ 1 đỉnh. Luôn chọn cạnh nhẹ nhất nối giữa "vùng đã kết nạp" ($S$) và "vùng chưa kết nạp" ($V \setminus S$).
* **Từng bước thực hiện**:
  1. Khởi tạo mảng đánh dấu `visited = [False] * n`, đánh dấu `visited[start] = True`.
  2. Khởi tạo `mst_edges = []`, `total_weight = 0`, `trace_table = []`.
  3. Lặp $N - 1$ lần (mỗi lần kết nạp thêm 1 đỉnh mới vào cây):
     * Tìm trong tất cả các cạnh $(u, v, w)$ sao cho: $u$ đã thăm (`visited[u] == True`) và $v$ chưa thăm (`visited[v] == False`).
     * Chọn cạnh có $w$ nhỏ nhất trong số đó: $(u^*, v^*, w^*)$.
     * Đánh dấu `visited[v^*] = True`.
     * Thêm $(u^*, v^*, w^*)$ vào `mst_edges`, `total_weight += w^*`.
     * Ghi vết bước lặp vào `trace_table`.
* **Output trả về**: `mst_edges`, `total_weight`, `trace_table`.

---

# 👤 3. TUẤN — LUỒNG CỰC ĐẠI & LÁT CẮT HẸP NHẤT (MAX FLOW & MIN CUT)

* **File cần mở**: `core/max_flow.py`
* **Ý nghĩa toán học**:
  * **Mạng luồng (Flow Network)**: Mạng lưới đường ống/giao thông có hướng từ Nguồn ($S$) đến Đích ($T$), mỗi cung có sức chứa tối đa (Capacity).
  * **Luồng cực đại (Max Flow)**: Lưu lượng lớn nhất có thể bơm đồng thời từ $S \to T$ mà không vượt quá sức chứa của bất kỳ ống nào.
  * **Định lý Ford-Fulkerson**: $\text{Max Flow} = \text{Min Cut}$ (Giá trị luồng cực đại luôn bằng tổng sức chứa của Lát cắt hẹp nhất).

---

### 📌 CÁC HÀM TUẤN CẦN VIẾT:

#### 🔹 3.1 Hàm `ford_fulkerson(edges, n, source, sink)` (Thuật toán Edmonds-Karp - Mục 7.5)
* **Ý tưởng**: Dùng **BFS** tìm đường tăng luồng (Augmenting Path) ngắn nhất trên Đồ thị thặng dư (Residual Graph).
* **Từng bước thực hiện**:
  1. Khởi tạo ma trận dung lượng `capacity = [[0]*n for _ in range(n)]`.
  2. Duyệt từng cung `(u, v, cap)` trong `edges`: gán `capacity[u][v] = cap`.
  3. Khởi tạo ma trận luồng thặng dư `residual = [row[:] for row in capacity]`.
  4. Khởi tạo `max_flow = 0`, `trace_table = []`, `step = 0`.
  5. **Vòng lặp tìm đường tăng luồng (BFS)**:
     * Viết hàm phụ `bfs_find_path(residual, n, source, sink)`:
       * Dùng Queue tìm đường đi từ `source` đến `sink` sao cho mọi cạnh trên đường đi đều có `residual[u][v] > 0`.
       * Trả về mảng `parent` lưu vết đường đi (nếu không tìm thấy đường thì trả về `None`).
     * Nếu tìm thấy đường đi $P$ từ $S \to T$:
       * `step += 1`
       * Tìm lượng luồng nghẽn cổ chai: $\Delta f = \min_{(u, v) \in P} \text{residual}[u][v]$.
       * Cập nhật lại đồ thị thặng dư dọc theo đường $P$:
         * Giảm chiều xuôi: $\text{residual}[u][v] -= \Delta f$.
         * Tăng chiều ngược: $\text{residual}[v][u] += \Delta f$.
       * Tăng tổng luồng: `max_flow += Δf`.
       * Ghi vết: `trace_table.append({"step": step, "path": P, "bottleneck": Δf, "max_flow": max_flow})`.
     * Nếu không còn tìm thấy đường nào nữa $\implies$ Kết thúc vòng lặp!

---

#### 🔹 3.2 Tìm Lát cắt hẹp nhất (Min Cut):
1. Dùng BFS/DFS xuất phát từ `source` trên đồ thị thặng dư `residual` cuối cùng:
   * Tập $S$: Tất cả các đỉnh mà `source` có thể đi tới được (qua các cạnh còn dư `residual[u][v] > 0`).
   * Tập $T$: Các đỉnh còn lại ($V \setminus S$).
2. Xác định danh sách các cạnh thuộc Lát cắt hẹp nhất (`min_cut_edges`):
   * Duyệt qua tất cả các cung gốc $(u, v, cap)$ ban đầu:
   * Nếu $u \in S$ và $v \in T$ $\implies$ Cung $(u, v)$ thuộc Lát cắt hẹp nhất!
3. Tính ma trận luồng thực tế trên từng cạnh: `flow_matrix[u][v] = capacity[u][v] - residual[u][v]`.
* **Output trả về**: `max_flow: int/float`, `flow_matrix: list[list]`, `min_cut_edges: list[tuple]`, `cut_sets: (set(S), set(T))`, `trace_table: list[dict]`.

---

# 👤 4. NHẬT TRƯỜNG — TRỰC QUAN HÓA NÂNG CAO

* **File cần mở**: `visualizer/draw.py`
* **Ý nghĩa**: Biến các kết quả mảng số/tuple của 3 bạn trên thành **hình vẽ đồ thị trực quan, đẹp mắt và chuyên nghiệp** lưu ra file ảnh PNG bằng `matplotlib` + `networkx`.

---

### 📌 CÁC HÀM TRƯỜNG CẦN VIẾT:

#### 🔹 4.1 Hàm `draw_euler(g, path, edges_order, filename="euler_path.png")`
* **Input**: `g` (đối tượng Graph), `path` (danh sách đỉnh Euler), `edges_order` (danh sách cạnh Euler theo thứ tự).
* **Cách vẽ**:
  1. Vẽ đồ thị nền màu xám nhạt (`#cfd8dc`).
  2. Vẽ các cạnh trong `edges_order` bằng màu Cam/Đỏ nét đậm (`#ff5722`, `linewidth=2.5`).
  3. **Đặc biệt**: Viết số thứ tự bước đi $1, 2, 3...$ tại trung điểm của mỗi cạnh Euler để người xem biết chặng nào đi trước, chặng nào đi sau!
  4. Đỉnh bắt đầu tô màu Xanh Lá (`#00e676`), đỉnh kết thúc tô màu Đỏ (`#d50000`).
  5. Lưu ảnh: `plt.savefig(filename, dpi=300, bbox_inches='tight')`.

---

#### 🔹 4.2 Hàm `draw_mst(g, mst_edges, total_weight, filename="mst_result.png")`
* **Input**: `g` (đối tượng Graph), `mst_edges` (list các cạnh MST), `total_weight` (tổng trọng số).
* **Cách vẽ**:
  1. Các cạnh **thuộc cây khung MST**: Vẽ màu Xanh Dương đậm nét to (`#2979ff`, `linewidth=3.0`), ghi rõ số trọng số $w$ màu xanh.
  2. Các cạnh **không thuộc MST**: Vẽ nét đứt mờ màu xám (`linestyle="--"`, `#90a4ae`).
  3. Tiêu đề ảnh (Title): `f"CÂY KHUNG NHỎ NHẤT (MST) — Tổng trọng số = {total_weight}"`.
  4. Lưu ảnh: `plt.savefig(filename, dpi=300, bbox_inches='tight')`.

---

#### 🔹 4.3 Hàm `draw_max_flow(g, flow_matrix, min_cut_edges, max_flow, source, sink, filename="max_flow.png")`
* **Input**: `g` (đối tượng Graph), `flow_matrix` (ma trận luồng), `min_cut_edges` (các cạnh lát cắt), `max_flow`, `source`, `sink`.
* **Cách vẽ**:
  1. Trên mỗi cung $(u, v)$: Hiển thị nhãn dạng `f"{flow}/{cap}"` (ví dụ `8/10` nghĩa là luồng 8 trên sức chứa 10).
  2. Cung nào đã bão hòa (`flow == cap`): Tô màu Đỏ rực nét đậm.
  3. Cung nào thuộc Lát cắt hẹp nhất (`min_cut_edges`): Vẽ viền bao quanh hoặc đường cắt màu Hồng/Đỏ.
  4. Đỉnh Nguồn ($S$): Tô màu Xanh Biển (`#00e5ff`, nhãn `S - Source`).
  5. Đỉnh Đích ($T$): Tô màu Cam Đỏ (`#ff3d00`, nhãn `T - Sink`).
  6. Tiêu đề ảnh: `f"LUỒNG CỰC ĐẠI TRONG MẠNG (MAX FLOW = {max_flow}) & LÁT CẮT HẸP NHẤT"`.
  7. Lưu ảnh: `plt.savefig(filename, dpi=300, bbox_inches='tight')`.

---

# 👤 5. JACKIE KHOA (NHÓM TRƯỞNG) — BÀI TOÁN THỰC TẾ, MENU CLI & TEST SUITE

* **File đảm nhận**: `data/sample_real_world.py`, `app/cli.py`, `tests/`
* **Ý nghĩa**: Đảm nhận vai trò **Tổng công trình sư (Lead Architect & QA)** — thiết kế bài toán thực tế Mục 8 (chiếm trọng số điểm cao), ghép nối giao diện tương tác CLI, và viết bộ kiểm thử tự động toàn diện cho dự án.

---

### 📌 CÁC NHIỆM VỤ CỦA NHÓM TRƯỞNG:

#### 🔹 5.1 Thiết kế Bài toán Thực tế (Mục 8 Đề bài) — `data/sample_real_world.py`
* **Chủ đề chọn**: **Tối ưu hóa Tuyến Xe Quét Rác & Vệ Sinh Môi Trường Đô Thị (Urban Street Sweeper Routing)** bằng **Chu trình Euler (Hierholzer/Fleury)**.
* **Mô tả 4 yếu tố chuẩn đề bài**:
  1. **Bài toán thực tế đặt ra**: Xe quét đường cần xuất phát từ Trạm vệ sinh môi trường, đi quét sạch toàn bộ tất cả các tuyến đường trong khu dân cư sao cho **mỗi tuyến đường chỉ đi qua đúng 1 lần** (không đi lặp lại) rồi quay về trạm, nhằm tiết kiệm nhiên liệu và thời gian.
  2. **Đỉnh (Node) đại diện cho cái gì?**: Các ngã ba, ngã tư giao lộ đô thị (có tọa độ GPS và tên giao lộ).
  3. **Cạnh (Edge) đại diện cho cái gì?**: Các đoạn phố nối giữa các giao lộ (có tên đường cụ thể: Lê Lợi, Nguyễn Huệ, Đồng Khởi...).
  4. **Trọng số (Weight) đại diện cho cái gì?**: Chiều dài tuyến phố (tính bằng mét).
  5. **Mục tiêu**: Tìm chu trình Euler khép kín đi qua tất cả các con phố với chi phí tối ưu nhất.

---

#### 🔹 5.2 Nâng cấp Giao diện Menu CLI tương tác (`app/cli.py`)
* Ghép thêm các mục Menu Phần Nâng Cao:
  * `[7.1]` Tìm chu trình / đường đi Euler bằng thuật toán Fleury
  * `[7.2]` Tìm chu trình / đường đi Euler bằng thuật toán Hierholzer
  * `[7.3]` Tìm cây khung nhỏ nhất (MST) bằng thuật toán Prim
  * `[7.4]` Tìm cây khung nhỏ nhất (MST) bằng thuật toán Kruskal (DSU)
  * `[7.5]` Tìm Luồng cực đại & Lát cắt hẹp nhất bằng Ford-Fulkerson
  * `[8]` 🚀 Chạy Demo Bài toán thực tế: Lộ trình Xe Quét Rác Đô Thị
* **Xuất Bảng ma trận & Bảng vết bước lặp**: In bảng vết chi tiết từng bước lặp ra màn hình terminal (giống như cách giải tay từng bước trên giấy thi đại học) để sinh viên dễ dàng đối chiếu.
* **Tự động gọi hàm vẽ hình**: Sau khi thuật toán chạy xong, tự động lưu ảnh ra file PNG và thông báo cho người dùng.

---

#### 🔹 5.3 Xây dựng Bộ Kiểm Thử Tự Động Toàn Diện (`tests/`)
* Viết 4 file test kiểm thử tự động với `assert` chặt chẽ:
  1. `tests/test_euler.py`: Test đồ thị có chu trình Euler, đồ thị có đường đi Euler, đồ thị không có Euler (bậc lẻ $>2$), đồ thị không liên thông.
  2. `tests/test_mst.py`: Test Prim và Kruskal trên đồ thị có trọng số, kiểm tra tổng trọng số MST của cả 2 thuật toán phải bằng nhau.
  3. `tests/test_max_flow.py`: Test Ford-Fulkerson trên mạng luồng chuẩn, kiểm tra Max Flow = Min Cut.
  4. `tests/test_draw.py`: Test sinh ra đầy đủ các file ảnh PNG mà không bị lỗi thư viện.
* Chạy lệnh kiểm thử toàn diện:
  ```bash
  .venv/bin/python3 -m unittest discover tests/
  ```

---

# 🚀 TỔNG KẾT QUY TRÌNH LÀM VIỆC CỦA NHÓM

1. **Bước 1**: Mỗi bạn tạo nhánh git riêng của mình:
   * Thanh: `git checkout -b feature/euler-dothanh`
   * Linh: `git checkout -b feature/mst-linh`
   * Tuấn: `git checkout -b feature/maxflow-tuan`
   * Trường: `git checkout -b feature/draw-nhattuong`
   * Khoa: `git checkout -b feature/cli-realworld-khoa`
2. **Bước 2**: Code xong phần của mình $\implies$ Nhóm trưởng Jackie Khoa sẽ chạy file test tương ứng để nghiệm thu.
3. **Bước 3**: Sau khi test pass 100% $\implies$ Tạo Pull Request gộp vào nhánh `main`.

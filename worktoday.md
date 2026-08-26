# BẢNG PHÂN CÔNG & TIẾN ĐỘ THỰC HIỆN DỰ ÁN CTRR

Tài liệu hướng dẫn chi tiết công việc cho từng thành viên trong nhóm 5 người.

---

# 📊 BẢNG TIẾN ĐỘ & PHÂN CÔNG NHIỆM VỤ

| Thành viên | Tên file đảm nhận | Nhiệm vụ chính | Trạng thái |
|:---|:---|:---|:---:|
| **Nhóm trưởng (Bạn)** | `core/converter.py` & `core/graph.py` | Nền tảng dữ liệu `Graph` & Chuyển đổi 3 dạng | ✅ **ĐÃ XONG 100%** |
| **Nhật Trường (Người B)** | `visualizer/draw.py` | Vẽ đồ thị & Lưu ảnh PNG bằng matplotlib | ⏳ Đang làm |
| **Đỗ Thanh (Người C)** | `core/traversal.py` | Duyệt BFS, DFS + Bảng vết chạy tay | ⏳ Đang làm |
| **Tuấn (Người D)** | `core/bipartite.py` | Kiểm tra Đồ thị 2 phía & Chu trình lẻ | ⏳ Đang làm |
| **Linh (Người E)** | `core/shortest_path.py` | Dijkstra & Bellman-Ford + Bảng ma trận | ⏳ Đang làm |
| **Cả nhóm (Ngày 2)** | `run_demo.py` | Ghép nối và chạy Demo tổng hợp | ⏸️ Chờ 4 bạn xong |

---

# 👤 1. NHẬT TRƯỜNG (NGƯỜI B) — VẼ VÀ LƯU ẢNH ĐỒ THỊ

> **File cần mở**: `visualizer/draw.py`  
> **Dữ liệu nhận vào từ Graph**: `g.n` (số đỉnh), `g.edges` (danh sách cạnh), `g.directed` (True/False).

### 🎯 Hướng dẫn tư duy và thực hiện:
1. **Tính tọa độ $n$ đỉnh trên đường tròn**:
   * Góc của đỉnh $i$: $\theta_i = \frac{2\pi \cdot i}{n}$
   * Tọa độ: $x_i = 10 \cdot \cos(\theta_i), \quad y_i = 10 \cdot \sin(\theta_i)$
2. **Vẽ các cạnh**:
   * Duyệt từng cạnh `(u, v, w)` trong `edges`: lấy tọa độ $(x_u, y_u)$ và $(x_v, y_v)$.
   * Nếu cạnh nằm trong list `highlight` $\implies$ tô màu ĐỎ nét đậm. Ngược lại tô màu XÁM.
   * Nếu `directed == False`: vẽ đoạn thẳng `plt.plot()`.
   * Nếu `directed == True`: vẽ mũi tên `ax.annotate()` với `arrowstyle="->"`.
   * Nếu trọng số $w \ne 1$: viết số trọng số tại trung điểm $\left(\frac{x_u+x_v}{2}, \frac{y_u+y_v}{2}\right)$.
3. **Vẽ các đỉnh**:
   * Vẽ hình tròn tại mỗi $(x_i, y_i)$ bằng `plt.Circle()`.
   * Màu đỉnh: lấy từ dict `colors` (ví dụ: `{0: 'red', 1: 'blue'}` khi vẽ đồ thị 2 phía) hoặc mặc định màu xanh lá.
   * Viết số hiệu đỉnh (0, 1, 2...) màu trắng tại tâm.
4. **Lưu file**:
   * Gọi `plt.savefig(filename, dpi=300, bbox_inches='tight')`.

### 🧪 Lệnh test nhanh cho Nhật Trường:
Mở Terminal gõ:
```bash
python3 tests/test_draw.py
```

---

# 👤 2. ĐỖ THANH (NGƯỜI C) — THUẬT TOÁN DUYỆT BFS & DFS

> **File cần mở**: `core/traversal.py`  
> **Dữ liệu nhận vào từ Graph**: `g.adj` (danh sách kề), `g.n` (số đỉnh), `start` (đỉnh bắt đầu).

### 🎯 Hướng dẫn tư duy và thực hiện:

#### A. Hàm `bfs(adj, n, start)` (Duyệt chiều rộng)
1. Tạo `visited = [False] * n`, `parent = [-1] * n`, `queue = [start]`, `visited[start] = True`.
2. Tạo danh sách kết quả: `order = []`, `tree_edges = []`, `trace_table = []`.
3. Vòng lặp `while len(queue) > 0:`
   * Lấy phần tử đầu: `u = queue.pop(0)`.
   * Thêm `u` vào `order`.
   * Lấy danh sách đỉnh kề của `u`, **bắt buộc `sorted` tăng dần**: `neighbors = sorted([v for v, w in adj.get(u, [])])`.
   * Với mỗi $v \in neighbors$: nếu `not visited[v]`:
     * Đánh dấu `visited[v] = True`, `parent[v] = u`.
     * Đẩy vào cuối queue: `queue.append(v)`.
     * Ghi nhận cạnh cây khung: `tree_edges.append((u, v))`.
   * Lưu 1 dòng vết vào `trace_table`: `{"step": len(order), "u": u, "queue": list(queue), "visited": list(visited)}`.
4. `return order, tree_edges, trace_table`.

#### B. Hàm `dfs(adj, n, start)` (Duyệt chiều sâu)
1. Tạo `visited = [False] * n`, `order = []`, `tree_edges = []`, `trace_table = []`.
2. Viết hàm đệ quy `dfs_visit(u)`:
   * `visited[u] = True`, thêm `u` vào `order`.
   * Lưu 1 dòng vết vào `trace_table`.
   * Lấy các đỉnh kề của `u` (`sorted` tăng dần): với mỗi $v$ chưa thăm $\implies$ thêm `(u, v)` vào `tree_edges` và gọi đệ quy `dfs_visit(v)`.
3. Gọi `dfs_visit(start)`.
4. `return order, tree_edges, trace_table`.

### 🧪 Lệnh test nhanh cho Đỗ Thanh:
Mở Terminal gõ:
```bash
python3 tests/test_traversal.py
```

---

# 👤 3. TUẤN (NGƯỜI D) — KIỂM TRA ĐỒ THỊ HAI PHÍA (BIPARTITE)

> **File cần mở**: `core/bipartite.py`  
> **Dữ liệu nhận vào từ Graph**: `g.adj` (danh sách kề), `g.n` (số đỉnh).

### 🎯 Hướng dẫn tư duy và thực hiện:

#### Hàm `check_bipartite(adj, n)`
1. Tạo mảng màu `color = [0] * n` (`0`: chưa tô, `1`: màu Đỏ, `-1`: màu Xanh) và `parent = [-1] * n`.
2. Lặp qua tất cả các đỉnh `for i in range(n):` (xử lý cả đồ thị không liên thông):
   * Nếu `color[i] == 0`:
     * Gán `color[i] = 1`, `queue = [i]`.
     * Vòng lặp BFS `while queue:`
       * `u = queue.pop(0)`.
       * Với mỗi đỉnh $v$ kề $u$ (`for v, w in adj.get(u, []):`):
         * **Nếu `color[v] == 0` (chưa tô)**: gán màu ngược lại `color[v] = -color[u]`, `parent[v] = u`, `queue.append(v)`.
         * **Nếu `color[v] == color[u]` (XUNG ĐỘT MÀU!)**:
           * Đồ thị KHÔNG là 2 phía.
           * Lần ngược `parent` từ $u$ và $v$ về gốc chung để trích xuất danh sách đỉnh của **Chu trình lẻ**.
           * `return {"is_bipartite": False, "odd_cycle": [danh_sách_đỉnh]}`.
3. Nếu tô xong toàn bộ mà không xung đột:
   * Tập 1 (Đỏ): `v1 = [i for i in range(n) if color[i] == 1]`.
   * Tập 2 (Xanh): `v2 = [i for i in range(n) if color[i] == -1]`.
   * `return {"is_bipartite": True, "v1": v1, "v2": v2, "colors": {i: ('red' if color[i]==1 else 'blue') for i in range(n)}}`.

### 🧪 Lệnh test nhanh cho Tuấn:
Mở Terminal gõ:
```bash
python3 tests/test_bipartite.py
```

---

# 👤 4. LINH (NGƯỜI E) — ĐƯỜNG ĐI NGẮN NHẤT (DIJKSTRA & BELLMAN-FORD)

> **File cần mở**: `core/shortest_path.py`  
> **Dữ liệu nhận vào từ Graph**: `g.adj`, `g.edges`, `g.n`, `start`, `end`.

### 🎯 Hướng dẫn tư duy và thực hiện:

#### A. Hàm `dijkstra(adj, n, start, end=None)` (Cho trọng số $\ge 0$)
1. `dist = [float('inf')] * n`, `visited = [False] * n`, `parent = [-1] * n`, `dist[start] = 0`, `trace = []`.
2. Lặp $n$ lần:
   * Tìm đỉnh $u$ chưa thăm (`not visited[u]`) có `dist[u]` nhỏ nhất. Nếu `dist[u] == inf` $\implies$ break.
   * `visited[u] = True` (chốt $u$).
   * Lưu 1 dòng vết: `trace.append({"step": step+1, "u": u, "dist": list(dist), "parent": list(parent)})`.
   * Nới lỏng cạnh: Với mỗi $v, w$ kề $u$:
     * Nếu `not visited[v]` và `dist[u] + w < dist[v]`:
       * `dist[v] = dist[u] + w`, `parent[v] = u`.
3. Phục hồi đường đi `path`: Nếu có `end`, lần ngược `parent` từ `end` về `start` rồi đảo ngược.
4. `return {"dist": dist, "parent": parent, "path": path, "cost": dist[end] if end is not None else None, "trace": trace}`.

#### B. Hàm `bellman_ford(edges, n, start, directed=False, end=None)` (Xử lý trọng số âm)
1. `dist = [float('inf')] * n`, `parent = [-1] * n`, `dist[start] = 0`, `trace = []`.
2. Nếu `directed == False`: nhân đôi mỗi cạnh `(u, v, w)` thành cả `(v, u, w)`.
3. Lặp $n-1$ vòng:
   * `changed = False`
   * Quét mọi cạnh `(u, v, w)`: nếu `dist[u] != inf` và `dist[u] + w < dist[v]`:
     * `dist[v] = dist[u] + w`, `parent[v] = u`, `changed = True`.
   * Lưu vết mảng `dist` sau mỗi vòng.
   * Nếu `not changed`: break sớm.
4. **Vòng thứ $n$ (kiểm tra chu trình âm)**:
   * `has_neg = False`
   * Quét lại cạnh: nếu vẫn còn cạnh mà `dist[u] + w < dist[v]` $\implies$ `has_neg = True`.
5. Phục hồi `path` giống Dijkstra.
6. `return {"dist": dist, "parent": parent, "path": path, "cost": dist[end] if end is not None else None, "has_negative_cycle": has_neg, "trace": trace}`.

### 🧪 Lệnh test nhanh cho Linh:
Mở Terminal gõ:
```bash
python3 tests/test_shortest_path.py
```

---

# 🚀 5. BƯỚC GHÉP NỐI TOÀN BỘ (NGÀY 2) — `run_demo.py`

Khi cả 4 bạn hoàn thành, Nhóm trưởng sẽ mở file `run_demo.py` và chạy lệnh tổng hợp:
```bash
python3 run_demo.py
```

# HƯỚNG DẪN CHI TIẾT TỪNG BƯỚC CHO 5 THÀNH VIÊN (WORK TODAY)

Tài liệu này hướng dẫn chi tiết từng bước cho từng người: **Mở file nào -> Tham số đầu vào là gì -> Viết logic ra sao -> Trả về kết quả gì -> Chạy lệnh nào để test**.

---

# 🗺️ BẢN ĐỒ PHỤ THUỘC (AI LÀM TRƯỚC, AI LÀM SAU)

```
[BƯỚC 1: Buổi Sáng]
Người A: Viết core/converter.py + core/graph.py  (LÀM XONG TRƯỚC 11h)
Người B: Viết visualizer/draw.py                 (LÀM XONG TRƯỚC 11h)

[BƯỚC 2: Buổi Chiều] (Khi Người A đã xong)
Người C: Viết core/traversal.py     (BFS & DFS)
Người D: Viết core/bipartite.py     (Kiểm tra 2 phía)
Người E: Viết core/shortest_path.py (Dijkstra & Bellman-Ford)

[BƯỚC 3: Ngày 2]
Cả 5 người: Mở run_demo.py ghép lại và chạy test toàn bộ!
```

---

# 👤 1. NGƯỜI A (NHÓM TRƯỞNG) — LÀM NỀN TẢNG DỮ LIỆU

> **Nhiệm vụ**: Tạo ra công cụ biến đổi dữ liệu đồ thị để các bạn khác có dữ liệu mà chạy thuật toán.

### 📄 File 1: Mở `core/converter.py` và viết 6 hàm:

#### 1. `matrix_to_adj(matrix, directed=False)`
* **Đầu vào (`matrix`)**: Mảng 2 chiều, ví dụ `[[0, 5], [5, 0]]` (đồ thị 2 đỉnh, cạnh 0-1 có trọng số 5).
* **Cách làm**:
  1. Tạo `adj = {i: [] for i in range(len(matrix))}`
  2. Dùng 2 vòng lặp: `for i in range(n):` `for j in range(n):`
  3. Nếu `matrix[i][j] != 0` -> Thêm `(j, matrix[i][j])` vào `adj[i]`
* **Đầu ra**: Trả về `{0: [(1, 5)], 1: [(0, 5)]}`

#### 2. `matrix_to_edges(matrix, directed=False)`
* **Cách làm**:
  1. Tạo list rỗng `edges = []`
  2. Nếu `directed == True`: duyệt hết ô $(i, j)$
  3. Nếu `directed == False`: chỉ duyệt $j \ge i$ (để không bị lặp lại cạnh ngược lại)
  4. Nếu `matrix[i][j] != 0` -> thêm `(i, j, matrix[i][j])` vào `edges`
* **Đầu ra**: Trả về `[(0, 1, 5)]`

#### 3. `edges_to_matrix(edges, n, directed=False)`
* **Đầu vào**: `edges = [(0, 1, 5)]`, số đỉnh `n = 2`
* **Cách làm**:
  1. Tạo ma trận toàn số 0: `M = [[0]*n for _ in range(n)]`
  2. Duyệt từng `(u, v, w)` trong `edges`: gán `M[u][v] = w`
  3. Nếu `directed == False`: gán thêm `M[v][u] = w`
* **Đầu ra**: Trả về `[[0, 5], [5, 0]]`

#### 4. `edges_to_adj(edges, n, directed=False)`
* **Cách làm**:
  1. Tạo `adj = {i: [] for i in range(n)}`
  2. Duyệt từng `(u, v, w)`: `adj[u].append((v, w))`
  3. Nếu `directed == False`: `adj[v].append((u, w))`
* **Đầu ra**: Trả về `{0: [(1, 5)], 1: [(0, 5)]}`

#### 5. `adj_to_matrix(adj, n)`
* **Cách làm**:
  1. Tạo ma trận `M = [[0]*n for _ in range(n)]`
  2. Duyệt `for u, neighbors in adj.items():`
  3. Duyệt `for v, w in neighbors:` gán `M[u][v] = w`
* **Đầu ra**: Trả về `[[0, 5], [5, 0]]`

#### 6. `adj_to_edges(adj, directed=False)`
* **Cách làm**:
  1. Tạo `edges = []`
  2. Duyệt qua dict `adj`: nếu `directed == True` hoặc `u <= v` thì thêm `(u, v, w)`
* **Đầu ra**: Trả về list các cạnh `[(0, 1, 5)]`

---

### 📄 File 2: Mở `core/graph.py` và viết Class `Graph`:
Class này chỉ cần gọi các hàm từ `converter.py` đã viết ở trên:
```python
from core.converter import *

class Graph:
    def __init__(self, n=0, directed=False, weighted=False):
        self.n = n
        self.directed = directed
        self.weighted = weighted
        self.matrix = [[0]*n for _ in range(n)]
        self.adj = {i: [] for i in range(n)}
        self.edges = []

    def from_matrix(self, matrix):
        self.n = len(matrix)
        self.matrix = matrix
        self.adj = matrix_to_adj(matrix, self.directed)
        self.edges = matrix_to_edges(matrix, self.directed)
        return self

    def from_edges(self, edges, n):
        self.n = n
        self.edges = edges
        self.matrix = edges_to_matrix(edges, n, self.directed)
        self.adj = edges_to_adj(edges, n, self.directed)
        return self

    def from_text(self, text):
        lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
        first_line = lines[0].split()
        if len(first_line) == 1: # Là Ma trận
            n = int(first_line[0])
            mat = [[int(x) for x in l.split()] for l in lines[1:n+1]]
            self.from_matrix(mat)
        else: # Là Danh sách cạnh
            edges = []
            for l in lines:
                p = l.split()
                edges.append((int(p[0]), int(p[1]), int(p[2]) if len(p)>=3 else 1))
            self.from_edges(edges, max(max(u, v) for u, v, *r in edges) + 1)
        return self
```

---

# 👤 2. NGƯỜI B — LÀM PHẦN VẼ HÌNH ĐỒ THỊ

> **Nhiệm vụ**: Nhận danh sách đỉnh và cạnh, dùng `matplotlib` vẽ thành file ảnh `.png`.

### 📄 File cần mở: `visualizer/draw.py`
Viết hàm `draw(...)`:
```python
import matplotlib.pyplot as plt
import math

def draw(n, edges, directed=False, filename="graph.png", colors=None, highlight=None, title=None):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axis('off')
    
    # 1. Tính tọa độ tròn cho n đỉnh
    pos = {}
    for i in range(n):
        angle = 2 * math.pi * i / n
        pos[i] = (10 * math.cos(angle), 10 * math.sin(angle))
        
    # 2. Vẽ các cạnh
    hl_set = set(highlight) if highlight else set()
    for u, v, *w in edges:
        weight = w[0] if w else 1
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        is_hl = (u, v) in hl_set or (v, u) in hl_set
        color = 'red' if is_hl else 'gray'
        lw = 2.5 if is_hl else 1.2
        
        if directed:
            ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="->", color=color, lw=lw, shrinkA=15, shrinkB=15))
        else:
            ax.plot([x1, x2], [y1, y2], color=color, lw=lw)
            
        if weight != 1:
            ax.text((x1+x2)/2, (y1+y2)/2, str(weight), color='blue', fontsize=10)

    # 3. Vẽ các đỉnh tròn
    for i in range(n):
        x, y = pos[i]
        c = colors.get(i, '#4CAF50') if colors else '#4CAF50'
        circle = plt.Circle((x, y), 1.2, color=c, ec='black', zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, str(i), color='white', weight='bold', ha='center', va='center', zorder=3)
        
    if title:
        plt.title(title)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
```

---

# 👤 3. NGƯỜI C — LÀM THUẬT TOÁN DUYỆT BFS & DFS

> **Nhiệm vụ**: Duyệt đồ thị từ 1 đỉnh, lưu lại thứ tự duyệt, cây khung và BẢNG VẾT để đối chiếu chạy tay.

### 📄 File cần mở: `core/traversal.py`

#### 1. Hàm `bfs(adj, n, start)`
* **Đầu vào**: `adj` (danh sách kề dạng `{0: [(1, 1), (2, 1)], ...}`), `n` (số đỉnh), `start` (đỉnh bắt đầu).
* **Cách code từng bước**:
  1. Tạo `visited = [False]*n`, `queue = [start]`, `visited[start] = True`
  2. Tạo `order = []`, `tree_edges = []`, `trace = []`
  3. Vòng lặp `while len(queue) > 0:`
     - `u = queue.pop(0)` (lấy phần tử đầu tiên)
     - `order.append(u)`
     - Lấy các đỉnh kề $v$ của $u$, **nhớ sort tăng dần**: `neighbors = sorted([v for v, w in adj.get(u, [])])`
     - Với mỗi $v$: nếu `not visited[v]`:
       - `visited[v] = True`
       - `queue.append(v)`
       - `tree_edges.append((u, v))`
     - Lưu 1 dòng trace: `trace.append({"step": len(order), "u": u, "queue": list(queue), "visited": list(visited)})`
* **Đầu ra**: `return order, tree_edges, trace`

#### 2. Hàm `dfs(adj, n, start)`
* **Cách code từng bước**:
  1. Tạo `visited = [False]*n`, `order = []`, `tree_edges = []`, `trace = []`
  2. Viết hàm con đệ quy:
     ```python
     def dfs_visit(u):
         visited[u] = True
         order.append(u)
         trace.append({"u": u, "visited": list(visited)})
         neighbors = sorted([v for v, w in adj.get(u, [])])
         for v in neighbors:
             if not visited[v]:
                 tree_edges.append((u, v))
                 dfs_visit(v)
     ```
  3. Gọi `dfs_visit(start)`
* **Đầu ra**: `return order, tree_edges, trace`

---

# 👤 4. NGƯỜI D — LÀM KIỂM TRA ĐỒ THỊ HAI PHÍA (BIPARTITE)

> **Nhiệm vụ**: Dùng thuật toán tô 2 màu (Đỏ / Xanh). Nếu tô được -> Là 2 phía (xuất 2 tập). Nếu 2 đỉnh kề cùng màu -> Không 2 phía (trích chu trình lẻ).

### 📄 File cần mở: `core/bipartite.py`
Viết hàm `check_bipartite(adj, n)`:
* **Cách code từng bước**:
  1. Tạo `color = [0]*n` (0: Chưa tô, 1: Đỏ, -1: Xanh) và `parent = [-1]*n`
  2. Lặp qua tất cả đỉnh `for i in range(n):` (để duyệt hết các nhánh rời nhau):
     - Nếu `color[i] == 0`:
       - Gán `color[i] = 1`, `queue = [i]`
       - `while queue:`
         - `u = queue.pop(0)`
         - Duyệt qua đỉnh kề $v$ của $u$ (`for v, w in adj.get(u, []):`):
           - **Nếu `color[v] == 0`**: Gán màu ngược lại `color[v] = -color[u]`, `parent[v] = u`, đẩy `queue.append(v)`
           - **Nếu `color[v] == color[u]`**: (XUNG ĐỘT MÀU!)
             - Đồ thị KHÔNG 2 phía.
             - Tìm chu trình lẻ: Lần ngược `parent` từ $u$ và $v$ về gốc chung.
             - `return {"is_bipartite": False, "odd_cycle": [danh_sách_đỉnh_chu_trình_lẻ]}`
  3. Nếu duyệt xong hết mà không xung đột:
     - `v1 = [i for i in range(n) if color[i] == 1]`
     - `v2 = [i for i in range(n) if color[i] == -1]`
     - `return {"is_bipartite": True, "v1": v1, "v2": v2}`

---

# 👤 5. NGƯỜI E — LÀM ĐƯỜNG ĐI NGẮN NHẤT (DIJKSTRA & BELLMAN-FORD)

> **Nhiệm vụ**: Tìm đường đi ngắn nhất từ `start` đến `end`, lưu bảng vết từng bước và bắt chu trình âm.

### 📄 File cần mở: `core/shortest_path.py`

#### 1. Hàm `dijkstra(adj, n, start, end=None)`
* **Cách code từng bước**:
  1. `dist = [float('inf')]*n`, `visited = [False]*n`, `parent = [-1]*n`
  2. `dist[start] = 0`, `trace = []`
  3. Lặp `for step in range(n):`
     - Tìm đỉnh $u$ chưa thăm (`not visited[u]`) có `dist[u]` nhỏ nhất
     - Nếu không tìm được hoặc `dist[u] == inf` -> `break`
     - Đánh dấu `visited[u] = True`
     - Lưu 1 dòng trace: `trace.append({"step": step+1, "u": u, "dist": list(dist)})`
     - Nới lỏng cạnh: Với mỗi $v, w$ kề $u$:
       - Nếu `not visited[v]` và `dist[u] + w < dist[v]`:
         - `dist[v] = dist[u] + w`
         - `parent[v] = u`
  4. Phục hồi đường đi `path`: Nếu có `end`, đi ngược từ `end` về `start` bằng `parent`:
     ```python
     path = []
     curr = end
     while curr != -1:
         path.append(curr)
         curr = parent[curr]
     path.reverse()
     ```
* **Đầu ra**: `return {"dist": dist, "parent": parent, "path": path, "cost": dist[end], "trace": trace}`

#### 2. Hàm `bellman_ford(edges, n, start, directed=False, end=None)`
* **Cách code từng bước**:
  1. `dist = [float('inf')]*n`, `parent = [-1]*n`, `dist[start] = 0`, `trace = []`
  2. Chuẩn bị danh sách cạnh: nếu `directed == False`, nhân đôi mỗi cạnh `(u, v, w)` thành cả `(v, u, w)`
  3. Lặp $n-1$ vòng (`for k in range(1, n):`):
     - `changed = False`
     - Duyệt qua tất cả cạnh `(u, v, w)`:
       - Nếu `dist[u] != inf` và `dist[u] + w < dist[v]`:
         - `dist[v] = dist[u] + w`
         - `parent[v] = u`
         - `changed = True`
     - Lưu trace vòng lặp: `trace.append({"round": k, "dist": list(dist)})`
     - Nếu `not changed`: `break` (dừng sớm)
  4. **Vòng thứ $n$ (bắt chu trình âm)**:
     - `has_neg_cycle = False`
     - Quét lại toàn bộ cạnh: nếu vẫn còn cạnh mà `dist[u] + w < dist[v]` -> `has_neg_cycle = True`
* **Đầu ra**: `return {"dist": dist, "parent": parent, "path": path, "cost": dist[end], "has_negative_cycle": has_neg_cycle, "trace": trace}`

---

# 🚀 TỔNG KẾT: CÁCH 5 BẠN LÀM VIỆC CÙNG NHAU

1. **Sáng Ngày 1**:
   - Bạn (Người A) ngồi code `converter.py` và `graph.py`.
   - Người B ngồi code `draw.py`.
   - C, D, E đọc tài liệu này để hiểu biến đầu vào/đầu ra.
2. **Trưa Ngày 1 (Khoảng 11h)**:
   - Bạn A báo: *"Tôi đã xong Graph và Converter rồi!"*
   - C, D, E lấy code của A về và bắt đầu viết hàm của mình.
3. **Chiều Ngày 1**:
   - C code `traversal.py`
   - D code `bipartite.py`
   - E code `shortest_path.py`
   - Mỗi người tự chạy đoạn test nhanh ở cuối phần của mình.
4. **Ngày 2**:
   - Mở `run_demo.py` ghép tất cả lại và chạy 1 lệnh là xong toàn bộ phần cơ bản!

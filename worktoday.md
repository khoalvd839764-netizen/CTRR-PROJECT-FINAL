# HƯỚNG DẪN CÁCH TƯ DUY VÀ TRIỂN KHAI CHO 5 THÀNH VIÊN (WORK TODAY)

Tài liệu này không chứa mã nguồn dài dòng, mà tập trung giải thích **CÁCH CODE TỪNG BƯỚC** và **TẠI SAO LẠI LÀM NHƯ VẬY** để từng thành viên tự hiểu bản chất và tự tay gõ code.

---

# 🗺️ THỨ TỰ THỰC HIỆN CỦA NHÓM

```
[NGÀY 1 - BUỔI SÁNG]
- Người A (Nhóm trưởng): Làm nền tảng dữ liệu (converter.py + graph.py)  --> XONG TRƯỚC 11H
- Người B: Làm module vẽ hình (draw.py)                                 --> XONG TRƯỚC 11H

[NGÀY 1 - BUỔI CHIỀU] (Sau khi Người A xong)
- Người C: Làm duyệt đồ thị (traversal.py: BFS & DFS)
- Người D: Làm kiểm tra đồ thị 2 phía (bipartite.py)
- Người E: Làm đường đi ngắn nhất (shortest_path.py: Dijkstra & Bellman-Ford)

[NGÀY 2]
- Cả 5 người: Mở run_demo.py ghép nối và chạy thử nghiệm toàn bộ.
```

---

# 👤 1. NGƯỜI A (NHÓM TRƯỞNG) — NỀN TẢNG CHUYỂN ĐỔI & LỚP GRAPH

---

### 📄 File 1: `core/converter.py`

#### 1. Hàm `matrix_to_adj(matrix, directed=False)`
* **Đầu vào**: Ma trận vuông $N \times N$ (ô $(i, j)$ chứa trọng số cạnh $i \to j$).
* **Cách code**:
  1. Tạo một dictionary với $N$ đỉnh: `{0: [], 1: [], ..., N-1: []}`.
  2. Dùng 2 vòng lặp lồng nhau duyệt qua từng dòng $i$ và từng cột $j$.
  3. Nếu ô `matrix[i][j]` khác 0 $\implies$ thêm cặp `(j, matrix[i][j])` vào danh sách của đỉnh $i$.
* **Tại sao làm vậy?** 
  * Ma trận kề tốn bộ nhớ $O(V^2)$, trong khi Danh sách kề chỉ tốn $O(V + E)$. Chuyển sang Danh sách kề giúp các thuật toán như BFS, DFS, Dijkstra duyệt qua các đỉnh kề của đỉnh $u$ cực nhanh mà không phải duyệt qua những đỉnh không có nối.

#### 2. Hàm `matrix_to_edges(matrix, directed=False)`
* **Cách code**:
  1. Tạo một danh sách rỗng.
  2. Nếu là đồ thị **có hướng**: duyệt toàn bộ các ô $(i, j)$.
  3. Nếu là đồ thị **vô hướng**: chỉ duyệt nửa trên của ma trận ($j \ge i$).
  4. Nếu ô khác 0 $\implies$ thêm bộ ba `(i, j, weight)` vào danh sách.
* **Tại sao chỉ duyệt $j \ge i$ khi vô hướng?**
  * Vì trong đồ thị vô hướng, cạnh $(0, 1)$ và cạnh $(1, 0)$ là cùng một cạnh duy nhất. Nếu duyệt toàn bộ ma trận, bạn sẽ bị lặp cạnh 2 lần $\implies$ sai lệch khi tính số cạnh và làm thuật toán Kruskal/Bellman-Ford duyệt thừa.

#### 3. Hàm `edges_to_matrix(edges, n, directed=False)`
* **Cách code**:
  1. Tạo ma trận kích thước $n \times n$ chứa toàn số 0.
  2. Duyệt qua từng bộ `(u, v, w)` trong danh sách cạnh: gán ô `matrix[u][v] = w`.
  3. Nếu `directed == False`: gán thêm ô đối xứng `matrix[v][u] = w`.
* **Tại sao phải gán đối xứng?**
  * Đồ thị vô hướng có tính chất đối xứng qua đường chéo chính: đi từ $u \to v$ cũng chính là đi từ $v \to u$ với cùng chi phí $w$.

#### 4. Hàm `edges_to_adj(edges, n, directed=False)`
* **Cách code**:
  1. Tạo dictionary rỗng cho $n$ đỉnh.
  2. Duyệt qua từng cạnh `(u, v, w)`: nạp `(v, w)` vào `adj[u]`.
  3. Nếu vô hướng: nạp thêm `(u, w)` vào `adj[v]`.
* **Tại sao làm vậy?**
  * Để khi đứng tại đỉnh $v$, ta cũng biết được $v$ có nối về $u$.

#### 5. Hàm `adj_to_matrix(adj, n)` & `adj_to_edges(adj, directed=False)`
* **Cách code**: Lặp qua các cặp khóa - giá trị của dictionary `adj` để trích xuất các cạnh và nạp vào ma trận hoặc danh sách cạnh tương tự như trên.

---

### 📄 File 2: `core/graph.py` (Class `Graph`)
* **Cách code**:
  1. Hàm khởi tạo `__init__`: lưu số đỉnh `self.n`, cờ `self.directed`, `self.weighted`, và 3 biến `self.matrix`, `self.adj`, `self.edges`.
  2. Các hàm `from_matrix`, `from_edges`: nhận dữ liệu vào, lưu lại và gọi ngay các hàm tương ứng từ `converter.py` để tự động cập nhật đồng bộ 2 dạng còn lại.
  3. Hàm `from_text`: đọc văn bản, kiểm tra dòng đầu (nếu chỉ có 1 số thì là Ma trận, nếu nhiều số thì là Danh sách cạnh) $\implies$ gọi `from_matrix` hoặc `from_edges`.
* **Tại sao phải làm Class `Graph`?**
  * Đóng vai trò là "Ngôi nhà chung". Người dùng chỉ cần nạp dữ liệu một lần bằng bất kỳ định dạng nào, đối tượng `Graph` sẽ tự động tính sẵn cả 3 dạng biểu diễn để sẵn sàng cung cấp cho bất kỳ thuật toán nào phía sau.

---

# 👤 2. NGƯỜI B — MODULE TRỰC QUAN HÓA (VẼ & LƯU ẢNH)

---

### 📄 File cần mở: `visualizer/draw.py`

#### Hàm `draw(n, edges, directed=False, filename="graph.png", colors=None, highlight=None, title=None)`
* **Mục đích**: Vẽ đồ thị ra màn hình phẳng và lưu thành file ảnh PNG theo yêu cầu đề bài.
* **Cách code từng bước**:
  1. **Bước 1 (Tính tọa độ các đỉnh)**:
     * Chia đường tròn $360^\circ$ ($2\pi$ radian) thành $n$ phần bằng nhau.
     * Tọa độ đỉnh thứ $i$: $x_i = R \cdot \cos\left(\frac{2\pi \cdot i}{n}\right)$, $y_i = R \cdot \sin\left(\frac{2\pi \cdot i}{n}\right)$.
     * *Tại sao xếp theo hình tròn?* Vì các đỉnh cách đều nhau, không bao giờ bị đè lên nhau, nhìn rất đẹp và cân đối.
  2. **Bước 2 (Vẽ các cạnh)**:
     * Lặp qua từng cạnh `(u, v, w)`. Lấy tọa độ $(x_1, y_1)$ của đỉnh $u$ và $(x_2, y_2)$ của đỉnh $v$.
     * Nếu cạnh nằm trong danh sách `highlight` $\implies$ tô màu Đỏ, nét đậm. Ngược lại tô màu Xám.
     * Nếu vô hướng: vẽ đoạn thẳng `plt.plot()`.
     * Nếu có hướng: vẽ mũi tên `ax.annotate()` chỉ từ $(x_1, y_1)$ sang $(x_2, y_2)$.
     * Nếu trọng số $w \ne 1$: viết chữ trọng số tại tọa độ trung điểm $\left(\frac{x_1+x_2}{2}, \frac{y_1+y_2}{2}\right)$.
  3. **Bước 3 (Vẽ các đỉnh)**:
     * Vẽ hình tròn tại từng $(x_i, y_i)$ bằng `plt.Circle()`.
     * Màu đỉnh lấy từ dictionary `colors` (nếu có, ví dụ Đỏ/Xanh cho Bipartite) hoặc màu mặc định xanh lá.
     * Viết số hiệu đỉnh (0, 1, 2...) màu trắng ở chính giữa hình tròn.
  4. **Bước 4 (Lưu file)**:
     * Gọi `plt.savefig(filename, dpi=300)` để xuất file ảnh chất lượng cao.

---

# 👤 3. NGƯỜI C — THUẬT TOÁN DUYỆT ĐỒ THỊ (BFS & DFS)

---

### 📄 File cần mở: `core/traversal.py`

#### 1. Hàm `bfs(adj, n, start)` (Duyệt theo chiều rộng)
* **Tư tưởng**: Như sóng nước loang, thăm hết các đỉnh cách nguồn 1 cạnh, rồi đến 2 cạnh, 3 cạnh...
* **Cấu trúc dữ liệu**: Hàng đợi **Queue (FIFO - Vào trước ra trước)**.
* **Cách code từng bước**:
  1. Tạo mảng đánh dấu `visited = [False] * n`, mảng đỉnh cha `parent = [-1] * n`.
  2. Đưa đỉnh `start` vào `queue = [start]`, đánh dấu `visited[start] = True`.
  3. Khi hàng đợi chưa rỗng (`while len(queue) > 0`):
     - Lấy phần tử ở đầu hàng đợi ra: `u = queue.pop(0)`.
     - Thêm `u` vào danh sách kết quả `bfs_order`.
     - Lấy tất cả đỉnh kề $v$ của $u$, **bắt buộc sắp xếp tăng dần** (`sorted`).
     - Với mỗi đỉnh $v$: nếu `visited[v] == False`:
       - Đánh dấu `visited[v] = True`.
       - Gán `parent[v] = u`.
       - Đẩy $v$ vào cuối hàng đợi (`queue.append(v)`).
       - Ghi nhận cạnh $(u, v)$ vào danh sách cây khung BFS (`tree_edges`).
     - Ghi nhận 1 dòng trạng thái vào `trace_table` gồm: (Bước hiện tại, đỉnh $u$ vừa lấy, trạng thái Queue sau bước này, mảng `visited`).
* **Tại sao phải `sorted` đỉnh kề tăng dần?**
  * Khi sinh viên giải tay trên giấy thi, quy ước chuẩn là luôn chọn đỉnh có nhãn nhỏ hơn trước. Nếu code không sort, thứ tự duyệt sẽ bị ngẫu nhiên và không khớp với bài giải tay.
* **Đầu ra**: Trả về `(bfs_order, tree_edges, trace_table)`.

---

#### 2. Hàm `dfs(adj, n, start)` (Duyệt theo chiều sâu)
* **Tư tưởng**: Đi một lèo đến tận cùng nhánh, khi gặp ngõ cụt mới quay lui (Backtrack) để thử nhánh khác.
* **Cấu trúc dữ liệu**: Đệ quy (sử dụng Call Stack của hệ thống).
* **Cách code từng bước**:
  1. Tạo mảng `visited = [False] * n`, danh sách `dfs_order = []`, `tree_edges = []`, `trace = []`.
  2. Viết hàm đệ quy `dfs_visit(u)`:
     - Đánh dấu `visited[u] = True`, thêm `u` vào `dfs_order`.
     - Lưu 1 dòng vết vào `trace`.
     - Lấy danh sách đỉnh kề của $u$, sắp xếp tăng dần.
     - Với mỗi đỉnh kề $v$: nếu `visited[v] == False`:
       - Thêm cạnh $(u, v)$ vào `tree_edges`.
       - Gọi đệ quy `dfs_visit(v)`.
  3. Bắt đầu bằng lệnh gọi `dfs_visit(start)`.
* **Tại sao dùng đệ quy thay vì vòng lặp Stack?**
  * Đệ quy phản ánh trực tiếp bản chất quay lui của DFS, code cực kỳ ngắn gọn (chưa tới 15 dòng) và thứ tự duyệt hoàn toàn trùng khớp với bài giải tay.
* **Đầu ra**: Trả về `(dfs_order, tree_edges, trace)`.

---

# 👤 4. NGƯỜI D — KIỂM TRA ĐỒ THỊ HAI PHÍA (BIPARTITE)

---

### 📄 File cần mở: `core/bipartite.py`

#### Hàm `check_bipartite(adj, n)`
* **Cơ sở toán học (Định lý König)**: Đồ thị là hai phía khi và chỉ khi có thể tô bằng 2 màu (ví dụ Đỏ và Xanh) sao cho 2 đỉnh kề nhau luôn khác màu $\iff$ đồ thị không chứa chu trình độ dài lẻ.
* **Cách code từng bước**:
  1. **Bước 1 (Khởi tạo)**:
     - Tạo mảng màu `color = [0] * n` (quy ước: `0` là chưa tô, `1` là màu Đỏ, `-1` là màu Xanh).
     - Tạo mảng `parent = [-1] * n` để lưu vết.
  2. **Bước 2 (Duyệt toàn bộ đỉnh)**:
     - Dùng vòng lặp `for start in range(n):` để đảm bảo duyệt hết mọi thành phần liên thông (kể cả khi đồ thị bị đứt làm nhiều mảnh).
     - Nếu `color[start] == 0`:
       - Gán `color[start] = 1`, đưa `start` vào `queue = [start]`.
       - Vòng lặp BFS `while queue:`
         - Lấy `u = queue.pop(0)`.
         - Duyệt mọi đỉnh kề $v$ của $u$:
           - **Tình huống 1 (Đỉnh $v$ chưa tô màu - `color[v] == 0`)**:
             - Tô màu đối nghịch cho $v$: `color[v] = -color[u]` (nếu $u$ đỏ thì $v$ xanh, nếu $u$ xanh thì $v$ đỏ).
             - Ghi nhận `parent[v] = u`.
             - Đẩy $v$ vào `queue`.
           - **Tình huống 2 (Đỉnh $v$ đã tô và CÙNG MÀU với $u$ - `color[v] == color[u]`)**:
             - **PHÁT HIỆN MÂU THUẪN MÀU!** Kết luận ngay: Đồ thị KHÔNG PHẢI là hai phía.
             - **Truy vết chu trình lẻ**: Lần ngược mảng `parent` từ đỉnh $u$ và đỉnh $v$ về đỉnh tổ tiên chung để lấy danh sách các đỉnh tạo thành chu trình lẻ.
             - Trả về ngay: `{"is_bipartite": False, "odd_cycle": [danh_sách_đỉnh]}`.
  3. **Bước 3 (Kết luận thành công)**:
     - Nếu tô xong toàn bộ mà không gặp xung đột:
     - Gom tập đỉnh màu 1: $V_1 = \{i \mid color[i] == 1\}$.
     - Gom tập đỉnh màu -1: $V_2 = \{i \mid color[i] == -1\}$.
     - Trả về: `{"is_bipartite": True, "v1": V1, "v2": V2}`.
* **Tại sao phải dùng số `1` và `-1` để biểu diễn 2 màu?**
  * Vì khi muốn đổi sang màu ngược lại, ta chỉ cần gán `color[v] = -color[u]` cực kỳ nhanh và gọn!

---

# 👤 5. NGƯỜI E — ĐƯỜNG ĐI NGẮN NHẤT (DIJKSTRA & BELLMAN-FORD)

---

### 📄 File cần mở: `core/shortest_path.py`

#### 1. Hàm `dijkstra(adj, n, start, end=None)` (Cho trọng số không âm $w \ge 0$)
* **Tư tưởng (Tham lam - Greedy)**: Tại mỗi bước, chốt đỉnh có khoảng cách tạm thời nhỏ nhất, sau đó tối ưu khoảng cách tới các đỉnh lân cận.
* **Cách code từng bước**:
  1. Tạo `dist = [float('inf')] * n` (lưu khoảng cách ngắn nhất tạm thời, ban đầu là $\infty$).
  2. Gán `dist[start] = 0`, `visited = [False] * n` (đánh dấu đỉnh đã chốt), `parent = [-1] * n`.
  3. Lặp $n$ bước (`for step in range(n):`):
     - Quét tìm đỉnh $u$ trong số các đỉnh chưa chốt (`not visited[u]`) có giá trị `dist[u]` nhỏ nhất.
     - Nếu không tìm được hoặc `dist[u] == inf` $\implies$ dừng vòng lặp (các đỉnh còn lại không tới được).
     - Đánh dấu `visited[u] = True` (chốt khoảng cách cho đỉnh $u$).
     - Lưu 1 dòng vết vào `trace_table` gồm: (Bước $k$, đỉnh $u$ vừa chốt, mảng `dist` hiện tại).
     - **Thư giãn cạnh (Relaxation)**: Với mọi đỉnh kề $v$ của $u$ có trọng số $w$:
       - Nếu `not visited[v]` và `dist[u] + w < dist[v]`:
         - Cập nhật khoảng cách mới: `dist[v] = dist[u] + w`.
         - Cập nhật đỉnh trước: `parent[v] = u`.
  4. **Phục hồi đường đi**: Nếu người dùng có truyền vào đỉnh đích `end`:
     - Bắt đầu từ `curr = end`, liên tục lùi về `curr = parent[curr]` cho đến khi gặp `-1`.
     - Đảo ngược danh sách lại để thu được đường đi từ `start` đến `end`.
* **Tại sao Dijkstra không chạy được với trọng số âm?**
  * Vì chiến lược Tham lam một khi đã đánh dấu `visited[u] = True` thì sẽ không bao giờ xét lại đỉnh đó nữa. Nếu có cạnh âm xuất hiện phía sau làm giảm khoảng cách, Dijkstra sẽ bỏ qua và cho ra kết quả sai.
* **Đầu ra**: Trả về `{"dist": dist, "parent": parent, "path": path, "cost": dist[end], "trace": trace_table}`.

---

#### 2. Hàm `bellman_ford(edges, n, start, directed=False, end=None)` (Xử lý được trọng số âm)
* **Tư tưởng (Quy hoạch động)**: Một đường đi đơn ngắn nhất qua $n$ đỉnh chỉ chứa tối đa $n-1$ cạnh. Do đó lặp qua toàn bộ cạnh $n-1$ lần là chắc chắn tối ưu được khoảng cách.
* **Cách code từng bước**:
  1. Tạo `dist = [float('inf')] * n`, `dist[start] = 0`, `parent = [-1] * n`.
  2. Chuẩn bị danh sách cạnh: nếu `directed == False`, nhân đôi mỗi cạnh `(u, v, w)` thành cả `(v, u, w)`.
  3. **Thực hiện $n-1$ vòng lặp** (`for k in range(1, n):`):
     - Đặt cờ `changed = False`.
     - Duyệt qua **tất cả các cạnh $(u, v, w)$** trong danh sách:
       - Nếu `dist[u] != inf` và `dist[u] + w < dist[v]`:
         - `dist[v] = dist[u] + w`.
         - `parent[v] = u`.
         - `changed = True`.
     - Lưu 1 dòng vết biến thiên của mảng `dist` vào `trace_table`.
     - Nếu qua 1 vòng lặp mà `changed == False` $\implies$ dừng sớm (vì khoảng cách đã tối ưu hoàn toàn).
  4. **Vòng lặp thứ $n$ (Kiểm tra Chu trình âm - Negative Cycle)**:
     - `has_neg_cycle = False`.
     - Quét lại toàn bộ cạnh một lần nữa: Nếu vẫn còn cạnh nào thỏa mãn `dist[u] + w < dist[v]` $\implies$ `has_neg_cycle = True`.
* **Tại sao vòng thứ $n$ lại phát hiện được chu trình âm?**
  * Vì nếu đồ thị bình thường, sau $n-1$ vòng khoảng cách đã đạt cực tiểu tuyệt đối. Nếu sang vòng thứ $n$ mà khoảng cách vẫn tiếp tục giảm được, chỉ có 1 lý do duy nhất: tồn tại một chu trình có tổng trọng số âm (đi vòng vòng qua chu trình đó chi phí sẽ giảm mãi tới $-\infty$).
* **Đầu ra**: Trả về `{"dist": dist, "parent": parent, "path": path, "cost": dist[end], "has_negative_cycle": has_neg_cycle, "trace": trace_table}`.

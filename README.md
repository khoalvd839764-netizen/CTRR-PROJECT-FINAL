# KẾ HOẠCH TRIỂN KHAI DỰ ÁN CTRR FINAL PROJECT

---

# CÂY THƯ MỤC

```
CTRR FINAL PROJECT/
├── core/                    # Thuật toán thuần (100% tự viết)
│   ├── graph.py             # Class Graph + parser input
│   ├── converter.py         # 6 hàm chuyển đổi Matrix ↔ List ↔ EdgeList
│   ├── traversal.py         # BFS, DFS + bảng vết
│   ├── bipartite.py         # Kiểm tra đồ thị 2 phía
│   ├── shortest_path.py     # Dijkstra, Bellman-Ford + bảng vết
│   ├── euler.py             # Fleury, Hierholzer
│   ├── mst.py               # Prim, Kruskal + class DSU
│   └── max_flow.py          # Ford-Fulkerson (Edmonds-Karp)
├── visualizer/
│   └── draw.py              # Vẽ đồ thị bằng matplotlib, lưu PNG
├── data/
│   └── samples.py           # Đồ thị mẫu cho tất cả bài toán
├── tests/
├── run_demo.py              # Script chạy demo toàn bộ
└── requirements.txt         # matplotlib
```

---

# GIAI ĐOẠN 1: CƠ BẢN (Mục 1 - 5)

---

## FILE `core/graph.py` — Class Graph

> **Phục vụ chức năng**: Mục 1 (Input đồ thị) + Mục 2 (Hiển thị các phương pháp biểu diễn)
>
> **Mục đích**: Làm đối tượng trung tâm nhận dữ liệu đầu vào và lưu đồ thị dưới cả 3 dạng cùng lúc. Khi người dùng nhập 1 dạng bất kỳ (ma trận / danh sách cạnh / danh sách kề), class tự động tính ra 2 dạng còn lại.
>
> **Lý do**: Mỗi thuật toán cần dạng biểu diễn khác nhau. BFS/DFS/Dijkstra cần danh sách kề (duyệt đỉnh kề nhanh). Bellman-Ford/Kruskal cần danh sách cạnh (quét toàn bộ cạnh). Ford-Fulkerson cần ma trận kề (truy cập `capacity[u][v]` nhanh). Nếu không có class này, mỗi lần chạy thuật toán phải tự chuyển đổi thủ công.

### `__init__(n, is_directed, is_weighted)`
- Lưu `self.n`, `self.is_directed`, `self.is_weighted`
- Khởi tạo 3 dạng rỗng: `adj_matrix`, `adj_list`, `edge_list`

### `load_from_matrix(matrix)`
- Gán `self.adj_matrix = matrix`
- Gọi `matrix_to_adj_list()` → cập nhật `self.adj_list`
- Gọi `matrix_to_edge_list()` → cập nhật `self.edge_list`

### `load_from_edge_list(edges, n)`
- Gán `self.edge_list`
- Gọi `edge_list_to_matrix()` → cập nhật `self.adj_matrix`
- Gọi `edge_list_to_adj_list()` → cập nhật `self.adj_list`

### `load_from_text(raw_text)`
- Tách dòng, đọc dòng đầu: nếu chỉ 1 số → dạng ma trận, ngược lại → dạng danh sách cạnh
- Gọi `load_from_matrix()` hoặc `load_from_edge_list()` tương ứng
- **Mục đích**: Cho phép người dùng nhập từ bàn phím hoặc đọc file text đều dùng được cùng 1 hàm này

### `get_all_representations()`
- Trả về dict chứa cả 3 dạng để hiển thị song song trên màn hình
- **Mục đích**: Phục vụ Mục 2 — cho người dùng thấy đồng thời cả 3 bảng biểu diễn để so sánh

---

## FILE `core/converter.py` — 6 hàm chuyển đổi

> **Phục vụ chức năng**: Mục 2 (Chuyển đổi `adjacency matrix ↔ adjacency list ↔ edge list`)
>
> **Mục đích**: Đề bài yêu cầu chuyển đổi 2 chiều giữa 3 dạng biểu diễn. File này chứa 6 hàm tương ứng 6 chiều chuyển đổi.
>
> **Lý do tách riêng file**: `graph.py` gọi các hàm này bên trong. Tách ra để dễ test từng hàm riêng biệt mà không cần tạo cả đối tượng Graph.

### `matrix_to_adj_list(matrix, is_directed)`
- Duyệt 2 vòng lặp `for i` `for j` trên ma trận $n \times n$
- Nếu `matrix[i][j] != 0` → thêm `(j, matrix[i][j])` vào `adj_list[i]`
- Trả về dict `{0: [(1, w), (2, w)], 1: [...], ...}`
- **Ví dụ**: `matrix = [[0,5],[5,0]]` → `{0: [(1, 5)], 1: [(0, 5)]}`

### `matrix_to_edge_list(matrix, is_directed)`
- Nếu **có hướng**: quét toàn bộ `(i, j)`
- Nếu **vô hướng**: chỉ quét `j >= i` để tránh trùng cạnh (vì $(0,1)$ và $(1,0)$ là 1 cạnh)
- **Lý do quét nửa trên**: Nếu quét hết sẽ ra cạnh trùng `(0,1,5)` và `(1,0,5)` — sai

### `edge_list_to_matrix(edge_list, n, is_directed)`
- Tạo mảng `[[0]*n for _ in range(n)]`
- Duyệt từng `(u, v, w)`: gán `M[u][v] = w`
- Nếu vô hướng: gán thêm `M[v][u] = w` (vì cạnh đi được 2 chiều)

### `edge_list_to_adj_list(edge_list, n, is_directed)`
- Tạo dict rỗng cho n đỉnh
- Duyệt từng `(u, v, w)`: `adj[u].append((v, w))`
- Nếu vô hướng: `adj[v].append((u, w))` (vì v cũng kề u)

### `adj_list_to_matrix(adj_list, n)`
- Tạo mảng `[[0]*n ...]`
- Quét dict: gán `M[u][v] = w`

### `adj_list_to_edge_list(adj_list, is_directed)`
- Gom `(u, v, w)` từ dict
- Nếu vô hướng: chỉ lấy khi `u <= v` (tránh trùng lặp giống `matrix_to_edge_list`)

---

## FILE `visualizer/draw.py` — Vẽ đồ thị

> **Phục vụ chức năng**: Mục 1 (Vẽ & Lưu hình đồ thị) + Mục 7 (Trực quan hóa kết quả thuật toán)
>
> **Mục đích**: Biến dữ liệu số thành hình ảnh trực quan. Đề bài yêu cầu "Vẽ & Lưu hình" và "Trực quan hóa kết quả". Không có hình thì không demo được.
>
> **Lý do dùng matplotlib**: Đây là thư viện vẽ hình duy nhất được phép dùng theo đề bài ("không sử dụng thư viện có sẵn trừ phần Trực quan hóa").

### `draw_graph(n, edge_list, is_directed, filename, node_colors, highlight_edges, title)`
- Tính tọa độ đỉnh theo đường tròn: $x = R\cos(2\pi i/n)$, $y = R\sin(2\pi i/n)$
- **Lý do xếp tròn**: Mọi đỉnh cách đều nhau, không bị đè chồng, dễ nhìn
- Vẽ cạnh: `plt.plot()` cho vô hướng, `ax.annotate()` với mũi tên cho có hướng
- Ghi trọng số ở trung điểm cạnh (nếu có trọng số)
- Vẽ đỉnh: `plt.Circle()` tô màu, ghi số hiệu ở tâm
- Tham số `highlight_edges`: tô đỏ các cạnh đặc biệt — dùng cho đường đi ngắn nhất, cây khung MST, đường Euler
- Tham số `node_colors`: tô màu riêng từng đỉnh — dùng cho đồ thị 2 phía (Đỏ/Xanh), min-cut (S/T)
- `plt.savefig(filename, dpi=300)` lưu file ảnh

---

## FILE `core/traversal.py` — BFS & DFS

> **Phục vụ chức năng**: Mục 3 (Duyệt đồ thị từ 1 node bất kỳ bằng BFS & DFS. So với kết quả chạy tay.)
>
> **Mục đích**: Duyệt qua tất cả đỉnh của đồ thị theo 2 chiến lược khác nhau, xuất ra thứ tự duyệt + cây khung + bảng vết từng bước.
>
> **Lý do sinh bảng vết (trace_table)**: Đề bài yêu cầu "So với kết quả chạy tay". Bảng vết mô phỏng chính xác từng bước như sinh viên làm bài trên giấy — giúp đối chiếu và chứng minh thuật toán chạy đúng.

### `bfs(adj_list, n, start_node)`
- **Chức năng**: Duyệt theo chiều rộng — thăm tất cả đỉnh cách nguồn 1 cạnh trước, rồi 2 cạnh, 3 cạnh...
- Chuẩn bị: `visited = [False]*n`, `parent = [-1]*n`, `queue = [start]`
- Vòng lặp `while queue`:
  - `u = queue.pop(0)` (lấy đầu — FIFO)
  - Quét đỉnh kề $v$ của $u$ (**sorted tăng dần**)
  - Nếu $v$ chưa thăm → đánh dấu, thêm vào queue, ghi cạnh cây khung
  - Lưu 1 dòng vào `trace_table`: bước, đỉnh $u$, queue hiện tại, visited, cạnh mới
- **Lý do sorted tăng dần**: Khi giải tay, sinh viên luôn chọn đỉnh nhỏ trước. Nếu không sort, thứ tự code khác bài giải tay → thầy cô cho sai
- Trả về `(bfs_order, tree_edges, trace_table)`

### `dfs(adj_list, n, start_node)`
- **Chức năng**: Duyệt theo chiều sâu — đi sâu nhất có thể rồi mới quay lui
- Hàm đệ quy `dfs_visit(u)`:
  - `visited[u] = True`, thêm $u$ vào dfs_order
  - Quét đỉnh kề $v$ chưa thăm (**sorted tăng dần**) → ghi cạnh → đệ quy `dfs_visit(v)`
  - Lưu vết: bước, đỉnh $u$, đỉnh cha, visited
- **Lý do dùng đệ quy thay vì Stack**: Đệ quy cho ra thứ tự duyệt giống cách sinh viên giải tay (đi sâu xong quay lui). Stack có thể cho thứ tự khác.
- Trả về `(dfs_order, tree_edges, trace_table)`

---

## FILE `core/bipartite.py` — Kiểm tra đồ thị 2 phía

> **Phục vụ chức năng**: Mục 4 (Kiểm tra xem đồ thị có là đồ thị hai phía)
>
> **Mục đích**: Xác định xem có thể chia tập đỉnh thành 2 nhóm sao cho mọi cạnh chỉ nối giữa 2 nhóm khác nhau. Nếu không được thì chỉ ra chu trình lẻ chứng minh.
>
> **Lý do dùng thuật toán tô 2 màu**: Theo định lý König, đồ thị 2 phía ↔ có thể tô 2 màu ↔ không có chu trình lẻ. Tô màu bằng BFS là cách đơn giản và chính xác nhất.

### `check_bipartite(adj_list, n)`
- Chuẩn bị: `color = [0]*n` (0: chưa tô, 1: Đỏ, -1: Xanh), `parent = [-1]*n`
- **Lý do lặp qua tất cả đỉnh**: Đồ thị có thể không liên thông (nhiều mảnh rời), phải kiểm tra từng mảnh
- Với mỗi đỉnh chưa tô → gán màu 1, BFS:
  - $v$ chưa tô → `color[v] = -color[u]` (tô màu ngược lại)
  - $v$ cùng màu $u$ → **xung đột!** → đồ thị KHÔNG phải 2 phía
    - Lần ngược `parent` từ $u$ và $v$ tìm đỉnh chung → trích xuất chu trình lẻ
    - **Lý do trích chu trình lẻ**: Để chứng minh cho người dùng thấy tại sao đồ thị không phải 2 phía — có bằng chứng cụ thể
    - Trả về `{is_bipartite: False, odd_cycle: [...]}`
- Nếu xong hết → trả về `{is_bipartite: True, set_v1: [...], set_v2: [...]}`
  - **Lý do trả về 2 tập**: Để vẽ đồ thị 2 phía với 2 màu khác nhau (Đỏ/Xanh) cho trực quan

---

## FILE `core/shortest_path.py` — Dijkstra & Bellman-Ford

> **Phục vụ chức năng**: Mục 5 (Tìm đường đi ngắn nhất giữa 2 nodes bất kỳ bằng Dijkstra & Bellman-Ford. So với kết quả chạy tay.)
>
> **Mục đích**: Tìm đường đi có tổng trọng số nhỏ nhất từ đỉnh nguồn đến đỉnh đích.
>
> **Lý do cần 2 thuật toán**: Dijkstra nhanh nhưng chỉ đúng khi trọng số ≥ 0. Bellman-Ford chậm hơn nhưng xử lý được trọng số âm và phát hiện chu trình âm. Đề bài yêu cầu cả 2 để so sánh.

### `dijkstra(adj_list, n, start, target)`
- **Chức năng**: Tìm đường ngắn nhất trên đồ thị trọng số không âm ($w \ge 0$)
- Chuẩn bị: `dist = [∞]*n`, `visited = [False]*n`, `parent = [-1]*n`, `dist[start] = 0`
- Lặp n lần:
  - Tìm đỉnh $u$ chưa thăm có `dist[u]` nhỏ nhất
  - **Lý do chọn min**: Chiến lược Tham lam — đỉnh gần nhất chắc chắn đã có khoảng cách tối ưu (chỉ đúng khi $w \ge 0$)
  - Chốt `visited[u] = True`
  - Quét đỉnh kề $v$: nếu `dist[u] + w < dist[v]` → cập nhật (Relaxation)
  - Lưu 1 dòng vào `trace_table`: bước, đỉnh chọn, dist hiện tại, parent hiện tại
  - **Lý do lưu trace**: Đề bài yêu cầu "So với kết quả chạy tay" — sinh bảng ma trận bước lặp giống bài thi
- Phục hồi đường đi: lần ngược `parent` từ target về start
- **Lý do cần mảng parent**: dist chỉ cho biết chi phí ngắn nhất, còn parent cho biết đi qua đỉnh nào — cần cả 2 để trả lời đầy đủ
- Trả về `{dist, parent, path, cost, trace_table}`

### `bellman_ford(edge_list, n, start, is_directed, target)`
- **Chức năng**: Tìm đường ngắn nhất, xử lý được trọng số âm, phát hiện chu trình âm
- **Lý do dùng edge_list thay vì adj_list**: Bellman-Ford duyệt toàn bộ cạnh mỗi vòng, dùng danh sách cạnh tiện hơn
- Chuẩn bị: `dist = [∞]*n`, `dist[start] = 0`, `parent = [-1]*n`
- Nếu vô hướng: nhân đôi mỗi cạnh thành 2 chiều
  - **Lý do nhân đôi**: Cạnh vô hướng $(u,v,w)$ nghĩa là đi được cả $u→v$ lẫn $v→u$, cần relax cả 2 chiều
- Lặp $n-1$ vòng qua toàn bộ cạnh:
  - Nếu `dist[u] + w < dist[v]` → cập nhật
  - **Lý do lặp đúng $n-1$ lần**: Đường đi đơn ngắn nhất qua tối đa $n-1$ cạnh. Mỗi vòng lặp đảm bảo tìm được đường tối ưu dài thêm 1 cạnh
  - Lưu biến thiên `dist` qua từng vòng vào `trace_table`
  - Dừng sớm nếu không có thay đổi (tối ưu, không bắt buộc)
- Vòng thứ $n$: quét lại cạnh → nếu còn cập nhật được → `has_negative_cycle = True`
  - **Lý do thêm vòng thứ n**: Nếu sau $n-1$ vòng mà vẫn giảm được khoảng cách → có chu trình âm (đi vòng vòng mãi chi phí cứ giảm → khoảng cách $= -\infty$)
- Trả về `{dist, parent, path, cost, has_negative_cycle, trace_table}`

---

# GIAI ĐOẠN 2: NÂNG CAO (Mục 7.1 - 7.5)

---

## FILE `core/euler.py` — Fleury & Hierholzer

> **Phục vụ chức năng**: Mục 7.1 (Fleury) + Mục 7.2 (Hierholzer)
>
> **Mục đích**: Tìm chu trình/đường đi Euler — đi qua mỗi cạnh đúng 1 lần.
>
> **Lý do cần 2 thuật toán**: Fleury dễ hiểu nhưng chậm ($O(E^2)$). Hierholzer nhanh ($O(E)$) nhưng khó hiểu hơn. Đề bài yêu cầu cả 2 để so sánh cách tiếp cận và hiệu năng.

### `fleury(adj_list, n, is_directed)`
- **Chức năng**: Tìm Euler bằng quy tắc "Không đi qua cầu trừ khi hết đường"
- Kiểm tra điều kiện Euler: liên thông + đếm đỉnh bậc lẻ = 0 (chu trình) hoặc 2 (đường đi)
  - **Lý do kiểm tra trước**: Nếu không thỏa điều kiện thì chạy vô ích, phải báo cho người dùng biết
- Viết hàm con `is_bridge(u, v)`: tạm xóa cạnh $(u,v)$, đếm đỉnh liên thông bằng DFS, so sánh trước/sau
  - **Lý do cần kiểm tra cầu**: Nếu đi qua cầu khi vẫn còn đường khác → sẽ chia đồ thị thành 2 mảnh → không thể hoàn thành Euler
- Tại mỗi bước: chọn cạnh không phải cầu (nếu có), xóa cạnh, di chuyển
- Trả về `(euler_path, steps_log)`

### `hierholzer(adj_list, n, is_directed)`
- **Chức năng**: Tìm Euler bằng kỹ thuật ghép chu trình con — nhanh gấp nhiều lần Fleury
- Kiểm tra điều kiện Euler
- `stack = [start]`, `circuit = []`
- Khi stack chưa rỗng:
  - `u = stack[-1]`
  - Nếu $u$ còn cạnh → lấy cạnh $(u, v)$, xóa, `stack.append(v)`
  - Nếu hết cạnh → `circuit.append(stack.pop())`
  - **Lý do dùng 2 danh sách stack + circuit**: stack dùng để đi tìm chu trình con, circuit gom kết quả cuối cùng. Khi đỉnh hết cạnh (= đã hoàn thành 1 chu trình con), đẩy vào circuit
- Trả về `(circuit[::-1], steps_log)`
  - **Lý do đảo ngược**: Vì đỉnh được đẩy vào circuit theo thứ tự ngược

---

## FILE `core/mst.py` — Prim, Kruskal & DSU

> **Phục vụ chức năng**: Mục 7.3 (Prim) + Mục 7.4 (Kruskal)
>
> **Mục đích**: Tìm Cây khung nhỏ nhất (MST) — nối tất cả đỉnh lại với nhau sao cho tổng trọng số cạnh nhỏ nhất.
>
> **Lý do cần 2 thuật toán**: Prim phát triển cây từ 1 đỉnh (giống Dijkstra). Kruskal sắp xếp cạnh rồi chọn lọc (cần DSU). 2 cách tiếp cận khác nhau nhưng cùng kết quả.

### Class `DSU` (Disjoint Set Union)
- **Chức năng**: Quản lý các nhóm đỉnh riêng biệt, kiểm tra 2 đỉnh có cùng nhóm không
- **Lý do cần DSU**: Kruskal cần biết nhanh "thêm cạnh $(u,v)$ có tạo chu trình không?" → nếu $u$ và $v$ cùng nhóm → có chu trình → bỏ qua
- `__init__(n)`: `parent = [0..n-1]` (mỗi đỉnh tự là gốc), `rank = [0]*n`
- `find(u)`: tìm gốc nhóm chứa $u$, kèm nén đường đi `parent[u] = find(parent[u])`
  - **Lý do nén đường đi**: Không nén thì cây có thể dài, `find()` chậm. Nén xong `find()` gần như $O(1)$
- `union(u, v)`: gộp 2 nhóm theo rank
  - **Lý do gộp theo rank**: Gắn cây thấp vào cây cao, giữ chiều cao cây nhỏ → `find()` nhanh

### `prim(adj_list, n)`
- **Chức năng**: Xây MST bằng cách mở rộng cây từ 1 đỉnh
- `in_mst = [False]*n`, `in_mst[0] = True`, `mst_edges = []`
- Lặp $n-1$ lần: quét tìm cạnh nhẹ nhất $(u, v, w)$ có $u$ trong MST, $v$ ngoài MST
  - **Lý do chọn cạnh nhẹ nhất cắt giữa trong/ngoài**: Tính chất Cut Property đảm bảo cạnh nhẹ nhất qua lát cắt luôn thuộc MST
- Kết nạp cạnh, đánh dấu $v$
- Trả về `(mst_edges, total_weight, steps_log)`

### `kruskal(edge_list, n)`
- **Chức năng**: Xây MST bằng cách chọn cạnh nhẹ nhất toàn cục mà không tạo chu trình
- Sắp xếp cạnh theo trọng số tăng dần
  - **Lý do sắp xếp**: Luôn ưu tiên cạnh nhẹ nhất → đảm bảo MST tối ưu
- `dsu = DSU(n)`, `mst_edges = []`
- Duyệt từng cạnh: nếu `dsu.find(u) != dsu.find(v)` → kết nạp, `dsu.union(u, v)`
  - **Lý do kiểm tra find**: Nếu $u, v$ cùng nhóm → thêm cạnh sẽ tạo chu trình → cây khung không được có chu trình
- Trả về `(mst_edges, total_weight, steps_log)`

---

## FILE `core/max_flow.py` — Ford-Fulkerson (Edmonds-Karp)

> **Phục vụ chức năng**: Mục 7.5 (Ford-Fulkerson)
>
> **Mục đích**: Tìm lượng luồng cực đại có thể đẩy từ nguồn S đến bồn T trong mạng luồng, và tìm lát cắt hẹp nhất (Min-Cut).
>
> **Lý do dùng Edmonds-Karp (BFS) thay vì DFS**: BFS đảm bảo tìm đường tăng luồng ngắn nhất → thuật toán chạy tối đa $O(VE^2)$, trong khi DFS có thể chạy rất lâu trên một số đồ thị.

### `ford_fulkerson(capacity, n, source, sink)`
- **Chức năng**: Tìm luồng cực đại + lát cắt hẹp nhất
- Khởi tạo `flow = [[0]*n for ...]`
- Viết hàm con `bfs_find_path()`: BFS trên đồ thị phần dư tìm đường $S → T$
  - Cung thuận: dung lượng dư = `capacity[u][v] - flow[u][v]`
  - Cung nghịch: dung lượng dư = `flow[v][u]`
  - **Lý do cần cung nghịch**: Cho phép "hủy" luồng đã đẩy sai hướng — nếu không có cung nghịch, thuật toán có thể kẹt mà chưa đạt luồng tối ưu
- Vòng lặp:
  - Tìm đường tăng luồng bằng BFS
  - Không tìm được → dừng (đã đạt Max Flow)
  - Tìm $\Delta$ = min dung lượng dư trên đường
    - **Lý do lấy min**: Đường đi bị giới hạn bởi cung hẹp nhất (cổ chai)
  - Cập nhật: `flow[u][v] += Δ`, `flow[v][u] -= Δ`
  - Lưu vết: đường đi, $\Delta$, flow hiện tại
- Tìm Min-Cut: BFS từ $S$ trên đồ thị phần dư → tập $S$ = đỉnh tới được, tập $T$ = phần còn lại
  - **Lý do Min-Cut = Max-Flow**: Đây là Định lý Max-Flow Min-Cut — dung lượng lát cắt hẹp nhất đúng bằng giá trị luồng cực đại
- Trả về `{max_flow, flow_matrix, min_cut_S, min_cut_T, steps_log}`

---

# FILE `data/samples.py` — Đồ thị mẫu

> **Mục đích**: Cung cấp sẵn các đồ thị kinh điển để chạy demo ngay mà không cần gõ tay. Mỗi bộ mẫu được thiết kế riêng cho từng bài toán để kết quả chạy ra có ý nghĩa minh họa.

Các bộ mẫu đã tạo sẵn:
- `GRAPH_BASIC`: 6 đỉnh vô hướng → cho BFS/DFS
- `GRAPH_WEIGHTED`: 5 đỉnh có trọng số → cho Dijkstra/Bellman-Ford
- `GRAPH_BIPARTITE`: Chu trình chẵn $C_4$ → kiểm tra ra True
- `GRAPH_NOT_BIPARTITE`: Tam giác $C_3$ → kiểm tra ra False
- `GRAPH_EULER`: Đồ thị mọi đỉnh bậc chẵn → cho Fleury/Hierholzer
- `GRAPH_MST`: 6 đỉnh có trọng số → cho Prim/Kruskal
- `GRAPH_FLOW`: Mạng luồng 6 đỉnh (nguồn 0, bồn 5) → cho Ford-Fulkerson

---

# FILE `run_demo.py` — Script chạy demo

> **Mục đích**: Chạy 1 lệnh duy nhất `python3 run_demo.py` là thấy toàn bộ kết quả của tất cả thuật toán. Tiện cho lúc demo trước thầy cô.

### `main()`
- Import tất cả module từ `core/` và `visualizer/`
- Import đồ thị mẫu từ `data/samples.py`
- Chạy tuần tự:
  1. Nạp đồ thị mẫu → in 3 bảng biểu diễn → vẽ & lưu PNG
  2. Chạy BFS & DFS → in bảng vết
  3. Kiểm tra Bipartite → in kết quả → vẽ tô 2 màu
  4. Chạy Dijkstra & Bellman-Ford → in bảng vết → vẽ highlight đường đi
  5. Chạy Fleury & Hierholzer → in chuỗi Euler → vẽ highlight
  6. Chạy Prim & Kruskal → in MST → vẽ highlight cây khung
  7. Chạy Ford-Fulkerson → in luồng & min-cut → vẽ mạng luồng
# CTRR-PROJECT-FINAL

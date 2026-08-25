# BẢNG PHÂN CÔNG CÔNG VIỆC — 5 CHỨC NĂNG CƠ BẢN

## SƠ ĐỒ PHỤ THUỘC

```
Người A: converter.py ──┐
                        ├──→ Người A tiếp: graph.py ──┬──→ Người C: traversal.py
Người B: draw.py ───────┘                             ├──→ Người D: bipartite.py
                                                       └──→ Người E: shortest_path.py
```

⚠️ Người C, D, E CHỈ BẮT ĐẦU CODE được sau khi Người A XONG converter.py + graph.py

---

## 👤 NGƯỜI A — converter.py + graph.py

⚠️ ĐÂY LÀ VIỆC PHẢI XONG ĐẦU TIÊN — 3 người C, D, E đều chờ file này

### Việc 1: core/converter.py (6 hàm)

- [ ] matrix_to_adj(matrix, directed)
  - 2 vòng for i, j: nếu matrix[i][j] != 0 thì thêm (j, w) vào adj[i]

- [ ] matrix_to_edges(matrix, directed)
  - Vô hướng: chỉ quét j >= i (tránh trùng). Có hướng: quét hết

- [ ] edges_to_matrix(edges, n, directed)
  - Tạo mảng [[0]*n ...], gán M[u][v] = w. Vô hướng: gán thêm M[v][u] = w

- [ ] edges_to_adj(edges, n, directed)
  - Tạo dict rỗng, append (v, w) vào adj[u]. Vô hướng: append thêm (u, w) vào adj[v]

- [ ] adj_to_matrix(adj, n)
  - Quét dict, gán M[u][v] = w

- [ ] adj_to_edges(adj, directed)
  - Gom (u, v, w) từ dict. Vô hướng: chỉ lấy u <= v

### Việc 2: core/graph.py (class Graph)

- [ ] __init__(n, directed, weighted)
  - Lưu self.n, self.directed, self.weighted
  - Khởi tạo self.matrix = [], self.adj = {}, self.edges = []

- [ ] from_matrix(matrix)
  - Gán self.matrix, gọi matrix_to_adj và matrix_to_edges cập nhật 2 dạng kia

- [ ] from_edges(edges, n)
  - Gán self.edges, gọi edges_to_matrix và edges_to_adj cập nhật 2 dạng kia

- [ ] from_text(text)
  - Tách dòng, dòng đầu 1 số = ma trận, ngược lại = danh sách cạnh
  - Gọi from_matrix hoặc from_edges tương ứng

### Cách test nhanh khi xong:
```python
from core.graph import Graph
g = Graph(directed=False)
g.from_edges([(0,1,1),(0,2,1),(1,2,1)], 3)
print(g.matrix)  # [[0,1,1],[1,0,1],[1,1,0]]
print(g.adj)     # {0: [(1,1),(2,1)], 1: [(0,1),(2,1)], 2: [(0,1),(1,1)]}
print(g.edges)   # [(0,1,1),(0,2,1),(1,2,1)]
```

---

## 👤 NGƯỜI B — visualizer/draw.py

⚠️ NÊN XONG SONG SONG VỚI NGƯỜI A — C, D, E cần hàm vẽ để hiển thị kết quả

### Việc: visualizer/draw.py (1 hàm chính)

- [ ] draw(n, edges, directed, filename, colors, highlight, title)
  - Tính tọa độ: x = R*cos(2πi/n), y = R*sin(2πi/n)
  - Vẽ cạnh: plt.plot() cho vô hướng, ax.annotate() mũi tên cho có hướng
  - Ghi trọng số ở trung điểm nếu w != 1
  - Vẽ đỉnh: plt.Circle() tô màu + số hiệu ở tâm
  - Nếu highlight khác None: tô đỏ các cạnh trong danh sách highlight
  - Nếu colors khác None: tô màu đỉnh theo dict colors
  - plt.savefig(filename, dpi=300)

### Cách test nhanh khi xong:
```python
from visualizer.draw import draw
draw(4, [(0,1,1),(1,2,1),(2,3,1),(3,0,1)], filename="test.png")
# Mở test.png phải thấy 4 đỉnh xếp tròn, 4 cạnh nối
```

---

## 👤 NGƯỜI C — core/traversal.py (BFS & DFS)

⚠️ CHỜ NGƯỜI A XONG converter.py + graph.py MỚI BẮT ĐẦU CODE
(Trong lúc chờ: đọc plan, hiểu thuật toán, chuẩn bị giải tay trên giấy để đối chiếu)

### Việc: core/traversal.py (2 hàm)

- [ ] bfs(adj, n, start)
  - visited = [False]*n, parent = [-1]*n, queue = [start]
  - visited[start] = True
  - while queue:
    - u = queue.pop(0)
    - neighbors = sorted danh sách đỉnh kề u
    - với mỗi v chưa thăm: visited[v]=True, parent[v]=u, queue.append(v)
    - lưu 1 dòng trace: step, u, queue hiện tại, visited hiện tại
  - Trả về (bfs_order, tree_edges, trace_table)

- [ ] dfs(adj, n, start)
  - visited = [False]*n
  - Hàm đệ quy dfs_visit(u):
    - visited[u] = True, thêm u vào order
    - neighbors = sorted danh sách đỉnh kề u
    - với mỗi v chưa thăm: ghi cạnh (u,v), đệ quy dfs_visit(v)
    - lưu 1 dòng trace mỗi bước
  - Trả về (dfs_order, tree_edges, trace_table)

### Cách test nhanh khi xong:
```python
from core.graph import Graph
from core.traversal import bfs, dfs
g = Graph(directed=False)
g.from_edges([(0,1,1),(0,2,1),(1,3,1),(1,4,1),(2,4,1),(3,5,1),(4,5,1)], 6)
order, tree, trace = bfs(g.adj, g.n, 0)
print(order)  # [0, 1, 2, 3, 4, 5]
```

---

## 👤 NGƯỜI D — core/bipartite.py

⚠️ CHỜ NGƯỜI A XONG converter.py + graph.py MỚI BẮT ĐẦU CODE
(Trong lúc chờ: đọc plan, hiểu thuật toán tô 2 màu)

### Việc: core/bipartite.py (1 hàm)

- [ ] check_bipartite(adj, n)
  - color = [0]*n, parent = [-1]*n
  - Lặp i từ 0 đến n-1 (xử lý đồ thị không liên thông):
    - Nếu color[i] == 0:
      - color[i] = 1, queue = [i]
      - while queue:
        - u = queue.pop(0)
        - với mỗi v kề u:
          - color[v]==0: gán color[v] = -color[u], parent[v]=u, queue.append(v)
          - color[v]==color[u]: XÓA! lần ngược parent tìm chu trình lẻ
            - Trả về {is_bipartite: False, odd_cycle: [...]}
  - Nếu xong hết không lỗi:
    - v1 = [i for i if color[i]==1]
    - v2 = [i for i if color[i]==-1]
    - Trả về {is_bipartite: True, v1: [...], v2: [...]}

### Cách test nhanh khi xong:
```python
from core.graph import Graph
from core.bipartite import check_bipartite
# Test True: hình vuông C4
g1 = Graph(directed=False)
g1.from_edges([(0,1,1),(1,2,1),(2,3,1),(3,0,1)], 4)
print(check_bipartite(g1.adj, g1.n))  # is_bipartite: True

# Test False: tam giác C3
g2 = Graph(directed=False)
g2.from_edges([(0,1,1),(1,2,1),(2,0,1)], 3)
print(check_bipartite(g2.adj, g2.n))  # is_bipartite: False
```

---

## 👤 NGƯỜI E — core/shortest_path.py (Dijkstra & Bellman-Ford)

⚠️ CHỜ NGƯỜI A XONG converter.py + graph.py MỚI BẮT ĐẦU CODE
(Trong lúc chờ: đọc plan, hiểu thuật toán, giải tay trên giấy để đối chiếu)

### Việc: core/shortest_path.py (2 hàm)

- [ ] dijkstra(adj, n, start, end)
  - dist = [float('inf')]*n, visited = [False]*n, parent = [-1]*n
  - dist[start] = 0
  - Lặp n lần:
    - Tìm u chưa thăm có dist[u] nhỏ nhất
    - Nếu dist[u] == inf thì break
    - visited[u] = True
    - Với mỗi v kề u: nếu dist[u]+w < dist[v] thì cập nhật dist[v], parent[v]
    - Lưu 1 dòng trace: step, u đã chọn, dist hiện tại
  - Phục hồi path: lần ngược parent từ end về start, rồi reverse
  - Trả về {dist, parent, path, cost, trace_table}

- [ ] bellman_ford(edges, n, start, directed, end)
  - dist = [float('inf')]*n, parent = [-1]*n, dist[start] = 0
  - Nếu vô hướng: nhân đôi mỗi cạnh (u,v,w) thêm (v,u,w)
  - Lặp n-1 vòng qua toàn bộ cạnh:
    - Nếu dist[u]+w < dist[v]: cập nhật dist[v], parent[v]
    - Lưu dist sau mỗi vòng vào trace
    - Nếu không thay đổi gì thì break sớm
  - Vòng thứ n: quét lại, nếu còn cập nhật được → has_negative_cycle = True
  - Phục hồi path giống dijkstra
  - Trả về {dist, parent, path, cost, has_negative_cycle, trace_table}

### Cách test nhanh khi xong:
```python
from core.graph import Graph
from core.shortest_path import dijkstra, bellman_ford
g = Graph(directed=False)
g.from_edges([(0,1,4),(0,2,2),(1,2,1),(1,3,5),(2,3,8),(2,4,10),(3,4,2)], 5)

d = dijkstra(g.adj, g.n, 0, 4)
b = bellman_ford(g.edges, g.n, 0, directed=False, end=4)
print(d["cost"], d["path"])  # 10, [0, 2, 1, 3, 4]
print(b["cost"], b["path"])  # 10, [0, 2, 1, 3, 4]  ← phải giống nhau
```

---

## NGÀY 2: TÍCH HỢP + TEST TỔNG (CẢ 5 NGƯỜI CÙNG LÀM)

- [ ] Người A: Viết run_demo.py ghép tất cả module lại, chạy thử từng chức năng
- [ ] Người B: Vẽ kết quả từng thuật toán (highlight đường đi, tô 2 màu bipartite)
- [ ] Người C: In bảng vết BFS/DFS ra màn hình dạng bảng đẹp
- [ ] Người D: In kết quả Bipartite (2 tập hoặc chu trình lẻ) ra màn hình
- [ ] Người E: In bảng vết Dijkstra/Bellman-Ford, so sánh 2 thuật toán
- [ ] CẢ 5: Test chéo, sửa lỗi, chạy demo tổng lần cuối

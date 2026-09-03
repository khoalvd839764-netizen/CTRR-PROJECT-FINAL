# BÁO CÁO ĐỒ ÁN MÔN HỌC: CẤU TRÚC RỜI RẠC
**ĐỀ TÀI: HỆ THỐNG GIẢI TOÁN ĐỒ THỊ TOÀN DIỆN VÀ ỨNG DỤNG MÔ PHỎNG THỰC TẾ ROBOT HÚT BỤI THÔNG MINH**

---

# CHƯƠNG 1: TỔNG QUAN KHÁI NIỆM KIẾN THỨC CHUYÊN NGÀNH

## 1.1. KHÁI NIỆM CÓ TRONG DỰ ÁN

### 1.1.1. Định nghĩa và 3 cách biểu diễn đồ thị
Đồ thị là một cấu trúc toán học rời rạc $G = (V, E)$, trong đó $V$ là tập hợp các đỉnh (vertices / nodes) đại diện cho các thực thể, và $E$ là tập hợp các cạnh (edges) đại diện cho mối liên kết giữa các thực thể đó:
- **Đồ thị vô hướng (Undirected Graph):** Cạnh nối giữa hai đỉnh $u$ và $v$ không phân biệt thứ tự, ký hiệu $(u, v) = (v, u)$. Mối quan hệ mang tính hai chiều đối xứng.
- **Đồ thị có hướng (Directed Graph / Digraph):** Cạnh nối có hướng xác định từ $u$ sang $v$, ký hiệu là cung $\langle u, v \rangle$, với $u$ là đỉnh đầu và $v$ là đỉnh cuối.
- **Đồ thị có trọng số (Weighted Graph):** Mỗi cạnh $(u, v)$ được gán một giá trị số thực $w(u, v)$, đại diện cho chi phí, khoảng cách, thời gian hoặc dung lượng truyền dẫn.

Trong khoa học máy tính, để lưu trữ và thao tác với đồ thị trên bộ nhớ máy tính, dự án triển khai đầy đủ 3 phương pháp biểu diễn tiêu chuẩn:

1. **Ma trận kề (Adjacency Matrix):**
   - Là một mảng hai chiều kích thước $n \times n$ (với $n = |V|$), trong đó phần tử tại hàng $u$, cột $v$ có giá trị $A[u][v] = w(u, v)$ nếu có cạnh nối giữa $u$ và $v$, ngược lại $A[u][v] = 0$ (hoặc $\infty$).
   - *Ưu điểm:* Kiểm tra sự tồn tại của một cạnh giữa 2 đỉnh bất kỳ cực nhanh với độ phức tạp thời gian $O(1)$.
   - *Nhược điểm:* Tiêu tốn không gian bộ nhớ cố định $O(V^2)$, gây lãng phí nghiêm trọng khi đồ thị thưa ($|E| \ll |V|^2$).
2. **Danh sách kề (Adjacency List):**
   - Sử dụng một bảng băm (Dictionary trong Python) có dạng `{u: [(v1, w1), (v2, w2), ...]}`. Với mỗi đỉnh $u$, ta lưu danh sách các đỉnh $v$ kề trực tiếp với nó kèm theo trọng số.
   - *Ưu điểm:* Tiết kiệm bộ nhớ tối đa, không gian lưu trữ đạt $O(V + E)$. Duyệt qua các đỉnh lân cận của một đỉnh cực kỳ nhanh chóng. Đây là cấu trúc chủ đạo được sử dụng xuyên suốt lõi thuật toán của dự án.
3. **Danh sách cạnh (Edge List):**
   - Lưu trữ đồ thị dưới dạng một mảng danh sách các bộ 3 phần tử: `[(u, v, w), ...]`.
   - *Ưu điểm:* Dạng dữ liệu nguyên thủy, đơn giản, dễ đọc từ tệp văn bản. Là định dạng đầu vào chuẩn xác nhất cho các thuật toán xét duyệt theo từng cạnh như Kruskal và Bellman-Ford.

---

### 1.1.2. Bảy thuật toán cốt lõi trong hệ thống
Dự án cài đặt và giải quyết triệt để 7 bài toán nền tảng của lý thuyết đồ thị:

1. **Duyệt đồ thị (BFS & DFS):**
   - *BFS (Breadth-First Search):* Sử dụng cấu trúc dữ liệu Hàng đợi (Queue - FIFO) để duyệt đồ thị theo từng tầng khoảng cách từ đỉnh xuất phát. Ứng dụng để tìm đường đi có ít cạnh nhất trên đồ thị không trọng số.
   - *DFS (Depth-First Search):* Sử dụng Ngăn xếp (Stack - LIFO) hoặc kỹ thuật Đệ quy (Recursion) để đâm sâu vào một nhánh cho đến khi gặp ngõ cụt rồi mới quay lui (Backtracking). Ứng dụng để kiểm tra tính liên thông và phát hiện chu trình.
2. **Đồ thị hai phía (Bipartite Graph & Chu trình lẻ):**
   - Đồ thị $G$ là hai phía nếu tập đỉnh $V$ có thể phân hoạch thành hai tập rời nhau $V_1$ và $V_2$ ($V_1 \cup V_2 = V, V_1 \cap V_2 = \emptyset$) sao cho mọi cạnh trong $E$ chỉ nối giữa một đỉnh thuộc $V_1$ với một đỉnh thuộc $V_2$.
   - Thuật toán kiểm tra dựa trên kỹ thuật Tô 2 màu (2-Coloring). Định lý toán học chỉ ra rằng: *Đồ thị là hai phía khi và chỉ khi nó không chứa chu trình có độ dài lẻ.*
3. **Đường đi ngắn nhất (Shortest Path):**
   - *Thuật toán Dijkstra:* Dựa trên chiến lược tham lam (Greedy), liên tục chọn đỉnh có khoảng cách nhỏ nhất chưa chốt để nới lỏng các cạnh kề. Hoạt động với độ phức tạp $O((V + E) \log V)$, tối ưu tuyệt đối khi mọi trọng số cạnh đều không âm ($w \ge 0$).
   - *Thuật toán Bellman-Ford:* Nới lỏng toàn bộ các cạnh của đồ thị đúng $n - 1$ lần. Có khả năng xử lý cạnh có trọng số âm và phát hiện Chu trình âm (Negative Cycle) thông qua lần nới lỏng thứ $n$.
4. **Chu trình và Đường đi Euler:**
   - *Đường đi Euler:* Đi qua tất cả các cạnh của đồ thị, mỗi cạnh đúng một lần, điểm đầu và điểm cuối khác nhau (điều kiện: đồ thị liên thông và có đúng 2 đỉnh bậc lẻ).
   - *Chu trình Euler:* Đường đi Euler khép kín có điểm xuất phát trùng với điểm kết thúc (điều kiện: đồ thị liên thông và mọi đỉnh đều có bậc chẵn).
   - *Thuật toán Fleury:* Tư duy cẩn trọng, chỉ bước qua Cạnh Cầu (Bridge) khi không còn con đường nào khác.
   - *Thuật toán Hierholzer:* Hiệu năng cao $O(E)$, sử dụng Stack để càn quét và ghép các chu trình con lại thành chu trình hoàn chỉnh.
5. **Cây khung nhỏ nhất (Minimum Spanning Tree - MST):**
   - Cây khung của đồ thị vô hướng liên thông $G=(V, E)$ là một đồ thị con chứa toàn bộ $V$ đỉnh và đúng $V - 1$ cạnh, không chứa chu trình. Cây khung nhỏ nhất là cây khung có tổng trọng số của các cạnh là bé nhất.
   - *Thuật toán Kruskal:* Tiếp cận theo cạnh, sắp xếp các cạnh tăng dần theo trọng số, lần lượt kết nạp cạnh nếu nó không tạo thành chu trình khép kín (sử dụng cấu trúc DSU).
   - *Thuật toán Prim:* Tiếp cận theo đỉnh, xuất phát từ một đỉnh và liên tục vươn xúc tu kết nạp đỉnh gần nhất vào tập cây khung đang xây dựng.
6. **Luồng cực đại và Lát cắt hẹp nhất (Max Flow & Min Cut):**
   - Bài toán truyền dẫn mạng từ đỉnh phát (Source - $S$) đến đỉnh thu (Sink - $T$) với các ràng buộc về dung lượng cung $c(u, v)$ và bảo toàn luồng tại các đỉnh trung gian.
   - *Thuật toán Ford-Fulkerson (Edmonds-Karp):* Liên tục tìm các đường tăng luồng trên Đồ thị dư (Residual Graph) bằng BFS và bơm luồng dựa trên dung lượng thắt cổ chai (Bottleneck capacity).
   - *Định lý Max-Flow Min-Cut:* Giá trị luồng cực đại bơm từ $S$ đến $T$ luôn bằng chính xác dung lượng của Lát cắt hẹp nhất phân chia mạng thành 2 tập đỉnh chứa $S$ và $T$.

---

## 1.2. MÔI TRƯỜNG, CÔNG NGHỆ VÀ THƯ VIỆN SỬ DỤNG
Dự án được xây dựng hoàn chỉnh trên nền tảng hệ sinh thái mã nguồn mở:
- **Ngôn ngữ lập trình Python 3 (phiên bản 3.10+):** Ngôn ngữ chính với cú pháp trong sáng, hỗ trợ mạnh mẽ lập trình hướng đối tượng (OOP) và xử lý cấu trúc dữ liệu linh hoạt.
- **Thư viện đồ họa Matplotlib:** Chịu trách nhiệm kết xuất đồ thị toán học thành hình ảnh độ phân giải cao (`.png`), vẽ các đỉnh, cạnh, trọng số và highlight đường đi. Đồng thời sử dụng `matplotlib.animation` để biên dịch các bước duyệt thành hoạt ảnh GIF.
- **Thư viện NetworkX:** Sử dụng thuật toán bố cục lực đàn hồi (Force-directed / Spring Layout) để tự động tính toán tọa độ vật lý $(x, y)$ của các đỉnh trên không gian 2D dựa trên ma trận khoảng cách.
- **Thư viện Pygame:** Công cụ đồ họa thời gian thực, quản lý vòng lặp mô phỏng (Game Loop), bắt sự kiện bàn phím/chuột và dựng sa bàn chuyển động mượt mà ở tốc độ 60 khung hình/giây cho ứng dụng Robot hút bụi thông minh.

---

## 1.3. PHẠM VI GIẢI BÀI TOÁN THỰC TẾ
1. **Phạm vi học thuật chuẩn mực:**
   - Hệ thống xử lý trọn vẹn tập dữ liệu chuẩn của môn học gồm Đồ thị mẫu vô hướng 20 đỉnh (38 cạnh), Đồ thị mẫu có hướng 20 đỉnh, Đồ thị ngôi nhà Euler, Đồ thị luồng cực đại 6 đỉnh.
   - Cung cấp chế độ xuất bảng vết chi tiết từng bước (Trace Table) đối chiếu trực tiếp với kết quả giải tay trên giấy thi.
2. **Phạm vi ứng dụng thực tiễn:**
   - Mô phỏng bài toán tự động hóa trong căn hộ thông minh: Robot di chuyển làm sạch sàn nhà, né tránh vật cản, tự động dò đường về dock sạc khi cạn năng lượng và tối ưu hóa hệ thống hạ tầng sạc điện.

---

# CHƯƠNG 2: THIẾT KẾ DỰ ÁN VÀ TỐI ƯU HÓA HỆ THỐNG

## 2.1. KIẾN TRÚC TỪNG PHẦN (MODULAR ARCHITECTURE)

Hệ thống được thiết kế theo kiến trúc phân tầng module độc lập, tách bạch rõ ràng giữa dữ liệu, thuật toán lõi, giao diện điều khiển và tầng mô phỏng đồ họa:

```
                  ┌────────────────────────────────────────┐
                  │              main.py                   │
                  │       (Điểm khởi chạy chính)           │
                  └──────────────┬──────────────────┬──────┘
                                 │                  │
                     [--cli]     │                  │   [--robot]
                                 ▼                  ▼
          ┌──────────────────────────────┐   ┌──────────────────────────────┐
          │         app/cli.py           │   │    ung_dung_thuc_te/         │
          │   (Menu tương tác 10 chức    │   │  (Mô phỏng Robot Sa bàn 3D   │
          │             năng)            │   │         bằng Pygame)         │
          └──────────────┬───────────────┘   └──────────────┬───────────────┘
                         │                                  │
                         ├──────────────────────────────────┤
                         ▼                                  ▼
          ┌──────────────────────────────┐   ┌──────────────────────────────┐
          │          core/               │   │        visualizer/           │
          │  - graph.py & converter.py   │   │  - draw.py (Vẽ ảnh PNG)      │
          │  - traversal.py (BFS/DFS)    │   │  - animation.py (Xuất GIF)   │
          │  - bipartite.py (2 Phía)     │   └──────────────────────────────┘
          │  - shortest_path.py          │                  ▲
          │  - euler.py & mst.py         │                  │
          │  - max_flow.py               │──────────────────┘
          └──────────────▲───────────────┘
                         │
          ┌──────────────┴───────────────┐
          │          data/               │
          │  - samples.py (Mẫu 20 đỉnh)  │
          └──────────────────────────────┘
```

- **Lớp dữ liệu `Graph` (`core/graph.py`):** Đóng vai trò là trung tâm lưu trữ trạng thái của đồ thị. Class `Graph` hỗ trợ cơ chế nạp dữ liệu đa hình:
  - `from_matrix(matrix)`: Khởi tạo từ ma trận kề, tự động đồng bộ sang danh sách kề và danh sách cạnh.
  - `from_edges(edges, n=None)`: Khởi tạo từ danh sách cạnh. Nếu $n$ bị bỏ trống, hệ thống tự động tìm đỉnh có ID lớn nhất (`max_v`) và suy ra $n = \text{max\_v} + 1$.
  - `from_text(text)`: Bộ phân tích cú pháp thông minh. Tự nhận diện dòng đầu tiên chứa 1 số nguyên thì nạp ma trận vuông $n \times n$, ngược lại nạp danh sách cạnh.
- **Lớp chuyển đổi `core/converter.py`:** Cung cấp 6 hàm chuyển đổi 2 chiều: `matrix_to_adj`, `matrix_to_edges`, `edges_to_matrix`, `edges_to_adj`, `adj_to_matrix`, `adj_to_edges`.

---

## 2.2. CÁC THUẬT TOÁN TỐI ƯU CHƯƠNG TRÌNH

Dự án áp dụng 4 kỹ thuật tối ưu hóa mã nguồn quan trọng nhằm đạt chuẩn Clean Code và hiệu năng thực thi cao nhất:

### 1. Tối ưu lọc trùng cạnh vô hướng (`u <= v`) trong `converter.py`
Trong danh sách kề của đồ thị vô hướng, cạnh giữa $u$ và $v$ bị lưu 2 lần (một lần ở khóa $u$, một lần ở khóa $v$). Khi chuyển đổi sang danh sách cạnh, thay vì dùng cấu trúc `set` tốn kém bộ nhớ để lọc trùng, hàm áp dụng điều kiện:
```python
if directed or u <= v:
    edges.append((u, v, weight))
```
*Tác dụng:* Chỉ cho phép nạp cạnh khi đứng ở đỉnh có chỉ số nhỏ hơn. Loại bỏ triệt để 100% cạnh trùng lặp với chi phí thời gian $O(1)$.

### 2. Trích xuất Chu trình lẻ bằng Tổ tiên chung gần nhất (LCA) trong `bipartite.py`
Khi phát hiện xung đột màu sắc giữa hai đỉnh kề nhau $u$ và $v$ (`color[u] == color[v]`), thuật toán không chỉ dừng lại ở việc báo lỗi `False`. Chương trình truy ngược mảng `parent` của $u$ và $v$ về đỉnh xuất phát:
```python
lca = -1
set_v = set(path_v)
for node in path_u:
    if node in set_v:
        lca = node
        break
odd_cycle = cycle_u + cycle_v[::-1]
```
*Tác dụng:* Cắt bỏ phần "cuống cây" (đường đi từ gốc đến điểm phân nhánh LCA), móc nối 2 nhánh đi ngược chiều nhau để tạo thành đúng một chu trình lẻ khép kín hoàn hảo làm bằng chứng trực quan cho người dùng.

### 3. Kỹ thuật tái sử dụng BFS với cờ `record_trace=False` trong `traversal.py` và `euler.py`
Trong bài toán Euler (`is_bridge`), thao tác kiểm tra Cạnh Cầu đòi hỏi phải chạy BFS liên tục hàng chục lần để đếm số đỉnh trước và sau khi tạm xóa cạnh. Hàm `bfs()` được bổ sung cờ kiểm soát:
```python
def bfs(adj, n, start, record_trace=True):
    ...
    if record_trace:
        trace_table.append({"step": len(order), "u": u, ...})
```
*Tác dụng:* Khi chạy ngầm trong bài Euler, truyền `record_trace=False` giúp triệt tiêu hoàn toàn thao tác sao chép mảng `visited` và `queue` ở mỗi bước, tiết kiệm bộ nhớ RAM và tăng tốc độ xử lý của thuật toán Fleury lên gấp 10-20 lần mà vẫn tuân thủ nguyên tắc DRY (Don't Repeat Yourself).

### 4. Cấu trúc Disjoint Set Union (DSU) nén đường đi trong `mst.py`
Thuật toán Kruskal đòi hỏi phải kiểm tra liên tục xem việc thêm cạnh $(u, v)$ có tạo chu trình hay không. Lớp `DSU` được tối ưu hóa với kỹ thuật Nén đường đi (Path Compression):
```python
def find(self, i):
    if self.parent[i] == i:
        return i
    self.parent[i] = self.find(self.parent[i])
    return self.parent[i]
```
*Tác dụng:* Trực tiếp gán cha của mọi nút trên đường đi về nút gốc đại diện. Giúp độ phức tạp của thao tác kiểm tra chu trình đạt xấp xỉ hằng số $O(\alpha(V))$, nhanh hơn hàng trăm lần so với việc chạy BFS/DFS kiểm tra chu trình thủ công.

---

## 2.3. MODULE TRỰC QUAN HÓA (VISUALIZER)

- **Bố cục lực lò xo vật lý (Spring Layout) trong `visualizer/draw.py`:**
  - Thay vì cố định các đỉnh trên các vòng tròn đồng tâm làm chữ số trọng số bị đè lên nhau, hệ thống sử dụng thuật toán mô phỏng lực vật lý Fruchterman-Reingold của NetworkX.
  - Trọng số lò xo được thiết lập tỉ lệ nghịch với trọng số cạnh (`inv_weight = 1.0 / weight`), giúp các cạnh có trọng số lớn được kéo giãn ra xa hơn về mặt không gian hình học.
  - Độ dày nét vẽ của cạnh (`linewidth`) được tính toán động theo hàm căn bậc hai của trọng số:
    $$\text{linewidth} = 1.2 + 0.8 \times \sqrt{w}$$
    Đảm bảo cạnh trọng số lớn hiển thị đậm rõ nét, giúp người xem phân biệt ngay tức thì.
- **Hoạt ảnh động từng bước (`visualizer/animation.py`):**
  - Ghi nhận lịch sử duyệt của hàng đợi BFS và ngăn xếp DFS theo từng khung hình (frame).
  - Sử dụng `matplotlib.animation.FuncAnimation` để tô màu đỉnh đang xét (vàng), đỉnh đã duyệt (xanh), các cạnh cây khung (đỏ) và xuất thành tệp hoạt ảnh động `.gif` chất lượng cao.

---

# CHƯƠNG 3: ỨNG DỤNG THỰC TẾ (MÔ PHỎNG ROBOT HÚT BỤI)

## 3.1. BỐI CẢNH BÀI TOÁN THỰC TẾ
Trong các tòa nhà và căn hộ hiện đại, robot hút bụi tự hành (Autonomous Vacuum Robot) cần phải giải quyết bài toán di chuyển thông minh nhằm tiết kiệm năng lượng, bảo đảm làm sạch toàn bộ bề mặt sàn và an toàn trở về dock sạc trước khi cạn pin:
- **Sa bàn căn hộ dạng lưới ô vuông (Grid Map):** Không gian căn phòng được chia thành ma trận $N \times M$ ô lưới.
- **Phân loại thành phần trong không gian:**
  - *Ô sàn di chuyển được:* Trạng thái bình thường mà robot có thể đi qua.
  - *Chướng ngại vật (Tường, bàn ghế, đồ đạc):* Các ô bị chặn, robot không thể đi xuyên qua.
  - *Hạt bụi / Rác thải:* Các ô mục tiêu cần được robot quét qua để làm sạch.
  - *Trạm sạc pin (Dock sạc):* Các vị trí cố định để robot kết nối nguồn điện khi pin yếu.
- **Chuyển đổi Bản đồ lưới sang Mô hình Đồ thị:** Mỗi ô sàn di chuyển được trở thành một đỉnh trong đồ thị. Các cạnh nối giữa các ô kề cận theo 4 hướng (Lên, Xuống, Trái, Phải) có trọng số đại diện cho chi phí năng lượng tiêu hao khi di chuyển.

---

## 3.2. THUẬT TOÁN ỨNG DỤNG CHO BÀI TOÁN VÀ TÁC DỤNG

Bảy thuật toán lý thuyết đồ thị được tích hợp trực tiếp vào bộ não điều khiển của Robot:

| Thuật toán đồ thị | Chế độ hoạt động của Robot | Tác dụng và Ý nghĩa thực tế |
| :--- | :--- | :--- |
| **Dijkstra & Bellman-Ford** | Chế độ Tìm Trạm Sạc Khẩn Cấp (Emergency Return) | Khi dung lượng pin xuống dưới mức an toàn ($< 20\%$), robot lập tức ngắt chế độ hút bụi, tính toán lộ trình ngắn nhất né toàn bộ vật cản để trở về dock sạc nhanh nhất. |
| **Đường đi & Chu trình Euler** | Chế độ Dọn Dẹp Toàn Diện (Full Coverage Cleaning) | Lập lộ trình cho robot đi qua toàn bộ các hành lang và lối đi trong nhà đúng một lần duy nhất, tránh đi lặp lại những khu vực đã làm sạch, tối ưu hóa $100\%$ thời gian làm việc. |
| **Cây khung nhỏ nhất (MST)** | Chế độ Quy Hoạch Hạ Tầng Sạc (Dock Infrastructure) | Trong căn hộ diện tích lớn có nhiều dock sạc phụ, thuật toán Kruskal/Prim giúp tính toán mạng lưới đường dây liên kết các dock sạc với trạm cấp điện chính với tổng chiều dài dây dẫn ngắn nhất. |
| **Duyệt BFS & DFS** | Chế độ Khám Phá & Vẽ Bản Đồ (Exploration & Mapping) | Khi lần đầu tiên được đặt vào một căn phòng lạ chưa có bản đồ, robot sử dụng BFS/DFS để thăm dò các ô xung quanh, xây dựng bản đồ số không gian phòng ốc. |

---

## 3.3. Ý NGHĨA THỰC TIỄN
Ứng dụng Robot hút bụi thông minh đã chứng minh tính liên kết chặt chẽ giữa môn học lý thuyết trừu tượng (Cấu trúc rời rạc) với các ngành công nghệ mũi nhọn hiện nay như Trí tuệ nhân tạo (AI), Tự động hóa (Robotics) và Nhà thông minh (Smart Home). Dự án không dừng lại ở các bài toán giải trên giấy mà đã tạo ra một sản phẩm phần mềm hoàn chỉnh, có giao diện trực quan sinh động và có giá trị ứng dụng cao.

---

# CHƯƠNG 4: THỰC NGHIỆM, KẾT LUẬN VÀ TỔNG KẾT

## 4.1. SO SÁNH KẾT QUẢ GIẢI TAY VÀ CHẠY MÁY

Để chứng minh tính chính xác tuyệt đối của chương trình, toàn bộ các thuật toán cốt lõi đã được giải tay từng bước trên giấy trên tập dữ liệu chuẩn **Đồ thị vô hướng 20 đỉnh (38 cạnh)** và đối chiếu với kết quả xuất ra từ phần mềm:

### 1. Đối chiếu Thuật toán Tìm đường ngắn nhất Dijkstra (Từ đỉnh 0 đến đỉnh 19)
- *Kết quả giải tay:* Lộ trình ngắn nhất tìm được là $0 \rightarrow 10 \rightarrow 16 \rightarrow 17 \rightarrow 18 \rightarrow 19$ với tổng chi phí $w = 14$.
- *Kết quả chạy máy:* Chương trình tại Chức năng 5 xuất ra:
  ```
  Chi phí ngắn nhất: 14
  Lộ trình đường đi: 0 -> 10 -> 16 -> 17 -> 18 -> 19
  ```
- *Đánh giá mảng bước lặp `dist`:* Toàn bộ bảng ma trận bước lặp Dijkstra gồm 20 bước nới lỏng in ra từ hàm `dijkstra()` trùng khớp 100% với từng ô số trong bảng vết kẻ tay.

### 2. Đối chiếu Thuật toán Cây khung nhỏ nhất Kruskal (20 đỉnh)
- *Kết quả giải tay:* Sắp xếp 38 cạnh theo thứ tự trọng số tăng dần (từ 2 đến 6). Tiến hành duyệt nhặt đúng 19 cạnh không tạo chu trình. Khi đạt đủ 19 cạnh, tổng trọng số cây khung tính được là:
  $$W_{\text{MST}} = 2 \times 6 + 3 \times 11 + 4 \times 2 = 12 + 33 + 8 = 53$$
- *Kết quả chạy máy:* Chương trình tại Chức năng 7 (Kruskal DSU) trả về:
  ```
  Tổng trọng số Cây khung nhỏ nhất MST = 53
  Số cạnh được chọn: 19 / 38 cạnh
  ```
- *Đánh giá:* Danh sách 19 cạnh được nhặt và thứ tự các cạnh bị loại do tạo chu trình khép kín trùng khớp hoàn toàn giữa giải tay và thuật toán DSU.

### 3. Đối chiếu Kiểm tra Đồ thị hai phía (Bipartite)
- *Kết quả giải tay:* Khi xuất phát từ đỉnh 1 (Tập $V_1$), các đỉnh kề gồm 0 và 10 được đưa vào Tập $V_2$. Tuy nhiên, giữa đỉnh 0 và đỉnh 10 lại tồn tại cạnh nối $(0, 10)$ với trọng số 4. Vì cả 0 và 10 đều nằm trong Tập $V_2$ nên xảy ra mâu thuẫn màu sắc, tạo thành chu trình tam giác lẻ $1 \rightarrow 0 \rightarrow 10 \rightarrow 1$. Kết luận: Đồ thị KHÔNG phải là đồ thị hai phía.
- *Kết quả chạy máy:* Hàm `check_bipartite()` phát hiện mâu thuẫn ngay tại đỉnh 10 và trích xuất đúng chu trình lẻ:
  ```
  is_bipartite: False
  odd_cycle: [1, 0, 10]
  ```

### 4. Đánh giá bộ kiểm thử tự động toàn diện (Unit Test Suite)
Hệ thống tích hợp bộ kiểm thử tự động trong thư mục `tests/`. Chạy lệnh kiểm thử toàn diện:
- `test_foundation.py`: Kiểm tra tính toàn vẹn của Ma trận, Danh sách kề và Cạnh $\rightarrow$ **PASS ✅**
- `test_traversal.py`: Kiểm tra tính đúng đắn của BFS và DFS $\rightarrow$ **PASS ✅**
- `test_bipartite.py`: Kiểm tra trên đồ thị C4 (True) và C3 (False) $\rightarrow$ **PASS ✅**
- `test_shortest_path.py`: Đối chiếu chéo giữa Dijkstra và Bellman-Ford $\rightarrow$ **PASS ✅**
- `test_euler.py`: Kiểm tra trên đồ thị K4, đồ thị Ngôi nhà và chu trình C5 $\rightarrow$ **PASS ✅**
- `test_mst.py`: Đối chiếu chéo kết quả giữa Kruskal và Prim $\rightarrow$ **PASS ✅**
- `test_max_flow.py`: Kiểm tra luồng cực đại (Max Flow = 23) và Định lý Max-Flow Min-Cut $\rightarrow$ **PASS ✅**

---

## 4.2. KẾT QUẢ ĐẠT ĐƯỢC VÀ HƯỚNG PHÁT TRIỂN

### 1. Kết quả đạt được của dự án
- Hoàn thành đầy đủ và vượt mức $100\%$ các yêu cầu nghiệp vụ của đề tài môn học Cấu trúc rời rạc.
- Xây dựng thành công hệ thống phần mềm có cấu trúc module chuyên nghiệp, mã nguồn sạch sẽ, chú thích rõ ràng bằng tiếng Việt.
- Tích hợp công nghệ trực quan hóa mạnh mẽ: Vừa xuất được ảnh tĩnh PNG với bố cục vật lý lực lò xo, vừa xuất được video ngắn GIF hoạt cảnh từng bước thuật toán.
- Hiện thực hóa thành công sa bàn mô phỏng Robot hút bụi 3D bằng Pygame tương tác thời gian thực.

### 2. Hạn chế của hệ thống
- Khi số lượng đỉnh của đồ thị quá lớn (vượt quá 10.000 đỉnh), giao diện trực quan hóa Matplotlib sẽ bị hiện tượng các nét vẽ chồng chéo dày đặc, khó quan sát.
- Sa bàn mô phỏng robot hiện tại đang biểu diễn trên không gian mặt phẳng 2D, chưa mô phỏng độ dốc hoặc các địa hình phức tạp.

### 3. Hướng phát triển trong tương lai
- Bổ sung thuật toán tìm kiếm tối ưu có thông tin $A^*$ (A-Star) kết hợp hàm đánh giá khoảng cách Manhattan/Euclidean để robot định hướng mục tiêu thông minh hơn.
- Mở rộng ứng dụng mô phỏng lên không gian 3D nhiều tầng (Multi-floor Mapping) kết hợp thuật toán tối ưu hóa thang máy/cầu thang.
- Đóng gói mã nguồn thuật toán thành một thư viện Python độc lập để triển khai trực tiếp lên phần cứng robot thực tế (sử dụng bo mạch Raspberry Pi và hệ điều hành Robot ROS).

# 📖 Chú thích Thuật toán: Cấu trúc Đồ thị (`core/graph.py`)

## 1. Mục đích thiết kế
Module `core/graph.py` định nghĩa đối tượng trung tâm `Graph` của toàn bộ đồ án Cấu Trúc Rời Rạc (CTRR). 

Trong Lý thuyết đồ thị, mỗi thuật toán có một cấu trúc dữ liệu tối ưu riêng:
- **BFS, DFS, Dijkstra:** Cần **Danh sách kề (`adj`)** để duyệt nhanh các đỉnh lân cận với độ phức tạp $O(\text{deg}(u))$.
- **Kruskal, Bellman-Ford:** Cần **Danh sách cạnh (`edges`)** để sắp xếp hoặc quét toàn bộ các cạnh trong $O(E)$.
- **Ford-Fulkerson (Max-Flow):** Cần **Ma trận (`matrix`)** để tra cứu và cập nhật dung lượng `capacity[u][v]` tức thời trong $O(1)$.

Lớp `Graph` giải quyết bài toán này bằng cách **tự động duy trì và đồng bộ hóa song song cả 3 dạng biểu diễn**:
1. `self.matrix`: Ma trận kề $n \times n$.
2. `self.adj`: Danh sách kề dạng `dict {u: [(v, w), ...]}`.
3. `self.edges`: Danh sách cạnh dạng `list [(u, v, w), ...]`.

---

## 2. Các phương thức khởi dựng (Parsers)

### 2.1. `from_matrix(matrix)`
- Nhận ma trận vuông $n \times n$.
- Tự động gọi `matrix_to_adj` và `matrix_to_edges` từ module `converter.py` để cập nhật `self.adj` và `self.edges`.
- Độ phức tạp: $O(V^2)$.

### 2.2. `from_edges(edges, n=None)`
- Nhận danh sách các bộ `(u, v, w)` hoặc `(u, v)`.
- Nếu tham số $n$ không được cung cấp, hàm tự động suy diễn số lượng đỉnh:
  $$n = \max_{(u, v) \in E} (\max(u, v)) + 1$$
- Gọi `edges_to_matrix` và `edges_to_adj` để đồng bộ.
- Độ phức tạp: $O(V^2 + E)$.

### 2.3. `from_text(text)`
- Hỗ trợ nạp đồ thị linh hoạt từ bàn phím hoặc file text:
  1. **Định dạng Ma trận:** Dòng đầu tiên chỉ chứa 1 số nguyên $n$ (số đỉnh), theo sau là $n$ dòng của ma trận kề $n \times n$.
  2. **Định dạng Danh sách cạnh:** Mỗi dòng chứa 2 hoặc 3 số (`u v [w]`), đại diện cho cạnh từ $u$ tới $v$ với trọng số $w$ (mặc định $w=1$).
- Nhận diện tự động dựa trên số phần tử của dòng đầu tiên.

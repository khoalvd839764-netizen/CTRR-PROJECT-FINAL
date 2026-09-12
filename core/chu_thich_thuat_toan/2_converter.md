# 📖 Chú thích Thuật toán: Chuyển đổi Biểu diễn Đồ thị (`core/converter.py`)

## 1. Nguyên lý toán học & Quy ước
Đồ thị $G = (V, E)$ có 3 cách biểu diễn kinh điển:
1. **Ma trận kề (Adjacency Matrix):** Mảng 2 chiều kích thước $n \times n$. Nếu có cạnh nối giữa $u$ và $v$, $M[u][v] = w$, ngược lại bằng $0$.
   - Với đồ thị vô hướng: Ma trận luôn đối xứng qua đường chéo chính, nghĩa là $M[u][v] = M[v][u]$.
2. **Danh sách kề (Adjacency List):** Cấu trúc dictionary ánh xạ từ đỉnh $u$ sang danh sách các cặp $(v, w)$ đỉnh kề.
3. **Danh sách cạnh (Edge List):** Danh sách các bộ ba $(u, v, w)$.

---

## 2. Chi tiết 6 hàm chuyển đổi hai chiều

### 2.1. `matrix_to_adj(matrix, directed=False)`
- **Thuật toán:** Quét từng ô $(i, j)$ trong ma trận $n \times n$. Nếu $M[i][j] \ne 0$, kết nạp $(j, M[i][j])$ vào `adj[i]`.
- **Độ phức tạp:** $O(V^2)$.

### 2.2. `matrix_to_edges(matrix, directed=False)`
- **Điểm cốt lõi:**
  - Nếu đồ thị có hướng (`directed=True`): Quét toàn bộ ô $j \in [0, n-1]$.
  - Nếu đồ thị vô hướng (`directed=False`): Chỉ cần quét nửa trên tam giác của ma trận ($j \in [i, n-1]$) để tránh ghi nhận cạnh hai lần (cạnh $(i, j)$ và $(j, i)$ cùng đại diện cho 1 cạnh vô hướng).
- **Độ phức tạp:** $O(V^2)$.

### 2.3. `edges_to_matrix(edges, n, directed=False)`
- **Thuật toán:** Khởi tạo ma trận toàn số $0$. Với mỗi cạnh $(u, v, w)$, gán $M[u][v] = w$. Nếu là đồ thị vô hướng, gán thêm $M[v][u] = w$.
- **Độ phức tạp:** $O(V^2 + E)$.

### 2.4. `edges_to_adj(edges, n, directed=False)`
- **Thuật toán:** Thêm $(v, w)$ vào `adj[u]`. Nếu vô hướng, thêm đối xứng $(u, w)$ vào `adj[v]`.
- **Độ phức tạp:** $O(V + E)$.

### 2.5. `adj_to_matrix(adj, n)`
- **Thuật toán:** Lặp qua từng đỉnh $u$ và danh sách kề $(v, w)$, gán ô ma trận tương ứng $M[u][v] = w$.
- **Độ phức tạp:** $O(V^2 + E)$.

### 2.6. `adj_to_edges(adj, directed=False)`
- **Khử trùng lặp cạnh vô hướng:** Với đồ thị vô hướng, cạnh $(u, v)$ xuất hiện trong cả `adj[u]` và `adj[v]`. Để không ghi lặp, hàm chỉ kết nạp khi $u \le v$.
- **Độ phức tạp:** $O(V + E)$.

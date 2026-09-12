# 📖 Chú thích Thuật toán: Luồng Cực Đại & Lát Cắt Hẹp Nhất (`core/max_flow.py`)

## 1. Mạng Luồng & Định lý Max-Flow Min-Cut
- Mạng luồng $G = (V, E)$ là đồ thị có hướng, mỗi cung $(u, v)$ có dung lượng $c(u, v) \ge 0$.
- Có 1 đỉnh Nguồn (Source - $S$) phát luồng và 1 đỉnh Đích (Sink - $T$) thu luồng.
- **Định lý Max-Flow Min-Cut:**
  > Giá trị luồng cực đại từ $S$ đến $T$ **bằng đúng** tổng dung lượng của lát cắt hẹp nhất phân hoạch hai tập đỉnh $(S_{\text{set}}, T_{\text{set}})$.

---

## 2. Biến thể Edmonds-Karp (Ford-Fulkerson dùng BFS)
Thay vì dùng DFS dễ rơi vào lặp dài, biến thể Edmonds-Karp sử dụng **BFS** để luôn tìm đường tăng luồng có **ít cạnh nhất** từ $S$ đến $T$ trên đồ thị phần dư.

### Các bước thực hiện:
1. **Khởi tạo Đồ thị phần dư (Residual Graph):** Ban đầu dung lượng thặng dư `residual` bằng đúng dung lượng ban đầu `capacity`.
2. **Vòng lặp tăng luồng:**
   - Dùng BFS tìm đường tăng luồng ngắn nhất `path` từ $S$ đến $T$ trên các cung có `residual[u][v] > 0`.
   - Nếu không còn đường tới $T \implies$ Đã đạt Luồng cực đại, dừng lặp.
   - Tìm **Nghẽn cổ chai (Bottleneck):**
     $$\text{bottleneck} = \min_{(u, v) \in \text{path}} \text{residual}[u][v]$$
   - **Cập nhật đồ thị phần dư:**
     - Giảm cung thuận: $\text{residual}[u][v] \gets \text{residual}[u][v] - \text{bottleneck}$
     - Tăng cung nghịch: $\text{residual}[v][u] \gets \text{residual}[v][u] + \text{bottleneck}$
     *(Cung nghịch cho phép các bước sau có thể hủy hoặc chuyển hướng luồng đẩy sai, đảm bảo nghiệm tối ưu toàn cục).*
   - Cộng dồn $\text{max\_flow} \gets \text{max\_flow} + \text{bottleneck}$.

---

## 3. Xác định Lát cắt hẹp nhất (Min-Cut $S - T$)
Khi không còn đường tăng luồng:
1. Chạy BFS từ đỉnh nguồn $S$ trên đồ thị phần dư cuối cùng.
2. Tập tất cả các đỉnh còn đến được từ $S$ (qua cung có `residual > 0`) tạo thành tập $S_{\text{set}}$.
3. Tập các đỉnh còn lại là $T_{\text{set}} = V \setminus S_{\text{set}}$.
4. Các cung ban đầu $u \rightarrow v$ với $u \in S_{\text{set}}$ và $v \in T_{\text{set}}$ chính là các cung thuộc **Lát cắt hẹp nhất (Min-Cut)**. Tổng dung lượng ban đầu của các cung này bằng đúng giá trị Max Flow.

---

## 4. Độ phức tạp tính toán
- Thuật toán Edmonds-Karp luôn kết thúc trong thời gian $O(V \cdot E^2)$, độc lập hoàn toàn với giá trị dung lượng trên các cạnh.

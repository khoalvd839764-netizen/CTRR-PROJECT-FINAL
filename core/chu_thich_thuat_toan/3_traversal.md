# 📖 Chú thích Thuật toán: Duyệt Đồ thị BFS & DFS (`core/traversal.py`)

## 1. Nguyên lý tổng quát
Duyệt đồ thị là quá trình ghé thăm tất cả các đỉnh có thể đến được từ một đỉnh nguồn `start`:
1. **BFS (Breadth-First Search - Duyệt theo chiều rộng):**
   - Sử dụng cấu trúc hàng đợi **FIFO (First-In First-Out)**.
   - Quét loang theo từng tầng khoảng cách: xét đỉnh nguồn $\rightarrow$ các đỉnh cách 1 cạnh $\rightarrow$ các đỉnh cách 2 cạnh...
2. **DFS (Depth-First Search - Duyệt theo chiều sâu):**
   - Sử dụng **Ngăn xếp Call Stack (Đệ quy)**.
   - Đi sâu nhất có thể theo một nhánh cho tới khi gặp ngõ cụt, sau đó quay lui (Backtracking) để khám phá nhánh còn lại.

---

## 2. Quy ước chuẩn mực giải tay của sinh viên (Tie-Breaking Rule)
Trong các đề thi và bài tập môn CTRR, khi một đỉnh có nhiều đỉnh kề chưa thăm, quy ước chuẩn mực là:
> **Luôn ưu tiên chọn đỉnh có chỉ số nhỏ hơn trước (`sorted`).**

Cả 2 hàm `bfs()` và `dfs()` đều thực thi lệnh `sorted([v for v, w in adj.get(u, [])])` trước khi duyệt, đảm bảo thứ tự duyệt và cây khung sinh ra trùng khớp 100% với bài giải tay trên giấy.

---

## 3. Cấu trúc đầu ra
Mỗi hàm trả về một bộ gồm 3 thành phần:
1. `order`: Danh sách thứ tự duyệt các đỉnh (ví dụ: `[0, 1, 2, 3]`).
2. `tree_edges`: Danh sách các cạnh tạo nên Cây khung duyệt đồ thị (Tree Edges) (ví dụ: `[(0, 1), (0, 2), (1, 3)]`).
3. `trace_table`: Bảng vết từng bước lặp:
   - Ghi nhận chỉ số bước `step`, đỉnh hiện tại `u`, trạng thái hàng đợi `queue` (hoặc stack) và mảng đánh dấu `visited` tại từng bước lặp để xuất ra console hoặc báo cáo.

---

## 4. Độ phức tạp tính toán
- Sử dụng danh sách kề: $O(V + E)$.
- Bộ nhớ bổ sung: $O(V)$ cho mảng `visited` và hàng đợi `queue`.

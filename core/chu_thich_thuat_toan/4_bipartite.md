# 📖 Chú thích Thuật toán: Kiểm tra Đồ thị Hai phía & Chu trình lẻ (`core/bipartite.py`)

## 1. Định lý Toán học Rời rạc
> **Định lý König:** Một đồ thị là đồ thị hai phía (Bipartite Graph) KHI VÀ CHỈ KHI nó **không chứa bất kỳ chu trình có độ dài lẻ** (Odd Cycle) nào.

Nếu đồ thị là hai phía, tập đỉnh $V$ có thể phân hoạch thành hai tập rời nhau $V_1$ và $V_2$ sao cho mọi cạnh trong $E$ chỉ nối giữa một đỉnh thuộc $V_1$ và một đỉnh thuộc $V_2$ (không có cạnh nào nối giữa 2 đỉnh cùng một tập).

---

## 2. Thuật toán Tô 2 màu bằng BFS (2-Coloring)
1. **Quy ước trạng thái màu:**
   - `0`: Đỉnh chưa xét / chưa tô màu.
   - `1`: Màu Đỏ (Tập $V_1$).
   - `-1`: Màu Xanh (Tập $V_2$).
2. **Xử lý đa thành phần liên thông:** Vòng lặp ngoài duyệt từ $0$ đến $n-1$, nếu `color[start] == 0` thì khởi động BFS từ `start` với `color[start] = 1`.
3. **Lan truyền màu:** Với mỗi đỉnh kề $v$ của $u$:
   - Nếu $v$ chưa tô màu: gán màu ngược lại với $u$: `color[v] = -color[u]`, ghi nhận `parent[v] = u` và đẩy $v$ vào queue.
   - Nếu $v$ đã tô màu và `color[v] == color[u]`: **Phát hiện xung đột màu!** Đồ thị chắc chắn không phải hai phía.

---

## 3. Kỹ thuật trích xuất Chu trình lẻ (Odd Cycle) bằng LCA
Khi phát hiện xung đột màu giữa 2 đỉnh kề $u$ và $v$ (`color[u] == color[v]`):
1. **Truy ngược đường đi:** Lần ngược mảng `parent` từ $u$ về gốc để lập danh sách `path_u`. Làm tương tự từ $v$ để lập danh sách `path_v`.
2. **Tìm Tổ tiên chung gần nhất (LCA - Lowest Common Ancestor):** Điểm chung đầu tiên xuất hiện trong cả `path_u` và `path_v`.
3. **Ghép chu trình lẻ:**
   - Lấy đoạn $u \rightsquigarrow \text{LCA}$ từ `path_u`.
   - Lấy đoạn $\text{LCA} \rightsquigarrow v$ từ `path_v` (đảo ngược thứ tự).
   - Ghép thêm cạnh nối trực tiếp $(v, u)$ để khép kín chu trình lẻ làm bằng chứng toán học phản bác tính hai phía.

---

## 4. Độ phức tạp tính toán
- Duyệt BFS qua tất cả các đỉnh và cạnh: $O(V + E)$.
- Tìm LCA và ghép chu trình: $O(V)$.
- Tổng độ phức tạp: $O(V + E)$.

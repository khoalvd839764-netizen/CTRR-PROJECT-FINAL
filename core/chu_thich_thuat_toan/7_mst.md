# 📖 Chú thích Thuật toán: Cây Khung Nhỏ Nhất & DSU (`core/mst.py`)

## 1. Khái niệm Cây Khung Nhỏ Nhất (MST)
- Cho đồ thị vô hướng liên thông $G = (V, E)$ có trọng số.
- Cây khung (Spanning Tree) là đồ thị con liên thông chứa tất cả $n$ đỉnh của $G$ và đúng $n-1$ cạnh, không chứa chu trình.
- Cây khung nhỏ nhất (MST) là cây khung có **tổng trọng số các cạnh là nhỏ nhất**.

---

## 2. Cấu trúc dữ liệu Disjoint Set Union (DSU)
Để kiểm tra xem 2 đỉnh $u$ và $v$ đã cùng thuộc một thành phần liên thông hay chưa (tránh tạo chu trình khi thêm cạnh), lớp `DSU` áp dụng 2 kỹ thuật tối ưu hóa kinh điển:

1. **Nén đường đi (Path Compression) trong `find(i)`:**
   - Trong quá trình đệ quy tìm gốc, trỏ thẳng cha của mọi nút dọc đường về đỉnh gốc:
     $$\text{self.parent}[i] = \text{self.find}(\text{self.parent}[i])$$
   - Giúp giảm chiều cao của cây xuống gần như $O(1)$ trong các lần truy vấn tiếp theo.
2. **Gộp theo hạng (Union by Rank) trong `union(i, j)`:**
   - So sánh chiều cao ước lượng (`rank`) của hai cây. Luôn gắn gốc của cây thấp hơn vào dưới gốc của cây cao hơn để giữ cây cân bằng.
   - Trả về `False` nếu $i$ và $j$ đã cùng chung một gốc (thêm cạnh sẽ tạo chu trình), `True` nếu hợp nhất thành công.

---

## 3. Thuật toán Kruskal
- **Chiến lược:** Tiếp cận toàn cục trên tập cạnh đã sắp xếp (Greedy):
  1. Sắp xếp toàn bộ các cạnh theo trọng số tăng dần: $w_1 \le w_2 \le \dots \le w_E$.
  2. Khởi tạo cấu trúc DSU với $n$ tập hợp riêng biệt.
  3. Lần lượt xét từng cạnh $(u, v, w)$ từ nhẹ nhất đến nặng nhất:
     - Dùng `dsu.union(u, v)` kiểm tra: nếu không tạo chu trình $\implies$ kết nạp cạnh vào MST.
     - Nếu tạo chu trình $\implies$ loại bỏ cạnh.
  4. **Dừng sớm:** Dừng ngay khi đã kết nạp đủ đúng $n-1$ cạnh.
- **Độ phức tạp:** $O(E \log E)$ chi phối bởi bước sắp xếp cạnh.

---

## 4. Thuật toán Prim
- **Chiến lược:** Tiếp cận lát cắt (Cut Property):
  1. Khởi đầu với tập đỉnh trong cây $S = \{\text{start}\}$, tập đỉnh ngoài cây $V \setminus S$.
  2. Tại mỗi bước, tìm cạnh nhẹ nhất $(u, v, w)$ bắc qua lát cắt giữa $S$ và $V \setminus S$ (với $u \in S, v \notin S$).
  3. Kết nạp $v$ vào $S$ và thêm cạnh $(u, v)$ vào cây khung.
  4. Lặp lại đúng $n-1$ lần cho đến khi toàn bộ $n$ đỉnh đều được kết nạp.
- **Độ phức tạp:** $O(V^2)$ với ma trận kề / danh sách kề.

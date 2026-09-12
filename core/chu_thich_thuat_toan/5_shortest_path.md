# 📖 Chú thích Thuật toán: Tìm Đường đi Ngắn nhất (`core/shortest_path.py`)

Module `core/shortest_path.py` cài đặt 2 thuật toán tìm đường đi ngắn nhất kinh điển trong Lý thuyết đồ thị.

---

## 1. Thuật toán Dijkstra

### 1.1. Điều kiện áp dụng & Nguyên lý
- **Điều kiện:** Áp dụng cho đồ thị có trọng số **không âm** ($w \ge 0$).
- **Chiến lược:** Tham lam (Greedy Strategy):
  1. Khởi tạo nhãn khoảng cách: $\text{dist}[\text{start}] = 0$, tất cả các đỉnh khác bằng $+\infty$.
  2. Tại mỗi bước lặp, chọn đỉnh $u^* \notin \text{visited}$ có $\text{dist}[u^*]$ nhỏ nhất. Chốt nhãn này là tối ưu vĩnh viễn (`visited[u*] = True`).
  3. **Nới lỏng cạnh (Relaxation):** Với mỗi đỉnh kề $v$ của $u^*$:
     $$\text{Nếu } \text{dist}[u^*] + w(u^*, v) < \text{dist}[v] \implies \text{dist}[v] = \text{dist}[u^*] + w(u^*, v), \quad \text{parent}[v] = u^*$$
  4. Lặp lại cho đến khi chốt đủ $n$ đỉnh hoặc chốt xong đỉnh đích `end`.

### 1.2. Độ phức tạp tính toán
- Sử dụng ma trận / danh sách kề quét tìm đỉnh nhỏ nhất: $O(V^2)$.
- Sinh bảng vết `trace` chứa trạng thái mảng `dist` tại từng bước lặp phục vụ xuất ma trận bước lặp.

---

## 2. Thuật toán Bellman-Ford

### 2.1. Điều kiện áp dụng & Nguyên lý
- **Điều kiện:** Xử lý được đồ thị có **trọng số âm** ($w < 0$).
- **Nguyên lý Toán học Rời rạc:**
  - Trong đồ thị $n$ đỉnh không có chu trình âm, đường đi đơn ngắn nhất qua tối đa $n-1$ cạnh.
  - Do đó, lặp $n-1$ vòng Relaxation qua **toàn bộ tập cạnh** chắc chắn sẽ tìm được khoảng cách ngắn nhất đến mọi đỉnh.
  - **Tối ưu dừng sớm:** Nếu qua một vòng lặp mà không có cạnh nào được nới lỏng thêm (`changed == False`), thuật toán đã hội tụ sớm và có thể dừng ngay.

### 2.2. Phát hiện Chu trình âm (Vòng lặp thứ $n$)
- Sau $n-1$ vòng Relaxation, thuật toán tiến hành quét lại toàn bộ cạnh ở vòng lặp thứ $n$:
  $$\text{Nếu tồn tại cạnh } (u, v) \text{ thỏa } \text{dist}[u] + w < \text{dist}[v] \implies \text{Đồ thị chứa Chu trình âm!}$$
- Khi phát hiện chu trình âm, hàm trả về cờ `has_negative_cycle = True` và cảnh báo đường đi ngắn nhất không tồn tại vì chi phí có thể giảm vô hạn về $-\infty$.

### 2.3. Độ phức tạp tính toán
- Độ phức tạp thời gian: $O(V \cdot E)$.

# 📋 ĐỀ BÀI ĐỒ ÁN CUỐI KỲ — CẤU TRÚC RỜI RẠC (CTRR FINAL PROJECT)

> **Yêu cầu chung**: Xây dựng và chạy demo ứng dụng có các chức năng chính sau (**không sử dụng thư viện có sẵn trừ phần Trực quan hóa**).

---

## 🟢 PHẦN CƠ BẢN

1. **Input đồ thị. Vẽ & Lưu hình đồ thị**
   - Hỗ trợ nhập đồ thị (từ bàn phím, ma trận, danh sách cạnh hoặc file text).
   - Vẽ hình trực quan và lưu thành file ảnh đồ thị.

2. **Hiển thị các phương pháp biểu diễn đồ thị**
   - Chuyển đổi qua lại 2 chiều giữa 3 dạng:
     $$\text{Adjacency Matrix} \longleftrightarrow \text{Adjacency List} \longleftrightarrow \text{Edge List}$$

3. **Duyệt đồ thị từ 1 node bất kỳ bằng BFS & DFS. So với kết quả chạy tay**
   - Duyệt BFS & DFS, xuất thứ tự duyệt và Cây khung.
   - Xuất Bảng vết từng bước để đối chiếu với cách làm bài thi trên giấy.

4. **Kiểm tra xem đồ thị có là đồ thị hai phía (Bipartite)**
   - Dùng thuật toán tô 2 màu: chia thành 2 tập $V_1, V_2$ (nếu đúng) hoặc chỉ ra Chu trình lẻ (nếu sai).

5. **Tìm đường đi ngắn nhất giữa 2 nodes bất kỳ bằng Dijkstra & Bellman-Ford. So với kết quả chạy tay**
   - *(Chú ý: đồ thị có thể là vô hướng hoặc có hướng)*.
   - Xuất đường đi, chi phí ngắn nhất và Bảng ma trận bước lặp.
   - Bellman-Ford có khả năng phát hiện Chu trình âm.

---

## 🔴 PHẦN NÂNG CAO

7. **Chạy & Trực quan hóa kết quả các thuật toán:**
   - **7.1** Fleury (Tìm chu trình / đường đi Euler)
   - **7.2** Hierholzer (Tìm chu trình / đường đi Euler)
   - **7.3** Prim (Cây khung nhỏ nhất - MST)
   - **7.4** Kruskal (Cây khung nhỏ nhất - MST kết hợp DSU)
   - **7.5** Ford-Fulkerson (Luồng cực đại trong mạng - Max Flow & Min Cut)

8. **Tìm hiểu và áp dụng một bài toán thực tế với một trong các thuật toán đã học:**
   - Mô tả rõ bài toán thực tế đặt ra.
   - Sự liên quan đến thuật toán muốn xét (ví dụ: Node là gì, Edge là gì, Trọng số là gì, Mục tiêu cần tìm là gì...).
   - Chạy kết quả thực tế trên chương trình.

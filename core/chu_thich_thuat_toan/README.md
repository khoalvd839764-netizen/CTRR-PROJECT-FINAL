# 📚 CHÚ THÍCH THUẬT TOÁN - THƯ VIỆN ĐỒ THỊ CTRR

Thư mục này chứa tài liệu giải thích chi tiết nguyên lý toán học, thuật toán, độ phức tạp và hướng dẫn triển khai cho toàn bộ các module trong thư viện `core/`.

## 📌 Danh mục tài liệu:

1. **[1. Cấu trúc Đồ thị & Đồng bộ Biểu diễn (graph.py)](1_graph.md)**
   - Lớp đối tượng `Graph`, cơ chế đồng bộ tự động giữa 3 dạng biểu diễn (Ma trận kề, Danh sách kề, Danh sách cạnh) và bộ phân tích cú pháp chuỗi văn bản.
2. **[2. Chuyển đổi Biểu diễn Đồ thị (converter.py)](2_converter.md)**
   - 6 hàm chuyển đổi hai chiều giữa Ma trận kề, Danh sách kề và Danh sách cạnh, quy tắc bảo toàn tính đối xứng và lọc cạnh vô hướng.
3. **[3. Duyệt Đồ thị BFS & DFS (traversal.py)](3_traversal.md)**
   - Thuật toán BFS (Hàng đợi FIFO) và DFS (Call Stack đệ quy), quy ước sắp xếp đỉnh kề tăng dần để khớp 100% với bài giải tay của sinh viên, sinh cây khung và bảng vết (trace table).
4. **[4. Kiểm tra Đồ thị Hai phía & Trích xuất Chu trình lẻ (bipartite.py)](4_bipartite.md)**
   - Thuật toán tô 2 màu (2-Coloring BFS), xử lý đa thành phần liên thông và kỹ thuật tìm Tổ tiên chung gần nhất (LCA) trích xuất chu trình lẻ.
5. **[5. Tìm Đường đi Ngắn nhất Dijkstra & Bellman-Ford (shortest_path.py)](5_shortest_path.md)**
   - Thuật toán Dijkstra (Tham lam + Nới lỏng cạnh) cho trọng số không âm và Bellman-Ford xử lý trọng số âm, phát hiện chu trình âm qua vòng lặp thứ $n$.
6. **[6. Chu trình & Đường đi Euler (euler.py)](6_euler.md)**
   - Kiểm tra điều kiện Euler có hướng/vô hướng, Thuật toán Fleury (kiểm tra cạnh cầu bằng BFS) và Thuật toán Hierholzer (ghép chu trình con bằng Stack tối ưu $O(E)$).
7. **[7. Cây khung Nhỏ nhất & Cấu trúc DSU (mst.py)](7_mst.md)**
   - Cấu trúc Disjoint Set Union (DSU) với Nén đường đi (Path Compression) và Gộp theo hạng (Union by Rank), Thuật toán Kruskal và Prim (nguyên lý lát cắt).
8. **[8. Luồng Cực đại & Lát cắt Hẹp nhất (max_flow.py)](8_max_flow.md)**
   - Thuật toán Ford-Fulkerson (biến thể Edmonds-Karp BFS), cập nhật đồ thị phần dư (residual graph), tìm nghẽn cổ chai (bottleneck) và xác định lát cắt hẹp nhất Min-Cut $S-T$.

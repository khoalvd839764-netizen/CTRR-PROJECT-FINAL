# BẢNG PHÂN CÔNG & TIẾN ĐỘ THỰC HIỆN DỰ ÁN CTRR

Tài liệu hướng dẫn chi tiết công việc cho từng thành viên trong nhóm 5 người.

---

# 📊 BẢNG TIẾN ĐỘ & PHÂN CÔNG NHIỆM VỤ

| Thành viên | Tên file đảm nhận | Nhiệm vụ chính | Trạng thái |
|:---|:---|:---|:---:|
| **Jackie Khoa (Nhóm trưởng)** | `core/converter.py` & `core/graph.py` | Nền tảng dữ liệu `Graph` & Chuyển đổi 3 dạng | ✅ **ĐÃ XONG 100%** |
| **Nhật Trường** | `visualizer/draw.py` | Vẽ đồ thị & Lưu ảnh PNG bằng matplotlib | ✅ **ĐÃ XONG 100%** |
| **Đỗ Thanh** | `core/traversal.py` | Duyệt BFS, DFS + Bảng vết chạy tay | ✅ **ĐÃ XONG 100%** |
| **Tuấn** | `core/bipartite.py` | Kiểm tra Đồ thị 2 phía & Chu trình lẻ | ⏳ Đang làm |
| **Linh** | `core/shortest_path.py` | Dijkstra & Bellman-Ford + Bảng ma trận | ✅ **ĐÃ XONG 100%** |
| **Cả nhóm (Ngày 2)** | `run_demo.py` | Ghép nối và chạy Demo tổng hợp | ⏸️ Chờ Tuấn xong |

---

# 👤 1. NHẬT TRƯỜNG — VẼ VÀ LƯU ẢNH ĐỒ THỊ

> **File đã hoàn thành**: `visualizer/draw.py` (✅ **Xong 100%**)

---

# 👤 2. ĐỖ THANH — THUẬT TOÁN DUYỆT BFS & DFS

> **File đã hoàn thành**: `core/traversal.py` (✅ **Xong 100%**)

---

# 👤 3. TUẤN — KIỂM TRA ĐỒ THỊ HAI PHÍA (BIPARTITE)

> **File cần mở**: `core/bipartite.py`  
> **Dữ liệu nhận vào từ Graph**: `g.adj` (danh sách kề), `g.n` (số đỉnh).

### 🎯 Hướng dẫn tư duy và thực hiện:

#### Hàm `check_bipartite(adj, n)`
1. Tạo mảng màu `color = [0] * n` (`0`: chưa tô, `1`: màu Đỏ, `-1`: màu Xanh) và `parent = [-1] * n`.
2. Lặp qua tất cả các đỉnh `for i in range(n):` (xử lý cả đồ thị không liên thông):
   * Nếu `color[i] == 0`:
     * Gán `color[i] = 1`, `queue = [i]`.
     * Vòng lặp BFS `while queue:`
       * `u = queue.pop(0)`.
       * Với mỗi đỉnh $v$ kề $u$ (`for v, w in adj.get(u, []):`):
         * **Nếu `color[v] == 0` (chưa tô)**: gán màu ngược lại `color[v] = -color[u]`, `parent[v] = u`, `queue.append(v)`.
         * **Nếu `color[v] == color[u]` (XUNG ĐỘT MÀU!)**:
           * Đồ thị KHÔNG là 2 phía.
           * Lần ngược `parent` từ $u$ và $v$ về gốc chung để trích xuất danh sách đỉnh của **Chu trình lẻ**.
           * `return {"is_bipartite": False, "odd_cycle": [danh_sách_đỉnh]}`.
3. Nếu tô xong toàn bộ mà không xung đột:
   * Tập 1 (Đỏ): `v1 = [i for i in range(n) if color[i] == 1]`.
   * Tập 2 (Xanh): `v2 = [i for i in range(n) if color[i] == -1]`.
   * `return {"is_bipartite": True, "v1": v1, "v2": v2, "colors": {i: ('red' if color[i]==1 else 'blue') for i in range(n)}}`.

### 🧪 Lệnh test nhanh cho Tuấn:
Mở Terminal gõ:
```bash
python3 tests/test_bipartite.py
```

---

# 👤 4. LINH — ĐƯỜNG ĐI NGẮN NHẤT (DIJKSTRA & BELLMAN-FORD)

> **File đã hoàn thành**: `core/shortest_path.py` (✅ **Xong 100%**)

---

# 🚀 5. BƯỚC GHÉP NỐI TOÀN BỘ (NGÀY 2) — `run_demo.py`

Khi Tuấn hoàn thành, Nhóm trưởng sẽ mở file `run_demo.py` và chạy lệnh tổng hợp:
```bash
python3 run_demo.py
```

# 📖 Chú thích Thuật toán: Chu trình & Đường đi Euler (`core/euler.py`)

## 1. Định lý Euler trong Lý thuyết đồ thị

### 1.1. Đồ thị vô hướng liên thông
- **Chu trình Euler:** Đi qua mỗi cạnh đúng 1 lần và quay về đỉnh xuất phát. Tồn tại $\iff$ **tất cả các đỉnh đều có bậc chẵn** ($\text{deg}(v) \pmod 2 = 0$).
- **Đường đi Euler:** Đi qua mỗi cạnh đúng 1 lần, xuất phát tại đỉnh này và kết thúc tại đỉnh khác. Tồn tại $\iff$ **có đúng 2 đỉnh bậc lẻ** (xuất phát từ 1 đỉnh lẻ và kết thúc ở đỉnh lẻ còn lại).

### 1.2. Đồ thị có hướng liên thông yếu
- **Chu trình Euler:** Tồn tại $\iff$ bán bậc vào bằng bán bậc ra tại mọi đỉnh ($\text{in\_deg}(v) = \text{out\_deg}(v), \forall v$).
- **Đường đi Euler:** Tồn tại $\iff$ có đúng 1 đỉnh có $\text{out} = \text{in} + 1$ (đỉnh bắt đầu), đúng 1 đỉnh có $\text{in} = \text{out} + 1$ (đỉnh kết thúc), và mọi đỉnh khác có $\text{in} = \text{out}$.

---

## 2. Kiểm tra Cạnh Cầu (`is_bridge`)
- **Định nghĩa:** Cạnh $(u, v)$ là Cầu (Bridge) nếu việc xóa nó làm tăng số thành phần liên thông của đồ thị.
- **Thuật toán:**
  1. Dùng BFS đếm số đỉnh tới được từ $u$ trước khi xóa cạnh: `count_before`.
  2. Tạm thời xóa cạnh $(u, v)$ khỏi danh sách kề.
  3. Dùng BFS đếm lại số đỉnh tới được từ $u$: `count_after`.
  4. Khôi phục lại cạnh. Nếu `count_after < count_before` $\implies$ Cạnh là CẦU.

---

## 3. Thuật toán Fleury
- **Triết lý:** *"Không bao giờ đi qua cạnh cầu trừ khi không còn lựa chọn nào khác!"*
- **Các bước thực hiện:**
  1. Xuất phát từ đỉnh bậc lẻ (nếu tìm đường đi) hoặc đỉnh bất kỳ (nếu tìm chu trình).
  2. Tại đỉnh hiện tại:
     - Nếu chỉ có 1 cạnh kề: bắt buộc đi qua cạnh đó.
     - Nếu có nhiều cạnh: kiểm tra và ưu tiên chọn cạnh **không phải là cầu**.
  3. Đi qua cạnh và xóa cạnh vừa duyệt khỏi đồ thị.
- **Độ phức tạp:** $O(E^2)$ do mỗi lần chọn cạnh cần chạy BFS để kiểm tra cầu.

---

## 4. Thuật toán Hierholzer
- **Triết lý:** Ghép các chu trình con lại với nhau bằng cấu trúc **Ngăn xếp (Stack)**.
- **Các bước thực hiện:**
  1. Bắt đầu với đỉnh nguồn trong Stack `curr_path = [start]`.
  2. Tại đỉnh $u = \text{curr\_path}[-1]$:
     - Nếu $u$ còn cạnh kề $(u, v)$: xóa cạnh $(u, v)$ khỏi đồ thị và đẩy $v$ vào Stack (`curr_path.append(v)`).
     - Nếu $u$ hết cạnh kề (chạm ngõ cụt của một chu trình con): pop $u$ ra khỏi Stack và kết nạp vào kết quả `circuit.append(u)`.
  3. Lặp lại cho tới khi Stack rỗng.
  4. **Đảo ngược danh sách `circuit`** để thu được chu trình/đường đi Euler hoàn chỉnh.
- **Độ phức tạp tối ưu:** $O(E)$ — Nhanh hơn vượt trội so với Fleury.

# 🐙 HƯỚNG DẪN GIT WORKFLOW CHO NHÓM (CTRR PROJECT)

Tài liệu hướng dẫn quy trình làm việc nhóm bằng Git: **Clone repo -> Tạo nhánh riêng -> Code & Test -> Push lên GitHub -> Tạo Pull Request (PR) -> Nhóm trưởng duyệt merge**.

---

## 📌 QUY TRÌNH TỔNG QUAN

```
1. Clone repo về máy
      │
      ▼
2. Tạo nhánh riêng: git checkout -b feature/<tên-bạn>
      │
      ▼
3. Code và chạy test: python3 tests/test_xxx.py
      │
      ▼
4. Commit và Push: git push origin feature/<tên-bạn>
      │
      ▼
5. Tạo Pull Request (PR) trên GitHub
      │
      ▼
6. Nhóm trưởng (Jackie Khoa) duyệt (Approve) & Merge vào Main
```

---

## 🚀 DÀNH CHO 4 THÀNH VIÊN (Nhật Trường, Đỗ Thanh, Tuấn, Linh)

### 🔹 Bước 1: Clone Repository về máy tính
Mở Terminal / Git Bash và gõ:
```bash
git clone https://github.com/khoalvd839764-netizen/CTRR-PROJECT-FINAL.git
cd CTRR-PROJECT-FINAL
```

---

### 🔹 Bước 2: Tạo nhánh riêng theo tên của mình
⚠️ **QUY TẮC BẮT BUỘC**: Không được code trực tiếp trên nhánh `main`. Nhánh `main` đã bật chế độ bảo vệ (Branch Protection), bạn phải làm trên nhánh riêng của mình.

Mỗi bạn gõ lệnh tạo nhánh tương ứng:

* **Nhật Trường**:
  ```bash
  git checkout -b feature/draw-nhattruong
  ```
* **Đỗ Thanh**:
  ```bash
  git checkout -b feature/traversal-dothanh
  ```
* **Tuấn**:
  ```bash
  git checkout -b feature/bipartite-tuan
  ```
* **Linh**:
  ```bash
  git checkout -b feature/shortest-path-linh
  ```

*(Để kiểm tra xem mình đang ở nhánh nào, gõ lệnh `git branch`)*

---

### 🔹 Bước 3: Code và Chạy test trên máy của bạn
Mở file của bạn ra code theo hướng dẫn trong `worktoday.md`, sau đó chạy file test tự động để đảm bảo code hoạt động chính xác:

* **Nhật Trường**: `python3 tests/test_draw.py`
* **Đỗ Thanh**: `python3 tests/test_traversal.py`
* **Tuấn**: `python3 tests/test_bipartite.py`
* **Linh**: `python3 tests/test_shortest_path.py`

---

### 🔹 Bước 4: Lưu (Commit) và Đẩy (Push) code lên GitHub
Khi chạy test thấy tất cả đều đạt kết quả tốt, bạn gõ 3 lệnh sau:

```bash
# 1. Thêm tất cả file đã sửa vào vùng chuẩn bị
git add .

# 2. Tạo commit ghi rõ nội dung bạn vừa làm
git commit -m "feat: hoàn thành module của [Tên_Bạn]"

# 3. Đẩy nhánh của bạn lên GitHub
git push origin <tên-nhánh-của-bạn>
```

*Ví dụ Đỗ Thanh sẽ gõ*:
```bash
git push origin feature/traversal-dothanh
```

---

### 🔹 Bước 5: Tạo Pull Request (PR) chờ duyệt
1. Truy cập vào link repository của nhóm trên trình duyệt:  
   👉 `https://github.com/khoalvd839764-netizen/CTRR-PROJECT-FINAL`
2. Bạn sẽ thấy một thanh thông báo màu vàng/xanh hiện lên: **"Compare & pull request"** $\to$ Bấm vào nút đó.
3. Điền thông tin PR:
   * **Title**: `[Feature] Hoàn thành module <Tên_Module> - <Tên_Bạn>`
   * **Description**: Mô tả ngắn gọn các hàm bạn đã viết và kết quả chạy test.
4. Bấm nút xanh **"Create pull request"**.
5. Nhắn tin vào group chat nhóm: *"Khoa ơi mình tạo PR rồi, bạn vào check và merge giúp mình nhé!"*

---

## 👑 DÀNH CHO NHÓM TRƯỞNG (Jackie Khoa) — REVIEW VÀ MERGE PR

1. Mở repository trên GitHub, vào tab **Pull requests**.
2. Nhấp vào Pull Request của thành viên vừa gửi:
   * Chuyển sang tab **Files changed** để xem những dòng code mà bạn đó đã thêm/sửa.
3. Nếu code chuẩn xác và không có xung đột:
   * Bấm nút **"Review changes"** ở góc phải $\to$ Chọn **"Approve"** $\to$ Bấm **"Submit review"**.
   * Bấm nút **"Merge pull request"** $\to$ Chọn **"Confirm merge"**.
4. Lúc này code của thành viên đã được tích hợp an toàn vào nhánh `main`.

---

## 🔄 CẬP NHẬT CODE MỚI NHẤT TỪ MAIN VỀ MÁY CỦA BẠN (KHI CÓ NGƯỜI VỪA MERGE)

Mỗi khi có một thành viên khác vừa được merge code vào `main`, các bạn khác nên cập nhật code mới nhất về máy mình bằng cách gõ:

```bash
git checkout main
git pull origin main
git checkout <tên-nhánh-của-bạn>
git merge main
```

# -*- coding: utf-8 -*-
"""
Điểm khởi chạy trung tâm duy nhất (Single Main Entry Point) cho Đồ án CTRR Final Project:
  - Trường Đại học Giao thông vận tải TP.HCM (UTH)
  - Giảng viên hướng dẫn: Thầy Tăng Lê Ngọc Gia Huy

Cách sử dụng:
  1. Khởi động Menu Console 10 Chức năng Thuật toán chuẩn CTRR:
     python main.py
  2. Khởi động trực tiếp Sa bàn Giao thông Đô thị Thông minh & Cứu hộ Khẩn cấp (Pygame GUI):
     python main.py --gui
     (hoặc: python main.py --traffic / -t / -g)
"""
import sys

def main():
    # Kiểm tra tham số dòng lệnh để phân nhánh thực thi
    if len(sys.argv) > 1 and sys.argv[1].lower() in ["--traffic", "-t", "--gui", "-g", "--robot", "-r"]:
        # Chế độ Sa bàn Giao diện Đồ họa Trực quan (Pygame)
        from ung_dung_thuc_te.main import run as run_traffic_gui
        run_traffic_gui()
    else:
        # Chế độ Menu Dòng lệnh Tương tác 10 Chức năng cốt lõi
        from app.cli import App
        app = App()
        app.run()

if __name__ == "__main__":
    main()

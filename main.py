# -*- coding: utf-8 -*-
"""
Điểm khởi chạy chính (Main Entry Point) cho toàn bộ Đồ án CTRR.
Tự động kích hoạt môi trường venv nếu thiếu thư viện pygame / matplotlib.
"""
import sys
import os

try:
    import pygame
    import matplotlib
except ImportError:
    venv_python = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv", "bin", "python3")
    if os.path.exists(venv_python) and os.path.abspath(sys.executable) != os.path.abspath(venv_python):
        os.execl(venv_python, venv_python, *sys.argv)

from app.cli import App
from ung_dung_thuc_te.main import run as run_robot_sim

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["--robot", "-r", "--gui", "-g"]:
            print("🤖 Đang khởi động Ứng Dụng Thực Tế: Robot Hút Bụi Thông Minh...")
            run_robot_sim()
            return
        elif arg in ["--help", "-h"]:
            print("🎓 HƯỚNG DẪN KHỞI CHẠY ĐỒ ÁN CTRR:")
            print("  python3 main.py           : Mở Menu tương tác CLI tổng hợp (10 chức năng)")
            print("  python3 main.py --robot   : Mở trực tiếp Giao diện 3D Robot Hút Bụi (Khuyên dùng khi demo)")
            print("  python3 run_demo.py       : Mở Menu tương tác CLI tổng hợp")
            print("  python3 run_robot_sim.py  : Mở trực tiếp Giao diện 3D Robot Hút Bụi")
            return

    app = App()
    app.run()

if __name__ == "__main__":
    main()

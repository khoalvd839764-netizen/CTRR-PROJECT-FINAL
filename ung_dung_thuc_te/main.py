"""
Module: ung_dung_thuc_te/main.py
Mục đích: Điểm khởi chạy (Entry Point) trực tiếp cho Module Ứng Dụng Thực Tế.
"""
import sys
from ung_dung_thuc_te.gui_dashboard import SmartRobotSimulationApp

def run():
    """Khởi tạo và chạy ứng dụng mô phỏng Robot Hút Bụi."""
    app = SmartRobotSimulationApp()
    app.run()

if __name__ == "__main__":
    run()

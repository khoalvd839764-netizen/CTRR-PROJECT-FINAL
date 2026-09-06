# -*- coding: utf-8 -*-
"""
Module: ung_dung_thuc_te/traffic_dashboard.py
Wrapper kết nối tương thích cho giao diện sa bàn giao thông và script khởi chạy.
"""
from ung_dung_thuc_te.main import run


class TrafficSimulationApp:
    """Lớp bọc ứng dụng mô phỏng sa bàn."""
    def __init__(self):
        pass

    def run(self):
        run()


def launch_traffic_dashboard():
    """Hàm khởi chạy nhanh sa bàn giao thông."""
    run()


if __name__ == "__main__":
    launch_traffic_dashboard()

# -*- coding: utf-8 -*-
"""
Module: app/robot_sim.py
Mục đích: Module chuyển tiếp (Forwarding Wrapper) gọi trực tiếp sang package ung_dung_thuc_te.
Đảm bảo tính tương thích ngược cho các script khởi chạy cũ.
"""
from ung_dung_thuc_te.traffic_dashboard import TrafficSimulationApp, launch_traffic_dashboard
from ung_dung_thuc_te.main import run

def launch_robot_simulation():
    """Khởi chạy ứng dụng mô phỏng Giao Thông Đô Thị Thông Minh (CTRR)."""
    run()

if __name__ == "__main__":
    launch_robot_simulation()


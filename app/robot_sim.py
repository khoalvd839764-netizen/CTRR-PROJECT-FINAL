# -*- coding: utf-8 -*-
"""
Module: app/robot_sim.py
Mục đích: Module chuyển tiếp (Forwarding Wrapper) gọi trực tiếp sang package ung_dung_thuc_te.
Đảm bảo tính tương thích ngược và cấu trúc thư mục sạch đẹp.
"""
from ung_dung_thuc_te.data_model import (
    HOUSE_NODES_DATA, HOUSE_BASE_COORDS, HOUSE_EDGES,
    EDGE_CURVATURE, ROOMS_LAYOUT_3D, FURNITURE_3D_BLOCKS
)
from ung_dung_thuc_te.algorithms import RobotAlgorithms
from ung_dung_thuc_te.gui_dashboard import (
    SmartRobotSimulationApp,
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    COL_Y, COL_HEIGHT, COL1_X, COL1_WIDTH, COL2_X, COL2_WIDTH, COL3_X, COL3_WIDTH,
    COLOR_APP_BG, COLOR_CARD_BG, COLOR_CARD_BORDER, COLOR_CARD_BORDER_GLOW,
    COLOR_TEXT_WHITE, COLOR_TEXT_CYAN, COLOR_TEXT_GOLD, COLOR_TEXT_GREEN,
    COLOR_TEXT_RED, COLOR_TEXT_MUTED, get_vietnamese_font
)

def launch_robot_simulation():
    """Khởi chạy ứng dụng mô phỏng Robot Hút Bụi."""
    app = SmartRobotSimulationApp()
    app.run()

if __name__ == "__main__":
    launch_robot_simulation()

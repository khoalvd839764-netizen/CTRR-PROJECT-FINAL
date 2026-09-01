# -*- coding: utf-8 -*-
"""
File khởi chạy tương thích: Giao diện 3D Robot Hút Bụi Thông Minh.
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

from ung_dung_thuc_te.main import run

if __name__ == "__main__":
    run()

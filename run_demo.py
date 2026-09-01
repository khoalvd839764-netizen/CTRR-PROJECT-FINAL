# -*- coding: utf-8 -*-
"""
File khởi chạy tương thích: Menu CLI Tổng Hợp Đồ Án CTRR.
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

from main import main

if __name__ == "__main__":
    main()

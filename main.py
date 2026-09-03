# -*- coding: utf-8 -*-
"""
Main Entry Point for CTRR Final Project
Supports:
  - python3 main.py         : Launches interactive 10-function CLI Menu
  - python3 main.py --robot : Directly launches 3D Smart Vacuum Robot Simulation GUI
"""
import sys
import os

def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() in ["--robot", "-r", "--gui", "-g"]:
        from ung_dung_thuc_te.main import run as run_robot_gui
        run_robot_gui()
    else:
        from app.cli import App
        app = App()
        app.run()

if __name__ == "__main__":
    main()

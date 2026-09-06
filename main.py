# -*- coding: utf-8 -*-
"""
Main Entry Point for CTRR Final Project
Supports:
  - python3 main.py           : Launches interactive 10-function CLI Menu
  - python3 main.py --traffic : Directly launches Smart Urban Traffic Grid Simulation GUI
  - python3 main.py --gui     : Directly launches Smart Urban Traffic Grid Simulation GUI
"""
import sys
import os

def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() in ["--traffic", "-t", "--gui", "-g", "--robot", "-r"]:
        from ung_dung_thuc_te.main import run as run_traffic_gui
        run_traffic_gui()
    else:
        from app.cli import App
        app = App()
        app.run()

if __name__ == "__main__":
    main()


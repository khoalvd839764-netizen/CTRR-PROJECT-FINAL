"""
Module: ung_dung_thuc_te/main.py
Purpose: Direct entry point for the Smart Vacuum Robot Simulation Application.
"""
import sys
from ung_dung_thuc_te.gui_dashboard import SmartRobotSimulationApp

def run():
    """Initializes and runs the Smart Vacuum Robot simulation dashboard."""
    app = SmartRobotSimulationApp()
    app.run()

if __name__ == "__main__":
    run()

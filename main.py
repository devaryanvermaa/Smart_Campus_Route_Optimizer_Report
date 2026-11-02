"""
Smart Campus Shortest Route Finder
Entry Point: main.py
Author: Aryan (MCA DAA Practical Project)
Description:
    Launches the clean, user-friendly desktop application for finding
    the shortest path between campus buildings using Dijkstra's Algorithm.
"""

import sys
import tkinter as tk
from gui import CampusRouteGUI


def main():
    """Application entry point."""
    root = tk.Tk()
    app = CampusRouteGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

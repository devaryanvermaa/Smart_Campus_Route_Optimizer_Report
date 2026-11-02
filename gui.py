"""
Campus Route Optimizer
Module: gui.py
Purpose:
    Clean, user-friendly desktop GUI built with Tkinter.
    Features:
    - Interactive Campus Map with nodes (buildings) and road distances.
    - Source and Destination dropdown selector.
    - One-click Dijkstra shortest route calculation.
    - Real-time path visualization highlighting on Canvas.
    - Step-by-step distance breakdown and DAA viva facts.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from graph import create_campus_graph
from dijkstra import dijkstra_shortest_path


class CampusRouteGUI:
    """Clean and user-friendly GUI for Campus Shortest Path calculation."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Smart Campus Shortest Route Finder | DAA Practical Project")
        self.root.geometry("1060x650")
        self.root.minsize(980, 600)
        self.root.configure(bg="#F4F6F9")

        # Load Graph
        self.graph = create_campus_graph()
        self.locations = self.graph.get_locations()

        # Route State
        self.highlighted_path = []
        self.highlighted_dist = 0.0

        # Styles
        self._setup_styles()

        # Build UI Structure
        self._build_header()
        self._build_main_layout()
        self._build_status_bar()

        # Initial Draw
        self._draw_campus_map()

    def _setup_styles(self):
        """Configure clean font and widget styling."""
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure(".", font=("Segoe UI", 9))
        self.style.configure("Header.TLabel", font=("Segoe UI", 15, "bold"), background="#1E293B", foreground="#F8FAFC")
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 9), background="#1E293B", foreground="#94A3B8")
        self.style.configure("CardTitle.TLabel", font=("Segoe UI", 10, "bold"), foreground="#0F172A")
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=6)

    def _build_header(self):
        """Top banner."""
        banner = tk.Frame(self.root, bg="#1E293B", height=60)
        banner.pack(side=tk.TOP, fill=tk.X)

        title = ttk.Label(banner, text="📍 SMART CAMPUS ROUTE FINDER", style="Header.TLabel")
        title.pack(anchor="w", padx=20, pady=(8, 0))

        sub = ttk.Label(
            banner,
            text="Shortest Path Optimization using Dijkstra's Algorithm | DAA Practical Examination",
            style="SubHeader.TLabel"
        )
        sub.pack(anchor="w", padx=20, pady=(0, 8))

    def _build_status_bar(self):
        """Bottom status bar."""
        self.status_var = tk.StringVar(value="Ready. Select Source and Destination, then click 'Find Shortest Route'.")
        status_bar = tk.Frame(self.root, bg="#E2E8F0", height=24)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        lbl = tk.Label(status_bar, textvariable=self.status_var, font=("Segoe UI", 8), bg="#E2E8F0", fg="#334155")
        lbl.pack(side=tk.LEFT, padx=12, pady=3)

        info = tk.Label(status_bar, text="MCA DAA Project | Dijkstra SSSP Algorithm", font=("Segoe UI", 8, "italic"), bg="#E2E8F0", fg="#64748B")
        info.pack(side=tk.RIGHT, padx=12, pady=3)

    def _build_main_layout(self):
        """Splits the window into Left Controls and Right Canvas Map."""
        main_frame = tk.Frame(self.root, bg="#F4F6F9")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        # 1. Left Control Panel (width ~340px)
        left_panel = tk.Frame(main_frame, bg="#F4F6F9", width=340)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)

        # --- Card 1: Selection Controls ---
        card1 = tk.Frame(left_panel, bg="white", relief=tk.RIDGE, bd=1, padx=14, pady=12)
        card1.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(card1, text="1. Select Route Endpoints", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))

        # Source Dropdown
        tk.Label(card1, text="Starting Location (Source):", font=("Segoe UI", 9, "bold"), bg="white", fg="#475569").pack(anchor="w")
        self.combo_source = ttk.Combobox(card1, values=self.locations, state="readonly", font=("Segoe UI", 9))
        self.combo_source.set(self.locations[0] if self.locations else "")
        self.combo_source.pack(fill=tk.X, pady=(2, 8))

        # Destination Dropdown
        tk.Label(card1, text="Target Location (Destination):", font=("Segoe UI", 9, "bold"), bg="white", fg="#475569").pack(anchor="w")
        self.combo_dest = ttk.Combobox(card1, values=self.locations, state="readonly", font=("Segoe UI", 9))
        # Default destination to Computer Lab or second node
        default_dest = "Computer Lab" if "Computer Lab" in self.locations else (self.locations[1] if len(self.locations) > 1 else "")
        self.combo_dest.set(default_dest)
        self.combo_dest.pack(fill=tk.X, pady=(2, 10))

        # Action Buttons
        btn_frame = tk.Frame(card1, bg="white")
        btn_frame.pack(fill=tk.X)

        btn_find = tk.Button(
            btn_frame,
            text="⚡ Find Shortest Route",
            command=self._calculate_route,
            font=("Segoe UI", 9, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=6,
            cursor="hand2"
        )
        btn_find.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        btn_reset = tk.Button(
            btn_frame,
            text="🔄 Reset",
            command=self._reset_route,
            font=("Segoe UI", 9),
            bg="#E2E8F0",
            fg="#1E293B",
            relief=tk.FLAT,
            padx=8,
            pady=6,
            cursor="hand2"
        )
        btn_reset.pack(side=tk.RIGHT)

        # --- Card 2: Calculation Results ---
        self.card2 = tk.Frame(left_panel, bg="white", relief=tk.RIDGE, bd=1, padx=14, pady=12)
        self.card2.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        ttk.Label(self.card2, text="2. Shortest Route Result", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 6))

        # Total distance badge
        self.lbl_distance_val = tk.Label(
            self.card2,
            text="-- meters",
            font=("Segoe UI", 16, "bold"),
            bg="#EFF6FF",
            fg="#2563EB",
            padx=10,
            pady=6
        )
        self.lbl_distance_val.pack(fill=tk.X, pady=(0, 6))

        # Path sequence string
        self.lbl_path_str = tk.Label(
            self.card2,
            text="Select locations and press 'Find Shortest Route'.",
            font=("Segoe UI", 9),
            bg="white",
            fg="#475569",
            wraplength=300,
            justify=tk.LEFT
        )
        self.lbl_path_str.pack(anchor="w", pady=(0, 8))

        # Segment breakdown list
        tk.Label(self.card2, text="Step-by-Step Segments:", font=("Segoe UI", 8, "bold"), bg="white", fg="#64748B").pack(anchor="w")
        self.segment_listbox = tk.Listbox(
            self.card2,
            font=("Segoe UI", 8),
            height=5,
            bg="#F8FAFC",
            fg="#1E293B",
            relief=tk.SOLID,
            bd=1,
            highlightthickness=0
        )
        self.segment_listbox.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        # --- Card 3: Quick Viva Facts for Teacher ---
        card3 = tk.Frame(left_panel, bg="#FEF3C7", relief=tk.RIDGE, bd=1, padx=12, pady=8)
        card3.pack(fill=tk.X)

        tk.Label(card3, text="💡 Quick DAA Viva Facts:", font=("Segoe UI", 8, "bold"), bg="#FEF3C7", fg="#92400E").pack(anchor="w")
        facts = (
            "• Algorithm: Dijkstra's SSSP\n"
            "• Paradigm: Greedy Strategy\n"
            "• Data Structure: Min-Heap (heapq)\n"
            "• Time Complexity: O((V + E) log V)\n"
            "• Space Complexity: O(V + E)\n"
            "• Graph: 8 Locations, 14 Roads"
        )
        tk.Label(card3, text=facts, font=("Segoe UI", 8), bg="#FEF3C7", fg="#78350F", justify=tk.LEFT).pack(anchor="w")

        # 2. Right Canvas Map (Interactive Visualizer)
        right_panel = tk.Frame(main_frame, bg="white", relief=tk.RIDGE, bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Map Title Bar
        map_bar = tk.Frame(right_panel, bg="#F1F5F9", padx=12, pady=6)
        map_bar.pack(side=tk.TOP, fill=tk.X)

        tk.Label(map_bar, text="🗺️ Interactive Campus Map", font=("Segoe UI", 10, "bold"), bg="#F1F5F9", fg="#1E293B").pack(side=tk.LEFT)
        tk.Label(map_bar, text="Click on any building to quickly set Source/Destination", font=("Segoe UI", 8, "italic"), bg="#F1F5F9", fg="#64748B").pack(side=tk.RIGHT)

        # Canvas widget
        self.canvas = tk.Canvas(right_panel, bg="#FAFAFA", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self._on_canvas_click)

    # =========================================================
    # ROUTE CALCULATION & CANVAS RENDERING
    # =========================================================

    def _calculate_route(self):
        """Runs Dijkstra algorithm and updates results and map."""
        src = self.combo_source.get().strip()
        dest = self.combo_dest.get().strip()

        if not src or not dest:
            messagebox.showwarning("Incomplete Selection", "Please select both a Starting Location and a Destination.")
            return

        # Execute Dijkstra's algorithm from scratch
        distance, path = dijkstra_shortest_path(self.graph, src, dest)

        self.highlighted_path = path
        self.highlighted_dist = distance

        # Update Result Box
        self.segment_listbox.delete(0, tk.END)

        if distance == float('inf'):
            self.lbl_distance_val.config(text="Unreachable", fg="#DC2626", bg="#FEF2F2")
            self.lbl_path_str.config(text=f"No connected path exists between {src} and {dest}.")
            self.status_var.set(f"No route found between {src} and {dest}.")
        elif src == dest:
            self.lbl_distance_val.config(text="0.0 meters", fg="#059669", bg="#ECFDF5")
            self.lbl_path_str.config(text="Source is identical to Destination (You are already here).")
            self.segment_listbox.insert(tk.END, f"Start & End: {src}")
            self.status_var.set("Source equals destination (Distance: 0m).")
        else:
            self.lbl_distance_val.config(text=f"{distance:.1f} meters", fg="#16A34A", bg="#F0FDF4")
            path_display = " ➔ ".join(path)
            self.lbl_path_str.config(text=f"Shortest Path:\n{path_display}")

            # Fill step-by-step segment listbox
            cum_dist = 0.0
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                w = self.graph.adj[u][v]
                cum_dist += w
                self.segment_listbox.insert(
                    tk.END,
                    f"Step {i + 1}: {u} ➔ {v} ({w:.0f}m) [Total: {cum_dist:.0f}m]"
                )

            self.status_var.set(f"Shortest route found: {distance:.1f}m ({len(path) - 1} road segments).")

        # Redraw map with path highlighted
        self._draw_campus_map()

    def _reset_route(self):
        """Clears highlighted path and resets output labels."""
        self.highlighted_path = []
        self.highlighted_dist = 0.0
        self.lbl_distance_val.config(text="-- meters", fg="#2563EB", bg="#EFF6FF")
        self.lbl_path_str.config(text="Select locations and press 'Find Shortest Route'.")
        self.segment_listbox.delete(0, tk.END)
        self.status_var.set("Route cleared. Ready.")
        self._draw_campus_map()

    def _draw_campus_map(self):
        """Draws all roads, distance labels, and campus buildings on Canvas."""
        self.canvas.delete("all")

        # Set of edges on the highlighted shortest path
        hl_edges = set()
        if len(self.highlighted_path) > 1:
            for i in range(len(self.highlighted_path) - 1):
                u = self.highlighted_path[i]
                v = self.highlighted_path[i + 1]
                hl_edges.add(tuple(sorted([u, v])))

        # 1. Draw Normal (Unselected) Roads
        for u, v, dist in self.graph.get_all_roads():
            if tuple(sorted([u, v])) in hl_edges:
                continue
            x1, y1 = self.graph.positions[u]
            x2, y2 = self.graph.positions[v]

            # Gray road line
            self.canvas.create_line(x1, y1, x2, y2, fill="#CBD5E1", width=2)

            # Distance badge at midpoint
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_rectangle(mx - 16, my - 8, mx + 16, my + 8, fill="#FFFFFF", outline="#E2E8F0")
            self.canvas.create_text(mx, my, text=f"{int(dist)}m", font=("Segoe UI", 7), fill="#64748B")

        # 2. Draw Highlighted Shortest Route Roads (Thick Vibrant Line)
        for u, v, dist in self.graph.get_all_roads():
            if tuple(sorted([u, v])) in hl_edges:
                x1, y1 = self.graph.positions[u]
                x2, y2 = self.graph.positions[v]

                # Highlight line in vibrant emerald / orange
                self.canvas.create_line(x1, y1, x2, y2, fill="#EA580C", width=5)

                # Distance badge
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                self.canvas.create_rectangle(mx - 18, my - 9, mx + 18, my + 9, fill="#FFF7ED", outline="#EA580C", width=1.5)
                self.canvas.create_text(mx, my, text=f"{int(dist)}m", font=("Segoe UI", 8, "bold"), fill="#C2410C")

        # 3. Draw Campus Buildings (Nodes)
        path_nodes = set(self.highlighted_path)
        for name, (x, y) in self.graph.positions.items():
            is_on_path = name in path_nodes
            is_source = (self.highlighted_path and name == self.highlighted_path[0])
            is_dest = (self.highlighted_path and name == self.highlighted_path[-1])

            # Dimensions
            radius = 16 if is_on_path else 12

            # Color Schemes
            if is_source:
                fill_color = "#16A34A"  # Green for Source
                outline_color = "#15803D"
                border_width = 3
            elif is_dest:
                fill_color = "#DC2626"  # Red for Destination
                outline_color = "#B91C1C"
                border_width = 3
            elif is_on_path:
                fill_color = "#EA580C"  # Orange for Intermediate route nodes
                outline_color = "#C2410C"
                border_width = 3
            else:
                fill_color = "#1E293B"  # Navy Slate for normal nodes
                outline_color = "#0F172A"
                border_width = 2

            # Draw outer ring for endpoints
            if is_source or is_dest:
                self.canvas.create_oval(x - radius - 5, y - radius - 5, x + radius + 5, y + radius + 5, outline=fill_color, width=2)

            # Draw main node circle
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=fill_color, outline=outline_color, width=border_width)

            # Node label text
            text_color = "#0F172A" if not is_on_path else ("#15803D" if is_source else ("#B91C1C" if is_dest else "#C2410C"))
            font_weight = "bold" if is_on_path else "normal"
            self.canvas.create_text(x, y + radius + 11, text=name, font=("Segoe UI", 8, font_weight), fill=text_color)

    def _on_canvas_click(self, event):
        """Allows user to click a building on the map to set Source or Destination."""
        click_x, click_y = event.x, event.y
        closest_node = None
        min_d = 25  # Click threshold radius

        for name, (x, y) in self.graph.positions.items():
            dist = ((click_x - x) ** 2 + (click_y - y) ** 2) ** 0.5
            if dist < min_d:
                min_d = dist
                closest_node = name

        if closest_node:
            current_src = self.combo_source.get()
            if not current_src or current_src == closest_node:
                self.combo_dest.set(closest_node)
            else:
                # If clicking a new node, set as destination
                self.combo_dest.set(closest_node)
            self.status_var.set(f"Selected '{closest_node}' via map click.")
            self._calculate_route()

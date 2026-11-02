"""
Script to generate high-resolution application screenshots and diagrams
for the MCA DAA Project Report.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "report_images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. Generate Campus Map Diagram (Figure 7.1 / Map View)
# -------------------------------------------------------------
def generate_campus_map():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=200)
    ax.set_facecolor("#F8FAFC")
    fig.patch.set_facecolor("#F8FAFC")

    # Campus Nodes coordinates
    nodes = {
        "Main Gate": (80, 250),
        "Parking Lot": (200, 380),
        "Sports Ground": (200, 120),
        "Library": (380, 380),
        "Academic Block": (380, 250),
        "Cafeteria": (380, 120),
        "Computer Lab": (560, 320),
        "Auditorium": (560, 180),
    }

    roads = [
        ("Main Gate", "Parking Lot", 150),
        ("Main Gate", "Sports Ground", 180),
        ("Main Gate", "Academic Block", 320),
        ("Parking Lot", "Library", 160),
        ("Parking Lot", "Academic Block", 210),
        ("Sports Ground", "Cafeteria", 190),
        ("Sports Ground", "Academic Block", 230),
        ("Library", "Computer Lab", 190),
        ("Library", "Academic Block", 140),
        ("Academic Block", "Computer Lab", 180),
        ("Academic Block", "Auditorium", 190),
        ("Academic Block", "Cafeteria", 140),
        ("Cafeteria", "Auditorium", 180),
        ("Computer Lab", "Auditorium", 150),
    ]

    # Highlighted Path: Main Gate -> Academic Block -> Computer Lab
    hl_path = [("Main Gate", "Academic Block"), ("Academic Block", "Computer Lab")]
    hl_edges = set(tuple(sorted(e)) for e in hl_path)

    # Draw normal roads
    for u, v, w in roads:
        edge_pair = tuple(sorted((u, v)))
        if edge_pair not in hl_edges:
            x1, y1 = nodes[u]
            x2, y2 = nodes[v]
            ax.plot([x1, x2], [y1, y2], color="#94A3B8", linewidth=2, zorder=1, linestyle="-")
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my, f"{w}m", color="#475569", fontsize=8, ha="center", va="center",
                    bbox=dict(boxstyle="square,pad=0.2", facecolor="white", edgecolor="#CBD5E1", linewidth=1), zorder=2)

    # Draw highlighted roads (Thick Orange Line)
    for u, v in hl_path:
        x1, y1 = nodes[u]
        x2, y2 = nodes[v]
        ax.plot([x1, x2], [y1, y2], color="#EA580C", linewidth=5, zorder=3, linestyle="-")
        w = [road[2] for road in roads if tuple(sorted((road[0], road[1]))) == tuple(sorted((u, v)))][0]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my, f"{w}m", color="#C2410C", fontsize=9, fontweight="bold", ha="center", va="center",
                bbox=dict(boxstyle="square,pad=0.3", facecolor="#FFF7ED", edgecolor="#EA580C", linewidth=1.5), zorder=4)

    # Draw Nodes
    path_nodes = {"Main Gate", "Academic Block", "Computer Lab"}
    for name, (x, y) in nodes.items():
        if name == "Main Gate":
            color = "#16A34A"  # Source Green
            ring = True
        elif name == "Computer Lab":
            color = "#DC2626"  # Destination Red
            ring = True
        elif name in path_nodes:
            color = "#EA580C"  # Intermediate Path Orange
            ring = True
        else:
            color = "#1E293B"  # Default Slate Navy
            ring = False

        if ring:
            outer = plt.Circle((x, y), 22, color=color, fill=False, linewidth=2, zorder=5)
            ax.add_patch(outer)

        circle = plt.Circle((x, y), 16, color=color, zorder=6)
        ax.add_patch(circle)

        # Labels
        lbl_color = color if ring else "#0F172A"
        ax.text(x, y - 32, name, color=lbl_color, fontsize=10, fontweight="bold" if ring else "normal",
                ha="center", va="center", zorder=7)

    # Title & Legend Box
    ax.text(320, 460, "CAMPUS ROAD TOPOLOGY & SHORTEST ROUTE (DIJKSTRA)",
            fontsize=13, fontweight="bold", color="#0F172A", ha="center")
    ax.text(320, 440, "Highlighted Path: Main Gate ➔ Academic Block ➔ Computer Lab (Total Distance: 500m)",
            fontsize=10, color="#EA580C", fontweight="bold", ha="center")

    ax.set_xlim(20, 620)
    ax.set_ylim(50, 480)
    ax.axis("off")
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "campus_map.png")
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("Saved", out_path)

# -------------------------------------------------------------
# 2. Generate Full GUI Screenshot Simulation
# -------------------------------------------------------------
def generate_gui_screenshot():
    # Load the campus map image we just saved
    map_img_path = os.path.join(OUTPUT_DIR, "campus_map.png")
    if not os.path.exists(map_img_path):
        generate_campus_map()
    map_img = Image.open(map_img_path)

    # Resize map to fit into the right panel of GUI
    width, height = 1200, 720
    gui = Image.new("RGB", (width, height), color="#F4F6F9")
    draw = ImageDraw.Draw(gui)

    # 1. Header Banner
    draw.rectangle([(0, 0), (width, 70)], fill="#1E293B")
    # Header text
    try:
        font_title = ImageFont.truetype("segoeui.ttf", 22)
        font_sub = ImageFont.truetype("segoeui.ttf", 12)
        font_bold = ImageFont.truetype("segoeuib.ttf", 13)
        font_card_title = ImageFont.truetype("segoeuib.ttf", 14)
        font_regular = ImageFont.truetype("segoeui.ttf", 12)
        font_small = ImageFont.truetype("segoeui.ttf", 11)
        font_stat = ImageFont.truetype("segoeuib.ttf", 26)
    except:
        font_title = font_sub = font_bold = font_card_title = font_regular = font_small = font_stat = None

    draw.text((25, 12), "📍 SMART CAMPUS SHORT ROUTE FINDER", fill="#FFFFFF", font=font_title)
    draw.text((25, 42), "Shortest Path Optimization using Dijkstra's Algorithm | DAA Practical Examination", fill="#94A3B8", font=font_sub)

    # 2. Left Control Panel
    panel_left, panel_top, panel_right, panel_bottom = 20, 85, 380, 680
    
    # Card 1: Route Selection
    draw.rounded_rectangle([(panel_left, panel_top), (panel_right, 260)], radius=8, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((35, 95), "1. Select Route Endpoints", fill="#0F172A", font=font_card_title)
    
    draw.text((35, 125), "Starting Location (Source):", fill="#475569", font=font_bold)
    draw.rounded_rectangle([(35, 145), (365, 175)], radius=4, fill="#F8FAFC", outline="#CBD5E1", width=1)
    draw.text((45, 152), "Main Gate", fill="#0F172A", font=font_regular)
    draw.text((345, 152), "▼", fill="#64748B", font=font_small)

    draw.text((35, 185), "Target Location (Destination):", fill="#475569", font=font_bold)
    draw.rounded_rectangle([(35, 205), (365, 235)], radius=4, fill="#F8FAFC", outline="#CBD5E1", width=1)
    draw.text((45, 212), "Computer Lab", fill="#0F172A", font=font_regular)
    draw.text((345, 212), "▼", fill="#64748B", font=font_small)

    # Button: Find Shortest Route
    draw.rounded_rectangle([(35, 245), (280, 280)], radius=4, fill="#2563EB")
    draw.text((65, 252), "⚡ Find Shortest Route", fill="#FFFFFF", font=font_bold)
    draw.rounded_rectangle([(290, 245), (365, 280)], radius=4, fill="#E2E8F0")
    draw.text((308, 252), "🔄 Reset", fill="#1E293B", font=font_bold)

    # Card 2: Calculation Results
    draw.rounded_rectangle([(panel_left, 290), (panel_right, 520)], radius=8, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((35, 300), "2. Shortest Route Result", fill="#0F172A", font=font_card_title)

    # Distance Badge
    draw.rounded_rectangle([(35, 325), (365, 375)], radius=6, fill="#F0FDF4", outline="#BBF7D0", width=1)
    draw.text((105, 335), "500.0 meters", fill="#16A34A", font=font_stat)

    # Path Details
    draw.text((35, 385), "Shortest Path:", fill="#475569", font=font_bold)
    draw.text((35, 405), "Main Gate  ➔  Academic Block  ➔  Computer Lab", fill="#EA580C", font=font_bold)

    # Step Breakdown Box
    draw.text((35, 430), "Step-by-Step Segments:", fill="#64748B", font=font_small)
    draw.rounded_rectangle([(35, 448), (365, 510)], radius=4, fill="#F8FAFC", outline="#E2E8F0", width=1)
    draw.text((45, 455), "Step 1: Main Gate ➔ Academic Block (320m) [Total: 320m]", fill="#334155", font=font_small)
    draw.text((45, 480), "Step 2: Academic Block ➔ Computer Lab (180m) [Total: 500m]", fill="#334155", font=font_small)

    # Card 3: Quick Viva Facts
    draw.rounded_rectangle([(panel_left, 530), (panel_right, 680)], radius=8, fill="#FEF3C7", outline="#FDE68A", width=1)
    draw.text((35, 540), "💡 Quick DAA Viva Facts:", fill="#92400E", font=font_bold)
    draw.text((35, 560), "• Algorithm: Dijkstra's SSSP Algorithm", fill="#78350F", font=font_small)
    draw.text((35, 578), "• Strategy: Greedy Strategy", fill="#78350F", font=font_small)
    draw.text((35, 596), "• Data Structure: Min-Heap (heapq priority queue)", fill="#78350F", font=font_small)
    draw.text((35, 614), "• Time Complexity: O((V + E) log V)", fill="#78350F", font=font_small)
    draw.text((35, 632), "• Space Complexity: O(V + E)", fill="#78350F", font=font_small)
    draw.text((35, 650), "• Network: 8 Locations, 14 Roads (Non-negative weights)", fill="#78350F", font=font_small)

    # 3. Right Map Panel
    map_left, map_top, map_right, map_bottom = 400, 85, width - 20, 680
    draw.rounded_rectangle([(map_left, map_top), (map_right, map_bottom)], radius=8, fill="#FFFFFF", outline="#E2E8F0", width=1)

    # Map Header Bar
    draw.rounded_rectangle([(map_left, map_top), (map_right, map_top + 40)], radius=8, fill="#F1F5F9")
    draw.text((map_left + 15, map_top + 10), "🗺️ Interactive Campus Map", fill="#1E293B", font=font_bold)
    draw.text((map_right - 350, map_top + 12), "Click any building to select Source/Destination", fill="#64748B", font=font_small)

    # Paste Map Image inside
    map_resized = map_img.resize((map_right - map_left - 10, map_bottom - map_top - 50))
    gui.paste(map_resized, (map_left + 5, map_top + 45))

    # 4. Bottom Status Bar
    draw.rectangle([(0, height - 25), (width, height)], fill="#E2E8F0")
    draw.text((15, height - 19), "Shortest route found: 500.0m (2 road segments). Path highlighted on map.", fill="#334155", font=font_small)
    draw.text((width - 270, height - 19), "MCA DAA Practical Project | Chandigarh University", fill="#64748B", font=font_small)

    out_path = os.path.join(OUTPUT_DIR, "dashboard_screenshot.png")
    gui.save(out_path)
    print("Saved", out_path)

# -------------------------------------------------------------
# 3. Generate Flowchart Diagram (Figure 5.1)
# -------------------------------------------------------------
def generate_flowchart():
    fig, ax = plt.subplots(figsize=(7, 9), dpi=200)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")

    steps = [
        ("Start Application", "ellipse", "#1E293B"),
        ("Initialize Campus Graph\n(8 Nodes, 14 Roads in Adjacency List)", "box", "#0284C7"),
        ("User Selects Source and Destination\n(e.g., Main Gate -> Computer Lab)", "box", "#0284C7"),
        ("Initialize dist[v] = Infinity, dist[Source] = 0\nPush (0, Source) into Min-Heap", "box", "#475569"),
        ("Extract Min from Priority Queue:\nPop node 'u' with lowest distance", "box", "#D97706"),
        ("Is 'u' the Destination Node?", "diamond", "#D97706"),
        ("Relax Neighbor Edges:\nIf dist[u] + weight < dist[v]\nUpdate dist[v] and prev[v] = u\nPush (new_dist, v) into Min-Heap", "box", "#0284C7"),
        ("Backtrack path using 'prev' pointers\nfrom Destination to Source", "box", "#16A34A"),
        ("Display Total Distance, Step Segments\nand Highlight Route in Orange on Map", "box", "#16A34A"),
        ("End / Await New User Query", "ellipse", "#1E293B")
    ]

    y = 9.0
    y_step = 0.9

    for i, (text, shape, color) in enumerate(steps):
        # Draw box
        if shape == "ellipse":
            bbox = dict(boxstyle="round4,pad=0.5", facecolor=color, edgecolor="#0F172A", alpha=0.9)
            text_color = "white"
        elif shape == "diamond":
            bbox = dict(boxstyle="square,pad=0.5", facecolor=color, edgecolor="#B45309", alpha=0.9)
            text_color = "white"
        else:
            bbox = dict(boxstyle="round,pad=0.5", facecolor=color, edgecolor="#0369A1", alpha=0.85)
            text_color = "white"

        ax.text(3.5, y, text, color=text_color, fontsize=8.5, fontweight="bold",
                ha="center", va="center", bbox=bbox)

        # Draw connecting arrow
        if i < len(steps) - 1:
            if i == 5: # diamond branch
                ax.annotate("Yes", xy=(3.5, y - 0.5), xytext=(3.5, y - 0.25),
                            arrowprops=dict(facecolor="#16A34A", edgecolor="#16A34A", width=1.5, headwidth=6),
                            fontsize=8, fontweight="bold", color="#16A34A", ha="left")
            else:
                ax.annotate("", xy=(3.5, y - 0.55), xytext=(3.5, y - 0.25),
                            arrowprops=dict(facecolor="#475569", edgecolor="#475569", width=1.5, headwidth=6))

        y -= y_step

    ax.set_xlim(0, 7)
    ax.set_ylim(-0.2, 9.8)
    ax.axis("off")
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "flowchart.png")
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("Saved", out_path)

if __name__ == "__main__":
    generate_campus_map()
    generate_gui_screenshot()
    generate_flowchart()

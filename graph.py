"""
Campus Route Optimizer
Module: graph.py
Purpose:
    Represents the college campus road network as a Weighted Undirected Graph
    using an Adjacency List (Python Dictionary).
"""

class CampusGraph:
    """
    Campus road network represented using an Adjacency List.
    - Vertices (Nodes): Campus buildings / locations.
    - Edges: Roads connecting two locations with a distance in meters.
    """

    def __init__(self):
        # Adjacency list: {node: {neighbor: distance_in_meters}}
        self.adj = {}
        # Coordinates for drawing on the Canvas: {node: (x, y)}
        self.positions = {}

    def add_location(self, name: str, x: int, y: int):
        """Add a campus location with (x, y) coordinates for map drawing."""
        if name not in self.adj:
            self.adj[name] = {}
            self.positions[name] = (x, y)

    def add_road(self, u: str, v: str, distance: float):
        """Add a two-way road between location u and location v with distance in meters."""
        if distance < 0:
            raise ValueError("Road distance cannot be negative.")
        
        # Roads are two-way (undirected graph)
        self.adj[u][v] = distance
        self.adj[v][u] = distance

    def get_locations(self):
        """Return list of all location names sorted alphabetically."""
        return sorted(list(self.adj.keys()))

    def get_neighbors(self, location: str):
        """Return list of (neighbor, distance) for a given location."""
        return list(self.adj.get(location, {}).items())

    def get_all_roads(self):
        """Return unique list of all roads as (u, v, distance)."""
        roads = []
        seen = set()
        for u in self.adj:
            for v, dist in self.adj[u].items():
                pair = tuple(sorted([u, v]))
                if pair not in seen:
                    seen.add(pair)
                    roads.append((pair[0], pair[1], dist))
        return roads


def create_campus_graph() -> CampusGraph:
    """
    Creates a sample campus map with 8 realistic locations and road distances.
    Mapped cleanly on an 700x500 visual canvas.
    """
    g = CampusGraph()

    # 1. Add Campus Buildings with (x, y) Canvas Coordinates
    g.add_location("Main Gate", 80, 250)
    g.add_location("Parking Lot", 200, 120)
    g.add_location("Sports Ground", 200, 380)
    g.add_location("Library", 360, 120)
    g.add_location("Academic Block", 360, 250)
    g.add_location("Cafeteria", 360, 380)
    g.add_location("Computer Lab", 540, 180)
    g.add_location("Auditorium", 540, 320)

    # 2. Add Road Connections with distances in meters
    roads = [
        ("Main Gate", "Parking Lot", 150.0),
        ("Main Gate", "Sports Ground", 180.0),
        ("Main Gate", "Academic Block", 320.0),
        
        ("Parking Lot", "Library", 160.0),
        ("Parking Lot", "Academic Block", 210.0),

        ("Sports Ground", "Cafeteria", 190.0),
        ("Sports Ground", "Academic Block", 230.0),

        ("Library", "Computer Lab", 190.0),
        ("Library", "Academic Block", 140.0),

        ("Academic Block", "Computer Lab", 180.0),
        ("Academic Block", "Auditorium", 190.0),
        ("Academic Block", "Cafeteria", 140.0),

        ("Cafeteria", "Auditorium", 180.0),
        ("Computer Lab", "Auditorium", 150.0),
    ]

    for u, v, dist in roads:
        g.add_road(u, v, dist)

    return g

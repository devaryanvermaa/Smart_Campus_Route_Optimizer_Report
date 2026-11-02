"""
Campus Route Optimizer
Module: dijkstra.py
Purpose:
    Implements Dijkstra's Shortest Path Algorithm from scratch using
    Python's standard 'heapq' (Min-Heap Priority Queue).

DAA Key Facts for Teacher / Practical Viva:
    1. Strategy: Greedy Strategy
    2. Problem Type: Single-Source Shortest Path (SSSP)
    3. Time Complexity: O((V + E) log V)
       - V = Number of locations (vertices)
       - E = Number of roads (edges)
    4. Space Complexity: O(V + E)
    5. Rule: Works only with non-negative edge weights (distances >= 0).
"""

import heapq
from typing import Tuple, List
from graph import CampusGraph


def dijkstra_shortest_path(graph: CampusGraph, source: str, destination: str) -> Tuple[float, List[str]]:
    """
    Finds the shortest route between two campus locations.

    Args:
        graph: CampusGraph instance.
        source: Starting building name.
        destination: Target building name.

    Returns:
        (total_distance_in_meters, list_of_locations_in_order)
    """
    # 1. Base Case: Source and Destination are the same
    if source == destination:
        return 0.0, [source]

    # 2. Step 1: Initialize distances to infinity and predecessors to None
    all_locations = graph.get_locations()
    dist = {loc: float('inf') for loc in all_locations}
    prev = {loc: None for loc in all_locations}
    visited = set()

    # Distance to source is always 0
    dist[source] = 0.0

    # 3. Step 2: Create Min-Heap Priority Queue with (distance, location)
    # The heap always pops the location with the smallest current distance (Greedy choice).
    min_heap = []
    heapq.heappush(min_heap, (0.0, source))

    # 4. Step 3: Relaxation loop
    while min_heap:
        curr_dist, u = heapq.heappop(min_heap)

        # Skip if already finalized
        if u in visited:
            continue
        visited.add(u)

        # Stop early once we reach the destination
        if u == destination:
            break

        # Check all neighboring locations connected by road
        for v, road_distance in graph.get_neighbors(u):
            if v not in visited:
                new_dist = curr_dist + road_distance

                # Relaxation condition: Found a shorter route to v through u
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u
                    heapq.heappush(min_heap, (new_dist, v))

    # 5. Step 4: Check if destination is reachable
    if dist[destination] == float('inf'):
        return float('inf'), []

    # 6. Step 5: Path Reconstruction (Backtracking using 'prev' pointers)
    path = []
    curr = destination
    while curr is not None:
        path.append(curr)
        curr = prev[curr]

    # Reverse path so it goes from Source -> Destination
    path.reverse()

    return dist[destination], path

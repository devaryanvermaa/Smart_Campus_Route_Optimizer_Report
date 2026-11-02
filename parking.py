"""
Smart Campus Parking & Route Optimizer
Module: parking.py
Author: Aryan (MCA DAA Project)
Description:
    Parking slot representation and Greedy Allocation Engine.
    Coordinates between campus graph nodes, real-time slot statuses,
    and Dijkstra-based shortest-distance calculations.

DAA Concept:
    Greedy Allocation Strategy
    - Optimization Criteria: Minimize walking / driving distance between
      the assigned parking slot and the driver's target destination building.
    - Greedy Choice Property: At the moment of allocation, evaluate all currently
      available slots and pick the locally optimal candidate (minimum Dijkstra distance).
    - Tie-Breaking Rule: Deterministic lowest Slot ID (e.g., 'PA-01' before 'PA-02').
    - State Transition: Slot is transitioned from 'Available' to 'Occupied' only
      after a valid path has been proven and confirmed.
"""

from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from graph import CampusGraph
from dijkstra import dijkstra_shortest_path, dijkstra_all_destinations
from sorting_searching import merge_sort, linear_search, binary_search


class ParkingSlot:
    """
    Represents an individual designated parking space on campus.
    """

    def __init__(self, slot_id: str, area_name: str, status: str = "Available", distance: Optional[float] = None):
        self.slot_id = slot_id.strip().upper()
        self.area_name = area_name.strip()
        status_clean = status.strip().capitalize()
        if status_clean not in ("Available", "Occupied"):
            raise ValueError(f"Invalid status '{status}'. Must be 'Available' or 'Occupied'.")
        self.status = status_clean
        self.distance: Optional[float] = float(distance) if distance is not None else None

    @property
    def is_available(self) -> bool:
        return self.status == "Available"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "slot_id": self.slot_id,
            "area_name": self.area_name,
            "status": self.status,
            "distance": self.distance if self.distance is not None else ""
        }

    def __repr__(self) -> str:
        return f"ParkingSlot(ID={self.slot_id}, Area={self.area_name}, Status={self.status}, Dist={self.distance})"


class ParkingManager:
    """
    Manages campus parking slots, state updates, sorting, searching,
    and greedy shortest-path allocation.
    """

    def __init__(self):
        # Dictionary mapping slot_id -> ParkingSlot
        self.slots: Dict[str, ParkingSlot] = {}

    def add_slot(self, slot_id: str, area_name: str, status: str = "Available", distance: Optional[float] = None) -> ParkingSlot:
        """
        Adds a new parking slot to the repository.

        Raises:
            ValueError: If slot_id is empty, invalid, or already exists.
        """
        slot_id = slot_id.strip().upper()
        area_name = area_name.strip()

        if not slot_id:
            raise ValueError("Slot ID cannot be empty.")
        if not area_name:
            raise ValueError("Parking Area name cannot be empty.")
        if slot_id in self.slots:
            raise ValueError(f"Parking Slot with ID '{slot_id}' already exists. Duplicates are not allowed.")

        slot = ParkingSlot(slot_id, area_name, status, distance)
        self.slots[slot_id] = slot
        return slot

    def remove_slot(self, slot_id: str) -> bool:
        """Removes a parking slot by ID."""
        slot_id = slot_id.strip().upper()
        if slot_id in self.slots:
            del self.slots[slot_id]
            return True
        return False

    def get_slot(self, slot_id: str) -> Optional[ParkingSlot]:
        """Fetch slot by ID (O(1) hash map lookup)."""
        return self.slots.get(slot_id.strip().upper())

    def get_all_slots(self) -> List[ParkingSlot]:
        """Returns all registered parking slots."""
        return list(self.slots.values())

    def get_available_slots(self) -> List[ParkingSlot]:
        """Returns all currently available slots."""
        return [s for s in self.slots.values() if s.is_available]

    def get_occupied_slots(self) -> List[ParkingSlot]:
        """Returns all currently occupied slots."""
        return [s for s in self.slots.values() if not s.is_available]

    def get_total_count(self) -> int:
        return len(self.slots)

    def get_available_count(self) -> int:
        return len(self.get_available_slots())

    def get_occupied_count(self) -> int:
        return len(self.get_occupied_slots())

    def mark_occupied(self, slot_id: str) -> bool:
        """
        Marks an existing available slot as Occupied.
        """
        slot = self.get_slot(slot_id)
        if not slot:
            raise ValueError(f"Slot '{slot_id}' does not exist.")
        if not slot.is_available:
            raise ValueError(f"Slot '{slot_id}' is already occupied.")
        slot.status = "Occupied"
        return True

    def release_slot(self, slot_id: str) -> bool:
        """
        Releases an occupied slot, making it Available.
        """
        slot = self.get_slot(slot_id)
        if not slot:
            raise ValueError(f"Slot '{slot_id}' does not exist.")
        if slot.is_available:
            raise ValueError(f"Slot '{slot_id}' is already marked available.")
        slot.status = "Available"
        return True

    # ---------------------------------------------------------
    # DAA SEARCHING & SORTING OPERATIONS
    # ---------------------------------------------------------

    def sort_slots(self, criterion: str = "id", reverse: bool = False) -> List[ParkingSlot]:
        """
        Sorts slots using manual Merge Sort (O(n log n)).

        Criteria supported:
            - 'id': Lexicographical slot ID order
            - 'status': Available first, then Occupied (or vice-versa)
            - 'distance': Proximity distance in meters (None placed at end)
            - 'area': Parking Area name
        """
        all_slots = self.get_all_slots()
        criterion = criterion.strip().lower()

        if criterion == "id":
            return merge_sort(all_slots, key=lambda s: s.slot_id, reverse=reverse)
        elif criterion == "status":
            return merge_sort(all_slots, key=lambda s: s.status, reverse=reverse)
        elif criterion == "area":
            return merge_sort(all_slots, key=lambda s: s.area_name, reverse=reverse)
        elif criterion == "distance":
            # For distance: items with None distance are treated as infinity
            return merge_sort(
                all_slots,
                key=lambda s: (s.distance if s.distance is not None else float('inf')),
                reverse=reverse
            )
        else:
            return merge_sort(all_slots, key=lambda s: s.slot_id, reverse=reverse)

    def search_slot_linear(self, target_slot_id: str) -> Tuple[Optional[ParkingSlot], int]:
        """
        Searches for a slot by ID using O(n) Linear Search on current slot list.
        Returns: (ParkingSlot_or_None, comparisons_count)
        """
        slots_list = self.get_all_slots()
        idx, comparisons = linear_search(slots_list, target_slot_id, key=lambda s: s.slot_id)
        slot = slots_list[idx] if idx is not None else None
        return slot, comparisons

    def search_slot_binary(self, target_slot_id: str) -> Tuple[Optional[ParkingSlot], int]:
        """
        Sorts slots by ID first via Merge Sort, then executes O(log n) Binary Search.
        Returns: (ParkingSlot_or_None, comparisons_count)
        """
        # Pre-condition requirement for Binary Search: array must be sorted
        sorted_slots = self.sort_slots(criterion="id", reverse=False)
        idx, comparisons = binary_search(sorted_slots, target_slot_id, key=lambda s: s.slot_id)
        slot = sorted_slots[idx] if idx is not None else None
        return slot, comparisons

    # ---------------------------------------------------------
    # GREEDY ALLOCATION ALGORITHM
    # ---------------------------------------------------------

    def update_slot_distances_to_destination(self, graph: CampusGraph, destination: str) -> None:
        """
        Calculates and assigns Dijkstra shortest distance to each slot
        relative to the target destination building.
        """
        destination = destination.strip()
        if not graph.has_node(destination):
            for s in self.slots.values():
                s.distance = None
            return

        # Run Dijkstra from destination to all nodes once (O((V+E) log V))
        distances_from_dest, _ = dijkstra_all_destinations(graph, destination)

        for slot in self.slots.values():
            area = slot.area_name
            if graph.has_node(area):
                dist = distances_from_dest.get(area, float('inf'))
                slot.distance = dist if dist != float('inf') else None
            else:
                slot.distance = None

    def find_best_parking_slot(
        self,
        graph: CampusGraph,
        destination: str
    ) -> Tuple[Optional[ParkingSlot], float, List[str], List[Dict[str, Any]]]:
        """
        Greedy Parking Allocation:
        1. Query all available parking slots.
        2. Compute shortest route distance from each eligible parking lot vertex
           to destination using Dijkstra's algorithm.
        3. Pick candidate with MINIMUM route distance.
        4. Tie-breaking rule: lowest slot ID alphabetically.

        Returns:
            (best_slot, min_distance, shortest_route, evaluation_logs)
        """
        destination = destination.strip()
        if not graph.has_node(destination):
            raise ValueError(f"Destination '{destination}' does not exist on campus.")

        available_slots = self.get_available_slots()
        if not available_slots:
            return None, float('inf'), [], []

        # Run Dijkstra from destination to all nodes once
        distances, paths = dijkstra_all_destinations(graph, destination)

        evaluations: List[Dict[str, Any]] = []
        candidates: List[Tuple[float, str, ParkingSlot, List[str]]] = []

        for slot in available_slots:
            area = slot.area_name
            if not graph.has_node(area):
                evaluations.append({
                    "slot_id": slot.slot_id,
                    "area": area,
                    "distance": float('inf'),
                    "status": "Area not in graph",
                    "route": []
                })
                continue

            dist = distances.get(area, float('inf'))
            slot.distance = dist if dist != float('inf') else None

            if dist != float('inf'):
                # Invert path so it reads: Parking Area -> ... -> Destination
                # dijkstra_all_destinations(dest) produced dest -> ... -> area
                route = list(reversed(paths[area]))
                evaluations.append({
                    "slot_id": slot.slot_id,
                    "area": area,
                    "distance": dist,
                    "status": "Eligible",
                    "route": route
                })
                # Tuple for sorting: (distance, slot_id, slot, route)
                # Guarantees primary key: min distance, tie-breaker: min slot_id
                candidates.append((dist, slot.slot_id, slot, route))
            else:
                evaluations.append({
                    "slot_id": slot.slot_id,
                    "area": area,
                    "distance": float('inf'),
                    "status": "Unreachable",
                    "route": []
                })

        if not candidates:
            return None, float('inf'), [], evaluations

        # Greedy choice: Sort candidates by (distance ASC, slot_id ASC)
        candidates.sort(key=lambda item: (item[0], item[1]))
        best_dist, _, best_slot, best_route = candidates[0]

        return best_slot, best_dist, best_route, evaluations

    def allocate_slot(
        self,
        graph: CampusGraph,
        destination: str,
        driver_name: str = "Campus Visitor",
        vehicle_number: str = "CAMPUS-01"
    ) -> Dict[str, Any]:
        """
        Executes the greedy allocation, updates slot state to 'Occupied',
        and generates an allocation record for history storage.
        """
        best_slot, dist, route, evaluations = self.find_best_parking_slot(graph, destination)

        if best_slot is None:
            if not self.get_available_slots():
                return {
                    "success": False,
                    "message": "All parking slots on campus are currently full (Occupied).",
                    "slot": None,
                    "distance": float('inf'),
                    "route": [],
                    "evaluations": evaluations
                }
            else:
                return {
                    "success": False,
                    "message": f"No available parking area has a connected route to '{destination}'.",
                    "slot": None,
                    "distance": float('inf'),
                    "route": [],
                    "evaluations": evaluations
                }

        # Transition state: Mark Occupied
        best_slot.status = "Occupied"
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        record = {
            "success": True,
            "message": f"Successfully allocated Slot {best_slot.slot_id} in {best_slot.area_name} ({dist:.1f}m to {destination}).",
            "timestamp": timestamp_str,
            "slot_id": best_slot.slot_id,
            "area_name": best_slot.area_name,
            "destination": destination,
            "distance": dist,
            "route": " -> ".join(route),
            "driver_name": driver_name.strip() or "Campus Visitor",
            "vehicle_number": vehicle_number.strip().upper() or "CAMPUS-01",
            "evaluations": evaluations
        }

        return record


def create_sample_parking_manager() -> ParkingManager:
    """
    Initializes a realistic campus parking inventory across
    Parking A (North), Parking B (South), and Parking C (East).
    """
    pm = ParkingManager()

    sample_slots = [
        # Parking A (North - close to Library & Academic Block)
        ("PA-01", "Parking A", "Available"),
        ("PA-02", "Parking A", "Occupied"),
        ("PA-03", "Parking A", "Available"),
        ("PA-04", "Parking A", "Available"),
        ("PA-05", "Parking A", "Occupied"),

        # Parking B (South - close to Cafeteria & Academic Block)
        ("PB-01", "Parking B", "Available"),
        ("PB-02", "Parking B", "Available"),
        ("PB-03", "Parking B", "Occupied"),
        ("PB-04", "Parking B", "Available"),
        ("PB-05", "Parking B", "Available"),

        # Parking C (East - close to Sports Complex & Computer Lab)
        ("PC-01", "Parking C", "Available"),
        ("PC-02", "Parking C", "Available"),
        ("PC-03", "Parking C", "Available"),
        ("PC-04", "Parking C", "Occupied"),
    ]

    for sid, area, status in sample_slots:
        pm.add_slot(sid, area, status)

    return pm

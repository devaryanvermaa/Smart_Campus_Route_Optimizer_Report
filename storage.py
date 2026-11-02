"""
Smart Campus Parking & Route Optimizer
Module: storage.py
Author: Aryan (MCA DAA Project)
Description:
    CSV Data Storage and Persistence Manager.
    Manages loading and saving of parking slots, graph road network,
    and allocation logs using Python's standard `csv` module.

DAA / System Considerations:
    - Path Resolution: Anchored to project root directory using os.path.abspath(__file__),
      ensuring stability regardless of the terminal invocation directory.
    - Fault Tolerance: Gracefully handles missing files, empty lines, and malformed rows.
    - Atomic writes / Immediate sync: Writes state to disk upon add/allocate/release actions.
"""

import os
import csv
from typing import List, Dict, Any, Optional
from graph import CampusGraph, create_sample_campus_graph
from parking import ParkingManager, ParkingSlot, create_sample_parking_manager

# Resolve absolute paths based on module location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

PARKING_SLOTS_FILE = os.path.join(DATA_DIR, "parking_slots.csv")
CAMPUS_GRAPH_FILE = os.path.join(DATA_DIR, "campus_graph.csv")
ALLOCATION_HISTORY_FILE = os.path.join(DATA_DIR, "allocation_history.csv")


def ensure_data_directory_exists() -> None:
    """Ensures that the /data folder exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


# ==========================================
# 1. PARKING SLOTS CSV STORAGE
# ==========================================

def load_parking_slots(filepath: str = PARKING_SLOTS_FILE) -> ParkingManager:
    """
    Loads parking slots from CSV into a ParkingManager instance.
    If file is absent or empty, creates default sample inventory and saves it.
    """
    ensure_data_directory_exists()
    pm = ParkingManager()

    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        # Create default initial data
        pm = create_sample_parking_manager()
        save_parking_slots(pm, filepath)
        return pm

    try:
        with open(filepath, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, start=2):
                if not row:
                    continue
                slot_id = row.get("slot_id", "").strip().upper()
                area_name = row.get("area_name", "").strip()
                status = row.get("status", "Available").strip()

                if slot_id and area_name:
                    try:
                        pm.add_slot(slot_id, area_name, status)
                    except ValueError:
                        # Skip corrupted duplicates or invalid status rows safely
                        continue
    except Exception as e:
        print(f"[Warning] Error reading '{filepath}': {e}. Falling back to default slots.")
        pm = create_sample_parking_manager()
        save_parking_slots(pm, filepath)

    if pm.get_total_count() == 0:
        pm = create_sample_parking_manager()
        save_parking_slots(pm, filepath)

    return pm


def save_parking_slots(pm: ParkingManager, filepath: str = PARKING_SLOTS_FILE) -> None:
    """
    Saves all parking slots from ParkingManager to CSV.
    """
    ensure_data_directory_exists()
    slots = pm.get_all_slots()

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        fieldnames = ["slot_id", "area_name", "status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for slot in sorted(slots, key=lambda s: s.slot_id):
            writer.writerow({
                "slot_id": slot.slot_id,
                "area_name": slot.area_name,
                "status": slot.status
            })


# ==========================================
# 2. CAMPUS GRAPH CSV STORAGE
# ==========================================

def load_campus_graph(filepath: str = CAMPUS_GRAPH_FILE) -> CampusGraph:
    """
    Loads campus road network edges from CSV into a CampusGraph.
    If file is absent or empty, creates default sample campus graph and saves it.
    """
    ensure_data_directory_exists()

    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        graph = create_sample_campus_graph()
        save_campus_graph(graph, filepath)
        return graph

    # Start with base layout with coordinates
    graph = create_sample_campus_graph()
    # Clear edges so we read exactly what is in the CSV
    for u in list(graph.adj.keys()):
        graph.adj[u] = {}

    try:
        with open(filepath, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            has_edges = False
            for row in reader:
                if not row:
                    continue
                u = row.get("source", "").strip()
                v = row.get("destination", "").strip()
                w_str = row.get("weight", "").strip()
                bidirectional = row.get("bidirectional", "True").strip().lower() == "true"

                if u and v and w_str:
                    try:
                        weight = float(w_str)
                        if weight >= 0:
                            graph.add_edge(u, v, weight, bidirectional=bidirectional)
                            has_edges = True
                    except ValueError:
                        continue

            if not has_edges:
                graph = create_sample_campus_graph()
                save_campus_graph(graph, filepath)

    except Exception as e:
        print(f"[Warning] Error reading '{filepath}': {e}. Loading default sample graph.")
        graph = create_sample_campus_graph()
        save_campus_graph(graph, filepath)

    return graph


def save_campus_graph(graph: CampusGraph, filepath: str = CAMPUS_GRAPH_FILE) -> None:
    """
    Saves campus graph edges to CSV.
    """
    ensure_data_directory_exists()
    edges = graph.get_all_edges()

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        fieldnames = ["source", "destination", "weight", "bidirectional"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for u, v, weight in edges:
            writer.writerow({
                "source": u,
                "destination": v,
                "weight": f"{weight:.1f}",
                "bidirectional": "True"
            })


# ==========================================
# 3. ALLOCATION HISTORY CSV STORAGE
# ==========================================

def load_allocation_history(filepath: str = ALLOCATION_HISTORY_FILE) -> List[Dict[str, str]]:
    """
    Reads the history of all parking allocations from CSV.
    """
    ensure_data_directory_exists()
    records: List[Dict[str, str]] = []

    if not os.path.exists(filepath):
        # Create empty file with headers
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "slot_id", "area_name", "destination",
                "distance", "route", "driver_name", "vehicle_number"
            ])
        return records

    try:
        with open(filepath, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row and row.get("slot_id"):
                    records.append(row)
    except Exception as e:
        print(f"[Warning] Error reading '{filepath}': {e}")

    return records


def append_allocation_history(record: Dict[str, Any], filepath: str = ALLOCATION_HISTORY_FILE) -> None:
    """
    Appends a new successful parking allocation record to the history CSV.
    """
    ensure_data_directory_exists()
    file_exists = os.path.exists(filepath) and os.path.getsize(filepath) > 0

    fieldnames = [
        "timestamp", "slot_id", "area_name", "destination",
        "distance", "route", "driver_name", "vehicle_number"
    ]

    with open(filepath, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": record.get("timestamp", ""),
            "slot_id": record.get("slot_id", ""),
            "area_name": record.get("area_name", ""),
            "destination": record.get("destination", ""),
            "distance": f"{record.get('distance', 0.0):.1f}" if isinstance(record.get('distance'), (int, float)) else str(record.get('distance', '')),
            "route": record.get("route", ""),
            "driver_name": record.get("driver_name", "Campus Visitor"),
            "vehicle_number": record.get("vehicle_number", "CAMPUS-01")
        })


def init_default_data_files_if_missing() -> None:
    """Ensures all data files are initialized with sample content."""
    ensure_data_directory_exists()
    if not os.path.exists(PARKING_SLOTS_FILE):
        save_parking_slots(create_sample_parking_manager(), PARKING_SLOTS_FILE)
    if not os.path.exists(CAMPUS_GRAPH_FILE):
        save_campus_graph(create_sample_campus_graph(), CAMPUS_GRAPH_FILE)
    if not os.path.exists(ALLOCATION_HISTORY_FILE):
        load_allocation_history(ALLOCATION_HISTORY_FILE)

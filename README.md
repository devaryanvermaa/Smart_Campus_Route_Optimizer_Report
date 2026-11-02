# Smart Campus Parking Allocation and Shortest-Path Optimization System

A comprehensive, beginner-friendly desktop application built with **Python 3** and **Tkinter/ttk** for academic evaluation in Design and Analysis of Algorithms (DAA).

---

## 📌 Project Overview

- **Project Title:** Design and Implementation of a Smart Campus Parking Allocation and Shortest-Path Optimization System Using Graph Algorithms
- **Target Audience:** MCA / B.Tech / M.Sc Computer Science students
- **Primary Subject:** Design and Analysis of Algorithms (DAA / Advanced Algorithms)
- **Primary Paradigms:** Greedy Strategy, Graph Theory, Single-Source Shortest Path (SSSP), Divide and Conquer, Binary Search.

---

## 🚀 Key Features

1. **Greedy Smart Parking Allocation:**
   - Evaluates all available campus parking slots in real time.
   - Calculates the exact shortest walking/driving route from candidate parking lots to the user's destination using Dijkstra's Algorithm.
   - Allocates the slot with minimal distance and enforces deterministic tie-breaking (lexicographical slot ID).
   - Prevents double-allocation and handles full capacity gracefully.

2. **Dijkstra's Shortest Path Algorithm:**
   - Implemented from scratch using an adjacency list and Python's min-heap (`heapq`).
   - Computes minimum path distances in meters.
   - Reconstructs complete step-by-step route traversal sequences.
   - Rejects negative edge weights and handles disconnected vertices safely.
   - Time Complexity: $\mathcal{O}((V + E) \log V)$ | Space Complexity: $\mathcal{O}(V + E)$.

3. **Parking Slot Inventory Management:**
   - Treeview table with status indicators (Green for Available, Red for Occupied).
   - Manual **Merge Sort** ($\mathcal{O}(n \log n)$) sorting by Slot ID, Status, Distance, or Parking Area.
   - **Linear Search** ($\mathcal{O}(n)$) and **Binary Search** ($\mathcal{O}(\log n)$) on sorted slot data with real-time comparison counts.
   - Instant addition, release, and occupancy marking with duplicate validation.

4. **Dual Campus Graph Visualization:**
   - High-performance, dependency-free native **Tkinter Canvas** visualizer.
   - Optional **Matplotlib** mode if installed.
   - Color-coded node topology (Parking Lots vs Academic Facilities).
   - Dynamic highlighting of calculated shortest routes and allocated paths.

5. **DAA Empirical Benchmarking & Reports:**
   - Live benchmarking module using `time.perf_counter()`.
   - Compares manual Merge Sort vs Python's built-in C-level Timsort on arrays of $N = 100$ to $10,000$.
   - Full CSV persistence across sessions for parking slots, road edges, and allocation history.

---

## 📂 Project Structure

```text
SmartCampusParking/
├── main.py                 # Application entry point and environment check
├── gui.py                  # Full Tkinter & ttk graphical desktop interface
├── dijkstra.py             # Dijkstra's shortest path algorithm implementation
├── graph.py                # Graph data structure using Adjacency List
├── parking.py              # ParkingSlot class & Greedy Allocation Engine
├── sorting_searching.py    # Manual Merge Sort, Linear Search, Binary Search & Benchmarks
├── storage.py              # CSV file persistence and recovery manager
├── requirements.txt        # Optional dependencies (Matplotlib)
├── README.md               # User manual and setup documentation
├── PROJECT_REPORT.md       # Full 21-section academic MCA DAA report
├── VIVA_QUESTIONS.md       # 25+ detailed viva questions and answers
├── data/                   # Persistent CSV storage (auto-generated)
│   ├── parking_slots.csv
│   ├── campus_graph.csv
│   └── allocation_history.csv
└── tests/                  # Automated unit test suite (30 test cases)
    ├── __init__.py
    ├── test_dijkstra.py
    ├── test_parking.py
    ├── test_sorting_searching.py
    ├── test_graph.py
    └── test_storage.py
```

---

## 🛠️ Installation & Setup (Windows)

### Prerequisites
- Python 3.8 or higher installed on Windows.
- Ensure **tcl/tk and IDLE** was checked during Python installation.

### Step 1: Open Terminal in the Project Directory
Open PowerShell or Command Prompt and navigate to the project directory:
```powershell
cd C:\Users\Aryan\.gemini\antigravity\scratch\SmartCampusParking
```

### Step 2: (Recommended) Create a Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install Optional Dependencies
The core system runs exclusively on Python's built-in standard library without needing external packages.
To enable enhanced Matplotlib plotting:
```powershell
pip install -r requirements.txt
```

---

## 🖥️ Running the Application

Execute the entry-point script:
```powershell
python main.py
```

### Troubleshooting: Missing Tkinter on Windows
If you receive an error stating `No module named '_tkinter'`, run the official Python Windows Installer, choose **Modify**, check the box for **tcl/tk and IDLE**, and finish the setup.

---

## 🧪 Running Automated Unit Tests

The project includes 30 unit tests covering algorithmic correctness, edge cases, negative weight rejections, and CSV serialization.

Run all tests via Python's built-in test runner:
```powershell
python -m unittest discover -s tests -p "test_*.py"
```

Expected output:
```text
..............................
----------------------------------------------------------------------
Ran 30 tests in 0.097s

OK
```

---

## 💡 DAA Concepts Quick Reference

| Algorithm / Structure | Strategy | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- |
| **Adjacency List** | Hash Map / Linked List | Query: $\mathcal{O}(\text{deg}(v))$ | $\mathcal{O}(V + E)$ |
| **Dijkstra's Algorithm** | Greedy (Min-Heap) | $\mathcal{O}((V + E) \log V)$ | $\mathcal{O}(V + E)$ |
| **Parking Allocation** | Greedy Search | $\mathcal{O}((V + E) \log V + S \log S)$ | $\mathcal{O}(V + S)$ |
| **Merge Sort** | Divide & Conquer | $\mathcal{O}(n \log n)$ (all cases) | $\mathcal{O}(n)$ |
| **Binary Search** | Divide & Conquer | $\mathcal{O}(\log n)$ | $\mathcal{O}(1)$ |
| **Linear Search** | Brute Force / Sequential | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ |

---

## 📜 License
This project is developed for academic instructional use and practical laboratory demonstrations in Master of Computer Applications (MCA) and Computer Science coursework.

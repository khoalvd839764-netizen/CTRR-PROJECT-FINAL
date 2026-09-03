# 🤖 REAL-WORLD APPLICATION: SMART VACUUM & MOPPING ROBOT SIMULATION

> **Course**: Discrete Mathematics / Graph Theory  
> **Topic**: Comprehensive application of 7 Core Graph Algorithms to Autonomous Navigation and Path Optimization for Smart Vacuum Robots in Modern Apartments.  
> **Framework**: Python 3, Pygame, Matplotlib.  
> **Source Directory**: [`ung_dung_thuc_te/`](./)  

---

## 📌 I. REAL-WORLD CONTEXT & PROBLEM FORMULATION

In the modern smart home era, autonomous cleaning robots (such as Roborock, Ecovacs, Dreame, Roomba) face several critical graph optimization challenges:
1. **Battery & Power Conservation**: Calculating the shortest obstacle-free path back to the charging dock when battery is low.
2. **Infrastructure Planning**: Interconnecting all strategic cleaning waypoints with minimum total cable length.
3. **Automated SLAM Mapping**: Incrementally mapping unknown spaces level-by-level using revolving Lidar sensor waves.
4. **Perimeter & Corner Deep Cleaning**: Tracing walls and deep corners with guaranteed backtracking when hitting dead ends.
5. **100% Non-Repetitive Full Coverage**: Traversing all corridors and walkways exactly once to maximize efficiency and brush lifespan.
6. **Intelligent Floor Surface Zoning**: Classifying Dry Zones (living room, bedrooms) for vacuuming vs. Wet Zones (kitchen, balcony, restrooms) for wet mopping.
7. **Dust Evacuation Throughput & Bottleneck Analysis**: Modeling pipe capacity from rooms to the main dustbin to identify bottlenecks (Min Cut).

This project **mathematically models an entire real-world apartment as a graph $G = (V, E)$** and applies **7 Core Discrete Mathematics Algorithms** to solve these challenges.

---

## 🏠 II. APARTMENT GRAPH MODEL $G = (V, E)$

```
                            [0] CHARGING DOCK BASE
                                     |
                            [1] FOYER SHOE CABINET
                                     |
     [LIVING ROOM]           [MASTER BEDROOM]        [KIDS BEDROOM]
   (Nodes 2, 3, 4, 5)      (Nodes 13, 14, 15, 16)   (Nodes 17, 18, 19, 20)
           \                       |                       /
            \                      |                      /
             -----> [10] NORTH CORRIDOR --- [11] EAST CORRIDOR <-----
                           |                      |
                           |                      |
                    [KITCHEN & DINING]     [12] SOUTH CORRIDOR
                    (Nodes 6, 7, 8, 9)            |
                           |                      |
                           -------------------> [BALCONY & WC]
                                               (Nodes 21, 22, 23, 24)
```

### 1. Set of 25 Nodes ($V$ - Waypoints)
Every node represents a strategic cleaning point situated in **navigable free space**, at least 15-20px away from furniture obstacles:
* **Foyer & Dock Area**:
  * `[0] Charging Dock Base`: Home origin and charging station.
  * `[1] Foyer Shoe Cabinet`: Main entrance hall walkway.
* **Living Room Area**:
  * `[2] Left Sofa`, `[3] Right Sofa`, `[4] Living Room Door`, `[5] Tea Table`.
* **Kitchen & Dining Area**:
  * `[6] Kitchen Door`, `[7] Dining Table`, `[8] Sink Area`, `[9] Cooking Stove`.
* **Central Corridor Hub**:
  * `[10] North Corridor` (links Living Room and Kitchen).
  * `[11] East Corridor` (links Master and Kids Bedrooms).
  * `[12] South Corridor` (links Kids Bedroom and Balcony).
* **Master Bedroom Area**:
  * `[13] Master Bedroom Door`, `[14] King Bed`, `[15] Dressing Table`, `[16] Wardrobe`.
* **Kids Bedroom Area**:
  * `[17] Kids Room Door`, `[18] Study Desk`, `[19] Bunk Bed`, `[20] Toy Corner`.
* **Balcony & Restroom Area**:
  * `[21] Balcony Door`, `[22] Plants Area`, `[23] Washing Machine`, `[24] Restroom Corner`.

### 2. Set of 36 Edges ($E$ - Navigable Corridors)
* Each edge $(u, v)$ has a weight $w(u, v)$ representing actual metric distance (meters) and capacity $cap(u, v)$ representing dust evacuation flow (grams/min).
* **Quadratic Bézier Curvature**: Applies normal offset vectors to bend parallel and crossing edges, ensuring **100% non-overlapping visual topology**.
* **Obstacle Avoidance**: All edge trajectories bypass furniture blocks (tables, sofas, beds, refrigerators).

---

## 🧮 III. 7 DISCRETE MATHEMATICS GRAPH ALGORITHMS APPLIED

All 7 algorithms are **directly reused from the core library `core/`**:

```
+-----------------------------------------------------------------------------------+
|                        7 CORE GRAPH ALGORITHMS SYSTEM                             |
+-------------------+--------------------------------+------------------------------+
| Algorithm         | Reused Function from core/     | Practical Application        |
+-------------------+--------------------------------+------------------------------+
| 1. Kruskal MST    | core.mst.kruskal (DSU)         | Charging grid wire planning  |
| 2. Dijkstra       | core.shortest_path.dijkstra    | Emergency return to Dock     |
| 3. BFS SLAM       | core.traversal.bfs             | Lidar wave-front mapping     |
| 4. DFS Wall-Follow| core.traversal.dfs             | Deep perimeter cleaning      |
| 5. Euler Circuit  | core.euler.hierholzer          | 100% path coverage once      |
| 6. Bipartite Graph| core.bipartite.check_bipartite | Dry vs Wet floor zoning      |
| 7. Max Flow & Cut | core.max_flow.ford_fulkerson   | Dust flow throughput & cut   |
+-------------------+--------------------------------+------------------------------+
```

### 1. Kruskal Minimum Spanning Tree (MST)
* **Practical Purpose**: Interconnects all 25 waypoints across the apartment with **minimum total charging infrastructure cable length**.
* **Mathematical Core**:
  * Sorts 36 edges ascending by weight $w(u, v)$.
  * Employs **Disjoint Set Union (DSU)** with path compression to test connectivity.
  * If $find(u) \neq find(v)$, connects $union(u, v)$ and adds edge to MST. Otherwise, rejects edge to prevent cycles.
* **Outcome**: Selects exactly $24$ edges connecting $25$ nodes with minimum total distance.

### 2. Dijkstra Shortest Path (Return to Dock)
* **Practical Purpose**: When battery falls below $15\%$ while cleaning at `[22] Plants Area`, computes the optimal obstacle-free route back to `[0] Charging Dock Base`.
* **Mathematical Core**:
  * Initializes distance labels $d[start] = 0$, all others $\infty$.
  * Greedily selects unvisited node $u$ with minimum $d[u]$, relaxing adjacent nodes:
    $$\text{If } d[u] + w(u, v) < d[v] \implies d[v] = d[u] + w(u, v), \quad parent[v] = u$$
* **Outcome**: Shortest path: `[22]` ➔ `[21]` ➔ `[12]` ➔ `[10]` ➔ `[4]` ➔ `[0]`.

### 3. BFS SLAM Mapping (Wavefront Exploration)
* **Practical Purpose**: Simulates 360° revolving Lidar sensors expanding the digital map layer by layer from the dock to adjacent rooms.
* **Mathematical Core**:
  * Uses a **FIFO Queue**. Nodes discovered first are expanded first.
  * Guarantees all living room areas are mapped before exploring bedrooms and balcony.

### 4. DFS Wall-Following (Deep Perimeter Cleaning & Backtracking)
* **Practical Purpose**: Traces room perimeters and tight corners. When reaching a dead end, the robot **backtracks** to the previous junction to continue.
* **Mathematical Core**:
  * Implements recursive depth traversal equivalent to a **Call Stack**.
  * Features animated backtracking: the robot visually reverses to parent node $u$ rather than teleporting.

### 5. Hierholzer Euler Circuit (100% Full House Coverage)
* **Practical Purpose**: Deep-cleaning mode traversing all 36 paths **exactly once**, eliminating redundant travel and brush wear.
* **Mathematical Core**:
  * Verifies Eulerian condition: all 25 vertices have **even degrees** ($deg(v) \in \{2, 4, 6\}$).
  * Runs **Hierholzer's Algorithm**: starting at `[0] Dock`, removes traversed edges and splices sub-circuits into a complete 36-step Euler circuit.

### 6. Bipartite Graph Matching (Dry vs Wet Floor Partitioning)
* **Practical Purpose**: Automatically adjusts cleaning mechanism based on floor type:
  * **Set V1 (Dry Floor - DRY)**: Living Room, Master Bedroom, Kids Bedroom $\implies$ Vacuuming mode, lifts wet mop.
  * **Set V2 (Wet Floor - WET)**: Kitchen, Balcony, Restrooms $\implies$ Lowers mop pad, increases water pump rate.
* **Mathematical Core**:
  * 2-color BFS test ($0$ and $1$). If adjacent nodes share the same color $\implies$ detects conflict and extracts odd cycle.

### 7. Ford-Fulkerson Max Flow & Min Cut (Dust Evacuation Throughput)
* **Practical Purpose**: Models automatic dust evacuation pipes from rooms to central bin `[22]`, identifying the bottleneck pipe (Min Cut) needing maintenance.
* **Mathematical Core**:
  * **Edmonds-Karp**: Finds augmenting paths from Source $S=0$ to Sink $T=22$ using BFS.
  * Augments flow by bottleneck $\Delta f = \min(c_f(u, v))$ until no augmenting path remains.
  * Identifies the bottleneck $\text{Min Cut} = (S, T)$ with capacity equal to $\text{Max Flow}$.

---

## 🖥️ IV. MULTI-VIEW 3-COLUMN DASHBOARD

The **Pygame** dashboard runs at $1920 \times 1080$ Full-HD resolution, divided into 3 synchronized columns:

```
+-----------------------------------------------------------------------------------------------------------+
| [1] Kruskal MST | [2] Dijkstra | [3] BFS SLAM | [4] DFS Wall | [5] Euler | [6] Bipartite | [7] Max-Flow   |
+------------------------------------+---------------------------------------+------------------------------+
| 🏠 COLUMN 1: 3D ISOMETRIC FLOORPLAN| 📐 COLUMN 2: MATHEMATICAL GRAPH G=(V,E)| 🔍 COLUMN 3: PSEUDOCODE & VARS|
|                                    |                                       |                              |
| - 3D 5-room apartment perspective  | - 25 Nodes & 36 Curved Bézier Edges   | - Active pseudocode highlight|
| - Obstacle-free 3D furniture       | - Synchronized energy pulse ball      | - Live Variables: DSU, Queue,|
| - Glowing Roomba with Lidar scan   | - Metric distance tags                |   Stack, Min-Cut, Distances  |
| - Controls: Zoom, Pan, 360° Rotate | - Color-coded Accepted/Rejected edges | - Controls: [PREV] [NEXT] ...|
+------------------------------------+---------------------------------------+------------------------------+
```

---

## 🎮 V. CONTROLS & KEYBOARD SHORTCUTS

| Shortcut / Action | Function |
| :--- | :--- |
| **`Number Keys 1 .. 7`** | Switch immediately between the 7 Graph Algorithms |
| **`Space Bar`** | Toggle **Auto-Play** simulation mode |
| **`S` key or `Right Arrow`** | Advance **1 Step** (*Step Next*) |
| **`B` key or `Left Arrow`** | Reverse **1 Step** (*Step Previous*) |
| **`R` key** | **Reset** algorithm to Step 0 |
| **`Mouse Wheel` / `+` `-`** | Zoom 3D view in/out (40% to 300%) |
| **`0` key** | Reset camera zoom and pan to default |
| **`Left Mouse Drag`** | Rotate 3D apartment camera 360° (*Orbit Yaw / Pitch*) |
| **`Right Mouse Drag`** | Pan 3D camera (*Translate View*) |
| **`V` key** | Toggle between **3D Isometric** and **2D Top-Down** view |
| **`F11` key** | Toggle **Fullscreen Mode** |

---

## 🚀 VI. HOW TO RUN

Launch the project from **[`main.py`](file:///home/jackie-khoa/Downloads/course/CTRR%20FINAL%20PROJECT/main.py)**:

### 1. Launch Main CLI Menu (10 Functions)
```bash
python3 main.py
```
*(Select option `10` from the menu to open the Robot Simulation, or options `1`..`9` for core graph theory modules)*

### 2. Launch Robot Simulation Dashboard Directly
```bash
python3 main.py --robot
```
*(Or: `python3 main.py --gui`)*

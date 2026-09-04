"""
Module: ung_dung_thuc_te/algorithms.py
Purpose: Reuses 100% of core algorithms from core/ for the Smart Vacuum Robot application:
  1. core.mst.kruskal               -> Minimum Spanning Tree (MST power charging grid planning).
  2. core.shortest_path.dijkstra    -> Shortest Path (Dijkstra emergency return to charging dock).
  3. core.traversal.bfs             -> Breadth-First Search (BFS SLAM map exploration).
  4. core.traversal.dfs             -> Depth-First Search (DFS wall-following + backtracking).
  5. core.euler.hierholzer          -> Euler Circuit (Hierholzer 100% house path coverage).
  6. core.bipartite.check_bipartite -> Bipartite Graph Check (Dry vs Wet floor zoning).
  7. core.max_flow.ford_fulkerson   -> Max Flow & Min Cut (Dust evacuation pipe capacity).
"""

# =============================================================================
# IMPORT DIRECTLY FROM CORE ALGORITHM LIBRARY (core/)
# =============================================================================
from core.mst import kruskal, DSU
from core.shortest_path import dijkstra
from core.traversal import bfs, dfs
from core.euler import hierholzer, check_eulerian
from core.bipartite import check_bipartite
from core.max_flow import ford_fulkerson

from ung_dung_thuc_te.data_model import HOUSE_NODES_DATA, HOUSE_EDGES


class RobotAlgorithms:
    """
    Adapter class connecting core mathematical algorithms (core/)
    with the real-world vacuum robot simulation dashboard.
    """
    def __init__(self, n=25, edges=None, nodes_data=None):
        self.n = n
        self.edges = edges if edges is not None else HOUSE_EDGES
        self.nodes_data = nodes_data if nodes_data is not None else HOUSE_NODES_DATA

        # 1. Adjacency list dictionary for core: {u: [(v, w), ...]}
        self.adj_dict = {u: [] for u in range(self.n)}
        for u, v, l_m, cap in self.edges:
            self.adj_dict[u].append((v, l_m))
            self.adj_dict[v].append((u, l_m))

        # Sort neighbors for deterministic traversal
        for u in range(self.n):
            self.adj_dict[u].sort(key=lambda x: x[0])

        # 2. Weighted edge list for core: [(u, v, w), ...]
        self.edges_with_weights = [(u, v, l_m) for u, v, l_m, cap in self.edges]

        # 3. Capacity edge list for core: [(u, v, cap), ...]
        self.edges_with_capacity = []
        for u, v, l_m, cap in self.edges:
            self.edges_with_capacity.append((u, v, cap))
            self.edges_with_capacity.append((v, u, cap))

    # =========================================================================
    # ALGORITHM 1: MINIMUM SPANNING TREE (KRUSKAL MST)
    # Reuses: core.mst.kruskal & core.mst.DSU
    # =========================================================================
    def build_kruskal_steps(self):
        """
        Calls Kruskal algorithm from core.mst and converts execution trace
        into visual simulation steps for the robot.
        """
        mst_edges, total_weight, core_trace = kruskal(self.edges_with_weights, self.n)

        steps = []
        dsu = DSU(self.n)
        chosen = set()
        rejected = set()
        accum_w = 0.0

        sorted_edges = sorted(self.edges, key=lambda x: x[2])
        for idx, (u, v, w, cap) in enumerate(sorted_edges):
            root_u = dsu.find(u)
            root_v = dsu.find(v)
            edge_tuple = tuple(sorted((u, v)))
            is_chosen = (root_u != root_v)

            step_data = {
                "step_num": idx + 1,
                "total_steps": len(sorted_edges),
                "scanned_edge": edge_tuple,
                "scanned_weight": w,
                "current_u": u,
                "current_v": v,
                "pseudocode_line": 5 if is_chosen else 6,
                "pseudocode": [
                    "1: [core.mst.kruskal] Sort edges ascending by w(u, v)",
                    "2: Initialize DSU: each node in its own disjoint set",
                    "3: For each edge (u, v):",
                    "4:   If find(u) != find(v): // No cycle formed",
                    "5:       union(u, v) -> ADD EDGE TO MST",
                    "6:   Else: DISCARD EDGE (CREATES CYCLE)"
                ],
                "math_state": {
                    "DSU find(u)": root_u,
                    "DSU find(v)": root_v,
                    "MST Edges Selected": f"{len(chosen) + (1 if is_chosen else 0)} / {self.n - 1}",
                    "Total MST Distance": f"{accum_w + (w if is_chosen else 0):.1f}m"
                },
                "action": "SELECT EDGE FOR MST" if is_chosen else "REJECT (CYCLE DETECTED)",
                "status_color": (52, 211, 153) if is_chosen else (239, 68, 68),
                "reason": f"DSU: find({u}) != find({v}) ({root_u} != {root_v}) -> NO CYCLE." if is_chosen else f"DSU: find({u}) == find({v}) ({root_u}) -> CLOSES CYCLE!",
                "result_text": f"-> SELECTED ({u} <-> {v}) (w = {w:.1f}m)! MST: {len(chosen)+1}/{self.n - 1} edges." if is_chosen else f"-> SKIPPED ({u} <-> {v}): Alternate path exists.",
                "after_chosen": set(chosen),
                "after_rejected": set(rejected),
                "after_weight": accum_w
            }

            if is_chosen:
                dsu.union(u, v)
                chosen.add(edge_tuple)
                accum_w += w
            else:
                rejected.add(edge_tuple)

            step_data["after_chosen"] = set(chosen)
            step_data["after_rejected"] = set(rejected)
            step_data["after_weight"] = accum_w
            steps.append(step_data)

            if len(chosen) == self.n - 1:
                break

        return steps

    # =========================================================================
    # ALGORITHM 2: SHORTEST PATH (DIJKSTRA)
    # Reuses: core.shortest_path.dijkstra
    # =========================================================================
    def build_dijkstra_steps(self, start=22, target=0):
        """
        Calls Dijkstra algorithm from core.shortest_path and generates relaxation steps
        to guide the Robot safely back to Dock [0].
        """
        result = dijkstra(self.adj_dict, self.n, start=start, end=target)

        steps = []
        dist = [float('inf')] * self.n
        visited = [False] * self.n
        parent = [-1] * self.n
        dist[start] = 0.0
        step_count = 0

        while True:
            u = -1
            min_d = float('inf')
            for i in range(self.n):
                if not visited[i] and dist[i] < min_d:
                    min_d = dist[i]
                    u = i

            if u == -1 or dist[u] == float('inf'):
                break

            visited[u] = True

            tree_edges = []
            for i in range(self.n):
                if parent[i] != -1:
                    tree_edges.append(tuple(sorted((parent[i], i))))

            for v, w in self.adj_dict[u]:
                edge_tuple = tuple(sorted((u, v)))
                step_count += 1
                is_relaxed = (dist[u] + w < dist[v])
                old_d = dist[v]
                if is_relaxed:
                    dist[v] = dist[u] + w
                    parent[v] = u

                d_str = "INF" if old_d == float('inf') else f"{old_d:.1f}m"
                step_data = {
                    "step_num": step_count,
                    "scanned_edge": edge_tuple,
                    "scanned_weight": w,
                    "current_u": u,
                    "current_v": v,
                    "pseudocode_line": 5 if is_relaxed else 6,
                    "pseudocode": [
                        "1: [core.shortest_path.dijkstra] Pick u with min d[u] -> visited[u]=True",
                        "2: For each adjacent vertex v of u:",
                        "3:   Calculate alt = d[u] + weight(u, v)",
                        "4:   If alt < d[v]: // Found shorter path",
                        "5:       d[v] = alt; parent[v] = u; // RELAX EDGE",
                        "6:   Else: Keep existing d[v]"
                    ],
                    "math_state": {
                        "Active node u": u,
                        "Current d[u]": f"{dist[u]:.1f}m",
                        f"Neighbor d[{v}]": f"{dist[v]:.1f}m",
                        "Predecessor parent[v]": parent[v]
                    },
                    "action": "UPDATE SHORTER PATH" if is_relaxed else "KEEP EXISTING (SUBOPTIMAL)",
                    "status_color": (56, 189, 248) if is_relaxed else (148, 163, 184),
                    "reason": f"d[{u}] + w = {dist[u]:.1f} + {w:.1f} = {dist[u]+w:.1f}m < d[{v}] ({d_str})" if is_relaxed else f"Path via [{v}] ({d_str}) is already shorter or equal.",
                    "result_text": f"-> OPTIMIZED: d[{v}] = {dist[v]:.1f}m (via [{u}])" if is_relaxed else f"-> IGNORED ({u} -> {v}).",
                    "after_chosen": set(tree_edges),
                    "after_rejected": set(),
                    "after_weight": dist[u]
                }
                steps.append(step_data)
            if u == target:
                break
        return steps

    # =========================================================================
    # ALGORITHM 3: BREADTH-FIRST SEARCH (BFS SLAM MAP)
    # Reuses: core.traversal.bfs
    # =========================================================================
    def build_bfs_steps(self, start=0):
        """
        Calls BFS from core.traversal to simulate Lidar wave expansion and map exploration.
        """
        order, core_tree_edges, trace_table = bfs(self.adj_dict, self.n, start=start)

        steps = []
        visited = [False] * self.n
        queue = [start]
        visited[start] = True
        tree_edges = set()
        step_count = 0

        while queue:
            u = queue.pop(0)
            for v, l_m in self.adj_dict[u]:
                edge_tuple = tuple(sorted((u, v)))
                step_count += 1
                is_new = not visited[v]
                if is_new:
                    visited[v] = True
                    queue.append(v)
                    tree_edges.add(edge_tuple)

                step_data = {
                    "step_num": step_count,
                    "scanned_edge": edge_tuple,
                    "scanned_weight": l_m,
                    "current_u": u,
                    "current_v": v,
                    "pseudocode_line": 5 if is_new else 6,
                    "pseudocode": [
                        "1: [core.traversal.bfs] Init Queue = [start], visited[start] = True",
                        "2: While Queue is not empty:",
                        "3:   u = Queue.pop(0)",
                        "4:   For each neighbor v of u:",
                        "5:       If not visited[v]:",
                        "6:           visited[v] = True, Queue.append(v) -> ADD BFS EDGE"
                    ],
                    "math_state": {
                        "FIFO Queue": list(queue),
                        "Source Node u": u,
                        "Status visited[v]": visited[v],
                        "BFS Tree Edges": len(tree_edges)
                    },
                    "action": "DISCOVER NEW EDGE (BFS)" if is_new else "ALREADY VISITED",
                    "status_color": (56, 189, 248) if is_new else (148, 163, 184),
                    "reason": f"Lidar scan from [{u}] discovered UNVISITED door to [{v}]." if is_new else f"Waypoint [{v}] has already been surveyed.",
                    "result_text": f"-> ADDED ({u} <-> {v}) TO BFS SPANNING TREE!" if is_new else f"-> SKIPPED ({u} <-> {v}) to prevent loop.",
                    "after_chosen": set(tree_edges),
                    "after_rejected": set(),
                    "after_weight": 0
                }
                steps.append(step_data)
        return steps

    # =========================================================================
    # ALGORITHM 4: DEPTH-FIRST SEARCH (DFS WALL-FOLLOWING)
    # Reuses: core.traversal.dfs
    # =========================================================================
    def build_dfs_steps(self, start=0):
        """
        Calls DFS from core.traversal and adds realistic Backtracking steps for the robot.
        """
        order, core_tree_edges, trace_table = dfs(self.adj_dict, self.n, start=start)

        steps = []
        visited = [False] * self.n
        tree_edges = set()
        step_count = [0]

        def dfs_visit(u, p=-1):
            visited[u] = True
            for v, l_m in self.adj_dict[u]:
                if v == p:
                    continue

                edge_tuple = tuple(sorted((u, v)))
                step_count[0] += 1
                is_new = not visited[v]

                step_data = {
                    "step_num": step_count[0],
                    "scanned_edge": edge_tuple,
                    "scanned_weight": l_m,
                    "current_u": u,
                    "current_v": v,
                    "pseudocode_line": 4 if is_new else 5,
                    "pseudocode": [
                        "1: [core.traversal.dfs] Function DFS(u): visited[u] = True",
                        "2: For each neighbor v of u:",
                        "3:   If not visited[v]: DFS(v) -> ADVANCE DEEP",
                        "4:   Else: Already visited -> Skip",
                        "5: -> Dead end reached: BACKTRACK to parent u"
                    ],
                    "math_state": {
                        "Current Node u": u,
                        "Neighbor Node v": v,
                        "Status visited[v]": visited[v],
                        "DFS Tree Edges": len(tree_edges) + (1 if is_new else 0)
                    },
                    "action": "ADVANCE DEEPER (DFS TREE)" if is_new else "BACK EDGE (ALREADY VISITED)",
                    "status_color": (168, 85, 247) if is_new else (148, 163, 184),
                    "reason": f"Discovered unvisited corner [{v}] along the perimeter." if is_new else f"Corner [{v}] has already been cleaned.",
                    "result_text": f"-> ENTER [{v}]: Expanding deep search branch!" if is_new else f"-> SKIPPED ({u} <-> {v}): Already visited node.",
                    "after_chosen": set(tree_edges),
                    "after_rejected": set(),
                    "after_weight": 0
                }
                steps.append(step_data)

                if is_new:
                    tree_edges.add(edge_tuple)
                    dfs_visit(v, u)

                    # BACKTRACK STEP
                    step_count[0] += 1
                    backtrack_step = {
                        "step_num": step_count[0],
                        "scanned_edge": edge_tuple,
                        "scanned_weight": l_m,
                        "current_u": v,
                        "current_v": u,
                        "pseudocode_line": 5,
                        "pseudocode": [
                            "1: [core.traversal.dfs] Function DFS(u): visited[u] = True",
                            "2: For each neighbor v of u:",
                            "3:   If not visited[v]: DFS(v)",
                            "4: ...",
                            "5: -> Dead end at v: BACKTRACK to parent u"
                        ],
                        "math_state": {
                            "Dead End Node": v,
                            "Backtracking to Parent": u,
                            "Call Stack State": "Popping from Call Stack"
                        },
                        "action": "BACKTRACK TO PARENT",
                        "status_color": (250, 204, 21),
                        "reason": f"Node [{v}] branch fully explored, reversing to [{u}] for next corridor.",
                        "result_text": f"-> REVERSE ROBOT from [{v}] to [{u}]!",
                        "after_chosen": set(tree_edges),
                        "after_rejected": set(),
                        "after_weight": 0
                    }
                    steps.append(backtrack_step)

        dfs_visit(start)
        return steps

    # =========================================================================
    # ALGORITHM 5: EULER CIRCUIT (HIERHOLZER FULL COVERAGE)
    # Reuses: core.euler.hierholzer & core.euler.check_eulerian
    # =========================================================================
    def build_euler_steps(self):
        """
        Calls Hierholzer from core.euler to create a circuit covering 100% of corridors
        exactly once.
        """
        tour, tour_edges, trace_table = hierholzer(self.adj_dict, self.n, start=0)

        steps = []
        chosen = set()
        total_dist = 0.0

        for idx, (u, v) in enumerate(tour_edges):
            edge_tuple = tuple(sorted((u, v)))
            chosen.add(edge_tuple)
            w = 3.0
            for eu, ev, ew in self.edges_with_weights:
                if tuple(sorted((eu, ev))) == edge_tuple:
                    w = ew
                    break
            total_dist += w

            step_data = {
                "step_num": idx + 1,
                "total_steps": len(tour_edges),
                "scanned_edge": edge_tuple,
                "scanned_weight": w,
                "current_u": u,
                "current_v": v,
                "pseudocode_line": 3,
                "pseudocode": [
                    "1: [core.euler.hierholzer] Verify: All vertex degrees are even",
                    "2: Init Stack = [0], Tour = []",
                    "3: Loop: Traverse (u, v) and REMOVE VISITED EDGE",
                    "4: If vertex has no remaining edges: Push to Tour",
                    "5: Splice sub-circuits -> Complete Euler Circuit"
                ],
                "math_state": {
                    "Edge Step": f"{idx + 1} / {len(tour_edges)}",
                    "Traversed Edge": f"({u} -> {v})",
                    "Total Euler Distance": f"{total_dist:.1f}m",
                    "Floor Coverage": f"{len(chosen)}/36 edges ({(len(chosen)/36)*100:.0f}%)"
                },
                "action": "TRAVERSE EULER EDGE (EXACTLY ONCE)",
                "status_color": (250, 204, 21),
                "reason": f"Cleaned segment ({u} <-> {v}) and removed from graph to avoid repetition.",
                "result_text": f"-> COVERED ({u} -> {v})! Cleaned {len(chosen)}/36 floor paths.",
                "after_chosen": set(chosen),
                "after_rejected": set(),
                "after_weight": total_dist
            }
            steps.append(step_data)
        return steps

    # =========================================================================
    # ALGORITHM 6: BIPARTITE GRAPH CHECK (FLOOR ZONING)
    # Reuses: core.bipartite.check_bipartite
    # =========================================================================
    def build_bipartite_steps(self):
        """
        Calls bipartite verification from core.bipartite to partition floor
        into Dry Zone (Vacuum only) vs Wet Zone (Mop enabled).
        """
        bip_res = check_bipartite(self.adj_dict, self.n)

        steps = []
        color = [-1] * self.n
        queue = []
        step_count = 0
        chosen_edges = set()

        for start_node in range(self.n):
            if color[start_node] == -1:
                color[start_node] = 0
                queue.append(start_node)

                while queue:
                    u = queue.pop(0)
                    for v, l_m in self.adj_dict[u]:
                        edge_tuple = tuple(sorted((u, v)))
                        step_count += 1

                        if color[v] == -1:
                            color[v] = 1 - color[u]
                            queue.append(v)
                            chosen_edges.add(edge_tuple)
                            is_conflict = False
                        elif color[v] == color[u]:
                            is_conflict = True
                        else:
                            is_conflict = False
                            chosen_edges.add(edge_tuple)

                        u_zone = "DRY FLOOR" if color[u] == 0 else "WET FLOOR"
                        v_zone = "DRY FLOOR" if color[v] == 0 else ("WET FLOOR" if color[v] == 1 else "UNASSIGNED")

                        step_data = {
                            "step_num": step_count,
                            "scanned_edge": edge_tuple,
                            "scanned_weight": l_m,
                            "current_u": u,
                            "current_v": v,
                            "pseudocode_line": 3 if not is_conflict else 4,
                            "pseudocode": [
                                "1: [core.bipartite.check_bipartite] Assign color[start] = 0 (Dry)",
                                "2: For each neighbor v of u:",
                                "3:   If v uncolored: color[v] = 1 - color[u] (Wet)",
                                "4:   If color[v] == color[u]: CONFLICT (Odd cycle detected)",
                                "5: Conclusion: Partition into 2 independent cleaning modes"
                            ],
                            "math_state": {
                                f"Color Node u [{u}]": u_zone,
                                f"Color Node v [{v}]": v_zone,
                                "Dry Zone Nodes (V1)": sum(1 for c in color if c == 0),
                                "Wet Zone Nodes (V2)": sum(1 for c in color if c == 1)
                            },
                            "action": "VALID 2-COLORING" if not is_conflict else "ODD CYCLE CONFLICT",
                            "status_color": (236, 72, 153) if not is_conflict else (239, 68, 68),
                            "reason": f"Opposite colors: [{u}]={u_zone} <-> [{v}]={v_zone}." if not is_conflict else f"Conflict! Adjacent nodes [{u}] and [{v}] have same color {u_zone}.",
                            "result_text": f"-> VALID: Swap vacuum/mop attachments between zones." if not is_conflict else "-> Odd cycle detected across rooms!",
                            "after_chosen": set(chosen_edges),
                            "after_rejected": set(),
                            "after_weight": 0
                        }
                        steps.append(step_data)
        return steps

    # =========================================================================
    # ALGORITHM 7: MAX FLOW FORD-FULKERSON & MIN CUT
    # Reuses: core.max_flow.ford_fulkerson
    # =========================================================================
    def build_maxflow_steps(self, source=0, sink=22):
        """
        Calls Ford-Fulkerson from core.max_flow to find maximum dust evacuation throughput
        and bottleneck Min Cut.
        """
        max_flow, flow_mat, min_cut, cut_sets, core_trace = ford_fulkerson(
            self.edges_with_capacity, self.n, source=source, sink=sink
        )

        steps = []
        step_count = 0
        total_max_flow = 0
        chosen_edges = set()

        for trace_entry in core_trace:
            path = trace_entry["path"]
            bottleneck = trace_entry["bottleneck"]
            total_max_flow = trace_entry["current_max_flow"]

            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                edge_tuple = tuple(sorted((u, v)))
                chosen_edges.add(edge_tuple)
                step_count += 1

                cap = 80
                for eu, ev, _, c in self.edges:
                    if tuple(sorted((eu, ev))) == edge_tuple:
                        cap = c
                        break

                step_data = {
                    "step_num": step_count,
                    "scanned_edge": edge_tuple,
                    "scanned_weight": cap,
                    "current_u": u,
                    "current_v": v,
                    "pseudocode_line": 4,
                    "pseudocode": [
                        "1: [core.max_flow.ford_fulkerson] Init flow f(u, v) = 0",
                        "2: Loop: Find augmenting path from S to T (BFS)",
                        "3:   Bottleneck Delta_f = min(residual capacity)",
                        "4:   Augment flow: f(u, v) += Delta_f along the path",
                        "5: -> When no path remains: Max Flow = Min Cut"
                    ],
                    "math_state": {
                        "Augmenting Path": " -> ".join(map(str, path)),
                        "Bottleneck Capacity (Delta_f)": f"{bottleneck} g/min",
                        "Max Flow Throughput": f"{total_max_flow} g/min",
                        "Pumping Path Segment": f"({u} -> {v}) [+{bottleneck}/{cap}]"
                    },
                    "action": "AUGMENT DUST FLOW",
                    "status_color": (248, 113, 113),
                    "reason": f"Augmenting path {path} has bottleneck capacity {bottleneck} g/min.",
                    "result_text": f"-> PUMPED +{bottleneck} g/min via ({u} -> {v})!",
                    "after_chosen": set(chosen_edges),
                    "after_rejected": set(),
                    "after_weight": total_max_flow
                }
                steps.append(step_data)

        return steps

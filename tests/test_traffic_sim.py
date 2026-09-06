# -*- coding: utf-8 -*-
"""
Module: tests/test_traffic_sim.py
Purpose: Unit tests for Urban Smart Traffic Grid Simulation & 4 Core CTRR Algorithms:
  1. Dijkstra Dynamic Re-routing
  2. BFS Concentric Rescue Wave Dispatch
  3. DFS 1-Way Deadlock & Cycle Detection
  4. MST Kruskal Smart Signal Cabling Network
"""

import unittest
from ung_dung_thuc_te.city_data_model import CityTrafficGrid, TrafficNode, TrafficEdge
from ung_dung_thuc_te.traffic_algorithms import TrafficAlgorithms


class TestTrafficGridDataModel(unittest.TestCase):
    """Tests the Graph Data Model initialization and structural properties."""

    def setUp(self):
        self.grid = CityTrafficGrid()

    def test_grid_initialization(self):
        """Validates that all 16 city intersections and 27 roads are initialized."""
        self.assertEqual(self.grid.get_num_nodes(), 16, "City graph must have exactly 16 nodes.")
        self.assertEqual(len(self.grid.edges), 27, "City graph must have exactly 27 edges.")

        # Check key landmarks
        fire_station = self.grid.get_node(0)
        self.assertIsNotNone(fire_station)
        self.assertEqual(fire_station.node_type, "fire_station")

        hospital = self.grid.get_node(1)
        self.assertIsNotNone(hospital)
        self.assertEqual(hospital.node_type, "hospital")

        toc = self.grid.get_node(2)
        self.assertIsNotNone(toc)
        self.assertEqual(toc.node_type, "toc")

    def test_adjacency_list_construction(self):
        """Verifies graph connectivity and adjacency representation."""
        adj = self.grid.build_adjacency_list(use_dynamic_weight=False)
        self.assertEqual(len(adj), 16)
        for u in range(16):
            self.assertGreater(len(adj[u]), 0, f"Node {u} must have at least one outgoing connection.")

    def test_spatial_lookups(self):
        """Tests nearest node and edge spatial point queries for mouse interaction."""
        node_0 = self.grid.get_node(0)
        found_nid = self.grid.find_nearest_node(node_0.x + 2, node_0.y - 2, max_radius=30)
        self.assertEqual(found_nid, 0, "Spatial query must resolve node 0.")


class TestTrafficAlgorithms(unittest.TestCase):
    """Tests 4 CTRR Graph algorithms on the Traffic Grid."""

    def setUp(self):
        self.grid = CityTrafficGrid()
        self.algo = TrafficAlgorithms(self.grid)

    def test_1_dijkstra_ambulance_shortest_path(self):
        """Tests Dijkstra shortest path from Fire Station [0] to Hospital [1]."""
        res = self.algo.compute_ambulance_route(start=0, end=1)
        self.assertTrue(res["success"], "Dijkstra must find path from 0 to 1.")
        self.assertEqual(res["path"][0], 0)
        self.assertEqual(res["path"][-1], 1)
        self.assertGreater(res["actual_distance_meters"], 0)
        self.assertGreater(res["estimated_time_minutes"], 0)
        self.assertFalse(res["is_rerouted"], "Initial path in clear conditions should not be rerouted.")

    def test_1_dijkstra_dynamic_rerouting(self):
        """Tests that Dijkstra dynamically avoids heavy traffic jams and chooses an alternate route."""
        # 1. Baseline route
        res_base = self.algo.compute_ambulance_route(start=0, end=1)
        original_path = list(res_base["path"])

        # 2. Block/severely jam the edges along the original path
        for i in range(len(original_path) - 1):
            u = original_path[i]
            v = original_path[i + 1]
            edge = self.grid.get_edge_between(u, v)
            if edge:
                edge.set_congestion(4.0)  # Maximum gridlock

        # 3. Recalculate
        res_rerouted = self.algo.compute_ambulance_route(start=0, end=1)
        self.assertTrue(res_rerouted["success"])
        self.assertEqual(res_rerouted["path"][0], 0)
        self.assertEqual(res_rerouted["path"][-1], 1)
        self.assertTrue(res_rerouted["is_rerouted"], "Dijkstra must trigger re-routing when main route is jammed.")
        self.assertNotEqual(res_rerouted["path"], original_path, "Path must diverge from the jammed route.")

    def test_1b_dijkstra_breakpoint_rerouting(self):
        """Tests Yêu cầu 1: Breakpoint detection & Pivot rerouting when a path edge is severed."""
        base_res = self.algo.compute_ambulance_route(start=0, end=1)
        path = base_res["path"]
        self.assertGreater(len(path), 2)
        
        # Sever the middle edge
        break_edge = (path[1], path[2])
        reroute_res = self.algo.compute_reroute_at_breakpoint(0, 1, blocked_edge=break_edge)
        
        self.assertTrue(reroute_res["success"], "Must find alternate detour.")
        self.assertEqual(reroute_res["pivot_node"], path[1], "Pivot must be the node immediately before break.")
        self.assertEqual(reroute_res["full_path"][0], 0)
        self.assertEqual(reroute_res["full_path"][-1], 1)
        # Ensure severed edge is not in detour
        for i in range(len(reroute_res["detour_path"]) - 1):
            seg = (reroute_res["detour_path"][i], reroute_res["detour_path"][i+1])
            rev_seg = (seg[1], seg[0])
            self.assertNotEqual(seg, break_edge)
            self.assertNotEqual(rev_seg, break_edge)

    def test_2_bfs_rescue_wave(self):
        """Tests BFS radial level-by-level dispatch from incident epicenter."""
        incident = 2  # TOC
        bfs_res = self.algo.compute_rescue_wave_bfs(incident_node=incident)

        self.assertEqual(bfs_res["incident_node"], incident)
        self.assertEqual(bfs_res["order"][0], incident, "BFS must start at incident epicenter.")
        self.assertEqual(len(bfs_res["order"]), 16, "BFS on connected city graph must reach all 16 nodes.")
        self.assertGreaterEqual(bfs_res["max_level"], 2, "City radius should have multiple levels.")
        self.assertEqual(len(bfs_res["tree_edges"]), 15, "BFS tree on 16 nodes must have exactly 15 edges.")
        # Yêu cầu 2: Node level map for layer coloring
        self.assertIn("node_level_map", bfs_res)
        self.assertEqual(bfs_res["node_level_map"][incident], 0)
        self.assertIn("levels", bfs_res)

    def test_3_tarjan_bridges_and_cut_vertices(self):
        """Tests Yêu cầu 3: Tarjan DFS discovery of critical bridges and cut vertices."""
        tarjan_res = self.algo.find_critical_bridges_and_cut_vertices(start_node=0)

        self.assertIn("bridges", tarjan_res)
        self.assertIn("cut_vertices", tarjan_res)
        self.assertGreater(tarjan_res["num_bridges"], 0, "Must detect lifeline bridges (Cát Lái & Bến Xe Miền Đông).")
        self.assertGreater(tarjan_res["num_cut_vertices"], 0, "Must detect cut vertices.")

        # Check discovered bridges
        bridge_pairs = [(min(b["u"], b["v"]), max(b["u"], b["v"])) for b in tarjan_res["bridges"]]
        # Bridge to Cát Lái Container Port [9] from [8]
        self.assertIn((8, 9), bridge_pairs, "Cầu Cát Lái (8, 9) must be identified as critical bridge.")
        # Bridge to Bến Xe Miền Đông [3] from [12]
        self.assertIn((3, 12), bridge_pairs, "Cầu Bến Xe Miền Đông (12, 3) must be identified as critical bridge.")

        # Check cut vertices
        self.assertIn(8, tarjan_res["cut_vertices"], "Node 8 must be cut vertex guarding Port 9.")
        self.assertIn(12, tarjan_res["cut_vertices"], "Node 12 must be cut vertex guarding Bus Terminal 3.")

        # Check mathematical condition for all bridges: low[v] > discovery_time[u]
        disc = tarjan_res["discovery_time"]
        low = tarjan_res["low"]
        for b in tarjan_res["bridges"]:
            u, v = b["u"], b["v"]
            # one direction must satisfy low > disc
            cond1 = low[v] > disc[u]
            cond2 = low[u] > disc[v]
            self.assertTrue(cond1 or cond2, f"Bridge ({u}, {v}) must satisfy low > disc.")

    def test_3_dfs_deadlock_and_cycles(self):
        """Tests backward-compatible DFS helper."""
        dfs_res = self.algo.detect_traffic_deadlocks_dfs(start_node=2)
        self.assertIn("bridges", dfs_res)
        self.assertIn("cut_vertices", dfs_res)
        self.assertIn("trace_table", dfs_res)

    def test_4_mst_kruskal_smart_signal_cabling(self):
        """Tests Kruskal MST for optical fiber signal cabling."""
        mst_res = self.algo.plan_smart_signal_mst()

        self.assertEqual(mst_res["num_nodes"], 16)
        self.assertEqual(mst_res["num_mst_edges"], 15, "MST on 16 nodes must have exactly 15 edges (|V|-1).")
        self.assertGreater(mst_res["total_cable_length_meters"], 0)
        self.assertGreater(mst_res["savings_percent"], 0, "MST must save significant cable vs full mesh.")
        self.assertLess(mst_res["total_cable_length_meters"], mst_res["all_roads_length_meters"])


if __name__ == "__main__":
    unittest.main()

"""
Module: ung_dung_thuc_te/data_model.py
Purpose: Defines the complete real-world apartment data model for the Smart Vacuum Robot simulation.
Includes:
  1. 25 Nodes representing strategic cleaning points across 5 rooms and corridors (with Dry/Wet floor zones).
  2. 36 Edges representing physical movement corridors (metric distance in meters and dust flow capacity).
  3. Obstacle-Free 2D coordinates (Free Space Coordinates).
  4. Anti-overlapping Bézier curvature table for clean edge visualization.
  5. 3D Architectural furniture blocks and room floor boundaries.
"""

# =============================================================================
# 1. 25 NODES DATA (APARTMENT WAYPOINTS)
# =============================================================================
# Each node represents a strategic cleaning position:
# - name: Real-world location description
# - room: Room category (DOCK, LIVING, KITCHEN, CORRIDOR, MASTER, KIDS, BALCONY)
# - zone: Floor type (DRY: Hardwood/dry tile, WET: Wet tile/balcony/kitchen)
# - dust: Initial dust accumulation (grams)
HOUSE_NODES_DATA = {
    # Foyer & Dock Area
    0: {"name": "Charging Dock Base", "room": "DOCK", "zone": "DRY", "dust": 0},
    1: {"name": "Foyer Shoe Cabinet", "room": "DOCK", "zone": "DRY", "dust": 30},

    # Living Room
    2: {"name": "Left Sofa", "room": "LIVING", "zone": "DRY", "dust": 60},
    3: {"name": "Right Sofa", "room": "LIVING", "zone": "DRY", "dust": 65},
    4: {"name": "Living Room Door", "room": "LIVING", "zone": "DRY", "dust": 70},
    5: {"name": "Tea Table", "room": "LIVING", "zone": "DRY", "dust": 80},

    # Kitchen & Dining Area
    6: {"name": "Kitchen Door", "room": "KITCHEN", "zone": "WET", "dust": 90},
    7: {"name": "Dining Table", "room": "KITCHEN", "zone": "WET", "dust": 110},
    8: {"name": "Sink Area", "room": "KITCHEN", "zone": "WET", "dust": 95},
    9: {"name": "Cooking Stove", "room": "KITCHEN", "zone": "WET", "dust": 120},

    # Central Corridor Hub
    10: {"name": "North Corridor", "room": "CORRIDOR", "zone": "DRY", "dust": 40},
    11: {"name": "East Corridor", "room": "CORRIDOR", "zone": "DRY", "dust": 45},
    12: {"name": "South Corridor", "room": "CORRIDOR", "zone": "DRY", "dust": 50},

    # Master Bedroom
    13: {"name": "Master Bedroom Door", "room": "MASTER", "zone": "DRY", "dust": 55},
    14: {"name": "King Bed", "room": "MASTER", "zone": "DRY", "dust": 50},
    15: {"name": "Dressing Table", "room": "MASTER", "zone": "DRY", "dust": 40},
    16: {"name": "Wardrobe", "room": "MASTER", "zone": "DRY", "dust": 45},

    # Kids Bedroom
    17: {"name": "Kids Room Door", "room": "KIDS", "zone": "DRY", "dust": 65},
    18: {"name": "Study Desk", "room": "KIDS", "zone": "DRY", "dust": 85},
    19: {"name": "Bunk Bed", "room": "KIDS", "zone": "DRY", "dust": 90},
    20: {"name": "Toy Corner", "room": "KIDS", "zone": "DRY", "dust": 130},

    # Balcony & Restroom
    21: {"name": "Balcony Door", "room": "BALCONY", "zone": "WET", "dust": 100},
    22: {"name": "Plants Area", "room": "BALCONY", "zone": "WET", "dust": 140},
    23: {"name": "Washing Machine", "room": "BALCONY", "zone": "WET", "dust": 70},
    24: {"name": "Restroom Corner", "room": "BALCONY", "zone": "WET", "dust": 60}
}


# =============================================================================
# 2. 2D OBSTACLE-FREE COORDINATES (FREE SPACE COORDINATES)
# =============================================================================
# (x, y) coordinates on the 560 x 780 px floorplan reference space.
# All 25 nodes reside in navigable free space, at least 15-20px away from furniture edges.
HOUSE_BASE_COORDS = {
    # Foyer & Dock
    0: (60, 115),    # [0] Charging Dock Base
    1: (130, 115),   # [1] Foyer Shoe Cabinet

    # Living Room
    2: (200, 130),   # [2] Left Sofa
    3: (285, 130),   # [3] Right Sofa
    4: (185, 235),   # [4] Living Room Door
    5: (290, 235),   # [5] Tea Table

    # Kitchen & Dining
    6: (150, 345),   # [6] Kitchen Door
    7: (60, 395),    # [7] Dining Table
    8: (60, 510),    # [8] Sink Area
    9: (150, 510),   # [9] Cooking Stove

    # Central Corridor
    10: (230, 345),  # [10] North Corridor
    11: (310, 345),  # [11] East Corridor
    12: (310, 510),  # [12] South Corridor

    # Master Bedroom
    13: (380, 115),  # [13] Master Bedroom Door
    14: (470, 115),  # [14] King Bed
    15: (380, 235),  # [15] Dressing Table
    16: (470, 235),  # [16] Wardrobe

    # Kids Bedroom
    17: (380, 355),  # [17] Kids Room Door
    18: (470, 355),  # [18] Study Desk
    19: (380, 510),  # [19] Bunk Bed
    20: (470, 510),  # [20] Toy Corner

    # Balcony & Restroom
    21: (180, 675),  # [21] Balcony Door
    22: (80, 725),   # [22] Plants Area
    23: (310, 675),  # [23] Washing Machine
    24: (440, 725)   # [24] Restroom Corner
}


# =============================================================================
# 3. 36 ACCURATE HOUSE EDGES
# =============================================================================
# Structure: (u, v, length_in_meters, capacity_in_grams)
# - u, v: Connected nodes
# - length: Physical robot navigation distance (meters)
# - capacity: Dust evacuation throughput / bandwidth (grams/min)
HOUSE_EDGES = [
    # 1. Dock & Foyer Area (4 edges)
    (0, 1, 2.0, 50),
    (1, 2, 2.5, 60),
    (2, 4, 3.0, 80),
    (4, 0, 4.0, 70),

    # 2. Living Room Area (5 edges)
    (2, 3, 3.0, 80),
    (3, 5, 3.0, 80),
    (5, 4, 3.0, 80),
    (4, 10, 2.5, 90),
    (10, 2, 3.5, 90),

    # 3. Kitchen & Dining Area (7 edges)
    (6, 7, 2.5, 90),
    (7, 8, 3.0, 100),
    (8, 9, 2.5, 90),
    (9, 6, 3.0, 80),
    (6, 8, 3.5, 90),
    (6, 10, 2.0, 90),
    (8, 10, 3.5, 90),

    # 4. Central Corridor Hub (3 edges)
    (10, 11, 3.5, 120),
    (11, 12, 3.5, 120),
    (12, 10, 3.5, 120),

    # 5. Master Bedroom Area (5 edges)
    (13, 14, 2.5, 70),
    (14, 16, 3.0, 70),
    (16, 15, 2.5, 70),
    (11, 13, 2.5, 80),
    (15, 11, 3.0, 80),

    # 6. Kids Bedroom Area (5 edges)
    (17, 18, 2.5, 75),
    (18, 20, 3.0, 75),
    (20, 19, 2.5, 75),
    (12, 17, 2.5, 80),
    (19, 12, 3.0, 80),

    # 7. Balcony & Restroom Area (7 edges)
    (21, 22, 3.5, 90),
    (22, 23, 3.0, 70),
    (23, 24, 3.5, 70),
    (24, 21, 4.0, 90),
    (21, 23, 4.0, 90),
    (12, 21, 3.5, 100),
    (23, 12, 4.0, 100)
]
                                                                                            

# =============================================================================
# 4. ANTI-OVERLAPPING BÉZIER CURVATURES
# =============================================================================
# Normal offset (pixels) to bend overlapping or parallel edges:
# - Positive (+): Bend to the right of direction vector
# - Negative (-): Bend to the left of direction vector
EDGE_CURVATURE = {
    # Living Room & Foyer
    (4, 10): 22,
    (2, 10): -22,
    (0, 4): -18,
    (2, 4): 16,
    (4, 5): 14,

    # Kitchen & Dining
    (6, 10): 18,
    (8, 10): -24,
    (6, 8): 18,
    (9, 6): -14,

    # Central Corridor Hub
    (12, 10): 16,

    # Master Bedroom
    (11, 13): 18,
    (11, 15): -18,
    (14, 16): 14,

    # Kids Bedroom
    (12, 17): 18,
    (12, 19): -18,
    (18, 20): 14,

    # Balcony & Restroom
    (12, 21): 20,
    (12, 23): -20,
    (21, 23): 18,
    (22, 23): -18,
    (21, 24): 26
}


# =============================================================================
# 5. 3D ARCHITECTURAL ROOM LAYOUT & SOLID FURNITURE BLOCKS
# =============================================================================
# Room tuple: (x, y, width, depth, label, floor_color, grid_color)
ROOMS_LAYOUT_3D = [
    (20, 50, 310, 240, "LIVING ROOM", (23, 37, 84, 50), (30, 58, 138, 40)),
    (20, 310, 170, 310, "KITCHEN & DINING", (69, 26, 3, 45), (146, 64, 14, 35)),
    (350, 50, 190, 240, "MASTER BEDROOM", (59, 7, 100, 45), (107, 33, 168, 35)),
    (350, 310, 190, 310, "KIDS BEDROOM", (30, 41, 59, 50), (71, 85, 105, 35)),
    (20, 640, 520, 120, "BALCONY & RESTROOM", (6, 78, 59, 45), (4, 120, 87, 35))
]

# 3D Furniture blocks placed against walls, completely clear of graph paths
FURNITURE_3D_BLOCKS = [
    # 1. Foyer & Charging Dock
    {"x": 45, "y": 55, "z": 0, "w": 30, "d": 25, "h": 8, "top": (14, 165, 233), "sx": (2, 132, 199), "sy": (3, 105, 161)},
    {"x": 115, "y": 55, "z": 0, "w": 35, "d": 25, "h": 22, "top": (100, 116, 139), "sx": (71, 85, 105), "sy": (51, 65, 85)},

    # 2. Living Room
    {"x": 235, "y": 55, "z": 0, "w": 85, "d": 20, "h": 26, "top": (37, 99, 235), "sx": (29, 78, 216), "sy": (30, 64, 175)},
    {"x": 235, "y": 75, "z": 0, "w": 85, "d": 35, "h": 14, "top": (59, 130, 246), "sx": (37, 99, 235), "sy": (29, 78, 216)},
    {"x": 235, "y": 175, "z": 0, "w": 35, "d": 30, "h": 12, "top": (217, 119, 6), "sx": (180, 83, 9), "sy": (146, 64, 14)},
    {"x": 25, "y": 165, "z": 0, "w": 20, "d": 55, "h": 12, "top": (30, 41, 59), "sx": (15, 23, 42), "sy": (15, 23, 42)},
    {"x": 27, "y": 170, "z": 12, "w": 5, "d": 45, "h": 24, "top": (14, 165, 233), "sx": (2, 132, 199), "sy": (3, 105, 161)},

    # 3. Kitchen & Dining
    {"x": 25, "y": 315, "z": 0, "w": 35, "d": 35, "h": 46, "top": (148, 163, 184), "sx": (100, 116, 139), "sy": (71, 85, 105)},
    {"x": 25, "y": 390, "z": 0, "w": 50, "d": 55, "h": 18, "top": (180, 83, 9), "sx": (146, 64, 14), "sy": (120, 53, 15)},
    {"x": 25, "y": 555, "z": 0, "w": 140, "d": 45, "h": 20, "top": (100, 116, 139), "sx": (71, 85, 105), "sy": (51, 65, 85)},
    {"x": 60, "y": 560, "z": 20, "w": 28, "d": 22, "h": 2, "top": (226, 232, 240), "sx": (203, 213, 225), "sy": (148, 163, 184)},
    {"x": 120, "y": 560, "z": 20, "w": 26, "d": 22, "h": 2, "top": (239, 68, 68), "sx": (185, 28, 28), "sy": (153, 27, 27)},

    # 4. Master Bedroom
    {"x": 435, "y": 55, "z": 0, "w": 90, "d": 16, "h": 32, "top": (107, 33, 168), "sx": (88, 28, 135), "sy": (59, 7, 100)},
    {"x": 440, "y": 71, "z": 0, "w": 80, "d": 65, "h": 16, "top": (248, 250, 252), "sx": (203, 213, 225), "sy": (148, 163, 184)},
    {"x": 490, "y": 175, "z": 0, "w": 40, "d": 95, "h": 44, "top": (63, 63, 70), "sx": (39, 39, 42), "sy": (24, 24, 27)},
    {"x": 360, "y": 55, "z": 0, "w": 40, "d": 25, "h": 18, "top": (147, 51, 234), "sx": (126, 34, 206), "sy": (107, 33, 168)},

    # 5. Kids Bedroom
    {"x": 455, "y": 320, "z": 0, "w": 70, "d": 42, "h": 18, "top": (14, 165, 233), "sx": (2, 132, 199), "sy": (3, 105, 161)},
    {"x": 480, "y": 475, "z": 0, "w": 50, "d": 110, "h": 32, "top": (59, 130, 246), "sx": (37, 99, 235), "sy": (29, 78, 216)},
    {"x": 360, "y": 555, "z": 0, "w": 40, "d": 40, "h": 14, "top": (245, 158, 11), "sx": (217, 119, 6), "sy": (180, 83, 9)},

    # 6. Balcony & Restroom
    {"x": 35, "y": 650, "z": 0, "w": 30, "d": 30, "h": 26, "top": (16, 185, 129), "sx": (5, 150, 105), "sy": (4, 120, 87)},
    {"x": 290, "y": 705, "z": 0, "w": 40, "d": 38, "h": 26, "top": (226, 232, 240), "sx": (203, 213, 225), "sy": (148, 163, 184)},
    {"x": 485, "y": 705, "z": 0, "w": 35, "d": 38, "h": 22, "top": (248, 250, 252), "sx": (203, 213, 225), "sy": (148, 163, 184)}
]

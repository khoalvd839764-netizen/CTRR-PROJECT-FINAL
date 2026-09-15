import math
import os
import subprocess
import matplotlib.pyplot as plt


DEFAULT_RESULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results"))


def _resolve_filepath(filename):
    if not os.path.isabs(filename):
        dirname = os.path.dirname(filename)
        if not dirname:
            filename = os.path.join(DEFAULT_RESULT_DIR, filename)
        elif not filename.startswith("results") and not filename.startswith("./results"):
            filename = os.path.join(DEFAULT_RESULT_DIR, os.path.basename(filename))
        else:
            filename = os.path.abspath(filename)
    filename = os.path.normpath(filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    return filename


def compute_smart_layout(g_or_n):
    import math
    
    n = g_or_n.get('n', 0) if isinstance(g_or_n, dict) else (g_or_n.n if hasattr(g_or_n, 'n') else g_or_n)
    
    if n <= 8:
        R_max, node_radius, node_font, weight_font, fig_size = 10, 0.9, 11, 9, (8, 8)
    elif n == 14:
        R_max, node_radius, node_font, weight_font, fig_size = 16.0, 0.95, 11, 9.5, (15, 11)
    elif n == 15:
        R_4max, node_radius, node_font, weight_font, fig_size = 16, 0.85, 10, 8.5, (10, 10)
        R_max = 16
    elif n == 20:
        R_max, node_radius, node_font, weight_font, fig_size = 19.0, 0.85, 10, 8.5, (14, 11)
    elif n == 30:
        R_max, node_radius, node_font, weight_font, fig_size = 22, 0.75, 8.5, 7.5, (13, 13)
    else:
        R_max, node_radius, node_font, weight_font, fig_size = max(12, n * 0.7), 0.7, 9, 8, (11, 11)

    pos_dict = g_or_n.get('pos') if isinstance(g_or_n, dict) else getattr(g_or_n, 'pos', None)
    if isinstance(pos_dict, dict) and len(pos_dict) == n:
        xs = [pt[0] for pt in pos_dict.values()]
        ys = [pt[1] for pt in pos_dict.values()]
        if xs and ys:
            max_coord = max(max(abs(x) for x in xs), max(abs(y) for y in ys))
            R_max = max(R_max, max_coord)
        return dict(pos_dict), R_max, node_radius, node_font, weight_font, fig_size

    if hasattr(g_or_n, 'edges') and len(g_or_n.edges) > 0:
        try:
            import networkx as nx
            G = nx.Graph()
            for edge in g_or_n.edges:
                u, v = edge[0], edge[1]
                w = edge[2] if len(edge) > 2 else 1
                w_val = float(w)
                inv_w = 1.0 / max(0.1, w_val)
                G.add_edge(u, v, weight=inv_w)
            
            for i in range(n):
                G.add_node(i)

            pos = nx.spring_layout(G, weight='weight', seed=42, iterations=150)
            coords = {i: (pos[i][0] * R_max, pos[i][1] * R_max) for i in range(n)}
            return coords, R_max, node_radius, node_font, weight_font, fig_size
        except ImportError:
            pass

    coords = {}
    if n <= 8:
        for i in range(n):
            theta = (2 * math.pi * i) / n if n > 0 else 0
            coords[i] = (R_max * math.cos(theta), R_max * math.sin(theta))
    elif n == 15:
        for i in range(10):
            theta = (2 * math.pi * i) / 10
            coords[i] = (16 * math.cos(theta), 16 * math.sin(theta))
        for i in range(5):
            theta = (2 * math.pi * i) / 5 + (math.pi / 10)
            coords[10 + i] = (8 * math.cos(theta), 8 * math.sin(theta))
    elif n == 20:
        coords = {
            0: (-16.0, 5.0),  1: (-16.0, -5.0),
            2: (-10.5, 12.0), 3: (-10.0, 4.0),  4: (-10.0, -4.0),  5: (-10.5, -12.0),
            6: (-3.5, 14.5),  7: (-3.0, 6.5),   8: (-3.0, -1.5),   9: (-3.0, -8.5),  10: (-3.5, -15.0),
            11: (4.0, 13.5),  12: (4.0, 5.5),   13: (4.0, -2.5),   14: (4.0, -9.5),  15: (4.0, -15.5),
            16: (11.0, 9.5),  17: (11.0, 1.0),  18: (11.0, -8.0),
            19: (17.0, 0.0)
        }
    elif n == 30:
        for i in range(16):
            theta = (2 * math.pi * i) / 16
            coords[i] = (22 * math.cos(theta), 22 * math.sin(theta))
        for i in range(10):
            theta = (2 * math.pi * i) / 10 + (math.pi / 16)
            coords[16 + i] = (13 * math.cos(theta), 13 * math.sin(theta))
        for i in range(4):
            theta = (2 * math.pi * i) / 4 + (math.pi / 8)
            coords[26 + i] = (5.5 * math.cos(theta), 5.5 * math.sin(theta))
    else:
        num_layers = max(1, math.ceil(n / 10))
        nodes_per_layer = n // num_layers
        curr = 0
        for layer in range(num_layers, 0, -1):
            r = (R_max * layer) / num_layers
            count = nodes_per_layer if layer > 1 else (n - curr)
            for j in range(count):
                if curr < n:
                    theta = (2 * math.pi * j) / count
                    coords[curr] = (r * math.cos(theta), r * math.sin(theta))
                    curr += 1
                    
    xs = [pt[0] for pt in coords.values()]
    ys = [pt[1] for pt in coords.values()]
    if xs and ys:
        max_coord = max(max(abs(x) for x in xs), max(abs(y) for y in ys))
        R_max = max(R_max, max_coord)
    return coords, R_max, node_radius, node_font, weight_font, fig_size


def _draw_base_nodes(ax, coords, node_radius, node_font, colors=None, labels=None, default_color="#2E7D32"):
    if colors is None:
        colors = {}
    if labels is None:
        labels = {}

    for i, (x, y) in coords.items():
        node_color = colors.get(i, default_color)
        circle = plt.Circle((x, y), node_radius, color=node_color, ec="#1B5E20", lw=1.2, zorder=5)
        ax.add_patch(circle)

        text_label = labels.get(i, str(i))
        ax.text(x, y, text_label, color="white", fontweight="bold", fontsize=node_font, ha="center", va="center", zorder=6)


def _handle_save_and_show(fig, filename, show):
    filepath = _resolve_filepath(filename)
    try:
        plt.savefig(filepath, dpi=300, bbox_inches="tight", facecolor="#fafafa")
    except OSError:
        base, ext = os.path.splitext(filepath)
        import time
        alt_filepath = f"{base}_{int(time.time())}{ext}"
        try:
            plt.savefig(alt_filepath, dpi=300, bbox_inches="tight", facecolor="#fafafa")
            print(f"\n[!] Cảnh báo: Tệp '{os.path.basename(filepath)}' đang được mở hoặc bị khóa bởi ứng dụng khác.")
            print(f"    -> Đã tự động lưu thành: '{os.path.basename(alt_filepath)}'")
            filepath = alt_filepath
        except Exception as e:
            print(f"\n[!] Lỗi: Không thể lưu hình ảnh đồ thị: {e}")
    if show:
        try:
            if os.name == "posix":
                cmd = "open" if "darwin" in os.sys.platform else "xdg-open"
                subprocess.Popen([cmd, filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif os.name == "nt":
                os.startfile(filepath)
        except Exception:
            plt.show(block=False)
            plt.pause(0.5)
    plt.close(fig)
    return filepath


def draw(g_or_n, edges=None, directed=False, filename="current_graph.png", highlight=None, colors=None, show=True):
    if hasattr(g_or_n, "n"):
        n = g_or_n.n
        edges_list = getattr(g_or_n, "edges", [])
        is_directed = getattr(g_or_n, "directed", False)
        is_weighted = getattr(g_or_n, "weighted", False)
        curvatures = getattr(g_or_n, "curvatures", {}) or {}
        labels = getattr(g_or_n, "labels", None)
        weight_positions = getattr(g_or_n, "weight_positions", {}) or {}
    elif isinstance(g_or_n, dict):
        n = g_or_n.get("n", 0)
        edges_list = g_or_n.get("edges", edges or [])
        is_directed = g_or_n.get("directed", directed)
        is_weighted = g_or_n.get("weighted", False)
        curvatures = g_or_n.get("curvatures", {}) or {}
        labels = g_or_n.get("labels", None)
        weight_positions = g_or_n.get("weight_positions", {}) or {}
    else:
        n = int(g_or_n)
        edges_list = edges if edges is not None else []
        is_directed = directed
        is_weighted = False
        curvatures = {}
        labels = None
        weight_positions = {}

    if highlight is None:
        highlight = []
    if colors is None:
        colors = {}

    coords, max_R, node_radius, node_font, weight_font, fig_size = compute_smart_layout(g_or_n)
    fig, ax = plt.subplots(figsize=fig_size, facecolor="#fafafa")
    ax.set_facecolor("#fafafa")

    for edge in edges_list:
        u, v = edge[0], edge[1]
        w = edge[2] if len(edge) > 2 else 1
        x_u, y_u = coords[u]
        x_v, y_v = coords[v]

        is_highlighted = (
            (u, v) in highlight
            or (u, v, w) in highlight
            or (not is_directed and ((v, u) in highlight or (v, u, w) in highlight))
        )

        edge_color = "#E53935" if is_highlighted else "#78909C"
        
        import math
        try:
            w_val = float(w)
            dynamic_lw = max(0.8, min(8.0, 0.5 + math.sqrt(w_val) * 0.9))
        except:
            dynamic_lw = 1.2
            
        line_width = (dynamic_lw * 1.6) if is_highlighted else dynamic_lw
        z_order = 3 if is_highlighted else 1
        rad = curvatures.get((u, v), 0.07 if is_directed else 0.0)

        if not is_directed:
            ax.plot([x_u, x_v], [y_u, y_v], color=edge_color, linewidth=line_width, zorder=z_order, alpha=0.85)
        else:
            ax.annotate(
                "",
                xy=(x_v, y_v),
                xytext=(x_u, y_u),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=edge_color,
                    lw=line_width,
                    shrinkA=node_radius * 18,
                    shrinkB=node_radius * 18,
                    mutation_scale=12 if n >= 20 else 14,
                    connectionstyle=f"arc3,rad={rad}",
                ),
                zorder=z_order,
                alpha=0.9,
            )

        if is_weighted or w != 1:
            if (u, v) in weight_positions:
                mid_x, mid_y = weight_positions[(u, v)]
            elif not is_directed and (v, u) in weight_positions:
                mid_x, mid_y = weight_positions[(v, u)]
            else:
                mid_x, mid_y = (x_u + x_v) / 2, (y_u + y_v) / 2

            ax.text(
                mid_x, mid_y, str(w),
                fontsize=weight_font, fontweight="bold",
                color="#1565C0" if not is_highlighted else "#B71C1C",
                ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="#ffffff", edgecolor="#CFD8DC", alpha=0.92, lw=0.6),
                zorder=4,
            )

    _draw_base_nodes(ax, coords, node_radius, node_font, colors=colors, labels=labels, default_color="#2E7D32")
    margin = max_R * 1.15
    ax.set_aspect("equal")
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin, margin)
    plt.axis("off")
    return _handle_save_and_show(fig, filename, show)


draw_graph = draw


def draw_euler(g, path, edges_order, filename="euler_path.png", show=True):
    coords, max_R, node_radius, node_font, _, fig_size = compute_smart_layout(g)
    fig, ax = plt.subplots(figsize=fig_size, facecolor="#fafafa")
    ax.set_facecolor("#fafafa")

    for edge in g.edges:
        u, v = edge[0], edge[1]
        xu, yu, xv, yv = coords[u][0], coords[u][1], coords[v][0], coords[v][1]
        if not g.directed:
            ax.plot([xu, xv], [yu, yv], color="#cfd8dc", linewidth=1.5, zorder=1)
        else:
            ax.annotate("", xy=(xv, yv), xytext=(xu, yu), arrowprops=dict(arrowstyle="->", color="#cfd8dc", lw=1.5, shrinkA=12, shrinkB=12, mutation_scale=12), zorder=1)

    for step, edge in enumerate(edges_order, 1):
        u, v = edge[0], edge[1]
        xu, yu, xv, yv = coords[u][0], coords[u][1], coords[v][0], coords[v][1]
        if not g.directed:
            ax.plot([xu, xv], [yu, yv], color="#ff5722", linewidth=2.5, zorder=2)
        else:
            ax.annotate("", xy=(xv, yv), xytext=(xu, yu), arrowprops=dict(arrowstyle="->", color="#ff5722", lw=2.5, shrinkA=12, shrinkB=12, mutation_scale=15), zorder=2)

        mid_x, mid_y = (xu + xv) / 2, (yu + yv) / 2
        ax.text(mid_x, mid_y, str(step), fontsize=9, fontweight="bold", color="#ff5722", ha="center", va="center", bbox=dict(boxstyle="circle,pad=0.2", facecolor="white", edgecolor="#ff5722", alpha=0.9), zorder=4)

    node_colors = {}
    if path:
        node_colors[path[0]] = "#00e676"
        node_colors[path[-1]] = "#d50000"

    _draw_base_nodes(ax, coords, node_radius, node_font, colors=node_colors, default_color="#78909c")
    margin = max_R * 1.15
    ax.set_aspect("equal")
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin, margin)
    plt.axis("off")
    return _handle_save_and_show(fig, filename, show)


def draw_mst(g, mst_edges, total_weight, filename="mst_result.png", show=True):
    coords, max_R, node_radius, node_font, _, fig_size = compute_smart_layout(g)
    fig, ax = plt.subplots(figsize=fig_size, facecolor="#fafafa")
    ax.set_facecolor("#fafafa")

    mst_set = set()
    for e in mst_edges:
        mst_set.add((e[0], e[1]))
        mst_set.add((e[1], e[0]))

    for edge in g.edges:
        u, v = edge[0], edge[1]
        w = edge[2] if len(edge) > 2 else 1
        xu, yu, xv, yv = coords[u][0], coords[u][1], coords[v][0], coords[v][1]

        import math
        try:
            dyn_lw = max(0.8, min(8.0, 0.5 + math.sqrt(float(w)) * 0.9))
        except:
            dyn_lw = 1.2
            
        if (u, v) in mst_set:
            ax.plot([xu, xv], [yu, yv], color="#2979ff", linewidth=dyn_lw * 1.5, zorder=2)
            mid_x, mid_y = (xu + xv) / 2, (yu + yv) / 2
            ax.text(mid_x, mid_y, str(w), fontsize=9, fontweight="bold", color="#2979ff", ha="center", va="center", bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#2979ff", alpha=0.9), zorder=4)
        else:
            ax.plot([xu, xv], [yu, yv], color="#90a4ae", linestyle="--", linewidth=dyn_lw * 0.6, zorder=1)
            mid_x, mid_y = (xu + xv) / 2, (yu + yv) / 2
            ax.text(mid_x, mid_y, str(w), fontsize=8, color="#90a4ae", ha="center", va="center", bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.7), zorder=3)

    _draw_base_nodes(ax, coords, node_radius, node_font, default_color="#2979ff")
    plt.title(f"CÂY KHUNG NHỎ NHẤT (MST) – Tổng trọng số = {total_weight}", fontsize=13, fontweight="bold", pad=20)
    margin = max_R * 1.15
    ax.set_aspect("equal")
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin, margin)
    plt.axis("off")
    return _handle_save_and_show(fig, filename, show)


def draw_max_flow(g, flow_matrix, min_cut_edges, max_flow, source, sink, filename="max_flow.png", show=True):
    from matplotlib.lines import Line2D
    coords, max_R, node_radius, node_font, _, fig_size = compute_smart_layout(g)
    fig, ax = plt.subplots(figsize=fig_size, facecolor="#fafafa")
    ax.set_facecolor("#fafafa")

    cut_set = set((e[0], e[1]) for e in min_cut_edges)
    is_orig_undirected = getattr(g, "original_undirected", False)
    edges_to_draw = getattr(g, "base_edges", g.edges) if is_orig_undirected else g.edges
    edge_pairs = set((e[0], e[1]) for e in edges_to_draw)

    for edge in edges_to_draw:
        u, v = edge[0], edge[1]
        cap = edge[2] if len(edge) > 2 else 0

        if is_orig_undirected:
            f_uv = flow_matrix[u][v] if (u < len(flow_matrix) and v < len(flow_matrix[u])) else 0
            f_vu = flow_matrix[v][u] if (v < len(flow_matrix) and u < len(flow_matrix[v])) else 0
            if f_vu > f_uv:
                u, v = v, u
                flow = f_vu
            else:
                flow = f_uv
        else:
            flow = flow_matrix[u][v] if (u < len(flow_matrix) and v < len(flow_matrix[u])) else 0

        xu, yu, xv, yv = coords[u][0], coords[u][1], coords[v][0], coords[v][1]

        is_saturated = (flow == cap and cap > 0)
        is_active = (0 < flow < cap)
        is_cut = (u, v) in cut_set or (is_orig_undirected and (v, u) in cut_set)

        has_rev = (v, u) in edge_pairs and not is_orig_undirected
        rad = 0.16 if has_rev else 0.0

        if is_saturated:
            edge_color = "#d32f2f"
            lw = 2.8
            ls = "-"
            alpha = 1.0
            zorder_edge = 4
        elif is_active:
            edge_color = "#1976d2"
            lw = 2.2
            ls = "-"
            alpha = 0.95
            zorder_edge = 3
        else:
            edge_color = "#b0bec5"
            lw = 1.0
            ls = "--"
            alpha = 0.55
            zorder_edge = 1

        shrink_val = max(10, int(node_radius * 0.95))
        arrowstyle = "->" if not is_orig_undirected else "-"
        conn = f"arc3,rad={rad}"

        ax.annotate(
            "", xy=(xv, yv), xytext=(xu, yu),
            arrowprops=dict(
                arrowstyle=arrowstyle,
                color=edge_color,
                lw=lw,
                linestyle=ls,
                alpha=alpha,
                shrinkA=shrink_val,
                shrinkB=shrink_val,
                mutation_scale=14,
                connectionstyle=conn
            ),
            zorder=zorder_edge
        )

        mx, my = (xu + xv) / 2.0, (yu + yv) / 2.0
        if rad != 0.0:
            dx, dy = xv - xu, yv - yu
            dist = math.hypot(dx, dy)
            if dist > 0:
                nx, ny = -dy / dist, dx / dist
                offset = rad * dist * 0.5
                mx += nx * offset
                my += ny * offset

        lbl_text = f"{flow}/{cap}"
        show_label = (flow > 0 or is_cut or g.n <= 8)
        if show_label:
            if is_cut:
                lbl_text = f"✂ {flow}/{cap}"
                box_props = dict(boxstyle="round,pad=0.25", facecolor="#fff8e1", edgecolor="#f57f17", linewidth=1.8, alpha=0.95)
                text_color = "#b71c1c"
                fontweight = "bold"
            elif is_saturated:
                box_props = dict(boxstyle="round,pad=0.2", facecolor="#ffebee", edgecolor="#e57373", linewidth=1.2, alpha=0.95)
                text_color = "#b71c1c"
                fontweight = "bold"
            elif is_active:
                box_props = dict(boxstyle="round,pad=0.2", facecolor="#e3f2fd", edgecolor="#64b5f6", linewidth=1.0, alpha=0.95)
                text_color = "#0d47a1"
                fontweight = "bold"
            else:
                box_props = dict(boxstyle="round,pad=0.15", facecolor="#f5f5f5", edgecolor="#cfd8dc", linewidth=0.6, alpha=0.8)
                text_color = "#78909c"
                fontweight = "normal"

            ax.text(mx, my, lbl_text, fontsize=8 if g.n > 10 else 9, fontweight=fontweight,
                    color=text_color, ha="center", va="center", bbox=box_props, zorder=5)

    node_colors, node_labels = {}, {}
    for i in range(g.n):
        if i == source:
            node_colors[i], node_labels[i] = "#00e676", f"{i}\n(S)"
        elif i == sink:
            node_colors[i], node_labels[i] = "#ff3d00", f"{i}\n(T)"
        else:
            node_colors[i], node_labels[i] = "#cfd8dc", str(i)

    _draw_base_nodes(ax, coords, node_radius, node_font, colors=node_colors, labels=node_labels)

    legend_elements = [
        Line2D([0], [0], color="#d32f2f", lw=2.5, label="Bão hòa (flow = cap)"),
        Line2D([0], [0], color="#1976d2", lw=2.0, label="Có luồng (0 < flow < cap)"),
        Line2D([0], [0], color="#b0bec5", lw=1.2, linestyle="--", label="Không có luồng (0/cap)"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor="#fff8e1", markeredgecolor="#f57f17",
               markersize=10, label="Lát cắt hẹp nhất (✂ Min-Cut)"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#00e676", markersize=10, label="Điểm phát S (Source)"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#ff3d00", markersize=10, label="Điểm thu T (Sink)"),
    ]
    ax.legend(handles=legend_elements, loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=3,
              fontsize=8 if g.n > 10 else 9, framealpha=0.95, facecolor="#ffffff", edgecolor="#b0bec5")

    plt.title(f"LUỒNG CỰC ĐẠI TRONG MẠNG (MAX FLOW = {max_flow}) & LÁT CẮT HẸP NHẤT", fontsize=12, fontweight="bold", pad=20)
    margin = max_R * 1.15
    ax.set_aspect("equal")
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin, margin)
    plt.axis("off")
    return _handle_save_and_show(fig, filename, show)

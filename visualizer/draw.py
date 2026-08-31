import math
import os
import subprocess
import matplotlib.pyplot as plt


def compute_smart_layout(n):
    coords = {}
    if n <= 8:
        R = 10
        for i in range(n):
            theta = (2 * math.pi * i) / n if n > 0 else 0
            coords[i] = (R * math.cos(theta), R * math.sin(theta))
        return coords, R, 0.9, 11, 9, (8, 8)
    elif n == 15:
        R_out = 16
        R_in = 8
        for i in range(10):
            theta = (2 * math.pi * i) / 10
            coords[i] = (R_out * math.cos(theta), R_out * math.sin(theta))
        for i in range(5):
            theta = (2 * math.pi * i) / 5 + (math.pi / 10)
            coords[10 + i] = (R_in * math.cos(theta), R_in * math.sin(theta))
        return coords, R_out, 0.85, 10, 8.5, (10, 10)
    elif n == 30:
        R1, R2, R3 = 22, 13, 5.5
        for i in range(16):
            theta = (2 * math.pi * i) / 16
            coords[i] = (R1 * math.cos(theta), R1 * math.sin(theta))
        for i in range(10):
            theta = (2 * math.pi * i) / 10 + (math.pi / 16)
            coords[16 + i] = (R2 * math.cos(theta), R2 * math.sin(theta))
        for i in range(4):
            theta = (2 * math.pi * i) / 4 + (math.pi / 8)
            coords[26 + i] = (R3 * math.cos(theta), R3 * math.sin(theta))
        return coords, R1, 0.75, 8.5, 7.5, (13, 13)
    else:
        num_layers = max(1, math.ceil(n / 10))
        R_max = max(12, n * 0.7)
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
        return coords, R_max, 0.7, 9, 8, (11, 11)


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
    plt.savefig(filename, dpi=300, bbox_inches="tight", facecolor="#fafafa")
    if show:
        try:
            if os.name == "posix":
                cmd = "open" if "darwin" in os.sys.platform else "xdg-open"
                subprocess.Popen([cmd, filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif os.name == "nt":
                os.startfile(filename)
        except Exception:
            plt.show(block=False)
            plt.pause(0.5)
    plt.close(fig)


def draw(g_or_n, edges=None, directed=False, filename="current_graph.png", highlight=None, colors=None, show=True):
    if hasattr(g_or_n, "n"):
        n = g_or_n.n
        edges_list = getattr(g_or_n, "edges", [])
        is_directed = getattr(g_or_n, "directed", False)
    else:
        n = int(g_or_n)
        edges_list = edges if edges is not None else []
        is_directed = directed

    if highlight is None:
        highlight = []
    if colors is None:
        colors = {}

    coords, max_R, node_radius, node_font, weight_font, fig_size = compute_smart_layout(n)
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
        line_width = 2.8 if is_highlighted else 1.1
        z_order = 3 if is_highlighted else 1
        rad = 0.07 if is_directed else 0.0

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

        if w != 1:
            mid_x, mid_y = (x_u + x_v) / 2, (y_u + y_v) / 2
            ax.text(
                mid_x, mid_y, str(w),
                fontsize=weight_font, fontweight="bold",
                color="#1565C0" if not is_highlighted else "#B71C1C",
                ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="#ffffff", edgecolor="#CFD8DC", alpha=0.92, lw=0.6),
                zorder=4,
            )

    _draw_base_nodes(ax, coords, node_radius, node_font, colors=colors, default_color="#2E7D32")
    margin = max_R * 1.15
    ax.set_aspect("equal")
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin, margin)
    plt.axis("off")
    _handle_save_and_show(fig, filename, show)


draw_graph = draw


def draw_euler(g, path, edges_order, filename="euler_path.png", show=True):
    coords, max_R, node_radius, node_font, _, fig_size = compute_smart_layout(g.n)
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
    _handle_save_and_show(fig, filename, show)


def draw_mst(g, mst_edges, total_weight, filename="mst_result.png", show=True):
    coords, max_R, node_radius, node_font, _, fig_size = compute_smart_layout(g.n)
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

        if (u, v) in mst_set:
            ax.plot([xu, xv], [yu, yv], color="#2979ff", linewidth=3.0, zorder=2)
            mid_x, mid_y = (xu + xv) / 2, (yu + yv) / 2
            ax.text(mid_x, mid_y, str(w), fontsize=9, fontweight="bold", color="#2979ff", ha="center", va="center", bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#2979ff", alpha=0.9), zorder=4)
        else:
            ax.plot([xu, xv], [yu, yv], color="#90a4ae", linestyle="--", linewidth=1.2, zorder=1)
            mid_x, mid_y = (xu + xv) / 2, (yu + yv) / 2
            ax.text(mid_x, mid_y, str(w), fontsize=8, color="#90a4ae", ha="center", va="center", bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.7), zorder=3)

    _draw_base_nodes(ax, coords, node_radius, node_font, default_color="#2979ff")
    plt.title(f"CÂY KHUNG NHỎ NHẤT (MST) – Tổng trọng số = {total_weight}", fontsize=13, fontweight="bold", pad=20)
    margin = max_R * 1.15
    ax.set_aspect("equal")
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin, margin)
    plt.axis("off")
    _handle_save_and_show(fig, filename, show)


def draw_max_flow(g, flow_matrix, min_cut_edges, max_flow, source, sink, filename="max_flow.png", show=True):
    coords, max_R, node_radius, node_font, _, fig_size = compute_smart_layout(g.n)
    fig, ax = plt.subplots(figsize=fig_size, facecolor="#fafafa")
    ax.set_facecolor("#fafafa")

    cut_set = set((e[0], e[1]) for e in min_cut_edges)

    for edge in g.edges:
        u, v = edge[0], edge[1]
        cap = edge[2] if len(edge) > 2 else 0
        flow = flow_matrix[u][v] if (u < len(flow_matrix) and v < len(flow_matrix[u])) else 0
        xu, yu, xv, yv = coords[u][0], coords[u][1], coords[v][0], coords[v][1]

        is_saturated = (flow == cap and cap > 0)
        is_cut = (u, v) in cut_set
        edge_color = "#d50000" if is_saturated else "#78909c"
        lw = 2.8 if is_saturated else 1.2

        ax.annotate("", xy=(xv, yv), xytext=(xu, yu), arrowprops=dict(arrowstyle="->", color=edge_color, lw=lw, shrinkA=12, shrinkB=12, mutation_scale=15), zorder=2)

        mid_x, mid_y = (xu + xv) / 2, (yu + yv) / 2
        box_props = dict(boxstyle="round,pad=0.2", facecolor="#ffebee" if is_saturated else "white", edgecolor="#e91e63" if is_cut else "none", linewidth=1.8 if is_cut else 0, alpha=0.9)
        ax.text(mid_x, mid_y, f"{flow}/{cap}", fontsize=9, fontweight="bold", color="#d50000" if is_saturated else "#37474f", ha="center", va="center", bbox=box_props, zorder=4)

    node_colors, node_labels = {}, {}
    for i in range(g.n):
        if i == source:
            node_colors[i], node_labels[i] = "#00e5ff", f"{i}\n(S)"
        elif i == sink:
            node_colors[i], node_labels[i] = "#ff3d00", f"{i}\n(T)"
        else:
            node_colors[i], node_labels[i] = "#b0bec5", str(i)

    _draw_base_nodes(ax, coords, node_radius, node_font, colors=node_colors, labels=node_labels)
    plt.title(f"LUỒNG CỰC ĐẠI TRONG MẠNG (MAX FLOW = {max_flow}) & LÁT CẮT HẸP NHẤT", fontsize=12, fontweight="bold", pad=20)
    margin = max_R * 1.15
    ax.set_aspect("equal")
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin, margin)
    plt.axis("off")
    _handle_save_and_show(fig, filename, show)
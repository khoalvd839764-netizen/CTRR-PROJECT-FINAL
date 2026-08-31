import math
import matplotlib.pyplot as plt


def _get_coords(n):
    coords = {}
    for i in range(n):
        theta = (2 * math.pi * i) / n if n > 0 else 0
        x = 10 * math.cos(theta)
        y = 10 * math.sin(theta)
        coords[i] = (x, y)
    return coords


def _draw_base_nodes(ax, coords, colors=None, labels=None, default_color="green"):
    if colors is None:
        colors = {}
    if labels is None:
        labels = {}

    node_radius = 0.8
    for i, (x, y) in coords.items():
        node_color = colors.get(i, default_color)
        circle = plt.Circle((x, y), node_radius, color=node_color, zorder=5)
        ax.add_patch(circle)

        text_label = labels.get(i, str(i))
        ax.text(
            x,
            y,
            text_label,
            color="white",
            fontweight="bold",
            fontsize=10,
            ha="center",
            va="center",
            zorder=6,
        )

def draw(g_or_n, edges=None, directed=False, filename="test_graph.png", highlight=None, colors=None):
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

    coords = _get_coords(n)
    fig, ax = plt.subplots(figsize=(8, 8))

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

        edge_color = "red" if is_highlighted else "gray"
        line_width = 2.5 if is_highlighted else 1.0
        z_order = 2 if is_highlighted else 1

        if not is_directed:
            ax.plot([x_u, x_v], [y_u, y_v], color=edge_color, linewidth=line_width, zorder=z_order)
        else:
            ax.annotate(
                "",
                xy=(x_v, y_v),
                xytext=(x_u, y_u),
                arrowprops=dict(
                    arrowstyle="->",
                    color=edge_color,
                    lw=line_width,
                    shrinkA=12,
                    shrinkB=12,
                    mutation_scale=15,
                ),
                zorder=z_order,
            )

        if w != 1:
            mid_x = (x_u + x_v) / 2
            mid_y = (y_u + y_v) / 2
            ax.text(
                mid_x,
                mid_y,
                str(w),
                fontsize=9,
                fontweight="bold",
                color="black",
                ha="center",
                va="center",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.85),
                zorder=3,
            )

    _draw_base_nodes(ax, coords, colors=colors, default_color="green")

    ax.set_aspect("equal")
    ax.set_xlim(-13, 13)
    ax.set_ylim(-13, 13)
    plt.axis("off")

    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close(fig)


draw_graph = draw


def draw_euler(g, path, edges_order, filename="euler_path.png"):
    coords = _get_coords(g.n)
    fig, ax = plt.subplots(figsize=(8, 8))

    for edge in g.edges:
        u, v = edge[0], edge[1]
        xu, yu = coords[u]
        xv, yv = coords[v]
        if not g.directed:
            ax.plot([xu, xv], [yu, yv], color="#cfd8dc", linewidth=1.5, zorder=1)
        else:
            ax.annotate(
                "",
                xy=(xv, yv),
                xytext=(xu, yu),
                arrowprops=dict(
                    arrowstyle="->",
                    color="#cfd8dc",
                    lw=1.5,
                    shrinkA=12,
                    shrinkB=12,
                    mutation_scale=12,
                ),
                zorder=1,
            )

    for step, edge in enumerate(edges_order, 1):
        u, v = edge[0], edge[1]
        xu, yu = coords[u]
        xv, yv = coords[v]

        if not g.directed:
            ax.plot([xu, xv], [yu, yv], color="#ff5722", linewidth=2.5, zorder=2)
        else:
            ax.annotate(
                "",
                xy=(xv, yv),
                xytext=(xu, yu),
                arrowprops=dict(
                    arrowstyle="->",
                    color="#ff5722",
                    lw=2.5,
                    shrinkA=12,
                    shrinkB=12,
                    mutation_scale=15,
                ),
                zorder=2,
            )

        mid_x = (xu + xv) / 2
        mid_y = (yu + yv) / 2
        ax.text(
            mid_x,
            mid_y,
            str(step),
            fontsize=9,
            fontweight="bold",
            color="#ff5722",
            ha="center",
            va="center",
            bbox=dict(boxstyle="circle,pad=0.2", facecolor="white", edgecolor="#ff5722", alpha=0.9),
            zorder=4,
        )

    node_colors = {}
    if path:
        node_colors[path[0]] = "#00e676"
        node_colors[path[-1]] = "#d50000"

    _draw_base_nodes(ax, coords, colors=node_colors, default_color="#78909c")

    ax.set_aspect("equal")
    ax.set_xlim(-13, 13)
    ax.set_ylim(-13, 13)
    plt.axis("off")

    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close(fig)


def draw_mst(g, mst_edges, total_weight, filename="mst_result.png"):
    coords = _get_coords(g.n)
    fig, ax = plt.subplots(figsize=(8, 8))

    mst_set = set()
    for e in mst_edges:
        mst_set.add((e[0], e[1]))
        mst_set.add((e[1], e[0]))

    for edge in g.edges:
        u, v = edge[0], edge[1]
        w = edge[2] if len(edge) > 2 else 1
        xu, yu = coords[u]
        xv, yv = coords[v]

        is_in_mst = (u, v) in mst_set

        if is_in_mst:
            ax.plot([xu, xv], [yu, yv], color="#2979ff", linewidth=3.0, zorder=2)
            mid_x = (xu + xv) / 2
            mid_y = (yu + yv) / 2
            ax.text(
                mid_x,
                mid_y,
                str(w),
                fontsize=9,
                fontweight="bold",
                color="#2979ff",
                ha="center",
                va="center",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#2979ff", alpha=0.9),
                zorder=4,
            )
        else:
            ax.plot([xu, xv], [yu, yv], color="#90a4ae", linestyle="--", linewidth=1.2, zorder=1)
            mid_x = (xu + xv) / 2
            mid_y = (yu + yv) / 2
            ax.text(
                mid_x,
                mid_y,
                str(w),
                fontsize=8,
                color="#90a4ae",
                ha="center",
                va="center",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.7),
                zorder=3,
            )

    _draw_base_nodes(ax, coords, default_color="#2979ff")

    plt.title(f"CÂY KHUNG NHỎ NHẤT (MST) – Tổng trọng số = {total_weight}", fontsize=13, fontweight="bold", pad=20)

    ax.set_aspect("equal")
    ax.set_xlim(-13, 13)
    ax.set_ylim(-13, 13)
    plt.axis("off")

    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close(fig)


def draw_max_flow(g, flow_matrix, min_cut_edges, max_flow, source, sink, filename="max_flow.png"):
    coords = _get_coords(g.n)
    fig, ax = plt.subplots(figsize=(9, 9))

    cut_set = set()
    for e in min_cut_edges:
        cut_set.add((e[0], e[1]))

    for edge in g.edges:
        u, v = edge[0], edge[1]
        cap = edge[2] if len(edge) > 2 else 0
        flow = flow_matrix[u][v] if (u < len(flow_matrix) and v < len(flow_matrix[u])) else 0

        xu, yu = coords[u]
        xv, yv = coords[v]

        is_saturated = (flow == cap and cap > 0)
        is_cut = (u, v) in cut_set

        edge_color = "#d50000" if is_saturated else "#78909c"
        lw = 2.8 if is_saturated else 1.2

        ax.annotate(
            "",
            xy=(xv, yv),
            xytext=(xu, yu),
            arrowprops=dict(
                arrowstyle="->",
                color=edge_color,
                lw=lw,
                shrinkA=12,
                shrinkB=12,
                mutation_scale=15,
            ),
            zorder=2,
        )

        mid_x = (xu + xv) / 2
        mid_y = (yu + yv) / 2
        label_text = f"{flow}/{cap}"

        box_props = dict(
            boxstyle="round,pad=0.2",
            facecolor="#ffebee" if is_saturated else "white",
            edgecolor="#e91e63" if is_cut else "none",
            linewidth=1.8 if is_cut else 0,
            alpha=0.9,
        )

        ax.text(
            mid_x,
            mid_y,
            label_text,
            fontsize=9,
            fontweight="bold",
            color="#d50000" if is_saturated else "#37474f",
            ha="center",
            va="center",
            bbox=box_props,
            zorder=4,
        )

    node_colors = {}
    node_labels = {}

    for i in range(g.n):
        if i == source:
            node_colors[i] = "#00e5ff"
            node_labels[i] = f"{i}\n(S)"
        elif i == sink:
            node_colors[i] = "#ff3d00"
            node_labels[i] = f"{i}\n(T)"
        else:
            node_colors[i] = "#b0bec5"
            node_labels[i] = str(i)

    _draw_base_nodes(ax, coords, colors=node_colors, labels=node_labels)

    plt.title(f"LUỒNG CỰC ĐẠI TRONG MẠNG (MAX FLOW = {max_flow}) & LÁT CẮT HẸP NHẤT", fontsize=12, fontweight="bold", pad=20)

    ax.set_aspect("equal")
    ax.set_xlim(-13, 13)
    ax.set_ylim(-13, 13)
    plt.axis("off")

    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close(fig)
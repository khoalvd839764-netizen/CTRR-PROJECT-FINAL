import math
import matplotlib.pyplot as plt


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

    coords = {}
    for i in range(n):
        theta = (2 * math.pi * i) / n if n > 0 else 0
        x = 10 * math.cos(theta)
        y = 10 * math.sin(theta)
        coords[i] = (x, y)

    fig, ax = plt.subplots(figsize=(8, 8))
    node_radius = 0.8

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

    for i in range(n):
        x, y = coords[i]
        node_color = colors.get(i, "green")

        circle = plt.Circle((x, y), node_radius, color=node_color, zorder=4)
        ax.add_patch(circle)

        ax.text(
            x,
            y,
            str(i),
            color="white",
            fontweight="bold",
            fontsize=11,
            ha="center",
            va="center",
            zorder=5,
        )

    ax.set_aspect("equal")
    ax.set_xlim(-13, 13)
    ax.set_ylim(-13, 13)
    plt.axis("off")

    # 4. Lưu file
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close(fig)

draw_graph = draw
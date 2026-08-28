import math
import os
import subprocess
import matplotlib.pyplot as plt


def compute_smart_layout(n):
    """
    Tự động tính toán tọa độ các đỉnh theo bố cục đa tầng đồng tâm (Concentric Rings)
    để các đỉnh không bao giờ bị đè lên nhau, hình vẽ thoáng đãng và đẹp mắt nhất.
    """
    coords = {}
    
    # 1. Đồ thị nhỏ (<= 8 đỉnh): 1 vòng tròn đơn
    if n <= 8:
        R = 10
        for i in range(n):
            theta = (2 * math.pi * i) / n
            coords[i] = (R * math.cos(theta), R * math.sin(theta))
        return coords, R, 0.9, 11, 9, (8, 8)

    # 2. Đồ thị 15 đỉnh: Bố cục 2 vòng đồng tâm (10 đỉnh vòng ngoài + 5 đỉnh vòng trong)
    elif n == 15:
        R_out = 16
        R_in = 8
        # 10 đỉnh vòng ngoài (0 -> 9)
        for i in range(10):
            theta = (2 * math.pi * i) / 10
            coords[i] = (R_out * math.cos(theta), R_out * math.sin(theta))
        # 5 đỉnh vòng trong (10 -> 14)
        for i in range(5):
            theta = (2 * math.pi * i) / 5 + (math.pi / 10)  # Lệch góc một chút cho đẹp
            coords[10 + i] = (R_in * math.cos(theta), R_in * math.sin(theta))
        return coords, R_out, 0.85, 10, 8.5, (10, 10)

    # 3. Đồ thị 30 đỉnh: Bố cục 3 tầng đô thị (16 đỉnh ngoài + 10 đỉnh giữa + 4 đỉnh lõi)
    elif n == 30:
        R1 = 22  # Tầng 1: Vòng ngoài cùng
        R2 = 13  # Tầng 2: Vòng giữa
        R3 = 5.5 # Tầng 3: Cụm lõi trung tâm
        
        # 16 đỉnh vòng ngoài (0 -> 15)
        for i in range(16):
            theta = (2 * math.pi * i) / 16
            coords[i] = (R1 * math.cos(theta), R1 * math.sin(theta))
            
        # 10 đỉnh vòng giữa (16 -> 25)
        for i in range(10):
            theta = (2 * math.pi * i) / 10 + (math.pi / 16)
            coords[16 + i] = (R2 * math.cos(theta), R2 * math.sin(theta))
            
        # 4 đỉnh cụm lõi (26 -> 29)
        for i in range(4):
            theta = (2 * math.pi * i) / 4 + (math.pi / 8)
            coords[26 + i] = (R3 * math.cos(theta), R3 * math.sin(theta))
            
        return coords, R1, 0.75, 8.5, 7.5, (13, 13)

    # 4. Đồ thị số đỉnh bất kỳ: Tự động chia tầng thông minh
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


def draw(g_or_n, edges=None, directed=False, filename="current_graph.png", highlight=None, colors=None, show=True):
    # =========================================================================
    # [1. NHẬN DIỆN THAM SỐ ĐẦU VÀO ĐA HÌNH]
    # =========================================================================
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

    # =========================================================================
    # [⭐ NÂNG CẤP: TÍNH TỌA ĐỘ ĐA TẦNG THÔNG MINH - CHỐNG ĐÈ 100%]
    # =========================================================================
    coords, max_R, node_radius, node_font, weight_font, fig_size = compute_smart_layout(n)

    fig, ax = plt.subplots(figsize=fig_size, facecolor='#fafafa')
    ax.set_facecolor('#fafafa')

    # =========================================================================
    # [2. VẼ CÁC CẠNH VÀ MŨI TÊN CÓ HƯỚNG]
    # =========================================================================
    for edge in edges_list:
        u, v = edge[0], edge[1]
        w = edge[2] if len(edge) > 2 else 1

        x_u, y_u = coords[u]
        x_v, y_v = coords[v]

        # Kiểm tra highlight
        is_highlighted = (
            (u, v) in highlight
            or (u, v, w) in highlight
            or (not is_directed and ((v, u) in highlight or (v, u, w) in highlight))
        )

        edge_color = "#E53935" if is_highlighted else "#78909C"
        line_width = 2.8 if is_highlighted else 1.1
        z_order = 3 if is_highlighted else 1
        
        # Độ cong nhẹ cho mũi tên
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

        # Ghi nhãn trọng số
        if w != 1:
            mid_x = (x_u + x_v) / 2
            mid_y = (y_u + y_v) / 2
            
            # Căn chỉnh vị trí nhãn để không đè lên cạnh khác
            ax.text(
                mid_x,
                mid_y,
                str(w),
                fontsize=weight_font,
                fontweight="bold",
                color="#1565C0" if not is_highlighted else "#B71C1C",
                ha="center",
                va="center",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="#ffffff", edgecolor="#CFD8DC", alpha=0.92, lw=0.6),
                zorder=4,
            )

    # =========================================================================
    # [3. VẼ CÁC ĐỈNH HÌNH TRÒN]
    # =========================================================================
    for i in range(n):
        x, y = coords[i]
        node_color = colors.get(i, "#2E7D32")

        circle = plt.Circle((x, y), node_radius, color=node_color, ec="#1B5E20", lw=1.2, zorder=5)
        ax.add_patch(circle)

        ax.text(
            x,
            y,
            str(i),
            color="white",
            fontweight="bold",
            fontsize=node_font,
            ha="center",
            va="center",
            zorder=6,
        )

    # =========================================================================
    # [4. CĂN BIÊN MÀN HÌNH TỰ ĐỘNG]
    # =========================================================================
    margin = max_R * 1.15
    ax.set_aspect("equal")
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin, margin)
    plt.axis("off")

    # 5. Lưu file ảnh chất lượng cao
    plt.savefig(filename, dpi=300, bbox_inches="tight", facecolor='#fafafa')
    
    # 6. Tự động hiển thị ảnh lên màn hình
    if show:
        try:
            if os.name == 'posix':
                cmd = 'open' if 'darwin' in os.sys.platform else 'xdg-open'
                subprocess.Popen([cmd, filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif os.name == 'nt':
                os.startfile(filename)
        except Exception:
            plt.show(block=False)
            plt.pause(0.5)

    plt.close(fig)

draw_graph = draw

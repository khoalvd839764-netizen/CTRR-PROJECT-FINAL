import math
import os
import subprocess
import matplotlib.pyplot as plt

# Thư mục mặc định lưu ảnh kết quả: nằm ở thư mục "results" ngang cấp với thư mục cha của file hiện tại
DEFAULT_RESULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results"))


def _resolve_filepath(filename):
    """
    Chuẩn hóa và tạo đường dẫn đầy đủ đến file kết quả.
    Đảm bảo thư mục lưu trữ luôn tồn tại trước khi ghi file.
    """
    if not os.path.isabs(filename):
        dirname = os.path.dirname(filename)
        if not dirname:
            # Nếu chỉ truyền tên file (không có đường dẫn), lưu vào thư mục DEFAULT_RESULT_DIR
            filename = os.path.join(DEFAULT_RESULT_DIR, filename)
        elif not filename.startswith("results") and not filename.startswith("./results"):
            # Nếu đường dẫn không bắt đầu bằng 'results', lấy tên file đưa vào DEFAULT_RESULT_DIR
            filename = os.path.join(DEFAULT_RESULT_DIR, os.path.basename(filename))
        else:
            filename = os.path.abspath(filename)
            
    # Tạo thư mục chứa file nếu chưa tồn tại
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    return filename


def compute_smart_layout(g_or_n):
    """
    Tự động tính toán tọa độ (layout) và các thông số hiển thị cho đồ thị.
    Hỗ trợ:
      - Nhận vào đối tượng đồ thị g (có thuộc tính .n, .pos, .edges) hoặc số lượng đỉnh n.
      - Sử dụng tọa độ thủ công nếu có sẵn (g.pos).
      - Sử dụng giải thuật lực lò xo (spring layout qua networkx) nếu có cạnh.
      - Bố trí hình tròn / đồng tâm theo số lượng đỉnh (n <= 8, 15, 20, 30,...) nếu không có thư viện ngoài.
    
    Trả về: (coords, R_max, node_radius, node_font, weight_font, fig_size)
    """
    import math
    
    # Xác định số lượng đỉnh n
    n = g_or_n.n if hasattr(g_or_n, 'n') else g_or_n
    
    # Thiết lập kích thước đồ họa dựa theo quy mô số đỉnh
    if n <= 8:
        R_max, node_radius, node_font, weight_font, fig_size = 10, 0.9, 11, 9, (8, 8)
    elif n == 15:
        R_4max, node_radius, node_font, weight_font, fig_size = 16, 0.85, 10, 8.5, (10, 10)
        R_max = 16
    elif n == 20:
        R_max, node_radius, node_font, weight_font, fig_size = 19.0, 0.85, 10, 8.5, (14, 11)
    elif n == 30:
        R_max, node_radius, node_font, weight_font, fig_size = 22, 0.75, 8.5, 7.5, (13, 13)
    else:
        R_max, node_radius, node_font, weight_font, fig_size = max(12, n * 0.7), 0.7, 9, 8, (11, 11)

    # Trường hợp 1: Đồ thị đã định nghĩa sẵn tọa độ (pos) cho từng đỉnh
    if hasattr(g_or_n, 'pos') and isinstance(g_or_n.pos, dict) and len(g_or_n.pos) == n:
        xs = [pt[0] for pt in g_or_n.pos.values()]
        ys = [pt[1] for pt in g_or_n.pos.values()]
        if xs and ys:
            max_coord = max(max(abs(x) for x in xs), max(abs(y) for y in ys))
            R_max = max(R_max, max_coord)
        return dict(g_or_n.pos), R_max, node_radius, node_font, weight_font, fig_size

    # Trường hợp 2: Bố trí bằng Spring Layout (NetworkX) nếu có danh sách cạnh
    if hasattr(g_or_n, 'edges') and len(g_or_n.edges) > 0:
        try:
            import networkx as nx
            G = nx.Graph()
            for edge in g_or_n.edges:
                u, v = edge[0], edge[1]
                w = edge[2] if len(edge) > 2 else 1
                w_val = float(w)
                # Trọng số càng lớn thì lực hút càng gần (nghịch đảo trọng số)
                inv_w = 1.0 / max(0.1, w_val)
                G.add_edge(u, v, weight=inv_w)
            
            for i in range(n):
                G.add_node(i)

            # Tính tọa độ theo mô hình đàn hồi
            pos = nx.spring_layout(G, weight='weight', seed=42, iterations=150)
            coords = {i: (pos[i][0] * R_max, pos[i][1] * R_max) for i in range(n)}
            return coords, R_max, node_radius, node_font, weight_font, fig_size
        except ImportError:
            pass  # Nếu chưa cài networkx, tiếp tục xuống thuật toán dự phòng

    # Trường hợp 3: Bố trí hình học mặc định (vòng tròn / đa giác đều)
    coords = {}
    if n <= 8:
        # Bố trí trên 1 vòng tròn đều
        for i in range(n):
            theta = (2 * math.pi * i) / n if n > 0 else 0
            coords[i] = (R_max * math.cos(theta), R_max * math.sin(theta))
    elif n == 15:
        # Bố trí 2 vòng tròn: 10 đỉnh vòng ngoài, 5 đỉnh vòng trong
        for i in range(10):
            theta = (2 * math.pi * i) / 10
            coords[i] = (16 * math.cos(theta), 16 * math.sin(theta))
        for i in range(5):
            theta = (2 * math.pi * i) / 5 + (math.pi / 10)
            coords[10 + i] = (8 * math.cos(theta), 8 * math.sin(theta))
    elif n == 20:
        # Tọa độ cố định theo cấu trúc phân tầng định sẵn
        coords = {
            0: (-16.0, 5.0),   1: (-16.0, -5.0),
            2: (-10.5, 12.0),  3: (-10.0, 4.0),   4: (-10.0, -4.0),   5: (-10.5, -12.0),
            6: (-3.5, 14.5),   7: (-3.0, 6.5),    8: (-3.0, -1.5),    9: (-3.0, -8.5),   10: (-3.5, -15.0),
            11: (4.0, 13.5),   12: (4.0, 5.5),    13: (4.0, -2.5),    14: (4.0, -9.5),   15: (4.0, -15.5),
            16: (11.0, 9.5),   17: (11.0, 1.0),   18: (11.0, -8.0),
            19: (17.0, 0.0)
        }
    elif n == 30:
        # Bố trí 3 vòng tròn đồng tâm: ngoài (16), giữa (10), trong cùng (4)
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
        # n tổng quát: chia thành nhiều tầng vòng tròn đồng tâm
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
                    
    # Cập nhật lại bán kính tối đa R_max dựa trên tọa độ thực tế
    xs = [pt[0] for pt in coords.values()]
    ys = [pt[1] for pt in coords.values()]
    if xs and ys:
        max_coord = max(max(abs(x) for x in xs), max(abs(y) for y in ys))
        R_max = max(R_max, max_coord)
        
    return coords, R_max, node_radius, node_font, weight_font, fig_size


def _draw_base_nodes(ax, coords, node_radius, node_font, colors=None, labels=None, default_color="#2E7D32"):
    """
    Hàm phụ trợ vẽ các hình tròn đại diện cho đỉnh và nhãn số/chữ bên trong đỉnh.
    """
    if colors is None:
        colors = {}
    if labels is None:
        labels = {}

    for i, (x, y) in coords.items():
        # Vẽ hình tròn đỉnh
        node_color = colors.get(i, default_color)
        circle = plt.Circle((x, y), node_radius, color=node_color, ec="#1B5E20", lw=1.2, zorder=5)
        ax.add_patch(circle)

        # Hiển thị nhãn của đỉnh (mặc định là chỉ số đỉnh)
        text_label = labels.get(i, str(i))
        ax.text(x, y, text_label, color="white", fontweight="bold", fontsize=node_font, ha="center", va="center", zorder=6)


def _handle_save_and_show(fig, filename, show):
    """
    Lưu figure hiện tại ra file ảnh (.png) và mở trực tiếp bằng phần mềm xem ảnh của hệ điều hành.
    """
    filepath = _resolve_filepath(filename)
    plt.savefig(filepath, dpi=300, bbox_inches="tight", facecolor="#fafafa")
    
    if show:
        try:
            # Mở file bằng trình xem ảnh mặc định của hệ thống
            if os.name == "posix":
                cmd = "open" if "darwin" in os.sys.platform else "xdg-open"
                subprocess.Popen([cmd, filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif os.name == "nt":  # Windows
                os.startfile(filepath)
        except Exception:
            plt.show(block=False)
            plt.pause(0.5)
            
    plt.close(fig)
    return filepath


def draw(g_or_n, edges=None, directed=False, filename="current_graph.png", highlight=None, colors=None, show=True):
    """
    Vẽ đồ thị tổng quát (có hướng hoặc vô hướng, có trọng số hoặc không).
    Hỗ trợ highlight các cạnh và tô màu tùy biến cho các đỉnh.
    """
    # Chuẩn hóa dữ liệu đầu vào
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

    # Lấy layout tọa độ và kích thước
    coords, max_R, node_radius, node_font, weight_font, fig_size = compute_smart_layout(g_or_n)
    fig, ax = plt.subplots(figsize=fig_size, facecolor="#fafafa")
    ax.set_facecolor("#fafafa")

    # Vẽ danh sách các cạnh
    for edge in edges_list:
        u, v = edge[0], edge[1]
        w = edge[2] if len(edge) > 2 else 1
        x_u, y_u = coords[u]
        x_v, y_v = coords[v]

        # Kiểm tra cạnh có nằm trong danh sách highlight cần làm nổi bật không
        is_highlighted = (
            (u, v) in highlight
            or (u, v, w) in highlight
            or (not is_directed and ((v, u) in highlight or (v, u, w) in highlight))
        )

        edge_color = "#E53935" if is_highlighted else "#78909C"
        
        # Điều chỉnh độ dày đường vẽ cạnh dựa theo độ lớn của trọng số w
        import math
        try:
            w_val = float(w)
            dynamic_lw = max(0.8, min(8.0, 0.5 + math.sqrt(w_val) * 0.9))
        except:
            dynamic_lw = 1.2
            
        line_width = (dynamic_lw * 1.6) if is_highlighted else dynamic_lw
        z_order = 3 if is_highlighted else 1
        rad = 0.07 if is_directed else 0.0

        # Vẽ cạnh vô hướng hoặc mũi tên có hướng
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

        # Vẽ trọng số cạnh (nếu trọng số khác 1)
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

    # Vẽ các đỉnh lên trên các cạnh
    _draw_base_nodes(ax, coords, node_radius, node_font, colors=colors, default_color="#2E7D32")
    
    # Căn chỉnh khung hình vẽ
    margin = max_R * 1.15
    ax.set_aspect("equal")
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin, margin)
    plt.axis("off")
    return _handle_save_and_show(fig, filename, show)


# Alias tương thích ngược
draw_graph = draw


def draw_euler(g, path, edges_order, filename="euler_path.png", show=True):
    """
    Vẽ chu trình hoặc đường đi Euler:
      - Làm mờ các cạnh ban đầu.
      - Đánh số thứ tự các bước đi qua từng cạnh bằng màu cam nổi bật.
      - Đỉnh xuất phát màu xanh lục, đỉnh kết thúc màu đỏ.
    """
    coords, max_R, node_radius, node_font, _, fig_size = compute_smart_layout(g)
    fig, ax = plt.subplots(figsize=fig_size, facecolor="#fafafa")
    ax.set_facecolor("#fafafa")

    # 1. Vẽ khung cạnh ban đầu của đồ thị bằng màu nhạt
    for edge in g.edges:
        u, v = edge[0], edge[1]
        xu, yu, xv, yv = coords[u][0], coords[u][1], coords[v][0], coords[v][1]
        if not g.directed:
            ax.plot([xu, xv], [yu, yv], color="#cfd8dc", linewidth=1.5, zorder=1)
        else:
            ax.annotate("", xy=(xv, yv), xytext=(xu, yu), arrowprops=dict(arrowstyle="->", color="#cfd8dc", lw=1.5, shrinkA=12, shrinkB=12, mutation_scale=12), zorder=1)

    # 2. Vẽ các bước đi Euler theo thứ tự duyệt và đánh số bước
    for step, edge in enumerate(edges_order, 1):
        u, v = edge[0], edge[1]
        xu, yu, xv, yv = coords[u][0], coords[u][1], coords[v][0], coords[v][1]
        if not g.directed:
            ax.plot([xu, xv], [yu, yv], color="#ff5722", linewidth=2.5, zorder=2)
        else:
            ax.annotate("", xy=(xv, yv), xytext=(xu, yu), arrowprops=dict(arrowstyle="->", color="#ff5722", lw=2.5, shrinkA=12, shrinkB=12, mutation_scale=15), zorder=2)

        # Hiển thị số thứ tự bước đi (1, 2, 3,...) ngay giữa cạnh
        mid_x, mid_y = (xu + xv) / 2, (yu + yv) / 2
        ax.text(mid_x, mid_y, str(step), fontsize=9, fontweight="bold", color="#ff5722", ha="center", va="center", bbox=dict(boxstyle="circle,pad=0.2", facecolor="white", edgecolor="#ff5722", alpha=0.9), zorder=4)

    # 3. Đánh dấu màu đỉnh đầu và đỉnh cuối
    node_colors = {}
    if path:
        node_colors[path[0]] = "#00e676"   # Xanh lá: đỉnh bắt đầu
        node_colors[path[-1]] = "#d50000"  # Đỏ: đỉnh kết thúc

    _draw_base_nodes(ax, coords, node_radius, node_font, colors=node_colors, default_color="#78909c")
    margin = max_R * 1.15
    ax.set_aspect("equal")
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin, margin)
    plt.axis("off")
    return _handle_save_and_show(fig, filename, show)


def draw_mst(g, mst_edges, total_weight, filename="mst_result.png", show=True):
    """
    Vẽ Cây khung nhỏ nhất (Minimum Spanning Tree - MST):
      - Cạnh thuộc MST được vẽ nét liền màu xanh dương (#2979ff), đậm và nổi bật.
      - Cạnh không thuộc MST vẽ nét đứt màu xám (#90a4ae).
      - Tiêu đề hiển thị tổng trọng số của cây khung.
    """
    coords, max_R, node_radius, node_font, _, fig_size = compute_smart_layout(g)
    fig, ax = plt.subplots(figsize=fig_size, facecolor="#fafafa")
    ax.set_facecolor("#fafafa")

    # Tập hợp các cạnh thuộc MST (cho cả 2 chiều u->v và v->u)
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
            
        mid_x, mid_y = (xu + xv) / 2, (yu + yv) / 2
        
        if (u, v) in mst_set:
            # Cạnh nằm trong MST: nét liền, màu xanh nổi bật
            ax.plot([xu, xv], [yu, yv], color="#2979ff", linewidth=dyn_lw * 1.5, zorder=2)
            ax.text(mid_x, mid_y, str(w), fontsize=9, fontweight="bold", color="#2979ff", ha="center", va="center", bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#2979ff", alpha=0.9), zorder=4)
        else:
            # Cạnh không thuộc MST: nét đứt xám mờ
            ax.plot([xu, xv], [yu, yv], color="#90a4ae", linestyle="--", linewidth=dyn_lw * 0.6, zorder=1)
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
    """
    Vẽ mạng luồng cực đại (Max Flow) và Lát cắt hẹp nhất (Min Cut):
      - Cạnh bão hòa (flow == capacity): màu đỏ đậm (#d50000).
      - Cạnh thuộc lát cắt hẹp nhất (Min-Cut): viền hộp chữ màu hồng cánh sen (#e91e63).
      - Hiển thị tỷ lệ flow/capacity trên từng cung.
      - Đỉnh nguồn (S) màu xanh ngọc, đỉnh đích (T) màu cam đỏ.
    """
    coords, max_R, node_radius, node_font, _, fig_size = compute_smart_layout(g)
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
        
        import math
        try:
            dyn_lw = max(0.8, min(8.0, 0.5 + math.sqrt(float(cap)) * 0.9))
        except:
            dyn_lw = 1.2
        lw = (dyn_lw * 1.5) if is_saturated else dyn_lw

        # Vẽ cung có hướng (mũi tên)
        ax.annotate("", xy=(xv, yv), xytext=(xu, yu), arrowprops=dict(arrowstyle="->", color=edge_color, lw=lw, shrinkA=12, shrinkB=12, mutation_scale=15), zorder=2)

        # Hộp hiển thị giá trị luồng/khả năng thông qua (flow / cap)
        mid_x, mid_y = (xu + xv) / 2, (yu + yv) / 2
        box_props = dict(
            boxstyle="round,pad=0.2",
            facecolor="#ffebee" if is_saturated else "white",
            edgecolor="#e91e63" if is_cut else "none",
            linewidth=1.8 if is_cut else 0,
            alpha=0.9
        )
        ax.text(mid_x, mid_y, f"{flow}/{cap}", fontsize=9, fontweight="bold", color="#d50000" if is_saturated else "#37474f", ha="center", va="center", bbox=box_props, zorder=4)

    # Đánh dấu và đổi màu đỉnh nguồn S, đỉnh đích T
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
    return _handle_save_and_show(fig, filename, show)
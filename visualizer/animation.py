"""
Module: visualizer/animation.py
Trực quan hóa động (Animation) từng bước duyệt đồ thị (DFS / BFS) bằng Matplotlib FuncAnimation.
Hỗ trợ:
  - Hiển thị trực tiếp (Live Animation window)
  - Xuất file ảnh động .GIF (Pillow Writer) để lưu trữ và nộp bài báo cáo.
"""
import math
import os
import subprocess
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from visualizer.draw import compute_smart_layout, _resolve_filepath


def _open_image_safely(filepath):
    try:
        if os.name == "posix":
            cmd = "open" if "darwin" in os.sys.platform else "xdg-open"
            subprocess.Popen([cmd, filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif os.name == "nt":
            os.startfile(filepath)
    except Exception:
        pass


def _generate_dfs_frames(g, start=0):
    """
    Sinh chuỗi các sự kiện từng bước của thuật toán DFS (thăm đỉnh, xét cạnh, quay lui).
    """
    events = []
    visited = [False] * g.n
    stack = []
    order = []
    tree_edges = []

    def dfs_recursive(u, parent=None):
        visited[u] = True
        stack.append(u)
        order.append(u)
        if parent is not None:
            tree_edges.append((parent, u))

        events.append({
            "type": "VISIT",
            "u": u,
            "parent": parent,
            "active_edge": (parent, u) if parent is not None else None,
            "visited": list(visited),
            "stack": list(stack),
            "order": list(order),
            "tree_edges": list(tree_edges),
            "action": f"Bắt đầu duyệt từ đỉnh nguồn {u}" if parent is None else f"Đi theo cạnh ({parent} -> {u}) thăm đỉnh mới {u}"
        })

        for v, _ in g.adj[u]:
            if not visited[v]:
                dfs_recursive(v, u)
                events.append({
                    "type": "BACKTRACK",
                    "u": u,
                    "from_v": v,
                    "active_edge": (v, u),
                    "visited": list(visited),
                    "stack": list(stack),
                    "order": list(order),
                    "tree_edges": list(tree_edges),
                    "action": f"Quay lui (Backtrack) từ đỉnh {v} về lại đỉnh {u}"
                })

        stack.pop()

    dfs_recursive(start)
    
    # Khung hình kết thúc
    events.append({
        "type": "DONE",
        "u": None,
        "parent": None,
        "active_edge": None,
        "visited": list(visited),
        "stack": [],
        "order": list(order),
        "tree_edges": list(tree_edges),
        "action": f"HOÀN THÀNH DUYỆT DFS TOÀN BỘ ĐỒ THỊ ({len(order)} đỉnh đã duyệt)!"
    })

    return events


def _generate_bfs_frames(g, start=0):
    """
    Sinh chuỗi các sự kiện từng bước của thuật toán BFS (Hàng đợi Queue, thăm lân cận).
    """
    events = []
    visited = [False] * g.n
    from collections import deque
    queue = deque([start])
    visited[start] = True
    order = []
    tree_edges = []

    events.append({
        "type": "VISIT",
        "u": start,
        "active_edge": None,
        "visited": list(visited),
        "queue": list(queue),
        "order": list(order),
        "tree_edges": list(tree_edges),
        "action": f"Khởi tạo BFS: Đưa đỉnh nguồn {start} vào Hàng đợi (Queue)"
    })

    while queue:
        u = queue.popleft()
        order.append(u)

        events.append({
            "type": "POP",
            "u": u,
            "active_edge": None,
            "visited": list(visited),
            "queue": list(queue),
            "order": list(order),
            "tree_edges": list(tree_edges),
            "action": f"Lấy đỉnh {u} ra khỏi Queue để duyệt các đỉnh kề"
        })

        for v, _ in g.adj[u]:
            if not visited[v]:
                visited[v] = True
                queue.append(v)
                tree_edges.append((u, v))
                events.append({
                    "type": "ENQUEUE",
                    "u": u,
                    "active_edge": (u, v),
                    "visited": list(visited),
                    "queue": list(queue),
                    "order": list(order),
                    "tree_edges": list(tree_edges),
                    "action": f"Phát hiện đỉnh kề {v} chưa thăm -> Kết nạp cạnh ({u} -> {v}) và đưa {v} vào Queue"
                })

    events.append({
        "type": "DONE",
        "u": None,
        "active_edge": None,
        "visited": list(visited),
        "queue": [],
        "order": list(order),
        "tree_edges": list(tree_edges),
        "action": f"HOÀN THÀNH DUYỆT BFS TOÀN BỘ ĐỒ THỊ ({len(order)} đỉnh đã duyệt)!"
    })

    return events


def animate_traversal(g, method="dfs", start=0, filename=None, fps=1.5, interval=700, show=False):
    """
    Tạo Animation Matplotlib trực quan hóa từng bước duyệt đồ thị (DFS hoặc BFS).
    Lưu kết quả ra file .GIF động.
    """
    if filename is None:
        filename = f"{method.lower()}_animation.gif"
    filepath = _resolve_filepath(filename)

    coords, R, node_r, fs_node, fs_edge, fig_sz = compute_smart_layout(g)
    
    if method.lower() == "dfs":
        frames_data = _generate_dfs_frames(g, start)
        title_prefix = "HOẠT HÌNH TRỰC QUAN HÓA THUẬT TOÁN DFS (DEPTH-FIRST SEARCH)"
    else:
        frames_data = _generate_bfs_frames(g, start)
        title_prefix = "HOẠT HÌNH TRỰC QUAN HÓA THUẬT TOÁN BFS (BREADTH-FIRST SEARCH)"

    fig, ax = plt.subplots(figsize=fig_sz)
    fig.patch.set_facecolor("#0f172a")

    def draw_frame(frame_idx):
        ax.clear()
        ax.set_facecolor("#0f172a")
        
        event = frames_data[frame_idx]
        visited_nodes = event["visited"]
        active_u = event.get("u", None)
        active_edge = event.get("active_edge", None)
        tree_edges_set = set(event["tree_edges"])
        stack_or_queue = event.get("stack", event.get("queue", []))
        order = event["order"]
        action_text = event["action"]

        # 1. Vẽ tất cả các cạnh cơ sở của đồ thị
        seen_undir = set()
        for u, v, w in g.edges:
            if not g.directed:
                canon = tuple(sorted((u, v)))
                if canon in seen_undir:
                    continue
                seen_undir.add(canon)

            x1, y1 = coords[u]
            x2, y2 = coords[v]

            # Kiểm tra xem cạnh có thuộc cây khung duyệt hay đang hoạt động không
            is_active = (active_edge is not None and (
                (u == active_edge[0] and v == active_edge[1]) or
                (not g.directed and u == active_edge[1] and v == active_edge[0])
            ))
            is_in_tree = ((u, v) in tree_edges_set or (not g.directed and (v, u) in tree_edges_set))

            import math
            try:
                dyn_base = max(0.8, min(8.0, 0.5 + math.sqrt(float(w)) * 0.9))
            except:
                dyn_base = 1.2

            if is_active:
                edge_color = "#ff1744"  # Đỏ rực
                lw = dyn_base * 1.8
                ls = "-"
                z = 5
            elif is_in_tree:
                edge_color = "#00e5ff"  # Xanh ngọc phát sáng
                lw = dyn_base * 1.3
                ls = "-"
                z = 4
            else:
                edge_color = "#334155"  # Xám mờ
                lw = dyn_base * 0.6
                ls = "--"
                z = 2

            if g.directed:
                dx = x2 - x1
                dy = y2 - y1
                dist = math.hypot(dx, dy)
                if dist > 0:
                    ux = dx / dist
                    uy = dy / dist
                    sx = x1 + ux * node_r
                    sy = y1 + uy * node_r
                    ex = x2 - ux * (node_r + 0.3)
                    ey = y2 - uy * (node_r + 0.3)
                    ax.annotate(
                        "", xy=(ex, ey), xytext=(sx, sy),
                        arrowprops=dict(
                            arrowstyle="-|>",
                            color=edge_color,
                            lw=lw,
                            mutation_scale=14,
                            linestyle=ls
                        ),
                        zorder=z
                    )
            else:
                ax.plot([x1, x2], [y1, y2], color=edge_color, lw=lw, linestyle=ls, zorder=z)

        # 2. Vẽ tất cả các đỉnh
        for i in range(g.n):
            x, y = coords[i]
            is_active_node = (i == active_u)
            is_in_stack = (i in stack_or_queue)
            is_visited = visited_nodes[i]

            if is_active_node:
                face_col = "#f59e0b"  # Cam vàng nổi bật
                edge_col = "#ffffff"
                glow_r = node_r * 1.3
                ax.add_patch(plt.Circle((x, y), glow_r, color="#f59e0b", alpha=0.35, zorder=6))
                lw_node = 2.5
            elif is_in_stack:
                face_col = "#38bdf8"  # Xanh da trời
                edge_col = "#ffffff"
                lw_node = 2.0
            elif is_visited:
                face_col = "#10b981"  # Xanh lá (Đã duyệt)
                edge_col = "#047857"
                lw_node = 2.0
            else:
                face_col = "#1e293b"  # Chưa duyệt
                edge_col = "#64748b"
                lw_node = 1.5

            circle = plt.Circle((x, y), node_r, facecolor=face_col, edgecolor=edge_col, linewidth=lw_node, zorder=7)
            ax.add_patch(circle)

            text_col = "#0f172a" if (is_active_node or is_in_stack or is_visited) else "#e2e8f0"
            ax.text(x, y, str(i), color=text_col, fontsize=fs_node, fontweight="bold", ha="center", va="center", zorder=8)

        # 3. Tiêu đề & Thông tin tiến trình (HUD)
        ax.set_title(
            f"{title_prefix}\n[Bước {frame_idx + 1}/{len(frames_data)}] — {action_text}",
            fontsize=10.5, fontweight="bold", color="#f8fafc", pad=14
        )

        # 4. Hộp trạng thái ngăn xếp & Thứ tự duyệt
        struct_name = "Ngăn xếp (Stack)" if method.lower() == "dfs" else "Hàng đợi (Queue)"
        status_line_1 = f"• Thứ tự duyệt {method.upper()}: " + (" -> ".join(map(str, order)) if order else "Chưa có")
        status_line_2 = f"• {struct_name}: {stack_or_queue}"

        bbox_hud = dict(boxstyle="round,pad=0.4", facecolor="#1e293b", edgecolor="#475569", lw=1.2, alpha=0.9)
        hud_text = f"{status_line_1}\n{status_line_2}"
        
        limit = R * 1.35
        ax.text(0, -limit * 0.95, hud_text, fontsize=8.5, color="#38bdf8", ha="center", va="center", bbox=bbox_hud, zorder=10)

        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_aspect("equal")
        ax.axis("off")

    # Tạo Animation
    anim = animation.FuncAnimation(fig, draw_frame, frames=len(frames_data), interval=interval, repeat=False)

    print(f"⏳ Đang dựng và xuất Animation ({len(frames_data)} khung hình)...")
    anim.save(filepath, writer="pillow", fps=fps)
    plt.close(fig)

    print(f"🎬 Đã tạo thành công Animation tại: {os.path.relpath(filepath)}")
    _open_image_safely(filepath)
    return filepath


def animate_dfs(g, start=0, filename="dfs_animation.gif", fps=1.5, interval=700, show=False):
    return animate_traversal(g, method="dfs", start=start, filename=filename, fps=fps, interval=interval, show=show)


def animate_bfs(g, start=0, filename="bfs_animation.gif", fps=1.5, interval=700, show=False):
    return animate_traversal(g, method="bfs", start=start, filename=filename, fps=fps, interval=interval, show=show)

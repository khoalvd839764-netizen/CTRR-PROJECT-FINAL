import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from visualizer.draw import draw

print("🧪 KIỂM TRA PHẦN CỦA NHẬT TRƯỜNG (VẼ ĐỒ THỊ):")
edges = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 0, 1)]
draw(4, edges, directed=False, filename="test_graph.png", highlight=[(0, 1)])
print("✅ Đã tạo file test_graph.png thành công! Nhật Trường mở file xem hình vẽ nhé.")
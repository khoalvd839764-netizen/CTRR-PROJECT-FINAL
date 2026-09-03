# chuyển ma trận kề qua danh sách kề
def matrix_to_adj(matrix, directed=False):
    n = len(matrix)
    adj = {i: [] for i in range(n)} # tạo dictionary chạy từ 0 đến n -1 và gắn key là i gắn value bằng list rỗng
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                adj[i].append((j, matrix[i][j]))    
# duyệt ma trận nếu  như có giá trị khác 0 thì add j cạnh ji là giá trị vào list rỗng lúc nãy
    return adj

# ma trận sang qua danh sách cạnh
def matrix_to_edges(matrix, directed=False):
    n = len(matrix)
    edges = []
    for i in range(n):
        start_j = 0 if directed else i # có hướng duyệt hết vô hướng duyệt nữa
        for j in range(start_j, n):
            if matrix[i][j] != 0:
                edges.append((i, j, matrix[i][j]))
                # duyệt ma trận nếu j i có giá trị khác 0 thì add i j tức là 2 đỉnh và ij value vào list cạnh
    return edges

# chuyển danh sách cạnh sang ma trận
def edges_to_matrix(edges, n, directed=False):
    matrix = [[0] * n for _ in range(n)] # tạo list chứ n hàng cột và full value 0 
    for edge in edges:
        u = edge[0]
        v = edge[1]
        # nếu có trọng số thì gắn value đó dô k thì gắn 1 
        weight = edge[2] if len(edge) >= 3 else 1
        matrix[u][v] = weight # tại vị trí u v gán value 
        if not directed:  # nếu vô hướng gán 2 lần ngược lại vì đôi xứng
            matrix[v][u] = weight
    return matrix

# cạnh sang cạnh kề
def edges_to_adj(edges, n, directed=False):
    adj = {i: [] for i in range(n)} # tạo distonory key i value rỗng
    for edge in edges:
        u = edge[0]
        v = edge[1]
        weight = edge[2] if len(edge) >= 3 else 1
        adj[u].append((v, weight)) # add đỉnh và value vào 
        if not directed: # vô hướng 2 lần có hướng 1 lần
            adj[v].append((u, weight))
    return adj

# canh ke sang ma tran
def adj_to_matrix(adj, n):
    matrix = [[0] * n for _ in range(n)] # ma tran full 0 
    for u, neighbors in adj.items():  # u là key nei là cạnh  và value
        for v, weight in neighbors:  # v là cạnh kề với u wei là value tỉ số
            matrix[u][v] = weight  # gắn vô ma trận tương ứng
    return matrix


# canh ke sang to cac canh
def adj_to_edges(adj, directed=False):
    edges = []
    for u, neighbors in adj.items():
        for v, weight in neighbors:
            if directed or u <= v: # dùng để lọc lặp của vô hướng
                edges.append((u, v, weight))
    return edges

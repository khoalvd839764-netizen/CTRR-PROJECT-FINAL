def matrix_to_adj(matrix, directed=False):
    n = len(matrix)
    adj = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                adj[i].append((j, matrix[i][j]))
    return adj

def matrix_to_edges(matrix, directed=False):
    n = len(matrix)
    edges = []
    for i in range(n):
        start_j = 0 if directed else i
        for j in range(start_j, n):
            if matrix[i][j] != 0:
                edges.append((i, j, matrix[i][j]))
    return edges

def edges_to_matrix(edges, n, directed=False):
    matrix = [[0] * n for _ in range(n)]
    for edge in edges:
        u = edge[0]
        v = edge[1]
        weight = edge[2] if len(edge) >= 3 else 1
        matrix[u][v] = weight
        if not directed:
            matrix[v][u] = weight
    return matrix

def edges_to_adj(edges, n, directed=False):
    adj = {i: [] for i in range(n)}
    for edge in edges:
        u = edge[0]
        v = edge[1]
        weight = edge[2] if len(edge) >= 3 else 1
        adj[u].append((v, weight))
        if not directed:
            adj[v].append((u, weight))
    return adj

def adj_to_matrix(adj, n):
    matrix = [[0] * n for _ in range(n)]
    for u, neighbors in adj.items():
        for v, weight in neighbors:
            matrix[u][v] = weight
    return matrix

def adj_to_edges(adj, directed=False):
    edges = []
    for u, neighbors in adj.items():
        for v, weight in neighbors:
            if directed or u <= v:
                edges.append((u, v, weight))
    return edges

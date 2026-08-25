class Graph:
    def __init__(self, n=0, directed=False, weighted=False):
        self.n = n
        self.directed = directed
        self.weighted = weighted
        self.matrix = []
        self.adj = {}
        self.edges = []

    def from_matrix(self, matrix):
        pass

    def from_edges(self, edges, n):
        pass

    def from_text(self, text):
        pass

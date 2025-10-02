from collections import defaultdict

class CentroidDecomposition:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.subtree_size = [0]*n
        self.centroid_marked = [False]*n
        self.parent = [-1]*n  # parent in centroid tree

    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)

    def dfs_size(self, u, p):
        self.subtree_size[u] = 1
        for v in self.adj[u]:
            if v != p and not self.centroid_marked[v]:
                self.dfs_size(v, u)
                self.subtree_size[u] += self.subtree_size[v]

    def find_centroid(self, u, p, n):
        for v in self.adj[u]:
            if v != p and not self.centroid_marked[v] and self.subtree_size[v] > n//2:
                return self.find_centroid(v, u, n)
        return u

    def decompose(self, u, p=-1):
        self.dfs_size(u, -1)
        centroid = self.find_centroid(u, -1, self.subtree_size[u])
        self.centroid_marked[centroid] = True
        self.parent[centroid] = p
        for v in self.adj[centroid]:
            if not self.centroid_marked[v]:
                self.decompose(v, centroid)
        return centroid

# ---------------- Example Usage ----------------
if __name__ == "__main__":
    n = 7
    cd = CentroidDecomposition(n)
    edges = [(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)]
    for u,v in edges:
        cd.add_edge(u,v)

    root_centroid = cd.decompose(0)
    print("Centroid tree parents:", cd.parent)

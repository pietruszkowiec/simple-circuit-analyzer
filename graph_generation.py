import networkx as nx


def generate_erdos_renyi(n, p, a, b):
    while True:
        G = nx.erdos_renyi_graph(n, p)
        if nx.is_connected(G):
            break
        
    for u, v in list(G.edges):
        if u == v:
            G.remove_edge(u, v)
            continue
        
        G[u][v]['R'] = 1

    return G


def generate_grid(n, m):
    G = nx.grid_2d_graph(n, m)

    H = nx.Graph()
    H.add_nodes_from([i for i in range(n*m)])

    for u, v in G.edges:
        H.add_edge(u[0]*m + u[1], v[0]*m + v[1], R=1)

    return H


def generate_small_world(n):
    while True:
        G = nx.navigable_small_world_graph(n)
        
        H = nx.Graph()
        H.add_nodes_from([i for i in range(n*n)])

        for u, v in G.edges:
            if u[0]*n + u[1] == v[0]*n + v[1]:
                continue
            H.add_edge(u[0]*n + u[1], v[0]*n + v[1], R=1)
        
        if nx.is_connected(H):
            return H

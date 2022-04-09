import networkx as nx


def save_circuit(G, s, t, U, filename):
    with open('circuits/' + filename, 'w') as f:
        f.write(f'{s} {t} {U}\n')
        for u, v, edgedata in G.edges(data=True):
            f.write(f"{u} {v} {edgedata['R']}\n")


def load_graph(filename):
    with open('circuits/' + filename) as f:
        lines = f.readlines()
        s, t, U = lines[0].split()
        s = int(s)
        t = int(t)
        U = int(U)

        n = -1
        G = nx.Graph()

        for line in lines[1:]:
            u, v, w = line.split()
            u = int(u)
            v = int(v)
            w = int(w)

            if not G.has_node(u):
                G.add_node(u)
            if not G.has_node(v):
                G.add_node(v)
                
            G.add_edge(u, v, R=w)

    return G, s, t, U


def save_results(G, total_current, filename):
    with open('results/' + filename, 'w') as f:
        f.write(f"{total_current:.2f}\n")
        for u, v, edgedata in G.edges(data=True):
            if edgedata['I'] > 0:
                f.write(f"{u} {v} {edgedata['R']} {edgedata['I']:.2f}\n")
            else:
                f.write(f"{v} {u} {edgedata['R']} {edgedata['I']:.2f}\n")

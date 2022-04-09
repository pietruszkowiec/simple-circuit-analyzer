import networkx as nx
import matplotlib.pyplot as plt


def transform_into_digraph(G):
    H = nx.DiGraph(G)

    for u, v, edgedata in G.edges(data=True):
        u, v = min(u, v), max(u, v)
        if edgedata['I'] > 0:
            H.remove_edge(v, u)
        else:
            H.remove_edge(u, v)
            H[v][u]['I'] *= -1
        
    return H


def draw_circuit(H, **kwargs):
    pos = nx.nx_pydot.graphviz_layout(H)
    fig, ax = plt.subplots(figsize=(7, 7))
    
    if 'title' in kwargs:
        title=kwargs['title']
        ax.set_title(title)

    node_size = kwargs.get('node_size', 100)

    nx.draw_networkx_nodes(H, pos, node_size=node_size, node_color='w', 
                           edgecolors='k', linewidths=1.0)

    font_size = kwargs.get('font_size', 8)

    if kwargs.get('node_labels', False):
        node_labels = {u: u for u in range(len(H))}
        
        if 's' in kwargs:
            s = kwargs['s']
            node_labels[s] = 's'
        
        if 't' in kwargs:
            t = kwargs['t']
            node_labels[t] = 't'

        nx.draw_networkx_labels(H, pos, node_labels, font_size=font_size)

    edge_colors = [edgedata['I'] for _, _, edgedata in H.edges(data=True)]
    
    if kwargs.get('edge_widths', False):
        edge_widths = [abs(edgedata['I']) for _, _, edgedata in H.edges(data=True)]
        nx.draw_networkx_edges(H, pos, edge_color=edge_colors, width=edge_widths)
    else:
        edge_width = kwargs.get('edge_width', 5.0)
        nx.draw_networkx_edges(H, pos, edge_color=edge_colors, width=edge_width)

    if 'edge_labels' in kwargs:
        if 'R' in kwargs['edge_labels'] and 'I' in kwargs['edge_labels']:
            edge_labels = {(u, v): f'{edgedata["R"]}Ω\n{edgedata["I"]:.2f}A' 
                            for u, v, edgedata in H.edges(data=True)}

            nx.draw_networkx_edge_labels(H, pos, edge_labels, font_size=font_size)
        elif 'R' in kwargs['edge_labels']:
            edge_labels = {(u, v): f'{edgedata["R"]}Ω' 
                            for u, v, edgedata in H.edges(data=True)}

            nx.draw_networkx_edge_labels(H, pos, edge_labels, font_size=font_size)
        elif 'I' in kwargs['edge_labels']:
            edge_labels = {(u, v): f'{edgedata["I"]:.2f}A' 
                            for u, v, edgedata in H.edges(data=True)}

            nx.draw_networkx_edge_labels(H, pos, edge_labels, font_size=font_size)

    ax.set_axis_off()
    fig.tight_layout()

    
    if 'filename' in kwargs:
        plt.savefig(f"imgs/{kwargs['filename']}", dpi=300)
    
    if kwargs.get('show', True):
        plt.show()
    
    plt.close()

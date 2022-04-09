from file_io import *
from graph_generation import *
from circuit_solver import *
from visualization import *
from tests import *


def load_compute_save_test(filename, draw=True):
    G, s, t, U = load_graph(filename)

    print(f"{filename.removesuffix('.txt')}")
    G, total_current = find_currents_in_circuit(G, s, t, U)

    print(f'Total current: {total_current:.2f} A')
    print('Satisfies the Kirchhoff\'s current law: ' +\
          f'{test_kirchhoffs_current_law(G, s, t, total_current)}')

    save_results(G, total_current, filename.removesuffix('.txt') + '_res.txt')

    print()

    if not draw:
        return

    H = transform_into_digraph(G)

    n = len(G)
    m = len(G.edges)

    title = r'$\|V\| =$' + str(n) + '  ' +\
            r'$\|E\| =$' + str(m) + '  ' +\
            r'$U_{s t} =$' + str(U) + 'V' + '  ' +\
            r'$I_{c} =$' + f'{total_current:.2f}' + 'A'
    
    img_filename = filename.removesuffix('.txt')
    
    draw_circuit(H, title=title, node_size=20, 
                 edge_width=2, filename=img_filename+'_1.png',
                 show=True)

    draw_circuit(H, node_labels=True, s=s, t=t, font_size=6, 
                 title=title, node_size=50, edge_width=2, 
                 filename=img_filename+'_2.png',
                 show=False)

    draw_circuit(H, node_labels=True, s=s, t=t, font_size=6, 
                 title=title, node_size=50, edge_width=2, 
                 edge_labels={'R', 'I'}, filename=img_filename+'_3.png',
                 show=False)



if __name__ == '__main__':

    filenames = []

    grid_n_m = [(2, 3), 
                (2, 5), 
                (4, 4), 
                (6, 6),
                (10, 10),
                (10, 20),
                (20, 20)]

    U = 50
    for n, m in grid_n_m:
        G = generate_grid(n, m)
        filename = f'grid_{n}_{m}.txt'
        save_circuit(G, 0, n*m-1, U, filename)
        filenames.append(filename)

    U = 50
    for n in range(3, 20, 3):
        G = generate_small_world(n)
        filename = f'small_world_{n}.txt'
        save_circuit(G, 0, n*n-1, U, filename)
        filenames.append(filename)

    erdos_renyi_n_p = [(n, p) for n in range(15, 26, 10) for p in [0.3, 0.4, 0.5]]
    
    U = 50
    for n, p in erdos_renyi_n_p:
        G = generate_erdos_renyi(n, p, 1, 10)
        filename = f'erdos_renyi_{n}_{p}.txt'
        save_circuit(G, 0, n-1, U, filename)
        filenames.append(filename)

    for filename in filenames:
        load_compute_save_test(filename)

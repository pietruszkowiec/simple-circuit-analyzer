import numpy as np
import networkx as nx


def k_ij(i, j, n):
    i, j = min(i, j), max(i, j)
    return j - i - 1 + n*(n-1)//2 - (n-i)*(n-i-1)//2

def ij_k(k, n):
    i = n - 2 - int((np.sqrt(4*n*(n-1) - 8*k - 7) - 1)/2)
    j = k + i + 1 - n*(n-1)//2 + (n-i)*(n-i-1)//2
    return i, j


def first_kirchhoffs_law(G, A, s, t):
    n = len(G)
    eq_i = 0

    for u in range(n):
        for v in G[u]:
            if u < v:
                A[eq_i][k_ij(u, v, n)] = 1
            else:
                A[eq_i][k_ij(v, u, n)] = -1
        eq_i += 1
    
    A[s][-1] = -1
    A[t][-1] = 1

    return eq_i


def second_kirchhoffs_law(G, A, b, eq_i, s, t, U):
    n = len(G)

    for path in nx.connectivity.edge_disjoint_paths(G, s, t):
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            if u < v:
                A[eq_i][k_ij(u, v, n)] = G[u][v]['R']
            else:
                A[eq_i][k_ij(v, u, n)] = -G[u][v]['R']
        b[eq_i] = U
        eq_i += 1

    for cycle in nx.cycle_basis(G):
        for i in range(len(cycle)): 
            u, v = cycle[i-1], cycle[i]
            if u < v:
                A[eq_i][k_ij(u, v, n)] = -G[u][v]['R']
            else:
                A[eq_i][k_ij(v, u, n)] = G[u][v]['R']
        eq_i += 1

    return eq_i


def print_equations(A, b, G):
    n = len(G)
    for i in range(len(A)):
        print(i)
        for j in range(n * (n - 1) // 2):
            u, v = ij_k(j, n)
            if u not in G[v]:
                continue
            if A[i][j] != 0:
                if A[i][j] > 0:
                    print('+ ', end='')
                else:
                    print('- ', end='')
                print(f'{abs(A[i][j])} * I_{u,v} ', end='')

        if A[i][-1] != 0:
            if A[i][-1] > 0:
                print('+ ', end='')
            else:
                print('- ', end='')
            print(f'{abs(A[i][-1])} * I_c ', end='')
        print(f'= {b[i]}')


def create_system_of_eq(G, s, t, U):
    n = len(G)
    m = len(G.edges)
    var_num = 1 + n * (n - 1) // 2
    
    A = np.zeros((n + m, var_num))
    b = np.zeros((n + m))

    eq_i = first_kirchhoffs_law(G, A, s, t)
    eq_i = second_kirchhoffs_law(G, A, b, eq_i, s, t, U)

    A = A[:eq_i]
    b = b[:eq_i]
    
    return A, b


def assign_currents_to_graph(G, x):
    n = len(G)
    var_num = 1 + n * (n - 1) // 2

    for k in range(var_num - 1):
        u, v = ij_k(k, n)
        if u in G[v]:
            G[u][v]['I'] = x[k]

    return G


def find_currents_in_circuit(G, s, t, U):
    A, b = create_system_of_eq(G, s, t, U)    
    
    n = len(G)
    m = len(G.edges)
    
    
    print(f'Number of nodes: {n}')
    print(f'Number of edges: {m}')
    print(f'Number of equations: {A.shape[0]}')
    print(f'Number of variables: {A.shape[1]}')

    # print_equations(A, b, G)

    x = np.linalg.lstsq(A, b, rcond=None)[0]
    total_current = x[-1]
    G = assign_currents_to_graph(G, x)
    
    return G, total_current

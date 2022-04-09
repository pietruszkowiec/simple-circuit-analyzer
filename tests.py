import numpy as np


def test_kirchhoffs_current_law(G, s, t, total_current):
    n = len(G)

    current_sums = np.zeros(n)

    for u in range(n):        
        for v in G[u]:
            if u < v:
                current_sums[u] += G[u][v]['I']
            else:
                current_sums[u] -= G[u][v]['I']

        if u == s:
            current_sums[u] -= total_current
        elif u == t:
            current_sums[u] += total_current

    return np.allclose(current_sums, np.zeros(n))

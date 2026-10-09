import matplotlib.pyplot as plt

def random_matrix(rows, cols, seed=0):
    """Deterministic pseudo-random matrix in [0, 1) (pure python, no imports needed)."""
    state = seed + 12345
    mat = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            state = (1103515245 * state + 12345) % (2**31)
            row.append(state / 2**31)
        mat.append(row)
    return mat

import numpy as np
from scipy.spatial import cKDTree


# --------------------------------------------------
# Inverse Distance Weighting (IDW)
# --------------------------------------------------

def idw_interpolation(x, y, z, xi, yi, power=2, k=8):
    """
    Perform Inverse Distance Weighting (IDW) interpolation
    using k nearest neighbors (fast & stable).
    """

    k = min(k, len(x))  # safety for small datasets

    tree = cKDTree(np.column_stack((x, y)))
    distances, indices = tree.query(
        np.column_stack((xi.ravel(), yi.ravel())),
        k=k
    )

    zi = np.empty(distances.shape[0])

    for i in range(distances.shape[0]):
        d = distances[i]
        idx = indices[i]

        # Exact coordinate match → return observed value
        if np.any(d == 0):
            zi[i] = z[idx[d == 0][0]]
        else:
            weights = 1 / (d ** power)
            zi[i] = np.sum(weights * z[idx]) / np.sum(weights)

    return zi.reshape(xi.shape)



# --------------------------------------------------
# Grid creation
# --------------------------------------------------

def create_grid(x, y, resolution=100):
    """
    Create a regular interpolation grid.
    """
    xi = np.linspace(min(x), max(x), resolution)
    yi = np.linspace(min(y), max(y), resolution)
    return np.meshgrid(xi, yi)

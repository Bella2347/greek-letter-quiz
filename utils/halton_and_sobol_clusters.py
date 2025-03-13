import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.qmc import Halton, Sobol

def main():
    group_sizes = [4, 4, 4, 6, 6]
    dim = len(group_sizes)

    # Generate clustered points
    points = generate_clustered_simplex_points(group_sizes, dim, method="halton")

    # Print first points (each row should sum to ~1)
    print("Clustered 5D Points:\n", points)
    print("\nSum of each vector (should be ~1):\n", np.sum(points, axis=1))

    visualize(points, group_sizes)

def generate_clustered_simplex_points(group_sizes, dim=5, method="halton"):
    """Generate quasi-random points in 5D where each point sums to 1,
    grouped into clusters.
    """
    assert len(group_sizes) == dim, "group_sizes must match the number of dimensions"

    N = sum(group_sizes)  # Total number of points

    # Generate quasi-random points
    if method == "halton":
        sampler = Halton(d=dim, scramble=True)
    elif method == "sobol":
        sampler = Sobol(d=dim,scramble=True)
    else:
        raise ValueError("Method must be 'halton' or 'sobol'")

    points = sampler.random(N)

    # Assign groups with different sizes and boost one axis
    start_idx = 0
    for i, group_size in enumerate(group_sizes):
        end_idx = start_idx + group_size
        points[start_idx:end_idx, i] += 3  # Boost one dimension (strong preference)
        start_idx = end_idx  # Move to next group

    # Normalize so each point sums to 1
    points /= points.sum(axis=1, keepdims=True)

    return points

def visualize(points, group_sizes):
    # Visualize in 3D (First three dimensions)
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')

    colors = ["blue", "red", "green", "purple", "orange"]
    start_idx = 0
    for i, group_size in enumerate(group_sizes):
        end_idx = start_idx + group_size
        ax.scatter(points[start_idx:end_idx, 0], points[start_idx:end_idx, 1], points[start_idx:end_idx, 2], 
                c=colors[i], s=10, label=f'Group {i+1}')
        start_idx = end_idx  # Move to the next group

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    plt.show()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- 1. The Objective Function ---
# This is the "hill" we want to find the peak of.
def objective_function(x, y):
    """A sample 2D function with multiple local maxima."""
    return np.sin(x**2) * np.cos(y**2)

# --- 2. The Hill Climbing Algorithm ---
def hill_climbing(objective_fn, bounds, n_iterations, step_size):
    """
    Performs the hill climbing search algorithm.

    Args:
        objective_fn: The function to be maximized.
        bounds: A list of tuples [(min, max), (min, max), ...] for each dimension.
        n_iterations: The total number of iterations to run.
        step_size: The size of the step to take when exploring neighbors.

    Returns:
        A tuple containing the best solution found (list) and its score.
    """
    # Generate a random starting point within the defined bounds
    solution = [bounds[i][0] + np.random.rand() * (bounds[i][1] - bounds[i][0]) for i in range(len(bounds))]
    solution_eval = objective_fn(solution[0], solution[1])

    # Keep track of the path for visualization
    path = [solution]
    
    # Main loop
    for i in range(n_iterations):
        # Take a copy of the current best solution
        candidate = list(solution)
        
        # Generate a random move (perturbation)
        # Move one variable at a time
        dim = np.random.randint(0, len(bounds))
        # Move up or down
        direction = np.random.choice([-1, 1])
        
        candidate[dim] += direction * step_size
        
        # Clip the candidate to stay within the bounds
        candidate[dim] = max(bounds[dim][0], min(bounds[dim][1], candidate[dim]))

        # Evaluate the candidate solution
        candidate_eval = objective_fn(candidate[0], candidate[1])
        
        # Check if we should keep the new point (is it higher?)
        if candidate_eval > solution_eval:
            solution, solution_eval = candidate, candidate_eval
            path.append(solution)
            print(f'> Iteration {i}, Position=({solution[0]:.4f}, {solution[1]:.4f}), Score={solution_eval:.4f}')
            
    return solution, solution_eval, np.array(path)


# --- 3. Run the Algorithm and Visualize ---
if __name__ == '__main__':
    # Define the bounds of our search space
    bounds = [(-2.0, 2.0), (-2.0, 2.0)]
    # Define hyperparameters
    iterations = 500
    step = 0.05
    
    # Perform the search
    best_solution, best_score, path = hill_climbing(objective_function, bounds, iterations, step)
    
    print("\n--- Search Complete ---")
    print(f"🎯 Best Solution Found: ({best_solution[0]:.5f}, {best_solution[1]:.5f})")
    print(f"🏔️ Height at Best Solution: {best_score:.5f}")

    # --- Visualization ---
    # Create a grid of points for the 3D plot
    x_range = np.arange(bounds[0][0], bounds[0][1], 0.05)
    y_range = np.arange(bounds[1][0], bounds[1][1], 0.05)
    x_grid, y_grid = np.meshgrid(x_range, y_range)
    z_grid = objective_function(x_grid, y_grid)
    
    # Create the figure
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the surface
    ax.plot_surface(x_grid, y_grid, z_grid, cmap='viridis', alpha=0.7, rstride=5, cstride=5)
    
    # Plot the path taken by the algorithm
    ax.plot(path[:, 0], path[:, 1], objective_function(path[:, 0], path[:, 1]), 'r-o', markersize=5, linewidth=3)
    
    # Mark start and end points
    ax.scatter(path[0, 0], path[0, 1], objective_function(path[0, 0], path[0, 1]), color='black', marker='X', s=150, label='Start')
    ax.scatter(path[-1, 0], path[-1, 1], objective_function(path[-1, 0], path[-1, 1]), color='red', marker='*', s=200, label='End (Local Maximum)')
    
    ax.set_title('Hill Climbing Search Path')
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('f(x, y) - Height')
    ax.legend()
    plt.show()
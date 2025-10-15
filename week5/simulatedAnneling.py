import numpy as np
import matplotlib.pyplot as plt
import math

# --- 1. The Objective Function ---
# This is the "landscape" we want to find the lowest point of.
def objective_function(x):
    """A sample 1D function with a global minimum and several local minima."""
    return (x - 2) * x * (x + 2)**2

# --- 2. The Simulated Annealing Algorithm ---
def simulated_annealing(objective, bounds, n_iterations, step_size, initial_temp, cooling_rate):
    """
    Performs the simulated annealing search algorithm.

    Args:
        objective: The function to be minimized.
        bounds: A list [(min, max)] for the search space.
        n_iterations: Total number of iterations.
        step_size: The maximum size of a step to take.
        initial_temp: The starting temperature.
        cooling_rate: The rate at which temperature decreases (e.g., 0.99).

    Returns:
        A tuple of the best solution found and its score.
    """
    # Generate a random starting point
    current_solution = np.random.uniform(bounds[0][0], bounds[0][1])
    current_eval = objective(current_solution)
    
    # Keep track of the best solution found so far
    best_solution, best_eval = current_solution, current_eval
    
    # Keep track of scores for plotting
    scores = []
    
    temperature = initial_temp
    
    for i in range(n_iterations):
        # Take a random step
        candidate = current_solution + np.random.uniform(-step_size, step_size)
        # Clip to stay within bounds
        candidate = max(bounds[0][0], min(bounds[0][1], candidate))
        
        candidate_eval = objective(candidate)
        
        # Check if the new candidate is better
        if candidate_eval < best_eval:
            best_solution, best_eval = candidate, candidate_eval
            print(f'> Iteration {i}, New Best=({best_solution:.4f}), Score={best_eval:.4f}')

        # Calculate the difference in energy (cost)
        diff = candidate_eval - current_eval
        
        # If the new solution is better, always accept it
        if diff < 0:
            current_solution, current_eval = candidate, candidate_eval
        else:
            # If the new solution is worse, maybe accept it anyway
            # This is the core of the algorithm
            acceptance_prob = math.exp(-diff / temperature)
            if np.random.rand() < acceptance_prob:
                current_solution, current_eval = candidate, candidate_eval

        # Cool the temperature
        temperature *= cooling_rate
        scores.append(best_eval)
        
    return best_solution, best_eval, scores

# --- 3. Run the Algorithm and Visualize ---
if __name__ == "__main__":
    # Define the bounds of our search space
    bounds = [(-3.0, 3.0)]
    # Define hyperparameters
    iterations = 1000
    step = 0.1
    temp = 10
    cooling = 0.99
    
    # Perform the search
    best_solution, best_score, scores = simulated_annealing(
        objective_function, bounds, iterations, step, temp, cooling
    )
    
    print("\n--- Search Complete ---")
    print(f"🎯 Best Solution Found: x = {best_solution:.5f}")
    print(f"🏔️ Lowest Point Found: f(x) = {best_score:.5f}")

    # Plotting the results
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    x_range = np.arange(bounds[0][0], bounds[0][1], 0.01)
    y_range = objective_function(x_range)
    plt.plot(x_range, y_range, label='Objective Function')
    plt.scatter([best_solution], [best_score], color='red', marker='*', s=150, zorder=5, label=f'Global Minimum Found')
    plt.title('Objective Function Landscape')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(scores)
    plt.title('Improvement Over Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Best Score')
    
    plt.tight_layout()
    plt.show()
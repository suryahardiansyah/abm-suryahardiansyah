# Agent-Based Segregation Model

This project simulates an agent-based model to study segregation dynamics in a 2D world. Agents of two different colors (red and blue) are placed on a grid. Each agent has a preference for the number of same-color neighbors it wants to have. The simulation runs iteratively, allowing agents to move to new locations if they are not happy with their current location.

## Features

- **Agent Class**: Represents individual agents with a color and preference for same-color neighbors.
- **World Class**: Represents the grid and manages the placement and movement of agents.
- **Simulation**: Runs the simulation for a specified number of iterations, updating agent locations and reporting their happiness.
- **Visualization**: Uses Matplotlib and Seaborn to visualize the state of the world at each iteration.

## Requirements

- Python 3.x
- Matplotlib
- Seaborn
- NumPy

You can install the required packages using pip:
```bash
pip install matplotlib seaborn numpy
```

## How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/agent-based-segregation.git
    cd agent-based-segregation
    ```

2. Run the simulation script:
    ```bash
    python segregation_model.py
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the Schelling Segregation Model.
- Visualization tools provided by Matplotlib and Seaborn.

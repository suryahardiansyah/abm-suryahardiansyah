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

## Code Overview

### Agent Class
```python
class Agent:
    def __init__(self, color, same_pref):
        self.color = color
        self.same_pref = same_pref
        self.location = None
    
    def move(self, world):
        if not self.am_i_happy(world):
            vacant_patches = world.find_vacant(return_all=True)
            for patch in vacant_patches:
                if self.am_i_happy(world, patch):
                    world.grid[self.location] = None
                    self.location = patch
                    world.grid[patch] = self
                    return 1
            return 2
        return 0
    
    def am_i_happy(self, world, loc=None):
        if loc is None:
            loc = self.location
        neighbors = self.locate_neighbors(world, loc)
        same_color_neighbors = sum(1 for neighbor in neighbors if neighbor and neighbor.color == self.color)
        total_neighbors = len(neighbors)
        if total_neighbors == 0:
            return False
        return same_color_neighbors >= self.same_pref
    
    def locate_neighbors(self, world, loc):
        x, y = loc
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (x + dx) % world.size[0], (y + dy) % world.size[1]
                neighbors.append(world.grid[(nx, ny)])
        return neighbors
```

### World Class
```python
class World:
    def __init__(self, size, num_agents, same_pref):
        self.size = size
        self.grid = self.build_grid(size)
        self.agents = self.build_agents(num_agents, same_pref)
        self.init_world()
    
    def build_grid(self, size):
        return {(x, y): None for x in range(size[0]) for y in range(size[1])}
    
    def build_agents(self, num_agents, same_pref):
        agents = []
        for i in range(num_agents):
            color = 'red' if i < num_agents / 2 else 'blue'
            agents.append(Agent(color, same_pref))
        return agents
    
    def init_world(self):
        for agent in self.agents:
            loc = self.find_vacant()
            if loc:
                agent.location = loc
                self.grid[loc] = agent
    
    def find_vacant(self, return_all=False):
        vacant = [loc for loc, occupant in self.grid.items() if occupant is None]
        if return_all:
            return vacant
        return random.choice(vacant) if vacant else None
    
    def run(self, max_iter):
        for iteration in range(max_iter):
            random.shuffle(self.agents)
            for agent in self.agents:
                agent.move(self)
            self.report_integration(iteration)
    
    def report_integration(self, iteration):
        happy_agents = sum(agent.am_i_happy(self) for agent in self.agents)
        print(f'Iteration report: {happy_agents}/{len(self.agents)} agents are happy.')
        self.plot_world(iteration)
    
    def plot_world(self, iteration):
        grid_size = self.size
        world_grid = np.zeros(grid_size)

        for (x, y), agent in self.grid.items():
            if agent is not None:
                if agent.color == 'red':
                    world_grid[x][y] = 1
                elif agent.color == 'blue':
                    world_grid[x][y] = 2

        plt.figure(figsize=(10, 10))
        sns.heatmap(world_grid, cbar=False, square=True, linewidths=.5, linecolor='black', annot=False,
                    xticklabels=False, yticklabels=False, cmap=sns.color_palette(["white", "red", "blue"]))
        plt.title(f'World State at Iteration {iteration}')
        plt.show()
```

### Main Execution
```python
if __name__ == "__main__":
    world_size = (20, 20)
    num_agents = 200
    same_pref = 3
    max_iter = 10
    
    world = World(world_size, num_agents, same_pref)
    world.run(max_iter)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the Schelling Segregation Model.
- Visualization tools provided by Matplotlib and Seaborn.

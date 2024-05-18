import random
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class Agent:
    def __init__(self, color, same_pref):
        """Initialize agent with its color and preference for same neighbors."""
        self.color = color
        self.same_pref = same_pref
        self.location = None
    
    def move(self, world):
        """Move agent to a new position if unhappy."""
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
        """Check if the agent is happy at its current or a given location."""
        if loc is None:
            loc = self.location
        neighbors = self.locate_neighbors(world, loc)
        same_color_neighbors = sum(1 for neighbor in neighbors if neighbor and neighbor.color == self.color)
        total_neighbors = len(neighbors)
        if total_neighbors == 0:
            return False
        return same_color_neighbors >= self.same_pref
    
    def locate_neighbors(self, world, loc):
        """Locate neighbors around the given location."""
        x, y = loc
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (x + dx) % world.size[0], (y + dy) % world.size[1]
                neighbors.append(world.grid[(nx, ny)])
        return neighbors

class World:
    def __init__(self, size, num_agents, same_pref):
        """Initialize the world with a grid and agents."""
        self.size = size
        self.grid = self.build_grid(size)
        self.agents = self.build_agents(num_agents, same_pref)
        self.init_world()
    
    def build_grid(self, size):
        """Build an empty grid for the world."""
        return {(x, y): None for x in range(size[0]) for y in range(size[1])}
    
    def build_agents(self, num_agents, same_pref):
        """Build a list of agents with random colors."""
        agents = []
        for i in range(num_agents):
            color = 'red' if i < num_agents / 2 else 'blue'
            agents.append(Agent(color, same_pref))
        return agents
    
    def init_world(self):
        """Place agents at random locations in the world."""
        for agent in self.agents:
            loc = self.find_vacant()
            if loc:
                agent.location = loc  # Ensure location is a tuple
                self.grid[loc] = agent
    
    def find_vacant(self, return_all=False):
        """Find a list of vacant patches."""
        vacant = [loc for loc, occupant in self.grid.items() if occupant is None]
        if return_all:
            return vacant
        return random.choice(vacant) if vacant else None
    
    def run(self, max_iter):
        """Run the simulation for a number of iterations."""
        for iteration in range(max_iter):
            random.shuffle(self.agents)
            for agent in self.agents:
                agent.move(self)
            self.report_integration(iteration)
    
    def report_integration(self, iteration):
        """Report the integration status of the world."""
        happy_agents = sum(agent.am_i_happy(self) for agent in self.agents)
        print(f'Iteration report: {happy_agents}/{len(self.agents)} agents are happy.')
        self.plot_world(iteration)
    
    def plot_world(self, iteration):
        """Plot the current state of the world."""
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

if __name__ == "__main__":
    world_size = (20, 20)
    num_agents = 200
    same_pref = 3
    max_iter = 10
    
    world = World(world_size, num_agents, same_pref)
    world.run(max_iter)

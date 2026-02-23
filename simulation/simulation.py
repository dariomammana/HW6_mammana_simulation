"""
Simulation module: Orchestrates the overall simulation loop and setup.
Classes: Simulation
"""

import random
import time

from .lifeforms import Grass, Sheep, Wolf
from .environment import Map


class Simulation:
    """Orchestrates the entire creature simulation."""
    
    def __init__(
        self,
        timestep=0.125,
        iterations=3,
        map_size=10,
        sheep_count=5,
        grass_growth_rate=0.05,
        wolf_count=10,
        dynamic_terminal=None
    ):
        """Initialize the simulation with specified parameters."""
        # Import here to avoid circular imports
        if dynamic_terminal is None:
            from visualisation import DynamicTerminal
            dynamic_terminal = DynamicTerminal(map_size + 2)
        
        self._dynamic_terminal = dynamic_terminal
        self.max_iter = iterations
        self.time_step = timestep
        self.current_iter = 0
        self.terminated = False
        self.sheep_count = sheep_count
        self.wolf_count = wolf_count
        self.map_size = map_size
        self.map = Map(map_size)
        self.lifeforms = list()
        self.grass_growth_rate = grass_growth_rate 
        self.setup()
        
    def setup(self):
        """Initialize the simulation with grass, sheep, and wolves."""
        # Grow initial grass
        Grass.grow(self.map, self.grass_growth_rate)
        
        # Place sheep
        for i in range(0, self.sheep_count):
            x = random.randint(0, self.map_size - 1) 
            y = random.randint(0, self.map_size - 1)
            while self.map.cells[x][y].inhabitant is not None:
                x = random.randint(0, self.map_size - 1)
                y = random.randint(0, self.map_size - 1)
            new_sheep = Sheep(self.map.cells[x][y])
            self.lifeforms.append(new_sheep)
            self.map.cells[x][y].inhabitant = new_sheep
            
        # Place wolves
        for i in range(0, self.wolf_count):
            x = random.randint(0, self.map_size - 1)
            y = random.randint(0, self.map_size - 1)
            while self.map.cells[x][y].inhabitant is not None:
                x = random.randint(0, self.map_size - 1)
                y = random.randint(0, self.map_size - 1)
            new_wolf = Wolf(self.map.cells[x][y])
            self.lifeforms.append(new_wolf)
            self.map.cells[x][y].inhabitant = new_wolf
        
    def step(self):
        """Execute one iteration of the simulation."""
        if self.current_iter < self.max_iter:
            self.current_iter += 1
            self.update()
            self.render()
        else:
            self.terminated = True
            print(f"The simulation has terminated after {self.current_iter} iterations.")
            
    def update(self):
        """Update all entities in the simulation."""
        time.sleep(self.time_step)
        Grass.grow(self.map, self.grass_growth_rate)
        for lifeform in list(self.lifeforms): 
            lifeform.act(self.map, self.lifeforms)
        Grass.consume(self.map)
    
    def render(self):
        """Render the current state of the simulation."""
        self._dynamic_terminal.render(
            ["Round " + str(self.current_iter), self.map.render()],
            self.map_size + 2
        )

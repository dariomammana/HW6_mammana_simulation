
# Our class OOP project here

import string 
import random
import sys    
import time   
import os
from abc import ABC

if os.name == 'nt':
    os.system('color')

class Lifeform(ABC):
    
    def __init__(self, location = None):
        self.location = location
        self._r = random.randint(0,255)
        self._g = random.randint(0,255)
        self._b = random.randint(0,255)
        self.symbol = f"\x1b[38;2;{self._r};{self._g};{self._b}m{random.choice(string.ascii_letters)}\x1b[0m"
        
    def act(self, map, lifeforms=None):
        """Perform one timestep of behavior for this lifeform."""
        if self.location is None:
            return
        self.age += 1
        self.energy -= self.e_move
        self.move(map, lifeforms)
        self.eat(map, lifeforms)
        self.reproduce(map, lifeforms)
        self.survive(map, lifeforms)
    
    def move(self, map, lifeforms=None):
        """Move the lifeform to a random adjacent cell if empty."""
        pass
    
    def eat(self, map, lifeforms=None):
        """Consume resources or other lifeforms if applicable."""
        pass

    def reproduce(self, map, lifeforms=None):
        """Create offspring if conditions are met. Override in subclasses."""
        pass
    
    def survive(self, map, lifeforms=None):
        """Remove the lifeform from the simulation if needed."""
        pass
            
    
    def render(self):
        """Return the display symbol for this lifeform."""
        return self.symbol
    
class Grass(Lifeform):
    """
    Grass is a lifeform represented by a green background in the terminal.
    Each turn, grass has a chance to grow in empty cells.
    Each turn, if a sheep occpiea a cell with grass, the grass gets consumed and the cell returns empty.
    Grass does not move
    """
    def __init__(self):
        super().__init__(location=None)
        self.symbol = "\x1b[48;2;34;139;34m \x1b[0m" # Green background for grass

# Grass does not move, eat, reproduce, or die
    def move(self, map, lifeforms=None):
        return

    def eat(self, map, lifeforms=None):
        return

    def reproduce(self, map, lifeforms=None):
        return

    def survive(self, map, lifeforms=None):
        return

    @classmethod
    def grow(cls, map, p_g=0.05):
        for i in range(0, map.size):
            for j in range(0, map.size):
                cell = map.cells[i][j]
                if cell.inhabitant is None and cell.state == ".":
                    if random.random() < p_g:
                        cell.state = cls().render()

    @classmethod
    def consume(cls, map):
        for i in range(0, map.size):
            for j in range(0, map.size):
                cell = map.cells[i][j]
                if isinstance(cell.inhabitant, Sheep) and cell.state != ".":
                    cell.state = "."

class Sheep(Lifeform):
    """
    Sheep is a lifeform represented by a white 'S' in the terminal.
    Each turn, sheep ages and loses energy for moving.
    Each turn, sheep moves to a random adjacent cell (up, down, left, right).
    If there's grass in the current cell, the sheep eats it and gains energy.
    """
    def __init__(
        self,
        location=None,
        e_sheep_init=10,
        e_grass=4,
        e_move=1,
        e_sheep_reproduce=12,
        max_age=30,
    ):
        super().__init__(location=location)
        self.symbol = "\x1b[38;2;255;255;255mS\x1b[0m" # White 'S' for sheep
        self.energy = e_sheep_init # Initial energy for the sheep
        self.e_grass = e_grass # Energy gained from eating grass
        self.e_move = e_move # Energy cost for moving
        self.e_sheep_reproduce = e_sheep_reproduce # Energy threshold for reproduction
        self.e_reproduce = e_sheep_reproduce
        self.max_age = max_age # Maximum age for the sheep
        self.age = 0 # Age of the sheep

    def move(self, map, lifeforms=None):
        """Sheep moves to a random adjacent cell."""
        moves = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        x_move, y_move = random.choice(moves)
        new_x = (self.location.x + x_move) % (len(map.cells))
        new_y = (self.location.y + y_move) % (len(map.cells))
        target = map.cells[new_x][new_y]
        if not target.inhabitant:
            self.location.inhabitant = None
            self.location = target
            target.inhabitant = self

    def eat(self, map, lifeforms=None):
        """Sheep eats grass to gain energy."""
        if self.location and self.location.state != ".":
            self.location.state = "."
            self.energy += self.e_grass

    def reproduce(self, map, lifeforms=None):
        """Sheep reproduces when energy threshold is met."""
        if not lifeforms or not self.location:
            return
        if self.energy < self.e_reproduce:
            return
        moves = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        random.shuffle(moves)
        for x_move, y_move in moves:
            new_x = (self.location.x + x_move) % (len(map.cells))
            new_y = (self.location.y + y_move) % (len(map.cells))
            target = map.cells[new_x][new_y]
            if target.inhabitant is None:
                child_energy = self.energy // 2
                self.energy -= child_energy
                lamb = Sheep(
                    location=target,
                    e_sheep_init=child_energy,
                    e_grass=self.e_grass,
                    e_move=self.e_move,
                    e_sheep_reproduce=self.e_sheep_reproduce,
                    max_age=self.max_age,
                )
                target.inhabitant = lamb
                lifeforms.append(lamb)
                break

    def survive(self, map, lifeforms=None):
        """Sheep dies if energy is depleted or max age is reached."""
        if self.energy <= 0 or self.age >= self.max_age:
            if self.location:
                self.location.inhabitant = None
                self.location = None
            if lifeforms and self in lifeforms:
                lifeforms.remove(self)

class Wolf(Lifeform):
    """
    Wolf is a predator represented by a red 'W'.
    It moves randomly, eats sheep, reproduces with enough energy,
    and can die from starvation, old age, or random chance.
    """
    def __init__(
        self,
        location=None,
        e_wolf_init=14,
        e_sheep=8,
        e_move=1,
        e_wolf_reproduce=18,
        max_age=40,
        death_chance=0.02,
    ):
        super().__init__(location=location)
        self.symbol = "\x1b[38;2;255;0;0mW\x1b[0m" # Red 'W' for wolf
        self.energy = e_wolf_init
        self.e_sheep = e_sheep
        self.e_move = e_move
        self.e_wolf_reproduce = e_wolf_reproduce
        self.e_reproduce = e_wolf_reproduce
        self.max_age = max_age
        self.death_chance = death_chance
        self.age = 0
        self._last_prey = None
        self.prey_class = Sheep

    def move(self, map, lifeforms=None):
        """Wolf moves to a random adjacent cell and targets sheep if present."""
        self._last_prey = None
        moves = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        x_move, y_move = random.choice(moves)
        new_x = (self.location.x + x_move) % (len(map.cells))
        new_y = (self.location.y + y_move) % (len(map.cells))
        target = map.cells[new_x][new_y]
        if isinstance(target.inhabitant, Sheep):
            self._last_prey = target.inhabitant
        if target.inhabitant is None or isinstance(target.inhabitant, Sheep):
            self.location.inhabitant = None
            self.location = target
            target.inhabitant = self
        """Wolf eats sheep to gain energy."""
        if not self._last_prey: 
            return
        prey = self._last_prey 
        if lifeforms and prey in lifeforms:
            lifeforms.remove(prey)
        prey.location = None
        self.energy += self.e_sheep
        self._last_prey = None

    def reproduce(self, map, lifeforms=None):
        """Wolf reproduces when energy threshold is met."""
        if not lifeforms or not self.location:
            return 
        if self.energy < self.e_reproduce:
            return
        moves = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        random.shuffle(moves)
        for x_move, y_move in moves:
            new_x = (self.location.x + x_move) % (len(map.cells))
            new_y = (self.location.y + y_move) % (len(map.cells))
            target = map.cells[new_x][new_y]
            if target.inhabitant is None:
                child_energy = self.energy // 2
                self.energy -= child_energy
                pup = Wolf(
                    location=target,
                    e_wolf_init=child_energy,
                    e_sheep=self.e_sheep,
                    e_move=self.e_move,
                    e_wolf_reproduce=self.e_wolf_reproduce,
                    max_age=self.max_age,
                    death_chance=self.death_chance,
                )
                target.inhabitant = pup
                lifeforms.append(pup)
                break

    def survive(self, map, lifeforms=None):
        """Wolf dies if energy is depleted, max age is reached, or by random chance."""
        if self.energy <= 0 or self.age >= self.max_age or random.random() < self.death_chance:
            if self.location:
                self.location.inhabitant = None
                self.location = None
            if lifeforms and self in lifeforms:
                lifeforms.remove(self)

class Map:
    
    def __init__(self, n = 10):
        self.size = n
        self.cells = dict()
        for i in range(0,self.size):
            self.cells[i] = dict()
            for j in range(0,self.size):
                self.cells[i][j] = Cell(i,j)
                
    def render(self):
        render_str = ""
        for i in range(0,self.size):
            render_str += "\n"
            for j in range(0,self.size):
                render_str += self.cells[i][j].render() + " "
        return(render_str)
    
class Cell:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "."
        self.inhabitant = None
        
    def render(self):
        if (self.inhabitant):
            return self.inhabitant.render()
        else:
            return self.state

class Simulation:
    
    def __init__(self, timestep = 0.125, iterations = 3, map_size = 10,sheep_count = 5, grass_growth_rate = 0.05, wolf_count = 10):
        self._dynamic_terminal = DynamicTerminal(map_size+2)
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
        Grass.grow(self.map, self.grass_growth_rate)
        for i in range(0,self.sheep_count):
            x = random.randint(0, self.map_size-1) 
            y = random.randint(0, self.map_size-1)
            while self.map.cells[x][y].inhabitant is not None: # Ensure we place the sheep in an empty cell
                x = random.randint(0, self.map_size-1)
                y = random.randint(0, self.map_size-1)
            new_life = Sheep(self.map.cells[x][y]) # Place a new sheep and not a generic lifeform.
            self.lifeforms.append(new_life)
            self.map.cells[x][y].inhabitant = new_life
        for i in range(0, self.wolf_count):
            x = random.randint(0, self.map_size-1)
            y = random.randint(0, self.map_size-1)
            while self.map.cells[x][y].inhabitant is not None: # Ensure we place the wolf in an empty cell
                x = random.randint(0, self.map_size-1)
                y = random.randint(0, self.map_size-1)
            new_wolf = Wolf(self.map.cells[x][y])
            self.lifeforms.append(new_wolf)
            self.map.cells[x][y].inhabitant = new_wolf
        
        
    def step(self):
        if self.current_iter < self.max_iter:
            self.current_iter += 1
            self.update()
            self.render()
        else:
            self.terminated = True
            print(f"The simulation has terminated after {self.current_iter} iterations.")
            
    def update(self):
        time.sleep(self.time_step)
        Grass.grow(self.map, self.grass_growth_rate)
        for lifeform in list(self.lifeforms): 
            lifeform.act(self.map, self.lifeforms)
        Grass.consume(self.map)
    
    def render(self):
        self._dynamic_terminal.render(["Round " + str(self.current_iter),self.map.render()],self.map_size+2)
        
class DynamicTerminal:
    """The dynamic termin provides an interface to repaint multiple rows in the terminal and animate the simulation"""

    def __init__(self,nrows = 12):
        for i in range(0,nrows):
            print("")

    def move_cursor_up(self, lines: int):
        """Move cursor up <lines> lines."""
        sys.stdout.write(f'\x1b[{lines}A')   # ESC[<n>A
        sys.stdout.flush()

    def rewrite_lines(self, new_lines):
        """Write <new_lines> starting at the current cursor position."""
        sys.stdout.write('\n'.join(new_lines) + '\n')
        sys.stdout.flush()

    def clear_line(self):
        """Clear the entire current line (ESC[2K)."""
        sys.stdout.write('\x1b[2K')
        sys.stdout.flush()

    def render(self, text, nrows):
        self.move_cursor_up(nrows)
        self.clear_line()
        self.rewrite_lines(text)
        
if __name__ == "__main__":
    sim = Simulation(iterations=20,map_size = 30,sheep_count = 40,wolf_count = 20, grass_growth_rate=0.05)
    while(not sim.terminated):
        sim.step()

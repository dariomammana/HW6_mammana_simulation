
# Our class OOP project here

import string 
import random
import sys    
import time   
import os

if os.name == 'nt':
    os.system('color')

class Lifeform:
    
    def __init__(self, location = None):
        self.location = location
        self._r = random.randint(0,255)
        self._g = random.randint(0,255)
        self._b = random.randint(0,255)
        self.symbol = f"\x1b[38;2;{self._r};{self._g};{self._b}m{random.choice(string.ascii_letters)}\x1b[0m"
        
    def act(self, map):
        self.move(map)
    
    def move(self, map):
        x_offset =random.randint(-1, 1)
        y_offset =random.randint(-1, 1)
        new_x = (self.location.x+x_offset) % (len(map.cells))
        new_y = (self.location.y+y_offset) % (len(map.cells))
        if not map.cells[new_x][new_y].inhabitant:
            self.location.inhabitant = None
            self.location = map.cells[new_x][new_y]
            map.cells[new_x][new_y].inhabitant = self
    
    def eat(self, map):
        """
        Docstring for eat
        INSERT BEHAVIOR HERE
        """
        pass

    def reproduce(self, map):
        """
        Docstring for reproduce
        INSERT BEHAVIOR HERE
        """
        pass

    def die(self, map):
        """
        Docstring for die
        INSERT BEHAVIOR HERE
        """
        pass
            
    
    def render(self):
        return(self.symbol)
    
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

    def act(self, map):
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
    Docstring for Sheep
    INSERT BEHAVIOR HERE
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
        self.max_age = max_age # Maximum age for the sheep
        self.age = 0 # Age of the sheep

    def act(self, map, lifeforms=None):
        '''each step it:
        ages,
        loses energy for moving,
        moves,
        eats grass if present,
        reproduces if energy is high enough,
        dies if energy is zero or age is maxed'''
        if self.location is None:
            return 
        self.age += 1
        self.energy -= self.e_move
        self.move(map)
        self.eat(map)
        if self.energy >= self.e_sheep_reproduce:
            self.reproduce(map, lifeforms)
        if self.energy <= 0 or self.age >= self.max_age:
            self.die(map, lifeforms)

    def move(self, map):
        moves = [(-1, 0), (0, -1), (0, 1), (1, 0)] # Up, Left, Right, Down
        x_move, y_move = random.choice(moves)
        new_x = (self.location.x + x_move) % (len(map.cells)) 
        new_y = (self.location.y + y_move) % (len(map.cells))
        if not map.cells[new_x][new_y].inhabitant: # Only move if the target cell is unoccupied
            self.location.inhabitant = None
            self.location = map.cells[new_x][new_y]
            map.cells[new_x][new_y].inhabitant = self

    def eat(self, map): # If there's grass in the current cell, eat it and gain energy
        if self.location and self.location.state != ".":
            self.location.state = "."
            self.energy += self.e_grass

    def reproduce(self, map, lifeforms): 
        if not lifeforms or not self.location: # Check if lifeforms list is provided and location is valid
            return
        
        moves = [(-1, 0), (0, -1), (0, 1), (1, 0)] # Up, Left, Right, Down
        random.shuffle(moves)
        for x_move, y_move in moves:
            new_x = (self.location.x + x_move) % (len(map.cells))
            new_y = (self.location.y + y_move) % (len(map.cells))
            target = map.cells[new_x][new_y]
            if target.inhabitant is None:
                child_energy = self.energy // 2 # Parent gives half of its energy to the child
                self.energy -= child_energy # Reduce parent's energy by the amount given to the child
                lamb = Sheep( # Create a small lamb in the target cell
                    location=target,
                    e_sheep_init=child_energy,
                    e_grass=self.e_grass,
                    e_move=self.e_move,
                    e_sheep_reproduce=self.e_sheep_reproduce,
                    max_age=self.max_age,
                )
                target.inhabitant = lamb
                lifeforms.append(lamb)
                break # Only reproduce once per turn

    def die(self, map, lifeforms): # Remove the sheep from the map and the lifeforms list
        if self.location:
            self.location.inhabitant = None
            self.location = None
        if lifeforms and self in lifeforms:
            lifeforms.remove(self)

class Wolf(Lifeform):
    """
    Docstring for Wolf
    INSERT BEHAVIOR HERE
    """
    pass

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
    
    def __init__(self, timestep = 0.125, iterations = 3, map_size = 10,lifeform_count = 5, grass_growth_rate = 0.05):
        self._dynamic_terminal = DynamicTerminal(map_size+2)
        self.max_iter = iterations
        self.time_step = timestep
        self.current_iter = 0
        self.terminated = False
        self.lifeform_count = lifeform_count
        self.map_size = map_size
        self.map = Map(map_size)
        self.lifeforms = list()
        self.grass_growth_rate = grass_growth_rate 
        self.setup()
        
    def setup(self):
        Grass.grow(self.map, self.grass_growth_rate)
        for i in range(0,self.lifeform_count):
            x = random.randint(0, self.map_size-1) 
            y = random.randint(0, self.map_size-1)
            new_life = Sheep(self.map.cells[x][y]) # Place a new sheep and not a generic lifeform.
            self.lifeforms.append(new_life)
            self.map.cells[x][y].inhabitant = new_life
        
        
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
    sim = Simulation(iterations=20,map_size = 30,lifeform_count = 50)
    while(not sim.terminated):
        sim.step()

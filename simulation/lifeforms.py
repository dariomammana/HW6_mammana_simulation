"""
Lifeforms module: Defines all creature classes in the simulation.
Classes: Lifeform (abstract base), Grass, Sheep, Wolf
"""

import string
import random
from abc import ABC


class Lifeform(ABC):
    """Abstract base class for all lifeforms in the simulation."""
    
    def __init__(self, location=None):
        self.location = location
        self._r = random.randint(0, 255)
        self._g = random.randint(0, 255)
        self._b = random.randint(0, 255)
        self.symbol = f"\x1b[38;2;{self._r};{self._g};{self._b}m{random.choice(string.ascii_letters)}\x1b[0m"
        
    def act(self, map, lifeforms=None):
        """Template method: Perform one timestep of behavior for this lifeform."""
        if self.location is None:
            return
        self.age += 1
        self.energy -= self.e_move
        self.move(map, lifeforms)
        self.eat(map, lifeforms)
        self.reproduce(map, lifeforms)
        self.survive(map, lifeforms)
    
    def move(self, map, lifeforms=None):
        """Move the lifeform to a new location if applicable."""
        pass
    
    def eat(self, map, lifeforms=None):
        """Consume resources or other lifeforms if applicable."""
        pass

    def reproduce(self, map, lifeforms=None):
        """Create offspring if conditions are met. Override in subclasses."""
        pass
    
    def survive(self, map, lifeforms=None):
        """Check survival conditions and remove lifeform if needed."""
        pass
            
    def render(self):
        """Return the display symbol for this lifeform."""
        return self.symbol


class Grass(Lifeform):
    """
    Grass is a lifeform represented by a green background.
    Does not move, eat, reproduce, or individually survive.
    Managed globally via grow() and consume() class methods.
    """
    def __init__(self):
        super().__init__(location=None)
        self.symbol = "\x1b[48;2;34;139;34m \x1b[0m"  # Green background

    def move(self, map, lifeforms=None):
        """Grass does not move."""
        pass

    def eat(self, map, lifeforms=None):
        """Grass does not eat."""
        pass

    def reproduce(self, map, lifeforms=None):
        """Grass reproduces via grow() class method."""
        pass

    def survive(self, map, lifeforms=None):
        """Grass does not individually survive/die."""
        pass

    @classmethod
    def grow(cls, map, p_g=0.05):
        """Grass grows in empty cells with probability p_g."""
        for i in range(0, map.size):
            for j in range(0, map.size):
                cell = map.cells[i][j]
                if cell.inhabitant is None and cell.state == ".":
                    if random.random() < p_g:
                        cell.state = cls().render()

    @classmethod
    def consume(cls, map):
        """Grass is consumed when a sheep occupies a cell with grass."""
        for i in range(0, map.size):
            for j in range(0, map.size):
                cell = map.cells[i][j]
                if isinstance(cell.inhabitant, Sheep) and cell.state != ".":
                    cell.state = "."


class Sheep(Lifeform):
    """
    Sheep is a herbivore represented by a white 'S'.
    Moves randomly, eats grass, reproduces when energy is sufficient,
    and dies from starvation or old age.
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
        self.symbol = "\x1b[38;2;255;255;255mS\x1b[0m"  # White 'S'
        self.energy = e_sheep_init
        self.e_grass = e_grass
        self.e_move = e_move
        self.e_sheep_reproduce = e_sheep_reproduce
        self.e_reproduce = e_sheep_reproduce
        self.max_age = max_age
        self.age = 0

    def move(self, map, lifeforms=None):
        """Sheep moves to a random adjacent cell if unoccupied."""
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
        """Sheep eats grass in its current cell."""
        if self.location and self.location.state != ".":
            self.location.state = "."
            self.energy += self.e_grass

    def reproduce(self, map, lifeforms=None):
        """Sheep reproduces when energy exceeds threshold."""
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
    Moves randomly, targets and eats sheep, reproduces when energy is sufficient,
    and dies from starvation, old age, or random chance.
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
        self.symbol = "\x1b[38;2;255;0;0mW\x1b[0m"  # Red 'W'
        self.energy = e_wolf_init
        self.e_sheep = e_sheep
        self.e_move = e_move
        self.e_wolf_reproduce = e_wolf_reproduce
        self.e_reproduce = e_wolf_reproduce
        self.max_age = max_age
        self.death_chance = death_chance
        self.age = 0
        self._last_prey = None

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

    def eat(self, map, lifeforms=None):
        """Wolf eats the sheep it caught during movement."""
        if not self._last_prey:
            return
        prey = self._last_prey
        if lifeforms and prey in lifeforms:
            lifeforms.remove(prey)
        prey.location = None
        self.energy += self.e_sheep
        self._last_prey = None

    def reproduce(self, map, lifeforms=None):
        """Wolf reproduces when energy exceeds threshold."""
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

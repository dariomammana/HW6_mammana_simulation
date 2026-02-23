"""
Environment module: Defines the simulation world (Map and Cell).
Classes: Map, Cell
"""


class Map:
    """Represents the 2D grid environment for the simulation."""
    
    def __init__(self, n=10):
        """Initialize a square map of size n x n."""
        self.size = n
        self.cells = dict()
        for i in range(0, self.size):
            self.cells[i] = dict()
            for j in range(0, self.size):
                self.cells[i][j] = Cell(i, j)
                
    def render(self):
        """Render the map as a string for display."""
        render_str = ""
        for i in range(0, self.size):
            render_str += "\n"
            for j in range(0, self.size):
                render_str += self.cells[i][j].render() + " "
        return render_str


class Cell:
    """Represents a single cell in the map."""
    
    def __init__(self, x, y):
        """Initialize a cell at position (x, y)."""
        self.x = x
        self.y = y
        self.state = "."  # "." = empty, or grass symbol
        self.inhabitant = None  # Species occupying this cell
        
    def render(self):
        """Return the visual representation of this cell."""
        if self.inhabitant:
            return self.inhabitant.render()
        else:
            return self.state

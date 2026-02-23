"""
Simulation package: Core logic for the mammana simulation.
Submodules:
- lifeforms: Lifeform classes (Lifeform, Grass, Sheep, Wolf)
- environment: Map and Cell classes
- simulation: Simulation orchestration
"""

from .lifeforms import Lifeform, Grass, Sheep, Wolf
from .environment import Map, Cell
from .simulation import Simulation

__all__ = ["Lifeform", "Grass", "Sheep", "Wolf", "Map", "Cell", "Simulation"]

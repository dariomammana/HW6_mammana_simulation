# Introduction
The Wolf‑Sheep‑Grass simulation is a minimalist predator‑prey model that couples resource consumption, energy budgets, and reproduction with space. By tweaking just a handful of parameters—grass regrow rate, energy values, reproduction thresholds—you can explore classic ecological phenomena (boom‑bust cycles, extinction, spatial clustering) and even experiment with adaptive strategies or evolutionary dynamics.

# Relevance for Object-Oriented Programming
The Wolf‑Sheep‑Grass simulation showcases why we teach OOP for AI, simulation, or software‑design courses: it gives you a real‑world problem that naturally maps to objects with state and behaviour. It lets you practice:

•	Building a class hierarchy (Animal → Wolf, Sheep)

•	Applying core principles of OOP to a dynamic system

•	Using design patterns to keep the code modular

•	Testing individual agents in isolation

To learn OOP, start by modelling that little world and watch how a handful of classes can capture an entire ecosystem. Here is a key overview over the most important entities.

|Aspect|What it is|Why it matters|
|---|---|---|
| World | 2‑D toroidal grid (cells can wrap around edges) or an infinite continuous lattice | Gives agents a “neighborhood” to move and interact in, producing spatial patterns. |
| Entities | • Grass – a renewable resource<br>• Sheep – herbivorous preys<br>• Wolves– predators of sheep | The three species interact in a closed feedback loop that mirrors Lotka‑Volterra dynamics but with space. |
| Goal | Observe how simple local rules produce complex, often self‑organising, global behaviour (population oscillations, patchiness, extinction cascades). | Useful for teaching ecology, AI, cellular‑automata, or agent‑based modeling concepts. |

# Core rules (“minimal” variant)

These rules need to be implemented in the simulation inheriting from the class `Lifeform`.

All rules are applied at each discrete time step. The order can vary (wolf step → sheep step → grass step, or all simultaneously).

## Grass
|Attribute|Typical value / behaviour|
|---|---|
|Growth|In every empty `Cell` `Grass` grows with probability `p_g` (or after a fixed “regrow time” if it was eaten).|
|Consumption|When a `Sheep` lands on a `Cell` containing `Grass`, the grass is removed.|

## Sheep
|Attribute|Typical value / behaviour|
|---|---|
|Energy|Starts with `e_sheep_init`; increases by `e_grass` when eating grass; decreases by `e_move` each move.|
|Movement|Randomly chooses one of the 8 (or 4) adjacent cells and moves there.|
|Eating|If grass is present in the new cell, the sheep eats it: `energy += e_grass`.|
|Reproduction|If `energy >= e_sheep_reproduce`, the sheep splits: it produces a new sheep in a random adjacent cell (if empty). Energy may be halved or a fraction retained.|
|Death|Dies if `energy <= 0` (starvation) or after a maximum age.|

## Wolf
|Attribute|Typical value / behaviour|
|---|---|
|Energy|Starts with `e_wolf_init`; increases by `e_sheep` when eating a sheep; decreases by `e_move` each move.|
|Movement|Same random neighbor move as sheep.|
|Hunting|If a wolf lands on a cell with a sheep, it eats the sheep: `energy += e_sheep`.|
|Reproduction|If `energy >= e_wolf_reproduce`, the wolf splits, creating a new wolf in an adjacent cell (if empty).|
|Death|Starves if `energy <= 0`; may also die of old age or random “death chance.”|


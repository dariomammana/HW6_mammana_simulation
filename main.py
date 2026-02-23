from simulation import Simulation


if __name__ == "__main__":
    # Create and run simulation
    sim = Simulation(
        iterations=20,
        map_size=30,
        sheep_count=40,
        wolf_count=20,
        grass_growth_rate=0.05
    )
    
    # Run main loop
    while not sim.terminated:
        sim.step()

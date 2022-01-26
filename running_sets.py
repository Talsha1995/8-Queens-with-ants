

Nant = 200
Niter = 1000
EVAPORATION_FACTOR = 0.85
INIT_PHERO = 1
MAX_PHERO = 100

ITERATIONS = 1
SAVE_TO_FILES = True
DEBUG = False

N8 = {
    "n": 8,
    "Nant": Nant,
    "Niter": Niter,
    "rho": EVAPORATION_FACTOR,
    "init_pheromone": 15000,
    "max_pheromone": MAX_PHERO,
    "seed": None,
}

N10 = {
    "n": 10,
    "Nant": 200,
    "Niter": Niter,
    "rho": 0.95,
    "init_pheromone": 15000,
    "max_pheromone": MAX_PHERO,
    "seed": None,
}

N12 = {
    "n": 12,
    "Nant": Nant,
    "Niter": Niter,
    "rho": 0.95,
    "init_pheromone": 15000,
    "max_pheromone": MAX_PHERO,
    "seed": None,
}

N12_2 = {
    "n": 12,
    "Nant": Nant,
    "Niter": Niter,
    "rho": 0.95,
    "init_pheromone": INIT_PHERO,
    "max_pheromone": MAX_PHERO,
    "seed": None,
}

N13 = {
    "n": 13,
    "Nant": Nant,
    "Niter": Niter,
    "rho": 0.95,
    "init_pheromone": 100,
    "max_pheromone": 100,
    "seed": None,
}

N15 = {
    "n": 15,
    "Nant": Nant,
    "Niter": Niter,
    "rho": 0.95,
    "init_pheromone": INIT_PHERO,
    "max_pheromone": 400,
    "seed": None,
}

N16 = {
    "n": 16,
    "Nant": Nant,
    "Niter": Niter,
    "rho": 0.95,
    "init_pheromone": 15000,
    "max_pheromone": MAX_PHERO,
    "seed": None,
}

N16_2 = {
    "n": 16,
    "Nant": Nant,
    "Niter": Niter,
    "rho": 0.9,
    "init_pheromone": 15000,
    "max_pheromone": MAX_PHERO,
    "seed": None,
}

N32 = {
    "n": 32,
    "Nant": Nant,
    "Niter": Niter,
    "rho": EVAPORATION_FACTOR,
    "init_pheromone": INIT_PHERO,
    "max_pheromone": MAX_PHERO,
    "seed": None,
}

N64 = {
    "n": 64,
    "Nant": Nant,
    "Niter": Niter,
    "rho": EVAPORATION_FACTOR,
    "init_pheromone": INIT_PHERO,
    "max_pheromone": MAX_PHERO,
    "seed": None,
}


running_sets = [
    N8,
    # N10,
    # N12,
    # N12_2,
    # N13,
    # N15,
    N16,
    N16_2,
    # N32,
    # N64,
]

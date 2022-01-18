


Nant = 200
Niter = 300
EVAPORATION_FACTOR = 0.9
INIT_PHERO = 1
MAX_PHERO = 30
GOOD_PATH_FACTOR = 1.05

ITERATIONS = 1
SAVE_TO_FILES = True
DEBUG = False

N8 = {
    "n": 8,
    "Nant": Nant,
    "Niter": Niter,
    "rho": EVAPORATION_FACTOR,
    "init_pheromone": INIT_PHERO,
    "max_pheromone": MAX_PHERO,
    "good_path_factor": GOOD_PATH_FACTOR,
    "seed": None,
}

N10 = {
    "n": 11,
    "Nant": Nant,
    "Niter": Niter,
    "rho": 0.9,
    "init_pheromone": INIT_PHERO,
    "max_pheromone": MAX_PHERO,
    "good_path_factor": 1.01,
    "seed": None,
}

N12 = {
    "n": 12,
    "Nant": Nant,
    "Niter": Niter,
    "rho": 0.95,
    "init_pheromone": INIT_PHERO,
    "max_pheromone": MAX_PHERO,
    "good_path_factor": 1.01,
    "seed": None,
}

N16 = {
    "n": 16,
    "Nant": Nant,
    "Niter": Niter,
    "rho": EVAPORATION_FACTOR,
    "init_pheromone": INIT_PHERO,
    "max_pheromone": MAX_PHERO,
    "good_path_factor": 1.005,
    "seed": None,
}

N32 = {
    "n": 32,
    "Nant": Nant,
    "Niter": Niter,
    "rho": EVAPORATION_FACTOR,
    "init_pheromone": INIT_PHERO,
    "max_pheromone": MAX_PHERO,
    "good_path_factor": GOOD_PATH_FACTOR,
    "seed": None,
}

N64 = {
    "n": 64,
    "Nant": Nant,
    "Niter": Niter,
    "rho": EVAPORATION_FACTOR,
    "init_pheromone": INIT_PHERO,
    "max_pheromone": MAX_PHERO,
    "good_path_factor": GOOD_PATH_FACTOR,
    "seed": None,
}


running_sets = [
    # N8,
    N10,
    # N12,
    # N16,
    # N32,
    # N64,
]

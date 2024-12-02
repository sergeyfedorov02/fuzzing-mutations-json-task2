import random
from lect9.seed_with_structure import SeedWithStructure

exponent = 2


def assign_energy(population):
    for seed in population:
        frequency = seed.get_path_frequency()
        seed.set_energy(1 / (frequency ** exponent))


def normalized_energy(population):
    total_energy = sum(seed.energy for seed in population)
    return [seed.energy / total_energy for seed in population] if total_energy > 0 else [0] * len(population)


def choose(population) -> SeedWithStructure:
    assign_energy(population)

    norm_energy = normalized_energy(population)

    total_weight = sum(norm_energy)

    random_value = random.uniform(0, total_weight)

    population_list = list(population)

    for i in range(len(population_list)):
        random_value -= norm_energy[i]
        if random_value <= 0:
            return population_list[i]

    return population_list[-1]
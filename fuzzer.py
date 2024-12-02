import random
from typing import Self
from random import randint
from power_schedule import choose

from lect9.seed_with_structure import SeedWithStructure
from lect9.fragment_mutator import FragmentMutator

from lect9.fuzz_mutator import (
    insert_random_character,
    delete_random_character,
    flip_random_character,
    append,
    delete
)

from runner import Runner, RunnerResult
from json_my.json_parser import loads


class GreyBoxGrammarFuzzer:
    def __init__(
            self: Self,
            seed: set[SeedWithStructure],
            fragment_mutator: FragmentMutator,
            min_mutations: int,
            max_mutations: int,
            max_nonterminals: int,
            max_expansion_trials: int,
            runner: Runner,
            count: int,
    ) -> None:
        self.seed = seed
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        self.max_nonterminals = max_nonterminals
        self.max_expansion_trials = max_expansion_trials
        self.fragment_mutator = fragment_mutator
        self.runner = runner
        self.count = count

        self.population = seed
        self.input_candidate = None
        self.covered_lines = None
        self.result_status = None

        self.pass_result = 0
        self.fail_result = 0

        self.chosen_candidate = None
        self.candidate_after_fragment_mutator = None
        self.candidate_after_mutations = None
        self.candidate_after_delta_debugging = None

    def mutate(self, individual: str) -> str:
        turn = randint(1, 1)
        match turn:
            case 1:
                turn2 = randint(1, 3)
                match turn2:
                    case 1:
                        return insert_random_character(individual)
                    case 2:
                        return delete_random_character(individual)
                    case 3:
                        return flip_random_character(individual)
            case 2:
                turn2 = randint(1, 1)
                match turn2:
                    case 1:
                        return append(individual, self.max_nonterminals, self.max_expansion_trials)
                    case 2:
                        return delete(individual)

    def create_candidate(self: Self) -> SeedWithStructure:
        candidate = choose(self.population)
        self.input_candidate = candidate

        mutation_candidate_seed = SeedWithStructure(candidate.get_data())

        trials = randint(self.min_mutations, self.max_mutations)

        self.chosen_candidate = mutation_candidate_seed.get_data()

        for _ in range(trials):
            new_mutation_candidate_seed = self.fragment_mutator.mutate(mutation_candidate_seed)
            mutation_candidate_seed = SeedWithStructure(new_mutation_candidate_seed.get_data())

        self.candidate_after_fragment_mutator = mutation_candidate_seed.get_data()

        if not mutation_candidate_seed.get_has_structure() or random.randint(0, 1) == 1:
            dumb_trials = min(len(mutation_candidate_seed.get_data()), 1 << (random.randint(0, 5) + 1))
            for _ in range(dumb_trials):
                if isinstance(mutation_candidate_seed, SeedWithStructure):
                    new_data = self.mutate(mutation_candidate_seed.get_data())
                    mutation_candidate_seed.set_data(new_data)

        self.candidate_after_mutations = mutation_candidate_seed.get_data()

        return mutation_candidate_seed

    def run_candidate(self: Self, candidate: SeedWithStructure) -> RunnerResult:
        if isinstance(candidate, SeedWithStructure):
            _, result = self.runner.run(candidate.get_data())
            self.result_status = result
            candidate.set_result(result)

            self.boosted_grey_box_fuzzer(candidate, result)

            return result

    def set_covered_lines_for_candidate(self: Self, candidate: SeedWithStructure):
        all_covered_lines = set()
        for (filename, func_name), coverage in self.runner.coverage_tracker.functions_coverage.items():
            covered_lines = self.runner.coverage_tracker.covered_lines_per_function[(filename, func_name)]
            all_covered_lines.update(covered_lines)
        candidate.set_covered_lines(all_covered_lines)

    def set_covered_lines_for_seed(self: Self, candidate: SeedWithStructure):
        if self.covered_lines is None:
            self.covered_lines = candidate.get_covered_lines()
        elif self.input_candidate is None:
            current_covered_lines = self.covered_lines
            new_covered_lines = candidate.get_covered_lines()
            difference_lines = current_covered_lines.difference(new_covered_lines)
            if difference_lines:
                self.covered_lines.update(difference_lines)

    def boosted_grey_box_fuzzer(self: Self, candidate: SeedWithStructure, result: RunnerResult):
        # if result != RunnerResult.FAIL:
        self.set_covered_lines_for_candidate(candidate)
        candidate.set_path_frequency(1)

        # Установка значения covered_lines при прохождении начального seed
        self.set_covered_lines_for_seed(candidate)

        # Получим значение покрытых строк текущим кандидатом
        candidate_covered_lines = candidate.get_covered_lines()

        # Добавление кандидата в population
        if self.input_candidate is not None:
            different_lines = candidate_covered_lines.difference(self.covered_lines)

            # если путь повторяется -> увеличим path_id
            for individual in self.population:
                individual_covered_lines = individual.get_covered_lines()
                if candidate_covered_lines == individual_covered_lines:
                    new_path_frequency = individual.get_path_frequency() + 1
                    individual.set_path_frequency(new_path_frequency)

            # если открыли новое покрытие (новые функции) -> добавляем
            if different_lines:
                self.fragment_mutator.add_to_fragment_pool(candidate)

                if candidate.get_has_structure():
                    new_data = self.delta_debugging(candidate)
                    candidate.set_data(new_data)
                    self.candidate_after_delta_debugging = new_data

                    print()
                    print(f"Chosen candidate: {self.chosen_candidate}")
                    print(f"Candidate after FragmentMutator: {self.candidate_after_fragment_mutator}")
                    print(f"Candidate after Mutations: {self.candidate_after_mutations}")
                    print(f"Candidate after Delta Debugging: {self.candidate_after_delta_debugging}")

                    self.population.add(candidate)

                self.covered_lines.update(different_lines)

    def nothing_changed(self: Self, candidate: SeedWithStructure, new_str: str) -> bool:
        new_runner = Runner(loads)
        _, new_result = new_runner.run(new_str)

        if new_result == self.result_status:
            all_covered_lines = set()
            for (filename, func_name), coverage in new_runner.coverage_tracker.functions_coverage.items():
                covered_lines = new_runner.coverage_tracker.covered_lines_per_function[(filename, func_name)]
                all_covered_lines.update(covered_lines)

            if candidate.get_covered_lines() == all_covered_lines:
                return True

        return False

    def delta_debugging(self: Self, candidate: SeedWithStructure) -> str:
        current = candidate.get_data()
        n = 2  # Начальное количество фрагментов

        while n <= len(current):
            # Разбиваем строку на `n` фрагментов
            chunks = [current[i:i + len(current) // n] for i in range(0, len(current), len(current) // n)]
            if len(chunks) > n:  # Если осталось меньше символов, добавим их в последний фрагмент
                chunks[-2] += chunks[-1]
                chunks.pop()

            reduced = False
            for i in range(len(chunks)):
                # Пробуем исключить фрагмент
                without_chunk = ''.join(chunks[:i] + chunks[i + 1:])

                if self.nothing_changed(candidate, without_chunk):
                    # Если исключение фрагмента не изменило результат, "обрезаем" строку
                    current = without_chunk
                    n = max(n - 1, 2)  # Уменьшаем количество фрагментов
                    reduced = True
                    break

            if not reduced:  # Если не удалось упростить данные, увеличиваем количество фрагментов
                if n == len(current):
                    break
                n = min(n * 2, len(current))

        return current

    def run_seed(self: Self) -> None:
        for candidate in self.population:
            self.run_candidate(candidate)

    def run(self: Self) -> None:
        candidate = self.create_candidate()
        result = self.run_candidate(candidate)

        data_population_list = [pop_seed.data for pop_seed in self.population]

        # print(
        #     f"Candidate: {self.input_candidate.get_data()}  "
        #     f"Mutations: {candidate.get_data()}  ",
        #     f"Population: {data_population_list}  ",
        #     f"Candidate Status: {result}",
        # )

    def fuzz(self: Self) -> None:
        self.run_seed()
        for i in range(self.count):
            self.run()
            if self.result_status == RunnerResult.PASS:
                self.pass_result += 1
            else:
                self.fail_result += 1

from json_my.json_grammar import JsonGrammar
from simple_grammar_fuzzer import simple_grammar_fuzzer, ExpansionError
from json_my.json_parser import loads

from runner import Runner
from fuzzer import GreyBoxGrammarFuzzer

from lect9.seed_with_structure import SeedWithStructure
from lect9.fragment_mutator import FragmentMutator
from lect9.ast_derivation_tree_converter import ASTToDerivationTreeConverter

from lect6.derivation_tree_printer import DerivationTreePrinter

from antlr4 import *
from parser_antlr.JSONLexer import JSONLexer
from parser_antlr.JSONParser import JSONParser


# import json_my


def test_json_grammar():
    try:
        res = simple_grammar_fuzzer(JsonGrammar.JSON_GRAMMAR, JsonGrammar.START_SYMBOL, 6, 100, True)
        print("GENERATED EXPRESSION =", res)

    except ExpansionError as e:
        print(f"Error: {e}")


def create_initial_seed(current_seed_size):
    seed = []
    for _ in range(current_seed_size):
        try:
            new_seed_element = simple_grammar_fuzzer(JsonGrammar.JSON_GRAMMAR, JsonGrammar.START_SYMBOL, 6, 100, False)
            seed.append(new_seed_element)
        except ExpansionError as e:
            print(f"Error: {e}")

    return seed


def print_stats(runner, result, status):
    print("Json content:", result)
    print("\nStatus:", status)

    # Вывод статистики покрытия по каждой функции
    print("\nFunction Coverage (functions and lines covered/total lines):")
    for (filename, func_name), coverage in runner.coverage_tracker.functions_coverage.items():
        total_lines = runner.coverage_tracker.total_lines_per_function[(filename, func_name)]
        covered_lines = runner.coverage_tracker.covered_lines_per_function[(filename, func_name)]
        print(f"{func_name} : {coverage} covered / {total_lines} total")
        print(f"  Covered lines: {sorted(covered_lines)}")  # Выводим номера покрытых строк, сортируя для удобства


def test_coverage():
    runner = Runner(loads)
    seed = create_initial_seed(1)
    result, status = runner.run(seed[0])
    print_stats(runner, result, status)


def print_population_coverage(cur_fuzzer):
    print("Population content after fuzzing:")
    for individual in cur_fuzzer.population:
        print(f"\nJson content: {individual.get_data()}")
        print(f"Json result: {individual.get_result()}")
        print(f"Coverage: {len(individual.get_covered_lines())}/{119}")
        print(f"Covered lines: {individual.get_covered_lines()}")


def test_fragment_mutator():
    text = '{ "key": "value", "key_arr": [1, 2], "nested_obj": {"nested_key": "nested_value", "another_key": ["item1", "item2"]}, "boolean_value": true }'
    text2 = '{ "key": "value", "boolean_value": true }'
    text3 = '[4, 5, [1, 2]]'
    text4 = '{"key": "value", "boolean_value": true, "1":[4, 5, [1, 2]]}'

    # Создание лексера и парсера
    char_stream = InputStream(text4)
    lexer = JSONLexer(char_stream)
    tokens = CommonTokenStream(lexer)
    parser = JSONParser(tokens)

    # Запуск парсинга
    tree = parser.json()
    derivation_tree = ASTToDerivationTreeConverter.convert(tree)
    DerivationTreePrinter.print_tree(derivation_tree)

    valid_seed = SeedWithStructure(text4)
    print(valid_seed.get_data())

    init_set = set()
    init_set.add("<json>")

    mutator = FragmentMutator(parser, init_set)

    new_seed = mutator.mutate(valid_seed)
    print(new_seed.get_data())


def test_json_fuzzer(amount):
    text = '{ "key": "value", "key_arr": [1, 2], "nested_obj": {"nested_key": "nested_value", "another_key": ["item1", "item2"]}, "boolean_value": true }'

    # Создание лексера и парсера
    char_stream = InputStream(text)
    lexer = JSONLexer(char_stream)
    tokens = CommonTokenStream(lexer)
    parser = JSONParser(tokens)

    # Запуск парсинга
    tree = parser.json()
    derivation_tree = ASTToDerivationTreeConverter.convert(tree)
    DerivationTreePrinter.print_tree(derivation_tree)

    valid_seed_set = set()
    valid_seed = SeedWithStructure(text)
    valid_seed_set.add(valid_seed)

    init_set = set()
    init_set.add("<json>")

    mutator = FragmentMutator(parser, init_set)
    runner = Runner(loads)

    fuzzer = GreyBoxGrammarFuzzer(
        seed=valid_seed_set,
        fragment_mutator=mutator,
        min_mutations=1,
        max_mutations=3,
        max_nonterminals=6,
        max_expansion_trials=100,
        runner=runner,
        count=amount,
    )
    fuzzer.fuzz()

    print(f"\nPASS = {fuzzer.pass_result}")
    print(f"FAIL = {fuzzer.fail_result}\n")

    print_population_coverage(fuzzer)


if __name__ == '__main__':
    count = 10_000

    # test_coverage()
    # test_fragment_mutator()
    test_json_fuzzer(count)

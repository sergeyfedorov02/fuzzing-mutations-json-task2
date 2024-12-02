import random

from json_my.json_grammar import JsonGrammar


class ExpansionError(Exception):
    def __init__(self, message):
        super().__init__(message)


def simple_grammar_fuzzer(grammar, start_symbol, max_nonterminals, max_expansion_trials, log):
    term = start_symbol
    expansion_trials = 0

    while JsonGrammar.non_terminals(term):
        symbol_to_expand = random.choice(JsonGrammar.non_terminals(term))
        expansions = grammar[symbol_to_expand]
        expansion = random.choice(expansions)

        new_term = term.replace(symbol_to_expand, expansion, 1)

        if len(JsonGrammar.non_terminals(new_term)) < max_nonterminals:
            term = new_term

            if log:
                print(f"{symbol_to_expand: <40} {term}")

            expansion_trials = 0
        else:
            expansion_trials += 1
            if expansion_trials >= max_expansion_trials:
                raise ExpansionError(f"Cannot expand {term}")

    return term
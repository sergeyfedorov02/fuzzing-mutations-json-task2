from json.json_grammar import JsonGrammar
from simple_grammar_fuzzer import simple_grammar_fuzzer, ExpansionError
from random import randint


def create_new(initial: str, cur_max_nonterminals: int, cur_max_expansion_trials: int):
    if not initial:
        return ""

    result = ""
    except_flag = True

    while except_flag:
        try:
            result = simple_grammar_fuzzer(JsonGrammar.JSON_GRAMMAR, JsonGrammar.START_SYMBOL, cur_max_nonterminals,
                                           cur_max_expansion_trials, False)
            except_flag = False
        except ExpansionError as e:
            # print(f"Error: {e}")
            except_flag = True

    return result


def append(initial: str, max_nonterm, max_exp_trials):
    if not initial:
        return ""

    new_json = create_new(initial, max_nonterm, max_exp_trials)

    while initial[0] == "{" and new_json[0] == "[":
        new_json = create_new(initial, max_nonterm, max_exp_trials)

    with_brackets = initial[:len(initial) - 2] + ", " + new_json + initial[len(initial) - 2:]
    without_brackets = initial[:len(initial) - 2] + ", " + new_json[1:len(new_json) - 1] + initial[len(initial) - 2:]

    if initial[0] == "{" and new_json[0] == "{" or initial[0] == "[" and new_json[0] == "[":
        return without_brackets
    else:
        return with_brackets


def delete(initial: str):
    if not initial:
        return ""

    if len(initial) <= 2:
        return initial

    random_pos = randint(1, len(initial) - 2)

    return initial[:random_pos] + initial[random_pos + 1:]
import random
from concurrent.futures import ThreadPoolExecutor, Future, TimeoutError
import re
from collections import defaultdict

from lect6.derivation_tree_node import DerivationTreeNode
from lect6.grammar_utils import GrammarUtils
from lect9.seed_with_structure import SeedWithStructure
from lect9.fuzz_parser import FuzzParser


class FragmentMutator:
    """ Mutate inputs with input fragments from a pool """

    def __init__(self, parser, tokens: set[str]):
        self.parser = parser
        self.tokens = tokens
        self.fragments = defaultdict(list)
        self.seen_seeds = []
        self.to_swap = 0
        self.to_delete = 0

        for rule_name in parser.ruleNames:
            self.fragments[f"<{rule_name.lower()}>"] = []

    def add_fragment(self, fragment: DerivationTreeNode):
        """ Recursively adds fragments to the fragment pool """
        symbol = fragment.get_value()
        children = fragment.get_children()

        if not self.is_excluded(symbol):
            self.fragments[symbol].append(fragment)
            if children:
                for subfragment in children:
                    self.add_fragment(subfragment)

    def is_excluded(self, symbol: str) -> bool:
        """ Returns true if a fragment starting with a specific symbol and all its descendants can be excluded """
        if symbol not in self.fragments:
            return True
        if symbol in self.tokens:
            return True
        if not GrammarUtils.is_non_terminal(symbol):
            return True
        return False

    def add_to_fragment_pool(self, seed: SeedWithStructure):
        """ Adds all fragments of a seed to the fragment pool """
        try:
            parsed = self.exec_task(seed.get_data())
            seed.set_structure(parsed)
            self.add_fragment(seed.get_structure())
            seed.set_has_structure(True)
        except Exception:
            seed.set_has_structure(False)

    def exec_task(self, data: str) -> DerivationTreeNode:
        """ Executes parsing in a separate thread with a timeout """
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(lambda: FuzzParser.parse(data))
            try:
                return future.result(timeout=0.8)  # 800 milliseconds
            except TimeoutError:
                raise Exception("Parsing timed out")

    def mutate(self, seed: SeedWithStructure) -> SeedWithStructure:
        if seed not in self.seen_seeds:
            self.seen_seeds.append(seed)
            self.add_to_fragment_pool(seed)

        if random.random() > 0.5:
            return self.delete_fragment(seed)
        else:
            return self.delete_fragment(seed)

    def count_nodes(self, fragment: DerivationTreeNode) -> int:
        symbol = fragment.get_value()
        children = fragment.get_children()

        if self.is_excluded(symbol):
            return 0

        assert children is not None
        return 1 + sum(self.count_nodes(child) for child in children)

    def recursive_swap(self, fragment: DerivationTreeNode) -> DerivationTreeNode:
        """ Recursively finds the fragment to swap """
        symbol = fragment.get_value()
        children = fragment.get_children()

        if self.is_excluded(symbol):
            return DerivationTreeNode(symbol, children)

        self.to_swap -= 1
        if self.to_swap == 0:
            fragment_list = self.fragments[symbol]
            return random.choice(fragment_list)

        assert children is not None
        new_children = [self.recursive_swap(child) for child in children]
        return DerivationTreeNode(symbol, new_children)

    def swap_fragment(self, seed: SeedWithStructure) -> SeedWithStructure:
        """ Substitutes a random fragment with another with the same symbol """
        if seed.get_has_structure():
            n_nodes = self.count_nodes(seed.get_structure())

            if n_nodes < 2:
                self.to_swap = n_nodes
            else:
                self.to_swap = random.randint(2, n_nodes)

            new_structure = self.recursive_swap(seed.get_structure())
            new_seed = SeedWithStructure(new_structure.all_terminals())
            new_seed.set_has_structure(True)
            new_seed.set_structure(new_structure)

            return new_seed

        return seed

    def recursive_delete(self, fragment: DerivationTreeNode) -> DerivationTreeNode:
        """ Recursively finds the fragment to delete """
        symbol = fragment.get_value()
        children = fragment.get_children()

        if self.is_excluded(symbol):
            return DerivationTreeNode(symbol, children)

        self.to_delete -= 1
        if self.to_delete == 0:
            # return DerivationTreeNode(symbol,[])
            return self.empty_node(symbol)

        assert children is not None
        new_children = [self.recursive_delete(child) for child in children]
        return DerivationTreeNode(symbol, new_children)

    def delete_fragment(self, seed: SeedWithStructure) -> SeedWithStructure:
        """ Delete a random fragment """
        if seed.get_has_structure():
            n_nodes = self.count_nodes(seed.get_structure())

            if n_nodes < 2:
                self.to_delete = n_nodes
            else:
                self.to_delete = random.randint(2, n_nodes)

            new_structure = self.recursive_delete(seed.get_structure())
            new_seed = SeedWithStructure(new_structure.all_terminals())
            new_seed.set_has_structure(True)
            new_seed.set_structure(new_structure)

            # Do not return an empty new_seed
            if new_seed.get_data() == "":
                return seed
            else:
                return new_seed

        return seed

    def empty_node(self, symbol: str) -> DerivationTreeNode:
        if symbol == "<pair>":
            return DerivationTreeNode(symbol, [DerivationTreeNode(f"\"deleted_key\"", []), DerivationTreeNode(": ", []),
                                               DerivationTreeNode("deleted_value", [])])
        elif symbol == "<arr>":
            return DerivationTreeNode(symbol, [DerivationTreeNode("[", []), DerivationTreeNode("]", [])])

        return DerivationTreeNode(symbol, [DerivationTreeNode("0", [])])

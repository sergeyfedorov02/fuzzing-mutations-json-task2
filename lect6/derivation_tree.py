from lect6.grammar_utils import GrammarUtils


class DerivationTree:
    def __init__(self, root):
        self.root = root

    def get_root(self):
        return self.root

    def all_terminals(self):
        return self.root.all_terminals()

    def tree_to_string(self):
        return self.tree_to_string_helper(self.root)

    def tree_to_string_helper(self, node):
        symbol = node.get_value()
        children = node.get_children()

        if children is not None and children:
            result = []
            for child in children:
                result.append(self.tree_to_string_helper(child))
            return ''.join(result)
        else:
            # Проверяем, является ли символ нетерминалом
            return '' if GrammarUtils.is_non_terminal(symbol) else symbol
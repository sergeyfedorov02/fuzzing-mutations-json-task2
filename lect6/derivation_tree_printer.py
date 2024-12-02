from lect6.derivation_tree import DerivationTree
from lect6.derivation_tree_node import DerivationTreeNode


class DerivationTreePrinter:

    @staticmethod
    def print_tree(tree: DerivationTree):
        """Prints the entire derivation tree using the tree object."""
        DerivationTreePrinter.print_node(tree.get_root().get_value(), tree.get_root().get_children(), 0)

    @staticmethod
    def print_tree_node(node: DerivationTreeNode):
        """Prints the tree starting from a specific node."""
        DerivationTreePrinter.print_node(node.get_value(), node.get_children(), 0)

    @staticmethod
    def print_node(symbol, children, level):
        """Recursively prints the node and its children with indentation based on the level."""
        indent = "  " * level  # Используем пробелы для отступа
        print(indent + symbol)  # Печатаем символ с заданным отступом

        # Если есть дочерние узлы, рекурсивно выводим их
        if children is not None and len(children) > 0:
            for child in children:
                DerivationTreePrinter.print_node(child.get_value(), child.get_children(), level + 1)
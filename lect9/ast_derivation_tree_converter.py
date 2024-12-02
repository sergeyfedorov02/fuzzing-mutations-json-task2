from lect6.derivation_tree_node import DerivationTreeNode
from lect6.derivation_tree import DerivationTree
from antlr4 import *


class ASTToDerivationTreeConverter:
    @staticmethod
    def convert(ast_root):
        """ Convert the root of an AST to a DerivationTree. """
        root = ASTToDerivationTreeConverter.convert_node(ast_root)
        return DerivationTree(root)

    @staticmethod
    def convert_node(node):
        """ Recursively convert a ParseTree node to a DerivationTreeNode. """

        if isinstance(node, TerminalNode):
            value = node.__str__()
        else:
            # Получаем имя класса и формируем значение
            value = f"<{node.__class__.__name__.replace('Context', '').lower()}>"

        # Получаем дочерние узлы
        children = []
        for i in range(node.getChildCount()):
            child = node.getChild(i)
            child_node = ASTToDerivationTreeConverter.convert_node(child)
            children.append(child_node)

        return DerivationTreeNode(value, children)
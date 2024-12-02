import sys
from antlr4 import *
from parser_antlr.JSONLexer import JSONLexer
from parser_antlr.JSONParser import JSONParser

from lect9.ast_derivation_tree_converter import ASTToDerivationTreeConverter


class FuzzParser:
    @staticmethod
    def parse(input_string):
        """ Parse the given input string and return the root of the derivation tree. """

        # Создание лексера и парсера
        char_stream = InputStream(input_string)
        lexer = JSONLexer(char_stream)
        tokens = CommonTokenStream(lexer)
        parser = JSONParser(tokens)

        # Запуск парсинга
        tree = parser.json()  # Начинаем с правила json_my

        # Преобразование AST в дерево выводов
        derivation_tree = ASTToDerivationTreeConverter.convert(tree)

        d1 = derivation_tree.get_root()
        d2 = d1.get_children()[0]
        d3 = d2.get_children()[0]

        return d3
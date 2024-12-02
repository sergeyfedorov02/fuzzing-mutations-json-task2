import re


class JsonGrammar:
    START_SYMBOL = "<start>"

    PAIR_SYMBOL = "<pair>"

    JSON_GRAMMAR = {
        "<start>": [
            "<object>",
            "<array>"
        ],
        "<value>": [
            "<object>",
            "<array>",
            "<literal>",
            "<string>",
            "<number>"
        ],
        "<literal>": [
            "true",
            "false",
            "null"
        ],
        "<object>": [
            "{ <members> }"
        ],
        "<members>": [
            "<pair>",
            "<pair>, <members>"
        ],
        "<pair>": [
            "<string>: <value>"
        ],
        "<array>": [
            "[ <elements> ]"
        ],
        "<elements>": [
            "<value>",
            "<value>, <elements>"
        ],
        "<string>": [
            '"<chars>"'
        ],
        "<chars>": [
            "<char><chars>",
            ""
        ],
        "<char>": [
            # Здесь могут быть добавлены специальные символы и escape-последовательности
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
            "u", "v", "w", "x", "y", "z",  # маленькие буквы
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
            "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
            "U", "V", "W", "X", "Y", "Z",  # большие буквы
            # "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",  # цифры
            "-", "_", "@"
            # " ", "!", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",",
            # "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~",
            # r'\\\"', r'\\\\', r'\\b', r'\\f', r'\\n', r'\\r', r'\\t'  # escape-последовательности
        ],
        # "<char>": [
        #     *{chr(index) for index in range(0x0020, 0x10FFFF + 1) if chr(index) != '"' and chr(index) != "\\"}
        # ],
        "<number>": [
            "<int>",
            "<int>.<fraction>",
            "<int>.<fraction>e<sign><int>",
            "<int>e<sign><int>"
        ],
        "<int>": [
            "0",
            "<digit>",
            "<digit><int>"
        ],
        "<fraction>": [
            "<digit><digits>"
        ],
        "<digits>": [
            "<digit>",
            "<digit><digits>"
        ],
        "<digit>": [
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
        ],
        "<sign>": [
            "", "+", "-"  # знак может быть пропущен или быть +/-
        ]
    }

    RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')

    @staticmethod
    def non_terminals(expansion):
        expansion_str = expansion[0] if isinstance(expansion, (list, tuple)) else str(expansion)
        return JsonGrammar.RE_NONTERMINAL.findall(expansion_str)

    @staticmethod
    def is_non_terminal(s):
        return bool(JsonGrammar.RE_NONTERMINAL.match(s))
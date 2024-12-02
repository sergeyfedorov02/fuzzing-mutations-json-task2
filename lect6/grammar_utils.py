import re


class GrammarUtils:
    RE_NONTERMINAL = re.compile(r'<[^<> ]*>')

    @staticmethod
    def is_non_terminal(s):
        return bool(GrammarUtils.RE_NONTERMINAL.match(s))

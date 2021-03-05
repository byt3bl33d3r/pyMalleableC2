import pathlib
import pkg_resources
from lark import Lark, Tree, Token
from lark.reconstruct import Reconstructor

_grammar_file_path = pathlib.Path(
    pkg_resources.resource_filename(__name__, "grammar.lark")
)

_lark_parser = Lark.open(_grammar_file_path, parser="lalr") # LALR parser is faster than the default one

_reconstructor = Reconstructor(_lark_parser)

class Profile:
    def __init__(self, ast):
        self.ast = ast

    @classmethod
    def from_scratch(cls):
        return cls(
            Tree("start", [])
        )

    @classmethod
    def from_file(cls, profile_path):
        profile_path = pathlib.Path(profile_path)
        with profile_path.open() as profile:
            return cls(
                _lark_parser.parse(profile.read())
            )

    @classmethod
    def from_string(cls, profile_code):
        return cls(_lark_parser.parse(profile_code))

    def set_option(self, option_name, value):
        tree = Tree('global_option_set',
            [
                Token('GLOBAL_OPTION', option_name), 
                Tree('string',
                    [
                        Token('ESCAPED_STRING', f'"{value}"')
                    ]
                ),
                Token('DELIM', ';')
            ]
        )
        self.ast.children.append(tree)

    def add_code_block(self, tree):
        self.ast.children.append(tree.ast)

    def _postproc_indent(self, items):
        """
        Lark doesn't preserve whitespaces and has no way of keeping track of them in the AST so you need to build your grammar accordingly if you need/want them.
        This function's sole purpose is to output 'pretty' source code with indentation/spacing so your eyes don't bleed when you try to read the reconstructed profile.
        """
        stack = []
        indent_char = " "
        indent_n = 0

        yield "# Automatically generated with pyMalleableC2\n"
        yield "# https://github.com/Porchetta-Industries/pyMalleableC2\n"
        yield "#\n"
        yield "# !!! Make sure to run this profile through c2lint before using !!!\n"
        yield "\n"

        for item in items:
            if isinstance(item, Token) and item.type == "BEGIN_CODE_BLOCK_DELIM":
                stack.append(" " + item + "\n")
                indent_n += 4

            elif isinstance(item, Token) and item.type == "END_CODE_BLOCK_DELIM":
                indent_n -= 4
                stack.append( (indent_char * indent_n) + item + "\n" )

            elif isinstance(item, Token) and item.type == "DELIM":
                stack.append(item + "\n")

            elif isinstance(item, Token) and item.type == "ESCAPED_STRING":
                stack.append(" " + item)

            elif isinstance(item, Token) and item.type.endswith("LOCAL_OPTION"):
                stack.append(item)
            else:
                stack.append( (indent_char * indent_n) + item )

            yield " ".join(stack)
            stack = []

    def reconstruct(self, postproc=None):
        return _reconstructor.reconstruct(
            self.ast,
            postproc or self._postproc_indent
        )

    def __str__(self):
        return self.reconstruct()

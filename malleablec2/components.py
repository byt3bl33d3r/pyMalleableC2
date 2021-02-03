from lark import Token, Tree

class CodeBlock:
    def set_option(self, name, value):
        raise NotImplementedError

    def add_statement(self, name, *values):
        statement_values = [
            Tree('string',
                [   
                    Token('ESCAPED_STRING', f'"{value}"')
                ]
            ) for value in values
        ]

        tree = Tree(
            name, statement_values
        )

        tree.children[0].append(Token('DELIM', ';'))
        self.ast.append(tree)

    def add_code_block(self, tree):
        self.ast.children.append(tree)

class IdBlock(CodeBlock):
    def __init__(self):
        self.ast = Tree('id',
            [
                Tree('id_block',
                    [
                        Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                        Token('END_CODE_BLOCK_DELIM', '}')
                    ]
                )
            ]
        )

class OutputBlock(CodeBlock):
    def __init__(self):
        self.ast = Tree('output',
            [
                Tree('output_block',
                    [
                        Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                        Token('END_CODE_BLOCK_DELIM', '}')
                    ]
                )
            ]
        )

class MetadataBlock(CodeBlock):
    def __init__(self):
        self.ast = Tree('metadata',
            [
                Tree('metadata_block',
                    [
                        Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                        Token('END_CODE_BLOCK_DELIM', '}')
                    ]
                )
            ]
        )

class ClientBlock(CodeBlock):
    def __init__(self):
        self.ast = Tree('client',
            [
                Tree('client_block',
                    [
                        Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                        Token('END_CODE_BLOCK_DELIM', '}')
                    ]
                )
            ]
        )

class ServerBlock(CodeBlock):
    def __init__(self):
        self.ast = Tree('server',
            [
                Tree('server_block',
                    [
                        Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                        Token('END_CODE_BLOCK_DELIM', '}')
                    ]
                )
            ]
        )

class HttpPostBlock(CodeBlock):
    def __init__(self, variant_name=None):
        self.ast = Tree("http_post",
            [
                Tree(f"http_post_block",
                    [
                        Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                        Token('END_CODE_BLOCK_DELIM', '}')
                    ]
                )
            ]
        )

        if variant_name:
            self.ast.children[0].insert(0,
                Tree('string',
                    [
                        Token('ESCAPED_STRING', f'"{variant_name}"')
                    ]
                )
            )

    def set_option(self, name, value):
        tree = Tree(
            'local_option_set', 
            [   
                Token('HTTP_LOCAL_OPTION', f'{name}'),
                Tree('string',
                    [
                        Token('ESCAPED_STRING', f'"{value}"')
                    ]
                ),
                Token('DELIM', ';')
            ]
        )

        self.ast.append(tree)

class HttpGetBlock(CodeBlock):
    def __init__(self, variant_name=None):
            self.ast = Tree("http_get",
                [
                    Tree(f"http_get_block",
                        [
                            Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                            Token('END_CODE_BLOCK_DELIM', '}')
                        ]
                    )
                ]
            )

            if variant_name:
                self.ast.children[0].insert(0,
                    Tree('string',
                        [
                            Token('ESCAPED_STRING', f'"{variant_name}"')
                        ]
                    )
                )
    
    def set_option(self, name, value):
        tree = Tree(
            'local_option_set', 
            [   
                Token('HTTP_LOCAL_OPTION', f'{name}'),
                Tree('string',
                    [
                        Token('ESCAPED_STRING', f'"{value}"')
                    ]
                ),
                Token('DELIM', ';')
            ]
        )

        self.ast.append(tree)

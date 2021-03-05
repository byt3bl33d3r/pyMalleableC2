from lark import Token, Tree

class CodeBlock:
    def set_option(self, name, value):
        if not hasattr(self, 'option_block_token') or not self.option_block_token:
            raise NotImplementedError

        tree = Tree('local_option_set',
            [Token(self.option_block_token, f'{name}'), Tree('string', [Token('ESCAPED_STRING', f'"{value}"')]), Token('DELIM', ';')]
        )

        self.ast.children[0].children.insert(-1, tree)

    def add_statement(self, name, *values):
        tree = Tree(f'{name}', [])

        if values:
            inner_tree = [
                Tree('string', [ Token('ESCAPED_STRING', f'"{value}"') ])
                for value in values
            ]
            inner_tree.append(Token('DELIM', ';'))
            tree.children.extend(inner_tree)
        else:
            tree.children.append(Token('DELIM', ';'))

        self.ast.children[0].children.insert(-1, tree)

    def add_code_block(self, tree):
        self.ast.children[0].children.insert(-1, tree.ast)

class HttpGetBlock(CodeBlock):
    def __init__(self, variant_name=None):
        self.option_block_token = 'HTTP_LOCAL_OPTION'
        self.ast = Tree("http_get",
        [
            Tree(f"http_get_block",
                [
                    Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                    Token('END_CODE_BLOCK_DELIM', '}')
                ])
        ])

        if variant_name:
            self.ast.children[0].insert(0,
                Tree('string',
                    [ Token('ESCAPED_STRING', f'"{variant_name}"')]
                )
            )

class HttpPostBlock(CodeBlock):
    def __init__(self, variant_name=None):
        self.option_block_token = 'HTTP_LOCAL_OPTION'
        self.ast = Tree("http_post",
        [
            Tree(f"http_post_block",
            [
                    Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                    Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])

        if variant_name:
            self.ast.children[0].insert(0,
                Tree('string',
                    [ Token('ESCAPED_STRING', f'"{variant_name}"') ]
                )
            )

class ClientBlock(CodeBlock):
    def __init__(self):
        self.ast = Tree('client',
        [
            Tree('client_block',
            [
                Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])

class IdBlock(CodeBlock):
    def __init__(self):
        self.ast = Tree('id',
        [
            Tree('id_block',
            [
                Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])

class DnsBeaconBlock(CodeBlock):
    def __init__(self):
        self.option_block_token = 'DNS_BEACON_LOCAL_OPTION'
        self.ast = Tree('dns_beacon',
        [
            Tree('dns_beacon_block', 
            [
                Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])

class OutputBlock(CodeBlock):
    def __init__(self):
        self.ast = Tree('output',
        [
            Tree('output_block',
            [
                Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])

class MetadataBlock(CodeBlock):
    def __init__(self):
        self.ast = Tree('metadata',
        [
            Tree('metadata_block',
            [
                Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])

class ServerBlock(CodeBlock):
    def __init__(self):
        self.ast = Tree('server',
        [
            Tree('server_block',
            [
                Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])
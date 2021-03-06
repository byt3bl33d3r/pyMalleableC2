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

class HttpConfigBlock(CodeBlock):
    def __init__(self):
        self.option_block_token = 'HTTP_CONFIG_LOCAL_OPTION'
        self.ast = Tree('http_config',
        [
            Tree('http_config_block',
            [
                Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])

class ProcessInjectBlock(CodeBlock):
    def __init__(self):
        self.option_block_token = 'PROCESS_INJECT_LOCAL_OPTION'
        self.ast = Tree('process_inject',
        [
            Tree('process_inject_block',
            [
                Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])

class Transform86Block(CodeBlock):
    def __init__(self):
        self.option_block_token = 'PROCESS_INJECT_LOCAL_OPTION'
        self.ast = Tree('transform_x86',
        [
            Tree('transform_block',
            [
                Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])

class Transform64Block(CodeBlock):
    def __init__(self):
        self.option_block_token = 'PROCESS_INJECT_LOCAL_OPTION'
        self.ast = Tree('transform_x64',
        [
            Tree('transform_block',
            [
                Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])

class ExecuteBlock(CodeBlock):
    def __init__(self):
        self.option_block_token = 'EXECUTE_STATEMENT_OPTION'
        self.ast = Tree('execute',
        [
            Tree('execute_block',
            [
                Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])

    def add_statement(self, name, *values):
        tree = Tree('execute_statement', [])

        children = [Token('EXECUTE_STATEMENT_OPTION', f'{name}')]
        if values:
            children.append(
                Tree('string', [Token('ESCAPED_STRING', f'"{values[0]}"')])
            )

        children.append(Token('DELIM', ';'))
        tree.children.extend(children)

        self.ast.children[0].children.insert(-1, tree)

class PostExBlock(CodeBlock):
    def __init__(self):
        self.option_block_token = 'POST_EX_LOCAL_OPTION'
        self.ast = Tree('post_ex',
        [
            Tree('post_ex_block',
            [
                Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])

class HttpStagerBlock(CodeBlock):
    def __init__(self):
        self.option_block_token = 'HTTP_STAGER_LOCAL_OPTION'
        self.ast = Tree('http_stager',
        [
            Tree('http_stager_block',
            [
                Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])

class StageBlock(CodeBlock):
    def __init__(self):
        self.option_block_token = 'STAGE_LOCAL_OPTION'
        self.ast = Tree('stage',
        [
            Tree('stage_block',
            [
                Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])

class CodeSignerBlock(CodeBlock):
    def __init__(self):
        self.option_block_token = 'CODE_SIGNER_LOCAL_OPTION'
        self.ast = Tree('code_signer',
        [
            Tree('code_signer_block',
            [
                Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])

class HttpsCertificateBlock(CodeBlock):
    def __init__(self):
        self.option_block_token = 'HTTPS_CERTIFICATE_LOCAL_OPTION'
        self.ast = Tree('https_certificate',
        [
            Tree('https_certificate_block',
            [
                Token('BEGIN_CODE_BLOCK_DELIM', '{'),
                Token('END_CODE_BLOCK_DELIM', '}')
            ])
        ])

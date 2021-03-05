import sys
from malleablec2 import Profile
from malleablec2.randomizer import ProfileRandomizer
from lark import Token

class MyExampleRandomizer(ProfileRandomizer):
    """
    This shows you how to randomize a Malleable C2 profile.
    This example 'randomizes' certain values with the word 'wat'. Obviously implement your own logic to randomize the values to something useful.

    Subclassed methods get called based on the parsed AST tokens.
    E.g 'local_option_set' method will get called when a "set <x>" statement in the profile is encountered.

    For a full list of tokens that you can subclass here see the grammar.lark file: you can generally subclass anything after the alias (->) statements.  
    """

    def local_option_set(self, tree):
        """
        Randomize some common local options

        'set uri' in http-get/post-blocks
        'set uri_x86/uri_x64' in http-stager blocks
        'set headers' in http-config block
        'set pipename' in post-ex block
        'set dns_stager_subhost' in dns-beacon blocks
        """

        option_name = tree.children[0]

        if option_name in ["uri", "uri_x86", "uri_x64"]:
            tree.children[1].children[0] = Token('ESCAPED_STRING', '"wat"')
        elif option_name == "pipename":
            tree.children[1].children[0] = Token('ESCAPED_STRING', '"wat"')
        elif option_name == "headers":
            tree.children[1].children[0] = Token('ESCAPED_STRING', '"wat"')
        elif option_name == "dns_stager_subhost":
            tree.children[1].children[0] = Token('ESCAPED_STRING', '"wat"')

    def global_option_set(self, tree):
        """
        Randomize some common global options
        """
        option_name = tree.children[0]

        if option_name in ["pipename", "ssh_pipename", "pipename_stager"]:
            tree.children[1].children[0] = Token('ESCAPED_STRING', '"wat"')
        elif option_name == "ssh_banner":
            tree.children[1].children[0] = Token('ESCAPED_STRING', '"wat"')

    def header(self, tree):
        """
        Randomize the header statements in http-get/http-post blocks
        """

        if len(tree.children) == 3:
            tree.children[1].children[0] = Token('ESCAPED_STRING', '"wat"')

    def parameter(self, tree):
        """
        Randomize the parameter statement in http-get/http-post blocks
        """

        tree.children[0].children[0] = Token('ESCAPED_STRING', '"wat"')

if __name__ == "__main__":
    p = Profile.from_file(
        sys.argv[1] 
        if len(sys.argv) == 2 else 
        "amazon.profile"
    )

    r = MyExampleRandomizer()
    r.randomize(p)

    print(p)
# pyMalleableC2

Python library that allows you to parse and build Cobalt Strike Malleable C2 Profiles programmatically.

Supports all of the Cobalt Strike Malleable C2 Profile grammar.

## 🚨 WARNING 🚨

**pyMalleableC2 treats you as a consenting adult and assumes you know how to write Malleable C2 Profiles: there are very few safety checks and it'll gladly generate invalid profiles if instructed to do so. Always run the generated profiles through [c2lint](https://www.cobaltstrike.com/help-malleable-c2) before using them in production!**

## Examples

(See the examples folder for more)

Generate the AST for a Malleable C2 Profile located in a file, then reconstruct the source code from the AST:

```python
from malleablec2 import Profile

# Parse a profile given its path
p = Profile.from_file("amazon.profile")

# Print the generated AST
print(p.ast.pretty())

# Reconstruct source code from the AST and print to console
print(p.reconstruct())

# Shortcut for the above :)
print(p)
```

Generate the AST for an 'inline' Malleable C2 Profile then reconstruct the source code from the AST:

```python
code = '''
set jitter "0";
set sleeptime "3000";

http-get {
    set uri "/wow/this/is/cool";
}

http-post {
    set uri "/pymalleablec2/is/the/shit";
}
'''

# Parse a profile from a string
p = Profile.from_string(code)

# Print the generated AST
print(p.ast.pretty())

# Reconstruct source code from the AST and print to console
print(p)
```

Build a Malleable C2 profile programmatically from scratch:

```python
from malleablec2 import Profile
from malleablec2.components import *

# Create an empty profile
p = Profile.from_scratch()

# Set some global options
p.set_option("sleeptime", "0")
p.set_option("jitter", "0")
p.set_option("pipename", "mojo__##")

# Create an http-get block
http_get = HttpGetBlock()
# Set the uri http-get option
http_get.set_option("uri", "/wat/a/tease")

# Create a client block
client = ClientBlock()
# Add a header statement to the client block
client.add_statement("header", "Accept", "*/*")

# Create a server block
server = ServerBlock()

# Add the client and server blocks to the http-get block
http_get.add_code_block(client)
http_get.add_code_block(server)

# Create a http-post block
http_post = HttpPostBlock()
# Set the uri http-post option
http_post.set_option("uri", "/wat/ucraycray")

# Add the http-get and http-post blocks to the profile
p.add_code_block(http_get)
p.add_code_block(http_post)

# Print the generated profile
print(p)
```

Super simple example on how to randomize a Malleable C2 Profile:

```python
from malleablec2 import Profile
from malleablec2.randomizer import ProfileRandomizer
from lark import Token

class MyRandomizer(ProfileRandomizer):

    # We implement the global_option_set method which will get called on every parsed global option statement in the profile
    def global_option_set(self, tree):
        option_name = tree.children[0]

        if option_name == "pipename":
            # "Randomize" the pipename value
            tree.children[1].children[0] = Token('ESCAPED_STRING', '"my_random_pipename_##"')

# Parse a profile given its path
p = Profile.from_file("amazon.profile")

r = MyRandomizer()

# Walk through the generated profile AST and apply randomization rules
r.randomize(p)

# Reconstruct source code and output the profile to the console
print(p)
```
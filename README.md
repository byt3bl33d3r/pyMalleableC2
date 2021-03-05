# pyMalleableC2

A Python "interpreter" for Cobalt Strike Malleable C2 profiles that allows you to parse, modify and build them programmatically.

Supports all of the Cobalt Strike Malleable C2 Profile grammar starting from Cobalt Strike version 4.3. **Not backwards compatible.**

# Sponsors
[<img src="https://www.blackhillsinfosec.com/wp-content/uploads/2016/03/BHIS-logo-L-300x300.png" width="130" height="130"/>](https://www.blackhillsinfosec.com/)
[<img src="https://handbook.volkis.com.au/assets/img/Volkis_Logo_Brandpack.svg" width="130" hspace="10"/>](https://volkis.com.au)
[<img src="https://user-images.githubusercontent.com/5151193/85817125-875e0880-b743-11ea-83e9-764cd55a29c5.png" width="200" vspace="21"/>](https://qomplx.com/blog/cyber/)
[<img src="https://user-images.githubusercontent.com/5151193/86521020-9f0f4e00-be21-11ea-9256-836bc28e9d14.png" width="250" hspace="20"/>](https://ledgerops.com)
[<img src="https://user-images.githubusercontent.com/5151193/95542303-a27f1c00-09b2-11eb-8682-e10b3e0f0710.jpg" width="200" hspace="20"/>](https://lostrabbitlabs.com/)

# Table of Contents

* [pyMalleableC2](#utinni)
  + [Installing](#installing)
  + [pyMalleableC2 vs Other Similar libraries/tools](#)
  + [Examples](#examples)
  + [FAQ](#faq)

# Installing

`pip3 installl pymalleablec2`

`docker pull byt3bl33d3r/pymalleablec2`

# What's the difference between pyMalleableC2 and other Malleable C2 profile parsers?

`pyMalleableC2` is different in many ways because of several design decisions (some listed below).

TL;DR `pyMalleableC2` is an interpreter for Malleable C2 profiles as supposed to just a "dumb" parser.

1. Parses profiles using Lark and a grammar file. This approach is a lot more robust then using plain user defined regexes.
2. Turns profiles into an Abstract Syntax Tree (AST) which we can then reconstruct back into source code.
3. Because of the above, we can easily build profiles programmatically or modify them on the fly.

# 🚨 WARNING 🚨

**pyMalleableC2 treats you as a consenting adult and assumes you know how to write Malleable C2 Profiles: there are very few safety checks and it'll gladly generate invalid profiles if instructed to do so. Always run the generated profiles through [c2lint](https://www.cobaltstrike.com/help-malleable-c2) before using them in production!**

(Technically you could build a Python version of c2lint using this library, *cough* PRs welcome *cough*)

# Examples

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

Super simple example showing how to programmatically randomize a Malleable C2 Profile:

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
<p align="center">
  <img src="https://user-images.githubusercontent.com/5151193/110083243-b3f30700-7d4b-11eb-8b69-28116e5ea1c9.png" alt="pyMalleableC2" height=300 width=500/>
</p>

# pyMalleableC2

A Python interpreter for Cobalt Strike Malleable C2 profiles that allows you to parse, modify, build them programmatically and validate syntax.

Supports all of the Cobalt Strike Malleable C2 Profile grammar starting from Cobalt Strike version 4.3. 

**It's not backwards compatible with previous Cobalt Strike releases.**

What are the differences between pyMalleableC2 and other projects of this nature? 

1. Parses profiles with [Lark](https://github.com/lark-parser/lark) using [eBNF notation](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form). This approach is a lot more robust then user defined regexes, templating engines or similar methods.
2. Turns profiles into an [Abstract Syntax Tree (AST)](https://en.wikipedia.org/wiki/Abstract_syntax_tree) which can then be reconstructed back into source code.
3. Because of the above, pyMalleableC2 allows you to build profiles programmatically or modify them on the fly.
4. Allows you to validate the syntax of Malleable C2 profiles (Does not perform runtime checks, see the warning below.)
5. It has AI in the form of a lot of `if` statements.

# Sponsors
[<img src="https://www.blackhillsinfosec.com/wp-content/uploads/2016/03/BHIS-logo-L-300x300.png" width="130" height="130"/>](https://www.blackhillsinfosec.com/)
[<img src="https://handbook.volkis.com.au/assets/img/Volkis_Logo_Brandpack.svg" width="130" hspace="10"/>](https://volkis.com.au)
[<img src="https://user-images.githubusercontent.com/5151193/85817125-875e0880-b743-11ea-83e9-764cd55a29c5.png" width="200" vspace="21"/>](https://qomplx.com/blog/cyber/)
[<img src="https://user-images.githubusercontent.com/5151193/86521020-9f0f4e00-be21-11ea-9256-836bc28e9d14.png" width="250" hspace="20"/>](https://ledgerops.com)
[<img src="https://user-images.githubusercontent.com/5151193/95542303-a27f1c00-09b2-11eb-8682-e10b3e0f0710.jpg" width="200" hspace="20"/>](https://lostrabbitlabs.com/)
[<img src="https://user-images.githubusercontent.com/5151193/113820904-334f6e00-9730-11eb-9f26-128b0917f5c6.png" width="150" height="150" hspace="20"/>](https://kovert.no/)
[<img src="https://user-images.githubusercontent.com/5151193/113820971-4c581f00-9730-11eb-91d6-01fe1e72f556.jpg" width="250" hspace="20"/>](https://www.ondefend.com/)

# Table of Contents

* [pyMalleableC2](#utinni)
  + [Installing](#installing)
  + [🚨 Warning! No runtime checks (yet!) 🚨](#-warning-)
  + [Author](#author)
  + [Official Discord Channel](#official-discord-channel)
  + [Examples](#examples)
  + [FAQ](#faq)

# Installing

pyMalleableC2 was built using Python 3.9, however it should be backwards compatible up to Python 3.6.

Install using Pip:
- `pip3 install pymalleablec2`

# 🚨 WARNING 🚨

**pyMalleableC2 treats you as a consenting adult and assumes you know how to write Malleable C2 Profiles. It's able to detect syntax errors, however there are no runtime checks implemented. It'll gladly generate profiles that don't actually work in production if instructed to do so. Always run the generated profiles through [c2lint](https://www.cobaltstrike.com/help-malleable-c2) before using them in production!**

(Technically you could build a Python version of c2lint using this library, *\*cough\** PRs welcome *\*cough\**)

## Author 

The primary author of pyMalleableC2 is Marcello Salvati 

Twitter: [@byt3bl33d3r](https://twitter.com/byt3bl33d3r), Github: [@byt3bl33d3r](https://github.com/byt3bl33d3r)

## Official Discord Channel

Come hang out on Discord!

[![Porchetta Industries](https://discordapp.com/api/guilds/736724457258745996/widget.png?style=banner3)](https://discord.gg/AKrqt6J)

## Examples

(See the [examples](https://github.com/Porchetta-Industries/pyMalleableC2/tree/main/examples) folder for more)

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

# Reconstruct source code from the generated AST and print to console
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

# Reconstruct source code then output the profile to the console
print(p)
```

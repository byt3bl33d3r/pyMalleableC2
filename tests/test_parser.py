import pytest
import pathlib
import malleablec2

def test_parsing():
    for profile in []:
        ast = malleablec2.parse()
        code = malleablec2.reconstruct(ast)

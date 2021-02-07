import pytest
import pathlib
from malleablec2 import Profile

def test_parsing():
    path = pathlib.Path('.')
    profiles = path.glob("tests/profiles/*.profile")

    for profile in profiles:
        p = Profile.from_file(profile)
        assert len(p.ast.children) > 0
        c = p.reconstruct()
        assert len(c) > 0

import pytest
from malleablec2 import Profile
from malleablec2.components import *

def test_builder():
    profile = Profile.from_scratch()
    profile.set_option("sleeptime", "5000")
    profile.set_option("jitter", "0")
    profile.set_option("pipename", "buildtest_##")

    http_get = HttpGetBlock()
    http_get.set_option("uri", "/test/wat")

    client = ClientBlock()
    client.add_statement("header", "Accept", "*/*")

    server = ServerBlock()
    server.add_statement("header", "Server", "Server")

    http_get.add_code_block(client)
    http_get.add_code_block(server)

    http_post = HttpPostBlock()
    http_post.set_option("uri", "/test/okurrr")

    profile.add_code_block(http_get)
    profile.add_code_block(http_post)

    assert len(profile.ast.children) > 0
    c = profile.reconstruct()
    assert len(c) > 0
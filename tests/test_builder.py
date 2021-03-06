import pytest
from malleablec2 import Profile
from malleablec2.components import *

def test_builder():
    profile = Profile.from_scratch()
    profile.set_option("sleeptime", "5000")
    profile.set_option("jitter", "0")
    profile.set_option("pipename", "buildtest_##")

    http_config = HttpConfigBlock()
    http_config.set_option("headers", "Date, Server, Content-Length, Keep-Alive, Connection, Content-Type")
    http_config.set_option("block_useragents", "curl*,lynx*,wget*")
    http_config.add_statement("header", "Connection", "Keep-Alive")

    profile.add_code_block(http_config)

    http_stager = HttpStagerBlock()
    http_stager.set_option("uri_x86", "/pymalleablec2/ftw")
    http_stager.set_option("uri_x64", "/pymalleablec2/is/the/shizzle")

    profile.add_code_block(http_stager)

    stage = StageBlock()
    stage.add_statement("stringw", "I am not Beacon")
    stage.set_option("allocator", "MapViewOfFile")

    profile.add_code_block(stage)

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

    process_inject = ProcessInjectBlock()
    process_inject.set_option("min_alloc", "16384")

    transform86 = Transform86Block()
    transform86.add_statement("prepend", r"\x90\x90")

    execute = ExecuteBlock()
    execute.add_statement("CreateThread", "ntdll.dll!RtlUserThreadStart")
    execute.add_statement("SetThreadContext")

    process_inject.add_code_block(execute)
    process_inject.add_code_block(transform86)

    postex = PostExBlock()
    postex.set_option("spawnto_x86", r"%windir%\syswow64\calc.exe")
    postex.set_option("spawnto_x64", r"%windir%\syswow64\calc.exe")
    postex.set_option("obfuscate", "true")

    https_certificate = HttpsCertificateBlock()
    https_certificate.set_option("C", "US")
    https_certificate.set_option("CN", "localhost")

    code_signer = CodeSignerBlock()
    code_signer.set_option("keystore", "keystore.jks")
    code_signer.set_option("password", "my_keystore_password")

    profile.add_code_block(code_signer)
    profile.add_code_block(https_certificate)
    profile.add_code_block(postex)
    profile.add_code_block(process_inject)
    profile.add_code_block(http_get)
    profile.add_code_block(http_post)

    assert len(profile.ast.children) > 0
    c = profile.reconstruct()
    assert len(c) > 0
    print(c)
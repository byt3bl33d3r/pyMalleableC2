from malleablec2 import Profile
from malleablec2.components import *

p = Profile.from_scratch()
p.set_option("jitter", "0")
p.set_option("pipename", "msagent_##")

http_get = HttpGetBlock()
http_get.set_option("uri", "/wat/tease")

client = ClientBlock()
client.add_statement("header", "Accept", "*/*")

server = ServerBlock()

http_get.add_code_block(client)
http_get.add_code_block(server)

http_post = HttpPostBlock()
http_post.set_option("uri", "/wat/ucraycray")

p.add_code_block(http_get)
p.add_code_block(http_post)

print(p)
from malleablec2 import Profile
from malleablec2.components import *

profile = Profile.from_scratch()
profile.set_option("sleeptime", "5000")
profile.set_option("jitter", "0")
profile.set_option("pipename", "buildtest_##")

http_config = HttpConfigBlock()
http_config.set_option("headers", "Date, Server, Content-Length, Keep-Alive, Connection, Content-Type")
http_config.set_option("block_useragents", "curl*,lynx*,wget*")
http_config.add_statement("header", "Connection", "Keep-Alive")

profile.add_code_block(http_config)

dns_beacon = DnsBeaconBlock()
dns_beacon.set_option("dns_idle", "1.2.3.4")
dns_beacon.set_option("get_A", "doc.la.")

profile.add_code_block(dns_beacon)

http_get = HttpGetBlock()
http_get.set_option("uri", "/test/wat")

client = ClientBlock()
client.add_statement("header", "Accept", "*/*")

server = ServerBlock()
server.add_statement("header", "Server", "Apache")

http_get.add_code_block(client)
http_get.add_code_block(server)

http_post = HttpPostBlock()
http_post.set_option("uri", "/test/okurrr")

profile.add_code_block(http_get)
profile.add_code_block(http_post)

print(profile)
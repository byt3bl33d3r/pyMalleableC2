from malleablec2 import Profile

def get_all_urls(items):
    collect_next_item = False
    for item in items:
        if collect_next_item:
            collect_next_item = False
            urls = set([url.strip() for url in item[1:-1].split()])
            for url in urls:
                yield url + "\n"

        if isinstance(item, Token) and item.type in ["HTTP_LOCAL_OPTION", "HTTP_STAGER_LOCAL_OPTION"]:
            if item != "verb":
                collect_next_item = True
                continue

if __name__ == "__main__":

    profile_code = '''
# Profile with all code blocks that are allowed to define a URL

http-get {
    set uri "/wat/test";
}

http-get "variant_get_1" {
    set uri "/wat/test/1";
}

http-post {
    set uri "/test/okurrr";
}

http-stage {
    set uri_x86 "/test/stager86";
    set uri_x64 "/test/stager64";
}
'''

    p = Profile.from_string(profile_code)
    urls = p.reconstruct(postproc=get_all_urls)
    print(urls)

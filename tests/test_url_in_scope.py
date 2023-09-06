from spider.scrape import url_in_scope

# TODO: put parameters in variables and change their order
def test_basic_depth():
    in_scope = url_in_scope("https://github.com", "https://github.com/louisabricot", 1)
    assert in_scope == True
    not_in_scope = url_in_scope("https://github.com", "https://github.com/louisabricot", 0)
    assert not_in_scope == False

def test_https_vs_http():
    in_scope = url_in_scope("http://github.com","https://github.com/louisabricot", 1)
    assert in_scope == True

def test_trailing_slash():
    in_scope = url_in_scope("https://github.com",
    "https://github.com/louisabricot/", 1)
    assert in_scope == True

def test_simple_not_matching_domain():
    not_in_scope = url_in_scope("https://github.com", "https://github.fr/lol",3)
    assert not_in_scope == False
    not_in_scope = url_in_scope("https://github.com", "https://githab.com/lol",3)
    assert not_in_scope == False
    not_in_scope = url_in_scope("https://github.com", "htps://github.com/lol",3)
    assert not_in_scope == False
    not_in_scope = url_in_scope("https://github.com/lol/sorry/wtf","/pouet",3)
    assert not_in_scope == False
    not_in_scope = url_in_scope("https://github.com/lol/sorry/wtf", "https://github.com/lol/sorry/wtf/../../../nope",3)
    assert not_in_scope == False

from tools.url_utils import url_in_scope


def test_basic_depth():
    base_url = "https://github.com"
    url = "https://github.com/louisabricot"
    in_scope = url_in_scope(url, base_url, 1)
    assert in_scope is True
    not_in_scope = url_in_scope(url, base_url, 0)
    assert not_in_scope is False


def test_https_vs_http():
    base_url = "http://github.com"
    url = "https://github.com/louisabricot"
    in_scope = url_in_scope(url, base_url, 1)
    assert in_scope is True


def test_trailing_slash():
    base_url = "https://github.com"
    url = "https://github.com/louisabricot/"
    in_scope = url_in_scope(url, base_url, 1)
    assert in_scope is True


def test_simple_not_matching_domain():
    not_in_scope = url_in_scope("https://github.com", "https://github.fr/lol", 3)
    assert not_in_scope is False
    not_in_scope = url_in_scope("https://github.com", "https://githab.com/lol", 3)
    assert not_in_scope is False
    not_in_scope = url_in_scope("https://github.com", "htps://github.com/lol", 3)
    assert not_in_scope is False
    not_in_scope = url_in_scope("https://github.com/lol/sorry/wtf", "/pouet", 3)
    assert not_in_scope is False
    not_in_scope = url_in_scope(
        "https://github.com/lol/sorry/wtf",
        "https://github.com/lol/sorry/wtf/../../../nope",
        3,
    )

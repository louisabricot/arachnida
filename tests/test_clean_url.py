from spider.url_utils import clean_url

def test_absolute_url_with_params_and_fragments():
    base_url = "http://github.com/"
    url = "http://github.com/path;parameters?query#fragment"
    result = clean_url(base_url, url)
    assert result == "http://github.com/path"

def test_relative_url_with_params_and_fragments():
    base_url = "http://github.com/path"
    url = "/page;parameters?query#fragment"
    result = clean_url(base_url, url)
    assert result == "http://github.com/page"

def test_relative_url_with_fragment():
    base_url = "https://example.com/path/to/page"
    url = "../another-page#section"
    result = clean_url(base_url, url)
    assert result == "https://example.com/another-page"

def test_empty_url():
    base_url = "https://example.com/path/to/page"
    url = ""
    result = clean_url(base_url, url)
    assert result == "https://example.com/path/to/page"

def test_absolute_url_with_query_params():
    base_url = "https://example.com/path/to/page"
    url = "https://example.com/another/page?param1=value1&param2=value2"
    result = clean_url(base_url, url)
    assert result == "https://example.com/another/page"

def test_relative_url_without_slash_prefix():
    base_url = "https://example.com/path/to/page/"
    url = "/relative/page"
    result = clean_url(base_url, url)
    assert result == "https://example.com/relative/page"

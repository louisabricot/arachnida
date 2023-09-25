import logging
import os
from tools.scrape import get_urls_from_page_content

logging.basicConfig(filename="test_scrape.log", level=logging.ERROR)


def test_get_urls(caplog):
    f = open("assets/page.html", "r")
    urls = set()

    webpage = f.read()

    urls = get_urls_from_page_content(webpage, "https://42.fr", "https://42.fr", 5)

    print(urls)

    assert len(urls) == 34
    assert len(caplog.text) == 0

    # Check it scrapes the correct amount of urls


# def test_get_files():
# Check it scsrapes the correct amount of files
def test_page_is_not_html(caplog):
    f = open("assets/page.txt", "r")
    urls = set()

    webpage = f.read()

    urls = get_urls_from_page_content(webpage, "https://42.fr", "https://42.fr", 2)

    assert "Not HTML for URL" in caplog.text
    assert len(urls) == 0

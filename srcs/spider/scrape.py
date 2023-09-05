from urllib.parse import urljoin, urlparse
from spider.url_utils import clean_url
from spider.download_utils import download_image, log_download_error
from collections import deque
import html.parser
from bs4 import BeautifulSoup
import requests
import re

def scrape_images(page_url: str, image_url_patterns: str) -> None:
    """
    Scrape images from the HTML page URL that match the given image URL
    patterns.

    Parameters:
        page_url (str): The URL of the HTML page to scrape for images.
        image_url_patterns (str): Regular expression pattern to match the image
        URLS.

    Returns:
        list: A list of unique image URLs that match the given patterns, or
        None if an error occurs.
    """
    try:
        # Make an HTTP get request to the page url
        response = requests.get(page_url, allow_redirects=True)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all iamge tags with valid 'src' attribute
        img_tags = soup.find_all("img", src=True)

        # Extract image URLs that match the provided patterns
        image_urls = []
        for img in img_tags:
            match = re.search(image_url_patterns, img["src"])
            if match:
                extracted_url = match.group()
                image_urls.append(extracted_url)

        # Remove duplicates from list
        image_urls = list(dict.fromkeys(image_urls))
        return image_urls

    except requests.exceptions.RequestException as e:
        log_download_error(page_url, e)
    return None


def url_in_scope(base_url: str, url: str, depth: int) -> bool:
    """
    Check if the given URL is within the scope of the base URL based on depth.

    Parameters:
        base_url (str): The base URL that defines the scope.
        url (str): The URL to check if it is within the scope.
        depth (int): The depth of the allowed paths within the scope from the
        base_url

    Returns:
        bool: True if the URL is within scope; otherwise, false.
    """

    base_path = urlparse(base_url).path
    url_path = urlparse(url).path

    if urlparse(base_url).netloc == urlparse(url).netloc and url_path.startswith(
        base_path
    ):
        return depth >= url_path.count('/') - base_path.count('/')
    return False


def get_page_content(base_url: str, url: str, depth: int) -> str:
    """
    Get the content of a web page given a URL while handling redirections and
    scope constraints.

    Parameters:
        base_url (str): The base URL that defines the scope.
        url (str): The URL of the page to retrieve content from.
        depth (int): The depth of the allowed paths within the scope from the
        base url.

    Returns:
        str: The content of the web page if successful, otherwise None.
    """

    try:
        # Make an HTTP get request to the page url
        response = requests.get(url, allow_redirects=False, timeout=10)
        response.raise_for_status()

        # Get content if redirection is within scope constraints
        if response.status_code in (301, 302, 303, 307, 308):
            location = clean_url(url, response.headers.get('Location'))
            if url_in_scope(base_url, location, depth):
                response = requests.get(url, allow_redirects=True, timeout=10)
                response.raise_for_status()
                return response.text
        else:
            return response.text
    except requests.exceptions.RequestException as e:
        log_download_error(url, e)
    return None


def get_subpaths(base_url: str, url_page: str, depth: int) -> set:
    """Scrapes html content and returns in scope subpaths"""

    links = set()
    subpaths = set()
    content = get_page_content(base_url, url, depth)
    if content:
        soup = BeautifulSoup(content, "html.parser")

        # Get all links from a and link 
        for link in soup.find_all(['link', 'a'], href=True):
            links.add(link.get('href'))

        for link in links:
            url = clean_url(base_url, link)
            if url.startswith(base_url) and url_in_scope(base_url, url, depth):
                subpaths.add(url)
    return subpaths


def retrieve_nested_urls(base_url: str, depth: int) -> set:
    """
    Iterates through paths containing the base_url and within the depth scope
    defined by depth and retrieve more paths
    Returns a set of the paths that were visited.
    """

    if depth == 0:
        return set([base_url])

    visited = set()
    to_visit = set([base_url])

    while len(to_visit) > 0:
        url = to_visit.pop()

        subpaths = retrieve_links_from_page(base_url, url, depth)

        visited.add(url)

        for path in subpaths:
            to_visit.add(path)

        to_visit.difference_update(visited)

    return visited

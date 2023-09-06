from urllib.parse import urljoin, urlparse
from spider.url_utils import clean_url
from spider.download_utils import download_image, log_download_error
from collections import deque
import html.parser
from bs4 import BeautifulSoup
import requests
import re
import logging

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


def url_in_scope(url: str, base_url: str, depth: int) -> bool:
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

    url_path = urlparse(url).path.rstrip('/')
    base_url_path = urlparse(base_url).path.rstrip('/')

    if urlparse(base_url).hostname == urlparse(url).hostname and url_path.startswith(base_url_path):
        return depth >= url_path.count('/') - base_url_path.count('/')
    return False


def fetch_url_content(url: str, base_url: str, depth: int) -> str:
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        elif response.status_code in (301, 302, 307, 308):
            redirection_url = response.headers.get('Location')
            if redirection_url and url_in_scope(redirection_url, base_url, depth):
                fetch_url_content(redirection_url, base_url, depth)
            else:
                logging.error(f"Redirection to an external URL: {redirection_url}")
        else:
            logging.error(f"HTTP Error {response.status_code} for URL: {url}")
    except requests.RequestException as e:
        logging.error(f"Request Exception: {str(e)} for URL: {url}")

    return None

def retrieve_links_from_page(base_url: str, url_page: str, depth: int) -> set:
    """Scrapes html content and returns in scope subpaths"""

    subpaths = set()
    content = fetch_url_content(base_url, url_page, depth)
    if content:
        soup = BeautifulSoup(content, "html.parser")

        # Get all links from a and link 
        for link in soup.find_all(['link', 'a'], href=True):

            url = clean_url(url_page, link.get('href'))
            if url.startswith(base_url) and url_in_scope(url, base_url, depth):
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

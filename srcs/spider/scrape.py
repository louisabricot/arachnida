from urllib.parse import urljoin, urlparse
from spider.url_utils import clean_url, url_in_scope
from spider.download_utils import download_image, log_download_error
from collections import deque
import html.parser
from bs4 import BeautifulSoup
import requests
import re
import logging
import validators


def scrape_images(webpage: str, image_url_patterns: str) -> set:
    """
    Scrapes image URLs from a webpage matching the specified image URLs
    patterns.

    Args:
        webpage (str): The URL of the web page to scrape.
        image_url_patterns (str): A regular expression pattern to filter image
        URLs

    Returns:
        set: A set of filtered image URLs matching the pattern.
            Returns an empty set if no matches are found or an error occurs.
    """

    try:
        # Make an HTTP GET request to the page URL
        response = requests.get(webpage, allow_redirects=True)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Gathers the 'src' attribute of all img tags
        img_srcs = set(img.attrs["src"] for img in soup.find_all(["img"], src=True))

        # Filters 'src' based on the provided pattern
        filtered_urls = {src for src in img_srcs if re.search(image_url_patterns, src)}

        return filtered_urls

    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP Error {response.status_code} for URL: {webpage}")

    return set()


def get_urls_from_page(
    webpage: str, base_url: str, depth: int, visited: set, nested_urls
) -> set():
    # Returns if the url is not valid
    if not validators.url(webpage):
        return set()

    try:
        # Make an HTTP GET request to the page URL
        response = requests.get(webpage)
        response.raise_for_status()

        if response.status_code == 200:
            # Only scrapes HTML pages
            if response.headers and "text/html" in response.headers.get("content-type"):
                nested_urls.add(webpage)
                # print(webpage)
                return get_urls_from_page_content(
                    response.text, webpage, base_url, depth
                )
            else:
                logging.error(
                    f"Cannot parse content-type {response.headers['content-type']} for URL: {webpage}"
                )

        # Fetch content if redirection within scope
        elif response.status_code in (301, 302, 307, 308):
            redirection_url = response.headers.get("Location")
            if redirection_url and url_in_scope(redirection_url, base_url, depth):
                if redirection_url not in visited:
                    get_urls_from_page(
                        redirection_url, base_url, depth, visited, nested_urls
                    )

                    # Add redirection URL to visited set
                    visited.add(redirection_url)
            else:
                logging.error(f"Redirection to an external URL: {redirection_url}")
    except requests.RequestException as e:
        logging.error(f"Request Exception: {str(e)}")

    return set()


def get_urls_from_page_content(
    content: str, webpage: str, base_url: str, depth: int
) -> set:
    subpaths = set()
    if content:
        if not re.search(r"<!DOCTYPE html>", content):
            logging.error(f"Not HTML for URL: {webpage}")
            return set()
        # TODO: Check if file starts with DOCTYPE
        soup = BeautifulSoup(content, "html.parser")
        # Get all links from a and link
        for link in soup.find_all(["link", "a"], href=True):
            url = clean_url(webpage, link.get("href"))
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
    nested_urls = set()
    to_visit = set([base_url])

    while to_visit:
        webpage = to_visit.pop()
        retrieved_urls = get_urls_from_page(
            webpage, base_url, depth, visited, nested_urls
        )
        if retrieved_urls:
            to_visit.update(retrieved_urls)
        visited.add(webpage)
        to_visit.difference_update(visited)

    return nested_urls

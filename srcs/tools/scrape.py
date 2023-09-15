"""
Web Scraping and URL Retrieval Module

This module provides functions for web scraping and URL retrieval. It utilizes
various libraries such as requests, BeautifulSoup, and validators to perform
these tasks efficiently. The module includes the following functions:

1. `scrape_files`: Scrapes file URLs from a webpage based on specified patterns.

2. `get_urls_from_page`: Retrieves URLs from a webpage and its nested pages up to
   a specified depth. It also checks for redirection and validates URLs.

3. `get_urls_from_page_content`: Extracts URLs from the HTML content of a web page
   using BeautifulSoup.

4. `retrieve_nested_urls`: Iterates through paths containing a base URL and within
   the specified depth to retrieve more paths, effectively creating a set of nested
   URLs.
"""

import re
import logging
import validators
import requests
from bs4 import BeautifulSoup
from tools.url_utils import clean_url, url_in_scope


def scrape_files(webpage: str, extensions: list) -> set:
    """
    Scrapes file URLs from a webpage matching the specified file URLs
    patterns.

    Args:
        webpage (str): The URL of the web page to scrape.
        extensions (list): A list of file extensions to scrape.

    Returns:
        set: A set of filtered file URLs matching the specified extensions.
            Returns an empty set if no matches are found or an error occurs.
    """

    try:
        # Make an HTTP GET request to the page URL
        response = requests.get(webpage, allow_redirects=True, timeout=5)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Gathers the 'src' attribute of all img tags
        links = set(link.attrs["src"] for link in soup.find_all(["img"], src=True))
        links.update(
            set(link.attrs["href"] for link in soup.find_all(["a"], href=True))
        )

        # Generate the URL pattern based on specified extensions
        extension_patterns = r"(?:.(?!https?:\/\/))+.({})$".format("|".join(extensions))

        # Filters links based on the provided pattern
        filtered_urls = {link for link in links if re.search(extension_patterns, link)}

        return filtered_urls

    except requests.exceptions.RequestException as e:
        logging.error("HTTP Error %s for URL: %s", str(e), webpage)

    return set()


def get_urls_from_page(
    webpage: str, base_url: str, depth: int, visited: set, nested_urls
) -> set():
    """
    Retrieves URLs from a webpage. If the webpage redirects to another page,
    this function checks that the redirection URL is in the scopeof the
    specified base URL and depth. The webpage must be an HTML page.

    Args:
        webpage (str): The URL of the web page to retrieve URLs from.
        base_url (str): The base URL to determine if retrieved URLs are in scope.
        depth (int): The maximum depth of nested pages to retrieve.
        visited (set): A set of visited URLs to prevent revisiting.
        nested_urls (set): A set to store nested URLs.

    Returns:
        set: A set of URLs retrieved from the page and its nested pages.
    """
    # Returns if the url is not valid
    if not validators.url(webpage):
        return set()

    try:
        # Make an HTTP GET request to the page URL
        response = requests.get(webpage, timeout=5)
        response.raise_for_status()

        if response.status_code == 200:
            # Only scrapes HTML pages
            if response.headers and "text/html" in response.headers.get("content-type"):
                nested_urls.add(webpage)
                return get_urls_from_page_content(
                    response.text, webpage, base_url, depth
                )
            logging.error(
                "Cannot parse content-type %s for URL: %s",
                response.headers["content-type"],
                webpage,
            )

        # Fetch content if redirection within scope
        elif response.status_code in (301, 302, 307, 308):
            redirection_url = response.headers.get("Location")
            if redirection_url and url_in_scope(redirection_url, base_url, depth):
                if redirection_url.rstrip("/") not in visited:
                    get_urls_from_page(
                        redirection_url, base_url, depth, visited, nested_urls
                    )

                    # Add redirection URL to visited set
                    visited.add(redirection_url.rstrip("/"))
            else:
                logging.error("Redirection to an external URL: %s", redirection_url)
    except requests.RequestException as e:
        logging.error("Request Exception: %s", str(e))

    return set()


def get_urls_from_page_content(
    content: str, webpage: str, base_url: str, depth: int
) -> set:
    """
    Extracts URLs from the HTML content of a web page using BeautifulSoup library.

    Args:
        content (str): The HTML content of the web page.
        webpage (str): The URL of the web page.
        base_url (str): The base URL to determine if retrieved URLs are in scope.
        depth (int): The maximum depth of nested pages to retrieve.

    Returns:
        set: A set of URLs extracted from the page content.
    """

    subpaths = set()
    if content:
        if not re.search(r"<!DOCTYPE html>", content):
            logging.error("Not HTML for URL: %s", webpage)
            return set()
        soup = BeautifulSoup(content, "html.parser")
        # Get all links from a and link
        for link in soup.find_all(["link", "a"], href=True):
            url = clean_url(webpage, link.get("href"))
            if url.startswith(base_url) and url_in_scope(url, base_url, depth):
                subpaths.add(url.rstrip("/"))
    return subpaths


def retrieve_nested_urls(base_url: str, depth: int) -> set:
    """
    Retrieves URLs within the scope specified by the base URL and depth.
    Each page visited is scraped for URLs. If the newly found URLs are within scope,
    they are visited.

    Args:
        base_url (str): The base URL to start the retrieval from.
        depth (int): The maximum depth of nested pages to retrieve.

    Returns:
        set: A set of nested URLs retrieved within the specified depth.
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
        visited.add(webpage.rstrip("/"))
        to_visit.difference_update(visited)

    return nested_urls

"""
This module provides utility functions for working with URLs.

Functions:
    clean_url(base_url: str, url: str) -> str:
        Cleans the given URL by removing any query parameters while preserving
        scheme, netloc, and path. Converts relative URLs to absolute URLs using
        the base URL.

    url_in_scope(url: str, base_url: str, depth: int) -> bool:
        Check if the given URL is within the scope of the base URL based on depth.
"""

from urllib.parse import urlparse, urljoin

def clean_url(base_url: str, url: str) -> str:
    """
    Cleans the given URL by removing any query parameters while preserving
    scheme, netloc and path.
    Converts relative URLs to absolute URLs using the base URL.

    Parameters:
        base_url (str): The base URL from which the URL is resolved.
        url (str): The relative or absolute URL to clean and convert.

    Returns:
        str: The cleaned absolute URL.
    """

    # Clean the absolute URL by removing query parameters and trailing
    # slashes
    url_parts = urlparse(url)._replace(params="", query="", fragment="")

    if not url_parts.netloc:
        # If the provided URL is relative, make it absolute using the base URL
        return urljoin(base_url, url_parts.path)

    return url_parts.geturl()


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

    url_path = urlparse(url).path.rstrip("/")
    base_url_path = urlparse(base_url).path.rstrip("/")

    if urlparse(base_url).hostname == urlparse(url).hostname and url_path.startswith(
        base_url_path
    ):
        return depth >= url_path.count("/") - base_url_path.count("/")
    return False

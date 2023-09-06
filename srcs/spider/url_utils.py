from enum import Enum
from urllib.parse import urlparse, urljoin
import os

class Extension(Enum):
    """
    Enumeration representing image file extensions.

    Attributes:
        JPEG (str): Represents the 'jpeg' image file extension.
        JPG (str): Represents the 'jpg' image file extension.
        GIF (str): Represents the 'gif' image file extension.
        BMP (str): Represents the 'bmp' image file extension.
        PNG (str): Represents the 'png' image file extension.
    """

    JPEG = "jpeg"
    JPG = "jpg"
    GIF = "gif"
    BMP = "bmp"
    PNG = "png"


def generate_url_patterns(extension_enum: Enum) -> str:
    """
    Dynamically generate URL pattern ending in one of the extension from the
    extension_enum.

    Parameters:
        extension_enum (Enum): An enumeration of extensions to be used in the
        URL pattern.

    Returns:
        str: The generated URL pattern.
    """

    extensions = [ext.value for ext in extension_enum]
    pattern = r"(?:.(?!https?:\/\/))+.({})$".format("|".join(extensions))
    return pattern

def clean_url(base_url: str, url: str) -> str:
    """
    Clean the given URL by removing any query parameters while preserving
    scheme, netloc and path.Convert relative URLs to absolute URLs using the base URL.

    Parameters:
        base_url (str): The base URL from which the URL is resolved.
        url (str): The relative or absolute URL to clean and convert.

    Returns:
        str: The cleaned absolute URL.
    """
    
    # Parse the base URL and the cleaned URL
    base_url_parts = urlparse(base_url)

    # Clean the absolute URL by removing query parameters and trailing
    # slashes
    url_parts = urlparse(url)._replace(params="", query="", fragment="")

    if not url_parts.netloc:
        # If the provided URL is relative, make it absolute using the base URL
        return urljoin(base_url, url_parts.path)

    return url_parts.geturl().rstrip('/')

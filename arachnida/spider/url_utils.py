from enum import Enum


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
    scheme, netloc and path.
    Convert relative URLs to absolute URLs using the base URL.

    Parameters:
        base_url (str): The base URL from which the URL is resolved.
        url (str): The relative or absolute URL to clean and convert.

    Returns:
        str: The cleaned absolute URL.

    Example:
        >>> base_url = "https://example.com/path/"
        >>> relative_url = "/page.html?param=123"
        >>> clean_url(base_url, relative_url)
        'https://example.com/path/page.html'

        >>> absolute_url = "https://example.com/other-page.html?param=456"
        >>> clean_url(base_url, absolute_url)
        'https://example.com/other-page.html'
    """

    parsed_base_url = urlparse(base_url)
    parsed_url = urlparse(url)

    if not parse_url.netloc:
        # If the parse URL has no netloc (i.e., relative URLs), use the base
        # URL's scheme and netloc
        cleaned_url = urljoin(
            parsed_base_url.scheme + "://" + parsed_base_url.netloc + parsed_url.path
        )
    else:
        # If the parsed URL has a netloc (i.e., absolute URL), use the parsed
        # URL's scheme, netloc and path
        cleaned_url = urljoin(
            parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
        )
    return cleaned_url

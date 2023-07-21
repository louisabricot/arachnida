from urllib.parse import urljoin, urlparse
from collections import deque
import html.parser
from bs4 import BeautifulSoup
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
        path_depth = url_path.count("/")
        return depth >= path_depth - base_path.count("/")
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
            location = clean_url(url, response.headers.get("Location"))
            if url_in_scope(base_url, location, depth):
                response = requests.get(url, allow_redirects=True, timeout=10)
                response.raise_for_status()
                return response.text
        else:
            return response.text
    except requests.exceptions.RequestException as e:
        log_download_error(url, e)
    return None


def get_subpaths(base_url: str, url: str, depth: int) -> set:
    """Scrapes html content and returns in scope subpaths"""

    subpaths = set()
    content = get_page_content(base_url, url, depth)
    if content:
        soup = BeautifulSoup(content, "html.parser")
        for link in soup.find_all(["link", "a"], href=True):
            url = clean_url(base_url, link.get("href"))
            if url_in_scope(base_url, url, depth):
                subpaths.add(url.rstrip("/"))
    return subpaths


def scrape_subpaths(base_url: str, depth: int) -> set:
    """
    Iteratively scrape a URL and its subpaths up to the specified depth.

    Parameters:
        base_url (str): The base URL to start scraping from.
        depth (int): The maximum depth of subpaths to scrape.

    Returns:
        set: A set containing the visited URLs (base URL and its subpaths)

    Raises:
        ValueError: If the depth is a negative integer.
    """

    visited = set()
    queue = deque([base_url])

    if depth == 0:
        return set([base_url])

    while queue:
        current_url = queue.popleft()
        if current_url in visited:
            continue
        subpaths = get_subpaths(base_url, current_url, depth)
        visited.add(current_url)
        for path in subpaths:
            if path not in visited:
                queue.append(path)
    return visited


def crawl_and_download_images(base_url: str, depth: int, download_directory: str) -> None:
    """
    Crawls a website starting from the given base URL, extracting images up to the specified depth,
    and downloads them to the provided download directory.

    Parameters:
        base_url (str): The base URL from which the spider starts crawling.
        depth (int): The maximum depth to crawl for subpaths.
        download_directory (str): The directory where the downloaded images will be saved.

    Example:
        >>> spider("https://example.com/", depth=3, download_directory="images")
        The spider will crawl the website starting from "https://example.com/" up to a depth of 3.
        It will extract images found during the crawl and download them to the "images" directory.
    """

    # Scrapes subpaths
    subpaths = scrape_subpaths(base_url, 1)

    # Generates the URL pattern based on the Extension enum
    url_patterns = re.compile(generate_url_patterns(Extension))

    # Crawls the site for more directory
    images = set()
    for subpath in subpaths:
        new_images = scrape_images(subpath, url_patterns)
        if new_images:
            images.update(new_images)

    # Downloads images from urls
    for image in images:
        download_image(image, download_directory)

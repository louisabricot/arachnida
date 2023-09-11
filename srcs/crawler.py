import sys
import os
import argparse
import re
import logging

from spider.parse_utils import url_type, range_limited_int_type
from spider.scrape import retrieve_nested_urls, scrape_images
from spider.download_utils import download_image
from spider.url_utils import generate_url_patterns
from spider.image_utils import Extension


def crawl_website(url: str, depth: int, download_directory: str) -> None:
    """
    Crawls a website, extracts images, and dowloads them.

    Args:
        url (str): The URL of the website to crawl.
        depth (int): The maximum depth of recursive crawling.
        download_directory (str): The directory where downloaded images.

    Returns:
        None
    """

    # Scrape nested URLs
    nested_urls = retrieve_nested_urls(url, depth)

    # Generate the URL pattern based on the Extension enum
    url_patterns = re.compile(generate_url_patterns(Extension))

    # Scrape images in nested_urls
    image_urls = set()
    for nested_url in nested_urls:
        scraped_images = scrape_images(nested_url, url_patterns)
        if scraped_images:
            images_urls.update(scraped_images)

    # Download images from URLs
    for image_url in images_urls:
        download_image(image_url, download_directory)


def crawl():
    """
    Main function for crawling a website and downloading images.

    This function parses command-line arguments, sets up logging,
    and initiates the crawling process.

    Usage:
        scorpion [OPTIONS] url

    Options:
        url                         The website's URL.
        -r, --recursive             Enable recursive download.
        -l, --level                 The maximum depth of the recursive download (default: 5).
        -p                          The path where downloaded files will be saved (default: ./data)
    """
    # Se up command-line argument parser
    parser = argparse.ArgumentParser(
        description="Extracts images from the provided URL",
        epilog="Developed by louisabricot",
    )

    parser.add_argument("url", type=url_type, help="The website's URL")

    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        required="-l" in sys.argv,
        help="Enable recursive download",
    )

    parser.add_argument(
        "--level",
        "-l",
        type=range_limited_int_type,
        default=5,
        help="The maximum depth of the recursive download. Default is 5",
    )

    parser.add_argument(
        "-p",
        type=str,
        default="./data/",
        help="The path where the downloaded files will be saved. Default is ./data/",
    )

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        filename="crawl_website.log", encoding="utf-8", level=logging.ERROR
    )

    # Creates the download directory if it doesn't exist
    if not os.path.exists(args.p):
        os.makedirs(args.p)

    if not args.recursive:
        args.level = 0

    # Start crawling
    crawl_website(url=args.url.rstrip("/"), depth=args.level, download_directory=args.p)

from spider.parse_utils import url_type, range_limited_int_type
from spider.scrape import retrieve_nested_urls, scrape_images
from spider.download_utils import download_image
from spider.url_utils import generate_url_patterns, Extension
import sys
import os
import argparse
import re

def crawler(url: str, depth: int, download_directory: str) -> None:
    """
    Crawls a website starting from the given base URL, extracting images up to the specified depth,
    and downloads them to the provided download directory.

    Parameters:
        base_url (str): The base URL from which the spider starts crawling.
        depth (int): The maximum depth to crawl for nested_urls.
        download_directory (str): The directory where the downloaded images will be saved.
    """

    # Scrapes nested_urls
    nested_urls = retrieve_nested_urls(url, depth)

    print(nested_urls)
    exit(0)

    # Generates the URL pattern based on the Extension enum
    url_patterns = re.compile(generate_url_patterns(Extension))

    # Scrapes images in nested_urls
    images = set()
    for url in nested_urls:
        scraped_images = scrape_images(url, url_patterns)
        if scraped_images:
            images.update(scraped_images)

    # Downloads images from urls
    for image in images:
        download_image(image, download_directory)

def crawl():
    """
    Parse command-line arguments for extracting images from the provided URL.

    Returns:
        argparse.Namespace: The parsed arguments as a namespace object.
    """

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
        help="Recursive download",
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
    
    download_error_log = "download_error.log"

    # Creates the download directory
    if not os.path.exists(args.p):
        os.makedirs(args.p)

    # Creates error log file
    if not os.path.exists(download_error_log):
        with open(download_error_log, "w") as file:
            pass

    if not args.recursive:
        args.depth = 0

    crawler(url=args.url.rstrip('/'), depth=args.level, download_directory=args.p) 

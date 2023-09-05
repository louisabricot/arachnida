from spider.parse_utils import url_type, range_limited_int_type
from spider.scrape import scrape_subpaths, scrape_images
from spider.download_utils import download_image
from spider.url_utils import clean_url, generate_url_patterns, Extension
import sys
import os
import argparse
import re

def crawler(url: str, level: int, download_directory: str) -> None:
    """
    Crawls a website starting from the given base URL, extracting images up to the specified depth,
    and downloads them to the provided download directory.

    Parameters:
        base_url (str): The base URL from which the spider starts crawling.
        depth (int): The maximum depth to crawl for subpaths.
        download_directory (str): The directory where the downloaded images will be saved.
    """

    # Scrapes subpaths
    subpaths = scrape_subpaths(url, level)

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
        help="The maximum depth level of the recursive download. Default is 5",
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
        args.level = 0

    crawler(url=args.url.rstrip('/'), level=args.level, download_directory=args.p) 

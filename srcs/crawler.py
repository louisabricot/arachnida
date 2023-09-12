import sys
import os
import argparse
import re
import logging
from termcolor import colored

from spider.parse_utils import url_type, range_limited_int_type
from spider.scrape import retrieve_nested_urls, scrape_images
from spider.download_utils import download_image
from spider.image_utils import Extension

logo = r"""                   .                                          ||         
                   .                                          || 
                   .                                          ||
   _____        _\( )/_    _                                  ||
  / ____|        /(O)\    | |                                 || 
 | (___    _ __    _    __| |   ___   _ __                    ||
  \___ \  | '_ \  | |  / _` |  / _ \ | '__|                   ||
  ____) | | |_) | | | | (_| | |  __/ | |                      ||
 |_____/  | .__/  |_|  \__,_|  \___| |_|                _ /\  ||  /\ _ 
          |_|                                          / X  \.--./  X \
          |_|                                         /_/ \/`    `\/ \_\
                                                     /|(`-/\_/)(\_/\-`)|\
                                                    ( |` (_(.oOOo.)_) `| )
                                                    ` |  `//\(  )/\\`  | `
                                                v0.1  (  // ()\/() \\  )
"""


def crawl_website(
    url: str, depth: int, extensions: list, download_directory: str
) -> None:
    """
    Crawls a website, extracts images, and dowloads them.

    Args:
        url (str): The URL of the website to crawl.
        depth (int): The maximum depth of recursive crawling.
        download_directory (str): The directory where downloaded images.

    Returns:
        None
    """

    if depth > 0:
        print(colored(f"\n\n 🕸️   Finding paths from {url} with depth {depth}...", "white", attrs=["bold"]), end="")

    # Scrape nested URLs
    nested_urls = retrieve_nested_urls(url, depth)
    print("Found " + colored(f"{len(nested_urls)}", "white", "on_yellow") + " URLs")

    # Generate the URL pattern based on specified extensions
    url_patterns = r"(?:.(?!https?:\/\/))+.({})$".format("|".join(extensions))

    print(colored(f" 🔍  Scraping {len(nested_urls)} URLs for images ending with {extensions}...", "white", attrs=["bold"]), end="")
    # Scrape images in nested_urls
    image_urls = set()
    for nested_url in nested_urls:
        scraped_images = scrape_images(nested_url, url_patterns)
        if scraped_images:
            image_urls.update(scraped_images)

    print("Found " + colored(f"{len(image_urls)}", "white", "on_yellow") + " images")
    
    print(colored(f" ⬇️   Downloading {len(image_urls)} images to {download_directory}...", "white", attrs=["bold"]), end="")
    # Download images from URLs
    downloaded = 0
    for image_url in image_urls:
        downloaded += download_image(image_url, download_directory)
    print("Successfully downloaded " + colored(f"{downloaded}" + "/" + f"{len(image_urls)}", "white", "on_yellow") + " images")

    print(colored(f" ✅  Done!", "light_green", attrs=["bold"]))


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
        -e, --extension             The file extensions we want to download (default: jpg, jpeg, png, gif and bmp)
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

    parser.add_argument(
        "--extension",
        "-e",
        type=str,
        nargs="+",
        default=[e.value for e in Extension],
        help="File extensions to download. Default is jpg, jpeg, gif, png and bmp",
    )

    args = parser.parse_args()

    logging.basicConfig(filename="crawler.log", level=logging.ERROR)

    # Creates the download directory if it doesn't exist
    if not os.path.exists(args.p):
        os.makedirs(args.p)

    if not args.recursive:
        args.level = 0

    print(colored(logo, "light_grey", attrs=["bold"]), end="")

    print(colored(" ............................................................................\n", "dark_grey"))
    print("    :: Base URL         : " + colored(f"{args.url}", "white", attrs=["bold"]))
    print("    :: Extension(s)     : " + colored(f"{args.extension}", "white", attrs=["bold"]))
    if args.recursive:
        print("    :: Recursion        : depth " + colored(f"{args.level}", "white", attrs=["bold"]))
    else:
        print("    :: Recursion        : " + colored(f"{args.recursive}", "white", attrs=["bold"]))
    
    print(colored(" ............................................................................\n", "dark_grey"))

    # Start crawling
    crawl_website(
        url=args.url.rstrip("/"),
        depth=args.level,
        extensions=args.extension,
        download_directory=args.p,
    )

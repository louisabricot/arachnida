"""
Module Name: spider.py

Description:
This module defines a web crawling and file downloading tool called "Spider".
Spider is designed to crawl a specified website, extract files,
and download them to a specified directory.
It supports recursive crawling and allows users to filter files by extensions.

Usage:
To use Spider, run this script from the command line with the following options:

    spider [OPTIONS] url

Options:
- `url`: The URL of the website to crawl.

- `-r, --recursive`: Enable recursive download to explore nested URLs.

- `-l, --level`: The maximum depth of recursive download (default: 5).

- `-e, --extension`: Specify the file extensions to download
        (default: jpg, jpeg, png, gif, and bmp).

- `-p`: Specify the path where downloaded files will be saved (default: ./data).

This script utilizes the termcolor library to provide colored console output
for better user experience. It also logs errors to a file named "spider.log".

Note:
Make sure to configure and run this script from the command line to initiate
the web crawling and file downloading process.

Developed by louisabricot
"""

import sys
import os
import argparse
import logging
from termcolor import cprint, colored
from tools.parse_utils import url_type, range_limited_int_type
from tools.scrape import retrieve_nested_urls, scrape_files
from tools.download import download_file

LOGO = r"""                   .                                          ||
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
                                                      (  // ()\/() \\  ) """


def crawl_website(
    url: str, depth: int, extensions: list, download_directory: str
) -> None:
    """
    Crawls a website, extracts files, and dowloads them.

    Args:
        url (str): The URL of the website to crawl.
        depth (int): The maximum depth of recursive crawling.
        download_directory (str): The directory where downloaded files.

    Returns:
        None
    """

    if depth > 0:
        cprint(
            f"\n\n 🕸️   Finding paths from {url} with depth {depth}...",
            "white",
            attrs=["bold"],
        )

    # Scrape nested URLs
    nested_urls = retrieve_nested_urls(url, depth)

    print("Found " + colored(f"{len(nested_urls)}", "white", "on_yellow") + " URLs")


    cprint(
        f" 🔍  Scraping {len(nested_urls)} URLs for files ending with {extensions}...",
        "white",
        attrs=["bold"],
    )

    # Scrape files in nested_urls
    file_urls = set()
    for nested_url in nested_urls:
        scraped_files = scrape_files(nested_url, extensions)
        if scraped_files:
            file_urls.update(scraped_files)

    print("Found " + colored(f"{len(file_urls)}", "white", "on_yellow") + " files")
    cprint(
        f" ⬇️   Downloading {len(file_urls)} files to {download_directory}...",
        "white",
        attrs=["bold"],
    )
    # Download files from URLs
    downloaded = 0
    for file_url in file_urls:
        downloaded += download_file(file_url, download_directory)
    print(
        "Successfully downloaded "
        + colored(f"{downloaded}" + "/" + f"{len(file_urls)}", "white", "on_yellow")
        + " files"
    )

    cprint(" ✅  Done!", "light_green", attrs=["bold"])


def crawl():
    """
    Main function for crawling a website and downloading files.

    This function parses command-line arguments, sets up logging,
    and initiates the crawling process.

    Usage:
        spider [OPTIONS] url

    Options:
        url                         The website's URL.
        -r, --recursive             Enable recursive download.
        -l, --level                 The maximum depth of the recursive download (default: 5).
        -e, --extension             The file extensions we want to download
            (default: jpg, jpeg, png, gif and bmp)
        -p                          The path where downloaded files will be saved (default: ./data)
    """
    # Se up command-line argument parser
    parser = argparse.ArgumentParser(
        description="Extracts files from the provided URL",
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
        default=["jpg", "jpeg", "png", "gif", "bmp"],
        help="File extensions to download. Default is jpg, jpeg, gif, png and bmp",
    )

    args = parser.parse_args()

    logging.basicConfig(filename="spider.log", level=logging.ERROR)

    # Creates the download directory if it doesn't exist
    if not os.path.exists(args.p):
        os.makedirs(args.p)

    if not args.recursive:
        args.level = 0

    cprint(LOGO, "light_grey", attrs=["bold"])

    cprint(
        " ............................................................................\n",
        "dark_grey",
    )
    print(
        "    :: Base URL         : " + colored(f"{args.url}", "white", attrs=["bold"])
    )
    print(
        "    :: Extension(s)     : "
        + colored(f"{args.extension}", "white", attrs=["bold"])
    )
    if args.recursive:
        print(
            "    :: Recursion        : depth "
            + colored(f"{args.level}", "white", attrs=["bold"])
        )
    else:
        print(
            "    :: Recursion        : "
            + colored(f"{args.recursive}", "white", attrs=["bold"])
        )
    cprint(
        " ............................................................................\n",
        "dark_grey",
    )

    # Start crawling
    crawl_website(
        url=args.url.rstrip("/"),
        depth=args.level,
        extensions=args.extension,
        download_directory=args.p,
    )

from spider.scrape import crawl_and_download_images
from spider.parse import url_type, range_limited_int_type
import sys
import os
import argparse

def main(url, recursive, level, p):

    download_error_log = "download_error.log"

    # Creates the download directory
    if not os.path.exists(p):
        os.makedirs(p)

    # Creates error log file
    if not os.path.exists(download_error_log):
        with open(download_error_log, "w") as file:
            pass

    if not recursive:
        level = 0
    crawl_and_download_images(url, level, p)


if __name__ == "__main__":
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
    main(url=args.url.rstrip('/'), recursive=args.recursive, level=args.level, p=args.p) 

from spider.scrape import crawl_and_download_images
from spider.parse import parse_arguments


def main():

    download_error_log = "download_error.log"

    args = parse.parse_arguments()
    print(args)

    # Creates the download directory
    if not os.path.exists(args.p):
        os.makedirs(args.p)

    # Creates error log file
    if not os.path.exists(download_error_log):
        with open(download_error_log, 'w') as file:
            pass

    if not args.r:
        args.depth = 0
    crawl_and_download_images(args.url, args.depth, args.p)

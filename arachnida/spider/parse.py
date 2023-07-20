""" Parses and validates binary arguments """

import sys
import argparse
import validators

LEVEL_MIN_VAL = 1
LEVEL_MAX_VAL = 100


def url_type(arg):
    """Type function for argparse - validates the url"""

    validation = validators.url(arg, public=True)
    if validation:
        return arg
    raise argparse.ArgumentTypeError("Must be a valid url")


def range_limited_int_type(arg):
    """Type function for argparse - an integer within some predefined bounds"""

    try:
        num = int(arg)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Must be an integer number") from exc
    if num < LEVEL_MIN_VAL or num > LEVEL_MAX_VAL:
        raise argparse.ArgumentTypeError(
            "Argument must be < " + str(LEVEL_MAX_VAL) + "and > " + str(LEVEL_MIN_VAL)
        )
    return num


def parse():
    """Extracts images from the url provided as argument"""
    parser = argparse.ArgumentParser(
        description="Extracts images from the provided url",
        epilog="Developed by louisabricot",
    )

    parser.add_argument(
        "url",
        type=url_type,
        help="The website's url"
    )

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
    print("Hello " + repr(type(args)))

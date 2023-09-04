import argparse
import validators

LEVEL_MIN_VAL = 1
LEVEL_MAX_VAL = 100


def url_type(arg):
    """
    Type function for argparse - validates the URL.

    Parameters:
        arg (str): The input URL.

    Returns:
        str: The validated URL if it's a valid URL, otherwise raises an
        argparse.ArgumentTypeError.

    Raises:
        argparse.ArgumentTypeError: If the URL is not valid.
    """

    validation = validators.url(arg, public=True)
    if validation:
        return arg
    raise argparse.ArgumentTypeError("Must be a valid URL")


def range_limited_int_type(arg):
    """
    Type function for argparse - an integer within some predefined bounds.

    Parameters:
        arg (str): The input integer as a string.

    Returns:
        int: The integer value if it falls within the defined bounds
        (LEVEL_MIN_VAL to LEVEL_MAX_VAL), otherwise raises an
        argparse.ArgumentTypeError.

    Raises:
        argparse.ArgumentTypeError: If the input is not a valid integer or if
        it falls outside the specified range.
    """

    try:
        num = int(arg)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Must be an integer number") from exc
    if num < LEVEL_MIN_VAL or num > LEVEL_MAX_VAL:
        raise argparse.ArgumentTypeError(
            f"Argument must be < {LEVEL_MAX_VAL} and > {LEVEL_MIN_VAL}"
        )
    return num


def parse_arguments():
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

    return parser.parse_args()

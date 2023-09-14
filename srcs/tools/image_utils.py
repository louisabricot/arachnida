from enum import Enum


class Extension(Enum):
    """
    Enumeration representing image file extensions.

    Attributes:
        JPEG (str): Represents the 'jpeg' image file extension.
        JPG (str): Represents the 'jpg' image file extension.
        GIF (str): Represents the 'gif' image file extension.
        BMP (str): Represents the 'bmp' image file extension.
        PNG (str): Represents the 'png' image file extension.
    """

    JPEG = "jpeg"
    JPG = "jpg"
    GIF = "gif"
    BMP = "bmp"
    PNG = "png"


def image_has_valid_extension(image_name: str, valid_extensions: Extension) -> bool:
    """
    Checks if the given image file name has a valid extension.

    Args:
        image_name (str): The name of the image file to check.
        extensions (Extension): A list of valid file extensions to compare against.

    Returns:
        bool: true if the image file name has a valid extension, False otherwise.
    """

    if not image_name or not valid_extensions:
        return False

    # Make the extension comparison case-insensitive
    image_extension = image_name.lower().split(".")[-1]

    valid_extensions = [ext.lower() for ext in valid_extensions]

    return image_extension in valid_extensions

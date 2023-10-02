import argparse
import logging
import os
from PIL import Image, UnidentifiedImageError
import exifread
from termcolor import cprint


def display(information: dict):
    cprint("GENERAL INFORMATION\n", "white", attrs=["bold"])
    for key, value in information.items():
        if key == "stats":
            stats = value
            print(
                f"Mode                                       {format(stats.st_mode, 'o')}"
            )
            print(f"Size                                       {stats.st_size}")
            print(f"Owner                                      {stats.st_uid}")
            print(f"Group                                      {stats.st_gid}")
            print(f"Dev                                        {stats.st_dev}")
            print(f"INODE                                      {stats.st_ino}")
        elif key == "exif":
            cprint("\nEXIF INFORMATION\n", "white", attrs=["bold"])
            exif = value
            for key, value in exif.items():
                print(f"{key:36}       {str(value)[:30]}")
            print("todo")
        else:
            print(f"{key.capitalize():40}   {value}")


def parse_exif(filepath: str, thumbnail: bool) -> dict:
    exif = {}
    with open(filepath, "rb") as file:
        tags = exifread.process_file(file)
        for tag in tags.items():
            exif[tag] = tags[tag]
            if thumbnail and tag == "JPEGThumbnail":
                basename, extension = os.path.splitext(filepath)
                thumbnailpath = f"{basename}_thumbnail{extension}"
                with open(thumbnailpath, "wb") as file:
                    file.write(tags[tag])
    return exif


def parse_file(filepath: str, thumbnail: bool) -> None:
    information = {}
    filename, extension = os.path.splitext(filepath)
    information["filename"] = filename
    information["extension"] = extension
    information["stats"] = os.stat(filepath)

    try:
        with Image.open(filepath) as img:
            information["format"] = img.format
            information["resolution"] = img.size

            for key, value in img.info.items():
                if key == "exif":
                    information["exif"] = parse_exif(filepath, thumbnail)
                else:
                    information[key] = value
    except UnidentifiedImageError:
        # Is not an image
        logging.error("%s is not an image", filepath)

    finally:
        display(information)


def parse():
    """
    Main function for displaying file metadata and downloading thumbnails.

    This function parses command-line arguments, sets up logging,
    and initiates the parsing process.

    Usage:
        scorpio [OPTIONS] files

    Options:
        files               A list of files.
        -t, --thumbnail     Downloads the file's thumbnail.
    """

    parser = argparse.ArgumentParser(
        description="Displays file metadata",
        epilog="Developed by louisabricot",
    )

    parser.add_argument("files", nargs="+", help="the files to parse")

    parser.add_argument(
        "--thumbnail",
        "-t",
        action="store_true",
        help="Downloads the file's thumbnail",
    )
    args = parser.parse_args()

    logging.basicConfig(filename="scorpio.log", encoding="utf-8", level=logging.ERROR)

    for file in args.files:
        if not os.path.isfile(file):
            logging.error("%s is not a file", file)
            args.files.remove(file)
        else:
            parse_file(file, args.thumbnail)

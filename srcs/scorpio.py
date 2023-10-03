import argparse
import logging
import os
from PIL import Image, UnidentifiedImageError
import exifread
from termcolor import cprint
from datetime import datetime


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
            print(
                f"Last Modified                              {datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')}"
            )
            print(
                f"Created At                                 {datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M')}"
            )
            print(
                f"Last Accessed At                           {datetime.fromtimestamp(stats.st_atime).strftime('%Y-%m-%d %H:%M')}"
            )
        elif key == "exif":
            cprint("\nEXIF INFORMATION\n", "white", attrs=["bold"])
            exif = value
            for key, value in exif.items():
                print(f"{key:36}       {str(value)[:30]}")
        else:
            print(f"{key.capitalize():40}   {value}")


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
                    with open(filepath, "rb") as file:
                        information["exif"] = exifread.process_file(file)
                else:
                    information[key] = value
    except UnidentifiedImageError:
        # Is not an image
        logging.error("%s is not an image", filepath)

    finally:
        display(information)
        # faire le truc de thumbnail ici
        if (
            thumbnail
            and "exif" in information
            and "JPEGThumbnail" in information["exif"]
        ):
            basename, extension = os.path.splitext(filepath)
            thumbnailpath = f"{basename}_thumbnail{extension}"
            with open(thumbnailpath, "wb") as file:
                file.write(information["exif"]["JPEGThumbnail"])


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

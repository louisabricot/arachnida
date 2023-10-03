"""
scorpio.py - A utility for displaying file metadata and generating thumbnails.

This script provides functionality to display metadata information of files, including
file mode, size, owner, group, device, INODE, last modified time, created time,
and last accessed time.
Additionally, it can extract and display EXIF (Exchangeable Image File Format)
information from image files.

Usage:
    scorpio [OPTIONS] files

Options:
    files               A list of files to parse.
    -t, --thumbnail     Generate and download thumbnails for image files.

Developed by louisabricot

Example usage:
1. Display metadata for a file:
    scorpio file.txt

2. Display metadata for multiple files and generate thumbnails:
    scorpio -t file1.jpg file2.jpg

3. Display EXIF information for an image file:
    scorpio image.jpg
"""

import argparse
import logging
import os
from datetime import datetime
from PIL import Image, UnidentifiedImageError
import exifread
from termcolor import cprint


def display(information: dict):
    """
    Display the parsed information from a file in a structured format.

    :param information: A dictionary containing metadata information to be displayed.

    This function takes a dictionary of metadata information and displays
     it in a structured format. It prints general file information such as mode, size,
     owner, group, device, INODE, last modified time, created time, and last accessed time.

    If EXIF data is present in the dictionary, it also prints EXIF information
     in a separate section.

    Example usage:
    display({
        "filename": "example.jpg",
        "extension": ".jpg",
        "stats": <os.stat_result object>,
        "format": "JPEG",
        "resolution": (1920, 1080),
        "exif": {"Make": "Canon", "Model": "EOS 5D Mark III", ...},
        # Other metadata key-value pairs
    })
    """

    cprint("GENERAL INFORMATION\n", "white", attrs=["bold"])
    for key, value in information.items():
        if key == "stats":
            stats = value
            print(f"{'Mode':40} {format(stats.st_mode, 'o')}")
            print(f"{'Size':40} {stats.st_size}")
            print(f"{'Owner':40} {stats.st_uid}")
            print(f"{'Group':40} {stats.st_gid}")
            print(f"{'Dev':40} {stats.st_dev}")
            print(f"{'INODE':40} {stats.st_ino}")
            print(
                f"{'Last Modified':40} \
                {datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')}"
            )
            print(
                f"{'Created At':40}  \
                {datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M')}"
            )
            print(
                f"{'Last Accessed At':40} \
                {datetime.fromtimestamp(stats.st_atime).strftime('%Y-%m-%d %H:%M')}"
            )
        elif key == "exif":
            cprint("\nEXIF INFORMATION\n", "white", attrs=["bold"])
            exif = value
            for key, value in exif.items():
                print(f"{key:40} {str(value)[:30]}")
        else:
            print(f"{key.capitalize():40} {value}")


def parse_file(filepath: str, thumbnail: bool) -> None:
    """
    Parse metadata from a file, including owner ID, creation time, and EXIF data (if available).

    :param filepath: A string representing the path to the file.
    :param thumbnail: A boolean indicating whether to generate a thumbnail if possible.

    This function parses various metadata from the specified file,
    including the filename, extension, file stats, image format, resolution,
    and any additional image information. If the file is an image,
    it also extracts EXIF (Exchangeable Image File Format) data.

    If the `thumbnail` parameter is set to `True`
    and the file contains a JPEG thumbnail in its EXIF data,
    a thumbnail image will be generated and
    saved in the same directory with "_thumbnail" appended to
    the original filename.

    Note: This function may raise an UnidentifiedImageError
     if the specified file is not an image. In this case, a log is added to the log file.

    Example usage:
    parse_file("example.jpg", thumbnail=True)
    """
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
        logging.error("%s is not an image", filepath)

    finally:
        display(information)
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

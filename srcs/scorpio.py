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


def parse_file(filepath: str, thumbnail: bool) -> None:
    information = {}

    f = open(filepath, "rb")
    filename, extension = os.path.splitext(filepath)
    information["filename"] = filename
    information["extension"] = extension
    information["stats"] = os.stat(filepath)

    try:
        with Image.open(filepath) as img:
            information["format"] = img.format
            information["resolution"] = img.size

            for key, value in img.info.items():
                # TODO: if exif, alors parser avec exif parser
                if key == "exif":
                    exif = {}
                    tags = exifread.process_file(f)
                    for tag in tags.keys():
                        exif[tag] = tags[tag]
                        # print(f"{tag:50}       {str(tags[tag])[:30]}")
                        if thumbnail and tag == "JPEGThumbnail":
                            basename, extension = os.path.splitext(filepath)
                            thumbnailpath = f"{basename}_thumbnail{extension}"
                            with open(thumbnailpath, "wb") as file:
                                file.write(tags[tag])
                    information["exif"] = exif
                else:
                    information[key] = value
                    # print(f"{key}: {value}")
    except Exception as e:
        # Is not an image
        logging.error(f"An error occured: {str(e)}")

    finally:
        display(information)


def parse():
    parser = argparse.ArgumentParser(
        description="Displays images metadata",
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

import sys
import os
import argparse
import re
import logging
from spider import image_has_valid_extension, Extension
import exiftool


def exif_parser(image_paths: list) -> None:
    for image_path in image_paths:
        # Check that image has valid extensions
        if not image_has_valid_extension(image_path, Extension):
            logging.error(f"Invalid extension for image {image_path}")

        with exiftool.ExifToolHelper("~/Downloads/Image-ExifTool-12.65") as et:
            metadata = et.get_metadata(image_path)
            for d in metadata:
                print(
                    "{:20.20} {:20.20}".format(
                        d["SourceFile"], d["EXIF:DateTimeOriginal"]
                    )
                )
        """
        with Image.open(image_path) as img:
            print(img.info)
            print('------')
            exif_data = img.getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    print(f"{tag_name}: {value}")
        """


def parse():
    parser = argparse.ArgumentParser(
        description="Displays images metadata",
        epilog="Developed by louisabricot",
    )

    parser.add_argument("images", nargs="+", help="The images to parse")

    args = parser.parse_args()

    logging.basicConfig(filename="parser.log", encoding="utf-8", level=logging.ERROR)

    exif_parser(image_paths=args.images)

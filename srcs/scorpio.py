import argparse
import logging
import os
from PIL import Image, UnidentifiedImageError
import exifread

def parse_file(filepath: str, thumbnail: bool) -> None:
    f = open(filepath, 'rb')

    # check for bmp, gif, 
    # will work only with TIFF, JPEG, PNG, WEBP, HEIC
    tags = exifread.process_file(f)
    for tag in tags.keys():
        print(f"{tag:50}       {str(tags[tag])[:30]}")
        if thumbnail and tag == 'JPEGThumbnail':
            basename, extension = os.path.splitext(filepath)
            thumbnailpath = f"{basename}_thumbnail{extension}"
            with open(thumbnailpath, 'wb') as file:
                file.write(tags[tag])



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

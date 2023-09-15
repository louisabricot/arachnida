import argparse
import logging
import os

def parse_file(filepath: str) -> None:
    
    print("---- ", filepath, " ----")

    print("Size: %d", os.path.getsize(filepath))



def parse():
    parser = argparse.ArgumentParser(
        description="Displays images metadata",
        epilog="Developed by louisabricot",
    )

    parser.add_argument("files", nargs="+", help="the files to parse")

    args = parser.parse_args()

    logging.basicConfig(filename="scorpio.log", encoding="utf-8", level=logging.ERROR)
    for file in args.files:
        if not os.path.isfile(file):
            logging.error("%s is not a file", file)
            args.files.remove(file)
        else:
            parse_file(file)

import os
import logging
import string
import random
import requests


def generate_unique_fullpath(pathname: str, download_directory: str) -> str:
    # Split the filename and extension
    filename, extension = os.path.splitext(pathname)

    fullpath = os.path.join(download_directory, pathname)
    while os.path.exists(fullpath):
        random_string = "".join(random.choices(string.ascii_letters, k=4))
        new_filename = "".join([filename, random_string, extension])
        fullpath = os.path.join(download_directory, new_filename)
    return fullpath


def download_file(url: str, download_directory: str) -> bool:
    try:
        # Sends GET request to the file URL
        response = requests.get(url, allow_redirects=False, timeout=5)
        response.raise_for_status()

        fullpath = generate_unique_fullpath(os.path.basename(url), download_directory)

        # Copy the content of the file locally
        with open(fullpath, "wb") as file:
            file.write(response.content)
            return True

    except requests.exceptions.RequestException as e:
        logging.error("%s", str(e))
    return False

"""
A collection of utility functions for file operations and downloading files from URLs.

This module provides two main functions:

1. `generate_unique_filename(directory, filename)`:
   Generate a unique filename by appending a numeric counter if a file with the same name
   already exists in the specified directory.

2. `download_file(directory, url)`:
   Download a file from a given URL and save it to the specified directory.

These functions are designed to assist in managing files and handling file downloads efficiently.
"""

import os
import logging
import requests


def generate_unique_filename(directory: str, filename: str) -> str:
    """
    Generate a unique filename by appending a numeric counter if a file
    with the same name already exists in the directory.

    Parameters:
        directory (str): The directory where the file should be saved.
        filename (str): The desired filename.

    Returns:
        str: A unique filename that does not already exist in the directory.
    """
    # Get the full path of the desired file
    fullpath = os.path.join(directory, filename)

    if not os.path.exists(fullpath):
        return fullpath

    # If the file exists, generate a unique filename
    basename, extension = os.path.splitext(filename)
    counter = 1

    while True:
        # Generate a new filename with a numeric counter
        new_filename = f"{basename}_{counter}{extension}"
        fullpath = os.path.join(directory, new_filename)

        # If the new filename does not exist, return it
        if not os.path.exists(fullpath):
            return fullpath

        counter += 1


def download_file(directory: str, url: str) -> bool:
    """
    Download a file from a given URL and save it to a specified directory.

    Parameters:
        directory (str): The directory where the downloaded file should be saved.
        url (str): The URL of the file to be downloaded.

    Returns:
        bool: True if the file was successfully downloaded and saved, False otherwise.
    """
    try:
        # Sends GET request to the file URL
        response = requests.get(url, allow_redirects=False, timeout=5)

        response.raise_for_status()

        if response.status_code == 200:
            fullpath = generate_unique_filename(directory, os.path.basename(url))

            # Copy the content of the file locally
            with open(fullpath, "wb") as file:
                file.write(response.content)
            return True

    except requests.exceptions.RequestException as e:
        logging.error("%s", str(e))
    return False

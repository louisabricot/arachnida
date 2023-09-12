import os
import requests


def log_download_error(url: str, exception: Exception) -> None:
    """
    Logs the URL and the exception details to a log file.

    Parameters:
        url (str): The URL that resulted in the download error.
        exception (Exception): The exception that was raised during the
        download.

    Returns:
        None

    Example:
        >>> log_download_error("https://example.com/image.jpg", requests.exceptions.HTTPError("404 Not Found"))
    """

    log_file = "download_error.log"
    with open(log_file, "a") as file:
        file.write(f"URL: {url}\nError: {str(exception)}\n\n")


def download_image(url: str, download_directory: str) -> bool:
    """
    Downloads the image from the given url to the specified download directory.

    Parameters:
        url (str): The URL from which the image will be downloaded.
        download_directory (str): The directory were the image will be saved.

    Raises:
        requests.exceptions.RequestException: If there is an issue while making
        the HTTP request.

    Example:
        >>> download_image("https://example.com/image.jpg")
    """
    try:
        response = requests.get(url, allow_redirects=False)
        response.raise_for_status()

        image_path = os.path.join(download_directory, os.path.basename(url))
        with open(image_path, "wb") as file:
            file.write(response.content)
            return True
    except requests.exceptions.RequestException as e:
        log_download_error(url, e)
    return False

"""Extracts images from the url provided as argument"""
import requests
import html.parser
from bs4 import BeautifulSoup
from enum import Enum
import re
import os

# TODO: Scrape subpaths
# TODO: Create log file

class Extension(Enum):
    JPEG = "jpeg"
    JPG = "jpg"
    GIF = "gif"
    BMP = "bmp"
    PNG = "png"


def download_image(url):
    """ Downloads the image from url to the download directory """
    try:
        response = requests.get(url, allow_redirects=False)
        response.raise_for_status()
        image_path = os.path.join("test", os.path.basename(url))
        with open(image_path, 'wb') as file:
            file.write(response.content)
        print("Downloaded image from ", url)
    except request.exceptions.RequestException as e:
        print("Could not download image from ", url)
        #TODO: adds the url to a log file and the exception

def generate_url_patterns(extension_enum):
    """ Dynamically generate URL pattern ending in extension """
    extensions = [ext.value for ext in extension_enum]
    pattern = r"(?:.(?!https?:\/\/))+.({})$".format('|'.join(extensions))
    return pattern

def scrape_images(page_url, image_url_patterns):
    """ Parse html page for images with extension from Extension and download
    them """
    
    try:
        response = requests.get(page_url, allow_redirects=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        img_tags = soup.find_all('img', src=True)
        image_urls = []
        for img in img_tags:
            match = re.search(image_url_patterns, img['src'])
            if match:
                extracted_url = match.group()
                image_urls.append(extracted_url)
        
        # Remove duplicates from list 
        image_urls = list(dict.fromkeys(image_urls))

        # Downloads images from urls
        for image_url in image_urls:
            download_image(image_url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

def scrape_subpaths(base_url, depth):
    """ """

    subpaths = []
    

def main():
    """Extracts images from the url provided as argument"""
    #base_url = 'https://unsplash.com/fr/t/wallpapers'
    base_url = 'https://github.com/louisabricot'

    # Scrapes subpaths
    subpaths = scrape_subpaths(base_url)

    # Generates the URL pattern based on the Extension enum
    url_patterns = re.compile(generate_url_patterns(Extension))

    # Crawls the site for more directory
    subpaths = []
    subpaths.append(base_url)
    for subpath in subpaths:
        scrape_images(subpath, url_patterns)
    


if __name__ == "__main__":
    main()

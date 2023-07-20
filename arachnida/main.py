"""Extracts images from the url provided as argument"""
from urllib.parse import urljoin, urlparse
import requests
import html.parser
from bs4 import BeautifulSoup
from enum import Enum
import re
import os
from collections import deque

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
    except requests.exceptions.RequestException as e:
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
        response = requests.get(page_url, allow_redirects=True)
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

def check_subpath_is_in_scope(base_url, subpath, depth):
    """ Returns true if subpath is within base_url domain and within path depth """

    base_depth = len(re.findall('\/[^\/]+?', urlparse(base_url).path, re.IGNORECASE))
    
    if urlparse(base_url).netloc == urlparse(subpath).netloc:
        #print(urlparse(base_url).path + " vs " + urlparse(subpath).path)
        if urlparse(base_url).path in urlparse(subpath).path:
            #print(len(re.findall('\/[^\/]+?', urlparse(subpath).path, re.IGNORECASE)))
            #print(urlparse(subpath).path)
            if len(re.findall('\/[^\/]+?', urlparse(subpath).path, re.IGNORECASE)) - base_depth >= 0 and len(re.findall('\/[^\/]+?', urlparse(subpath).path, re.IGNORECASE)) <= depth:
                return True
    return False

def get_subpaths(url, depth, base_url):
    """ """
    subpaths = set()

    try:
        response = requests.get(url, allow_redirects=False, timeout=20)
        if response.status_code in (301, 302, 303, 307, 308):
            redirect = response.headers.get('Location')
            if redirect.startswith("/"):
                redirect = urljoin(url, redirect)
            if check_subpath_is_in_scope(base_url, redirect, depth):
                response = requests.get(url, allow_redirects=True, timeout=20)
            else:
                print(f"Redirect URL {response.headers.get('Location')} is not on {base_url}")
                return subpaths
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print(f"Failed to retrive dataa from {url}. Skipping")
        return subpaths

    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all(["link", "a"], href=True):
        path = link.get("href")
        if path and path.startswith("/"):
            path = (urljoin(url, path))
        if check_subpath_is_in_scope(base_url, path, depth):
            subpaths.add(path.rstrip("/"))
    return subpaths

def scrape_subpaths(base_url, depth):
    visited = set()
    queue = deque([base_url])

    if depth < 0:
        raise ValueError("Depth must be a non-negative integer")
    
    while queue:
        current_url = queue.popleft()
        if current_url in visited:
            continue
        new_paths = get_subpaths(current_url, depth, base_url)
        print("visited: " + current_url)
        #print(new_paths)
        visited.add(current_url)
        for path in new_paths:
            #print(path)
            if path not in visited:
                queue.append(path)
    return visited

def main():
    """ Extracts images from the url provided as argument """
    
    base_url = 'https://www.theatlantic.com/photo'

    # Scrapes subpaths
    subpaths = scrape_subpaths(base_url, 3)

    # Generates the URL pattern based on the Extension enum
    url_patterns = re.compile(generate_url_patterns(Extension))

    # Crawls the site for more directory
    for subpath in subpaths:
        scrape_images(subpath, url_patterns)

if __name__ == "__main__":
    main()

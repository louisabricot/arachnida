from enum import Enum
import requests

# Checks that the website is accessible

# Creates a directory with the correct permissions
def create_download_directory(download_directory):
    """ Creates the download directory if it does not exist """
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
        print('Created directory ' + download_directory + '...')
    else:
        print('Directory ' + download_directory + 'already exists...')

# Envoyer une requete GET vers le site  
def make_request(url):
    """ Makes a GET request to the url """
    response = request.get(url)
    print('response status=' + repr(response.status_code))



class Extension(Enum):
    """ List of allowed file extension to scrape """
    JPEG
    JPG
    GIF
    PNG
    BMP

class Image:
    """ """

    def __init__(self, url: str, data: Vector, extension: Extension):
        self.url = url
        self.data = data
        self.extension = extension

## About this project

This project is the first in a series of cybersecurity-related projects at school 42. It involves developing two programs:
- **spider**: a web scraper that recursively downloads any files matching the specified extensions,
- **scorpion**: a metadata parser and editor.

### Built with

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Getting Started

### Prerequisites

To run this project you'll need:
- python3
- pip3
- make

### Installation

1. Clone the repository
```bash
  git clone https://github.com/louisabricot/arachnida
  cd arachnida
```

2. Install required packages
```bash
  make install
```

3. Setup the project
```bash
  make
``` 

## Usage

Use `spider` to recursively download all *.png* and *.jpg* files, choosing the depth of recursion:

```bash
  spider https://example.com --recursive --level=2 -p ./downloaded_images/ --extension jpg png
```

Use `scorpio` to display files metadata and remove them:
```bash
  scorpio ./downloaded_images/ ...
```

### Running tests

To run tests, run the following command:

```bash
  make test
```

## Spider

A web scraper, also known as a web crawling tool, is a software application or script designed to automatically extract data from websites.

## Scorpion

## License

## References


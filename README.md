# Arachnida

This project is the first in a series of cybersecurity-related projects at school 42. It involves developing two programs:
- **spider**: a web scraper that recursively downloads any files matching the specified extensions,
- **scorpion**: a metadata parser and editor.

Both projects were developed in Python.

## Table of Content

- [Run locally](#run-locally)
  - [Running tests](#running-tests) 
- [Spider](#spider)
- [Scorpion](#scorpion)
- [References](#references)

## Run locally

Pre-requisites: 
- python3 and pip installed
- make

Clone the repository and run the `make` command:

```bash
  git clone https://github.com/louisabricot/arachnida/
  cd arachnida
  make
```

Run the scraping tool:

```bash
  spider https://example.com --recursive --level=2 -p ./downloaded_images/ --extension jpg jpeg png
```

Run the parsing tool:

```bash
  scorpion ./downloaded_images/
```

Or get help:

```bash
  spider --help
  scorpion --help
```

### Running tests

To run tests, run the following command:

```bash
  make test
```

## Spider

A web scraper, also known as a web crawling tool, is a software application or script designed to automatically extract data from websites.

## Scorpion

## References

# Arachnida: Cybersecurity Tools Suite
<!-- BADGIE TIME -->

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

<!-- END BADGIE TIME -->

Arachnida is a cybersecurity project at School 42, consisting in two essential programs:
- **spider**: A web scraper for downloading specific file types recursively,
- **scorpion**: A metadata parser and editor.

## Getting Started

### Requirements

To run this project, ensure you have:
- Python3
- Pip3
- Make

### Installation

1. Clone the repository:
```bash
  git clone https://github.com/louisabricot/arachnida
  cd arachnida
```

2. Install the required packages:
```bash
  make install
```

3. Setup the project:
```bash
  make
``` 

## Usage

### Spider

Download .png and .jpg files recursively:

```bash
  # usage: spider [-h] [--recursive] [--level LEVEL] [--path PATH] [--extension EXTENSION [EXTENSION ...]] url
  spider https://example.com --recursive --level=2 -p ./downloaded_images/ --extension jpg png
```

### Scorpio

Display file metadata and make edits:
```bash
  # usage: scorpio [-h] images [images ...]
  scorpio ./downloaded_images/ ...
```

### Running tests

To run tests:

```bash
  make test
```

## Project Status

This project is actively in development.

## References


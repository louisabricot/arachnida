# Arachnida: Cybersecurity Tools Suite

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
  spider https://example.com --recursive --level=2 -p ./downloaded_images/ --extension jpg png
```

### Scorpio

Display file metadata and make edits:
```bash
  scorpio ./downloaded_images/ ...
```

### Running tests

To run tests:

```bash
  make test
```

## License

## Project Status

This project is actively in development.

## References


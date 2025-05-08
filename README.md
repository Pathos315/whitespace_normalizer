# Whitespace Normalizer

A simple desktop application that normalizes whitespace and optionally autocorrects text. Designed specifically for use with Frontline IEP Direct and Frontline 504.

## Features

- Normalize whitespace by removing excessive spaces, tabs, and trailing whitespace
- Convert various quote types to standard single quotes
- Optional spell-checking and autocorrection
- Automatic clipboard copying for easy pasting
- Simple and intuitive GUI interface

## Installation

### Prerequisites

- Python 3.13 or higher
- Poetry package manager

### Setup

1. Clone the repository

   ```pwsh
   git clone https://github.com/yourusername/whitespace-normalizer.git
   cd whitespace-normalizer
   ```

2. Install dependencies using Poetry

   ```pwsh
   poetry install
   ```

## Usage

Run the application:

```pwsh
poetry run python main.py
```

### How to Use

1. Paste text with irregular spacing into the left input area
2. Toggle the "Enable Autocorrect" checkbox if you want spell checking
3. Click "Normalize" to process the text
4. The normalized text will appear in the right output area and be automatically copied to your clipboard
5. Paste the normalized text where needed

## Development

### Project Structure

- `main.py` - Application entry point
- `src/` - Source code directory
  - `core.py` - Core text processing functions
  - `gui.py` - GUI implementation with Tkinter
  - `log.py` - Logging functionality
- `tests/` - Unit tests

### Running Tests

Run the tests using pytest:

```pwsh
poetry run pytest
```

Some tests are currently skipped with `@pytest.mark.skip` and need to be updated.

## Technical Details

- Built with Python's Tkinter for the GUI
- Uses `pyspellchecker` for autocorrection capabilities
- Implements `pyperclip` for clipboard interaction
- Features a custom logging system with rotation capabilities

## License

[Your License Here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

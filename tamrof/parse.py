import tokenize
from pathlib import Path


def parse(filepath: Path):
    """Parse a source string into a list of tokens."""
    with filepath.open() as file:
        return list(tokenize.generate_tokens(file.readline))

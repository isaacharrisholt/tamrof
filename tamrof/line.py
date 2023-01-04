from dataclasses import dataclass
from typing import List


@dataclass
class Line:
    """A line represents a single line of code.

    This may be a single statement, or a multi-line statement that could be
    written as a single line.

    For example, the following are both represented by single Line objects:

    ```
    a = 1
    ```

    ```
    a = (
        1,
        2,
    )
    ```

    The latter is represented as a single Line because it could be written as a
    single line: `a = (1, 2)`.
    """
    tokens: List[str]
    indent: int

    def __str__(self):
        return ''.join(self.tokens)
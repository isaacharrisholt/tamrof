from dataclasses import dataclass
from typing import List, Union

from tamrof.tokens import Token, BREAK_POINT, NEWLINE, INDENT, COMMA
from tamrof import constants


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

    Lines may contain sub-lines, which are then used when breaking a line into
    multiple lines.
    """
    content: List[Union[Token, 'Line']]
    indent: int

    def __str__(self):
        content_with_indent = (
            ([INDENT] * self.indent) +
            self.content
        )
        return ''.join(str(c) for c in content_with_indent)

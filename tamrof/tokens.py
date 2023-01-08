from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Token:
    """A token is a single unit of code.

    This may be a single character, or a larger unit of code such as a string,
    number, or keyword.
    """
    value: str
    spaces_before: int = 0
    spaces_after: int = 0
    use_spaces_before: bool = True
    use_spaces_after: bool = True

    def __str__(self):
        value = ''

        if self.use_spaces_before:
            value += ' ' * self.spaces_before

        value += self.value

        if self.use_spaces_after:
            value += ' ' * self.spaces_after

        return value

    def __eq__(self, other):
        return self.value == other.value

    def without_spaces(self) -> 'Token':
        """Return a copy of this token without spaces before or after."""
        return Token(
            self.value,
            spaces_before=0,
            spaces_after=0,
            use_spaces_before=False,
            use_spaces_after=False,
        )

    def with_no_space_after(self) -> 'Token':
        """Return a copy of this token without a space after."""
        return Token(
            self.value,
            spaces_before=self.spaces_before,
            spaces_after=self.spaces_after,
            use_spaces_before=self.use_spaces_before,
            use_spaces_after=False,
        )


# Token definitions
DEF = Token('def', spaces_after=1)
COLON = Token(':', spaces_after=1)
COMMA = Token(',', spaces_after=1)
EQUALS = Token('=', spaces_before=1, spaces_after=1)
STAR = Token('*', spaces_before=1, spaces_after=1)
DOUBLE_STAR = Token('**')
OPEN_PAREN = Token('(')
CLOSE_PAREN = Token(')')
F_SLASH = Token('/', spaces_before=1, spaces_after=1)
RIGHT_ARROW = Token('->', spaces_before=1, spaces_after=1)
INDENT = Token('    ')
NEWLINE = Token('\n')

# Break points
BREAK_POINT = Token('')

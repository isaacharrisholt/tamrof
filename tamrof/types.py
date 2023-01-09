from abc import ABC, abstractmethod
from typing import Any, List, Type, TypeVar

from tamrof import constants

_T = TypeVar('_T', bound='TamrofNode')
_B = TypeVar('_B', bound='BreakableNode')


class TamrofNode(ABC):
    """A node in the Tamrof AST."""
    __BREAKABLE: bool = False

    def __init__(self, indent: int = 0):
        self.indent = indent

    @property
    def is_breakable(self) -> bool:
        return self.__BREAKABLE

    @classmethod
    @abstractmethod
    def from_ast(cls: Type[_T], node: Any) -> _T:
        raise NotImplementedError


class Line:
    """A line represents a single line of code."""
    def __init__(self, content: List[TamrofNode] = None, indent: int = 0):
        if content is None:
            content = []

        self.content = content
        self.indent = indent

    def __str__(self):
        content_with_indent: List[Any] = (
            ([' '] * self.indent) +
            [str(node) for node in self.content]
        )
        return ''.join(content_with_indent)

    def __len__(self):
        return len(str(self))

    @property
    def is_breakable(self) -> bool:
        return any(node.is_breakable for node in self.content)


class BreakableNode(TamrofNode, ABC):
    """A node that can be broken."""
    __BREAKABLE = True

    def __init__(self, lines: List[Line] = None, indent: int = 0):
        # Call to super() first as _get_default_lines() may need to use
        # self.indent
        super().__init__(indent=indent)

        if not lines:
            self.lines = self._get_default_lines()
        else:
            self.lines = lines

    def __str__(self):
        return self.to_string()

    def _get_string_rep(self) -> str:
        return '\n'.join(str(line) for line in self.lines)

    def to_string(self, prev: str = '') -> str:
        string_rep = self._get_string_rep()
        longest_line = max(self.lines, key=len)

        if string_rep == prev:
            # print('Same as previous')
            return string_rep
        elif len(longest_line) > constants.MAX_LINE_LENGTH:
            # print('Too long')
            # print(longest_line)
            # print(len(longest_line))
            # if len(self.lines) > 1:
            #     raise NotImplementedError
            return self.break_node().to_string(prev=string_rep)

        # print('Good')
        return string_rep

    @abstractmethod
    def _get_default_lines(self) -> List[Line]:
        raise NotImplementedError

    @abstractmethod
    def break_node(self: _B) -> _B:
        raise NotImplementedError

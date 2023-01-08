from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Type, TypeVar

from tamrof import constants

_T = TypeVar('_T', bound='TamrofNode')
_B = TypeVar('_B', bound='BreakableNode')


class TamrofNode(ABC):
    """A node in the Tamrof AST."""
    __BREAKABLE: bool = False

    indent: int = 0

    @property
    def is_breakable(self) -> bool:
        return self.__BREAKABLE

    @classmethod
    @abstractmethod
    def from_ast(cls: Type[_T], node: Any) -> _T:
        raise NotImplementedError


@dataclass
class Line:
    """A line represents a single line of code."""
    content: List[TamrofNode] = field(default_factory=list)
    indent: int = 0

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


@dataclass
class BreakableNode(TamrofNode, ABC):
    """A node that can be broken."""
    __BREAKABLE = True

    lines: List[Line] = field(default_factory=list, kw_only=True)

    def __str__(self):
        return self.to_string()

    def __post_init__(self):
        if not self.lines:
            self.lines = self._get_default_lines()

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

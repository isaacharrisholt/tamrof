import ast

from tamrof.types import TamrofNode
from typing import Any, Type
from dataclasses import dataclass


@dataclass
class Name(TamrofNode):
    """A node for a name."""
    __BREAKABLE = False

    value: Any

    def __str__(self):
        return str(self.value)

    @classmethod
    def from_ast(cls: Type['Name'], node: ast.Name) -> 'Name':
        return cls(node.id)


@dataclass
class Constant(TamrofNode):
    """A node for a constant."""
    __BREAKABLE = False

    value: Any

    def __str__(self):
        return repr(self.value)

    @classmethod
    def from_ast(cls: Type['Constant'], node: ast.Constant) -> 'Constant':
        return cls(node.value)

import ast

from tamrof.types import TamrofNode
from typing import Any, Type


class Name(TamrofNode):
    """A node for a name."""
    __BREAKABLE = False

    def __init__(self, value: Any, indent: int = 0):
        self.value = value
        super().__init__(indent=indent)

    def __str__(self):
        return str(self.value)

    @classmethod
    def from_ast(cls: Type['Name'], node: ast.Name) -> 'Name':
        return cls(node.id)


class Constant(TamrofNode):
    """A node for a constant."""
    __BREAKABLE = False

    def __init__(self, value: Any, indent: int = 0):
        self.value = value
        super().__init__(indent=indent)

    def __str__(self):
        return repr(self.value)

    @classmethod
    def from_ast(cls: Type['Constant'], node: ast.Constant) -> 'Constant':
        return cls(node.value)

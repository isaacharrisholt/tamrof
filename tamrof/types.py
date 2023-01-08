from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar

T = TypeVar('T', bound='TamrofNode')


class TamrofNode(ABC):
    """A node in the Tamrof AST."""
    __BREAKABLE: bool = False

    @property
    def is_breakable(self) -> bool:
        return self.__BREAKABLE

    @classmethod
    @abstractmethod
    def from_ast(cls: Type[T], node: Any) -> T:
        raise NotImplementedError

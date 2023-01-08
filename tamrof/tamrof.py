import ast
from typing import Any, List

from tamrof.nodes import FunctionDef
from tamrof.types import TamrofNode


class Tamrof(ast.NodeVisitor):
    def __init__(self):
        self.indent = 0
        self.nodes: List[TamrofNode] = []

    def __str__(self) -> str:
        return '\n'.join(str(node) for node in self.nodes)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.nodes.append(FunctionDef.from_ast(node))

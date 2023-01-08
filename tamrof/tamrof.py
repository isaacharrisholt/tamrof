import ast
from typing import Any, List
import weakref

from tamrof.nodes import FunctionDef
from tamrof.types import TamrofNode


class Tamrof(ast.NodeVisitor):
    def __init__(self):
        self.indent = 0
        self.nodes: List[TamrofNode] = []

    def __str__(self) -> str:
        return '\n'.join(str(node) for node in self.nodes)

    def generic_visit(self, node: ast.AST) -> Any:
        for child in ast.iter_child_nodes(node):
            child.parent = weakref.proxy(node)

        super().generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        is_method = isinstance(node.parent, ast.ClassDef)
        self.nodes.append(FunctionDef.from_ast(node, is_method=is_method))
        self.generic_visit(node)

import ast
import warnings
from typing import Any, List, Optional, Type, Union

from tamrof import constants, tokens
from tamrof.tokens import Token
from tamrof.types import TamrofNode, BreakableNode, Line, _B
from tamrof.nodes.expressions import Constant, Name

from dataclasses import dataclass, field


@dataclass
class FunctionName(TamrofNode):
    """A function name."""
    name: str

    def __str__(self):
        return f'def {self.name}('

    @classmethod
    def from_ast(
        cls: Type['FunctionName'],
        node: ast.FunctionDef,
    ) -> 'FunctionName':
        return cls(node.name)


@dataclass
class FunctionEnd(BreakableNode):
    """A function end."""
    annotation: Optional[TamrofNode] = None

    def __str__(self):
        if self.annotation:
            return f') -> {self.annotation}:'

        return '):'

    @classmethod
    def from_ast(
        cls: Type['FunctionEnd'],
        node: ast.FunctionDef,
    ) -> 'FunctionEnd':
        return cls(annotation=generate_annotation(node))

    def _get_default_lines(self) -> List[Line]:
        return [
            Line(content=[Constant(value=self.annotation)], indent=self.indent),
        ]

    def break_node(self: _B) -> _B:
        raise NotImplementedError


@dataclass
class FunctionArg(BreakableNode):
    """A function argument."""
    name: str
    annotation: Optional[TamrofNode] = None
    default: Optional[TamrofNode] = None
    prefix: str = ''

    @classmethod
    def from_ast(
        cls: Type['FunctionArg'],
        node: ast.arg,
        default: ast.Expr = None,
        prefix: str = '',
    ) -> 'FunctionArg':
        annotation = generate_annotation(node)
        default = generate_default(default)
        return cls(node.arg, annotation, default, prefix)

    def _get_default_lines(self) -> List[Line]:
        content = [self.annotation, self.default]
        return [Line(content=content, indent=self.indent)]

    def to_string(self, prev: str = '') -> str:
        result = self.prefix + self.name

        if self.annotation and self.default:
            result += f': {self.annotation} = {self.default}'
        elif self.annotation:
            result += f': {self.annotation}'
        elif self.default:
            result += f'={self.default}'

        return result

    def break_node(self: _B) -> _B:
        raise NotImplementedError


@dataclass
class FunctionArgs(BreakableNode):
    """A function's arguments."""
    args: List[FunctionArg] = field(default_factory=list)

    @classmethod
    def from_ast(
        cls: Type['FunctionArgs'],
        node: ast.FunctionDef,
    ) -> 'FunctionArgs':
        args: List[FunctionArg] = []
        defaults: List[Any] = (
            [None] * (len(node.args.args) - len(node.args.defaults)) +
            node.args.defaults
        )
        args_with_defaults = [
            (arg, default)
            for arg, default in zip(node.args.args, defaults)
        ]

        kwonly_defaults: List[Any] = (
            [None] * (len(node.args.kwonlyargs) - len(node.args.kw_defaults)) +
            node.args.kw_defaults
        )
        kwonlyargs_with_defaults = [
            (arg, default)
            for arg, default in zip(node.args.kwonlyargs, kwonly_defaults)
        ]

        for arg in node.args.posonlyargs:
            args.append(FunctionArg.from_ast(arg))

        if node.args.posonlyargs:
            args.append(FunctionArg(name='/'))

        for arg, default in args_with_defaults:
            args.append(FunctionArg.from_ast(arg, default))

        if node.args.vararg:
            args.append(FunctionArg.from_ast(node.args.vararg, prefix='*'))
        elif node.args.kwonlyargs:
            args.append(FunctionArg(name='*'))

        for arg, default in kwonlyargs_with_defaults:
            args.append(FunctionArg.from_ast(arg, default))

        if node.args.kwarg:
            args.append(FunctionArg.from_ast(node.args.kwarg, prefix='**'))

        return cls(args)

    def _get_default_lines(self) -> List[Line]:
        return [Line(content=self.args, indent=self.indent)]

    def to_string(self, prev: str = '') -> str:
        if len(self.lines) <= 1:
            return ', '.join(str(arg) for arg in self.args)

        return ',\n'.join(str(line) for line in self.lines) + ','

    def break_node(self: 'FunctionArgs') -> 'FunctionArgs':
        curr_indent = self.lines[0].indent
        new_indent = curr_indent + constants.INDENT_SIZE
        if new_indent > 10:
            warnings.warn('Indentation is too deep')
            return self
        return FunctionArgs(
            args=self.args,
            lines=[
                Line(content=[arg], indent=new_indent)
                for arg in self.args
            ]
        )


@dataclass
class FunctionDef(BreakableNode):
    """A node for a function definition."""
    name: FunctionName
    args: FunctionArgs
    end: FunctionEnd
    indent: int = 0
    is_method: bool = False

    @classmethod
    def from_ast(
        cls: Type['FunctionDef'],
        node: ast.FunctionDef,
        is_method: bool = False,
    ) -> 'FunctionDef':
        return cls(
            name=FunctionName.from_ast(node),
            args=FunctionArgs.from_ast(node),
            end=FunctionEnd.from_ast(node),
            indent=node.col_offset,
            is_method=is_method,
        )

    def _get_default_lines(self) -> List[Line]:
        return [
            Line(content=[self.name, self.args, self.end], indent=self.indent),
        ]

    def break_node(self: 'FunctionDef') -> 'FunctionDef':
        new_args = self.args.break_node()
        return FunctionDef(
            name=self.name,
            args=new_args,
            end=self.end,
            indent=self.indent,
            is_method=self.is_method,
            lines=[
                Line(content=[self.name], indent=self.indent),
                Line(content=[new_args], indent=self.indent),
                Line(content=[self.end], indent=self.indent),
            ],
        )

    def to_string(self, prev: str = '') -> str:
        string_rep = self._get_string_rep()
        if len(self.lines) <= 1:
            if len(string_rep) > constants.MAX_LINE_LENGTH:
                return self.break_node().to_string(prev=prev)

        return string_rep


def generate_annotation(
    obj: Union[ast.arg, ast.FunctionDef],
) -> Optional[TamrofNode]:
    """Handle an argument annotation."""
    if isinstance(obj, ast.FunctionDef):
        annotation = obj.returns
    else:
        annotation = obj.annotation

    if not annotation:
        return None
    elif isinstance(annotation, ast.Name):
        return Name.from_ast(annotation)
    elif isinstance(annotation, ast.Constant):
        return Constant.from_ast(annotation)
    elif isinstance(annotation, ast.Subscript):
        raise NotImplementedError
    else:
        raise ValueError(f'Unknown annotation: {ast.dump(annotation)}')


def generate_default(obj: Optional[ast.Expr]) -> Optional[TamrofNode]:
    """Handle an argument default."""
    if not obj:
        return None
    elif isinstance(obj, ast.Name):
        return Name.from_ast(obj)
    elif isinstance(obj, ast.Constant):
        return Constant.from_ast(obj)
    else:
        raise ValueError(f'Unknown default: {ast.dump(obj)}')

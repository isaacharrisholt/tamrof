import token
import tokenize
from pathlib import Path
from typing import Any, List

from tamrof import parse, Line


def handle_op(tkn: tokenize.TokenInfo):
    """Handle an operator token."""
    match tkn.string:
        case '+':
            return ' + '
        case '-':
            return ' - '
        case '(':
            return '('
        case ')':
            return ')'
        case ':':
            return ': '
        case ',':
            return ', '
        case '=':
            return ' = '
        case '.':
            return '.'
        case '[':
            return '['
        case ']':
            return ']'
        case '{':
            return '{'
        case '}':
            return '}'
        case _:
            raise ValueError(f'Unknown operator: {tkn.string}')


class Comment:
    pass


def main():
    """Main entry point for the script."""
    filepath = Path(__file__).parent / "test.py"
    filepath_tabs = Path(__file__).parent / "test_tabs.py"

    import ast
    a = ast.parse(filepath.read_text())

    lines = []

    for node in ast.walk(a):
        if not isinstance(node, ast.FunctionDef):
            continue

        print(node.name)
        print(ast.dump(node))

        # Construct a line for the function definition
        tokens = [
            'def',
            node.name,
            '(',
        ]

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

        print(args_with_defaults)

        for poa in node.args.posonlyargs:
            tokens.append(poa.arg)
            tokens.append(',')

        if node.args.posonlyargs:
            tokens.append('/')
            tokens.append(',')

        for arg, default in args_with_defaults:
            tokens.append(arg.arg)
            if default:
                tokens.append('=')
                tokens.append(repr(default.value))
            tokens.append(',')

        if node.args.vararg:
            tokens.append('*')
            tokens.append(node.args.vararg.arg)
            tokens.append(',')
        elif node.args.kwonlyargs:
            tokens.append('*')
            tokens.append(',')

        for arg, default in kwonlyargs_with_defaults:
            tokens.append(arg.arg)
            if default:
                tokens.append('=')
                tokens.append(repr(default.value))
            tokens.append(',')

        if node.args.kwarg:
            tokens.append('**')
            tokens.append(node.args.kwarg.arg)
            tokens.append(',')

        while tokens[-1] in (',', '/', '*'):
            tokens.pop()

        tokens.append(')')
        tokens.append(':')

        lines.append(Line(tokens, 0))

        print()

    print(lines)
    print()

    for line in lines:
        print(''.join(line.tokens))









def func():
    tokens = parse(Path(__file__).parent / "test.py")
    output = []
    line = ''
    curr_indent = 0
    last_type = None
    for tkn in tokens:
        print(tkn)
        # if tkn.string == 'i':
        #     print(tkn)
        #     exit()
        match tkn.type:
            case token.NAME:
                if last_type == token.NAME:
                    line += ' '
                line += tkn.string
            case token.NEWLINE:
                line = '    ' * curr_indent + line
                output.append(line.rstrip())
                line = ''
            case token.COMMENT:
                output.append(tkn.string)
            case token.INDENT:
                curr_indent += 1
            case token.DEDENT:
                curr_indent -= 1
            case token.OP:
                line += handle_op(tkn)
            case token.STRING:
                line += tkn.string
            case token.NUMBER:
                line += tkn.string

        last_type = tkn.type

    print('\n'.join(output))


if __name__ == '__main__':
    main()

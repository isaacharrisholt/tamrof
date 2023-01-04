import token
import tokenize
from pathlib import Path
from typing import Any, List

from tamrof import parse, Line, TokenType, Token


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

    lines: List[Line] = []

    for node in ast.walk(a):
        if not isinstance(node, ast.FunctionDef):
            continue

        print(node.name)
        print(ast.dump(node))

        # Construct a line for the function definition
        tokens = [
            TokenType.DEF.value,
            Token(node.name),
            TokenType.OPEN_PAREN.value,
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
            tokens.append(Token(poa.arg))
            tokens.append(TokenType.COMMA.value)

        if node.args.posonlyargs:
            tokens.append(TokenType.F_SLASH.value.without_spaces())
            tokens.append(TokenType.COMMA.value)

        for arg, default in args_with_defaults:
            tokens.append(Token(arg.arg))
            if default:
                tokens.append(TokenType.EQUALS.value.without_spaces())
                tokens.append(Token(repr(default.value)))
            tokens.append(TokenType.COMMA.value)

        if node.args.vararg:
            tokens.append(TokenType.STAR.value.without_spaces())
            tokens.append(Token(node.args.vararg.arg))
            tokens.append(TokenType.COMMA.value)
        elif node.args.kwonlyargs:
            tokens.append(TokenType.STAR.value.without_spaces())
            tokens.append(TokenType.COMMA.value)

        for arg, default in kwonlyargs_with_defaults:
            tokens.append(Token(arg.arg))
            if default:
                tokens.append(TokenType.EQUALS.value.without_spaces())
                tokens.append(Token(repr(default.value)))
            tokens.append(TokenType.COMMA.value)

        if node.args.kwarg:
            tokens.append(TokenType.DOUBLE_STAR.value)
            tokens.append(Token(node.args.kwarg.arg))
            tokens.append(TokenType.COMMA.value)

        while tokens[-1] in (
            TokenType.COMMA.value,
            TokenType.F_SLASH.value,
            TokenType.STAR.value,
        ):
            tokens.pop()

        tokens.append(TokenType.CLOSE_PAREN.value)
        tokens.append(TokenType.COLON.value)

        lines.append(Line(tokens, 0))

        print()

    print(lines)
    print()

    for line in lines:
        print(line)









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

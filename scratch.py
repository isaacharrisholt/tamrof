import token
import tokenize
from pathlib import Path
from typing import Any, List

from tamrof import parse, Line, tokens, Token


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
        token_list = [
            tokens.DEF,
            Token(node.name),
            tokens.OPEN_PAREN,
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
            token_list.append(Token(poa.arg))
            token_list.append(tokens.COMMA)

        if node.args.posonlyargs:
            token_list.append(tokens.F_SLASH.without_spaces())
            token_list.append(tokens.COMMA)

        for arg, default in args_with_defaults:
            token_list.append(Token(arg.arg))
            if default:
                token_list.append(tokens.EQUALS.without_spaces())
                token_list.append(Token(repr(default.value)))
            token_list.append(tokens.COMMA)

        if node.args.vararg:
            token_list.append(tokens.STAR.without_spaces())
            token_list.append(Token(node.args.vararg.arg))
            token_list.append(tokens.COMMA)
        elif node.args.kwonlyargs:
            token_list.append(tokens.STAR.without_spaces())
            token_list.append(tokens.COMMA)

        for arg, default in kwonlyargs_with_defaults:
            token_list.append(Token(arg.arg))
            if default:
                token_list.append(tokens.EQUALS.without_spaces())
                token_list.append(Token(repr(default.value)))
            token_list.append(tokens.COMMA)

        if node.args.kwarg:
            token_list.append(tokens.DOUBLE_STAR)
            token_list.append(Token(node.args.kwarg.arg))
            token_list.append(tokens.COMMA)

        while token_list[-1] in (
            tokens.COMMA,
            tokens.F_SLASH,
            tokens.STAR,
        ):
            token_list.pop()

        token_list.append(tokens.CLOSE_PAREN)
        token_list.append(tokens.COLON)

        lines.append(Line(token_list, 0))

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

import copy
import io
import tokenize
import ast
import token
from dataclasses import dataclass

LINE_LENGTH = 80

OPEN_BRACKETS = ('(', '[', '{')
CLOSE_BRACKETS = (')', ']', '}')


@dataclass
class Token:
    string: str
    type: int


def forces_split(tkn):
    return tkn.type in (tokenize.COMMENT,)


def to_split(lst: list[tokenize.Token]) -> bool:
    return any(forces_split(tkn) for tkn in lst)


@dataclass
class Line:
    tokens: list[tokenize.Token]

    def __str__(self):
        return ''.join(tkn.string for tkn in self.tokens)

    def __post_init__(self):
        self.tokens = [tkn for tkn in self.tokens if tkn.type != tokenize.ENCODING]

    @property
    def to_split(self):
        return (
            any(forces_split(tkn) for tkn in self.tokens)
            or len(str(self)) > LINE_LENGTH
        )

    @staticmethod
    def _split_line(line: 'Line', prev: 'Line' = None) -> list['Line']:
        # print(f'Splitting line: {line}')
        paren_tracker = 0
        if not line.to_split or prev == line or len(line.tokens) == 1:
            return [line]

        intermediate = []
        last_token = len(line.tokens) + 1
        has_split = False

        # For now, split after each comma between the first and last parens
        for i, tkn in reversed(list(enumerate(line.tokens))):
            if tkn.type == tokenize.ENCODING or not tkn.type:
                continue

            if tkn.string in CLOSE_BRACKETS:
                paren_tracker += 1
            elif tkn.string in OPEN_BRACKETS:
                paren_tracker = max(paren_tracker - 1, 0)
                if paren_tracker == 1:
                    continue

            if paren_tracker > 1:
                continue

            if tkn.string in CLOSE_BRACKETS:
                new_tokens = line.tokens[i:last_token]
                if not new_tokens:
                    continue

                new_line = Line(new_tokens)
                intermediate.append(new_line)
                last_token = i
                has_split = True
                continue

            elif tkn.string in OPEN_BRACKETS:
                new_tokens = line.tokens[i+1:last_token]
                if not new_tokens:
                    continue
                new_line = Line([Token('    ', tokenize.INDENT), *new_tokens])
                intermediate.append(new_line)
                last_token = i + 1
                has_split = True
                continue

            elif tkn.string == ',':
                new_line = Line([Token('    ', tokenize.INDENT), *line.tokens[i+1:last_token]])
                intermediate.append(new_line)
                last_token = i + 1
                has_split = True
                continue

            if has_split and paren_tracker == 0:
                # Ensure we only break on the first pair of parens
                break

        if last_token != 0:
            new_line = Line(line.tokens[:last_token])
            intermediate.append(new_line)

        splits = []

        for new_line in intermediate[::-1]:
            lines = Line._split_line(new_line, prev=line)
            splits.extend(lines)

        splits = [
            l for l in splits
            if str(l).strip()
        ]

        return splits

    def split_line(self) -> list['Line']:
        if not self.to_split:
            return [self]
        else:
            return self._split_line(self)


code = '''
def g(
    x,
    y: int,  # Some comment
    z, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w: tuple[str, int, int, int, int, int, int, int] = ('hi', 'there', 'how', 'are', ('youuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu', 'todayyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')),
):
    return x + y + z


print(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,)
'''

tree = ast.parse(code)

# for node in ast.walk(tree):
#     if not isinstance(node, ast.FunctionDef):
#         continue

unparsed = ast.unparse(tree).split('\n')

for section in unparsed:
    tkns = list(tokenize.tokenize(io.BytesIO(section.encode('utf-8')).readline))

    ln = Line(tkns)

    for l in ln.split_line():
        # print(line.original)
        print(str(l))
        ...

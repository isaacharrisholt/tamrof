# Some comment
import json


def test():
    print("test")


def test_with_json():
    print(
        json.dumps(
            [
                {"a": 1, "b": 2},
                {"a": 1, "b": 2},
                {"a": 1, "b": 2},
                {"a": 1, "b": 2},
                {"a": 1, "b": 2},
            ],
        ),
    )


def test_with_args(a, b):
    print(a, b)


def test_with_kwargs(a=1, b=2):
    print(a, b)  # Some inline comment


def test_with_posonlyargs(a, /, b):
    print(a, b)


def test_with_args_and_kwargs(a, b, c=3, d=4):
    print(a, b, c, d)


def test_with_args_and_kwargs_and_posonlyargs(a, b, /, c=3, d=4):
    print(a, b, c, d)


def test_with_args_and_kwargs_and_posonlyargs_and_varargs(a, b, /, c=3, d=4, *args):
    print(a, b, c, d, args)


def test_with_kwonlyargs(a, b=2, *, c=3, d=4):
    print(a, b, c, d)


def test_with_annotations(
    a: int,
    /,
    b: int = 2,
    *,
    c: str = '3',
    d: 'float' = 4.0
) -> None:
    print(a, b, c, d)
    print(a, b, c, d)
    print(a, b, c, d)


def test_with_long_annotation(
    a: 'This is a very long annotation that should be broken up into multiple lines',
    /,
    b: int = 2,
    *,
    c: str = '3',
    d: 'float' = 4.0
) -> None:
    print(a, b, c, d)
    print(a, b, c, d)
    print(a, b, c, d)


class Test:
    def test_self_annotation(self: 'Test'):
        print(self)


test()
test_with_args_and_kwargs_and_posonlyargs_and_varargs(1, 2, 3, 4, 5, 6, 7, 8, 9)


for i in range(10):
    test_with_json()


if True:
    test_with_args(1, 2)


while True:
    test_with_kwargs(3, 4)
    break

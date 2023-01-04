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
	print(a, b)


test()


for i in range(10):
	test_with_json()


if True:
	test_with_args(1, 2)


while True:
	test_with_kwargs(3, 4)
	break

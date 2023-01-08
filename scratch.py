import ast

from tamrof import Tamrof

with open('test.py') as f:
    a = ast.parse(f.read())

f = Tamrof()
f.visit(a)

for line in f.nodes:
    print(line)

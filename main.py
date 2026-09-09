from symbols import *
from quintuple import Quintuple
from quadruple import Quadruple
from parsing import parse
from symbols import Shift

FILE = "_input_turing_machine.txt"

quintuplas = parse(FILE)

for q in quintuplas:
    print(f"quintupla:   {q}")

    res = q.convert_to_quadruples()

    print(f"quadrupla 1: {res[0]}")
    print(f"quadrupla 2: {res[1]}")
    print()
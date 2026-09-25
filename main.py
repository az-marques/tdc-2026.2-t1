from symbols import *
from quintuple import Quintuple
from quadruple import Quadruple
from machine import ReversibleMachine
from parsing import parse
from symbols import RED, GREEN, RESET

FILE = "_input_turing_machine.txt"


parsed_info = parse(FILE)

rm = ReversibleMachine(
    quintuples=parsed_info["quintuples"],
    initial_state=parsed_info["initial_state"],
    accept_state=parsed_info["accept_state"],
    input_string=parsed_info["input_string"],
)

print(rm.print_current_configuration())

while(True):
    foo = input(f"\n[{GREEN}enter{RESET}] -> próximo step | [{RED}x{RESET}] -> sair: ")

    print()
    rm.step()

    if foo == "x":
        break
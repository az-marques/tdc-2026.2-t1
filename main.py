from symbols import *
from quintuple import Quintuple
from quadruple import Quadruple
from machine import ReversibleMachine
from parsing import parse

FILE = "_input_turing_machine.txt"


parsed_info = parse(FILE)

#TODO fazer o parse retornar as outras informações
rm = ReversibleMachine(quintuples=parsed_info["quintuples"], initial_state="1", input_string="0011")

print(rm.print_current_configuration())

while(True):
    foo = input("enter -> próximo step | x -> sair: ")

    print()
    rm.step()

    if foo == "x":
        break
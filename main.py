from symbols import *
from quintuple import Quintuple
from quadruple import Quadruple
from parsing import parse
from symbols import Shift

#exemplo dos tipos de dados
quintupla_exemplo = Quintuple(input_state="A", input_symbol="1", output_symbol="2", shift_direction=Shift.RIGHT, output_state="B")
quadrupla1_exemplo = Quadruple(input_state="A",input_tapes=["1"], output_tapes=["2"], output_state="C")
quadrupla2_exemplo = Quadruple(input_state="C",input_tapes=[DO_NOT_READ], output_tapes=[Shift.RIGHT], output_state="B")

print(quintupla_exemplo)
print(quadrupla1_exemplo)
print(quadrupla2_exemplo)

#TODO
#filepath = "exemplo.txt"
#quintuples = parse(filepath)
#quadruples = []
#for i in quintuples:
#    quad = i.convert()
#    quadruples.append(quad)
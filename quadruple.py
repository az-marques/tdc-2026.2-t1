from typing import List

from symbols import *

class Quadruple:
    #guarda uma quadrupla A [t_1, t_2, ..., t_n] -> [t'_1, t'_2, ..., t'_n] -> A'
    #input_state input_tapes -> output_tapes output_state
    #representa uma função de transição de uma máquina de turing reversível com n fitas
    #input_tapes e output_tapes devem ter o mesmo tamanho
    #para cada output_tapes[i], output_tapes[i] é um Shift se e somente se input_tapes[i] é DO_NOT_READ
    def __init__(self,input_state : str, input_tapes : List[str | type(DO_NOT_READ)],
                      output_tapes : List[str | Shift], output_state : str):
        self.input_state = input_state
        self.input_tapes = input_tapes
        self.output_state = output_state
        self.output_tapes = output_tapes

    def __str__(self):
        return f"{self.input_state} [{", ".join(self.input_tapes)}] -> [{", ".join(self.output_tapes)}] {self.output_state}"

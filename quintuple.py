import itertools

from typing import List

from symbols import Shift, DO_NOT_READ

from quadruple import Quadruple

class Quintuple:
    #contador para criar os estados auxiliares
    counter = itertools.count() 
    
    #guarda uma quintupla A T -> T' σ A'
    #input_state input_symbol -> output_symbol, shift_direction, output_state
    #representa uma função de transição de uma máquina de turing
    def __init__(self,input_state : str, input_symbol : str,
                      output_symbol : str, shift_direction : Shift,output_state : str):
        self.input_state = input_state
        self.input_symbol = input_symbol
        self.output_symbol = output_symbol
        self.shift_direction = shift_direction
        self.output_state = output_state

    def __str__(self):
        return f"{self.input_state} {self.input_symbol} -> {self.output_symbol} {self.shift_direction} {self.output_state}"

    #converte uma quintuple (ex: A T -> T' σ A') em uma lista de quadruples (ex: A T -> T' A'' e  A''[/,/,...] -> σ A'
    #cria novos estados de controle (A'' no exemplo)
    def convert_to_quadruples(self) -> List[Quadruple]:
        aux_state = f"{self.input_state}_aux{next(self.counter)}"
 
        #A[T] -> [T'] A''        
        quadruple_1 = Quadruple(
            input_state=self.input_state,
            input_tapes=[self.input_symbol],
            output_tapes=[self.output_symbol],
            output_state=aux_state,
        )
        
        #A''[/] -> [σ] A'        
        quadruple_2 = Quadruple(
            input_state=aux_state,
            input_tapes=[DO_NOT_READ],
            output_tapes=[self.shift_direction],
            output_state=self.output_state,
        )
        
        return [quadruple_1, quadruple_2]    
    
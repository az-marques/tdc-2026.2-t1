from collections import defaultdict
from typing import Dict, List, Optional, Tuple
 
from symbols import Shift, DO_NOT_READ, BLANK
from quadruple import Quadruple
from quintuple import Quintuple

class Tape:
    def __init__(self, content: str = ""):
        self.cells = defaultdict(lambda: BLANK)
        for i, ch in enumerate(content):
            self.cells[i] = ch
        self.head = 0 

    def read(self) -> str:
        return self.cells[self.head]

    def write(self, symbol: str):
        self.cells[self.head] = symbol

    def move(self, shift: Shift):
        if shift == Shift.RIGHT:
            self.head += 1
        elif shift == Shift.LEFT:
            self.head -= 1
        #se o shift for null -> cabeça fica parada

    def span(self) -> Tuple[int, int]:
        #menor e maior indice com simbolo nao branco
        index = [i for i, v in self.cells.items() if v != BLANK]
        if not index:
            return 0, -1
        return min(index), max(index)

    #retorna uma representação em string dos conteúdos e posição da cabeça da tape
    #ex se head=2 e cells = "0011" -> "0|0|[H]1|1"
    def contents(self) -> str:
        lo, hi = self.span()
        left_of_head = "|".join(self.cells[i] for i in range(lo, self.head))
        
        if left_of_head != "":
            left_of_head += "|"

        right_of_head = "|".join(self.cells[i] for i in range(self.head, hi+1))

        if right_of_head == "":
            right_of_head += BLANK
        
        return left_of_head + "[H]" + right_of_head

#máquina de turing reversível que simula uma máquina de turing clássica
#tem três fitas (main, history, e copy) e opera em três estágios: A (computação), B(cópia), C(restauração), conforme o artigo
class ReversibleMachine:
    def __init__(self, quintuples : List[Quintuple], initial_state : str, input_string : str):
        self.main_tape = Tape(content=input_string)
        self.history_tape = Tape()
        self.copy_tape = Tape()

        self.quadruples = {}

        self.state = f"A_{initial_state}_0"

        self.__stage_a_quadruples(quintuples)

    def __str__(self):
        quads_str = "Transições:\n"
        for quad_list in self.quadruples.values():
            for quad in quad_list:
                quads_str += str(quad) + "\n"

        current_state_str = f"Estado atual: {self.state}\n"

        tapes_str = f"Fita Principal:\n{" "*self.main_tape.head}H\n{self.main_tape.contents()}\n"
        tapes_str += f"Fita de História:\n{" "*self.history_tape.head}H\n{self.history_tape.contents()}\n"
        tapes_str += f"Fita de Cópia:\n{" "*self.copy_tape.head}H\n{self.copy_tape.contents()}\n"

        return quads_str + self.print_current_configuration()

    #returna uma string representando o estado atual da máquina e os conteúdos e posição da head de cada fita
    def print_current_configuration(self) -> str:
        current_state_str = f"Estado atual: {self.state}\n"

        tapes_str = f"Fita Principal:\n{self.main_tape.contents()}\n"
        tapes_str += f"Fita de História:\n{self.history_tape.contents()}\n"
        tapes_str += f"Fita de Cópia:\n{self.copy_tape.contents()}\n"

        return current_state_str + tapes_str

    #cria quadruples para o estágio A da máquina reversível (computação)
    def __stage_a_quadruples(self, quintuples: List[Quintuple]):
        aux_state_id = 1
        for quin in quintuples:
            input_state = f"A_{quin.input_state}_0"
            aux_state = f"A_{quin.input_state}_{aux_state_id}"
            output_state = f"A_{quin.output_state}_0"

            quadruple_1 = Quadruple(
                input_state=input_state,

                            # main tape             history tape        copy tape
                input_tapes= [quin.input_symbol,    DO_NOT_READ,        BLANK],
                output_tapes=[quin.output_symbol,   Shift.RIGHT,        BLANK],

                output_state=aux_state,
            )

            quadruple_2 = Quadruple(
                input_state=aux_state,
                
                            # main tape             history tape        copy tape
                input_tapes= [DO_NOT_READ,          BLANK,              DO_NOT_READ],
                output_tapes=[quin.shift_direction, f"{aux_state_id}",  Shift.NULL],

                output_state=output_state,
            )

            if input_state not in self.quadruples:
                self.quadruples[input_state] = [quadruple_1]
            else:
                self.quadruples[input_state].append(quadruple_1)
            
            self.quadruples[aux_state] = [quadruple_2]

            aux_state_id +=1
    
    def reject(self): #TODO implementar
        print("REJEITOU!!!")
        exit()
        return

    def step(self):
        quad = self.__find_transition()
        
        if quad == None:
            self.reject()
            return

        print(f"Aplicado {quad}")

        self.__apply_transition(quad)

        print(self.print_current_configuration())

    #encontra a quadrupla cujo padrao de leitura bate com o estado e fitas atuais
    def __find_transition(self) -> Optional[Quadruple]:
        for q in self.quadruples.get(self.state, []):
            if all(t_in == DO_NOT_READ or t_in == tape.read() for t_in, tape in zip(q.input_tapes, (self.main_tape,self.history_tape,self.copy_tape))):
                return q
        return None

    #aplica uma quadrupla encontrada sobre as fitas e move a máquina para o novo estado
    #leitura/escrita OU shift | nunca ambos na mesma fita
    def __apply_transition(self, quadruple: Quadruple) -> str:
        for t_in, t_out, tape in zip(quadruple.input_tapes, quadruple.output_tapes, (self.main_tape,self.history_tape,self.copy_tape)):
            if t_in == DO_NOT_READ:
                tape.move(t_out)
            else:
                tape.write(t_out)
        self.state = quadruple.output_state
        return
        


def invert_shift(shift: Shift) -> Shift:
    if shift == Shift.RIGHT:
        return Shift.LEFT
    if shift == Shift.LEFT:
        return Shift.RIGHT
    return Shift.NULL

def invert_quadruple(quad: Quadruple, rename=lambda s: s) -> Quadruple:
    new_in, new_out = [], []
    for t_in, t_out in zip(quad.input_tapes, quad.output_tapes):
        if t_in == DO_NOT_READ:
            new_in.append(DO_NOT_READ)
            new_out.append(invert_shift(t_out))
        else:
            new_in.append(t_out)
            new_out.append(t_in)

    return Quadruple(
        input_state=rename(quad.output_state),
        input_tapes=new_in,
        output_tapes=new_out,
        output_state=rename(quad.input_state),
    )

#
def run(initial_state: str, tapes: List[Tape], quadruples: List[Quadruple], max_steps: int = 100_000) -> Tuple[str, int]: 
    idx_quadruples = index_quadruples(quadruples)
    state = initial_state
    steps = 0
    
    while steps < max_steps:
        new_state = step(state, tapes, idx_quadruples)
        if new_state is None:
            break #maquina parou
        state = new_state
        steps += 1
    return state, steps
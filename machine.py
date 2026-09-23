from collections import defaultdict
from typing import Dict, List, Optional, Tuple
 
from symbols import Shift, DO_NOT_READ
from quadruple import Quadruple
from quintuple import Quintuple

class Tape:
    def __init__(self, blank: str, content: str = ""):
        self.blank = blank
        self.cells = defaultdict(lambda: blank)
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
        index = [i for i, v in self.cells.items() if v != self.blank]
        if not index:
            return 0, -1
        return min(index), max(index)

    def contents(self) -> str:
        lo, hi = self.span()
        return "".join(self.cells[i] for i in range(lo, hi+1))

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
    
#agrupa as quadruplas por input_state
#retorna um dict: estado -> lista de quadruplas que partem desse estado
def index_quadruples(quadruples: List[Quadruple]) -> Dict[str, List[Quadruple]]:
    index: Dict[str, List[Quadruple]] = defaultdict(list)
    for q in quadruples:
        index[q.input_state].append(q)
    
    return index

#tendo o estado atual e a lista de fitas, encontra a quadrupla cujo padrao de leitura bate
#com o que as cabecas estao lendo no momento
def find_transition(state: str, tapes: List[Tape], quadruples: Dict[str, List[Quadruple]]) -> Optional[Quadruple]:
    for q in quadruples.get(state, []):
        if all(t_in == DO_NOT_READ or t_in == tape.read() for t_in, tape in zip(q.input_tapes, tapes)):
            return q
    return None

#aplica uma quadrupla encontrada sobre as fitas e retorna o novo estado
#leitura/escrita OU shift | nunca ambos
def apply_transition(quadruple: Quadruple, tapes: List[Tape]) -> str:
    for t_in, t_out, tape in zip(quadruple.input_tapes, quadruple.output_tapes, tapes):
        if t_in == DO_NOT_READ:
            tape.move(t_out)
        else:
            tape.write(t_out)
    return quadruple.output_state

#executa um unico passo da maquina a partir do estado atual
#retorna o novo estado ou se a maquina parou
def step(state: str, tapes: List[Tape], quadruples: Dict[str, List[Quadruple]]) -> Optional[str]:
    quadruple = find_transition(state, tapes, quadruples)
    if quadruple is None:
        return None
    return apply_transition(quadruple, tapes)

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
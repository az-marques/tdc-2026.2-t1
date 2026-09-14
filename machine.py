from collections import defaultdict
from typing import List, Tuple
 
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
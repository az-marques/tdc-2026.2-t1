from quintuple import Quintuple
from typing import List
from symbols import *

#recebendo um arquivo plaintext definindo quintuplas de uma máquina de turing, interpreta o arquvio e retorna elas como uma lista de objetos Quintuple
#considerando a entrada A T -> T' σ A'
def parse(filepath) -> List[Quintuple]:
    quintuples = []
    
    with open(filepath, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, start=1):
            line = line.strip()
            
            if not line or line.startswith("#"):
                continue
            
            parts = line.split()
            if len(parts) != 6 or parts[2] != "->":
                raise ValueError(f"problema de formatacao com a linha {line_num}: {line}\n")
            
            A, T, arrow, T_line, sigma, A_line = parts
            quintuples.append(
                Quintuple(
                    input_state=A,
                    input_symbol=T,
                    output_symbol=T_line,
                    shift_direction=Shift(sigma),
                    output_state=A_line,
                )
            )
        
        return quintuples
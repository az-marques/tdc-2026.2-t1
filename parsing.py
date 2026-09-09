import re
from quintuple import Quintuple
from typing import List
from symbols import *

#recebendo um arquivo plaintext definindo quintuplas de uma máquina de turing, interpreta o arquvio e retorna elas como uma lista de objetos Quintuple
#considerando a entrada (A,T)=(A',T',σ)
def parse(filepath) -> List[Quintuple]:
    quintuples = []
    
    with open(filepath, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, start=1):
            line = line.strip()
            
            if not line or not line.startswith("("):
                continue
            
            parts = re.split(r"[(,)=]",line)
            quintuples.append(
                Quintuple(
                    input_state=parts[1],
                    input_symbol=parts[2],
                    output_symbol=parts[6],
                    shift_direction=Shift(parts[7]),
                    output_state=parts[5],
                )
            )
        
        return quintuples
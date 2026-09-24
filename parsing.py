import re
from quintuple import Quintuple
from typing import List
from symbols import *

#recebendo um arquivo plaintext definindo uma máquina de turing, interpreta o arquvio e retorna um dicionário com as informações da máquina
def parse(filepath) -> dict:
    quintuples = []
    
    with open(filepath, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, start=1):
            line = line.strip()
            
            #TODO fazer o parse retornar as outras informações
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
        
        #TODO fazer o parse retornar as outras informações
        parsed = {
            "quintuples" : quintuples,
            "initial_state" : None,
            "input_string" : None,
            "accept_state" : None
        }

        return parsed
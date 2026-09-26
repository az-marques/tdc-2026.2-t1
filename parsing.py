import re
from typing import List
from quintuple import Quintuple
from symbols import *

#recebe um arquivo plaintext definindo uma maquina de Turing, interpreta o arquivo e retorna um dicionario com as infos da maquina
def parse(filepath) -> dict:
    quintuples = []
    
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()]
        
        #linha 1: num_states | num_sym_in | num_sym_tape | num_transitions
        header = lines[0].split()
        num_states      = int(header[0])
        num_sym_in      = int(header[1])
        num_sym_tape    = int(header[2])
        num_transitions = int(header[3])
        
        #linha 2: estados
        states = lines[1].split()
        
        #linha 3: alfabeto de entrada
        alphabet_in = lines[2].split()
        
        #linha 4: alfabeto da fita
        alphabet_tape = lines[3].split()
        
        #estados finais e iniciais
        initial_state = states[0]  if states else None 
        accept_state  = states[-1] if states else None 
        
        #regex para extrair os componentes de cada transicao no formato (q_in, s_in)=(q_out, s_out, dir)
        pattern = re.compile(r"^\((\S+),(\S+)\)=\((\S+),(\S+),(\S+)\)$")

        #transicoes (linha 4 a 4 + num_transitions)
        transition_lines = lines[4 : 4 + num_transitions]
        for line in transition_lines:
            match = pattern.match(line)
            if not match:
                raise ValueError(f"sintaxe invalida na linha: '{line}'")
            
            q_in, s_in, q_out, s_out, shift = match.groups()
            
            quintuples.append(
                Quintuple(
                    input_state=q_in,
                    input_symbol=s_in,
                    output_state=q_out,
                    output_symbol=s_out,
                    shift_direction=Shift(shift),
                )
            )

        #cadeia de entrada
        input_string_index = 4 + num_transitions
        input_string = lines[input_string_index] if len(lines) > input_string_index else ""
        
        parsed = {
            "num_states": num_states,
            "num_sym_in": num_sym_in,
            "num_sym_tape": num_sym_tape,
            "num_transitions": num_transitions,
            "states": states,
            "alphabet_in": alphabet_in,
            "alphabet_tape": alphabet_tape,
            "quintuples": quintuples,
            "initial_state": initial_state,
            "accept_state": accept_state,
            "input_string": input_string
        }
        
        return parsed


def print_parsed_machine(parsed: dict):
    print("informacoes parseadas do arquivo")
    
    #dados de configuração
    print(f"numero de estados:      {parsed['num_states']}")
    print(f"simbolos de entrada:    {parsed['num_sym_in']}")
    print(f"simbolos da fita:       {parsed['num_sym_tape']}")
    print(f"numero de transicoes:   {parsed['num_transitions']}")
    print(f"estados:                {parsed['states']}")
    print(f"alfabeto de entrada:    {parsed['alphabet_in']}")
    print(f"alfabeto da fita:       {parsed['alphabet_tape']}")
    print(f"estado inicial:         {parsed['initial_state']}")
    print(f"estado de aceitação:    {parsed['accept_state']}")
    print(f"cadeia de entrada:      '{parsed['input_string']}'")
    
    print("\nquintuplas lidas")
    for idx, q in enumerate(parsed['quintuples'], start=1):
        print(f"  {idx:02d}. δ({q.input_state}, {q.input_symbol}) = ({q.output_state}, {q.output_symbol}, {q.shift_direction})")
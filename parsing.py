import re

from quintuple import Quintuple
from symbols import *


#recebe um objeto tipo arquivo e retorna um dicionário
#com as informações da máquina de Turing
def parse(file) -> dict:
    quintuples = []

    #le todas as linhas, removendo espaços e linhas vazias
    lines = [line.strip() for line in file if line.strip()]

    if not lines:
        raise ValueError("arquivo de entrada vazio")

    #linha 1:
    #num_states num_sym_in num_sym_tape num_transitions
    header = lines[0].split()

    if len(header) != 4:
        raise ValueError(
            "cabeçalho inválido: esperado "
            "'num_states num_sym_in num_sym_tape num_transitions'"
        )

    num_states = int(header[0])
    num_sym_in = int(header[1])
    num_sym_tape = int(header[2])
    num_transitions = int(header[3])

    #linha 2: estados
    states = lines[1].split()

    #linha 3: alfabeto de entrada
    alphabet_in = lines[2].split()

    #linha 4: alfabeto da fita
    alphabet_tape = lines[3].split()

    #estado inicial = primeiro estado
    #estado de aceitação = último estado
    initial_state = states[0] if states else None
    accept_state = states[-1] if states else None

    #formato:
    #(q_in,s_in)=(q_out,s_out,direcao)
    pattern = re.compile(r"^\((\S+),(\S+)\)=\((\S+),(\S+),(\S+)\)$")

    #transições começam na linha 5
    transition_lines = lines[4:4 + num_transitions]

    if len(transition_lines) != num_transitions:
        raise ValueError(
            f"esperadas {num_transitions} transições, "
            f"mas foram encontradas {len(transition_lines)}"
        )

    for line in transition_lines:
        match = pattern.match(line)

        if not match:
            raise ValueError(f"sintaxe inválida na transição: '{line}'")

        q_in, s_in, q_out, s_out, shift = match.groups()

        try:
            shift_direction = Shift(shift)
        except ValueError:
            raise ValueError(f"direção inválida '{shift}' na transição '{line}'")

        quintuples.append(
            Quintuple(
                input_state=q_in,
                input_symbol=s_in,
                output_state=q_out,
                output_symbol=s_out,
                shift_direction=shift_direction,
            )
        )

    #depois das transições vem a cadeia de entrada
    input_string_index = 4 + num_transitions

    input_string = (
        lines[input_string_index]
        if len(lines) > input_string_index
        else ""
    )

    return {
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
        "input_string": input_string,
    }


def print_parsed_machine(parsed: dict):
    print("informações parseadas do arquivo")

    print(f"número de estados:      {parsed['num_states']}")
    print(f"símbolos de entrada:    {parsed['num_sym_in']}")
    print(f"símbolos da fita:       {parsed['num_sym_tape']}")
    print(f"número de transições:   {parsed['num_transitions']}")
    print(f"estados:                {parsed['states']}")
    print(f"alfabeto de entrada:    {parsed['alphabet_in']}")
    print(f"alfabeto da fita:       {parsed['alphabet_tape']}")
    print(f"estado inicial:         {parsed['initial_state']}")
    print(f"estado de aceitação:    {parsed['accept_state']}")
    print(f"cadeia de entrada:      '{parsed['input_string']}'")

    print("\nquíntuplas lidas")

    for idx, q in enumerate(parsed["quintuples"], start=1):
        print(
            f"  {idx:02d}. "
            f"δ({q.input_state}, {q.input_symbol}) = "
            f"({q.output_state}, "
            f"{q.output_symbol}, "
            f"{q.shift_direction})"
        )
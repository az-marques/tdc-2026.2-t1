from enum import StrEnum

#enum representando a direção de um shift de uma cabeça da máquina
class Shift(StrEnum):
    RIGHT = "+"
    NULL = "0"
    LEFT = "-"

#constante que guarda o símbolo que significa que uma fita em uma quadrupla não é lida
DO_NOT_READ = "/"
from enum import StrEnum

#cores ansi para o terminal
RESET  = "\033[0m"
RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"

#enum representando a direção de um shift de uma cabeça da máquina
class Shift(StrEnum):
    RIGHT = "R"
    NULL = "S"
    LEFT = "L"

#constante que guarda o símbolo que significa que uma fita em uma quadrupla não é lida
DO_NOT_READ = "/"

#constante que guarda o símbolo que representa um espaço vazio em uma fita
BLANK = "B"

#indica que a cabeca esta na borda da fita
BOUNDARY = object()
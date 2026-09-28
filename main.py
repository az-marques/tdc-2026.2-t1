import sys
import io

from machine import ReversibleMachine
from parsing import parse
from symbols import *


def main():
    if sys.stdin.isatty():
        print(
            "Forneça a máquina pela entrada padrão. Exemplo:\n"
            "  python main.py < arq.txt"
        )
        return

    input_data = sys.stdin.read()

    parsed_info = parse(io.StringIO(input_data))

    if sys.platform == "win32":
        sys.stdin = open("CONIN$", "r")
    else:
        sys.stdin = open("/dev/tty", "r")

    rm = ReversibleMachine(
        quintuples=parsed_info["quintuples"],
        initial_state=parsed_info["initial_state"],
        accept_state=parsed_info["accept_state"],
        input_string=parsed_info["input_string"],
        alphabet_tape=parsed_info["alphabet_tape"],
    )

    print(rm.print_current_configuration())

    while not rm.halted:
        command = input(
            f"\n"
            f"[{GREEN}enter/1{RESET}] -> 1 passo | "
            f"[{CYAN}r{RESET}] -> rodar inteira | "
            f"[{RED}x{RESET}] -> sair: "
        ).strip().lower()

        print()

        if command in ("", "1"):
            rm.step()

        elif command == "r":
            while not rm.halted:
                rm.step()

        elif command in ("x", "q", "s"):
            print(f"{YELLOW}Execução encerrada.{RESET}")
            break

        else:
            print(f"{RED}Opção inválida.{RESET}")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(f"\n{YELLOW}Execução interrompida pelo usuário.{RESET}")
        sys.exit(0)
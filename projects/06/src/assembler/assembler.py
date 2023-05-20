from .parser import Parser
from . import code
from .symbol_table import SymbolTable


class Assembler:
    def __init__(self, file):
        self.__parser = Parser(file)
        self.__symbols = SymbolTable()
        self.__variable_address = 15

        # Add default symbols to table
        default_symbols = [
            ("SP", 0),
            ("LCL", 1),
            ("ARG", 2),
            ("THIS", 3),
            ("THAT", 4),
            ("SCREEN", 16384),
            ("KBD", 24576),
        ]
        for i in range(16):
            default_symbols.insert(i, ("R" + str(i), i))

        for symbol, address in default_symbols:
            self.__symbols.add_entry(symbol, address)

    def __label_pass(self):
        self.__parser.reset()
        instruction = -1
        while self.__parser.has_more_lines():
            self.__parser.advance()
            if (
                self.__parser.instruction_type() == "A_INSTRUCTION"
                or self.__parser.instruction_type() == "C_INSTRUCTION"
            ):
                instruction += 1
            elif self.__parser.instruction_type() == "L_INSTRUCTION":
                self.__symbols.add_entry(self.__parser.symbol(), instruction + 1)
            else:
                raise ValueError(
                    "Instruction not supported: "
                    + self.__parser.instructions[self.__parser.current_instruction]
                )

    def __assembly_pass(self):
        self.__parser.reset()
        instruction = -1
        machine_code = []
        while self.__parser.has_more_lines():
            self.__parser.advance()
            if self.__parser.instruction_type() == "A_INSTRUCTION":
                instruction += 1
                if is_number(self.__parser.symbol()):
                    machine_code.append(bin(int(self.__parser.symbol()))[2:].zfill(16))
                else:
                    machine_code.append(
                        self.__variable(self.__parser.symbol(), instruction)
                    )
            elif self.__parser.instruction_type() == "C_INSTRUCTION":
                instruction += 1
                machine_code.append(
                    "111"
                    + code.comp(self.__parser.comp())
                    + code.dest(self.__parser.dest())
                    + code.jump(self.__parser.jump())
                )
            elif self.__parser.instruction_type() == "L_INSTRUCTION":
                continue
            else:
                raise ValueError(
                    "Instruction not supported: "
                    + self.__parser.instructions[self.__parser.current_instruction]
                )
        return machine_code

    def assemble(self):
        self.__label_pass()
        return self.__assembly_pass()

    def __variable(self, value, address):
        if self.__symbols.contains(value):
            return bin(self.__symbols.get_address(value))[2:].zfill(16)
        else:
            self.__variable_address += 1
            self.__symbols.add_entry(value, self.__variable_address)
            return bin(self.__variable_address)[2:].zfill(16)


def is_number(symbol):
    try:
        int(symbol)
        return True
    except ValueError:
        return False

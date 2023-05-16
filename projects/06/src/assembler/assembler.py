from .parser import Parser
from . import code


class Assembler:
    def __init__(self, file):
        self.parser = Parser(file)

    def assemble(self):
        machine_code = []
        instruction = -1
        while self.parser.has_more_lines():
            self.parser.advance()
            instruction += 1
            if self.parser.instruction_type() == "A_INSTRUCTION":
                machine_code.append(bin(int(self.parser.symbol()))[2:].zfill(16))
            elif self.parser.instruction_type() == "C_INSTRUCTION":
                machine_code.append(
                    "111"
                    + code.comp(self.parser.comp())
                    + code.dest(self.parser.dest())
                    + code.jump(self.parser.jump())
                )
            else:
                raise ValueError(
                    "Instruction not supported: "
                    + self.parser.instructions[self.parser.current_instruction]
                )
        return machine_code

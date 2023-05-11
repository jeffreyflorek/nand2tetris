from enum import Enum
from collections import deque


class Parser:
    current_instruction = ""

    def __init__(self, in_filename):
        self.instructions = deque([])
        with open(in_filename) as f:
            for line in f:
                instruction = line.strip()
                if not instruction:
                    continue
                elif instruction[:2] == "//":
                    continue
                else:
                    self.instructions.append(instruction)

    def has_more_lines(self):
        return len(self.instructions) > 0

    def advance(self):
        if self.has_more_lines():
            self.current_instruction = self.instructions.popleft()
        else:
            raise Exception("advance called with no remaining instruction")

    def instruction_type(self):
        if not self.current_instruction:
            raise Exception("current_instruction must not be empty")
        elif self.current_instruction[0] == "@":
            return Instruction.A_INSTRUCTION
        elif self.current_instruction[0] == "(" and self.current_instruction[-1] == ")":
            return Instruction.L_INSTRUCTION
        else:
            return Instruction.C_INSTRUCTION

    def symbol(self):
        if self.instruction_type() == Instruction.A_INSTRUCTION:
            return self.current_instruction[1:]
        elif self.instruction_type() == Instruction.L_INSTRUCTION:
            return self.current_instruction[1:-1]
        else:
            raise Exception(
                "current_instruction must be of type A_INSTRUCTION or L_INSTRUCTION"
            )

    def dest(self):
        return True

    def comp(self):
        return True

    def jump(self):
        return True


class Instruction(Enum):
    A_INSTRUCTION = 1
    C_INSTRUCTION = 2
    L_INSTRUCTION = 3

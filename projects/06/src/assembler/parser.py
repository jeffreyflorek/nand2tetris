from collections import deque


class Parser:
    current_instruction = -1

    def __init__(self, in_filename):
        self.instructions = []
        with open(in_filename) as f:
            for line in f:
                instruction = line.strip()
                if not instruction or instruction.startswith("//"):
                    continue
                if "//" in instruction:
                    instruction = instruction[: instruction.index("//")].strip()
                self.instructions.append(instruction)

    def has_more_lines(self):
        return self.current_instruction < (len(self.instructions) - 1)

    def advance(self):
        if self.has_more_lines():
            self.current_instruction += 1
        else:
            raise Exception("advance called with no remaining instruction")

    def reset(self):
        self.current_instruction = -1

    def instruction_type(self):
        if not self.instructions[self.current_instruction]:
            raise Exception("current_instruction must not be empty")
        elif self.instructions[self.current_instruction].startswith("@"):
            return "A_INSTRUCTION"
        elif self.instructions[self.current_instruction].startswith(
            "("
        ) and self.instructions[self.current_instruction].endswith(")"):
            return "L_INSTRUCTION"
        elif (
            ";" in self.instructions[self.current_instruction]
            or "=" in self.instructions[self.current_instruction]
        ):
            return "C_INSTRUCTION"
        else:
            return None

    def symbol(self):
        if self.instruction_type() == "A_INSTRUCTION":
            return self.instructions[self.current_instruction][1:]
        elif self.instruction_type() == "L_INSTRUCTION":
            return self.instructions[self.current_instruction][1:-1]
        else:
            raise Exception(
                "current_instruction must be of type A_INSTRUCTION or L_INSTRUCTION"
            )

    def dest(self):
        if (
            self.instruction_type() == "C_INSTRUCTION"
            and "=" in self.instructions[self.current_instruction]
        ):
            return self.instructions[self.current_instruction].split("=")[0]
        else:
            return None

    def comp(self):
        if self.instruction_type() == "C_INSTRUCTION":
            if "=" in self.instructions[self.current_instruction]:
                return (
                    self.instructions[self.current_instruction]
                    .split("=")[1]
                    .split(";")[0]
                )
            else:
                return self.instructions[self.current_instruction].split(";")[0]
        else:
            raise Exception("current_instruction must be of type C_INSTRUCTION")

    def jump(self):
        if (
            self.instruction_type() == "C_INSTRUCTION"
            and ";" in self.instructions[self.current_instruction]
        ):
            return self.instructions[self.current_instruction].split(";")[1]
        else:
            return None

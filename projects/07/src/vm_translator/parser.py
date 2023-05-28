class Parser:
    def __init__(self, file_path):
        self._commands = []
        with open(file_path) as f:
            for line in f:
                command = line.strip()
                if not command or command.startswith("//"):
                    continue
                if "//" in command:
                    command = command[: command.index("//")].strip()
                self._commands.append(Command(command))

    def __iter__(self):
        yield from self._commands


class Command:
    def __init__(self, command):
        self._command = command
        arithmetic_logic_commands = (
            "add",
            "sub",
            "neg",
            "eq",
            "gt",
            "lt",
            "and",
            "or",
            "not",
        )
        push_pop_commands = ("push", "pop")
        label_commands = ("label", "goto", "if-goto")
        function_commands = ("function", "call")

        match command.split():
            case [command] if command in arithmetic_logic_commands:
                self._type = "C_ARITHMETIC"
                self._arg1 = command
            case [command, segment, index] if command in push_pop_commands:
                self._type = "C_" + command.upper()
                self._arg1 = segment
                self._arg2 = int(index)
            case [command, label] if command in label_commands:
                self._type = "C_" + command.split("-")[0].upper()
                self._arg1 = label
            case [command, name, args] if command in function_commands:
                self._type = "C_" + command.upper()
                self._arg1 = name
                self._arg2 = int(args)
            case ["return"]:
                self._type = "C_RETURN"
            case _:
                raise ValueError("Unrecognized command: " + command)

    @property
    def type(self):
        return self._type

    @property
    def arg1(self):
        if self._type != "C_RETURN":
            return self._arg1
        else:
            raise TypeError("arg1 cannot be called on command type C_RETURN")

    @property
    def arg2(self):
        if self._type in ("C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"):
            return self._arg2
        else:
            raise TypeError("arg2 cannot be called on command type " + self._type)

from .parser import Parser
from .code_writer import CodeWriter


class VMTranslator:
    def __init__(self, input, output, bootstrap=True, debug_comments=False):
        self._out_file = output
        self._bootstrap = bootstrap
        self._debug = debug_comments
        self._in_files = input

    def translate(self):
        with CodeWriter(self._out_file, bootstrap=self._bootstrap) as writer:
            for file in self._in_files:
                parser = Parser(file)
                writer.file_name = file.stem
                print(f"Translating {file.stem}...")
                for command in parser:
                    if self._debug:
                        writer._file.write(f"// {command._command}\n")
                    if command.type == "C_ARITHMETIC":
                        writer.write_arithmetic(command.arg1)
                    elif command.type in ("C_PUSH", "C_POP"):
                        writer.write_pushpop(command.type, command.arg1, command.arg2)
                    elif command.type == "C_LABEL":
                        writer.write_label(command.arg1)
                    elif command.type == "C_GOTO":
                        writer.write_goto(command.arg1)
                    elif command.type == "C_IF":
                        writer.write_if(command.arg1)
                    elif command.type == "C_FUNCTION":
                        writer.write_function(command.arg1, command.arg2)
                    elif command.type == "C_CALL":
                        writer.write_call(command.arg1, command.arg2)
                    elif command.type == "C_RETURN":
                        writer.write_return()
                    else:
                        raise ValueError(f"{command._command} is not a valid command")

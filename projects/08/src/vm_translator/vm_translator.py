from .parser import Parser
from .code_writer import CodeWriter
import pathlib


class VMTranslator:
    def __init__(self, file_path, bootstrap=True):
        self._parser = Parser(file_path)
        self._out_file = pathlib.Path(file_path).with_suffix(".asm")
        self._bootstrap = bootstrap

    def translate(self):
        with CodeWriter(self._out_file, bootstrap=self._bootstrap) as writer:
            for command in self._parser:
                if command.type == "C_ARITHMETIC":
                    writer._file.write("// " + command._command + "\n")
                    writer.write_arithmetic(command.arg1)
                elif command.type in ("C_PUSH", "C_POP"):
                    writer._file.write("// " + command._command + "\n")
                    writer.write_pushpop(command.type, command.arg1, command.arg2)
                else:
                    raise NotImplementedError(
                        "command type " + command.type + " not implemented."
                    )

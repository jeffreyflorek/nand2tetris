class CodeWriter:
    def __init__(self, file_path, bootstrap=True):
        self._file_path = file_path
        self._file_name = file_path.stem
        self._bootstrap = bootstrap
        self._function_name = "none"

        self._return_count = 0
        self._label_id = 0
        self._segment_dict = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
        }

    def __enter__(self):
        self._file = open(self._file_path, mode="w")

        if self._bootstrap:
            self._file.write("@256\nD=A\n@SP\nM=D\n")
            self.write_call("Sys.init", "0")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            self._file.close()

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name

    def write_arithmetic(self, command):
        """Writes assembly code to perform arithmetic and logic commands."""

        match command:
            case "add" | "sub":
                self._write_add_sub(command)
            case "eq" | "gt" | "lt":
                self._write_comp(command)
            case "and" | "or":
                self._write_and_or(command)
            case "not" | "neg":
                self._write_not_neg(command)

    def write_pushpop(self, type, segment, index):
        """Writes assembly code to push segment[index] to the stack or pop from the
        stack to segment[index]"""

        if type == "C_PUSH":
            self._write_push(segment, index)
        else:
            self._write_pop(segment, index)

    def write_label(self, label):
        """Writes assembly code to define a label."""

        self._file.write(f"({self._function_name}${label})\n")

    def write_goto(self, label):
        """Writes assembly code to perform a GOTO command."""

        self._file.write(f"@{self._function_name}${label}\n0;JMP\n")

    def write_if(self, label):
        """Writes assembly code to perform an IF-GOTO command."""

        self._pop_d()
        self._file.write(f"@{self._function_name}${label}\nD;JNE\n")

    def write_function(self, function_name, variable_count):
        """Writes assembly code to define a function with a specified number of local
        variables"""

        self._function_name = function_name
        self._return_count = 0

        self._file.write(f"({self._function_name})\n")
        for _ in range(variable_count):
            self._file.write("@SP\nM=M+1\nA=M-1\nM=0\n")

    def write_call(self, function_name, argument_count):
        """Writes assembly code to call a function with a specified number of
        arguments."""

        # Push return address to stack
        return_address = f"{self._function_name}$ret{self._return_count}"
        self._load_addr_to_d(return_address, pointer=False)
        self._push_d()
        self._return_count += 1

        # Push LCL, ARG, THIS, and THAT to stack
        for pointer in self._segment_dict.values():
            self._load_addr_to_d(pointer)
            self._push_d()

        # Reposition ARG to SP - 5 - argument_count
        self._file.write(f"@5\nD=A\n@{argument_count}\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n")

        # Reposition LCL to SP
        self._file.write("@SP\nD=M\n@LCL\nM=D\n")

        # goto function_name
        self._file.write(f"@{function_name}\n0;JMP\n")

        # Inject return address label
        self._file.write(f"({return_address})\n")

    def write_return(self):
        """Writes assembly code to return from a function call."""

        # Store LCL in temporary variable
        self._file.write("@LCL\nD=M\n@R13\nM=D\n")

        # Store return address in a temporary variable
        self._file.write("@5\nD=A\n@R13\nA=M-D\nD=M\n@R14\nM=D\n")

        # Reposition return value for caller
        self._pop_d()
        self._file.write("@ARG\nA=M\nM=D\n")

        # Reposition SP for the caller
        self._file.write("@ARG\nD=M+1\n@SP\nM=D\n")

        # Restore THAT, THIS, ARG, and LCL for the caller
        for i, ptr in enumerate(reversed(self._segment_dict.values()), start=1):
            self._file.write(f"@{i}\nD=A\n@R13\nA=M-D\nD=M\n@{ptr}\nM=D\n")

        # goto return address
        self._file.write("@R14\nA=M\n0;JMP\n")

    def _pop_d(self):
        """Writes assembly code that pops a value off the stack and stores it in the D
        register."""

        self._file.write("@SP\nM=M-1\nA=M\nD=M\n")

    def _push_d(self):
        """Writes assembly code that pushes the value in the D register to the stack."""

        self._file.write("@SP\nM=M+1\nA=M-1\nM=D\n")

    def _write_add_sub(self, command):
        """Writes assembly code to pop two values from the stack, perform addition or
        subraction, and pop the result back to the stack."""

        self._pop_d()
        self._file.write("A=A-1\n")
        if command == "add":
            self._file.write("M=D+M\n")
        else:
            self._file.write("M=M-D\n")

    def _write_comp(self, command):
        """Writes assembly code to pop two values from the stack, compare them, and push
        -1 to the stack if the comparison is true or 0 if false."""

        self._pop_d()
        command = command.upper()
        self._file.write(f"A=A-1\nD=M-D\nM=-1\n@{command}{self._label_id}\n")
        self._file.write(f"D;J{command}\n@SP\nA=M-1\nM=0\n")
        self._file.write(f"({command}{self._label_id})\n")
        self._label_id += 1

    def _write_and_or(self, command):
        """Writes assembly code that pops two values from the stack, performs bitwise
        and/or, and pushes the result to the stack."""

        self._pop_d()
        self._file.write("A=A-1\n")
        if command == "and":
            self._file.write("M=D&M\n")
        else:
            self._file.write("M=D|M\n")

    def _write_not_neg(self, command):
        """Writes assembly code that performs bitwise not or negates the topmost value
        on the stack."""

        self._file.write("@SP\nA=M-1\n")
        if command == "not":
            self._file.write("M=!M\n")
        else:
            self._file.write("M=-M\n")

    def _write_push(self, segment, index=0):
        """Pushes the value stored in segment[index] to the stack."""

        load_address = False
        pointer = False
        match (segment, index):
            case (segment, _) if segment in self._segment_dict.keys():
                segment = self._segment_dict[segment]
                pointer = True
            case ("pointer", 0):
                segment = "THIS"
            case ("pointer", 1):
                segment = "THAT"
                index = 0
            case ("temp", _):
                segment = "5"
                load_address = True
                pointer = True
            case ("constant", val):
                segment = val
                index = 0
                load_address = True
            case ("static", _):
                segment = f"{self._file_name}.{str(index)}"
                index = 0

        self._load_to_d(segment, index, load_address, pointer)
        self._push_d()

    def _write_pop(self, segment, index):
        """Pops from the stack and stores the value in segment[index]."""

        pointer = False
        match (segment, index):
            case (segment, _) if segment in self._segment_dict.keys():
                self._load_addr_to_d(self._segment_dict[segment], index)
                segment = "R13"
                pointer = True
                self._load_d_to_addr(segment)
            case ("pointer", 0):
                segment = "THIS"
            case ("pointer", 1):
                segment = "THAT"
            case ("temp", _):
                segment = "R13"
                pointer = True
                self._load_addr_to_d("5", index, pointer=False)
                self._load_d_to_addr(segment)
            case ("static", _):
                segment = f"{self._file_name}.{str(index)}"

        self._pop_d()
        self._load_d_to_addr(segment, pointer)

    def _load_addr_to_d(self, address, offset=0, pointer=True):
        """Writes assembly code that loads a memory address to the D regsiter."""

        if offset and pointer:
            self._file.write(f"@{address}\nD=M\n@{offset}\nD=D+A\n")
        elif offset and not pointer:
            self._file.write(f"@{address}\nD=A\n@{offset}\nD=D+A\n")
        elif pointer and not offset:
            self._file.write(f"@{address}\nD=M\n")
        else:
            self._file.write(f"@{address}\nD=A\n")

    def _load_d_to_addr(self, address, pointer=False):
        """Writes assembly code to store value in the D register to a memory address.

        If pointer=True, then the value stored at the address given as an argument is
        used as the memory address in which to store the value in the D register.
        """

        if pointer:
            self._file.write(f"@{address}\nA=M\nM=D\n")
        else:
            self._file.write(f"@{address}\nM=D\n")

    def _load_to_d(self, address, offset=0, load_address=False, pointer=True):
        """Writes assembly code that loads value at memory address into the D
        regsiter."""

        if pointer and offset and not load_address:
            self._file.write(f"@{address}\nD=M\n@{offset}\nA=D+A\nD=M\n")
        elif pointer and offset and load_address:
            self._file.write(f"@{address}\nD=A\n@{offset}\nA=D+A\nD=M\n")
        elif load_address and not offset:
            self._file.write(f"@{address}\nD=A\n")
        elif pointer:
            self._file.write(f"@{address}\nA=M\nD=M\n")
        else:
            self._file.write(f"@{address}\nD=M\n")

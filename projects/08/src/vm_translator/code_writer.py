class CodeWriter:
    def __init__(self, file_path, bootstrap=True):
        self._file_path = file_path
        self._file_name = file_path.stem
        self._bootstrap = bootstrap
        self._function_name = "none"

        self._label_id = 0
        self._segment_dict = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
        }

    def __enter__(self):
        self._file = open(self._file_path, mode="w")
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
        if type == "C_PUSH":
            self._write_push(segment, index)
        else:
            self._write_pop(segment, index)

    def write_label(self, label):
        self._file.write(f"({self._file_name}.{self._function_name}${label})\n")

    def write_goto(self, label):
        self._file.write(f"@{self._file_name}.{self._function_name}${label}\n0;JMP\n")

    def write_if(self, label):
        self._pop_d()
        self._file.write(f"@{self._file_name}.{self._function_name}${label}\nD;JNE\n")

    def write_function(self, function_name, argument_count):
        raise NotImplementedError
        # self._function_name = function_name
        # self._file.write(f"({self._file_name}.{self._function_name})")
        # for _ in range(argument_count):
        #     self._file.write("@SP\nM=M+1\nA=M-1\nM=0\n")

    def write_call(self, function_name, argument_count):
        raise NotImplementedError

    def write_return(self):
        raise NotImplementedError

    def _pop_d(self):
        self._file.write("@SP\nM=M-1\nA=M\nD=M\n")

    def _push_d(self):
        self._file.write("@SP\nM=M+1\nA=M-1\nM=D\n")

    def _write_add_sub(self, command):
        self._pop_d()
        self._file.write("A=A-1\n")
        if command == "add":
            self._file.write("M=D+M\n")
        else:
            self._file.write("M=M-D\n")

    def _write_comp(self, command):
        self._pop_d()
        command = command.upper()
        self._file.write(f"A=A-1\nD=M-D\nM=-1\n@{command}{self._label_id}\n")
        self._file.write(f"D;J{command}\n@SP\nA=M-1\nM=0\n")
        self._file.write(f"({command}{self._label_id})\n")
        self._label_id += 1

    def _write_and_or(self, command):
        self._pop_d()
        self._file.write("A=A-1\n")
        if command == "and":
            self._file.write("M=D&M\n")
        else:
            self._file.write("M=D|M\n")

    def _write_not_neg(self, command):
        self._file.write("@SP\nA=M-1\n")
        if command == "not":
            self._file.write("M=!M\n")
        else:
            self._file.write("M=-M\n")

    def _write_push(self, segment, index=0):
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
        if offset and pointer:
            self._file.write(f"@{address}\nD=M\n@{offset}\nD=D+A\n")
        elif offset and not pointer:
            self._file.write(f"@{address}\nD=A\n@{offset}\nD=D+A\n")
        elif pointer and not offset:
            self._file.write(f"@{address}\nD=M\n")
        else:
            self._file.write(f"@{address}\nD=A\n")

    def _load_d_to_addr(self, address, pointer=False):
        if pointer:
            self._file.write(f"@{address}\nA=M\nM=D\n")
        else:
            self._file.write(f"@{address}\nM=D\n")

    def _load_to_d(self, address, offset=0, load_address=False, pointer=True):
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

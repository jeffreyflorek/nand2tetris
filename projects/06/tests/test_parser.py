from assembler.parser import Parser, Instruction


def test_advance():
    with Parser("./tests/parser/advance.asm") as advance:
        assert advance.current_instruction == ""
        advance.advance()
        assert advance.current_instruction == "@10"
        advance.advance()
        assert advance.current_instruction == "@20"


def test_has_more_lines():
    with Parser("./tests/parser/empty.asm") as empty:
        assert empty.has_more_lines() == False
    with Parser("./tests/parser/one_line.asm") as one_line:
        assert one_line.has_more_lines() == True
        one_line.in_file.readline()
        assert one_line.has_more_lines() == False


def test_instruction_type():
    with Parser("./tests/parser/empty.asm") as empty:
        empty.current_instruction = "@10"
        assert empty.instruction_type() == Instruction.A_INSTRUCTION
        empty.current_instruction = "0;jmp"
        assert empty.instruction_type() == Instruction.C_INSTRUCTION
        empty.current_instruction = "(LABEL)"
        assert empty.instruction_type() == Instruction.L_INSTRUCTION


def test_symbol():
    with Parser("./tests/parser/empty.asm") as empty:
        empty.current_instruction = "(LABEL)"
        assert empty.symbol() == "LABEL"
        empty.current_instruction = "@LABEL"
        assert empty.symbol() == "LABEL"
        empty.current_instruction = "@10"
        assert empty.symbol() == "10"


def test_dest():
    with Parser("./tests/parser/empty.asm") as empty:
        empty.current_instruction = "0;jmp"
        assert empty.dest() == "null"
        empty.current_instruction = "M=1"
        assert empty.dest() == "M"
        empty.current_instruction = "D=1"
        assert empty.dest() == "D"
        empty.current_instruction = "DM=1"
        assert empty.dest() == "DM"
        empty.current_instruction = "A=1"
        assert empty.dest() == "A"
        empty.current_instruction = "AM=1"
        assert empty.dest() == "AM"
        empty.current_instruction = "AD=1"
        assert empty.dest() == "AD"
        empty.current_instruction = "ADM=1"
        assert empty.dest() == "ADM"


def test_comp():
    with Parser("./tests/parser/empty.asm") as empty:
        empty.current_instruction = "0;jmp"
        assert empty.comp() == "0"
        empty.current_instruction = "M=1"
        assert empty.comp() == "	"
        empty.current_instruction = "D=-1"
        assert empty.comp() == "-1"
        empty.current_instruction = "M=D"
        assert empty.comp() == "D"
        empty.current_instruction = "D=A"
        assert empty.comp() == "A"
        empty.current_instruction = "D=M"
        assert empty.comp() == "M"
        empty.current_instruction = "M=!D"
        assert empty.comp() == "!D"
        empty.current_instruction = "M=!A"
        assert empty.comp() == "!A"
        empty.current_instruction = "D=!M"
        assert empty.comp() == "!M"
        empty.current_instruction = "M=-D"
        assert empty.comp() == "-D"
        empty.current_instruction = "M=-A"
        assert empty.comp() == "-A"
        empty.current_instruction = "D=-M"
        assert empty.comp() == "-M"
        empty.current_instruction = "M=D+1"
        assert empty.comp() == "D+1"
        empty.current_instruction = "D=A+1"
        assert empty.comp() == "A+1"
        empty.current_instruction = "A=M+1"
        assert empty.comp() == "M+1"
        empty.current_instruction = "M=D-1"
        assert empty.comp() == "D-1"
        empty.current_instruction = "D=A-1"
        assert empty.comp() == "A-1"
        empty.current_instruction = "A=M-1"
        assert empty.comp() == "M-1"
        empty.current_instruction = "D=D+A"
        assert empty.comp() == "D+A"
        empty.current_instruction = "D=D+M"
        assert empty.comp() == "D+M"
        empty.current_instruction = "D=D-A"
        assert empty.comp() == "D-A"
        empty.current_instruction = "D=D-M"
        assert empty.comp() == "D-M"
        empty.current_instruction = "D=A-D"
        assert empty.comp() == "A-D"
        empty.current_instruction = "D=M-D"
        assert empty.comp() == "M-D"
        empty.current_instruction = "D=D&A"
        assert empty.comp() == "D&A"
        empty.current_instruction = "D=D&M"
        assert empty.comp() == "D&M"
        empty.current_instruction = "D=D|A"
        assert empty.comp() == "D|A"
        empty.current_instruction = "D=D|M"
        assert empty.comp() == "D|M"


def test_jump():
    with Parser("./tests/parser/empty.asm") as empty:
        empty.current_instruction = "M=1"
        assert empty.dest() == "null"
        empty.current_instruction = "0;JGT"
        assert empty.dest() == "JGT"
        empty.current_instruction = "0;JEQ"
        assert empty.dest() == "JEQ"
        empty.current_instruction = "0;JGE"
        assert empty.dest() == "JGE"
        empty.current_instruction = "0;JLT"
        assert empty.dest() == "JLT"
        empty.current_instruction = "0;JNE"
        assert empty.dest() == "JNE"
        empty.current_instruction = "0;JLE"
        assert empty.dest() == "JLE"
        empty.current_instruction = "0;JMP"
        assert empty.dest() == "JMP"

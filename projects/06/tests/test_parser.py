from assembler.parser import Parser
import pytest


def test_advance():
    advance = Parser("./tests/parser/advance.asm")
    assert advance.current_instruction == -1
    advance.advance()
    assert advance.current_instruction == 0
    assert advance.instructions[advance.current_instruction] == "@10"
    advance.advance()
    assert advance.current_instruction == 1
    assert advance.instructions[advance.current_instruction] == "@20"


def test_has_no_more_lines():
    empty = Parser("./tests/parser/empty.asm")
    assert empty.has_more_lines() == False


def test_has_one_more_line():
    one_line = Parser("./tests/parser/one_line.asm")
    assert one_line.has_more_lines() == True
    one_line.advance()
    assert one_line.has_more_lines() == False


@pytest.mark.parametrize(
    "instruction, expected_type",
    [
        ("@10", "A_INSTRUCTION"),
        ("0;JMP", "C_INSTRUCTION"),
        ("(LABEL)", "L_INSTRUCTION"),
    ],
)
def test_instruction_type(instruction, expected_type):
    empty = Parser("./tests/parser/empty.asm")
    empty.current_instruction = 0
    empty.instructions.append(instruction)
    assert empty.instruction_type() == expected_type


@pytest.mark.parametrize(
    "instruction, expected_label",
    [
        ("(LABEL)", "LABEL"),
        ("@LABEL", "LABEL"),
        ("@10", "10"),
    ],
)
def test_symbol(instruction, expected_label):
    empty = Parser("./tests/parser/empty.asm")
    empty.current_instruction = 0
    empty.instructions.append(instruction)
    assert empty.symbol() == expected_label


@pytest.mark.parametrize(
    "instruction, expected_dest",
    [
        ("0;jmp", None),
        ("M=1", "M"),
        ("D=1", "D"),
        ("DM=1", "DM"),
        ("A=1", "A"),
        ("AM=1", "AM"),
        ("AD=1", "AD"),
        ("ADM=1", "ADM"),
    ],
)
def test_dest(instruction, expected_dest):
    empty = Parser("./tests/parser/empty.asm")
    empty.current_instruction = 0
    empty.instructions.append(instruction)
    assert empty.dest() == expected_dest


@pytest.mark.parametrize(
    "instruction, expected_comp",
    [
        ("0;jmp", "0"),
        ("M=1", "1"),
        ("D=-1", "-1"),
        ("M=D", "D"),
        ("D=A", "A"),
        ("D=M", "M"),
        ("M=!D", "!D"),
        ("M=!A", "!A"),
        ("D=!M", "!M"),
        ("M=-D", "-D"),
        ("M=-A", "-A"),
        ("D=-M", "-M"),
        ("M=D+1", "D+1"),
        ("D=A+1", "A+1"),
        ("A=M+1", "M+1"),
        ("M=D-1", "D-1"),
        ("D=A-1", "A-1"),
        ("A=M-1", "M-1"),
        ("D=D+A", "D+A"),
        ("D=D+M", "D+M"),
        ("D=D-A", "D-A"),
        ("D=D-M", "D-M"),
        ("D=A-D", "A-D"),
        ("D=M-D", "M-D"),
        ("D=D&A", "D&A"),
        ("D=D&M", "D&M"),
        ("D=D|A", "D|A"),
        ("D=D|M", "D|M"),
    ],
)
def test_comp(instruction, expected_comp):
    empty = Parser("./tests/parser/empty.asm")
    empty.current_instruction = 0
    empty.instructions.append(instruction)
    assert empty.comp() == expected_comp


@pytest.mark.parametrize(
    "instruction, expected_jump",
    [
        ("M=1", None),
        ("0;JGT", "JGT"),
        ("0;JEQ", "JEQ"),
        ("0;JGE", "JGE"),
        ("0;JLT", "JLT"),
        ("0;JNE", "JNE"),
        ("0;JLE", "JLE"),
        ("0;JMP", "JMP"),
    ],
)
def test_jump(instruction, expected_jump):
    empty = Parser("./tests/parser/empty.asm")
    empty.current_instruction = 0
    empty.instructions.append(instruction)
    assert empty.jump() == expected_jump

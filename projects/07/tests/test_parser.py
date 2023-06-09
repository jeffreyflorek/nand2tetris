from vm_translator.parser import Parser, Command
import pytest


@pytest.mark.parametrize(
    "command, expected_type",
    [
        ("add", "C_ARITHMETIC"),
        ("sub", "C_ARITHMETIC"),
        ("neg", "C_ARITHMETIC"),
        ("eq", "C_ARITHMETIC"),
        ("gt", "C_ARITHMETIC"),
        ("lt", "C_ARITHMETIC"),
        ("and", "C_ARITHMETIC"),
        ("or", "C_ARITHMETIC"),
        ("not", "C_ARITHMETIC"),
        ("push static 3", "C_PUSH"),
        ("pop local 4", "C_POP"),
        ("label WHILE_LOOP", "C_LABEL"),
        ("goto WHILE_LOOP", "C_GOTO"),
        ("if-goto WHILE_END", "C_IF"),
        ("function main 0", "C_FUNCTION"),
        ("function factorial 1", "C_FUNCTION"),
        ("function max 2", "C_FUNCTION"),
        ("return", "C_RETURN"),
        ("call main 0", "C_CALL"),
        ("call factorial 1", "C_CALL"),
    ],
)
def test_command_type(command, expected_type):
    empty = Parser("./tests/parser/Empty.vm")
    empty._commands.append(Command(command))
    for command in empty:
        assert command.type == expected_type


@pytest.mark.parametrize(
    "command, expected_arg1",
    [
        ("add", "add"),
        ("sub", "sub"),
        ("neg", "neg"),
        ("eq", "eq"),
        ("gt", "gt"),
        ("lt", "lt"),
        ("and", "and"),
        ("or", "or"),
        ("not", "not"),
        ("pop local 2", "local"),
        ("push static 8", "static"),
        ("label WHILE_LOOP", "WHILE_LOOP"),
        ("goto WHILE_LOOP", "WHILE_LOOP"),
        ("if-goto WHILE_END", "WHILE_END"),
        ("function main 0", "main"),
        ("function factorial 1", "factorial"),
        ("function max 2", "max"),
        ("call main 0", "main"),
        ("call factorial 1", "factorial"),
    ],
)
def test_arg1(command, expected_arg1):
    empty = Parser("./tests/parser/Empty.vm")
    empty._commands.append(Command(command))
    for command in empty:
        assert command.arg1 == expected_arg1


@pytest.mark.parametrize(
    "command, expected_arg2",
    [
        ("pop local 2", 2),
        ("push static 8", 8),
        ("function main 0", 0),
        ("function factorial 1", 1),
        ("function max 2", 2),
        ("call main 0", 0),
        ("call factorial 1", 1),
    ],
)
def test_arg2(command, expected_arg2):
    empty = Parser("./tests/parser/Empty.vm")
    empty._commands.append(Command(command))
    for command in empty:
        assert command.arg2 == expected_arg2

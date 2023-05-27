from vm_translator.code_writer import CodeWriter
import pytest
import filecmp


@pytest.mark.parametrize(
    "command",
    [
        ("add"),
        ("sub"),
        ("neg"),
        ("eq"),
        ("gt"),
        ("lt"),
        ("and"),
        ("or"),
        ("not"),
    ],
)
def test_write_arithmetic(command):
    with CodeWriter("./tests/code_writer/" + command + ".hack") as out_file:
        out_file.write_arithmetic(command)
    assert filecmp.cmp(
        "./tests/code_writer/" + command + ".hack",
        "./tests/code_writer/" + command + ".cmp",
    )


@pytest.mark.parametrize(
    "command, segment, index",
    [
        ("C_PUSH", "argument", 1),
        ("C_PUSH", "local", 2),
        ("C_PUSH", "static", 3),
        ("C_PUSH", "constant", 4),
        ("C_PUSH", "this", 5),
        ("C_PUSH", "that", 6),
        ("C_PUSH", "pointer", 0),
        ("C_PUSH", "pointer", 1),
        ("C_PUSH", "temp", 7),
        ("C_POP", "argument", 2),
        ("C_POP", "local", 3),
        ("C_POP", "static", 4),
        ("C_POP", "this", 5),
        ("C_POP", "that", 6),
        ("C_POP", "pointer", 0),
        ("C_POP", "pointer", 1),
        ("C_POP", "temp", 1),
    ],
)
def test_write_pushpop(command, segment, index):
    with CodeWriter(
        "./tests/code_writer/" + command + segment + str(index) + ".hack"
    ) as out_file:
        out_file.write_pushpop(command, segment, index)
    assert filecmp.cmp(
        "./tests/code_writer/" + command + segment + str(index) + ".hack",
        "./tests/code_writer/" + command + segment + str(index) + ".cmp",
    )

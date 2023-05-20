import pytest
import filecmp
import subprocess
from assembler.assembler import Assembler


@pytest.mark.parametrize(
    "file",
    [
        "./tests/add/Add",
        "./tests/max/MaxL",
        "./tests/rect/RectL",
        "./tests/pong/PongL",
    ],
)
def test_assembler_no_symbols(file):
    my_assembler = Assembler(file + ".asm")
    machine_code = my_assembler.assemble()
    with open(file + "_compare.hack") as compare_file:
        line_number = 0
        for line in compare_file:
            assert machine_code[line_number] == line.strip()
            line_number += 1


@pytest.mark.parametrize(
    "file",
    [
        "./tests/add/Add",
        "./tests/max/MaxL",
        "./tests/rect/RectL",
        "./tests/pong/PongL",
    ],
)
def test_assembler_command_no_symbols(file):
    subprocess.run("python -m assembler ../" + file + ".asm", cwd="./src", shell=True)
    assert filecmp.cmp(file + "_compare.hack", file + ".hack") == True

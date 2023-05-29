import pytest
import filecmp
import subprocess
from vm_translator.vm_translator import VMTranslator


@pytest.mark.parametrize(
    "file",
    [
        "./tests/StackArithmetic/SimpleAdd/SimpleAdd",
        "./tests/StackArithmetic/StackTest/StackTest",
        "./tests/MemoryAccess/BasicTest/BasicTest",
        "./tests/MemoryAccess/PointerTest/PointerTest",
        "./tests/MemoryAccess/StaticTest/StaticTest",
    ],
)
def test_translator(file):
    translator = VMTranslator(file + ".vm")
    translator.translate()
    test = subprocess.run(
        "../../tools/CPUEmulator.sh " + file + ".tst", shell=True, capture_output=True
    )
    if test.returncode:
        pytest.fail(test.stderr.decode("utf-8").strip())

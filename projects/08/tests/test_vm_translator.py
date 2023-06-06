#!/usr/bin/env python3

import pytest
import subprocess


@pytest.mark.parametrize(
    "file",
    [
        "../tests/ProgramFlow/BasicLoop/BasicLoop",
        "../tests/ProgramFlow/FibonacciSeries/FibonacciSeries",
    ],
)
def test_translate_file(file):
    translator = subprocess.run(
        "python -m vm_translator " + file + ".vm",
        cwd="./src",
        shell=True,
        capture_output=True,
    )
    if translator.returncode:
        pytest.fail(translator.stderr.decode("utf-8").strip())

    test = subprocess.run(
        "../../../tools/CPUEmulator.sh " + file + ".tst",
        cwd="./src",
        shell=True,
        capture_output=True,
    )
    if test.returncode:
        pytest.fail(test.stderr.decode("utf-8").strip())


@pytest.mark.parametrize(
    "folder",
    [
        "../tests/ProgramFlow/BasicLoop",
        "../tests/ProgramFlow/FibonacciSeries",
        "../tests/FunctionCalls/FibonnacciElement",
        "../tests/FunctionCalls/NestedCall",
        "../tests/FunctionCalls/SimpleFunction",
        "../tests/FunctionCalls/StaticsTest",
    ],
)
def test_translate_folder(folder):
    translator = subprocess.run(
        "python -m vm_translator " + folder,
        cwd="./src",
        shell=True,
        capture_output=True,
    )
    if translator.returncode:
        pytest.fail(translator.stderr.decode("utf-8").strip())

    test = subprocess.run(
        "../../../tools/CPUEmulator.sh " + folder + folder.split("/")[-1] + ".tst",
        cwd="./src",
        shell=True,
        capture_output=True,
    )
    if test.returncode:
        pytest.fail(test.stderr.decode("utf-8").strip())

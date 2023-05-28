#!/usr/bin/env python3

import argparse
from .vm_translator import VMTranslator

parser = argparse.ArgumentParser(
    prog="hack_vm_translator",
    description="Translates Hack VM commands into assembly language.",
)

parser.add_argument("-o", "--out", help="output file, defaults to Filename.asm")

required = parser.add_argument_group("required")
required.add_argument("file", help="file to be assembled, in the form of Filename.vm")

args = parser.parse_args()

try:
    vm_translator = VMTranslator(args.file)
except FileNotFoundError:
    raise SystemExit("No such file: '" + args.file + "'")

print("Translating " + args.file + "...")
print("Not implemented!")
print("Success!")

if args.out:
    outfile = args.out
else:
    outfile = ".".join(args.file.split(".")[0:-1]) + ".hack"

print("Writing " + outfile + "...")
print("Not implemented!")

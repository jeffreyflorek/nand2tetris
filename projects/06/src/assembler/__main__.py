#!/usr/bin/env python3

import argparse
from .assembler import Assembler

parser = argparse.ArgumentParser(
    prog="hack_assembler",
    description="Assembles Hack assembly language into machine code.",
)

parser.add_argument("-o", "--out", help="output file, defaults to filename.hack")

required = parser.add_argument_group("required")
required.add_argument("file", help="file to be assembled, in the form of filename.asm")

args = parser.parse_args()

try:
    assembler = Assembler(args.file)
except FileNotFoundError:
    raise SystemExit("No such file: '" + args.file + "'")

print("Assembling " + args.file + "...")
machine_code = assembler.assemble()
print("Success!")

if args.out:
    outfile = args.out
else:
    outfile = ".".join(args.file.split(".")[0:-1]) + ".hack"

print("Writing " + outfile + "...")
with open(outfile, "w") as f:
    f.write("\n".join(machine_code) + "\n")

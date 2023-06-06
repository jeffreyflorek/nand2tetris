#!/usr/bin/env python3

import argparse
import pathlib
import re
from .vm_translator import VMTranslator

parser = argparse.ArgumentParser(
    prog="hack_vm_translator",
    description="Translates Hack VM commands into assembly language.",
)

# parser.add_argument("-o", "--out", help="output file, defaults to Filename.asm")

# required = parser.add_argument_group("required")
parser.add_argument(
    "source",
    nargs="?",
    default=".",
    help="source to be assembled, either a folder or a .vm file",
)

args = parser.parse_args()

source = pathlib.Path(args.source)
if not source.exists():
    raise SystemExit('Source not found: "' + args.source + '"')

filename_format = re.compile(r"[A-Z][a-zA-Z]*.vm")

files = []
if source.is_dir():
    files = [
        f
        for f in source.iterdir()
        if filename_format.fullmatch(f.name) and not f.is_dir()
    ]
    if not files:
        raise SystemExit(
            'Folder "' + str(source) + '" must contain at least one .vm file'
        )
elif filename_format.fullmatch(source.name):
    files = source
else:
    raise SystemExit(
        "File name must start with a capital letter and have a .vm extension, e.g. Filename.vm"
    )

if isinstance(files, list):
    print("Translating files: " + ", ".join(file.name for file in files))
else:
    print("Translating file: " + files.name)

# try:
#     vm_translator = VMTranslator(args.file)
# except FileNotFoundError:
#     raise SystemExit("No such file: '" + args.file + "'")

# print("Translating " + args.file + "...")
# vm_translator.translate()
# print("Success!")
# if args.out:
#     outfile = args.out
# else:
#     outfile = ".".join(args.file.split(".")[0:-1]) + ".hack"

#!/usr/bin/env python3

import argparse
import pathlib
import re
from .vm_translator import VMTranslator

parser = argparse.ArgumentParser(
    prog="vm_translator",
    description="Translates Hack VM commands into assembly language.",
)

parser.add_argument(
    "-nb",
    "--no-bootstrap",
    action="store_false",
    help="don't write VM boostrap code to assembly file (for testing purposes only)",
)

parser.add_argument(
    "source",
    nargs="?",
    default=".",
    help="source to be assembled, either a folder or a .vm file, defaults to the current folder",
)

args = parser.parse_args()

source = pathlib.Path(args.source).absolute()
if not source.exists():
    raise SystemExit('Source not found: "' + args.source + '"')

filename_format = re.compile(r"[A-Z][a-zA-Z]*.vm")

if source.is_dir():
    if not [
        f
        for f in source.iterdir()
        if filename_format.fullmatch(f.name) and not f.is_dir()
    ]:
        raise SystemExit(
            'Folder "' + str(source) + '" must contain at least one .vm file'
        )
else:
    if not filename_format.fullmatch(source.name):
        raise SystemExit(
            "File name must start with a capital letter and have a .vm extension, e.g. Filename.vm"
        )

print("Loading " + source.name)
vm_translator = VMTranslator(source, bootstrap=parser.parse_args(["--no-bootstrap"]))

print("Translating " + source.name + "...")
vm_translator.translate()
print("Success!")

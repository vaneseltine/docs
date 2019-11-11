#!/usr/bin/env python3

import re
from pathlib import Path
import fileinput

SECTION_LINE = re.compile(r"^[=*#-]{3,}")


def gather_rsts(folder):
    return list(Path(folder).glob("**/*.rst"))


def handle_line(line, last_len):
    if not SECTION_LINE.match(line):
        return line
    if len(line) == last_len:
        return line
    new_line = line[0] * (last_len - 1) + "\n"
    return new_line


def plural(i):
    return "" if i == 1 else "s"


def main():
    rsts = gather_rsts(Path("./core"))
    print(f"{len(rsts)} input files.")
    changes = 0
    for rst in rsts:
        last_len = 0
        for line in fileinput.input(rst, inplace=True):
            output = handle_line(line, last_len)
            changes += line != output
            print(output, end="")
            last_len = len(line)
    print(f"{changes} line{plural(changes)} changed.")


if __name__ == "__main__":
    main()

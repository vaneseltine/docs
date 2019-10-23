#! /usr/bin/env python3
"""Invoke via `nox` or `python -m nox`"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import nox

nox.options.stop_on_first_error = True

IN_CI = os.getenv("CI", "").lower() == "true"


@nox.session(python=False)
def lint(session):
    session.run("doc8", ".")


@nox.session(python=False)
def build(session):
    # if IN_CI:
    # session.skip("Not building on CI")
    output_dir = Path("_build").resolve()
    # shutil.rmtree(output_dir, ignore_errors=True)  # eradicate previous build
    session.run(
        "python",
        "-m",
        "sphinx",
        ".",
        str(output_dir),
        "-q",  # only output problems
        "-a",  # don't reuse old output
        "-E",  # don't reuse previous environment
        "-n",  # nitpicky mode
        "-W",  # warnings are errors
        "--keep-going",  # gather all warnings before exit
    )
    print(f"Documentation at {output_dir / 'index.html'}")


@nox.session(python=False)
def autopush(session):
    if IN_CI:
        session.skip("Not in CI")
    if not nox.options.stop_on_first_error:
        session.skip("Error-free runs required")
    git_output = subprocess.check_output(["git", "status", "--porcelain"])
    if git_output:
        print(git_output.decode("ascii").rstrip())
        session.skip("Local repo is not clean")
    subprocess.check_output(["git", "push"])


if __name__ == "__main__":
    print(f"Invoke {__file__} by running Nox.")

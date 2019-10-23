#! /usr/bin/env python3
"""Invoke via `nox` or `python -m nox`"""

import os
import shutil
import subprocess
from pathlib import Path

import nox

nox.options.stop_on_first_error = True

IN_CI = os.getenv("CI", "").lower() == "true"
ERADICATE_PREVIOUS_BUILDS = False


@nox.session(python=False)
def lint(session):
    session.run("doc8", ".", "-q")


@nox.session(python=False)
def build(session):
    output_dir = Path("_build").resolve()
    if ERADICATE_PREVIOUS_BUILDS:
        shutil.rmtree(output_dir, ignore_errors=True)
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
        session.skip("Don't autopush from CI")
    if not nox.options.stop_on_first_error:
        session.skip("Don't autopush without requiring error-free run")
    git_output = subprocess.check_output(["git", "status", "--porcelain"])
    if git_output:
        print("Dirty repo:")
        print(git_output.decode("ascii").rstrip())
        session.skip("Local repo is not clean")
    subprocess.check_output(["git", "push"])


if __name__ == "__main__":
    print(f"Invoke {__file__} by running Nox.")

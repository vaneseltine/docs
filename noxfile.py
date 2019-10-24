#! /usr/bin/env python3
"""Invoke via `nox` or `python -m nox`"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import boto3
import nox
from zope.contenttype import guess_content_type

nox.options.stop_on_first_error = True

IN_CI = os.getenv("CI", "").lower() == "true"
IN_WINDOWS = sys.platform.startswith("win")
ERADICATE_PREVIOUS_BUILDS = True

COMPLETE_REUPLOAD = False

BUILD_DIR = Path("_build").resolve()
SITE = "misterdoubt.com"


@nox.session(python=False)
def lint(session):
    cmd = ["doc8", ".", "-q"]
    if IN_WINDOWS:
        cmd.append("--ignore=D002,D004")
    session.run(*cmd)


@nox.session(python=False)
def build(session):
    if ERADICATE_PREVIOUS_BUILDS:
        shutil.rmtree(BUILD_DIR, ignore_errors=True)
    session.run(
        "python",
        "-m",
        "sphinx",
        ".",
        str(BUILD_DIR),
        "-q",  # only output problems
        "-a",  # don't reuse old output
        "-E",  # don't reuse previous environment
        "-n",  # nitpicky mode
        # "-W",  # warnings are errors
        "--keep-going",  # gather all warnings before exit
    )
    print(f"Documentation at {BUILD_DIR / 'index.html'}")


@nox.session(python=False)
def bucket(session):
    # awsession = boto3.session.Session()
    # s3 = awsession.resource("s3")
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(SITE)
    GLOB = "**/*" if COMPLETE_REUPLOAD else "**/*.html"
    for path in BUILD_DIR.glob(GLOB):
        if not path.is_file():
            continue
        if "doctree" in str(path):
            continue
        key = str(path.relative_to(BUILD_DIR))
        content_type, encoding = guess_content_type(str(path), path.read_bytes())
        print(key, content_type, encoding)
        bucket.put_object(
            Key=key,
            Body=path.read_bytes(),
            ContentType=content_type,
            ContentEncoding=encoding or "",
        )
        # obj = bucket.Object(key)
        # if content_type := CONTENT_TYPES.get(path.suffix):
        #     obj.content_type = content_type
        # obj.set_contents_from_string(path.read_text(), policy='public-read')
        # bucket.put_object(Key=key, Body=path.read_text())
        # s3.meta.client.upload_file(str(path), SITE, str(key))


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

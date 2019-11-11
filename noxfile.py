#! /usr/bin/env python3
"""Invoke via `nox` or `python -m nox`"""

import fileinput
import logging
import re
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile

import boto3
import nox
from zope.contenttype import guess_content_type

for shhhhh in ["boto3", "urllib3", "botocore", "s3transfer"]:
    logging.getLogger(shhhhh).setLevel(logging.WARNING)

nox.options.stop_on_first_error = True

IN_WINDOWS = sys.platform.startswith("win")

COMPLETE_REUPLOAD = False
DEPLOYABLE = False

BUILD_DIR = Path("_build").resolve()
SITE = "misterdoubt.com"


@nox.session(python=False)
def format(session):
    def handle_line(line, last_len):
        if not re.match(r"^[=*#-]{3,}", line):
            return line
        if len(line) == last_len:
            return line
        new_line = line[0] * (last_len - 1) + "\n"
        return new_line

    rsts = list(Path("./core").glob("**/*.rst"))
    print(f"{len(rsts)} input files.")
    changes = 0
    for rst in rsts:
        last_len = 0
        original_text = rst.read_text()
        for line in fileinput.input(rst, inplace=True):
            output = handle_line(line, last_len)
            changes += line != output
            print(output, end="")
            last_len = len(line)
        new_text = rst.read_text()
        if len(original_text.splitlines()) != len(new_text.splitlines()):
            print("YIKES!", "%" * 60, original_text, "&" * 60, new_text, sep="\n\n")
            rst.write_text(original_text)
            raise RuntimeError("Line counts did not match")

    print(f"{changes} lines changed.")
    return 0


@nox.session(python=False)
def lint(session):
    cmd = ["doc8", ".", "-q"]
    if IN_WINDOWS:
        cmd.append("--ignore=D002,D004")
    session.run(*cmd)


@nox.session(python=False)
def build(session):
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
        "-W",  # warnings are errors
        "--keep-going",  # gather all warnings before exit
    )
    print(f"Documentation at {BUILD_DIR / 'index.html'}")


@nox.session(python=False)
def push(session):
    git_output = subprocess.check_output(["git", "status", "--porcelain"])
    if git_output:
        print("Dirty repo:")
        print(git_output.decode("ascii").rstrip())
        session.skip("Local repo is not clean")
    subprocess.check_output(["git", "push"])
    global DEPLOYABLE
    DEPLOYABLE = True


@nox.session(python=False)
def update_aws(session):
    if IN_WINDOWS:
        session.skip("Not deploying from Windows")
    if not DEPLOYABLE:
        session.skip("Not cleared to deploy")

    def path_to_key(path):
        return str(path.relative_to(BUILD_DIR))

    def key_to_path(s):
        return BUILD_DIR / s

    def need_to_upload(path):
        if not path.is_file():
            return False
        s = str(path)
        if "doctree" in s or "_sources" in s:
            return False
        if path.name in (".buildinfo"):
            return False
        return True

    def upload(bucket, *, path=None, key=None):
        key = key or path_to_key(path)
        path = path or key_to_path(key)
        content = path.read_bytes()
        content_type, encoding = guess_content_type(str(path), content)

        # print(f"Uploading {key} ({content_type}, {encoding})")
        bucket.put_object(
            Key=key,
            Body=content,
            ContentType=content_type,
            ContentEncoding=encoding or "",
        )

    # 1 generate a key for each file (from current repo)
    current_repo = {
        path_to_key(path): path
        for path in BUILD_DIR.glob("**/*")
        if need_to_upload(path)
    }
    repo_keys = set(current_repo)

    # 2 download the file attached to each key (from bucket)
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(SITE)  # pylint: disable=no-member
    site_objects = {obj.key: obj for obj in bucket.objects.all()}
    site_keys = set(site_objects)

    old_site_keys = site_keys - repo_keys
    print(f"{len(old_site_keys):>3} old site keys")
    for key in old_site_keys:
        print(f"Deleting {key}...")
        site_objects[key].delete()

    new_repo_keys = repo_keys - site_keys
    print(f"{len(new_repo_keys):>3} new repo keys")
    for key in new_repo_keys:
        print(f"Uploading {key}...")
        upload(bucket, key=key)

    shared_keys = repo_keys & site_keys
    print(f"{len(shared_keys):>3} shared keys")

    for key in sorted(shared_keys):
        with NamedTemporaryFile() as tmp:
            s3.meta.client.download_file(SITE, key, tmp.name)
            site_content = Path(tmp.name).read_bytes()
        repo_content = current_repo[key].read_bytes()
        path = key_to_path(key)
        if COMPLETE_REUPLOAD or repo_content != site_content:
            upload(bucket, path=path, key=key)


if __name__ == "__main__":
    print(f"Invoke {__file__} by running Nox.")

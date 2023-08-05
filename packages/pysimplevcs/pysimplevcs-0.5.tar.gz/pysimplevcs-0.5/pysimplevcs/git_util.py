############################################################
#
# pysimplevcs.git_util
# Copyright (C) 2017, Richard Cook
# Released under MIT License
# https://github.com/rcook/pysimplevcs
#
############################################################

from __future__ import print_function
from pyprelude.process import execute
from pyprelude.util import unpack_args

def _run_subcommand(subcommand, *args, **kwargs):
    command = ["git", subcommand] + map(str, unpack_args(*args))
    return execute(command, **kwargs).strip()

def git_init(*args, **kwargs):
    output = _run_subcommand("init", *args, **kwargs)
    if "Initialized empty Git repository" not in output:
        raise RuntimeError("git init failed with unexpected output: {}".format(output))

def git_clone(*args, **kwargs):
    output = _run_subcommand("clone", *args, **kwargs)

    lines = output.splitlines()
    if len(lines) == 0 or len(lines) == 1 and lines[0].startswith("Cloning into"):
        return

    raise RuntimeError("git clone failed with unexpected output: {}".format(output))

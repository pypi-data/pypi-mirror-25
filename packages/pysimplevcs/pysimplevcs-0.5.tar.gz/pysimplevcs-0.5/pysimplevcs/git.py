############################################################
#
# pysimplevcs.git
# Copyright (C) 2017, Richard Cook
# Released under MIT License
# https://github.com/rcook/pysimplevcs
#
############################################################

from __future__ import print_function
import os

from pyprelude.file_system import make_path
from pyprelude.platform import ON_WINDOWS
from pyprelude.process import execute, proxy_command
from pyprelude.util import unpack_args

_GIT_CAPS = None

def _get_git_caps():
    global _GIT_CAPS
    if _GIT_CAPS is None:
        _GIT_CAPS = _GitCaps()
    return _GIT_CAPS

def _get_config_path(prefix, terminator, p):
    if not p.startswith(prefix):
        return

    prefix_len = len(prefix)
    i = p.index(terminator, prefix_len)
    return p[prefix_len : i]

def _is_msys_git_executable(p):
    if not ON_WINDOWS:
        return False

    output = execute(p, "config", "--list", "--show-origin")
    for line in output.splitlines():
        path = _get_config_path("file:\"", "\"", line)
        if path is not None:
            return ":\\" not in path and ":/" not in path

        path = _get_config_path("file:", "\t", line)
        if path is not None:
            return ":\\" not in path and ":/" not in path

    raise RuntimeError("Cannot determine build type of Git executable")

class _GitCaps(object):
    def __init__(self):
        self._program_path = "git"
        self._is_msys_git_executable = _is_msys_git_executable(self._program_path)

    @property
    def program_path(self): return self._program_path

    def to_native_path(self, s):
        return execute("cygpath", "-w", s).strip() if self._is_msys_git_executable else s

class _Git(object):
    def __init__(self, caps, is_bare, repo_dir, git_dir, args):
        self._caps = caps
        self._is_bare = is_bare
        self._repo_dir = repo_dir
        self._git_dir = git_dir
        self._args = args

    @property
    def is_bare(self): return self._is_bare

    @property
    def repo_dir(self): return self._repo_dir

    @property
    def git_dir(self): return self._git_dir

    def with_args(self, *args):
        return _Git(
            self._is_bare,
            self._repo_dir,
            self._git_dir,
            self._args + unpack_args(*args))

    def to_native_path(self, s):
        return self._caps.to_native_path(s)

    def __getattr__(self, name):
        def _missing_method(*args, **kwargs):
            return proxy_command(
                name,
                self._repo_dir,
                lambda n, args: [self._caps.program_path] + self._args + [n] + args,
                *args,
                **kwargs)

        return _missing_method

class Git(_Git):
    def __init__(self, cwd=None, args=[]):
        if cwd is None:
            cwd = os.getcwd()

        cwd = os.path.abspath(cwd)

        caps = _get_git_caps()

        is_bare = execute(
            "git",
            "rev-parse",
            "--is-bare-repository",
            cwd=cwd).strip() == "true"

        if is_bare:
            repo_dir = cwd
            git_dir = repo_dir
        else:
            repo_dir = caps.to_native_path(execute("git", "rev-parse", "--show-toplevel", cwd=cwd).strip())
            git_dir = make_path(repo_dir, ".git")

        super(Git, self).__init__(caps, is_bare, repo_dir, git_dir, args)

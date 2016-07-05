#!/usr/bin/env python2
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

from __future__ import (unicode_literals, division, absolute_import,
                        print_function)
import os
import shutil

from .build_deps import init_env
from .constants import putenv, mkdtemp, PREFIX, CALIBRE_DIR, PYTHON
from .utils import run
from freeze import initialize_constants
from freeze.linux import main as freeze


def main(args):
    init_env()
    initialize_constants()
    build_dir, ext_dir = mkdtemp('build-'), mkdtemp('plugins-')
    putenv(
        CALIBRE_SETUP_EXTENSIONS_PATH=ext_dir,
        QMAKE=os.path.join(PREFIX, 'qt', 'bin', 'qmake'),
        SIP_BIN=os.path.join(PREFIX, 'bin', 'sip'),
        HOME=CALIBRE_DIR,
        SW=PREFIX
    )
    os.chdir(CALIBRE_DIR)
    ld = os.path.join(PREFIX, 'qt', 'lib')
    run('env', library_path=ld)
    cmd = [PYTHON, 'setup.py', 'build', '--build-dir=' + build_dir, '--output-dir=' + ext_dir]
    if args.only:
        cmd.append('--only=' + args.only)
    run(*cmd, library_path=ld)
    if not args.only:
        freeze(args, ext_dir)

    # After a successful run, remove the unneeded sw directory
    shutil.rmtree(PREFIX)
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Luis López <luis@cuarentaydos.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.


import argparse
import os
import shutil
import sys
from os import path


import txtflar


def _escape_filename(filename):
    return filename.replace("\\", "\\\\").replace("'", "\\'")


def main(argv=None):
    parser = argparse.ArgumentParser(prog='txtflar', add_help=True)
    parser.add_argument(
        '-n', '--dry-run',
        action='store_true',
        default=False,
        help="Don't rename files, just show whatever will be done"
        )
    parser.add_argument(
        '-f', '--force',
        action='store_true',
        default=False,
        help="Force rename even if destination filename exists"
        )
    parser.add_argument(
        'filenames',
        nargs='+')

    args = parser.parse_args(argv)
    for fn in args.filenames:
        if not os.path.exists(fn):
            msg = "# E: '{filename}' doesn't exists"
            msg = msg.format(filename=_escape_filename(fn))
            print(msg, file=sys.stderr)
            continue

        src_fn = path.realpath(fn)
        try:
            dst_fn = txtflar.get_language_aware_filename(src_fn)
        except OSError as e:
            msg = "# E: '{filename}' read error: {msg}"
            msg = msg.format(filename=_escape_filename(fn), msg=str(e))
            print(msg, file=sys.stderr)
            continue
        except txtflar.DetectError as e:
            msg = "# E: '{filename}' detect error: {msg}"
            msg = msg.format(filename=_escape_filename(fn), msg=str(e))
            print(msg, file=sys.stderr)
            continue

        if src_fn == dst_fn:
            msg = "# I: '{filename}' is already correct"
            msg = msg.format(filename=fn)
            print(msg, file=sys.stderr)
            continue

        if args.dry_run:
            msg = "mv '{src}' '{dst}'"
            msg = msg.format(
                src=_escape_filename(fn), dst=_escape_filename(dst_fn))
            print(msg)
            continue

        if path.exists(dst_fn):
            if not args.force:
                msg = ("# [E] Destination file '{filename}' already exists "
                       "and --force wasn't especified")
                msg = msg.format(filename=_escape_filename(dst_fn))
                print(msg, file=sys.stderr)
                continue

            try:
                os.unlink(dst_fn)
            except OSError as e:
                msg = ("# [E] Unable to remove previous destination file "
                       "'{filename}': {msg}")
                msg = msg.format(filename=_escape_filename(fn), msg=str(e))
                print(msg, file=sys.stderr)
                continue

        shutil.move(fn, dst_fn)


if __name__ == '__main__':
    main()

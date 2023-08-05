# -*- coding: utf-8 -*-

"""Console script for shebang."""
from __future__ import print_function

import argparse
import os
import re
import sys

from putshebang import __version__
from putshebang.shebangs import ShebangedFile, UnshebangedFile, ShebangNotFoundError, _decorate


def warn(msg):
    # type: (str) -> None
    """prints a warning to stderr"""

    print(_decorate("\n{WARN} {R}WARNING{W}: {GR}{msg}{W}", msg=msg),
          file=sys.stderr)


def error(err, exit_code=1):
    # type: (BaseException or str, int) -> None
    """prints an error to stderr and exits
    :param err: the exception that happened
    :param exit_code: the exit code to exit with
    """

    if isinstance(err, BaseException):
        fmt_str = "{Y}ERROR{Y}: {R}{error}{W}: {GR}{msg}"
    elif isinstance(err, str):
        fmt_str = "{Y}ERROR{W}: {GR}{msg}"
    else:
        raise TypeError()
    fmt_str = _decorate(fmt_str, error=type(err).__name__, msg=err)
    print(_decorate("\n{ERR} ") + fmt_str)
    sys.exit(exit_code)


def cleanup(shebanged_file):
    # type: (ShebangedFile) -> None
    if shebanged_file is not None and shebanged_file.file.created:
        os.remove(shebanged_file.file.name)


def main(args_=None):
    """The main entry for the whole thing."""

    parser = argparse.ArgumentParser(
        description="A small utility helps in adding the appropriate shebang to FILEs.",
        add_help=False,
        usage="%s [OPTIONS] [FILE ...]" % ("putshebang" if __name__ == '__main__' else "%(prog)s")
    )

    arguments = parser.add_argument_group("Arguments")
    arguments.add_argument("file", metavar="FILE", nargs=argparse.ZERO_OR_MORE,
                           # it's actually one or more, but the interface does't allow that
                           help="name of the file(s)")

    info = parser.add_argument_group("INFO")
    info.add_argument("-k", "--known", action="store_true", help="print known extensions")
    info.add_argument("-v", "--version", action="version", version="%(prog)s: {}".format(__version__))
    info.add_argument("-h", "--help", action="help", help="show this help message and exit")

    edit = parser.add_argument_group("EDITING")

    edit.add_argument("-x", "--executable", action="store_true",
                      help="make the file executable")
    edit.add_argument("-s", "--strict", action="store_true",
                      help="don't create the file if it doesn't exist")
    edit.add_argument("-o", "--overwrite", action="store_true",
                      help="overwrite the shebang if it's pointing to a wrong interpreter")
    edit.add_argument("-d", "--default", action="store_true",
                      help="use the default shebang")
    edit.add_argument("-F", "--no-symlinks", action="store_true",
                      help="don't get symlinks of paths that are already available")
    edit.add_argument("-l", "--lang", metavar="LANG",
                      help="forces the name of the language's interpreter to be LANG")
    edit.add_argument("-n", "--newline", metavar="N", type=int, default=1,
                      help="number of newlines to be put after the shebang; default is 1")

    args = parser.parse_args(args=args_)

    # return status
    rs = 0
    if args.known:
        ShebangedFile.print_known(args.no_symlinks)
        return rs

    if args.file is None:
        error(argparse.ArgumentError(args.file, "this argument is required"), 2)

    sf = None
    for f in args.file:
        try:
            sf = ShebangedFile(UnshebangedFile(f, args.strict, args.executable))
            (interpreters,
             paths) = ShebangedFile.get_interpreter_path(sf.file.name, args.lang, get_versions=True,
                                                         get_symlinks=not args.no_symlinks)

            all_paths = paths.get("all")
            all_inters = interpreters.get("all")
            if all_paths is None:
                if all_inters is None:
                    raise ShebangNotFoundError(
                        "The file name extension is not associated with any known interpreter name"
                    )
                else:
                    s = '(' + re.sub(", (.+)$", "or \1", str(all_inters)[1:-1]) + ')'
                    raise ShebangNotFoundError("Interpreter for %s not found in this machine's PATH" % s)

            if args.default or len(all_inters) == 1:
                path = paths["default"]
                if not path:
                    raise ShebangNotFoundError("Default interpreter not found on this machine's PATH")
            else:
                l = len(all_paths)  # trying to save some resources
                print(_decorate(
                    "{INFO} Found {G}{n}{GR} interpreters for file {C}{file!r}{GR}: ", n=l, file=f
                ))
                for n, s in zip(range(1, l + 1), all_paths):
                    print(_decorate("\t{Y}[{G}{n}{Y}]{GR}: {B}{path}", n=n, path=s))

                r = int(input(
                    _decorate(
                        "{GR}Choose one of the above paths {Y}[{G}1{Y}-{G}{n}{Y}]{W} (default is {G}1{W}){GR}: ", n=l))
                        or 1)
                path = all_paths[r - 1]

            sf.shebang = "#!{}\n".format(path)
        except Exception as e:
            cleanup(sf)
            warn(_decorate("file: {G}{file}{W}: {GR}{msg}", file=f, msg=e))
            rs = 1
            continue
        except KeyboardInterrupt:
            cleanup(sf)
            error(KeyboardInterrupt("Abort!"), 130)
        except BaseException as e:
            cleanup(sf)
            error(e, 2)

        code = sf.put_shebang(newline_count=args.newline, overwrite=args.overwrite)
        if code == 0:
            sf.file.save()
        elif code == 1:
            warn(_decorate("file: {G}{file}{W}: {GR}the correct shebang is already there.", file=f))
            rs = 0
        elif code == 2:
            warn(_decorate(
                "file: {G}{file}{W}: {GR}There's a shebang, but it's pointing to a wrong interpreter, "
                "use the option {G}--overwrite{GR} to overwrite it", file=f
            ))
            rs = 1
    return rs


if __name__ == "__main__":
    main()

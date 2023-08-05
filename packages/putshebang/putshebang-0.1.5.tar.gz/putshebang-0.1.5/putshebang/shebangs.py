# -*- coding: utf-8 -*-

"""Main module."""

from __future__ import print_function as _

import glob as _glob
import os as _os
import re as _re
import sys as _sys
import shutil as _shutil

from typing import List, Tuple, Dict


from putshebang._data import Data as _Data

# compatibility
if _sys.version_info.major == 2:
    input = raw_input


def which(cmd):
    # type: (str) -> List[str]
    """Like shutil.which, but uses globs, and less features."""

    paths = _os.environ.get("PATH", _os.defpath).split(":")
    l = []
    for path in paths:
        abs_path = _os.path.join(path, cmd)
        g = list(filter(lambda f: (not _os.path.isdir(f) and _os.access(f, _os.F_OK | _os.X_OK)), _glob.glob(abs_path)))
        if len(g) != 0:
            l.extend(g)
    return l


def _decorate(text, **otherkeys):
    text += "{W}"
    colors = dict(
        list(zip([
            'DR',  # Dark Red
            'R',  # Red
            'G',  # Green
            'Y',  # Yellow
            'B',  # Blue
            'M',  # Magenta
            'C',  # Cyan
            'GR',  # Grey
        ],
            list(map(lambda n: "\033[%dm" % n, range(30, 38)))
        ))
    )
    colors.update({"W": "\033[0m"})  # normal

    beginnings = {"ERR": "{R}[{Y}!{R}]{W}",
                  "WARN": "{R}[{Y}*{R}]{W}",
                  "INFO": "{G}[{Y}-{G}]{GR}",
                  }
    if _os.getenv('ANSI_COLORS_DISABLED') is not None:
        colors = {color: '' for color in colors}
    beginnings = {k: beginnings[k].format(**colors) for k in beginnings}

    return text.format(**beginnings, **colors, **otherkeys)


class ShebangNotFoundError(Exception):
    pass


class UnshebangedFile(object):
    """The file that requires the shebang.
    
    Generally, it should only be used when it's passed to the `ShebangedFile` constructor
    """

    def __init__(self, name, strict, make_executable):
        # type: (str, bool, bool) -> ...
        """Constructor.
        
        :param name: name of the file to operate on
        :param strict: a bool specifies the creatability
        :param make_executable: a bool specifies whether make the file executable or not (obviously)
        """
        self.name = name
        try:
            self.extension = _re.findall("\.(.+)$", self.name)[0]
        except IndexError:
            self.extension = ''
        self.contents = ''
        self.created = False  # to delete it if we want to

        if not _os.path.isfile(self.name):
            if not strict:
                self.create()
            else:
                raise ValueError("File name doesn't exist.")

        else:
            with open(self.name) as f:
                self.contents = f.read()

        if make_executable:
            self.make_executable()

    def create(self):
        # type: () -> None
        """create an empty file of the object's name, setting self.created into True."""
        self.created = True
        with open(self.name, 'w') as f:
            f.write('')

    def save(self):
        with open(self.name, 'w') as f:
            f.write(self.contents)

    def make_executable(self):
        # type: () -> None
        """change the stat of the object's file name to be executable
        
        Example:
             -rw-rw-rw becomes -rwxrwxrwx
             -rw------ becomes -rwx------
        """
        mode = _os.stat(self.name).st_mode
        mode |= (mode & 0o444) >> 2
        _os.chmod(self.name, mode)


class InterpreterPath(object):
    """The interpreter's path and its state."""

    def __init__(self, path, default=False, symlinks_to=''):
        """Constructor.
        :param path: the path of the interpreter
        :param default: whether it's the default interpreter or not
        :param symlinks_to: the file that it might symlinks
        """
        self.path = path
        self.default = default
        self.symlinks_to = symlinks_to

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        return repr(self.path)


class ShebangedFile(object):
    """The file that will implement the required shebang.
    
    basic usage:
        >>> sf = ShebangedFile(UnshebangedFile("file.py", False, False))
        >>> sf.put_shebang()
        0
        >>> print(sf.shebang)
        #!/usr/bin/python
        <BLANKLINE>
        >>> sf.file.make_executable()
        >>> sf.shebang = "#!/usr/bin/ruby\\n"
        >>> sf.put_shebang()
        0
        >>> print(sf.shebang)
        #!/usr/bin/ruby
        <BLANKLINE>
        >>> sf.file.save()
    """

    ALL_SHEBANGS = _Data.load()

    def __init__(self, unshebanged_file):
        # type: (UnshebangedFile) -> ...
        """Constructor.
        :param unshebanged_file: the file to add the shebang into
        """
        self.file = unshebanged_file
        try:
            self.shebang = "#!{}\n".format(which(ShebangedFile.ALL_SHEBANGS[self.file.extension]["default"][0])[0])
        except (IndexError, KeyError):
            self.shebang = ''

    def put_shebang(self, newline_count=1, overwrite=True):
        # type: (int, bool) -> int
        """Puts the shebang on the first line of self.file plus ('\n' * newline_count).
        
        :param newline_count: number of '\n' appended after the shebang
        :param overwrite: overwrite if it's a broken shebang
        :return: what check_shebang returns
        """

        code = self.check_shebang()
        if code == 1:
            return code
        elif code == 2:
            if overwrite:
                self.remove_shebang()
            else:
                return code

        self.file.contents = (self.shebang + '\n' * newline_count) + self.file.contents
        return 0

    def remove_shebang(self):
        # type: () -> bool
        """Removes the shebang line from the file plus any whitespaces.
        
        :return: True -> successfully removed the shebang
                 False - did nothing
        """
        con = self.file.contents  # just an alias
        if con.startswith("#!"):
            con = con[con.find('\n') + 1:]
            self.file.contents = _re.sub("^\s*", '', con)
            return True

        return False

    def check_shebang(self):
        # type: (bool) -> int
        """Checks if a shebang does exist and reports its state. 
        
        :return:
            2 -> There's a shebang, but it's pointing to a wrong interpreter
            1 -> The correct the shebang is already there
            0 -> Don't care..
        """

        con = self.file.contents
        if con.startswith(self.shebang):
            return 1

        elif con.startswith("#!"):
            return 2

        return 0

    @staticmethod
    def print_known(get_symlinks):
        """Prints a nice formatted table of known interpreters.
        
        prints a table its cells is consists of:
                           +------------+----------------------------+--------------------------------------------+
                           | .`extension'| interpreter name (a list) | available interpreter paths (also a list)) |
                           +------------+----------------------------+--------------------------------------------+
                Example:   | .py        | [python, pypy and jython]  | [/usr/bin/python and /usr/bin/python2]     | 
                           +------------+----------------------------+--------------------------------------------+
        :param get_symlinks: if true, get symlinks in `available paths' column
        """
        import tabulate

        def _format(dictionary):
            all = dictionary["all"]
            s = _decorate('{G}[')
            for i in all:
                # if it's a list it'll be an interpreter and we wan't to show it's version
                version = isinstance(dictionary["default"], list) and dictionary["default"][1] or 0
                dec_i = _decorate("{B}" + i)
                if i == dictionary["default"] or i in dictionary["default"]:
                    s += dec_i + _decorate(" ({GR}default{v}{GR})",
                                           v=(_decorate(' ({Y}v{G}{v}{GR})', v=version) if version else ''))
                else:
                    s += dec_i

                if i != all[-1]:
                    s += _decorate('{Y}, ')

            s += _decorate("{G}]")

            if len(all) >= 2:
                s = _decorate(" and").join(s.rsplit(',', 1))

            return s

        doesnt_fit = True
        headers = ("Extension", "Available Interpreter(s)", "Available Interpreter Path(s)")
        data = []
        for ext in ShebangedFile.ALL_SHEBANGS:
            tup = ShebangedFile.get_interpreter_path("file.{}".format(ext), get_versions=True,
                                                     get_symlinks=not get_symlinks)
            data.append(((_decorate("{GR}.{C}" + ext)), _format(tup[0]), _format(tup[1])))
        table = tabulate.tabulate(
            data,
            headers=tuple(map(lambda h: _decorate("{G}" + h), headers)),
            tablefmt="fancy_grid"
        )
        while doesnt_fit:

            if len(table.split('\n')[0]) >= _shutil.get_terminal_size()[0]:
                print(_decorate("{INFO} {GR}Your screen size doesn't fit for the whole table."))
                print(_decorate("{INFO} {GR}Available columns: " + ", ".join(
                    [_decorate("{G}[{Y}{n}{G}] {c}", n=n+1, c=c) for n, c in enumerate(headers)]
                ) + '.'))
                rep = input(_decorate("{INFO} {GR}Enter column numbers that you want to add separated by a comma: "))
                rep = rep.split(',')
                edited_headers = []
                error = False
                for h in rep:
                    try:
                        edited_headers.append(headers[int(h) - 1])
                    except (IndexError, ValueError):
                        print(_decorate("{ERR} {R}ERROR{W}: {GR} invalid input"))
                        error = True
                        break
                if error:
                    continue
            doesnt_fit = False
            print(table)

    @staticmethod
    def get_interpreter_path(name=None, interpreter=None, get_versions=False, get_symlinks=True):
        # type: (str, str, bool, bool) -> Tuple[Dict[str: List[str], str: List[str]], Dict[str: str, str: List[str]]]
        """Get path of interpreters.
        
        :param name: get interpreter path based on its extension
        :param interpreter: get interpreter path based on its name (higher precedence than the actual file name)
        :param get_versions: get available versions (however, if false, if `interpreter' or `the default interpreter'
        contains a version, you'll receive it)
        :param get_symlinks: get the symlink even if the realpath of it is already in the `available_paths'
                             (if get_versions is false, it'll have no effect) 
        :return: available interpreters (default and other) and their paths (default and other also)
        """

        version_regex = r'^%s-?(\d{1,4}(\.\d{1,2}(\.\d)?)?)?$'

        if interpreter is not None:
            l_name, version = _re.findall(version_regex % '(\w+)', interpreter)[0][:2]
            interpreters = {"default": [l_name, version], "all": [l_name]}
        elif name is not None:
            try:
                # the error might happens here and should only be here
                interpreters = ShebangedFile.ALL_SHEBANGS[_re.findall("\.(.+)$", name)[0]]

                interpreters = {"default": interpreters["default"],
                                "all": [interpreters["default"][0]] + interpreters["other"],
                                }
            except(IndexError, KeyError):
                # couldn't find the extension in the file name or it doesn't exist in the json file
                return {}, {}
        else:
            raise TypeError("either 'name' or 'lang' should be specified")

        # ======== Initializations used in all cases ==================
        default_path = ''
        d = interpreters["default"]
        a = interpreters["all"]
        regex = _re.compile("^{}-?{}$".format(*d))
        for i in which(d[0] + "*"):
            if regex.match(_os.path.basename(i)):
                default_path = i
                break
        del regex
        # ===============================================================

        if not get_versions:
            all_paths = [p for i in a for p in which(i)]

            return interpreters, {"default": default_path, "all": sorted(all_paths)}

        # bring all the files that starts with each `interpreter' and see if it matches the regex
        #                   (the goal is to specify any version of it)
        all_paths = [p for i in a for p in which(i + '*') if _re.match(version_regex % i, _os.path.basename(p))]

        if not get_symlinks:
            dummy = all_paths
            all_paths = filter(lambda path: not (_os.path.islink(path) and _os.path.realpath(path) in dummy),
                               all_paths)

        return interpreters, {"default": default_path, "all": sorted(all_paths, reverse=True)}

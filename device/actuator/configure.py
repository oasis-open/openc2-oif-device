#!/usr/bin/env python
"""
Creates Dockerfiles based off the template
"""
import importlib
import json
import os
import re
import string
import subprocess
import sys

if sys.version_info < (3, 6):
    print('PythonVersionError: Minimum version of v3.6+ not found')
    exit(1)


# Utility Classes
class FrozenDict(dict):
    def __init__(self, *args, **kwargs):
        self._hash = None
        super(FrozenDict, self).__init__(*args, **kwargs)

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(tuple(sorted(self.items())))  # iteritems() on py2
        return self._hash

    def __getattr__(self, item):
        return self.get(item, None)

    def _immutable(self, *args, **kws):
        raise TypeError('cannot change object - object is immutable')

    __setitem__ = _immutable
    __delitem__ = _immutable
    pop = _immutable
    popitem = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable


class ConsoleStyle:
    def __init__(self):
        import colorama
        colorama.init()
        self.encoding = sys.getdefaultencoding()
        self.format_regex = re.compile(r'\[\d+m', flags=re.MULTILINE)
        self.TextStyles = FrozenDict({
            # Styles
            'RESET': colorama.Fore.RESET,
            'NORMAL': colorama.Style.NORMAL,
            'DIM': colorama.Style.DIM,
            'BRIGHT': colorama.Style.BRIGHT,
            # Text Colors
            'FG_BLACK': colorama.Fore.BLACK,
            'FG_BLUE': colorama.Fore.BLUE,
            'FG_CYAN': colorama.Fore.CYAN,
            'FG_GREEN': colorama.Fore.GREEN,
            'FG_MAGENTA': colorama.Fore.MAGENTA,
            'FG_RED': colorama.Fore.RED,
            'FG_WHITE': colorama.Fore.WHITE,
            'FG_YELLOW': colorama.Fore.YELLOW,
            'FG_RESET': colorama.Fore.RESET,
            # Background Colors
            'BG_BLACK': colorama.Back.BLACK,
            'BG_BLUE': colorama.Back.BLUE,
            'BG_CYAN': colorama.Back.CYAN,
            'BG_GREEN': colorama.Back.GREEN,
            'BG_MAGENTA': colorama.Back.MAGENTA,
            'BG_RED': colorama.Back.RED,
            'BG_WHITE': colorama.Back.WHITE,
            'BG_YELLOW': colorama.Back.YELLOW,
            'BG_RESET': colorama.Back.RESET,
        })

    def _toStr(self, txt):
        return txt.decode(self.encoding, 'backslashreplace') if hasattr(txt, 'decode') else txt

    def colorize(self, txt, *styles):
        txt = self._toStr(txt)
        self._log(txt)
        color_text = ''.join([Stylize.TextStyles.get(s.upper(), '') for s in styles]) + txt
        return f'\033[0m{color_text}\033[0m'

    def _log(self, txt):
        pass

    # Headers
    def underline(self, txt):
        print(self.colorize(txt, 'UNDERLINE', 'BOLD'))

    def h1(self, txt):
        tmp = self.colorize(f'\n{txt}', 'UNDERLINE', 'BOLD', 'FG_CYAN')
        print(tmp)

    def h2(self, txt):
        print(self.colorize(f'\n{txt}', 'UNDERLINE', 'BOLD', 'FG_WHITE'))

    def debug(self, txt):
        print(self.colorize(txt, 'FG_WHITE'))

    def info(self, txt):
        print(self.colorize(f'> {txt}',  'FG_WHITE'))

    def success(self, txt):
        print(self.colorize(txt, 'FG_GREEN'))

    def error(self, txt):
        print(self.colorize(f'x {txt}', 'FG_RED'))

    def warn(self, txt):
        print(self.colorize(f'-> {txt}', 'FG_YELLOW'))

    def bold(self, txt):
        print(self.colorize(txt, 'BOLD'))

    def note(self, txt):
        print(f"{self.colorize('Note:', 'UNDERLINE', 'BOLD', 'FG_CYAN')} {self.colorize(txt, 'FG_CYAN')}")

    def default(self, txt):
        txt = self._toStr(txt)
        print(self.colorize(txt))

    def verbose(self, style, txt):
        if style is not 'verbose' and hasattr(self, style) and callable(getattr(self, style)):
            if options.verbose:
                getattr(self, style)(txt)
            else:
                self._log(txt)


# Util Function
def install(package):
    try:
        importlib.import_module(package[0])
    except ImportError:
        print(f'{package[1]} not installed')
        try:
            pkg_install = subprocess.Popen([sys.executable, "-m", "pip", "install", package[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = pkg_install.communicate()
        except Exception as e:
            print(e)
    finally:
        setattr(sys.modules[__name__], package[0], importlib.import_module(package[0]))


def safe_load(json_path):
    try:
        return json.load(open(json_path, 'r'))
    except (IOError, ValueError):
        return {}


def mk_dockerfile(act=None, def_args={}):
    act_path = os.path.join(CONFIG.WorkDir, act)
    if os.path.isdir(act_path):
        Stylize.info(f'Creating Dockerfile for {act}')
        args = dict(def_args)
        args['ACT_NAME'] = act
        args.update(safe_load(os.path.join(act_path, CONFIG.ArgFiles.Image)))

        with open(os.path.join(act_path, 'Dockerfile'), 'w+') as df:
            df.write(CONFIG.DockerTemplate.safe_substitute(**args))
    else:
        Stylize.error(f'No directory for {act}')


# Script Vars
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG = FrozenDict(
    WorkDir=ROOT_DIR,
    Requirements=(
        ('colorama', 'colorama'),
    ),
    ArgFiles=FrozenDict(
        Image='image.args.json',
        Default='default.args.json'
    ),
    TemplateFile=os.path.join(ROOT_DIR, 'Dockerfile.template')
)

Args = {key: value.strip() for key, value in os.environ.items()}
Args.update(safe_load(CONFIG.ArgFiles.Default))
Args['BASE_NAME'] = Args.get('BASE_IMAGE_NAME', Args.get('IMAGE_NAME', 'oif/base'))

CONFIG = FrozenDict(
    **CONFIG,
    Args=FrozenDict(Args),
    Actuators=tuple(d for d in os.listdir(CONFIG.WorkDir) if os.path.isdir(os.path.join(CONFIG.WorkDir, d)) and not d.startswith(('.', '_'))),
    DockerTemplate=string.Template(open(CONFIG.TemplateFile, 'r').read()) if os.path.isfile(CONFIG.TemplateFile) else ''
)
del Args

if __name__ == '__main__':
    print('Installing Requirements')
    for PKG in CONFIG.Requirements:
        install(PKG)

    Stylize = ConsoleStyle()

    # -------------------- Make Docker Files -------------------- #
    Stylize.h1('Make Dockerfiles ...')
    for act in CONFIG.Actuators:
        # Make Dockerfile
        mk_dockerfile(act, CONFIG.Args)

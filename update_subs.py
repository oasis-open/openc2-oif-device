#!/usr/bin/env python

import atexit
import fnmatch
import importlib
import os
import re
import shutil
import stat
import subprocess
import sys

from datetime import datetime
from getpass import getpass
from optparse import OptionParser

try:
    input = raw_input
except NameError:
    pass

if sys.version_info < (3, 6):
    print('PythonVersionError: Minimum version of v3.6+ not found')
    exit(1)


def checkRequiredArguments(opts, parser):
    missing_options = []
    for option in parser.option_list:
        if re.match(r'^\[REQUIRED\]', option.help) and eval('opts.' + option.dest) is None:
            missing_options.extend(option._long_opts)
    if len(missing_options) > 0:
        parser.error('Missing REQUIRED parameters: ' + str(missing_options))


# Option Parsing
parser = OptionParser()
parser.add_option("-u", "--url_base", dest="url_base", default="", help="[REQUIRED] Base URL for git repo")
parser.add_option("-r", "--repo_branch", dest="repo_branch", default="master", help="Branch to clone from the repo")
parser.add_option("-l", "--log_file", dest="log_file", help="Write logs to LOG_FILE")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose output of container build")

(options, args) = parser.parse_args()
checkRequiredArguments(options, parser)

log_file = None
init_now = datetime.now()

if options.log_file:
    name, ext = os.path.splitext(options.log_file)
    ext = '.log' if ext is '' else ext
    fn = f'{name}-{init_now:%Y.%m.%d_%H.%M.%S}{ext}'
    # log_file = open(fn, 'w+')
    log_file = open(options.log_file, 'w+')
    log_file.write(f'Configure run at {init_now:%Y.%m.%d_%H:%M:%S}\n\n')
    log_file.flush()
    atexit.register(log_file.close)


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
        if log_file:
            txt = self.format_regex.sub('', self._toStr(txt))
            log_file.write(f'{txt}\n')
            log_file.flush()

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


# Script Config
ItemCount = 1

if options.url_base.startswith("http"):
    Base_URL = options.url_base if options.url_base.endswith("/") else options.url_base + '/'
else:
    Base_URL = options.url_base if options.url_base.endswith(":") else options.url_base + ':'

CONFIG = FrozenDict(
    RootDir=os.path.dirname(os.path.realpath(__file__)),
    Requirements=(
        ('git', 'gitpython==2.1.11'),
        ('colorama', 'colorama')
    ),
    EmptyString=('', b'', None),
    BaseRepo=f"{Base_URL}ScreamingBunny",
    DefaultBranch="master",
    Remove=FrozenDict(
        Dirs=(".git", ".idea"),
        Files=(".git", ".gitlab-ci.yml", "dev-compose.yaml", ".gitmodules")
    ),
    ImageReplace=(
        ("base", "gitlab.*docker:alpine", "oif/base:alpine"),
        ("python3", "gitlab.*plus:alpine-python3", "oif/base:alpine-python3")
    ),
    Repos=FrozenDict(
        Actuators=('ISR', ),
        Transport=('HTTPS', 'MQTT'),
    )
)


# Utility Classes (Need Config)
class Stage:
    def __init__(self, name='Stage', root=CONFIG.RootDir):
        self.name = name
        self.root = root if root.startswith(CONFIG.RootDir) else os.path.join(CONFIG.RootDir, root)

    def __enter__(self):
        Stylize.h1(f"[Step {get_count()}]: Update {self.name}")
        return self._mkdir_chdir()

    def __exit__(self, type, value, traceback):
        global ItemCount
        ItemCount += 1
        os.chdir(CONFIG.RootDir)
        Stylize.success(f'Updated {self.name}')

    def _set_rw(self, operation, name, exc):
        os.chmod(name, stat.S_IWRITE)
        os.remove(name)

    def _mkdir_chdir(self):
        self._mkdir_p(self.root)
        os.chdir(self.root)
        return self.root

    def _mkdir_p(self, path='', rem=[]):
        if len(rem) > 0:
            path = os.path.join(path, rem[0])
            if not os.path.isdir(path):
                os.mkdir(path)
            if len(rem) > 1:
                self._mkdir_p(path, rem[1:])

        if not os.path.isdir(path):
            dirs = path.split(os.sep)
            self._mkdir_p((os.sep if path.startswith(os.sep) else '') + dirs[0], dirs[1:])


# Utility Functions
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


def recursive_find(rootdir='.', patterns=('*', ), directory=False):
    results = []
    for (base, dirs, files) in os.walk(rootdir):
        search = dirs if directory else files
        matches = [fnmatch.filter(search, pattern) for pattern in patterns]
        matches = [v for sl in matches for v in sl]
        results.extend(os.path.join(base, f) for f in matches)
    return results


def git_lsremote(url):
    remote_refs = {}
    g = git.cmd.Git()
    for ref in g.ls_remote(url).split('\n'):
        hash_ref_list = ref.split('\t')
        remote_refs[hash_ref_list[1]] = hash_ref_list[0]
    return remote_refs


def update_repo(repo_url, repo_path, branch=options.repo_branch):
    def set_rw(operation, name, exc):
        os.chmod(name, stat.S_IWRITE)
        os.remove(name)

    if os.path.isdir(repo_path):
        shutil.rmtree(repo_path, onerror=set_rw)
    try:
        branch = branch if f"refs/heads/{branch}" in git_lsremote(repo_url) else CONFIG.DefaultBranch
        repo = git.Repo.clone_from(repo_url, repo_path, branch=branch)
    except git.cmd.GitCommandError as e:
        Stylize.error(e)
        return

    os.chdir(repo_path)

    for f in recursive_find(patterns=CONFIG.Remove.Files):
        os.remove(f)

    for d in recursive_find(patterns=CONFIG.Remove.Dirs, directory=True):
        shutil.rmtree(d, onerror=set_rw)

    os.chdir('../')


def prompt(msg, err_msg, isvalid, password=False):
    res = None
    password = password if type(password) == bool else False

    while res is None:
        if password:
            res = getpass()
        else:
            res = input(str(msg)+': ')

        if not isvalid(res):
            print(str(err_msg))
            res = None
    return res


def get_count():
    global ItemCount
    c = ItemCount
    ItemCount += 1
    return c


if __name__ == '__main__':
    os.chdir(CONFIG.RootDir)

    print('Installing Requirements')
    for PKG in CONFIG.Requirements:
        install(PKG)

    Stylize = ConsoleStyle()
    import git

    Stylize.default('')

    if sys.platform in ["win32", "win64"]:  # Windows 32/64-bit
        git.Git.USE_SHELL = True

    Stylize.underline('Starting Update')

    # -------------------- Modules -------------------- #
    with Stage('Modules', 'modules'):
        Stylize.h2("Updating Utilities")
        update_repo(f"{CONFIG.BaseRepo}/Utils.git", 'utils')

    # -------------------- Device Transport -------------------- #
    with Stage('Device Transport', os.path.join('device', 'transport')):
        for transport in CONFIG.Repos.Transport:
            Stylize.h2(f"Updating Device {transport}")
            update_repo(f"{CONFIG.BaseRepo}/Device/Transport/{transport}.git", transport.lower())

    # -------------------- Device Actuators -------------------- #
    with Stage('Device', 'device') as d:
        Stylize.h2(f"Updating Actuators")
        update_repo(f"{CONFIG.BaseRepo}/Device/Actuator.git", 'actuator')

    # -------------------- Logger -------------------- #
    with Stage('Logger'):
        Stylize.h2("Updating Logger")
        update_repo(f"{CONFIG.BaseRepo}/Logger.git", 'logger')

    # -------------------- Dockerfile -------------------- #
    with Stage('Dockerfiles'):
        for dockerfile in recursive_find(patterns=['Dockerfile']):
            with open(dockerfile, 'r') as f:
                tmpFile = f.read()

            for img in CONFIG.ImageReplace:
                if re.search(img[1], tmpFile):
                    Stylize.info(f'Updating {dockerfile}')
                    Stylize.bold(f'- Found {img[0]} image, updating for public repo\n')
                    tmpFile = re.sub(img[1], img[2], tmpFile)
                    with open(dockerfile, 'w') as f:
                        f.write(tmpFile)
                    break

    Stylize.info("Run `configure.py` from the public folder to create the base containers necessary to run the OIF Device")

# Utility functions for update_subs and configure
import fnmatch
import importlib
import io
import os
import re
import shutil
import stat
import subprocess
import sys

try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain


# Classes
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
    def __init__(self, verbose=False, log=None):
        import colorama
        colorama.init()
        self._verbose = verbose if isinstance(verbose, bool) else False
        self._logFile = log if isinstance(verbose, (str, io.TextIOWrapper)) else None

        self._encoding = sys.getdefaultencoding()
        self._format_regex = re.compile(r"\[\d+m", flags=re.MULTILINE)
        self._textStyles = FrozenDict({
            # Styles
            "RESET": colorama.Fore.RESET,
            "NORMAL": colorama.Style.NORMAL,
            "DIM": colorama.Style.DIM,
            "BRIGHT": colorama.Style.BRIGHT,
            # Text Colors
            "FG_BLACK": colorama.Fore.BLACK,
            "FG_BLUE": colorama.Fore.BLUE,
            "FG_CYAN": colorama.Fore.CYAN,
            "FG_GREEN": colorama.Fore.GREEN,
            "FG_MAGENTA": colorama.Fore.MAGENTA,
            "FG_RED": colorama.Fore.RED,
            "FG_WHITE": colorama.Fore.WHITE,
            "FG_YELLOW": colorama.Fore.YELLOW,
            "FG_RESET": colorama.Fore.RESET,
            # Background Colors
            "BG_BLACK": colorama.Back.BLACK,
            "BG_BLUE": colorama.Back.BLUE,
            "BG_CYAN": colorama.Back.CYAN,
            "BG_GREEN": colorama.Back.GREEN,
            "BG_MAGENTA": colorama.Back.MAGENTA,
            "BG_RED": colorama.Back.RED,
            "BG_WHITE": colorama.Back.WHITE,
            "BG_YELLOW": colorama.Back.YELLOW,
            "BG_RESET": colorama.Back.RESET,
        })

    def _toStr(self, txt):
        return txt.decode(self._encoding, "backslashreplace") if hasattr(txt, "decode") else txt

    def colorize(self, txt, *styles):
        txt = self._toStr(txt)
        self._log(txt)
        color_text = "".join([self._textStyles.get(s.upper(), "") for s in styles]) + txt
        return f"\033[0m{color_text}\033[0m"

    def _log(self, txt):
        if self._logFile:
            if isinstance(self._logFile, str):
                with open(self._logFile, 'a') as f:
                    f.write(f"{self._format_regex.sub('', self._toStr(txt))}\n")
            elif isinstance(self._logFile, io.TextIOWrapper):
                self._logFile.write(f"{self._format_regex.sub('', self._toStr(txt))}\n")

    # Headers
    def underline(self, txt):
        print(self.colorize(txt, "UNDERLINE", "BOLD"))

    def h1(self, txt):
        tmp = self.colorize(f"\n{txt}", "UNDERLINE", "BOLD", "FG_CYAN")
        print(tmp)

    def h2(self, txt):
        print(self.colorize(f"\n{txt}", "UNDERLINE", "BOLD", "FG_MAGENTA"))

    def h3(self, txt):
        print(self.colorize(f"\n{txt}", "UNDERLINE", "BOLD", "FG_YELLOW"))

    def debug(self, txt):
        print(self.colorize(txt, "FG_WHITE"))

    def info(self, txt):
        print(self.colorize(f"> {txt}",  "FG_WHITE"))

    def success(self, txt):
        print(self.colorize(txt, "FG_GREEN"))

    def error(self, txt):
        print(self.colorize(f"x {txt}", "FG_RED"))

    def warn(self, txt):
        print(self.colorize(f"-> {txt}", "FG_YELLOW"))

    def bold(self, txt):
        print(self.colorize(txt, "BOLD"))

    def note(self, txt):
        print(f"{self.colorize('Note:', 'UNDERLINE', 'BOLD', 'FG_CYAN')} {self.colorize(txt, 'FG_CYAN')}")

    def default(self, txt):
        txt = self._toStr(txt)
        print(self.colorize(txt))

    def verbose(self, style, txt):
        if style != "verbose" and hasattr(self, style) and callable(getattr(self, style)):
            if self._verbose:
                getattr(self, style)(txt)
            else:
                self._log(txt)


# Config
CONFIG = FrozenDict(
    DefaultBranch="master",
    EmptyString=("", b"", None),
    Remove=FrozenDict(
        Dirs=(".git", ".idea"),
        Files=(".git", "*.gitlab-ci.yml", "dev-compose.yaml", ".gitmodules", ".gitignore", ".pipeline_trigger*")
    ),
    MinVersions=FrozenDict(
        Docker=(18, 0, 0),
        DockerCompose=(1, 20, 0)
    )
)


# Functions
def checkRequiredArguments(opts, parser):
    missing_options = []
    for option in parser.option_list:
        if re.match(r'^\[REQUIRED\]', option.help) and eval('opts.' + option.dest) is None:
            missing_options.extend(option._long_opts)
    if len(missing_options) > 0:
        parser.error('Missing REQUIRED parameters: ' + str(missing_options))


def set_rw(operation, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)


def install_pkg(package):
    try:
        importlib.import_module(package[0])
    except ImportError:
        print(f'{package[1]} not installed')
        failed = bool(pipmain(["install", package[1]]))

        print(f"Install of {package[1]} {'failed' if failed else 'success'}'")
        if failed:
            exit(1)
    finally:
        print(f'{package[1]} installed')
        setattr(sys.modules[__name__], package[0], importlib.import_module(package[0]))


def import_mod(mod=None):
    if mod not in sys.modules:
        setattr(sys.modules[__name__], mod, importlib.import_module(mod))


def recursive_find(rootdir='.', patterns=('*', ), directory=False):
    results = []
    for (base, dirs, files) in os.walk(rootdir):
        search = dirs if directory else files
        matches = [fnmatch.filter(search, pattern) for pattern in patterns]
        matches = [v for sl in matches for v in sl]
        results.extend(os.path.join(base, f) for f in matches)
    return results


def git_lsremote(url):
    import_mod('git')

    remote_refs = {}
    g = git.cmd.Git()
    for ref in g.ls_remote(url).split('\n'):
        hash_ref_list = ref.split('\t')
        remote_refs[hash_ref_list[1]] = hash_ref_list[0]
    return remote_refs


def update_repo(repo_url, repo_path, branch="master"):
    import_mod('git')

    if os.path.isdir(repo_path):
        shutil.rmtree(repo_path, onerror=set_rw)
    try:
        branch = branch if f"refs/heads/{branch}" in git_lsremote(repo_url) else CONFIG.DefaultBranch
        repo = git.Repo.clone_from(repo_url, repo_path, branch=branch)
    except git.cmd.GitCommandError as e:
        print(e)
        return e

    os.chdir(repo_path)

    for f in recursive_find(patterns=CONFIG.Remove.Files):
        os.remove(f)

    for d in recursive_find(patterns=CONFIG.Remove.Dirs, directory=True):
        shutil.rmtree(d, onerror=set_rw)

    os.chdir('../')


def check_docker(console=None):
    msg = "Checking installed docker version"
    console.h2(msg) if isinstance(console, ConsoleStyle) else print(msg)

    installed_docker = subprocess.Popen(["docker", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = installed_docker.communicate()

    if err in CONFIG.EmptyString:
        installed_version = re.search(r"\d{,2}\.\d{,2}\.\d{,2}", str(out)).group()
        version = tuple(int(n) for n in installed_version.split("."))

        msg = f"required min docker: {version_str(CONFIG.MinVersions.Docker)}"
        console.info(msg) if isinstance(console, ConsoleStyle) else print(msg)

        if CONFIG.MinVersions.Docker <= version:
            msg = f"installed docker version: {installed_version}"
            console.note(msg) if isinstance(console, ConsoleStyle) else print(msg)
        else:
            msg = f"Need to upgrade docker package to {version_str(CONFIG.MinVersions.Docker)}+"
            console.error(msg) if isinstance(console, ConsoleStyle) else print(msg)
            exit(1)
    else:
        msg = "Failed to parse docker version"
        console.error(msg) if isinstance(console, ConsoleStyle) else print(msg)
        exit(1)


def check_docker_compose(console=None):
    msg = "Checking installed docker-compose version"
    console.h2(msg) if isinstance(console, ConsoleStyle) else print(msg)

    installed_compose = subprocess.Popen(["docker-compose", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = installed_compose.communicate()

    if err in CONFIG.EmptyString:
        installed_version = re.search(r"\d{,2}\.\d{,2}\.\d{,2}", str(out)).group()
        version = tuple(int(n) for n in installed_version.split("."))

        msg = f"required min docker-compose: {version_str(CONFIG.MinVersions.DockerCompose)}"
        console.info(msg) if isinstance(console, ConsoleStyle) else print(msg)

        if CONFIG.MinVersions.DockerCompose <= version:
            msg = f"installed docker-compose version: {installed_version}"
            console.note(msg) if isinstance(console, ConsoleStyle) else print(msg)

        else:
            msg = f"Need to upgrade docker-compose  to {version_str(CONFIG.MinVersions.DockerCompose)}+"
            console.error(msg) if isinstance(console, ConsoleStyle) else print(msg)
            exit(1)

    else:
        msg = "Failed to parse docker-compose version"
        console.error(msg) if isinstance(console, ConsoleStyle) else print(msg)

        exit(1)


def build_image(docker_sys=None, console=None, **kwargs):
    import_mod('docker')
    if docker_sys is None:
        msg = f"docker_sys arg is required"
        console.error(msg) if isinstance(console, ConsoleStyle) else print(msg)
        exit(1)

    img = None
    name = kwargs.pop("name") or kwargs["tag"]
    console.info(f"Building {name} image")
    try:
        img = docker_sys.images.build(**kwargs)
    except docker.errors.ImageNotFound as e:
        msg = f"Cannot build image, base image not found: {e}"
        console.error(msg) if isinstance(console, ConsoleStyle) else print(msg)
        exit(1)
    except docker.errors.APIError as e:
        msg = f"Docker API error: {e}"
        console.error(msg) if isinstance(console, ConsoleStyle) else print(msg)
        exit(1)
    except TypeError as e:
        msg = "Cannot build image, path nor fileobj args are not specified"
        console.error(msg) if isinstance(console, ConsoleStyle) else print(msg)
        exit(1)
    except KeyboardInterrupt:
        msg = "Keyboard Interrupt"
        console.error(msg) if isinstance(console, ConsoleStyle) else print(msg)
        exit(1)

    msg = "".join(line.get("stream", "") for line in img[1])
    console.verbose("default", msg) if isinstance(console, ConsoleStyle) else print(msg)
    return img


def human_size(size, units=(" bytes", "KB", "MB", "GB", "TB", "PB", "EB")):
    """ Returns a human readable string reprentation of bytes"""
    return f"{size:,d}{units[0]}" if size < 1024 else human_size(size >> 10, units[1:])


def version_str(ver):
    return ".".join(str(x) for x in ver)

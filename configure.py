#!/usr/bin/env python

import atexit
import fnmatch
import importlib
import os
import re
import shutil
import subprocess
import sys

from datetime import datetime
from optparse import OptionParser

if sys.version_info < (3, 6):
    print('PythonVersionError: Minimum version of v3.6+ not found')
    exit(1)

# Option Parsing
parser = OptionParser()
parser.add_option("-b", "--build-image", action="store_true", dest="build_image", default=False, help="Build containers")
parser.add_option("-l", "--log-gui", action="store_true", dest="log_gui", default=False, help="Build Logger GUI")
parser.add_option("-f", "--log-file", dest="log_file", help="Write logs to LOG_FILE")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose output of container/GUI build")

(options, args) = parser.parse_args()

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


# Script Vars
ItemCount = 1

RootDir = os.path.dirname(os.path.realpath(__file__))

CONFIG = FrozenDict(
    WorkDir=RootDir,
    ModuleDir=os.path.join(RootDir, 'modules'),
    Requirements=(
        ('docker', 'docker'),
        ('colorama', 'colorama'),
        ('yaml', 'pyyaml')
    ),
    EmptyString=('', b'', None),
    ImagePrefix='oif',
    Logging=FrozenDict(
        Default=(
            ('device', '-p device -f device-compose.yaml -f device-compose.log.yaml'),
        ),
        Central=(
            ('device', '-p device -f device-compose.yaml'),
        )
    ),
    ModuleCopy=FrozenDict(
        utils=(
            ('base', 'modules'),
            ('device', 'transport', 'mqtt', 'module')
        )
    ),
    MinVersions=FrozenDict(
        Docker=(18, 0, 0),
        DockerCompose=(1, 20, 0)
    ),
    GUIS=FrozenDict(
        Logger=('logger', 'gui')
    ),
    Composes=tuple(file for file in os.listdir(RootDir) if re.match(r'^\w*?-compose(\.\w*?)?\.yaml$', file))
)


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


def check_docker():
    Stylize.h2('Checking installed docker version')
    installed_docker = subprocess.Popen(['docker', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = installed_docker.communicate()

    if err in CONFIG.EmptyString:
        installed_version = re.search(r'\d{,2}\.\d{,2}\.\d{,2}', str(out)).group()
        version = tuple(int(n) for n in installed_version.split('.'))

        Stylize.info(f"required min docker: {version_str(CONFIG.MinVersions.Docker)}")

        if CONFIG.MinVersions.Docker <= version:
            Stylize.note(f"installed docker version: {installed_version}")
        else:
            Stylize.error(f"Need to upgrade docker package to {version_str(CONFIG.MinVersions.Docker)}+")
            exit(1)
    else:
        Stylize.error('Failed to parse docker version')
        exit(1)


def check_docker_compose():
    Stylize.h2('Checking installed docker-compose version')
    installed_compose = subprocess.Popen(['docker-compose', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = installed_compose.communicate()

    if err in CONFIG.EmptyString:
        installed_version = re.search(r'\d{,2}\.\d{,2}\.\d{,2}', str(out)).group()
        version = tuple(int(n) for n in installed_version.split('.'))

        Stylize.info(f"required min docker-compose: {version_str(CONFIG.MinVersions.DockerCompose)}")

        if CONFIG.MinVersions.DockerCompose <= version:
            Stylize.note(f"installed docker-compose version: {installed_version}")
        else:
            Stylize.error(f"Need to upgrade docker-compose  to {version_str(CONFIG.MinVersions.DockerCompose)}+")
            exit(1)

    else:
        Stylize.error('Failed to parse docker-compose version')
        exit(1)


def build_image(**kwargs):
    img = None
    try:
        img = system.images.build(**kwargs)
    except docker.errors.ImageNotFound as e:
        Stylize.error(f'Cannot build image, from image not found: {e}')
        exit(1)
    except docker.errors.APIError as e:
        Stylize.error(f'Docker API error: {e}')
        exit(1)
    except TypeError as e:
        Stylize.error('Cannot build image, path nor fileobj args are not specified')
        exit(1)
    except KeyboardInterrupt:
        Stylize.error('Keyboard Interrupt')
        exit(1)

    output = ''.join(line.get('stream', '') for line in img[1])
    Stylize.verbose('default', output)

    return img


def build_gui(gui_root=()):
    npm_cmds = (
        "npm install",
        # "find ./node_modules/babel-runtime -type f -exec sed -i \"\" -e 's/core-js\/library\/fn\//core-js\/features\//g' {} \;",
        "npm run init",
        "npm run build"
    )

    try:
        gui_build = system.containers.run(
            image='node:10-alpine',
            command=f"sh -c \"cd /project; {' && '.join(npm_cmds)}\"",
            volumes={
                os.path.join(CONFIG.WorkDir, *gui_root): {
                    'bind': '/project',
                    'mode': 'rw'
                }
            },
            auto_remove=True
        )
        Stylize.verbose('default', gui_build)
    except docker.errors.ContainerError as e:
        Stylize.error(f'Docker Container error: {e}')
        exit(1)
    except docker.errors.ImageNotFound as e:
        Stylize.error('Cannot build core gui webapp, node:10-alpine image not found')
        exit(1)
    except docker.errors.APIError as e:
        Stylize.error(f'Docker API error: {e}')
        exit(1)
    except KeyboardInterrupt:
        Stylize.error('Keyboard Interrupt')
        exit(1)


def mkdir_p(path='', rem=[]):
    if len(rem) > 0:
        path = os.path.join(path, rem[0])
        if not os.path.isdir(path):
            os.mkdir(path)
        if len(rem) > 1:
            mkdir_p(path, rem[1:])

    if not os.path.isdir(path):
        dirs = path.split(os.sep)
        mkdir_p((os.sep if path.startswith(os.sep) else '') + dirs[0], dirs[1:])


def human_size(size, units=(' bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB')):
    """ Returns a human readable string reprentation of bytes"""
    return f'{size:,d}{units[0]}' if size < 1024 else human_size(size >> 10, units[1:])


def version_str(ver):
    return '.'.join(str(x) for x in ver)


def get_count():
    global ItemCount
    c = ItemCount
    ItemCount += 1
    return c


if __name__ == '__main__':
    os.chdir(CONFIG.WorkDir)

    print('Installing Requirements')

    for PKG in CONFIG.Requirements:
        install(PKG)

    Stylize = ConsoleStyle()
    import docker

    Stylize.h1(f"[Step {get_count()}]: Check Docker Environment")
    check_docker()
    check_docker_compose()
    system = docker.from_env()

    try:
        system.info()
    except Exception as e:
        Stylize.error('Docker connection failed, check that docker is running')
        exit(1)

        # -------------------- Build Logger GUIs -------------------- #
    if (not options.build_image and not options.log_gui) or options.log_gui:
        Stylize.h1(f"[Step {get_count()}]: Build Logger GUI ...")
        build_gui(CONFIG.GUIS.Logger)
    else:
        build_root = os.path.join(CONFIG.WorkDir, *CONFIG.GUIS.Logger, 'build')
        if not os.path.isdir(build_root):
            mkdir_p(build_root)
            with open(os.path.join(build_root, 'index.html'), 'w') as f:
                f.write('<h1>Logger GUI</h1><h3>GUI placeholder, not built</h3>')

    # -------------------- Build Images -------------------- #
    if (not options.build_image and not options.log_gui) or options.build_image:
        Stylize.h1(f"[Step {get_count()}]: Creating base images ...")

        # -------------------- Copy Modules -------------------- #
        for module, dirs in CONFIG.ModuleCopy.items():
            mod_dir = os.path.join(CONFIG.ModuleDir, module)
            if os.path.isdir(mod_dir):
                Stylize.info(f"Copying module: {module}")
                for cp_dir in dirs:
                    dst_dir = os.path.join(CONFIG.WorkDir, *cp_dir, module)
                    if os.path.isdir(dst_dir):
                        shutil.rmtree(dst_dir)
                    shutil.copytree(mod_dir, dst_dir)
            else:
                Stylize.error(f'Module not found: {module}')
                exit(1)

        # -------------------- Build Base Images -------------------- #
        Stylize.info("Building base alpine image")
        build_image(
            path='./base',
            dockerfile='./Dockerfile_alpine',
            tag=f'{CONFIG.ImagePrefix}/base:alpine',
            pull=True,
            rm=True
        )

        Stylize.info("Building base alpine python3 image")
        build_image(
            path='./base',
            dockerfile='./Dockerfile_alpine-python3',
            tag=f'{CONFIG.ImagePrefix}/base:alpine-python3',
            rm=True
        )

        Stylize.info("Building base alpine python3 with sb_utils image")
        build_image(
            path='./base',
            dockerfile='./Dockerfile_alpine-python3_utils',
            tag=f'{CONFIG.ImagePrefix}/base:alpine-python3_utils',
            rm=True
        )

        # -------------------- Build Compose Images -------------------- #
        Stylize.h1(f"[Step {get_count()}]: Creating compose images ...")
        from yaml import load

        try:
            from yaml import CLoader as Loader
        except ImportError:
            from yaml import Loader

        rslt = subprocess.call([sys.executable, os.path.join('device', 'actuator', 'configure.py')])
        if rslt != 0:
            exit(rslt)
        compose_images = []

        Stylize.h1(f"Build images ...")
        for compose in CONFIG.Composes:
            with open(f'./{compose}', 'r') as orc_compose:
                for service, opts in load(orc_compose.read(), Loader=Loader)['services'].items():
                    if 'build' in opts and opts['image'] not in compose_images:
                        compose_images.append(opts['image'])
                        Stylize.info(f"Building {opts['image']} image")
                        build_image(
                            rm=True,
                            path=opts['build']['context'],
                            dockerfile=opts['build'].get('dockerfile', 'Dockerfile'),
                            tag=opts['image']
                        )

        # -------------------- Cleanup Images -------------------- #
        Stylize.h1(f"[Step {get_count()}]: Cleanup unused images ...")
        try:
            rm_images = system.images.prune()
            Stylize.info(f"Space reclaimed {human_size(rm_images.get('SpaceReclaimed', 0))}")
            if rm_images['ImagesDeleted']:
                for image in rm_images['ImagesDeleted']:
                    Stylize.verbose('info', f"Image deleted: {image.get('Deleted', 'IMAGE')}")

        except docker.errors.APIError as e:
            Stylize.error('Docker API error: ' + e)
            exit(1)
        except KeyboardInterrupt:
            Stylize.error('Keyboard Interrupt')
            exit(1)

    Stylize.success("\nConfiguration Complete")
    for key, opts in CONFIG.Logging.items():
        Stylize.info(f"{key} logging")
        for opt in opts:
            Stylize.info(f"-- Run 'docker-compose {opt[1]} up' to start the {opt[0]} compose")

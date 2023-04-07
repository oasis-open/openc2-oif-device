#!/usr/bin/env python

import atexit
import os
import re
import subprocess
import sys

from datetime import datetime
from optparse import OptionParser
from pathlib import Path

from base.modules.script_utils import (
    # Functions
    checkRequiredArguments,
    install_pkg,
    recursive_find,
    update_repo,
    # Classes
    ConsoleStyle,
    FrozenDict
)


if sys.version_info < (3, 6):
    print('PythonVersionError: Minimum version of v3.6+ not found')
    exit(1)


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
    ext = '.log' if ext == '' else ext
    fn = f'{name}-{init_now:%Y.%m.%d_%H.%M.%S}{ext}'
    log_file = open(options.log_file, 'w+')
    log_file.write(f'Configure run at {init_now:%Y.%m.%d_%H:%M:%S}\n\n')
    log_file.flush()
    atexit.register(log_file.close)


# Script Config
ItemCount = 1

if options.url_base.startswith("http"):
    Base_URL = options.url_base if options.url_base.endswith("/") else options.url_base + '/'
else:
    Base_URL = options.url_base if options.url_base.endswith(":") else options.url_base + ':'

CONFIG = FrozenDict(
    RootDir=os.path.dirname(os.path.realpath(__file__)),
    Requirements=(
        ('git', 'gitpython'),
        ('colorama', 'colorama')
    ),
    ImagePrefix="screambunn",
    BaseRepo=f"{Base_URL}screamingbunny",
    Repos=FrozenDict(
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

    def _mkdir_chdir(self):
        Path(self.root).mkdir(parents=True, exist_ok=True)
        os.chdir(self.root)
        return self.root


# Utility Functions
def get_count():
    global ItemCount
    c = ItemCount
    ItemCount += 1
    return c


if __name__ == '__main__':
    os.chdir(CONFIG.RootDir)

    print('Installing Requirements')
    for PKG in CONFIG.Requirements:
        install_pkg(PKG)

    Stylize = ConsoleStyle(options.verbose, log_file)
    import git

    Stylize.default('')

    if sys.platform in ["win32", "win64"]:  # Windows 32/64-bit
        git.Git.USE_SHELL = True

    Stylize.underline('Starting Update')

    # -------------------- Modules -------------------- #
    with Stage('Modules', 'base/modules/tmp'):
        Stylize.h2("Updating Utilities")
        update_repo(f"{CONFIG.BaseRepo}/utils.git", 'sb_utils', options.repo_branch)

    # -------------------- Device Transport -------------------- #
    with Stage('Device Transport', os.path.join('device', 'transport')):
        for transport in CONFIG.Repos.Transport:
            Stylize.h2(f"Updating Device {transport}")
            t = transport.lower()
            update_repo(f"{CONFIG.BaseRepo}/device/transport/{t}.git", t, options.repo_branch)

    # -------------------- Device Actuators -------------------- #
    with Stage('Device', 'device') as d:
        Stylize.h2(f"Updating Actuators")
        update_repo(f"{CONFIG.BaseRepo}/device/actuator.git", 'actuator', options.repo_branch)

        rslt = subprocess.call(
            [sys.executable, os.path.join("actuator", "configure.py")],
            env={
                'BASE_IMAGE_NAME': f"{CONFIG.ImagePrefix}/alpine-python3_actuator"
            }
        )
        if rslt != 0:
            exit(rslt)

    # -------------------- Logger -------------------- #
    with Stage('Logger'):
        Stylize.h2("Updating Logger")
        update_repo(f"{CONFIG.BaseRepo}/logger.git", 'logger', options.repo_branch)

    # Stylize.info("Run `configure.py` from the public folder to create the base containers necessary to run the OIF Device")

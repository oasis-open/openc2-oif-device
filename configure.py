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
from optparse import OptionParser
from pathlib import Path


from modules.script_utils import (
    # Functions
    build_image,
    build_gui,
    check_docker,
    check_docker_compose,
    checkRequiredArguments,
    human_size,
    install_pkg,
    # Classes
    ConsoleStyle,
    FrozenDict
)

if sys.version_info < (3, 6):
    print("PythonVersionError: Minimum version of v3.6+ not found")
    exit(1)

# Option Parsing
parser = OptionParser()
parser.add_option("-b", "--build-image", action="store_true", dest="build_image", default=False, help="Build containers")
parser.add_option("-l", "--log-gui", action="store_true", dest="log_gui", default=False, help="Build Logger GUI")
parser.add_option("-f", "--log-file", dest="log_file", help="Write logs to LOG_FILE")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose output of container/GUI build")

(options, args) = parser.parse_args()
checkRequiredArguments(options, parser)

log_file = None
init_now = datetime.now()

if options.log_file:
    name, ext = os.path.splitext(options.log_file)
    ext = ".log" if ext is "" else ext
    fn = f"{name}-{init_now:%Y.%m.%d_%H.%M.%S}{ext}"
    # log_file = open(fn, "w+")
    log_file = open(options.log_file, "w+")
    log_file.write(f"Configure run at {init_now:%Y.%m.%d_%H:%M:%S}\n\n")
    log_file.flush()
    atexit.register(log_file.close)


# Script Vars
ItemCount = 1

RootDir = os.path.dirname(os.path.realpath(__file__))

CONFIG = FrozenDict(
    WorkDir=RootDir,
    ModuleDir=os.path.join(RootDir, "modules"),
    Requirements=(
        ("docker", "docker"),
        ("colorama", "colorama"),
        ("yaml", "pyyaml")
    ),
    ImagePrefix="oif",
    Logging=FrozenDict(
        Default=(
            ("device", "-p device -f device-compose.yaml -f device-compose.log.yaml"),
        ),
        Central=(
            ("device", "-p device -f device-compose.yaml"),
        )
    ),
    ModuleCopy=FrozenDict(
        utils=(
            ("base", "modules"),
            ("device", "transport", "mqtt", "module")
        )
    ),
    GUIS=FrozenDict(
        Logger=("logger", "gui")
    ),
    Composes=tuple(file for file in os.listdir(RootDir) if re.match(r"^\w*?-compose(\.\w*?)?\.yaml$", file))
)


# Utility Functions
def get_count():
    global ItemCount
    c = ItemCount
    ItemCount += 1
    return c


if __name__ == "__main__":
    os.chdir(CONFIG.WorkDir)

    print("Installing Requirements")

    for PKG in CONFIG.Requirements:
        install_pkg(PKG)

    Stylize = ConsoleStyle(options.verbose, log_file)
    import docker

    Stylize.h1(f"[Step {get_count()}]: Check Docker Environment")
    check_docker(Stylize)
    check_docker_compose(Stylize)
    system = docker.from_env()

    try:
        system.info()
    except Exception as e:
        Stylize.error("Docker connection failed, check that docker is running")
        exit(1)

        # -------------------- Build Logger GUIs -------------------- #
    if (not options.build_image and not options.log_gui) or options.log_gui:
        Stylize.h1(f"[Step {get_count()}]: Build Logger GUI ...")
        if build_gui(system, os.path.join(CONFIG.WorkDir, *CONFIG.GUIS.Logger), Stylize):
            Stylize.error("Build Logger GUI Failed, logs will be centralized but not available")

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
                Stylize.error(f"Module not found: {module}")
                exit(1)

        # -------------------- Build Base Images -------------------- #
        Stylize.info("Building base alpine image")
        build_image(
            docker_sys=system,
            console=Stylize,
            path="./base",
            dockerfile="./Dockerfile_alpine",
            tag=f"{CONFIG.ImagePrefix}/base:alpine",
            pull=True,
            rm=True
        )

        Stylize.info("Building base alpine python3 image")
        build_image(
            docker_sys=system,
            console=Stylize,
            path="./base",
            dockerfile="./Dockerfile_alpine-python3",
            tag=f"{CONFIG.ImagePrefix}/base:alpine-python3",
            rm=True
        )

        Stylize.info("Building base alpine python3 with sb_utils image")
        build_image(
            docker_sys=system,
            console=Stylize,
            path="./base",
            dockerfile="./Dockerfile_alpine-python3_utils",
            tag=f"{CONFIG.ImagePrefix}/base:alpine-python3_utils",
            rm=True
        )

        # -------------------- Build Compose Images -------------------- #
        Stylize.h1(f"[Step {get_count()}]: Creating compose images ...")
        from yaml import load

        try:
            from yaml import CLoader as Loader
        except ImportError:
            from yaml import Loader

        rslt = subprocess.call([sys.executable, os.path.join("device", "actuator", "configure.py")])
        if rslt != 0:
            exit(rslt)
        compose_images = []

        Stylize.h1(f"Build images ...")
        for compose in CONFIG.Composes:
            with open(f"./{compose}", "r") as orc_compose:
                for service, opts in load(orc_compose.read(), Loader=Loader)["services"].items():
                    if "build" in opts and opts["image"] not in compose_images:
                        compose_images.append(opts["image"])
                        Stylize.info(f"Building {opts['image']} image")
                        build_image(
                            docker_sys=system,
                            console=Stylize,
                            rm=True,
                            path=opts["build"]["context"],
                            dockerfile=opts["build"].get("dockerfile", "Dockerfile"),
                            tag=opts["image"]
                        )

        # -------------------- Cleanup Images -------------------- #
        Stylize.h1(f"[Step {get_count()}]: Cleanup unused images ...")
        try:
            rm_images = system.images.prune()
            Stylize.info(f"Space reclaimed {human_size(rm_images.get('SpaceReclaimed', 0))}")
            if rm_images["ImagesDeleted"]:
                for image in rm_images["ImagesDeleted"]:
                    Stylize.verbose("info", f"Image deleted: {image.get('Deleted', 'IMAGE')}")

        except docker.errors.APIError as e:
            Stylize.error(f"Docker API error: {e}")
            exit(1)
        except KeyboardInterrupt:
            Stylize.error("Keyboard Interrupt")
            exit(1)

    Stylize.success("\nConfiguration Complete")
    for key, opts in CONFIG.Logging.items():
        Stylize.info(f"{key} logging")
        for opt in opts:
            Stylize.info(f"-- Run 'docker-compose {opt[1]} up' to start the {opt[0]} compose")

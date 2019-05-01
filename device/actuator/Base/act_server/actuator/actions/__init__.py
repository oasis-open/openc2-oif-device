"""
Dynamically load the actions functions from the current directory
"""
import pkgutil
import sys

from importlib import import_module
from pathlib import Path

actions = []
pairs = {}

for (_, action, _) in pkgutil.iter_modules([Path(__file__).parent]):
    action_module = import_module(f'.{action}', package=__name__)
    action_fun = getattr(action_module, action, None)
    pairs[action] = list(getattr(action_module, 'TARGET_FUNCTIONS', {}).keys())

    if action_fun is not None and action_fun.__name__ == action:
        setattr(sys.modules[__name__], action, action_fun)
        actions.append(action)

    del _, action, action_module, action_fun

del pkgutil, sys, import_module, Path

__all__ = [
    'actions',
    'pairs',
    *[act for act in actions]
]

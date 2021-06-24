# Unittest utility functions
import glob
import os

from functools import partialmethod
from typing import Iterable, List, Tuple
from sb_utils import SerialFormats


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return f'{num:3.1f}{unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f}Yi{suffix}'


def ext_glob(base: str, ext: Iterable[str]) -> List[str]:
    return [f for e in ext for f in glob.glob(f'{base}.{e}')]


class MetaTests(type):
    def __new__(mcs, name: str, bases: Tuple[type, ...], attrs: dict):
        if name.startswith('None'):
            return None
        # Get test functions
        good_test = attrs.get('_test_good_msg')
        bad_test = attrs.get('_test_bad_msg')

        # Make tests
        new_attrs = dict(attrs)
        if msg_dir := attrs.get('msg_dir', None):
            for msg in ext_glob(os.path.join(msg_dir, 'input/good/*/*/*'), SerialFormats):
                test, ext = os.path.splitext(msg.replace(f'{msg_dir}/input/', ''))
                test = test.replace(os.path.sep, '_')
                new_attrs.update({f'test_{ext[1:]}_{f}_{test}': partialmethod(good_test, msg_file=msg, fmt=f) for f in SerialFormats})

            for msg in ext_glob(os.path.join(msg_dir, 'input/bad/*/*/*'), SerialFormats):
                test, ext = os.path.splitext(msg.replace(f'{msg_dir}/input/', ''))
                test = test.replace(os.path.sep, '_')
                new_attrs.update({f'test_{ext[1:]}_{f}_{test}': partialmethod(bad_test, msg_file=msg, fmt=f) for f in SerialFormats})
        return super(MetaTests, mcs).__new__(mcs, name, bases, new_attrs)



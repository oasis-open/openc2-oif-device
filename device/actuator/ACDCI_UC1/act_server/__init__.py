import sys

ver = sys.version_info

if ver < (3, 6):
    print('PythonVersionError: Minimum version of v3.6+ not found')
    exit(1)

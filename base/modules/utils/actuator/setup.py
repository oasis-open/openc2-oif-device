from setuptools import setup

version = dict(
    major=0,
    minor=2,
    bugfix=0
)

setup(
    name='ScreamingBunny Utils.Actuator',
    version='{major}.{minor}.{bugfix}'.format(**version),
    package_data={
        'SB_Utils': [
            './sb_utils/*',
        ]
    },
    include_package_data=True
)

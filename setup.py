from setuptools import setup

versionfile = 'yvrtransit/version.py'
with open(versionfile, 'rb') as f:
    exec(compile(f.read(), versionfile, 'exec'))

setup(
    name='yvrtransit',
    version=__version__,  # noqa
    url='https://github.com/tdsmith/yvrtransit',
    license='MIT',
    author='Tim D. Smith',
    author_email='yvrtransit@tds.xyz',
    description='Some utilities for Vancouver, BC transit data',
    packages=['yvrtransit'],
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['click', 'python-dateutil', 'requests'],
    entry_points={'console_scripts': [
        'yvrtransit_fetch=yvrtransit.fetch:fetch',
        'yvrtransit_archive=yvrtransit.fetch:archive',
    ]}
)

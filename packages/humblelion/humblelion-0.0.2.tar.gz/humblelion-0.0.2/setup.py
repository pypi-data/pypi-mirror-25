import sys

from distutils.core import setup
from setuptools import find_packages

with open('requirements.txt', 'r') as dependencies:
    install_requires = [line.strip().replace('\n', '') for line in dependencies.readlines()]

if sys.platform.startswith('linux'):
    install_requires += [
        'dbus-python',   # requires libdbus-glib-1-dev
        'secretstorage',
    ]
setup(
    name='humblelion',
    version='0.0.2',
    url='https://github.com/MestreLion/humblebundle',
    description='An unofficial Humble Bundle API for listing and downloading games and bundles',
    packages=find_packages(exclude=['tests']),
    setup_requires=['setuptools-git'],
    author='Rodrigo Silva',
    author_email='linux@rodrigosilva.com',
    license='GPLv3+',
    keywords='api',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'humblelion = humblelion:cli',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)


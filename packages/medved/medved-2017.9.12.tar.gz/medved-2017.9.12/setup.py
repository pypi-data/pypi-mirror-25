#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
from setuptools import setup

version = '2017.9.12'
frozen_name = 'medved/frozen.py'

try:
    # noinspection PyUnresolvedReferences
    import compile
    compile.main()
except ImportError:
    pass

we_run_setup = False
if not os.path.exists(frozen_name):
    we_run_setup = True
    hash_ = subprocess.Popen(['hg', 'id', '-i'], stdout=subprocess.PIPE).stdout.read().decode().strip()
    print(f'Medved mercurial hash is {hash_}')
    frozen = open(frozen_name, 'w')
    frozen.write(f'# -*- coding: utf-8 -*-\nhg_hash = "{hash_}"\nversion = "{version}"\n')
    frozen.close()


setup(
    name='medved',
    version=version,
    description='Modulation Enhanced Diffraction Viewer and EDitor',
    author='Vadim Dyadkin',
    author_email='diadkin@esrf.fr',
    url='https://soft.snbl.eu/medved.html',
    license='GPLv3',
    long_description='Do not forget to cite: https://doi.org/10.1107/S2053273316008378',
    install_requires=[
        'numpy>=1.9',
        'scipy>=0.10.0',
        'fortranformat>=0.2.5',
        'pyqtgraph>=0.10.0',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'medved=medved.__init__:main',
        ],
    },
    packages=[
        'medved',
        'medved.ui',
    ],
)

if we_run_setup:
    os.remove(frozen_name)

import os
from glob import glob

from setuptools import setup, find_packages


setup(
    name='upgradegit',
    version='0.0.4',
    license='BSD',
    description='Upgrade PIP and package.json git to latest HEAD',
    url='https://bitbucket.org/mybucks/upgrade',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[
        os.path.splitext(os.path.basename(path))[0]
        for path in glob('src/*.py')
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    keywords=[],
    install_requires=[
        'click==6.7',
        'requirements-parser==0.1.0'
    ],
    extras_require={},
    entry_points={
        'console_scripts': [
            'upgradegit = upgradegit.cli:upgrade',
        ]
    },
)

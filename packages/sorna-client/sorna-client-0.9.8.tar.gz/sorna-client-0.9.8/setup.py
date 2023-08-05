from setuptools import setup
from pathlib import Path

install_requires = [
    'aiohttp>=2.2.0',
    'namedlist>=1.6',
    'python-dateutil>=2.5',
    'requests>=2.12',
    'simplejson',
    'ConfigArgParse>=0.12.0',
]
dev_requires = [
]
ci_requires = [
    'wheel',
    'twine',
]
test_requires = [
    'pytest>=3.1',
    'pytest-cov',
    'pytest-mock',
    'pytest-asyncio',
    'asynctest',
    'codecov',
]


setup(
    name='sorna-client',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.9.8',
    description='Sorna API Client Library',
    long_description=Path('README.rst').read_text(),
    url='https://github.com/lablup/sorna-client',
    author='Lablup Inc.',
    author_email='joongi@lablup.com',
    license='LGPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Environment :: No Input/Output (Daemon)',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
    ],
    packages=['sorna', 'sorna.asyncio', 'sorna.cli'],
    python_requires='>=3.5',
    install_requires=install_requires,
    extras_require={
        'dev': dev_requires + ci_requires + test_requires,
        'test': test_requires,
        'ci': ci_requires + test_requires,
    },
    data_files=[],
    entry_points={
        'console_scripts': [
            'lcc = sorna.cli:main',
            'lpython = sorna.cli:main',
        ],
    },
)

from setuptools import setup
from watch import __version__, __author__, __url__

setup(
    name='bwatch',
    version=__version__,
    author=__author__,
    py_modules=['watch'],
    author_email="hellflamedly@gmail.com",
    keywords=('binary watch', ),
    license='MIT',
    url=__url__,
    entry_points={
        'console_scripts': [
            'bwatch=watch:terminal'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Terminals',
        'Topic :: Text Processing'
    ],
    description="display a binary watch view in the terminal"
)


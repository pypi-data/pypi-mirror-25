"""Yer average Python setup, for staticjam!

Reads version from staticjam package. The PyPi readme
is staticjam's module-level docstring.

"""

from setuptools import setup
import ast

from staticjam import __version__


with open('staticjam/staticjam.py') as f:
    staticjam_contents = f.read()

module = ast.parse(staticjam_contents)
readme_docstring = ast.get_docstring(module)

setup(
    name='staticjam',
    version=__version__,
    description='markdown + jinja, static site generator',
    long_description=readme_docstring,
    author='SlimeMaid',
    author_email='SlimeMaid@gmail.com',
    keywords='cli',
    install_requires=['jinja2', 'BeautifulSoup4', 'docopt', 'markdown', 'lxml'],
    packages=['staticjam',],
    entry_points = {
        'console_scripts': [
            'staticjam=staticjam.__main__:entrypoint',
        ],
    },
    package_dir={'staticjam': 'staticjam'},
)

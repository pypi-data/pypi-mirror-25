# FIXME: -f and -v at same time doesn't work
# should i just make it staticjam help?
# staticjam version?
"""staticjam: Markdown + Jinja Site Generator

Only works in Python 3.

Usage:
    staticjam make (blog|pages|both)
    staticjam test
    staticjam init
    staticjam prune [-f | -a]
    staticjam --version
    staticjam (-h | --help)

Options:
    -h --help             Show this screen.
    --version             Show version.
    -f --force            Do not show summaries or ask when pruning.
    -a --ask-verbosely    Print verbose summaries when pruning.

"""

from docopt import docopt

from . import __version__
from . import staticjam


def entrypoint():
    """The Python "entrypoint" (main) of this CLI script.

    """

    arguments = docopt(__doc__, version='StaticJaM ' + __version__)
    if arguments['make'] and arguments['pages']:
        staticjam.create_pages()
    elif arguments['make'] and arguments['blog']:
        staticjam.create_blog()
    elif arguments['make'] and arguments['both']:
        staticjam.create_pages()
        staticjam.create_blog()
    elif arguments['test']:
        staticjam.http_server_test()
    elif arguments['prune']:
        staticjam.prune_generated_content(
            arguments['--force'],
            arguments['--ask-verbosely']
        )
    elif arguments['init']:
        staticjam.init()
    elif arguments['--version']:
        print(__version__)


if __name__ == "__main__":
    entrypoint()

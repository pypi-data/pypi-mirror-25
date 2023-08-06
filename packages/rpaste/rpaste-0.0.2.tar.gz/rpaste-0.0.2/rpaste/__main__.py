# -*- coding: utf-8 -*-

import sys

from .version import __version__


def main():
    print("RPaste version {}".format(__version__))
    return 0


if __name__ == "__main__":
    sys.exit(main())

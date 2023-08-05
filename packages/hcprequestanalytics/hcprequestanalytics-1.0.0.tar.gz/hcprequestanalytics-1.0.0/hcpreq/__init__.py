# The MIT License (MIT)
#
# Copyright (c) 2017 Thorsten Simons (sw@snomis.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse

from version import Gvars


def parseargs():
    """
    args - build the argument parser, parse the command line.
    """

    mp = argparse.ArgumentParser()
    mp.add_argument('--version', action='version',
                    version="%(prog)s: {0}\n"
                    .format(Gvars.Version))

    mp.add_argument('-d', dest='db', required=True,
                            help='the database file')
    mp.add_argument('-a', dest='additionalqueries',
                    required=False,
                    help='a file containg addition queries '
                         '(see documentation)')

    sp = mp.add_subparsers(dest='cmd')

    # mkdbp = sp.add_parser('mkdb',
    #                       help='setup the database')

    loadp = sp.add_parser('load',
                          help='load the database')

    loadp.add_argument(dest='logpkg',
                       help='the HCP log package to process')

    analyzep = sp.add_parser('analyze',
                          help='analyze the database')
    analyzep.add_argument('-p', dest='prefix', required=False,
                          default='',
                       help='prefix for the output files')

    analyzep.add_argument(dest='queries', nargs='*',
                       help='a list of query names, or nothing '
                            'for "all"')

    mkdbp = sp.add_parser('showqueries',
                          help='show the available queries')

    result = mp.parse_args()
    return result

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

from configparser import ConfigParser

class Queries(object):
    """
    A class that loads and provides SQL queries.
    """

    def __init__(self, stdqueries, addqueries=None):
        """
        :param stdqueries:  the name of the file holding the standard queries
        :param addqueries:  (optional) a name of a file with additional queries
        """
        self.c = ConfigParser()
        self.c.read(stdqueries, addqueries)

        # for s in self.c.keys():
        #     print(s)
        #     for p in self.c[s].keys():
        #         print('\t', p, ':', self.c.get(s, p))



    # def _loadqueries(self):
    #     """
    #     Load the queries from ini-style files
    #     """

        # for s in self.C.keys():
        #     for p in self.C[s].keys():
        #         try:
        #             if self.C[s][p].type == 'bool':
        #                 _c[p] = confp.getboolean(s, p)
        #             elif self.C[s][p].type == 'float':
        #                 _c[p] = confp.getfloat(s, p)
        #             elif self.C[s][p].type == 'int':
        #                 _c[p] = confp.getint(s, p)
        #             elif self.C[s][p].type == 'str':
        #                 _c[p] = confp.get(s, p)
        #         except Exception as y:
        #             errors.append('[{}]\n\t{}\t{}\t--> {}'
        #                           .format(s, p, self.C[s][p].type.upper(), y))
        #             if not self.C[s][p].req:
        #                 _c[p] = None
        # if errors:
        #     err = 'Fatal: {} configuration error(s)'.format(len(errors))
        #     for e in errors:
        #         err += '\n\t{}'.format(e)
        #     sys.exit(err)
        # self.conf = _c


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

import sqlite3
import csv
from time import time, asctime
from collections import OrderedDict

from hcpreq.queries import builtin_queries


class DB():

    def __init__(self, db):
        """
        Initialize the DB handler class.

        :param db:  the database file
        """
        self.db = db

    def opendb(self):
        """
        Open the database
        """

        self.con = sqlite3.connect(self.db)
        self.con.row_factory = sqlite3.Row

    def checkdb(self):
        """
        Check if the database file exists and create it if it doesn't.

        :raises:    in case of an invalid DB
        """

        cur = self.con.execute("SELECT count(name) FROM sqlite_master "
                         "WHERE type='table' AND name='admin'")
        rec = cur.fetchone()

        # create the DB if it doesn't exist
        if not rec['count(name)']:
            self._mkdb()

        cur = self.con.execute('SELECT * FROM admin LIMIT 1')
        rec = cur.fetchone()
        if rec:
            if rec['magic'] != 'hcprequestanalytics':
                raise sqlite3.DatabaseError(
                    'not a valid hcprequestanalytics database')
        else:
            raise sqlite3.DatabaseError('not a valid hcprequestanalytics'
                                        'database')

    def listqueries(self):
        """
        Return a list of available queries.

        :return: a list of tuples (queryname, description)
        """

        return [(x, self.queries[x][0]) for x in self.queries.keys()]

    def _mkdb(self):
        """
        Setup a new database.
        """

        self.con.execute("CREATE TABLE admin (magic TEXT, creationdate TEXT)")
        self.con.commit()

        self.con.execute("CREATE TABLE logrecs (node TEXT,\n"
                         "                      clientip TEXT,\n"
                         "                      user TEXT,\n"
                         "                      timestamp FLOAT,\n"
                         "                      timestampstr TEXT,\n"
                         "                      request TEXT,\n"
                         "                      path TEXT,\n"
                         "                      httpcode INT,\n"
                         "                      size INT,\n"
                         "                      namespace TEXT,\n"
                         "                      latency INT)")
        self.con.commit()

        self.con.execute("INSERT INTO admin (magic, creationdate)"
                         "       VALUES ('hcprequestanalytics', ?)",
                         (asctime(),))
        self.con.commit()



    def loaddb(self, inhdl, node):
        """
        Load the database with the records from a single file

        :param inhdl:   a filehandle for an open accesslog file
        :return:        the no. of read records
        """

        # Example record:
        # 0             1 2            3                     4      5    6                                                                7         8   9 10        11
        # 10.46.165.130 - webfarm_PROD [16/Aug/2017:23:03:09 +0200] "PUT /rest/7/5/F0505680-10B2-AD01-DEAD-026C667E9F75?type=whole-object HTTP/1.1" 201 0 GEDP.saez 113


        cur = self.con.cursor()
        cur.execute('BEGIN IMMEDIATE TRANSACTION')

        count = 0
        for l in inhdl.readlines():
            rec = l.strip().split()
            try:
                _r = {'node': node,
                      'clientip': rec[0],
                      'user': rec[2],
                      'timestamp': 0.0,
                      'timestampstr': rec[3][1:] + rec[4][:-1],
                      'request': rec[5][1:],
                      'path': rec[6],
                      'httpcode': int(rec[8]),
                      'size': rec[9],
                      'namespace': rec[10],
                      'latency': int(rec[11])
                      }
            except IndexError as e:
                print(rec)
                continue
            count += 1

            cur.execute('INSERT INTO logrecs'
                        '       (node, clientip, user, timestamp, timestampstr,'
                        '        request, path, httpcode, size, namespace, '
                        '        latency) VALUES'
                        '       (:node, :clientip, :user, :timestamp,'
                        '        :timestampstr, :request, :path, :httpcode,'
                        '        :size, :namespace, :latency)',
                        _r)

        self.con.commit()
        return count

    def loadqueries(self, aq=None):
        """
        Load the built-in (and evetually, additional queries)
        :param aq: the name of a file containing additional queries
        """
        self.queries = builtin_queries

        if aq:
            additional_queries = {}
            with open(aq, 'r') as aqhdl:
                exec(aqhdl.read())
            self.queries.update(additional_queries)

    def analyze(self, prefix, queries=None):
        """
        Analyze the database.

        :param prefix:  the prefix to add to each csv file written
        :param queries: a list of queries to run, or None to run all
        """

        self.con.create_aggregate("percentile", 2, PercentileFunc)
        cur = self.con.cursor()

        for qs in sorted(self.queries):
            # skip unwanted queries
            if not queries or qs in queries:
                first = True
                with open(prefix+qs+'.csv', 'w') as csvhdl:
                    print('running query "{}"'.format(qs))
                    start = time()
                    exec(builtin_queries[qs][1])

                    for rec in cur.fetchall():
                        if first:
                            writer = csv.DictWriter(csvhdl, fieldnames=list(rec.keys()))
                            writer.writeheader()
                            first = False
                        writer.writerow(row2dict(rec))

                    print('\trun time for query "{}": {:.3f} seconds'
                          .format(qs, time() - start))

    def close(self):
        """
        Close the database.
        """
        self.con.close()

def row2dict(_r):
    """
    Convert a sqlite3.RowFactory object into a dict.

    :param _r:  sqlite3.RowFactory object
    :return:    a dict w/ the content of _r
    """
    _d = OrderedDict()
    for k in _r.keys():
        _d[k] = _r[k]
    return _d

class PercentileFunc():
    """
    Aggregate function for use with sqlite3 - calculates a given percentile.
    """
    def __init__(self):
        self.list = []
        self.percent = None

    def step(self, value, percent):
        if value is None:
            return
        if self.percent is None:
            self.percent = percent
        if self.percent != percent:
            return
        self.list.append(value)

    def finalize(self):
        if len(self.list) == 0:
            return None
        self.list.sort()
        return self.list[
            int(round((len(self.list) - 1) * self.percent / 100.0))]

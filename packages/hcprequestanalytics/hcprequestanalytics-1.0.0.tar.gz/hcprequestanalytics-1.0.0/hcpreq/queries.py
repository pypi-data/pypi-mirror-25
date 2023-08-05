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


builtin_queries = {
    'count': ['count all records',
              'cur.execute("SELECT count(*) FROM logrecs")'],
    'clientip': ['per-clientIP analysis',
            'cur.execute("SELECT clientip, count(*), '
            '    min(size), avg(size), max(size), '
            '    percentile(size, 10), percentile(size, 20), '
            '    percentile(size, 30), percentile(size, 40), '
            '    percentile(size, 50), percentile(size, 60), '
            '    percentile(size, 70), percentile(size, 80), '
            '    percentile(size, 90), percentile(size, 95), '
            '    percentile(size, 99), percentile(size, 99.9), '
            '    min(latency), avg(latency),'
            '    max(latency), '
            '    percentile(latency, 10), percentile(latency, 20), '
            '    percentile(latency, 30), percentile(latency, 40), '
            '    percentile(latency, 50), percentile(latency, 60), '
            '    percentile(latency, 70), percentile(latency, 80), '
            '    percentile(latency, 90), percentile(latency, 95), '
            '    percentile(latency, 99), percentile(latency, 99.9) '
            '    FROM logrecs GROUP BY clientip")'],
    'clientip_http': ['httpcode-per-clientIP analysis',
                 'cur.execute("SELECT request, httpcode, count(*), '
                '    min(size), avg(size), max(size), '
                '    percentile(size, 10), percentile(size, 20), '
                '    percentile(size, 30), percentile(size, 40), '
                '    percentile(size, 50), percentile(size, 60), '
                '    percentile(size, 70), percentile(size, 80), '
                '    percentile(size, 90), percentile(size, 95), '
                '    percentile(size, 99), percentile(size, 99.9), '
                '    min(latency), avg(latency),'
                '    max(latency), '
                '    percentile(latency, 10), percentile(latency, 20), '
                '    percentile(latency, 30), percentile(latency, 40), '
                '    percentile(latency, 50), percentile(latency, 60), '
                '    percentile(latency, 70), percentile(latency, 80), '
                '    percentile(latency, 90), percentile(latency, 95), '
                '    percentile(latency, 99), percentile(latency, 99.9) '
                '    FROM logrecs GROUP BY clientip, httpcode")'],
    'clientip_http_node': ['node-per-httpcode-per-clientIP analysis',
                      'cur.execute("SELECT clientip, httpcode, node, count(*), '
                     '    min(size), avg(size), max(size), '
                     '    percentile(size, 10), percentile(size, 20), '
                     '    percentile(size, 30), percentile(size, 40), '
                     '    percentile(size, 50), percentile(size, 60), '
                     '    percentile(size, 70), percentile(size, 80), '
                     '    percentile(size, 90), percentile(size, 95), '
                     '    percentile(size, 99), percentile(size, 99.9), '
                     '    min(latency), avg(latency),'
                     '    max(latency), '
                     '    percentile(latency, 10), percentile(latency, 20), '
                     '    percentile(latency, 30), percentile(latency, 40), '
                     '    percentile(latency, 50), percentile(latency, 60), '
                     '    percentile(latency, 70), percentile(latency, 80), '
                     '    percentile(latency, 90), percentile(latency, 95), '
                     '    percentile(latency, 99), percentile(latency, 99.9) '
                     '    FROM logrecs GROUP BY clientip, httpcode, node")'],
    'req': ['per-request analysis',
            'cur.execute("SELECT request, count(*), '
            '    min(size), avg(size), max(size), '
            '    percentile(size, 10), percentile(size, 20), '
            '    percentile(size, 30), percentile(size, 40), '
            '    percentile(size, 50), percentile(size, 60), '
            '    percentile(size, 70), percentile(size, 80), '
            '    percentile(size, 90), percentile(size, 95), '
            '    percentile(size, 99), percentile(size, 99.9), '
            '    min(latency), avg(latency),'
            '    max(latency), '
            '    percentile(latency, 10), percentile(latency, 20), '
            '    percentile(latency, 30), percentile(latency, 40), '
            '    percentile(latency, 50), percentile(latency, 60), '
            '    percentile(latency, 70), percentile(latency, 80), '
            '    percentile(latency, 90), percentile(latency, 95), '
            '    percentile(latency, 99), percentile(latency, 99.9) '
            '    FROM logrecs GROUP BY request")'],
    'req_http': ['httpcode-per-request analysis',
                 'cur.execute("SELECT request, httpcode, count(*), '
                '    min(size), avg(size), max(size), '
                '    percentile(size, 10), percentile(size, 20), '
                '    percentile(size, 30), percentile(size, 40), '
                '    percentile(size, 50), percentile(size, 60), '
                '    percentile(size, 70), percentile(size, 80), '
                '    percentile(size, 90), percentile(size, 95), '
                '    percentile(size, 99), percentile(size, 99.9), '
                '    min(latency), avg(latency),'
                '    max(latency), '
                '    percentile(latency, 10), percentile(latency, 20), '
                '    percentile(latency, 30), percentile(latency, 40), '
                '    percentile(latency, 50), percentile(latency, 60), '
                '    percentile(latency, 70), percentile(latency, 80), '
                '    percentile(latency, 90), percentile(latency, 95), '
                '    percentile(latency, 99), percentile(latency, 99.9) '
                '    FROM logrecs GROUP BY request, httpcode")'],
    'req_http_node': ['node-per-httpcode-per-request analysis',
                      'cur.execute("SELECT request, httpcode, node, count(*), '
                     '    min(size), avg(size), max(size), '
                     '    percentile(size, 10), percentile(size, 20), '
                     '    percentile(size, 30), percentile(size, 40), '
                     '    percentile(size, 50), percentile(size, 60), '
                     '    percentile(size, 70), percentile(size, 80), '
                     '    percentile(size, 90), percentile(size, 95), '
                     '    percentile(size, 99), percentile(size, 99.9), '
                     '    min(latency), avg(latency),'
                     '    max(latency), '
                     '    percentile(latency, 10), percentile(latency, 20), '
                     '    percentile(latency, 30), percentile(latency, 40), '
                     '    percentile(latency, 50), percentile(latency, 60), '
                     '    percentile(latency, 70), percentile(latency, 80), '
                     '    percentile(latency, 90), percentile(latency, 95), '
                     '    percentile(latency, 99), percentile(latency, 99.9) '
                     '    FROM logrecs GROUP BY request, httpcode, node")'],
    'node': ['per-node analysis',
             'cur.execute("SELECT node, count(*), '
                     '    min(size), avg(size), max(size), '
                     '    percentile(size, 10), percentile(size, 20), '
                     '    percentile(size, 30), percentile(size, 40), '
                     '    percentile(size, 50), percentile(size, 60), '
                     '    percentile(size, 70), percentile(size, 80), '
                     '    percentile(size, 90), percentile(size, 95), '
                     '    percentile(size, 99), percentile(size, 99.9), '
                     '    min(latency), avg(latency),'
                     '    max(latency), '
                     '    percentile(latency, 10), percentile(latency, 20), '
                     '    percentile(latency, 30), percentile(latency, 40), '
                     '    percentile(latency, 50), percentile(latency, 60), '
                     '    percentile(latency, 70), percentile(latency, 80), '
                     '    percentile(latency, 90), percentile(latency, 95), '
                     '    percentile(latency, 99), percentile(latency, 99.9) '
                     '    FROM logrecs GROUP BY node")'],
    'node_req': ['node-per-request analysis',
                 'cur.execute("SELECT node, request, count(*), '
                     '    min(size), avg(size), max(size), '
                     '    percentile(size, 10), percentile(size, 20), '
                     '    percentile(size, 30), percentile(size, 40), '
                     '    percentile(size, 50), percentile(size, 60), '
                     '    percentile(size, 70), percentile(size, 80), '
                     '    percentile(size, 90), percentile(size, 95), '
                     '    percentile(size, 99), percentile(size, 99.9), '
                     '    min(latency), avg(latency),'
                     '    max(latency), '
                     '    percentile(latency, 10), percentile(latency, 20), '
                     '    percentile(latency, 30), percentile(latency, 40), '
                     '    percentile(latency, 50), percentile(latency, 60), '
                     '    percentile(latency, 70), percentile(latency, 80), '
                     '    percentile(latency, 90), percentile(latency, 95), '
                     '    percentile(latency, 99), percentile(latency, 99.9) '
                     '    FROM logrecs GROUP BY node, request")'],
    'node_req_http': ['node-per-request-per-httpcode analysis',
                      'cur.execute("SELECT node, request, httpcode, count(*), '
                     '    min(size), avg(size), max(size), '
                     '    percentile(size, 10), percentile(size, 20), '
                     '    percentile(size, 30), percentile(size, 40), '
                     '    percentile(size, 50), percentile(size, 60), '
                     '    percentile(size, 70), percentile(size, 80), '
                     '    percentile(size, 90), percentile(size, 95), '
                     '    percentile(size, 99), percentile(size, 99.9), '
                     '    min(latency), avg(latency),'
                     '    max(latency), '
                     '    percentile(latency, 10), percentile(latency, 20), '
                     '    percentile(latency, 30), percentile(latency, 40), '
                     '    percentile(latency, 50), percentile(latency, 60), '
                     '    percentile(latency, 70), percentile(latency, 80), '
                     '    percentile(latency, 90), percentile(latency, 95), '
                     '    percentile(latency, 99), percentile(latency, 99.9) '
                     '    FROM logrecs GROUP BY node, request, httpcode")'],
}

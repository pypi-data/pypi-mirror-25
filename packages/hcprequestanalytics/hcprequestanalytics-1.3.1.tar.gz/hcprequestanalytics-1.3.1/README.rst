HCP request log analytics
=========================

**hcprequestanalytics** reads HTTP access logs from log packages created by
*Hitachi Content Platform* (HCP), loads the content into a SQL database and
runs SQL-queries against it.

Features
--------

It to provides information about topics like:

*   types of requests
*   types of requests to specific HCP nodes
*   types of reuests from specific clients
*   HTTP return codes
*   size distribution of requested objects
*   HCP internal latency distribution
*   clients

It can be easily extended with individual queries (see :doc:`30_queries`).

Results are generated as a multi-sheet XLSX workbook per default; optionally,
CSV files can be requested.

Dependencies
------------

You need to have at least Python 3.5.0 installed to run **hcprequestanalytics**.


Documentation
-------------

To be found at `readthedocs.io <http://hcprequestanalytics.readthedocs.io>`_

Installation
------------

Install **hcprequestanalytics** by running::

    $ pip install hcprequestanalytics


-or-

get the source from
`gitlab.com <https://gitlab.com/simont3/hcprequestanalytics>`_,
unzip and run::

    $ python setup.py install


-or-

Fork at `gitlab.com <https://gitlab.com/simont3/hcprequestanalytics>`_

Contribute
----------

- Source Code: `<https://gitlab.com/simont3/hcprequestanalytics>`_
- Issue tracker: `<https://gitlab.com/simont3/hcprequestanalytics/issues>`_

Support
-------

If you've found any bugs, please let me know via the Issue Tracker;
if you have comments or suggestions, send an email to `<sw@snomis.de>`_

License
-------

The MIT License (MIT)

Copyright (c) 2017 Thorsten Simons (sw@snomis.de)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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

import sys
import csv
import xlsxwriter


class Csv(object):
    """
    A class that handles the generation of CSV files.
    """

    def __init__(self, prefix):
        """
        :param prefix:  the prefix per generated filename
        """
        self.prefix = prefix

    def newsheet(self, name, fieldnames):
        """
        Create a new CSV file.

        :param name:        the files base name
        :param fieldnames:  a list of field names
        """
        fname = self.prefix + '-' + name + '.csv'
        try:
            self.hdl = open(fname, 'w')
        except Exception as e:
            sys.exit('open {} failed - {}'.format(fname ,e))

        self.writer = csv.DictWriter(self.hdl, fieldnames=list(fieldnames))
        self.writer.writeheader()

    def writerow(self, row):
        """
        Write a data row.

        :param row:     a data row, matching the header (dict)
        """
        self.writer.writerow(row)

    def closesheet(self):
        """
        Close the open file.
        """
        self.hdl.close()

    def close(self):
        """
        Close the object.
        """

class Xlsx(Csv):
    """
    A class that handles the generation of an XLXS file.
    """

    def __init__(self, prefix):
        """
        :param prefix:  the prefix per generated filename
        """
        super().__init__(prefix)

        self.wb = xlsxwriter.Workbook('{}-analyzed.xlsx'.format(prefix))
        self.wb.set_properties({'title': 'HCP Request Analytics',
                                'author': 'Thorsten Simons (sw@snomis.de)',
                                'category': 'analytics',
                                'comments': 'see documentation at '
                                            'https://hcprequestanalytics.'
                                            'readthedocs.io',
                                })
        self.bold = self.wb.add_format({'bold': True})
        self.title = self.wb.add_format({'bold': True,
                                         'font_size': 14,
                                         'bg_color': 'yellow',
                                         'bottom': 5})

    def newsheet(self, name, fieldnames):
        """
        Create a new worksheet

        :param name:        the files base name
        :param fieldnames:  a list of field names
        """
        self.fieldnames = fieldnames
        self.row = 0

        self.ws = self.wb.add_worksheet(name=name)

        # write the header
        self.ws.write_row(self.row, 0, fieldnames, self.title)
        # insert a spacer row
        self.ws.set_row(1, 8)
        self.row += 2

    def writerow(self, row):
        """
        Write a data row.

        :param row:     a data row, matching the header
        """
        vals = [row[x] for x in self.fieldnames]

        self.ws.write_row(self.row, 0, vals)
        self.row += 1

    def closesheet(self):
        """
        Close the open file.
        """
        return

    def close(self):
        """
        Close the object.
        """
        self.wb.close()

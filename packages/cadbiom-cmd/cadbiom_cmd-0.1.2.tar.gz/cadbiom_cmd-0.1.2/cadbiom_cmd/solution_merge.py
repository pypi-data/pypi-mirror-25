# -*- coding: utf-8 -*-
# Copyright (C) 2017  IRISA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# The original code contained here was initially developed by:
#
#     Pierre Vignet.
#     IRISA
#     Dyliss team
#     IRISA Campus de Beaulieu
#     35042 RENNES Cedex, FRANCE
from __future__ import unicode_literals
from __future__ import print_function

import glob
import csv
import itertools as it

def merge_cams_to_csv(directory, csvfile='merged_cams.csv'):
    """Merge *cam.txt files from a directory to a csv."""

    # Add dir separator to the end if not present
    directory = directory + '/' if directory[-1] != '/' else directory

    csv_data = list()

    # Read all files in the given directory
    for filename in glob.glob(directory + '*_cam.txt'):
        #print(filename)

        # Extract the formula from the filename
        # ex:
        # # ['./result/Whole NCI-PID database translated into CADBIOM formalism(and)', 'TGFB1', 'cam.txt']
        formula = ''.join(filename.split('_')[1:-1])

        # Read the content of the cam file & memorize this content
        with open(filename) as fd:
            # Add formula column, before each cam to futur csv file
            csv_data.append([[formula] + [line.rstrip('\n')] for line in fd])

    # Write the final csv
    with open(csvfile, 'w') as fd:
        writer = csv.writer(fd, delimiter=str(';'))
        writer.writerows(it.chain(*csv_data))


if __name__ == "__main__":

    merge_cams_to_csv('result')

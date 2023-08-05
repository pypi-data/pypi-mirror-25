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

import os
import glob


def get_solutions(file_descriptor):
    """return a tuple of the original line + the stripped line containing the solution"""

    for line in file_descriptor:
        # Remove possible \t separator from first line (frontier solution)
        line = line.rstrip('\n')
        stripped_line = line.rstrip('\t').replace('\t', ' ')

        # Next Line if empty
        if stripped_line == '':
            continue

        if stripped_line[0] not in ('%', '=', ' '):
            # print(stripped_line)
            # Sort in lower case, remove ' ' empty elements
            yield line, stripped_line


def sort_solutions(path):
    """
    """

    assert os.path.isfile(path) or os.path.isdir(path)

    if os.path.isdir(path):

        path = path if path[-1] == '/' else path + '/'
        [sort_solutions_in_file(file) for file in glob.glob(path + '*cam*')]
    else:
        sort_solutions_in_file(path)


def sort_solutions_in_file(file):
    """Sort all solutions in alphabetical order in place."""

    solutions = dict()

    with open(file, 'r+') as fd:

        for line, stripped_line in get_solutions(fd):
            # Sort in lower case, remove ' ' empty elements
            solutions[line] = \
                " ".join(sorted([place for place in stripped_line.split(' ')
                                 if place != ' '], key=lambda s: s.lower()))

        # Rewind
        fd.seek(0)

        # Load all the content
        file_text = fd.read()

        # Replace old sols with the new
        for original_sol, sorted_sol in solutions.items():
            file_text = file_text.replace(original_sol, sorted_sol)

        # print(file_text)
        # Rewind
        fd.seek(0)

        # Write all text in place
        fd.write(file_text)

################################################################################

def get_cam_lines(file):

        # Return cam lines
        with open(file, 'r+') as fd:
           return {stripped_line for _, stripped_line in get_solutions(fd)}


def make_matrix(path):

    import glob
    from collections import Counter

    if path[-1] != '/':
        path += '/'

    genes = 'COL1A1_gene', 'MMP2_gene', 'MMP9_gene', 'TGFB1_gene', 'TIMP1_gene', 'decorin_gene'

    i = 0
    for file in glob.glob(path + '*cam.txt'):

        i += 1

        patterns = set()

        for cam in get_cam_lines(file):

            patterns.add(frozenset({gene for gene in genes if gene in cam}))


        print('file:', file)
        print(patterns, len(patterns))
#        cnter_of_patterns = Counter(patterns)
#        print(cnter_of_patterns, len(cnter_of_patterns))
        raw_input('pause')

    print("nb files", i)



if __name__ == "__main__":



    make_matrix('./docker_results/')
    exit()


    import glob
    from collections import Counter

    total_cams = list()

    # Get each cams for each file
    for file in glob.glob('./docker_results/*cam.txt'):

        temp_cams = get_cam_lines(file)
        total_cams += list(temp_cams)

        # Print the number of cams for the given file
        print(file, len(temp_cams))


    # Verification of duplicated cams (number > 1)
    print([k for k, v in Counter(total_cams).items() if v != 1])
    print("total cams:", len(total_cams))
    print("len counter", len(Counter(total_cams)))



    # Check new results vs old results for SRP9 cams

    old_cams = get_cam_lines('/media/DATA/Projets/dyliss_tgf/cadbiom/data/pid_and_clock_no_perm_p21corrected_start_SRP9_complete.txt')
    new_cams = get_cam_lines('./bite/Whole NCI-PID database translated into CADBIOM formalism(and)_SRP9_cam.txt')



    print("Anciennes", len(old_cams)) # 317
    print("Nouvelles", len(new_cams)) # 557
    print("Intersection", len(old_cams & new_cams)) # 221

    diff = old_cams - new_cams
    print("Anciennes non retrouvées", len(diff)) # 96
    print("Nouvelles en plus", len(new_cams - old_cams)) # 336
    # print("Anciennes non retrouvées", diff)

    # Get list of lists of frontier places in old cams not found this time
    diff_pb = [problematic_cam.split(' ') for problematic_cam in diff] # Len: 96

    # Common frontier places in problematic cams
    common_frontier_places = set(diff_pb[0]).intersection(*diff_pb)
    # print("Places communes aux solutions non retrouvées", common_frontier_places)
    print("Nombre de places communes aux solutions non retrouvées", len(common_frontier_places)) # 14

    # Résutlat:
    set([u'SRF_nucl', u'ERK1_2', u'STAT5_cy', u'IL2Rgamma_JAK3_intToMb',
    u'IL2Rbeta_JAK1_LCK_intToMb', u'JNK1_2', u'MEKK1', u'ELK1_nucl',
    u'FOS_cy_gene', u'SRP9_gene', u'IL2_glycosylation_exCellRegion',
    u'ceramide_start', u'JUN_gene', u'IL2Ralpha_intToMb_gene'])

    # changement de nom dans chaque solution de l'ancien fichier: ceramide_start > ceramide
    new_ancient_cams = {cam.replace('ceramide_start', 'ceramide') for cam in old_cams}
    print("Anciennes retouchees", len(new_ancient_cams)) # 317 (normal)
    print("Anciennes non retrouvées", len(new_ancient_cams - new_cams)) # 0
    # => tout a été retrouvé



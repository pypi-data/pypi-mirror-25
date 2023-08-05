# -*- coding: utf-8 -*-
"""Unit tests for solver results"""

#from __future__ import unicode_literals
from __future__ import print_function

# Standard imports
import pytest
import tempfile
import os

# Custom imports
from cadbiom_cmd import solution_search


@pytest.fixture()
def feed_output():

    return ['Ax Bx\n'], \
           ['Ax Bx\n', '% h2 h00\n', '% h3\n', '% h0 h1\n', '% hlast\n'], \
           ['4\n']


def test_minigraph1(feed_output):
    """Test the obtention of frontier places & timings on Minigraph 1

    Output must be:

        camp:
            Ax   Bx
        cam complete:
            Ax Bx
            % h2 h00
            % h3
            % h0 h1
            % hlast
        cam step:
            4

    .. note:: Order of trajectories may change. (h2 h00, h3 vs h2, h3 h00)

    .. note:: This test is the equivalent of the following command line:

        cadbiom_cmd -vv debug compute_macs mini_test_publi.bcx Px --steps 10

    .. note:: The test directory is the temporary sytem folder.
    """

    # Create the file model in /tmp/
    # Note: prevent the deletion of the file after the close() call
    fd_model = tempfile.NamedTemporaryFile(suffix='.bcx', delete=False)
    fd_model.write(
        """<model xmlns="http://cadbiom" name="bicluster">
    <CSimpleNode name="Ax" xloc="0.156748911466" yloc="0.673568818514"/>
    <CSimpleNode name="n1" xloc="0.291727140784" yloc="0.673568818514"/>
    <CSimpleNode name="C1" xloc="0.404208998548" yloc="0.618757612668"/>
    <CSimpleNode name="n2" xloc="0.405660377359" yloc="0.722289890377"/>
    <CSimpleNode name="Px" xloc="0.577083086261" yloc="0.722140333368"/>
    <CSimpleNode name="Bx" xloc="0.157474600871" yloc="0.83922046285"/>
    <CSimpleNode name="n3" xloc="0.290570367401" yloc="0.803822907245"/>
    <CSimpleNode name="n4" xloc="0.292715433748" yloc="0.906099768906"/>
    <CSimpleNode name="C2" xloc="0.409124108889" yloc="0.803710739487"/>
    <CSimpleNode name="C3" xloc="0.408336298212" yloc="0.906099768906"/>
    <transition name="" ori="Ax" ext="n1" event="h00" condition="" action="" fact_ids="[]"/>
    <transition name="" ori="n1" ext="C1" event="h0" condition="" action="" fact_ids="[]"/>
    <transition name="" ori="n1" ext="n2" event="h1" condition="C2" action="" fact_ids="[]"/>
    <transition name="" ori="n2" ext="Px" event="hlast" condition="C1 and not C3" action="" fact_ids="[]"/>
    <transition name="" ori="Bx" ext="n3" event="h2" condition="" action="" fact_ids="[]"/>
    <transition name="" ori="Bx" ext="n4" event="h4" condition="" action="" fact_ids="[]"/>
    <transition name="" ori="n3" ext="C2" event="h3" condition="" action="" fact_ids="[]"/>
    <transition name="" ori="n4" ext="C3" event="h5" condition="" action="" fact_ids="[]"/>
    </model>"""
    )
    fd_model.close()

    # Build params
    # See the docstring for the normal command line in shell context
    params = {
        'all_macs': False,
        'chart_file': fd_model.name, # Filename + path
        'combinations': False,
        'continue': False,
        'final_prop': 'Px',
        'input_file': None,
        'inv_prop': None,
        'output': tempfile.gettempdir() + '/',
        'start_prop': None,
        'steps': 10,
        'verbose': 'debug',
    }

    # Launch the search of the minimal accessibility condition
    solution_search.launch_researchs(params)


    with open(fd_model.name[:-4] + "_Px_cam.txt", 'r') as file:
        found = [line for line in file]
        assert found == feed_output[0]

    with open(fd_model.name[:-4] + "_Px_cam_complete.txt", 'r') as file:
        found = [line for line in file]
        assert found == feed_output[1]

    with open(fd_model.name[:-4] + "_Px_cam_step.txt", 'r') as file:
        found = [line for line in file]
        assert found == feed_output[2]

    # Delete temp files
    os.remove(fd_model.name)
    os.remove(fd_model.name[:-4] + "_Px_cam.txt")
    os.remove(fd_model.name[:-4] + "_Px_cam_complete.txt")
    os.remove(fd_model.name[:-4] + "_Px_cam_step.txt")


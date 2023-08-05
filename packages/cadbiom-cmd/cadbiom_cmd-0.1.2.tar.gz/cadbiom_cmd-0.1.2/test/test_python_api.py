# -*- coding: utf-8 -*-
"""Unit tests for Python API"""

from __future__ import unicode_literals
from __future__ import print_function


# Standard imports
import pytest

@pytest.fixture()
def feed_logical_formula():

    frontier_places = {tuple(('A', 'B')), tuple(('AB', 'CD'))}

    return frontier_places

def test_make_logical_formula(feed_logical_formula):

    from cadbiom_cmd.solution_search import make_logical_formula

    found = make_logical_formula(feed_logical_formula, None)
    assert found == "not(((AB and CD) or (A and B)))"


    found = make_logical_formula(feed_logical_formula, 'START_PROP')
    assert found == "START_PROP and (not(((AB and CD) or (A and B))))"

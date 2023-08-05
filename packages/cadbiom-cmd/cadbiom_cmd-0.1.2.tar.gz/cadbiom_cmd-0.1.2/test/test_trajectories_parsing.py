# -*- coding: utf-8 -*-
"""Unit tests for Python API"""

from __future__ import unicode_literals
from __future__ import print_function

# Library imports
from cadbiom.models.biosignal.translators.gt_visitors import compile_cond
from cadbiom.models.guard_transitions.analyser.ana_visitors import TableVisitor
from cadbiom.models.biosignal.sig_expr import *

# Standard imports
import pytest

@pytest.fixture()
def feed_conditions():

    # {condition: (inhibitors, paths),}
    conditions = \
        {
            "((((CXCL10_CXCR3_intToMb and not(CCL11_CXCR3_intToMb)))or((CXCL10_CXCR3_intToMb and not(CXCL13_CXCR3_intToMb))))or(CXCL9_11_CXCR3_active_intToMb))or(CXCL4_CXCR3_intToMb)": ({'CCL11_CXCR3_intToMb', 'CXCL13_CXCR3_intToMb'}, [['CXCL10_CXCR3_intToMb', 'CCL11_CXCR3_intToMb'], ['CXCL10_CXCR3_intToMb', 'CXCL13_CXCR3_intToMb'], ['CXCL9_11_CXCR3_active_intToMb'], ['CXCL4_CXCR3_intToMb']]),
            "((((A and not(B)))or((A and not(C))))or(D))or(E)": ({'B', 'C'}, [['A', 'B'], ['A', 'C'], ['D'], ['E']]),
            "(A and not(B))": ({'B'}, [['A', 'B']]),
            "(((((A)or(B))or(C))or(B))or(D))or(E)": (set(), [['A'], ['B'], ['C'], ['B'], ['D'], ['E']]),
            "((((not(ATF2_JUND_macroH2A_nucl))or(Fra1_JUND_active_nucl))or(Fra1_JUN_active_nucl))or(TCF4_betacatenin_active_nucl))or(JUN_FOS_active_nucl)": ({'ATF2_JUND_macroH2A_nucl'}, [['ATF2_JUND_macroH2A_nucl'], ['Fra1_JUND_active_nucl'], ['Fra1_JUN_active_nucl'], ['TCF4_betacatenin_active_nucl'], ['JUN_FOS_active_nucl']]),
            "((A and B and C)) and (not((D and E and F and G)))": ({'E', 'D', 'G', 'F'}, [['A', 'B', 'C', 'D', 'E', 'F', 'G']]),
        }

    return conditions


def test_rec_tree(feed_conditions):

    from cadbiom_cmd.solution_repr import rec, Reporter

    # Error Reporter
    err = Reporter()
    tvi = TableVisitor(err)
    symb_tab = tvi.tab_symb


    for condition, solution in feed_conditions.items():
        inhibitors_nodes, paths = solution

        # Get tree object from condition string
        cond_sexpr = compile_cond(condition, symb_tab, err)
        # Get all possible paths from the condition
        found_inhibitors = set()
        found_paths = rec(cond_sexpr, found_inhibitors)
        # print(found_inhibitors)
        # print(found_paths)

        assert found_paths == paths
        assert found_inhibitors == inhibitors_nodes


def test_parse_condition():

    from cadbiom_cmd.solution_repr import parse_condition

    condition = "((((((STAT4__dimer___JUN_Cbp_active_nucl)or(JUN_FOSNFAT1_c_4_active_nucl))or((STAT5__dimer___active_active_nucl and Elf1)))or(IL2_IL2R_active_intToMb))or(JUN_FOSNFAT1_c_4_active_nucl))or(NFAT1_FOXP3))or(JUN_FOSNFAT1_c_4_active_nucl)"
    inhibitors = set()
    all_nodes = set(['JUN_FOSNFAT1_c_4_active_nucl', 'FOS_active_p_p_p_p_cy', 'JUN_nucl_gene', 'SRP9', 'ELK1_nucl', 'JUN_active_p_p_nucl', '14_3_3family_BAD_CaM_Ca2PLUS_CalcineurinAalpha_betaB1', 'IL2_glycosylation_exCellRegion', 'JUN_nucl', '14_3_3family', 'ERK1_2', 'STAT5_cy', 'FOS_cy', u'TGFB1__dimer___active_exCellRegion', 'NFAT1_c_4_inactive1_inactive_cy', u'SRF_nucl', 'ERK1_2_active_active_nucl', 'ERK1_2_active_active', 'ELK1_active_p_p_p_p_p_nucl', 'CaM_Ca2PLUS_CalcineurinAalpha_betaB1_active', 'FOS_cy_gene', u'PKCzeta', 'IL2Ralpha_intToMb_gene', 'IL2_IL2Ralpha_beta_gamma_JAK1_LCK_JAK3_active_intToMb', 'IL2Rgamma_JAK3_intToMb', 'STAT5__dimer___active_active_nucl', 'NFAT1_c_4_active_active_nucl', 'IL2Rbeta_JAK1_LCK_intToMb', 'SRP9_gene', 'IL2Ralpha_intToMb', 'BAD_mi', 'FOS_active_p_p_p_p_nucl'])


    found_valid_path = parse_condition(condition, all_nodes, inhibitors)

    assert found_valid_path == set([('JUN_FOSNFAT1_c_4_active_nucl',)])
    assert inhibitors == set()

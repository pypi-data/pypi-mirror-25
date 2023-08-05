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

# Standard imports
import datetime as dt
from collections import defaultdict
import networkx as nx
import itertools as it
import re
import json
from logging import DEBUG
# Remove matplotlib dependency
# It is used on demand during the drawing of a graph
try:
    import matplotlib.pyplot as plt
except ImportError:
    pass

# Library imports
from cadbiom.models.guard_transitions.translators.chart_xml \
    import MakeModelFromXmlFile
from cadbiom.models.biosignal.translators.gt_visitors import compile_cond, compile_event
from cadbiom.models.guard_transitions.analyser.ana_visitors import TableVisitor
from cadbiom.models.biosignal.sig_expr import *
from cadbiom.models.guard_transitions.analyser.ana_visitors import SigExpIdCollectVisitor

import cadbiom.commons as cm

LOGGER = cm.logger()

"""
Bx  Ax
% h2 h00
% h3
% h0 h1
% hlast
Bx  Ax
% h2
% h3 h00
% h0 h1
%
% hlast
Bx  Ax
% h2
% h3 h00
% h0 h1
% hlast
%
%
Bx  Ax
% h2 h00
% h3
% h0 h1
% hlast
%
%
%
"""

class Reporter(object):
    """Error reporter.

    .. note:: Link the lexer to the model allows to avoid error in Reporter
        like:  "-> dec -> Undeclared event or state"
        In practice this is time consuming and useless for what we want to do.
        See parse_condition()
    """

    def __init__(self):
        self.error = False
        self.mess = ""
        pass

    def display(self, e):
        self.error = True
        if "Undeclared event or state" not in e:
            LOGGER.debug("\t" + self.mess + " -> " + e)


def load_solutions(file):
    """Open a file with many solution/MACs.

    :param: File name
    :type: <str>
    :return:A tuple of "frontier places" and a list of events in each step.
        ("Bx Ax", [[u'h2', u'h00'], [u'h3'], [u'h0', u'h1'], [u'hlast']])
    :rtype: <tuple <str>, <list>>
    """

    sol_steps = defaultdict(list)
    sol = ""
    with open(file, 'r') as fd:
        for line in fd:
            LOGGER.debug("Load_solutions :: line: " + line)
            # Remove possible \t separator from first line (frontier solution)
            line = line.rstrip('\n').rstrip('\t').replace('\t', ' ')
            # TODO: remove last space ' ' => beware, may be informative...
            # (start transitions have no event names: ori="__start__0")
            line = line.rstrip(' ')
            if line == '' or line[0] == '=':
                # Blank line
                # Skip blank lines and solution separator in some files (=====)
                continue
            elif line[0] != '%':
                if sol == line:
                    # Same frontier places
                    yield sol, sol_steps[sol]

                    # reinit sol
                    sol_steps[sol] = list()
                    continue
                elif sol == '':
                    # First sol
                    sol = line
                else:
                    # Yield previous sol
                    yield sol, sol_steps[sol]
                    sol = line

            elif line[0] == '%':
                # Remove step with only "% "
                step = line.lstrip('% ')

                if step != '':
                    sol_steps[sol].append(step.split(' '))

        # Yield last sol
        yield sol, sol_steps[sol]


def get_transitions(file, all_places=False):
    """Get all transitions in a file model (bcx format).

    :param: Model in bcx format.
    :type: <str>
    :return: A dictionnary of events as keys, and transitions as values.
        Since many transitions can define an event, values are lists.
        Each transition is a tuple with: origin node, final node, attributes
        like label and condition.
        {u'h00': [('Ax', 'n1', {u'label': u'h00[]'}),]
    :rtype: <dict <list <tuple <str>, <str>, <dict <str>: <str>>>>
    """

    parser = MakeModelFromXmlFile(file)

#    print(dir(parser))
#    print(type(parser))
    #<type 'instance'>
    #['__doc__', '__init__', '__module__', 'get_model', 'handler', 'model', 'parser'

    g = (trans for transition in parser.handler.top_pile.transitions
         for trans in transition)

    transitions = defaultdict(list)

    for trans in g:

        # Get the names of clocks
        # Some event have many clocks (like _h_2755) for the same
        # ori/ext entities, so we have to extract them and their respective
        # conditions
        if trans.event == '':
            # null event without clock...
            # Avoids having SigConstExpr as event type in parse_event()
            continue
        elif re.match('_h_[0-9_\.]+', trans.event):
            # 1 event (with 1 clock)
            events = {trans.event: trans.condition}
        else:
            # Many events (with many clocks with condition(s))
            events = parse_event(trans.event)

        for event, condition in events.iteritems():
            # LOGGER.debug("NEW trans", event)

            # Handle multiple transitions for 1 event
            transitions[event].append(
                (
                    trans.ori.name, trans.ext.name,
                    {
                        'label': event, #+ '[' + trans.condition + ']',
                        'condition': condition,
                    }
                )
            )

    LOGGER.info("{} transitions loaded".format(len(transitions)))
    # Return a dict instead of defaultdict to avoid later confusions
    #(masked errors) by searching a transition that was not in the model...

    assert len(transitions) != 0, "No transitions found in the model ! " \
        "Please check the names of events (_h_xxx)"

    if all_places:
        # Return all nodes
        return dict(transitions), parser.handler.node_dict.keys()

    return dict(transitions)


def get_frontier_places(transitions, all_places):
    """Return frontier places of a model (deducted from its transitions).

    :param arg1: Model's transitions.
        {u'h00': [('Ax', 'n1', {u'label': u'h00[]'}),]
    :type arg1: <dict>
        keys: names of events
        values: list of transitions as tuples (with in/output, and label).
    :return: Set of frontier places.
    :rtype: <set>
    """

    # Get transitions in events
    g = tuple(trans for event in transitions.values() for trans in event)

    # Get input nodes & output nodes
#    input_places = {trans[0] for trans in g}
    output_places = {trans[1] for trans in g}

    # Get all places that are not in transitions in the "output" place
    return set(all_places) - output_places


def rec(tree, inhibitors_nodes):
    """

    tree = ('H', 'v', (
        ('F', 'v', 'G'),
        '^',
        (
            ('A', 'v', 'B'),
            '^',
            ('C', 'v', ('D', '^', 'E'))
        )
    ))
    """

#    print("TREE", tree, type(tree), dir(tree))

    if isinstance(tree, str):  # terminal node
        path = [tree]
        solutions = [path]
        return solutions
    if isinstance(tree, SigNotExpr):
        LOGGER.debug("NOT OPERAND: {}, {}".\
            format(
                tree.operand,
                type(tree.operand)
            )
        )
        try:
            current_inhibitors = get_places_from_condition(tree.operand.__str__())
            inhibitors_nodes.update(current_inhibitors)
            LOGGER.debug("INHIBITORS found: " + str(current_inhibitors))

            path = [tree.operand.name]
            solutions = [path]
            return solutions
        except AttributeError:
            tree = tree.operand

    if isinstance(tree, SigIdentExpr):
        path = [tree.name]
        solutions = [path]
        return solutions



    lch = tree.left_h
    op  = tree.operator
    rch = tree.right_h
#    print('OZCJSH:', lch, op, rch, sep='\t\t')
    lpaths = rec(lch, inhibitors_nodes)
    rpaths = rec(rch, inhibitors_nodes)
#    print('VFUENK:', lpaths, rpaths)
    if op == 'or':  # or
#        ret = [*lpaths, *rpaths]
        ret = list(it.chain(lpaths, rpaths))
#        print('RET:', ret)
        return ret
    else:  # and
        assert op == 'and'
#        print(list(it.product(lpaths, rpaths)))
#        raw_input('test')

        ret = list(l + r for l, r in it.product(lpaths, rpaths))
#        print('RET:', ret)
        return ret


def get_places_from_condition(condition):
    """Parse condition string and return all places, regardless of operators.

    .. note:: This function is only used to get all nodes in a condition when
        we know they all are inhibitors nodes.

    :param: Condition string.
    :type: <str>
    :return: Set of places.
    :rtype: <set>
    """

    replacement = ['and', 'or', 'not', '(', ')']

    for chr in replacement:
        condition = condition.replace(chr, ' ')

    # Must be exempt of unauthorized chars
    return {elem for elem in condition.split(' ')
            if elem != ''}


def parse_condition(condition, all_nodes, inhibitors_nodes):
    """Return valid paths according the given logical formula and nodes.

    """

    LOGGER.debug("CONDITION: " + condition)
    # Error Reporter
    err = Reporter()
    tvi = TableVisitor(err)
    # Link the lexer to the model allows to avoid error in Reporter
    # like:  "-> dec -> Undeclared event or state"
    # In practice this is time consuming and useless for what we want to do
    #parser = MakeModelFromXmlFile(BIO_MOLDELS_DIR + "Whole NCI-PID database translated into CADBIOM formalism(and).bcx")
    #parser.get_model().accept(tvi)
    symb_tab = tvi.tab_symb
    # Get tree object from condition string
    cond_sexpr = compile_cond(condition, symb_tab, err)
    # Get all possible paths from the condition
    possible_paths = rec(cond_sexpr, inhibitors_nodes)

    # Prune possible paths according to:
    # - Inhibitor nodes that must be removed because they will never
    # be in the graph.
    # - All nodes in transitions (ori -> ext) because we know all transitions
    # in the graph, so we know which entities can be choosen to validate a path.
    # - All frontier places, that are known entities that can be in conditions
    # (not only in ori/ext) of transitions.
    # So: authorized nodes = frontier_places + transition_nodes - inhibitor nodes
    valid_paths = {tuple(path) for path in possible_paths
                   if (set(path) - inhibitors_nodes).issubset(all_nodes)}

    # Debugging only
    if LOGGER.getEffectiveLevel() == DEBUG:
        LOGGER.debug("INHIBIT NODES: " + str(inhibitors_nodes))
        LOGGER.debug("ALL NODES: " + str(all_nodes))
        LOGGER.debug("POSSIBLE PATHS: " + str(possible_paths))
        LOGGER.debug("VALID PATHS: " + str(valid_paths))

        for path in possible_paths:
            pruned_places = set(path) - inhibitors_nodes
            isinsubset = pruned_places.issubset(all_nodes)
            LOGGER.debug(
                "PRUNED PATH: {}, VALID: {}".format(
                    pruned_places,
                    isinsubset
                )
            )

    assert len(valid_paths) > 0, "No valid path for: " + str(condition)
    if len(valid_paths) > 1:
        LOGGER.warning("Multiple valid paths for: {}:\n{}".format(condition,
                                                                  valid_paths))
    return valid_paths


    # condition expressions contains only node ident
    icv = SigExpIdCollectVisitor()
    lst1 = cond_sexpr.accept(icv)
    print(cond_sexpr)
    print(type(cond_sexpr))
    print(dir(cond_sexpr))
    print("LISTE", lst1)
#    <class 'cadbiom.models.biosignal.sig_expr.SigSyncBinExpr'>
#    'accept', 'get_signals', 'get_ultimate_signals', 'is_bot', 'is_clock',
# 'is_const', 'is_const_false', 'is_ident', 'left_h', 'operator', 'right_h', 'test_equal']

    print(cond_sexpr.get_signals())
#    print(cond_sexpr.get_ultimate_signals())
    print("LEFT", cond_sexpr.left_h)
    print("OPERATOR", cond_sexpr.operator)
    print("RIGHT", cond_sexpr.right_h)


#    ret = treeToTab(cond_sexpr)
#    [set([('((formule', True)])]
#    print("treeToTab", ret)
#    print(type(ret))
#    print(dir(ret))


def parse_event(event):
    """Decompile logical formula in event's name.

    :param: Event string.
    :type: <event string>
    :return: A dict of events and their conditions.
    :rtype: <dict>
        keys: event's names; values: logical formula attached (condition)
    """

    def treeToExprDefaultsList(tree):
        if isinstance(tree, SigDefaultExpr):
            return treeToExprDefaultsList(tree.left_h) + \
                treeToExprDefaultsList(tree.right_h)

        else:
            # Here, some tree are from classes SigConstExpr or SigIdentExpr
            # Ex: for the clock "_h_5231":
            #    ... default (_h_5231)" => No condition for this event
            # Other examples:
            # _h_2018 _h_820 _h_4939 _h_5231 _h_3301 _h_4967 _h_2303 _h_3301
            return [tree]

    def filterSigExpression(expr):
        """
        .. note:: No SigConstExpr here => filtered in get_transitions()
            by checking null events (event="") in the model.
        """

        if isinstance(expr, SigWhenExpr):
            # right : SigSyncBinExpr (logical formula), BUT
            # sometimes SigConstExpr (just a True boolean) when clock is empty
            # Ex: "when ()"
            # So, we replace this boolean with an empty condition
            right = '' if isinstance(expr.right_h, SigConstExpr) \
                        else str(expr.right_h)

            return expr.left_h.name, right

        if isinstance(expr, SigIdentExpr):
            return expr.name, ''

        raise AssertionError("You should never have been there ! "
                             "Your expression type is not yet supported...")

#    def filterSigExpression(listOfExpr):
#        return [filterSigExpression(expr) for expr in listOfExpr]

    # Error Reporter
    err = Reporter()
    tvi = TableVisitor(err)
    symb_tab = tvi.tab_symb

    # Get tree object from event string
    event_sexpr = compile_event(event, symb_tab, True, err)[0]

    # Filter when events
    g = (filterSigExpression(expr) \
         for expr in treeToExprDefaultsList(event_sexpr))
    eventToCondStr = \
        {event_name: event_cond for event_name, event_cond in g}


    LOGGER.debug("Clocks from event parsing: " + str(eventToCondStr))

    return eventToCondStr


def build_graph(solution, steps, transitions):
    """Build a graph for the given solution.

        - Get & make all needed edges
        - Build graph

    :param arg1: Frontier places.
    :param arg2: List of steps (with events in each step).
    :param arg3: A dictionnary of events as keys, and transitions as values
        (see get_transitions()).
    :type arg1: <str>
    :type arg2: <list <list>>
    :type arg3: <dict <list <tuple <str>, <str>, <dict <str>: <str>>>>
    :return:
        - Networkx graph object.
        - Nodes corresponding to transitions with conditions.
        - All nodes in the model
        - Edges between transition node and nodes in condition
        - Normal transitions without condition
    :rtype: <networkx.classes.digraph.DiGraph>, <list>, <list>, <list>, <list>
    """

    def filter_transitions(step_event):
        """ Insert a transittion in a transition event if there is a condition.

        => Insert a node in a edge.
        => Link all nodes involved in the condition with this new node.

        :param: A list of events (transitions) (from a step in a solution).
            [('Ax', 'n1', {u'label': u'h00[]'}),]
        :type: <tuple>
        :return: Fill lists of edges:
            edges_with_cond: link to a transition node for
                transition with condition.
            transition_nodes: add new nodes corresponding to transitions with
                conditions.
            edges_in_cond: Add all edges to nodes linked to a transition
                via the condition (group of nodes involved in the path
                choosen by the solver).
            edges: transition untouched if there is no condition.
        :rtype: None
        """
        assert len(step_event) != 0 # Todo: useful ?

        inhibitors_nodes = set() # Inactivated nodes in paths of conditions
        input_places = {trans[0] for trans in step_event}

        # Color nodes
        # Since we explore all possible paths for each condition,
        # some edges are rewrited multiple times.
        # => included edges between origin <=> transition node
        # These edges must be grey while, edges between a node that is
        # only in a condition and a transition node must be green.
        # => notion of activator vs inhibitor vs normal input/output node
        def color_map(node):
            # print("color for:", node)
            if node in inhibitors_nodes: # Test first (see cond below)
                return 'red'
            if node in input_places: # some /all frontier places are in this set
                return 'grey'
            else:
                return 'green'


        for trans in step_event:
            attributes = trans[2]
            ori = trans[0]
            ext = trans[1]
            event = attributes['label'].split('[')[0]

            # If there is a condition formula associated to this clock
            if attributes['condition'] != '':

                # Add the transition as node
                transition_nodes.append(
                    (
                        event,
                        {
                            'label': attributes['label'],
                            'name': attributes['label'],
                            'color': 'blue',
                            'condition': attributes['condition'],
                        }
                    )
                )

                # Origin => transition node
                edges_with_cond.append(
                    (
                        ori, event,
                        {
                            'label': ori + '-' + event,
                        }
                    )
                )

                # Transition node => ext
                edges_with_cond.append(
                    (
                        event, ext,
                        {
                            'label': event + '-' + ext,
                        }
                    )
                )

                # Add all transitions to nodes linked via the condition
                valid_paths = parse_condition(
                    attributes['condition'],
                    all_nodes,
                    inhibitors_nodes
                )
                for i, path in enumerate(valid_paths):
                    for node in path:
                        edges_in_cond.append(
                            (
                                node, event,
                                {
                                    'label': '{} ({})'.format(
                                        event,
                                        i
                                    ),
#                                    'label': '{} [{}] ({})'.format(
#                                        event,
#                                        ', '.join(path),
#                                        i
#                                    ), #node + '-' + event,
                                    'color': color_map(node),
                                }
                            )
                        )
            else:
                # Normal edges
                edges.append(trans)


    # Get & make all needed edges ##############################################
    LOGGER.debug("BUILD GRAPH FOR SOL: " + str(solution))
    LOGGER.debug("STEPS: " + str(steps))
#
#    print(transitions['_h_2755'])
#    print(transitions['_h_4716'])
#    print(transitions['_h_2206'])
#    print(transitions['_h_3426'])
#    exit()

    frontier_places  = solution.split(' ')
    edges_with_cond  = list() # Edges between ori <-> transition node <-> ext
    edges_in_cond    = list() # Edges between transition node and nodes in condition
    transition_nodes = list() # Nodes inserted because of condition in transition
    edges            = list() # Normal transitions without condition

    # Get all nodes in all transitions (origin & ext)
    all_transitions = (transitions[step_event] for step_event in it.chain(*steps))
    transitions_ori_ext = (tuple((trans[0], trans[1])) for trans in it.chain(*all_transitions))
    all_nodes = set(it.chain(*transitions_ori_ext)) | set(frontier_places)

    # Parse all conditions in transitions;
    # add nodes in conditions and transition nodes
    [filter_transitions(transitions[step_event])
        for step_event in it.chain(*steps)]

#    print("edges without cond", edges)
#    print("edges with cond", edges_with_cond)
#    print("transition nodes added", transition_nodes)
#    raw_input("PAUSE")

    # Make Graph ###############################################################
    G = nx.DiGraph()
    # Add all nodes (some frontier places are in this set)
    G.add_nodes_from(all_nodes, color='grey')
    # Add fontier places
    G.add_nodes_from(frontier_places, color='red')
    # Add all transition nodes
    G.add_nodes_from(transition_nodes, color='blue')

    # Node attribute ?
    # print(G.node['h1'])

    # Add all edges
    G.add_edges_from(edges)
    G.add_edges_from(edges_with_cond)
    G.add_edges_from(edges_in_cond)

    return G, transition_nodes, all_nodes, edges_in_cond, edges


def draw_graph(output_dir, solution, solution_index, G,
               transition_nodes, all_nodes,
               edges_in_cond, edges,
               matplotlib_export=False):
    """Draw graph with colors and export it to graphml format.

    .. note:: Legend:
        - red: frontier places (in solution variable),
        - white: middle edges,
        - blue: transition edges

    :param arg1: Solution string (mostly a set of frontier places).
    :param arg2: Index of the solution in the Cadbiom result file
        (used to distinguish exported filenames).
    :param arg3: Networkx graph object.
    :param arg4: Nodes corresponding to transitions with conditions.
    :param arg5: All nodes in the model
    :param arg6: Edges between transition node and nodes in condition
    :param arg7: Normal transitions without condition
    :type arg1: <str>
    :type arg2: <int> or <str>
    :type arg3: <networkx.classes.digraph.DiGraph>
    :type arg4: <list>
    :type arg5: <list>
    :type arg6: <list>
    :type arg7: <list>
    """

    # Drawing ##################################################################
    # draw_circular(G, **kwargs) On a circle.
    # draw_random(G, **kwargs)   Uniformly at random in the unit square.
    # draw_spectral(G, **kwargs) Eigenvectors of the graph Laplacian.
    # draw_spring(G, **kwargs)   Fruchterman-Reingold force-directed algorithm.
    # draw_shell(G, **kwargs)    Concentric circles.
    # draw_graphviz(G[, prog])   Draw networkx graph with graphviz layout.
    unzip = lambda l: list(zip(*l))

    pos = nx.circular_layout(G)

    # Legend of conditions in transition nodes
    if matplotlib_export:
        f = plt.figure(1)
        ax = f.add_subplot(1,1,1)
        text = '\n'.join(
            node_dict['label'] for node_dict in unzip(transition_nodes)[1]
        )
        ax.text(0, 0, text, style='italic', fontsize=10,
                bbox={'facecolor':'white', 'alpha':0.5, 'pad':10})

    # Draw nodes:
    # - red: frontier places (in solution variable),
    # - white: middle edges,
    # - blue: transition edges
    frontier_places  = set(solution.split(' '))
    def color_map(node):
        # print("color for:", node)
        if node in frontier_places: # Test first (see cond below)
            return 'red'
        if node in unziped_transition_nodes:
            return 'blue'
        if node in all_nodes: # some /all frontier places are in this set
            return 'grey'
        else:
            return 'white'

    # Get a list of transition nodes (without dictionnary of attributes)
    unziped_transition_nodes = unzip(transition_nodes)[0]

    # Color nodes
    colors = [color_map(node) for node in G.nodes_iter()]
    if matplotlib_export:
        nx.draw(G, pos=pos, with_labels=True,
                node_color=colors, node_size=1000, alpha=0.5, ax=ax)
    else:
        nx.draw(G, pos=pos, with_labels=True,
                node_color=colors, node_size=1000, alpha=0.5)

    # Draw edges involved in transitions with conditions
    edges_colors = [edge[2]['color'] for edge in edges_in_cond]
    nx.draw_networkx_edges(G, pos, edgelist=edges_in_cond,
                           edge_color=edges_colors, width=2, alpha=0.5)

    # Draw labels for normal transitions (move pos to the end of the arrow)
    # ex: [('Ax', 'n1', {u'condition': u'', u'label': u'h00[]'}),]
    edges_labels = {(edge[0], edge[1]): edge[2]['label'] for edge in edges}
    nx.draw_networkx_edge_labels(G, pos, edges_labels, label_pos=0.3)

    # Save & show
    date = dt.datetime.now().strftime("%H-%M-%S")
    if matplotlib_export:
        plt.legend()
        plt.savefig(
            output_dir + date + '_' + solution[:75] + ".svg",
            format="svg")
        plt.show()

    nx.write_graphml(
        G,
        "{}{}_{}_{}.graphml".format(
            output_dir, date, solution_index, solution[:75]
        )
    )


def process_solutions(output_dir, sol_steps, transitions):
    """Build a graph per solution"""

    for sol_index, (sol, steps) in enumerate(sol_steps):

        draw_graph(output_dir, sol, sol_index,
                   *build_graph(sol, steps, transitions)
        )


def test_main():
    """Test"""

    # chart_model.py
    # chart_xml.py
    parser = MakeModelFromXmlFile(BIO_MOLDELS_DIR + "mini_test_publi.bcx")
    print(type(parser.parser))
    print(dir(parser))
    print("HANDLER")
    print(dir(parser.handler))
    print(dir(parser.parser))
    print(dir(parser.get_model()))
    print("ICI")
#    print(parser.get_model().get_simple_node())
    print(parser.handler.node_dict)
    print(parser.handler.top_pile)
    print(parser.handler.pile_dict)
    print(parser.handler.transition.event)
    print(type(parser.handler.top_pile))

    transitions = dict()
    for transition in parser.handler.top_pile.transitions:
        # print(type(transition)) => list
        for trans in transition:
            # 'action', 'activated', 'clean', 'clock', 'condition', 'event',
            # 'ext', 'ext_coord', 'fact_ids', 'get_influencing_places',
            # 'get_key', 'is_me', 'macro_node', 'name', 'note', 'ori',
            # 'ori_coord', 'remove', 'search_mark', 'selected', 'set_action',
            # 'set_condition', 'set_event', 'set_name', 'set_note'

# {'name': '', 'clock': None, 'selected': False, 'activated': False,
# 'search_mark': False, 'note': '', 'ext': <cadbiom.models.guard_transitions.chart_model.CSimpleNode object at 0x7f391c7406d0>,
# 'ext_coord': 0.0, 'ori': <cadbiom.models.guard_transitions.chart_model.CSimpleNode object at 0x7f391c740650>,
# 'action': u'', 'macro_node': <cadbiom.models.guard_transitions.chart_model.CTopNode object at 0x7f391c7db490>,
# 'ori_coord': 0.0, 'event': u'h5', 'condition': u'', 'fact_ids': []}
            # print(dir(trans))
            print("NEW trans", trans.event)
#            print(trans.__dict__)
#            print(trans.name, trans.clock, trans.selected, trans.activated,
#                  trans.search_mark, trans.note, trans.ext, trans.ext_coord,
#                  trans.ori, trans.action, trans.macro_node, trans.ori_coord,
#                  trans.event, trans.condition, trans.fact_ids
#                  )

            transitions[trans.event] = trans.condition

#print("ORI", trans.ori.__dict__)
#{'name': 'n4', 'yloc': 0.906099768906, 'selected': False,
#'father': <cadbiom.models.guard_transitions.chart_model.CTopNode object at 0x7f09eed91490>,
#'xloc': 0.292715433748, 'search_mark': False, 'was_activated': False,
#'incoming_trans': [<cadbiom.models.guard_transitions.chart_model.CTransition object at 0x7f09eecf67d0>],
#'model': <cadbiom.models.guard_transitions.chart_model.ChartModel object at 0x7f09ef2cf3d0>,
#'outgoing_trans': [<cadbiom.models.guard_transitions.chart_model.CTransition object at 0x7f09eecf6850>],
#'activated': False, 'hloc': 1.0}
            print("ORI", trans.ori.name)
            try:
                print("ori INCO", [(tr.event, tr.condition) for tr in trans.ori.incoming_trans])
            except: pass
            try:
                print("ori OUTGO", [(tr.event, tr.condition) for tr in trans.ori.outgoing_trans])
            except: pass
            print("EXT", trans.ext.name)
            try:
                print("ext INCO", [(tr.event, tr.condition) for tr in trans.ext.incoming_trans])
            except: pass
            try:
                print("ext OUTGO", [(tr.event, tr.condition) for tr in trans.ext.outgoing_trans])
            except: pass
    print(transitions)



def sol_digging(sol_steps, transitions):
    """Get steps and all transitions and write all data for each step in a file.

    This is an exemple to quickly search all transition attributes involved in a
    complete MAC.

    .. note:: Output file: output.txt

    :param arg1: List of steps involved in a solution. See load_solutions().
    :param arg2: A dictionnary of events as keys, and transitions as values.
        Since many transitions can define an event, values are lists.
        Each transition is a tuple with: origin node, final node, attributes
        like label and condition.
        {u'h00': [('Ax', 'n1', {u'label': u'h00[]'}),]
        See get_transitions().
    :type arg1: <list>
    :type arg2: <dict <list <tuple <str>, <str>, <dict <str>: <str>>>>
    """

    def write_transition_def(step_event):
        """Write each event on a new line"""

        # Many transitions per event (ex: complex dissociation)
        for trans in step_event:

            # ori="JUN_nucl_gene" ext="JUN_nucl" event="_h_391"
            line = 'ori="{}" ext="{}" event="{}" condition="{}"'.format(
                trans[0],
                trans[1],
                trans[2]['label'].split('[')[0],
                trans[2]['condition']
            )
            fd.write(line + '\n')


    with open("output.txt", "w") as fd:
        for sol, steps in sol_steps:

            # Solution header
            fd.write(sol + '\n')

            for step in steps:

                for event in step:

                    step_event = transitions[event]
                    # print(step_event)
                    if len(step_event) == 0:
                        fd.write("ERROR for event: " + event + '\n')
                    else:
                        write_transition_def(transitions[event])

                # Step separation
                fd.write('\n')
            # Sol separation
            fd.write('\n====================================================\n')


def main(output_dir, model_file, solution_file):
    """Entry point for parse_trajectories"""

    process_solutions(
        output_dir,
        load_solutions(solution_file),
        get_transitions(model_file)
    )


def graph_isomorph_test(model_file_1, model_file_2, output_dir='graphs/',
                        make_graphs=False, make_json=False):
    """Entry point for model consistency checking.

    This functions checks if the 2 given models have the same topology,
    nodes & edges attributes/roles.

    .. note:: cf graphmatcher
        https://networkx.github.io/documentation/development/reference/generated/networkx.algorithms.isomorphism.categorical_edge_match.html

    :param arg1: File for the model 1.
    :param arg2: File for the model 2.
    :param arg3: Output path.
    :param arg4: If True, make a graphml file in output path.
    :param arg5: If True, make a json dump of results in output path.
    :type arg1: <str>
    :type arg2: <str>
    :type arg3: <str>
    :type arg4: <boolean>
    :type arg5: <boolean>
    :return: Dictionary with the results of tests.
        keys: 'topology', 'nodes', 'edges'; values: booleans
    :rtype: <dict <str>: <boolean>>
    """

    import networkx.algorithms.isomorphism as iso

    # Load transitions in the models
    # Transitions structure format:
    # {u'h00': [('Ax', 'n1', {u'label': u'h00[]'}),]
    transitions_1, all_places_1 = get_transitions(model_file_1, all_places=True)
    transitions_2, all_places_2 = get_transitions(model_file_2, all_places=True)

    # Get all frontier places in the models
    # (places that are never in output position in all transitions)
    # EDIT: why we use all_places from the model instead of
    # (input_places - output_places) to get frontier places ?
    # Because some nodes are only in conditions and not in transitions.
    # If we don't do that, these nodes are missing when we compute
    # valid paths from conditions.
    front_places_1 = " ".join(get_frontier_places(transitions_1, all_places_1))
    front_places_2 = " ".join(get_frontier_places(transitions_2, all_places_2))
    LOGGER.debug("Frontier places 1: " + str(front_places_1))
    LOGGER.debug("Frontier places 2: " + str(front_places_2))

    # Build graphs & get networkx object
    # We give all events in the model as a list of steps
    # So we simulate a cadbiom solution (with all events in the model).
    res_1 = build_graph(front_places_1, [transitions_1.keys()], transitions_1)
    G1 = res_1[0]
    res_2 = build_graph(front_places_2, [transitions_2.keys()], transitions_2)
    G2 = res_2[0]

    # Checking
    nm = iso.categorical_node_match('color', 'grey')
    em = iso.categorical_edge_match('color', '')

    check_state = \
    {
        'topology': nx.is_isomorphic(G1, G2),
        'nodes': nx.is_isomorphic(G1, G2, node_match=nm),
        'edges': nx.is_isomorphic(G1, G2, edge_match=em),
    }

    LOGGER.info("Topology checking: " + str(check_state['topology']))
    LOGGER.info("Nodes checking: " + str(check_state['nodes']))
    LOGGER.info("Edges checking: " + str(check_state['edges']))

    # Draw graph
    if make_graphs:
        draw_graph(output_dir, front_places_1, "first", *res_1)
        draw_graph(output_dir, front_places_2, "second", *res_2)

    # Export to json file
    if make_json:
        with open(output_dir + "comp_results.json", 'w') as fd:
            fd.write(json.dumps(check_state, sort_keys=True, indent=4) + '\n')

    return check_state


def graph_infos(model_file, output_dir='graphs/',
                make_graph=True, make_json=True, advanced_measures=False):
    """Entry point for model stats.

    :param arg1: File for the model.
    :param arg2: Output path.
    :param arg3: If True, make a graphml file in output path.
    :param arg4: If True, make a json dump of results in output path.
    :type arg1: <str>
    :type arg2: <str>
    :type arg3: <boolean>
    :type arg4: <boolean>
    :return: Dictionary with the results of measures on the given graph.
        keys: measure's name; values: measure's value
    :rtype: <dict>
    """

    # Load transitions in the model
    # Transitions structure format:
    # {u'h00': [('Ax', 'n1', {u'label': u'h00[]'}),]
    transitions_1, all_places_1 = get_transitions(model_file, all_places=True)

    # Get all frontier places in the models
    # (places that are never in output position in all transitions)
    # EDIT: why we use all_places from the model instead of
    # (input_places - output_places) to get frontier places ?
    # Because some nodes are only in conditions and not in transitions.
    # If we don't do that, these nodes are missing when we compute
    # valid paths from conditions.
    front_places = get_frontier_places(transitions_1, all_places_1)
    front_places_str = " ".join(front_places)
    LOGGER.debug("Frontier places 1: " + front_places_str)

    # Build graphs & get networkx object
    # We give all events in the model as a list of steps
    # So we simulate a cadbiom solution (with all events in the model).
    res_1 = build_graph(front_places_str, [transitions_1.keys()], transitions_1)
    G = res_1[0]

    infos = {
        'model': model_file,
        'nodes': len(G.nodes()),
        'edges': len(G.edges()),
        'transitions:': len(transitions_1),
        'places': len(all_places_1),
        'frontier places': len(front_places),
    }

    if advanced_measures:
        infos.update({
            'degree': nx.degree_centrality(G),
            'in_degree': nx.in_degree_centrality(G),
            'out_degree': nx.out_degree_centrality(G),
            'betweenness': nx.betweenness_centrality(G),
            'closeness': nx.closeness_centrality(G),
        })

    # Draw graph
    if make_graph:
        draw_graph(output_dir, front_places_str, 'stat', *res_1)

    # Export to json file
    if make_json:
        with open(output_dir + "infos_results.json", 'w') as fd:
            fd.write(json.dumps(infos, sort_keys=True, indent=4) + '\n')

    LOGGER.info(str(infos))
    return infos


if __name__ == "__main__":

    LOG_DIR = "./logs/"
    BIO_MOLDELS_DIR = "./bio_models/"

    graph_isomorph_test(BIO_MOLDELS_DIR + "mini_test_publi.bcx",
                        BIO_MOLDELS_DIR + "mini_test_publi_mod.bcx")
    exit()

    process_solutions(load_solutions(LOG_DIR + "../run/Whole NCI-PID database translated into CADBIOM formalism(and)_SRP9_cam_complete.txt"),
                get_transitions(BIO_MOLDELS_DIR + "Whole NCI-PID database translated into CADBIOM formalism(and).bcx"))
    exit()


    #sort_solutions("/media/DATA/Projets/dyliss_tgf/cadbiom/run/Whole NCI-PID database translated into CADBIOM formalism(and)_SRP9_cam_complete.txt")
    #sort_solutions("/media/DATA/Projets/dyliss_tgf/cadbiom/run/Whole NCI-PID database translated into CADBIOM formalism(and)_SRP9_cam.txt")
    #sort_solutions("/media/DATA/Projets/dyliss_tgf/cadbiom/run/pid_and_clock_no_perm_p21corrected_start_SRP9_complete.txt")
    #exit()

#    cond = "((((not(ATF2_JUND_macroH2A_nucl))or(Fra1_JUND_active_nucl))or(Fra1_JUN_active_nucl))or(TCF4_betacatenin_active_nucl))or(JUN_FOS_active_nucl)"
#    ret = parse_condition(cond)
#    print(ret)
#    exit()

#    sol_steps = load_solutions(LOG_DIR + "../run/pid_and_clock_SRP9_cam_complete_o.txt")
#    g = [sol_step for sol_step in sol_steps]
#    print(g)
#    exit()

    sol_digging(load_solutions(LOG_DIR + "../run/pid_and_clock_no_perm_p21corrected_start_SRP9_complete.txt"),
             get_transitions(BIO_MOLDELS_DIR + "Whole NCI-PID database translated into CADBIOM formalism(and).bcx"))
    exit()

    sol_digging(load_solutions(LOG_DIR + "sols_new_solver.txt"),
             get_transitions(BIO_MOLDELS_DIR + "mini_test_publi.bcx"))
    exit()
    process_solutions(load_solutions(LOG_DIR + "sols_new_solver.txt"),
                      get_transitions(BIO_MOLDELS_DIR + "mini_test_publi.bcx"))
    exit()

#    build_graph(load_solutions(LOG_DIR + "../run/pid_and_clock_SRP9_cam_complete_o.txt"),
#                get_transitions(BIO_MOLDELS_DIR + "pid_and_clock.bcx"))
    process_solutions(load_solutions(LOG_DIR + "../run/pid_and_clock_SRP9_cam_complete.txt"),
                get_transitions(BIO_MOLDELS_DIR + "pid_and_clock.bcx"))

##
## Filename    : extract_visitor.py
## Author(s)   : Michel Le Borgne
## Created     : 5 nov. 2012
## Revision    :
## Source      :
##
## Copyright 2009 - 2012 : IRISA/IRSET
##
## This library is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published
## by the Free Software Foundation; either version 2.1 of the License, or
## any later version.
##
## This library is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY, WITHOUT EVEN THE IMPLIED WARRANTY OF
## MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.  The software and
## documentation provided hereunder is on an "as is" basis, and IRISA has
## no obligations to provide maintenance, support, updates, enhancements
## or modifications.
## In no event shall IRISA be liable to any party for direct, indirect,
## special, incidental or consequential damages, including lost profits,
## arising out of the use of this software and its documentation, even if
## IRISA have been advised of the possibility of such damage.  See
## the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this library; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
##
## The original code contained here was initially developed by:
##
##     Michel Le Borgne.
##     IRISA
##     Symbiose team
##     IRISA  Campus de Beaulieu
##     35042 RENNES Cedex, FRANCE
##
##
##     http:
##     mailto:
##
## Contributor(s):  Geoffroy Andrieux
##
"""
Visitors for extracting submodels.
PathExtractor : abstract a trajectory as a set of path in the transition graph
"""

from cadbiom.models.guard_transitions.chart_model import ChartModel, CTransition
from cadbiom.models.guard_transitions.analyser.ana_visitors import \
        SigExpIdCollectVisitor
from cadbiom.models.biosignal.translators.gt_visitors import compile_cond, compile_event
from cadbiom.models.guard_transitions.analyser.ana_visitors import TableVisitor

class PathExtractor(object):
    """
    Extract a submodel consisting in all the path from a frontier subset to
    a target represented as a list of places
    The visitor clean and affect simple node attributes:
    activated: treated - incoming paths explored
    was_activated: reach frontier or not - has meaning if activated = True
    """
    def __init__(self, model, target, frontier, reporter):
        """
        Constructor
        @param target: a list of places
        @param frontier: a list of frontier places
        """
        self.model = model
        tvi = TableVisitor(reporter)
        model.accept(tvi)
        self.symb_tab = tvi.tab_symb
        self.found = []
        self.frontier = [] # OK frontier
        self.reporter = reporter
        try:
            for pla in target:
                self.found.append(model.simple_node_dict[pla])
            for pla in frontier:
                self.frontier.append(model.simple_node_dict[pla])
        except KeyError:
            pass

        self.extract_model = ChartModel(model.name + "_extract")

    def visit_chart_model(self, model):
        """
        Do the job
        """
        # set activated and was_activated simple node attributes to False
        model.clean()
        # explore all paths and build the sub model
        while len(self.found) > 0:
            xpl = self.found[0]
            self.found.remove(xpl)
            xpl.accept(self)
        # set to false non reachable places in events and conditions

        # clean
        model.clean()

    def visit_cstart_node(self, node):
        """
        do nothing: see transitions
        """
        return False

    def visit_csimple_node(self, node):
        """
        explore all incoming transitions
        @return: True if frontier or perm,input node reached from node
        """
        # node already visited (use activated attribute)
        if node.activated:
            return node.was_activated  # path to frontier or not
        node.activated = True
        # node without incoming transition (frontier but may not be OK)
        if len(node.incoming_trans) == 0:
            node.was_activated = node in self.frontier
            if node.was_activated and len(node.outgoing_trans) == 0:
                # isolated frontier OK node
                self.extract_model.get_root().add_copy(node)
            return node.was_activated
        # node with incoming transition
        natt = False
        for intr in node.incoming_trans:
            # deep first visit of predecessors
            fatt = intr.ori.accept(self)
            if fatt: # reach OK frontier this way
                # find new nodes in event and cond
                tr_var = extract_state_var(self.model, intr,
                                           self.symb_tab, self.reporter)
                # add nodes in found
                for nvar in tr_var:
                    node = self.model.node_dict[nvar]
                    if node.is_simple():
                        if not node.activated: # not treated
                            if not node in self.found: # not waiting
                                self.found.append(node)
                # add the transition to extracted model
                add_ext_transition(intr, self.extract_model)
                natt = True

        node.was_activated = natt
        return natt

    def visit_cinput_node(self, node):
        """
        An input node is a frontier node always available
        """
        return True

    def visit_cperm_node(self, node):
        """
        A permanent node is an always available frontier node
        """
        return True




# helper functions
def extract_state_var(model, intr, symb_tab, reporter):
    """
    Extract state variable (place names) from condition and
    event of a transition.
    """
    lst2 = []
    lst1 = []
    cond_sexpr = None
    ev_sexpr = None
    if intr.condition:
        cond_sexpr = compile_cond(intr.condition, symb_tab, reporter)
    if intr.event:
        ev_sexpr = compile_event(intr.event, symb_tab, True, reporter)[0]

    icv = SigExpIdCollectVisitor()
    if cond_sexpr:
        # condition expressions contains only node ident
        lst1 = cond_sexpr.accept(icv)
    if ev_sexpr:
        ll2 = ev_sexpr.accept(icv)
        for ident in ll2:
            if model.node_dict.has_key(ident): # state
                lst2.append(ident)
    lst = lst1 + lst2
    lst.sort()
    print 'LISTE', lst
    # eliminate doubles
    if len(lst) > 0:
        nres = [lst[0]]
        for i in range(len(lst)-1):
            if lst[i+1] != lst[i]:
                nres.append(lst[i+1])
    else:
        nres = []
    return nres

def add_ext_transition(trans, extract_model):
    """
    Add a copy of trans in extract_model
    """
    onam = trans.ori.name
    tnam = trans.ext.name
    # find origin and extremity
    try:
        new_ori = extract_model.node_dict[onam]
    except KeyError:
        new_ori = extract_model.get_root().add_copy(trans.ori)
    try:
        new_ext = extract_model.node_dict[tnam]
    except KeyError:
        new_ext = extract_model.get_root().add_copy(trans.ext)

    ntr = extract_model.get_root().add_transition(new_ori, new_ext)
    ntr.set_condition(trans.condition)
    ntr.set_event(trans.event)




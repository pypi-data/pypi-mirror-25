## Filename    : simul_aux.py
## Author(s)   : Michel Le Borgne
## Created     : 04/2010
## Revision    :
## Source      :
##
## Copyright 2010 : IRISA/INRIA
##
## This library is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published
## by the Free Software Foundation; either version 2.1 of the License, or
## any later version.
##
## This library is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY, WITHOUT EVEN THE IMPLIED WARRANTY OF
## MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.  The software and
## documentation provided here under is on an "as is" basis, and INRIA has
## no obligations to provide maintenance, support, updates, enhancements
## or modifications.
## In no event shall INRIA be liable to any party for direct, indirect,
## special, incidental or consequential damages, including lost profits,
## arising out of the use of this software and its documentation, even if
## INRIA have been advised of the possibility of such damage.  See
## the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this library; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
##
## The original code contained here was initially developed by:
##
##     Michel Le Borgne.
##     IRISA/INRIA
##     Symbiose team
##     IRISA  Campus de Beaulieu
##     35042 RENNES Cedex, FRANCE
##
##
## Contributor(s): Geoffroy Andrieux
##
"""
Auxiliary classes for simulator
"""

import sys
from cadbiom.models.guard_transitions.chart_model import ChartModel
from cadbiom.models.guard_transitions.simulator.simul_exceptions import SimulException

class ChartExpVisitor(object):
    """
    Evaluator of event and condition expressions
    """
    def __init__(self, stable):
        self.symb_table = stable
        pass

    def visit_sig_ident(self, iex):
        """
        @param iex: ident expression
        """
        try:
            elem = self.symb_table[iex.name]
        except:
            print 'ChartExpVisitor:BIG BUG in expression evaluation '+iex.name
            sys.exit(1)
        return elem.activated

    def visit_sig_const(self, cex):
        """
        Simply value
        """
        return cex.value

    def visit_sig_default(self, dex):
        """
        Compute value
        """
        cv1 = dex.left_h.accept(self)
        cv2 = dex.right_h.accept(self)
        return cv1 or cv2

    def visit_sig_when(self, wex):
        """
        Compute value
        """
        cv1 = wex.left_h.accept(self)
        cv2 = wex.right_h.accept(self)
        return cv1 and cv2

    def visit_sig_equal(self, eex):
        """
        TODO
        """
        pass

    def visit_sig_diff(self, dex):
        """
        TODO
        """
        pass

    def visit_sig_not(self, nex):
        """
        Compute value
        """
        cval = nex.operand.accept(self)
        return not cval

    def visit_sig_event(self, eex):
        """
        TODO
        """
        pass

    def visit_sig_sync(self, sex):
        """
        compute value
        """
        cv1 = sex.left_h.accept(self)
        cv2 = sex.right_h.accept(self)
        if sex.operator == 'or':
            return cv1 or cv2
        if sex.operator == 'and':
            return cv1 and cv2


    def visit_sig_poly(self, pex):
        """
        TODO
        """
        pass

    def visit_sig_poly_pow(self, poe):
        """
        TODO
        """
        pass

class ModelExtractorVisitor(object):
    """
    Extract a submodel including places and transitions activated during a simulation.
    """
    def __init__(self, name_suffix, ex_type):
        """

        """
        self.name_suffix = name_suffix
        self.ex_type = ex_type
        pass

    def visit_chart_model(self, model):
        """
        Entrance point
        """
        self.sub_model = ChartModel(model.name+'_'+self.name_suffix)
        model.get_root().accept(self)
        return

    def visit_cstart_node(self, node):
        """
        Nothing to do
        """
        return

    def visit_ctrap_node(self, node):
        """
        Nothing to do
        """
        return

    def visit_csimple_node(self, node):
        """
        Extract nodes activated during simulation
        """
        if node.was_activated:
            self.sub_model.get_root().add_simple_node(node.name, 0.0, 0.0)
        return

    def visit_cinput_node(self, node):
        """
        Same as simple nodes
        """
        if node.was_activated:
            self.sub_model.get_root().add_input_node(node.name, 0.0, 0.0)
        return

    def visit_cperm_node(self, node):
        """
        nothing to do
        """
        return

    def visit_cmacro_node(self, node):
        """
        treated as simple nodes (no subnodes allowed)
        """
        if len(node.sub_nodes) > 0:
            mess = 'ModelExtractorVisitor: subnodes in macro state'
            mess = mess + 'are not allowed'
            raise SimulException()
        self.visit_csimple_node(node)
        return

    def visit_ctop_node(self, node):
        """
        visit subnodes then transitions
        """
        for snode in node.sub_nodes:
            snode.accept(self)
        for gtr in node.transitions:
            for trans in gtr:
                trans.accept(self)
        return

    def visit_ctransition(self, trans):
        """
        visit a transition - activated transition are extracted
        """
        if not trans.activated:
            return
        ori = trans.ori
        target = trans.ext
        # ori already extracted?
        try:
            n_ori = self.sub_model.get_node(ori.name)
        except: # add a copy to
            n_ori = self.sub_model.get_root().add_copy(ori)
        # same for target
        try:
            n_target = self.sub_model.get_node(target.name)
        except:
            n_target = self.sub_model.get_root().add_copy(target)
        # first time added or bug
        n_tr = self.sub_model.get_root().add_transition(n_ori, n_target)
        n_tr.set_event(trans.event)
        n_tr.set_condition(trans.condition)
        n_tr.activated = True # for path marks
        # add concurrent transitions not used
        if self.ex_type:
            for ctr in ori.outgoing_trans:
                if not trans == ctr and not ctr.activated:
                    ctarg = ctr.ext
                    try:
                        n_ctarg = self.sub_model.get_node(ctarg.name)
                    except:
                        n_ctarg = self.sub_model.get_root().add_copy(ctarg)
                    n_ctr = self.sub_model.get_root().add_transition(n_ori,
                                                                     n_ctarg)
                    if n_ctr: # may be already added here
                        n_ctr.set_event(ctr.event)
                        n_ctr.set_condition(ctr.condition)
                        n_ctr.activated = False # for path marks
        return

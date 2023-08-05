## Filename    : gt_visitors.py
## Author(s)   : Michel Le Borgne
## Created     : 01/2012
## Revision    : 8/12 suppression des macros
## Source      :
##
## Copyright 2010-2012 : IRISA/IRSET
##
## This library is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published
## by the Free Software Foundation; either version 2.1 of the License, or
## any later version.
##
## This library is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY, WITHOUT EVEN THE IMPLIED WARRANTY OF
## MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.  The software and
## documentation provided here under is on an "as is" basis, and IRISA has
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
## Contributor(s): Geoffroy Andrieux
##
"""
Visitor for simulator generation
"""
import sys

from cadbiom.models.guard_transitions.simulator.chart_simul_elem import Place, \
                   STransition, Event, Condition, InputPlace, InputEvent
from cadbiom.models.biosignal.sig_expr import SigIdentExpr
from cadbiom.models.biosignal.translators.gt_visitors import compile_cond, compile_event

class GenSimVisitor(object):
    """
    Generate a simulator model - needs a symbol table of the charter model
    """
    def __init__(self, tab_symb, mod, free_clocks, report):
        """
        This visitor fill a simulation object - identifiers must be in
        tab_symb if free_clocks option = False. When free_clocks option = True
        undeclared ids in an event expression are considered as free clocks.
        @param tab_symb: symbol table obtained from TableVisitor
        @param mod: empty simulation model to be built
        @param free_clocks: allows free clocks if True
        @param report: error reporter of CompilReporter type
        """
        self.sim_model = mod       # empty simulator object
        self.tab_symb = tab_symb   # symbol table of chart_model representation
        # symbol table to retrieve simulator model element
        self.mod_symb_tab = dict()
        self.error_reporter = report
        self.error = False
        self.free_clock_collect = free_clocks
        self.free_clocks = [] # collect free clocks


    def visit_chart_model(self, model):
        """
        visit chart model, generate simulation model and collect free clocks
        """
        model.get_root().accept(self)
        # transform free clocks into inputs
        if self.free_clock_collect:
            for efc in self.free_clocks:
                try:
                    evt = self.mod_symb_tab[efc]
                except:
                    evt = InputEvent(SigIdentExpr(efc))
                    self.mod_symb_tab[efc] = evt
                    self.sim_model.add_event(evt, efc)
                    self.sim_model.add_input(evt)

    def visit_cstart_node(self, node):
        """
        do nothing: see transitions
        """
        return

    def visit_ctrap_node(self, node):
        """
        do nothing: see transitions
        """
        return

    def visit_csimple_node(self, node):
        """
        create a place in the simulator model
        register it in the symbol table
        """
        place = Place(node)
        name = node.name
        self.sim_model.add_state_place(place, name)
        self.mod_symb_tab[name] = place
        return

    def visit_cinput_node(self, node):
        """
        create an input place (artificial perm place)
        and an event representing the input
        """
        place = InputPlace(node)
        self.sim_model.add_place(place)
        name = input_perm_name(node)
        self.mod_symb_tab[name] = place
        # add corresponding event with name the name of the input place
        try:
            evt = self.mod_symb_tab[node.name]
        except:
            evt = InputEvent(SigIdentExpr(node.name))
            self.mod_symb_tab[node.name] = evt
            self.sim_model.add_event(evt, node.name)
            self.sim_model.add_input(evt)
        evt.add_ev_place(place)
        return

    def visit_cperm_node(self, node):
        """
        create a place in the simulator model
        register it in the symbol table
        mark it as permanent
        """
        place = Place(node)
        place.set_perm()
        name = node.name
        self.sim_model.add_state_place(place, name)
        self.mod_symb_tab[name] = place
        return

    def visit_cmacro_node(self, node):
        """
        macro nodes are treated as simple nodes (no real macros allowed)
        """
        if len(node.sub_nodes) >0:
            self.error_reporter.display("Macro node "+node.name+" is not empty")
            self.error = True
        self.visit_csimple_node(node)
        return

    def visit_ctop_node(self, node):
        """
        trap node is unique for all the system
        it is created here
        """
        trap_all = Place(None, '_trap_')
        self.mod_symb_tab["__trap_all__"] = trap_all
        self.sim_model.add_place(trap_all)
        self.sim_model.trap = trap_all

        # sub nodes creation (all places are created by this action)
        for snode in node.sub_nodes:
            snode.accept(self)

        # transitions
        for gtr in node.transitions:
            for trans in gtr:
                trans.accept(self)
        return

    def visit_ctransition(self, trans):
        """
        main visitor - the code generation is dispatched in
        several helper methods
        """
        if trans.ori.is_start(): # transition from start
            # nothing to do (start is a frontier mark)
            return
        elif trans.ori.is_input(): # transition from input
            self.build_input_transition(trans)
        elif trans.ext.is_trap(): # transition to trap node
            self.build_transition(trans, True)
        else:  # standard transition
            self.build_transition(trans)
        return



    # auxiliary functions for compilation
    def build_transition(self, trans, trap = False):
        """
        build a transition from a graph transition
        @param trans: the chart transition
        @param trap: True if target is a trap node
        """
        model = self.sim_model
        tab_symb = self.tab_symb
        report = self.error_reporter
        report.set_context(trans.ori.name+'->'+trans.ext.name)
        try:
            ori = self.mod_symb_tab[trans.ori.name]
            if trap:
                ext = self.sim_model.trap
            else:
                ext = self.mod_symb_tab[trans.ext.name]
        except LookupError, exc:
            print exc
            print trans.ori.name +' -> '+trans.ext.name , trap
            print self.mod_symb_tab
            print 'build_transition: BUG!'
            sys.exit(1)
        trs = STransition(ori, ext, trans)
        self.mod_symb_tab[trans.get_key()] = trs
        # event
        if len(trans.event)>0:
            event_text = trans.event
            event_tree, st_ev, fcl = compile_event(event_text, tab_symb,
                                                  self.free_clock_collect,
                                                  report)
            if self.free_clock_collect:
                self.free_clocks.extend(fcl)
            evt = Event(event_tree)
            trs.set_event(evt)
            # see if state events where used
            for ev_n in st_ev:
                try:
                    evt = self.mod_symb_tab[ev_n]
                except:
                    evt = Event(SigIdentExpr(ev_n))
                    self.mod_symb_tab[ev_n] = evt
                    self.sim_model.add_event(evt, ev_n)
                state_name = ev_n[:-1]   # ev_n = state> or ev_n = state<
                sign = ev_n[-1]
                place = self.mod_symb_tab[state_name]
                if sign == '>':
                    place.ev_up = evt
                else:
                    place.ev_down = evt
        # condition
        if len(trans.condition)>0:
            cond_text = trans.condition
            cond_tree = compile_cond(cond_text, tab_symb, report)
            cond = Condition(cond_tree)
            trs.set_condition(cond)
        # action (signal)
        if len(trans.action)>0:
            act_text = trans.action
            act_tree, ste, fcl = compile_event(act_text, tab_symb,
                                               self.free_clock_collect, report)
            if self.free_clock_collect:
                self.free_clocks.extend(fcl)
            if act_tree.is_ident():
                # create the event if not already done
                try:
                    evt = self.mod_symb_tab[act_tree.name]
                except:
                    evt = Event(act_tree)
                    self.mod_symb_tab[act_tree.name] = evt
                    model.add_event(evt, act_tree.name)
                trs.set_signal(evt)
            else:
                report.display("Syntax: Emitted event must be a name ")
                self.error = True
        self.sim_model.add_transition(trs)


    def build_input_transition(self, trans):
        """
        Build a perm place (if not already done) and a transition from
        the perm node to the target of trans.
        @param trans: the chart model transition
        """
        model = self.sim_model
        tab_symb = self.tab_symb
        report = self.error_reporter
        ev_name = trans.ori.name

        # input transition must have no event
        if trans.event:
            mess = "Syntax: A start transition must have no event: ->"
            mess = mess + trans.ext.name
            report.display(mess)
            self.error = True
        perm_name = input_perm_name(trans.ori)
        try:
            # should be created with other places
            input_place = self.mod_symb_tab[perm_name]
        except:
            print 'BUG: input place not built'
            sys.exit(1)

        ext = self.mod_symb_tab[trans.ext.name]
        # new transition from perm place to input target
        trs = STransition(input_place, ext, trans)
        model.add_transition(trs)
        self.mod_symb_tab[input_trans_name(trans)] = trs
        # event - is the input
        try:
            evt = self.mod_symb_tab[ev_name]
        except:
            pass #TODO internal error
        trs.set_event(evt)
        # condition
        if len(trans.condition)>0:
            cond_text = trans.condition
            cond_tree = compile_cond(cond_text, tab_symb, report)
            cond = Condition(cond_tree)
            trs.set_condition(cond)
        # action
        if len(trans.action)>0:
            act_text = trans.action
            # cannot find free clocks in action
            act_tree, ste, fcl = compile_event(act_text, tab_symb, False,
                                               report)
            if act_tree.is_ident():
                # create the event if not already done
                try:
                    evt = self.mod_symb_tab[act_tree.name]
                except:
                    evt = Event(act_tree)
                    self.mod_symb_tab[act_tree.name] = evt
                    model.add_event(evt, act_tree.name)
                trs.set_signal(evt)
            else:
                mess = "Syntax: Emitted event must be an id "
                mess = mess + trans.ori.name + "->" + trans.ext.name
                report.display(mess)
                self.error = True



# helper functions
def input_perm_name(in_node):
    """
    generate a standard name for pseudo perm places associated with inputs
    """
    return "__"+in_node.name+"$$input"

def input_trans_name(trans):
    """
    generate a standard name for transitions
    """
    return '__'+trans.ori.name+"__"+trans.ext.name


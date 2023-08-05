## Filename    : chart_simul.py
## Author(s)   : Michel Le Borgne
## Created     : 04/2010
## Revision    :
## Source      :
##
## Copyright 2010 : IRISA/IRSET
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
## In no event shall INRIA be liable to any party for direct, indirect,
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
## Contributor(s): Geoffroy Andrieux IRISA/IRSET
##
"""
Guarded transition systems simulator implementation
"""

from cadbiom.models.guard_transitions.analyser.ana_visitors import TableVisitor
from cadbiom.models.guard_transitions.simulator.translators.gt_visitors import\
                                      GenSimVisitor
from cadbiom.models.guard_transitions.simulator.simul_exceptions import\
                                      SimulException, SimulPropViolation
from cadbiom.models.guard_transitions.simulator.input_stream import CFileInput, ActInput
from simul_aux import ChartExpVisitor
from cadbiom.models.biosignal.translators.gt_visitors import compile_cond

# the simulator
class ChartSimulator(object):
    """
    wrap everything for simulation - this include the simulator model and simulator attribute to
    manage simulation.
    """
    def __init__(self):
        # the chart model which is the source of simulator model
        self.model = None

        # simulation model - components are described in chart_simul.py
        # first place to be activated at initialisation (graphical init)
        self.start = None
        self.__model_symb_tab = None
        self.__symb_tab = dict()   # symbol table
        # basic building blocks of a flat model (no macro state)
        self.__places = []
        self.__transitions = []    # other basic blocks
        self.__events = []
        self.__inputs = []
        self.input_names = []
        # list of __places which are activated at initialization
        self.init_places = []

        # properties
        self.invariant_prop = None
        self.reachable_prop = None

        # simulation helpers
        self.input_buffer = None # simulate __inputs described in file
        self.chrono = None       # auxiliary display"

        # simulator memory
        self.__activated_places = []
        self.__armed_transitions = []
        self.__fireabled_transitions = []
        self.__step = 0

    def build(self, chart_model, sim_option, reporter):
        """
        Given a chart_model, build a simulator
        @param chart_model: a ChartModel object
        @param sim_option: allows free clocks if True
        @param reporter: must be a CompilReporter
        """
        self.model = chart_model
        # symbol table built
        tvi = TableVisitor(reporter)
        chart_model.accept(tvi)
        if tvi.error:
            reporter.display("Error in symbol declarations")
            return
        # GenSimVisitor brings the simulator model with him and fill it
        # essentially flatten the initial model => no more macro
        self.__model_symb_tab = tvi.tab_symb
        gsv = GenSimVisitor(tvi.tab_symb, self, sim_option, reporter)
        chart_model.accept(gsv)

    def add_state_place(self, place, name):
        """
        state places are referenced in the simulator symbol table
        """
        self.__places.append(place)
        self.__symb_tab[name] = place

    def add_place(self, place):
        """
        add any place
        """
        self.__places.append(place)

    def add_transition(self, trans):
        """
        add a transition
        """
        self.__transitions.append(trans)

    def add_event(self, evt, name):
        """
        add an event
        """
        self.__events.append(evt)
        self.__symb_tab[name] = evt

    def add_input(self, inp):
        """
        add an input
        """
        self.__inputs.append(inp)
        self.input_names.append(inp.expression.name)

    def has_input(self):
        """
        test if the simulated model has inputs
        """
        return len(self.__inputs)>0

    def get_symb_tab(self):
        """
        the symbol table: name -> chart_simul_elem
        """
        return self.__symb_tab

    def get_step(self):
        """
        value of the simulator step counter
        """
        return self.__step


    def set_invariant_prop(self, prop):
        """
        set invariant property to be checked.
        A property violation exception is raised if violated
        @param prop: string - textual representation of property on places
        """
        reporter = SimReport()
        try:
            self.invariant_prop = compile_cond(prop, self.__model_symb_tab,
                                               reporter)
        except Exception , exc:
            raise SimulException("Error in property " + exc.__str__())

    def set_reachable_prop(self, prop):
        """
        set reachable property to be checked.
        @param prop: string - textual representation of property on places
        """
        reporter = SimReport()
        try:
            self.reachable_prop = compile_cond(prop, self.__model_symb_tab,
                                               reporter)
        except Exception , exc:
            raise SimulException("Error in property " + exc.__str__())


    def set_sce_file_input_stream(self, filename):
        """
        Find the file containing  description of a scenario
        set the input stream to read the __inputs only
        Throw SimulException
        """
        self.input_file = filename
        try:
            self.input_buffer = ActInput(filename)
            init_places = self.input_buffer.input_buffer[0].split()
            self.simul_init_places(init_places)
        except SimulException, sexc:
            self.input_buffer = None
            raise SimulException(sexc.message)

        except Exception, exc:
            self.input_buffer = None
            raise SimulException("Problem reading input file: " + exc.__str__())

    def set_act_file_input_stream(self, filename):
        """
        Find the file containing input description as an enumeration of activated
        __inputs  - set the input stream
        Throw SimulException
        """
        self.input_file = filename
        try:
            self.input_buffer = ActInput(filename)
        except SimulException, sexc:
            self.input_buffer = None
            raise SimulException(sexc.message)

        except Exception, exc:
            self.input_buffer = None
            raise SimulException("Problem reading input file:" + exc.__str__())

    def set_act_input_stream(self, act_input_list):
        """
        Set the input stream from a list of activated __inputs in format "% i1 i2 h2 h4 h8"
        """
        self.input_buffer = ActInput(inlist=act_input_list)


    def set_cfile_input_stream(self, filename):
        """
        Find the file containing input description using a language - set the input stream
        Throw SimulException
        """
        self.input_file = filename
        try:
            self.input_buffer = CFileInput(filename)
        except SimulException, sexc:
            self.input_buffer = None
            raise SimulException(sexc.message)

        except Exception, exc:
            self.input_buffer = None
            raise SimulException("Problem reading input file:" + exc.__str__())
        # check coherence with model
        inames = self.input_buffer.input_names
        nb_inames = self.input_buffer.nb_inputs
        if nb_inames == len(self.input_names):
            for name in inames:
                if not name in self.input_names:
                    self.input_buffer = None
                    raise SimulException("Name in file is not a model input")
        else:
            self.input_buffer = None
            mess = "Numbers of __inputs different in input file and model"
            raise SimulException(mess)

    # simulation methods
    def __set_armed_transitions(self):
        """
        At the beginning of the simulation we select __transitions with activated origin
        """
        self.__armed_transitions = []
        for place in self.__places:
            if place.activated:
                for trans in place.out_transitions:
                    self.__armed_transitions.append(trans)

    def __set_events(self):
        """
        Read the input buffer if any and set input __events
        """
        # set events to unactivated
        for evt in self.__events:
            evt.set_activated(False)
        # read input if any
        if self.input_buffer:
            nin = self.input_buffer.next_input()
            for evn in nin:
                try:
                    self.__symb_tab[evn].set_activated(True)
                except KeyError:
                    raise SimulException('Simul set_event: Unknown event')

    def __add_fireable_transitions(self):
        """
        A transition is fire-able if both its event and its condition are true
        """
        self.add_fir_trans = False
        expv = ChartExpVisitor(self.__symb_tab)
        for trans in self.__armed_transitions:
            if trans.event: # eval event
                ev_val = trans.event.expression.accept(expv)
            else:
                ev_val = True
            if ev_val: # event present
                if trans.condition: # eval condition
                    cond_val = trans.condition.expression.accept(expv)
                else:
                    cond_val = True
                if cond_val:
                    self.__fireabled_transitions.append(trans)
                    self.__armed_transitions.remove(trans)
                    self.add_fir_trans = True
                    # update __events
                    if trans.signal:
                        trans.signal.activated = True
                    # see if target and origin states emit an event
                    if trans.target.ev_up:
                        trans.target.ev_up.activated = True
                    if trans.origin.ev_down:
                        trans.origin.ev_down.activated = True

    def __set_fireable_transitions(self):
        """
        Fix point calculation of fire-able __transitions
        """
        self.__fireabled_transitions = []
        self.add_fir_trans = True
        while self.add_fir_trans:
            self.__add_fireable_transitions()

    def __fire_desactivate(self):
        """
        unactivation when transitions are fired
        """
        for trans in self.__fireabled_transitions:
            trans.desactivate()

    def __fire_activate(self):
        """
        activation when transitions are fired
        """
        for trans in self.__fireabled_transitions:
            trans.activate()


    def check_inv_conditions(self):
        """
        evaluate invariant property in the current state
        Raise a SimulPropViolation exception if invariant property is
        not satisfied.
        """
        if self.invariant_prop:
            expv = ChartExpVisitor(self.__symb_tab)
            val = self.invariant_prop.accept(expv)
            if not val:
                raise SimulPropViolation("Invariant violation",
                                         self.invariant_prop.__str__())

    def check_reachable_property(self):
        """
        evaluate final property in the current state
        @return: the result (bool) of the evaluation
        """
        if self.reachable_prop:
            expv = ChartExpVisitor(self.__symb_tab)
            val = self.reachable_prop.accept(expv)
            return val

    def simul_step(self):
        """
        Perform a simulation step
        """
        self.__set_armed_transitions()
        self.__set_events()
        self.__set_fireable_transitions()
        self.__fire_desactivate()
        self.__fire_activate()
        self.check_inv_conditions()
        self.model.notify()
        self.__step += 1

    def simul_step_trace(self, trace_file = None):
        """
        same as simul_step but register a trace
        """
        self.__set_armed_transitions()
        self.__set_events()
        self.__set_fireable_transitions()
        self.__fire_desactivate()
        self.__fire_activate()
        # __events are registered a step late
        if not trace_file:
            pln = []
            for place in self.__places:
                if place.activated and not place.is_input_place():
                    pln.append(place.name)
            for evt in self.__events:
                if evt.is_input_event() and evt.activated:
                    pln.append(evt.expression.__str__())
            print pln
        else:
            trace_file.write("\n%")
            for place in self.__places:
                if place.activated and not place.is_input_place():
                    trace_file.write(" "+place.name)
            for evt in self.__events:
                if evt.is_input_event() and evt.activated:
                    trace_file.write(evt.expression.__str__())
        self.check_inv_conditions()
        self.__step += 1

    def simul_init(self):
        """
        Simulator initialization
        """
        self.__step = 0
        self.model.clean()
        self.init_places = None
        for place in self.__places:
            place.force_desactivate()
        for str in self.__transitions:
            str.init_desactivate()
        for evt in self.__events:
            evt.set_activated(False)


    def simul_init_places(self, init_places):
        """
        @param init_places: list of place names to be activated
        """
        self.__step = 0
        self.model.clean()
        self.init_places = init_places
        for place in self.__places:
            if place.perm:
                place.activate()
            else:
                place.desactivate()
        for pl_name in init_places:
            self.__symb_tab[pl_name].activate()
        for str in self.__transitions:
            str.init_desactivate()
        self.check_inv_conditions()
        self.model.notify()

class SimReport(object):
    """
    Simple reporter used for simulation
    """

    def __init__(self):
        self.mess = ""

    def display(self, mess):
        """
        Interrupt all in case of problems
        """
        raise SimulException(mess)

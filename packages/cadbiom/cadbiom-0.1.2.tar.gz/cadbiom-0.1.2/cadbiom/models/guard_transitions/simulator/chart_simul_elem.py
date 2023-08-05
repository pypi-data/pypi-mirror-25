## Filename    : chart_simul_elem.py
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
Building blocks for a simulator
"""

import sys

class Place(object):
    """
    A place represents a component of the state of the system
    """
    def __init__(self, g_state, name = None):
        """
        @param g_state: the component in the graphic model
        @param name: name of the place. mandatory if g_state is None
        """
        self.graph_state = g_state # place in chart_model (may be None)
        if self.graph_state:
            self.name = g_state.name
        else:
            self.name = name
        # permanent place (not unactivated by firing an outgoing transition)
        self.perm = False         
        self.activated = False    # state of the place
        self.out_transitions = [] # filled by transition constructor
        self.in_transitions = []  # idem
        self.ev_up = None         # event state up if used
        self.ev_down = None       # event state down if used
        
    def __str__(self):
        return self.name
    
    def is_place(self):
        """
        As it says
        """
        return True
    
    def is_input_event(self):
        """
        As it says
        """
        return False
    
    def is_input_place(self):
        """
        As it says
        """
        return False
    
    def set_perm(self):
        """
        Turn into a permanent node
        """
        self.perm = True
        
    def activate(self):
        """
        As it says
        """
        self.activated = True
        # for graphical representation of activity
        if self.graph_state:
            self.graph_state.activated = True
            self.graph_state.was_activated = True
        
    def desactivate(self):
        """
        places without graph representation are artificial inputs thus perm = True
        """
        if not self.perm:
            self.activated = False
            if self.graph_state:
                self.graph_state.activated = False # don't touch was_activated
            

    def force_desactivate(self):
        """
        Used to clear chart_model places activations
        desactivate all places - even permanent places
        """
        self.activated = False
        if self.graph_state:
            self.graph_state.activated = False    


class InputPlace(Place):
    """
    @param g_state: Corresponding place in CadbiomChart model (possibly None)
    @param name: Must be given if g_state=None
    An input place coming from the graph model is a sort of perm place
    An input place representing a free event has no corresponding element in chart model (g_state = None)
    """
    def __init__(self, g_state, name = None):
        if g_state:
            Place.__init__(self, g_state)
        else:
            Place.__init__(self, None, name)
        self.perm = True
        
    def is_input_place(self):
        return True
        
    def activate(self):
        self.activated = True
        
    def desactivate(self):
        return
                    
    def input_activate(self):
        """
        special activation for input
        """
        if self.activated and self.graph_state:
            self.graph_state.activated = True
        
    def input_desactivate(self):
        """
        special unsactivation for input
        """
        if self.graph_state:
            self.graph_state.activated = False
       
class STransition(object):
    """
    Represents a normal transition between  places - For optimization of induced transitions,
    STransitions have several origins and several targets. This is for taking care of 
    initializations when a macro state is activated and multiple un-activations for output
    transitions from places representing macros.
    """
    def __init__(self, ori, ext, gtrans=None):
        self.origin = ori       # Place
        self.target = ext       # Place
        self.g_trans = gtrans       # graph transition if any
        self.event = None       # an Event object
        self.condition = None   # condition object
        self.signal = None      # simple event object
        # register at origin as out transiton 
        self.origin.out_transitions.append(self)
        # similarly for in transitions
        self.target.in_transitions.append(self)  
        # simulation attributes
        # remember if target was activated by normal transition
        self.target_up = False  
        
    def __str__(self):
        return self.origin.graph_state.name+'->'+self.target.graph_state.name
    
    def set_event(self, evt):
        """
        standard setter
        """
        self.event = evt
        
    def set_condition(self, cond):
        """
        standard setter
        """
        self.condition = cond
        
    def set_signal(self, sig):
        """
        standard setter
        """
        self.signal = sig
                
    def activate(self):
        """
        activation
        """
        if self.g_trans:
            self.g_trans.activated = True
        if not self.target.activated:
            self.target_up = True
        self.target.activate()
        
    def desactivate(self):
        """
        unactivation
        """
        self.origin.desactivate()
            
    def init_desactivate(self):
        """
        initial RAZ
        """
        if self.g_trans:
            self.g_trans.activated = False
                
            
class Event(object):
    """
    An event is a clock from a Biosignal point of view - it is defined as a signal expression
    """
    def __init__(self, exp):
        self.expression = exp  # signal expression from compiler
        # if the expression is an identifier, actual value of the identifier
        self.activated = False 
        
    def is_place(self):
        """
        As it says
        """
        return False
    
    def is_input_event(self):
        """
        As it says
        """
        return False
    
    def set_activated(self, val):
        """
        @param val: activation value 
        """
        self.activated = val

class InputEvent(Event):
    """
    Special events for inputs
    """
    def __init__(self, exp):
        Event.__init__(self, exp)
        self.event_places = []
    
    def is_input_event(self):
        return True
    
    def add_ev_place(self, pla):
        """
        pla must be an input place
        """
        if pla.is_input_place():
            self.event_places.append(pla)
        else:
            print "add_ev_place: BUG"
            sys.exit(1)
        
    def set_activated(self, val):
        """
        overload the method of general class
        """
        self.activated = val
        if val:
            for pla in self.event_places:
                pla.input_activate()
        else:
            for pla in self.event_places:
                pla.input_desactivate()
            
                
class Condition(object):
    """
    A condition is a boolean expression on place values
    """
    def __init__(self, exp):
        self.expression = exp    
       

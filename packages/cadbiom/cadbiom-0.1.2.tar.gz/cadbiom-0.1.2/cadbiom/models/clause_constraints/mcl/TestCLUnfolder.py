
## Filename    : TestCLUnfolder.py
## Author(s)   : Michel Le Borgne
## Created     : 13 sept. 2012
## Revision    :
## Source      :
##
## Copyright 2012 : IRISA/IRSET
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
## Contributor(s):
##
'''
Unitary Test of the unfolder
'''
import unittest


from cadbiom.models.guard_transitions.chart_model import ChartModel
from cadbiom.models.clause_constraints.CLDynSys import Literal, Clause
from cadbiom.models.guard_transitions.analyser.ana_visitors import TableVisitor
from cadbiom.models.clause_constraints.CLDynSys import CLDynSys
from cadbiom.models.clause_constraints.mcl.MCLTranslators import  GT2Clauses
from cadbiom.models.clause_constraints.mcl.CLUnfolder import CLUnfolder

# helper functions

def string_to_clause(text_clause):
    """
    text_clause is a string such that "a,not b,not c"
    it is transformed in the corresponding clause
    WARNING: strict syntax - no check - for tests
    """
    # split into literals
    clause = Clause([])
    llit = text_clause.split(',')
    # translate each literal
    for lit in llit:
        spl = lit.split()
        if len(spl) == 1: # "a"
            clause.add_lit(Literal(spl[0], True))
        else: # "not a"
            clause.add_lit(Literal(spl[1], False))
    return clause

def num_clause_equal(clause_1, clause_2):
    """
    test DIMACS clauses for equality
    """
    if len(clause_1) != len(clause_2):
        return False
    clause_1.sort()
    clause_2.sort()
    for i in range(len(clause_1)):
        if clause_1[i] != clause_2[i]:
            return False
    return True

def model1():
    """
    A simple ChartModel with two nodes and a transition
    """
    # build dynamical system
    model = ChartModel("Test")
    root = model.get_root()
    node_1 = root.add_simple_node('n1', 0, 0)
    node_2 = root.add_simple_node('n2', 0, 0)
    root.add_transition(node_1, node_2)
    return model

def model2():
    """
    A simple ChartModel with two nodes and a transition
    and a cycle without start
    """
    # build dynamical system
    model = model1()
    root = model.get_root()
    node_3 = root.add_simple_node('n3', 0, 0)
    node_4 = root.add_simple_node('n4', 0, 0)
    root.add_transition(node_3, node_4)
    node_5 = root.add_simple_node('n5', 0, 0)
    root.add_transition(node_4, node_5)
    root.add_transition(node_5, node_3)
    return model

def model3():
    """
    A simple ChartModel with two nodes and a transition
    and a cycle without start
    """
    # build dynamical system
    model = model2()
    root = model.get_root()
    node_s = root.add_start_node('n3', 0, 0)
    node_3 = model.get_simple_node('n3')
    root.add_transition(node_s, node_3)
    return model

def model4():
    """
    Simple chart model with one input and two free clocks
    """
    model = ChartModel("Test")
    root = model.get_root()
    node_1 = root.add_simple_node('n1', 0, 0)
    node_2 = root.add_simple_node('n2', 0, 0)
    tr0 = root.add_transition(node_1, node_2)
    tr0.set_event('hh1')
    tr0.set_condition("n3 or n4")
    node_3 = root.add_simple_node('n3', 0, 0)
    node_4 = root.add_simple_node('n4', 0, 0)
    root.add_transition(node_3, node_4)
    node_5 = root.add_simple_node('n5', 0, 0)
    tr1 = root.add_transition(node_4, node_5)
    tr2 = root.add_transition(node_5, node_3)
    tr1.set_event("hh2")
    tr1.set_condition("n1 and n3")
    node_i =  root.add_input_node('in1', 0, 0)
    tri = root.add_transition(node_i, node_1)
    tri.set_condition("n5")
    return model

def create_unfolder(model):
    """
    returns an unfolder for model
    """
    tvisit = TableVisitor(None) # no error display
    model.accept(tvisit)
    cld = CLDynSys( tvisit.tab_symb, None)
    reporter = ErrorReporter()
    cvisit = GT2Clauses(cld, reporter, True)
    model.accept(cvisit)
    # unfolder
    return CLUnfolder(cld)

# simple reporter: register errors
class ErrorReporter(object):
    """
    Simple reporter for tests
    """
    def __init__(self):
        self.error = False


    def display(self, mess):
        """
        as said
        """
        self.error = True
        #print '\n>> '+mess

class TestCLUnfolder(unittest.TestCase):
    """
    Test public and some private methods (test_method form)
    """
    def test_var_name(self):
        """
        Test of variables uncoding and decoding
        """
        model = model1()
        unfolder = create_unfolder(model)
        # naming and coding variables
        cn1 = unfolder.var_dimacs_code('n1')
        cn2 = unfolder.var_dimacs_code('n2')

        res = unfolder.get_var_name(cn1) == 'n1'
        res = res and (unfolder.get_var_name(cn2) == 'n2')
        self.assert_(res,'Error in variable name 1')

        res = unfolder.get_var_name(7) == 'n1'
        self.assert_(res,'Error in variable name 2')
        res = unfolder.get_var_name(8) == 'n2'
        self.assert_(res,'Error in variable name 3')

        res = unfolder.get_var_indexed_name(7) == 'n1_3'
        self.assert_(res,'Error in variable name 4')
        res = unfolder.get_var_indexed_name(8) == 'n2_3'
        self.assert_(res,'Error in variable name 5')



    def test_frontier(self):
        """
        Test frontier computation and encoding
        """
        # model1
        model = model1()
        unfolder = create_unfolder(model)
        # test frontier: should be n1
        cfr =  unfolder.get_frontier()[0]
        res = unfolder.get_var_name(cfr) == 'n1'
        res = res and (len(unfolder.get_frontier()) == 1)
        self.assert_(res,'Error in frontier: model1')

        # model2 (one cycle without start)
        model = model2()
        unfolder = create_unfolder(model)

        # test frontier: should be n1
        cfr =  unfolder.get_frontier()[0]
        res = unfolder.get_var_name(cfr) == 'n1'
        res = res and (len(unfolder.get_frontier()) == 1)
        self.assert_(res,'Error in frontier: model2')

        # model3: same as model2 but with a start on n3
        model = model3()
        unfolder = create_unfolder(model)

        # test frontier - should be {n1, n3}
        cfr =  unfolder.get_frontier()
        res = len(cfr) == 2
        res = res and unfolder.get_var_name(cfr[0]) == 'n1'
        res = res and unfolder.get_var_name(cfr[1]) == 'n3'
        self.assert_(res,'Error in frontier: model3')

        # model4
        model = model4()
        unfolder = create_unfolder(model)
        cfr =  unfolder.get_frontier()
        res = len(cfr) == 1
        res = res and unfolder.get_var_name(cfr[0]) == 'n3'
        self.assert_(res,'Error in frontier: model4')


    def test_free_clocks_inputs(self):
        """
        test on free clocks and input computation
        """
        # model3: no free clock, no input
        model = model3()
        unfolder = create_unfolder(model)
        lfc = unfolder.get_free_clocks()
        res = len(lfc) == 0
        self.assert_(res,'Error in free clocks: model3')
        lin = unfolder.get_inputs()
        res = len(lin) == 0
        self.assert_(res,'Error in inputs 1')

        # model4: two free clocks and one input
        model = model4()
        unfolder = create_unfolder(model)
        lfc = unfolder.get_free_clocks()
        res = len(lfc) == 2
        res = res and (unfolder.get_var_name(lfc[0]) == 'hh2')
        res = res and (unfolder.get_var_name(lfc[1]) == 'hh1')
        self.assert_(res,'Error in free clocks: model4')
        lin = unfolder.get_inputs()
        res = len(lin) == 1
        res = res and (unfolder.get_var_name(lin[0]) == 'in1')
        self.assert_(res,'Error in inputs: model4')

    def test_init_forward(self):
        """
        test forward initialization for various models and property
        """
        pass



if __name__ == "__main__":
    unittest.main()



## Filename    : TestMCLTranslators.py
## Author(s)   : Michel Le Borgne
## Created     : 9 mars 2012
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
"""
Unitary tests for the translators
"""

import unittest
import sys

from cadbiom.models.clause_constraints.CLDynSys import CLDynSys
from cadbiom.models.clause_constraints.mcl.MCLTranslators import  MCLSigExprVisitor, \
            gen_transition_clock, gen_transition_list_clock, \
            gen_simple_evolution, GT2Clauses
from cadbiom.models.biosignal.sig_expr import SigIdentExpr, \
            SigSyncBinExpr, SigWhenExpr, SigDefaultExpr
from cadbiom.models.guard_transitions.chart_model import ChartModel
from cadbiom.models.guard_transitions.analyser.ana_visitors import TableVisitor
from cadbiom.models.clause_constraints.mcl.MCLAnalyser import MCLAnalyser


# simple reporter
class ErrorRep(object):
    """
    Simple error reporter
    """
    def __init__(self):
        self.mess = ""
        self.error = False
        pass

    def display(self, mess):
        """
        set error and print
        """
        self.error = True
        self.mess += '\n>> '+mess
        print '\n DISPLAY CALL>> '+mess

TRACE_FILE = sys.stdout
#TRACE_FILE = open("/tmp/testMCLTranslator.txt",'w')

class TestTransitionClauses(unittest.TestCase):
    """
    Test of transitions into clauses
    """

    def test_no_cond(self): #OK
        """
        n1 --> n2; []
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        trans = root.add_transition(nn1, nn2)

        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit, reporter)
        TRACE_FILE.write('\ntestNoCond')
        TRACE_FILE.write( '\n\nn1 --> n2; []\n')
        htr = gen_transition_clock(trans, cl_ds, None, reporter)
        TRACE_FILE.write( 'Transition clock:'+ htr.__str__()+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        mess = 'free clocks registered:' + cl_ds.free_clocks.__str__() + '\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'reporter: '+ reporter.mess+'\n')

    def test_cond(self): #OK
        """
        n1 --> n2; [not n3]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        nn3 = root.add_simple_node('n3', 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("not n3")

        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, None)
        TRACE_FILE.write('\ntestCond')
        TRACE_FILE.write( '\n\nn1 --> n2; [not n3]'+'\n')
        htr = gen_transition_clock(trans, cl_ds, None, reporter)
        TRACE_FILE.write( 'Transition clock:' + htr.__str__()+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__() + '\n')
        mess =  'free clocks registered:' + cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'reporter: '+ reporter.mess+'\n')

    def test_no_cond_event(self): #OK
        """
        n1 --> n2; h[]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_event('h')

        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, reporter)
        TRACE_FILE.write('\ntestNoCondEvent')
        TRACE_FILE.write( '\n\nn1 --> n2; h[]'+'\n')
        htr = gen_transition_clock(trans, cl_ds, None, reporter)
        TRACE_FILE.write( 'Transition clock:'+ htr.__str__()+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__() + '\n')
        mess = 'free clocks registered:' +cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'reporter: '+ reporter.mess+'\n')

        TRACE_FILE.write( '---------- opti ----------------\n')
        sed = dict()
        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        cl_ds = CLDynSys(tvisit.tab_symb, reporter)
        htr = gen_transition_clock(trans, cl_ds, sed, reporter)
        TRACE_FILE.write( 'Transition clock:'+ htr.__str__()+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        mess = 'free clocks registered:' + cl_ds.free_clocks.__str__() + '\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'reporter: '+ reporter.mess+'\n')

    def test_cond_event(self): #OK
        """
        n1 --> n2; h[not n3]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        nn3 = root.add_simple_node('n3', 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("not n3")
        trans.set_event('h')

        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, None)
        TRACE_FILE.write('\ntestCondEvent')
        TRACE_FILE.write( '\n\nn1 --> n2; h[not n3]'+'\n')
        htr = gen_transition_clock(trans, cl_ds, None, reporter)
        TRACE_FILE.write( 'Transition clock:'+ htr.__str__()+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        mess = 'free clocks registered:'+ cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'reporter: '+ reporter.mess+'\n')

        TRACE_FILE.write( '---------- opti ----------------\n')
        sed = dict()
        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, None)
        TRACE_FILE.write('\ntestCondEvent')
        TRACE_FILE.write( '\n\nn1 --> n2; h[not n3]'+'\n')
        htr = gen_transition_clock(trans, cl_ds, sed, reporter)
        TRACE_FILE.write( 'Transition clock:'+ htr.__str__()+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        mess = 'free clocks registered:'+ cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'reporter: '+ reporter.mess+'\n')





    def test_perm_no_cond_event(self): #OK
        """
        n1/p --> n2; h[];
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_perm_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_event('h')

        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, None)
        TRACE_FILE.write('\ntestPermNoCondEvent')
        TRACE_FILE.write( '\n\nn1/p --> n2; h[]'+'\n' )
        htr = gen_transition_clock(trans, cl_ds, None, reporter)
        TRACE_FILE.write( 'Transition clock:'+htr.__str__()+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        mess =  'free clocks registered:'+ cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'reporter: '+ reporter.mess+'\n')

    def test_perm_cond_event(self): #OK
        """
        n4;
        n1/p --> n2; h[n4];
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_perm_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        nn4 = root.add_simple_node('n4', 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("n4")
        trans.set_event('h')

        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, None)
        TRACE_FILE.write('\ntestPermCondEvent')
        TRACE_FILE.write( '\n\nn1/p --> n2; h[n4]' +'\n')
        htr = gen_transition_clock(trans, cl_ds, None, reporter)
        TRACE_FILE.write( 'Transition clock:'+ htr.__str__()+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write(cla.__str__()+'\n')
        mess = 'free clocks registered:'+ cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'reporter: '+ reporter.mess+'\n')

    def test_input_cond_event(self): #OK
        """
        n4/i;
        n1/i --> n2; h[n4];
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_input_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        nn4 = root.add_input_node('n4', 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("n4")
        trans.set_event('h')

        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, None)
        TRACE_FILE.write('\ntestInputCondEvent')
        TRACE_FILE.write( '\n\nn1/i --> n2; h[n4]'+'\n')
        htr = gen_transition_clock(trans, cl_ds, None, reporter)
        TRACE_FILE.write( 'Transition clock:' +htr.__str__()+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        mess = 'free clocks registered:'+ cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'reporter: '+ reporter.mess+'\n')

    # complex events
    def test_no_cond_event_when1(self): #OK
        """
        n1 --> n2; h when n3[]
        n3;
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        nn3 = root.add_simple_node('n3', 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_event('h when n3')

        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys(tvisit.tab_symb, reporter)
        TRACE_FILE.write('\ntestNoCondEventWhen1')
        TRACE_FILE.write( '\n\nn1 --> n2; h when n3[]; n3;'+'\n')
        htr = gen_transition_clock(trans, cl_ds, None, reporter)
        TRACE_FILE.write( 'Transition clock:'+ htr.__str__()+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        mess = 'free clocks registered:' +cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'place_clocks'+ cl_ds.place_clocks.__str__()+'\n')
        TRACE_FILE.write( 'reporter: '+ reporter.mess+'\n')

    def test_no_cond_event_when2(self): #OK
        """
        n1 --> n2; h when n3[]
        n3 --> n1 ; h2 when h[]
        Error h is not a state
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        nn3 = root.add_simple_node('n3', 0, 0)
        tr1 = root.add_transition(nn1, nn2)
        tr1.set_event('h when n3')
        tr2 = root.add_transition(nn3, nn1)
        tr2.set_event('h2 when h')

        reporter = ErrorRep()
        tvisit = TableVisitor(reporter) # no error display
        model.accept(tvisit)

        cl_ds = CLDynSys(tvisit.tab_symb, reporter)
        TRACE_FILE.write('\ntestNoCondEventWhen1')
        mess =  '\n\nn1 --> n2; h when n3[]; n3 --> n1 ; h2 when h[];'+'\n'
        TRACE_FILE.write(mess)
        htr = gen_transition_clock(tr1, cl_ds, None, reporter)
        TRACE_FILE.write( 'Transition clock:'+ htr.__str__()+'\n')
        htr = gen_transition_clock(tr2, cl_ds, None, reporter)
        TRACE_FILE.write( 'Transition clock:'+ htr.__str__()+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        mess =  'free clocks registered:' +cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'place_clocks'+ cl_ds.place_clocks.__str__()+'\n')
        TRACE_FILE.write( 'reporter: '+ reporter.mess+'\n')

    def test_no_cond_event_when3(self): #OK
        """
        n1 --> n2; h when n3[]
        n3 --> n1 ; n2 when n1[]
        Error n2 is not a clock
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        nn3 = root.add_simple_node('n3', 0, 0)
        tr1 = root.add_transition(nn1, nn2)
        tr1.set_event('h when n3')
        tr2 = root.add_transition(nn3, nn1)
        tr2.set_event('n2 when n1')

        reporter = ErrorRep()
        tvisit = TableVisitor(reporter) # no error display
        model.accept(tvisit)

        cl_ds = CLDynSys(tvisit.tab_symb, reporter)
        TRACE_FILE.write('\ntestNoCondEventWhen1')
        TRACE_FILE.write( '\n\nn1 --> n2; n2 when n1[]; n3;'+'\n')
        htr = gen_transition_clock(tr1, cl_ds, None, reporter)
        TRACE_FILE.write( 'Transition clock:'+ htr.__str__()+'\n')
        htr = gen_transition_clock(tr2, cl_ds, None, reporter)
        TRACE_FILE.write( 'Transition clock:'+ htr.__str__()+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        mess = 'free clocks registered:' +cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'place_clocks'+ cl_ds.place_clocks.__str__()+'\n')
        TRACE_FILE.write( 'reporter: '+ reporter.mess+'\n')


    def test_no_cond_event_default(self): #OK
        """
        n1 --> n2; h1 when c1 default h2[c3]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        root.add_simple_node('c1', 0, 0)
        root.add_simple_node('c3', 0, 0)
        tr1 = root.add_transition(nn1, nn2)
        tr1.set_event('h when c1 default h2')
        tr1.set_condition('c3')

        reporter = ErrorRep()
        tvisit = TableVisitor(reporter) # no error display
        model.accept(tvisit)

        cl_ds = CLDynSys(tvisit.tab_symb, reporter)
        TRACE_FILE.write('\ntestNoCondEventWhen1')
        TRACE_FILE.write( '\n\nn1 --> n2; n2 when n1[]; n3;'+'\n')
        htr = gen_transition_clock(tr1, cl_ds, None, reporter)
        TRACE_FILE.write( 'Transition clock:'+ htr.__str__()+'\n')

        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        mess =  'free clocks registered:' +cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'place_clocks'+ cl_ds.place_clocks.__str__()+'\n')
        TRACE_FILE.write( 'reporter: '+ reporter.mess+'\n')


class TestTransitionList(unittest.TestCase):
    """
    As it says
    """

#    def setUp(self):
#        self.output = open('TestTransition.txt')
#        #self.output = sys.stdout


    def test_no_cond_on_out2events(self):
        """
        n1 --> n2; h1[not n4]
        n1 --> n3; h2[]
        n4 --> n1; h3[]
        gen_transition_list_clock tested
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        nn3 = root.add_simple_node('n3', 0, 0)
        nn4 = root.add_simple_node('n4', 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("not n4")
        trans.set_event('h1')
        trans = root.add_transition(nn1, nn3)
        trans.set_event('h2')
        trans = root.add_transition(nn4, nn1)
        trans.set_event('h3')

        tvisit = TableVisitor(None) # no error display/ might crash
        model.accept(tvisit)
        TRACE_FILE.write('\ntestNoCondOnOut2Events')
        mess = '\n\nn1 --> n2; h1[not n4] \nn1 --> n3; h2[]\nn4 --> n1; h3[]\n'
        TRACE_FILE.write(mess)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, None)
        trl = nn1.outgoing_trans
        sed = dict()
        htr = gen_transition_list_clock(trl, cl_ds, sed, reporter)
        TRACE_FILE.write( 'Transition clock:' +htr.__str__()+'\n')
        TRACE_FILE.write( 'NB Clauses:' +str(len(cl_ds.list_clauses))+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        mess = 'free clocks registered:'+cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)

    def test_very_simple(self): #OK to optimize
        """
        n1 --> n2; []
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        trans = root.add_transition(nn1, nn2)


        model.clean_code()
        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, None)
        TRACE_FILE.write('\ntestVerySimple')
        TRACE_FILE.write( '\n\nn1 --> n2; [] \n')
        gen_simple_evolution(nn1, cl_ds, None, reporter)
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        mess =  'free clocks registered:'+cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        model.clean_code()

    def test_simple(self):
        """
        n1 --> n2; h1[not n4]
        n1 --> n3; h2[]
        n4 --> n1; h3[]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        nn3 = root.add_simple_node('n3', 0, 0)
        nn4 = root.add_simple_node('n4', 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("not n4")
        trans.set_event('h1')
        trans = root.add_transition(nn1, nn3)
        trans.set_event('h2')
        trans = root.add_transition(nn4, nn1)
        trans.set_event('h3')

        model.clean_code()
        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, None)
        TRACE_FILE.write('\ntestSimple')
        mess =  '\n\nn1 --> n2; h1[not n4] \nn1 --> n3; h2[]\nn4 --> n1; h3[]\n'
        TRACE_FILE.write(mess)
        sed = dict()
        gen_simple_evolution(nn1, cl_ds, sed, reporter)
        TRACE_FILE.write( 'NB Clauses:' + str(len(cl_ds.list_clauses)) + '\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__() + '\n')
        mess = 'free clocks registered:'+ cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        model.clean_code()

    def test_simple_in_no_out(self):
        """
        n2 --> n1; h1[not n4]
        n4 --> n1; h3[]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        nn3 = root.add_simple_node('n3', 0, 0)
        nn4 = root.add_simple_node('n4', 0, 0)
        trans = root.add_transition(nn2, nn1)
        trans.set_condition("not n4")
        trans.set_event('h1')
        trans = root.add_transition(nn4, nn1)
        trans.set_event('h3')

        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, reporter)
        TRACE_FILE.write('\ntestSimpleInNoOut')
        TRACE_FILE.write( '\n\nn2 --> n1; h1[not n4] \nn4 --> n1; h3[]\n')
        gen_simple_evolution(nn1, cl_ds, None, reporter)
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        mess =  'free clocks registered:' + cl_ds.free_clocks.__str__() + '\n'
        TRACE_FILE.write(mess)

    def test_simple_out_no_in(self):
        """
        n1 --> n2; h1[not n4]
        n1 --> n3; h2[]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        nn3 = root.add_simple_node('n3', 0, 0)
        nn4 = root.add_simple_node('n4', 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("not n4")
        trans.set_event('h1')
        trans = root.add_transition(nn1, nn3)
        trans.set_event('h2')

        model.clean_code()
        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, None)
        TRACE_FILE.write('\ntestSimpleOutNoIn')
        TRACE_FILE.write( '\n\nn1 --> n2; h1[not n4] \nn1 --> n3; '+'\n')
        gen_simple_evolution(nn1, cl_ds, None, reporter)
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        mess =  'free clocks registered:'+ cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)

    def test_simple_no_trans(self): #OK
        """
        n1;
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node('n1', 0, 0)

        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, None)
        TRACE_FILE.write('\ntestSimpleNoTrans')
        TRACE_FILE.write( '\n\nn1; \n')
        gen_simple_evolution(nn1, cl_ds, None, reporter)
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__() + '\n')
        mess = 'free clocks registered:' + cl_ds.free_clocks.__str__() + '\n'
        TRACE_FILE.write(mess)


class TestFull(unittest.TestCase):
    """
    test full models
    """

    def test_model1(self):
        """
        n1 --> n2; h1[not n4]
        n1 --> n3; h2[]
        n4 --> n1; h3[]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        nn3 = root.add_simple_node('n3', 0, 0)
        nn4 = root.add_simple_node('n4', 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("not n4")
        trans.set_event('h1')
        trans = root.add_transition(nn1, nn3)
        trans.set_event('h2')
        trans = root.add_transition(nn4, nn1)
        trans.set_event('h3')

        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, reporter)
        TRACE_FILE.write('\ntestModel1')
        mess = '\n\nn1 --> n2; h1[not n4] \nn1 --> n3; h2[]\nn4 --> n1; h3[]\n'
        TRACE_FILE.write(mess)
        gt2clauses = GT2Clauses(cl_ds, False, reporter)
        model.accept(gt2clauses)
        TRACE_FILE.write( 'NB Clauses:' +str(len(cl_ds.list_clauses))+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        TRACE_FILE.write( 'variables'+ cl_ds.base_var_set.__str__()+'\n')
        mess = 'free clocks registered:'+ cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'place_clocks'+ cl_ds.place_clocks.__str__()+'\n')
        TRACE_FILE.write( 'inputs'+ cl_ds.inputs.__str__()+'\n')

    def test_model2(self): #OK
        """
        n1 --> n2; h1 when n2 default h2[not n4]
        n1 --> n3; h2 when n4[]
        n4 --> n1; h3[]
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_simple_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        nn3 = root.add_simple_node('n3', 0, 0)
        nn4 = root.add_simple_node('n4', 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("not n4")
        trans.set_event('h1 when n2 default h2')
        trans = root.add_transition(nn1, nn3)
        trans.set_event('h2 when n4')
        trans = root.add_transition(nn4, nn1)
        trans.set_event('h3')

        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, reporter)
        TRACE_FILE.write('\ntestModel2')
        mess =  '\n\nn1 --> n2; h1 when n2 default h2[not n4]'
        mess = mess + '\nn1 --> n3; h2 when n4[]\nn4 --> n1; h3[]\n'
        TRACE_FILE.write(mess)
        gt2clauses = GT2Clauses(cl_ds, reporter, False)
        model.accept(gt2clauses)
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        TRACE_FILE.write( 'variables'+ cl_ds.base_var_set.__str__()+'\n')
        mess = 'free clocks registered:'+ cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'place_clocks'+ cl_ds.place_clocks.__str__()+'\n')
        TRACE_FILE.write( 'inputs'+ cl_ds.inputs.__str__()+'\n')


    def test_model3(self): #OK
        """
        n4;
        n1/p --> n2; h[n4];
        """
        model = ChartModel("Test")
        root = model.get_root()
        nn1 = root.add_perm_node('n1', 0, 0)
        nn2 = root.add_simple_node('n2', 0, 0)
        nn4 = root.add_simple_node('n4', 0, 0)
        trans = root.add_transition(nn1, nn2)
        trans.set_condition("n4")
        trans.set_event('h')

        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, None)
        TRACE_FILE.write('\ntestInputCondEvent')
        TRACE_FILE.write( '\n\nn4; \nn1/p --> n2; h[n4]'+'\n')

        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, reporter)
        TRACE_FILE.write('\ntestModel2')
        TRACE_FILE.write( '\n\n\n')
        gt2clauses = GT2Clauses(cl_ds, reporter, False)
        model.accept(gt2clauses)
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        TRACE_FILE.write( 'variables'+ cl_ds.base_var_set.__str__()+'\n')
        mess =  'free clocks registered:'+ cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'place_clocks'+ cl_ds.place_clocks.__str__()+'\n')
        TRACE_FILE.write( 'inputs'+ cl_ds.inputs.__str__()+'\n')


    def test_constraints(self):
        """
        As it says
        """
        model = ChartModel("Test")
        root = model.get_root()
        aaa = root.add_simple_node('A', 0, 0)
        bbb = root.add_simple_node('B', 0, 0)
        ccc = root.add_simple_node('C', 0, 0)
        ddd = root.add_simple_node('D', 0, 0)
        trans = root.add_transition(aaa, bbb)
        trans.set_event('h1 default h2')
        trans = root.add_transition(ccc, ddd)
        trans.set_event('h3')
        cont = 'synchro(h1, h3);\nexclus(h1, h2);\nincluded(h3, h2);'
        model.constraints = cont
        tvisit = TableVisitor(None) # no error display
        model.accept(tvisit)
        reporter = ErrorRep()
        cl_ds = CLDynSys( tvisit.tab_symb, reporter)
        gt2clauses = GT2Clauses(cl_ds, reporter, False)
        model.accept(gt2clauses)
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')
        TRACE_FILE.write( 'variables'+ cl_ds.base_var_set.__str__()+'\n')
        mess = 'free clocks registered:'+ cl_ds.free_clocks.__str__()+'\n'
        TRACE_FILE.write(mess)
        TRACE_FILE.write( 'place_clocks'+ cl_ds.place_clocks.__str__()+'\n')
        TRACE_FILE.write( 'inputs'+ cl_ds.inputs.__str__()+'\n')

    def test_tgf_no_clock(self):
        """
        optimisation gain comparison
        """
        rep = ErrorRep()
        mcla = MCLAnalyser(rep)
        mcla.opti = False
        mcla.build_from_chart_file("../ucl/examples/test_tgfb_ref_300511.bcx")
        mess = '\n- NB Clauses:' + str(len(mcla.cl_dyn_sys.list_clauses))
        TRACE_FILE.write(mess)
        mcla = MCLAnalyser(rep)
        mcla.build_from_chart_file("../ucl/examples/test_tgfb_ref_300511.bcx")
        mess = '\n- NB Clauses:' + str(len(mcla.cl_dyn_sys.list_clauses))
        TRACE_FILE.write(mess)

class TestMCLSigExprVisitor (unittest.TestCase):
    """
    Test of signal expression
    """
    def test_ident1(self):
        """
        sigexp = xx
        """
        sexpr = SigIdentExpr('xx')
        cl_ds = CLDynSys(None, None)
        sexpv = MCLSigExprVisitor(cl_ds, 'Y', None)
        var = sexpr.accept(sexpv)
        TRACE_FILE.write( '\n\n sigexpr: xx'+'\n')
        TRACE_FILE.write( 'RETURN var (xx)'+ var.__str__()+'\n')
        TRACE_FILE.write( 'Clauses'+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')

    def test_bin1(self):
        """
        X or Y
        """
        sexpr1 = SigIdentExpr('x')
        sexpr2 = SigIdentExpr('y')
        sexpr = SigSyncBinExpr('or', sexpr1, sexpr2)
        cl_ds = CLDynSys(None, None)
        sexpv = MCLSigExprVisitor(cl_ds, 'Z', dict())
        var = sexpr.accept(sexpv)
        TRACE_FILE.write( '\n\n sigexpr: X or Y'+'\n')
        TRACE_FILE.write( 'RETURN var (Z)'+ var.__str__()+'\n')
        TRACE_FILE.write( 'Clauses'+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')

    def test_bin2(self):
        """
        X and Y
        """
        sexpr1 = SigIdentExpr('x')
        sexpr2 = SigIdentExpr('y')
        sexpr = SigSyncBinExpr('and', sexpr1, sexpr2)
        cl_ds = CLDynSys(None, None)
        sexpv = MCLSigExprVisitor(cl_ds, 'Z', dict())
        sexpv.output_lit = None # for output var generation
        var = sexpr.accept(sexpv)
        TRACE_FILE.writelines( '\n\n sigexpr: X and Y'+'\n')
        TRACE_FILE.write( 'RETURN var (aux var)'+ var.__str__()+'\n')
        TRACE_FILE.write( 'Clauses'+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')

    def test_bin3(self):
        """
        h1 default h2
        """
        sexpr1 = SigIdentExpr('h1')
        sexpr2 = SigIdentExpr('h2')
        sexpr = SigDefaultExpr(sexpr1, sexpr2)
        symb_tab = dict()
        symb_tab['h1'] = ('clock', -1)
        symb_tab['h2'] = ('clock', -1)
        cl_ds = CLDynSys(symb_tab, None)
        sexpv = MCLSigExprVisitor(cl_ds, None)
        #sexpv.output_lit = None # for output var generation
        var = sexpr.accept(sexpv)
        TRACE_FILE.writelines( '\n\n sigexpr: h1 default h2'+'\n')
        TRACE_FILE.write( 'RETURN var (aux var)'+ var.__str__()+'\n')
        TRACE_FILE.write( 'Clauses'+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')

    def test_bin4(self):
        """
        h1 when (a or b)
        """
        sexpr1 = SigIdentExpr('h1')
        sexpr2 = SigIdentExpr('h2')
        sexpr3 = SigIdentExpr('a')
        sexpr4 = SigIdentExpr('b')
        sexpr = SigSyncBinExpr('or', sexpr3, sexpr4)
        sexpr = SigWhenExpr(sexpr1, sexpr)
        symb_tab = dict()
        symb_tab['h1'] = ('clock', -1)
        symb_tab['h2'] = ('clock', -1)
        cl_ds = CLDynSys(symb_tab, None)
        sexpv = MCLSigExprVisitor(cl_ds, None)
        #sexpv.output_lit = None # for output var generation
        var = sexpr.accept(sexpv)
        TRACE_FILE.writelines( '\n\n sigexpr: h1 when (a or b)'+'\n')
        TRACE_FILE.write( 'RETURN var (aux var)'+ var.__str__()+'\n')
        TRACE_FILE.write( 'Clauses'+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')

    def test_cse1(self):
        """
        common subexpression elimination
        h1 when (a or b) default h2 when (b or a)
        """
        sexpr1 = SigIdentExpr('h1')
        sexpr2 = SigIdentExpr('h2')
        sexpr3 = SigIdentExpr('a')
        sexpr4 = SigIdentExpr('b')
        a_or_b1 = SigSyncBinExpr('and', sexpr3, sexpr4)
        a_or_b2 = SigSyncBinExpr('and', sexpr4, sexpr3)
        hh1 = SigWhenExpr(sexpr1, a_or_b1)
        hh2 = SigWhenExpr(sexpr2, a_or_b2)
        sexpr = SigDefaultExpr(hh1, hh2)
        TRACE_FILE.write('Formula: ' + sexpr.__str__())
        symb_tab = dict()
        symb_tab['h1'] = ('clock', -1)
        symb_tab['h2'] = ('clock', -1)
        cl_ds = CLDynSys(symb_tab, None)
        sub_exp = dict()
        sexpv = MCLSigExprVisitor(cl_ds, None, sub_exp)
        #sexpv.output_lit = None # for output var generation
        var = sexpr.accept(sexpv)
        TRACE_FILE.write( '\n\n- RETURN var (aux var)'+ var.__str__()+'\n')
        TRACE_FILE.write('\n- NB Clauses:' + str(len(cl_ds.list_clauses)))
        TRACE_FILE.write( '\n- Clauses'+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')

    def test_cse2(self):
        """
        common subexpression elimination
        h1 when (a or b) default h2 when (b or a)
        """
        hh1 = SigIdentExpr('h1')
        hh2 = SigIdentExpr('h2')
        h12 = SigDefaultExpr(hh1, hh2)
        h21 = SigDefaultExpr(hh2, hh1)
        sexpr = SigDefaultExpr(h12, h21)
        TRACE_FILE.write('Formula: ' + sexpr.__str__())
        symb_tab = dict()
        symb_tab['h1'] = ('clock', -1)
        symb_tab['h2'] = ('clock', -1)
        cl_ds = CLDynSys(symb_tab, None)
        sub_exp = dict()
        sexpv = MCLSigExprVisitor(cl_ds, None, sub_exp)
        #sexpv.output_lit = None # for output var generation
        var = sexpr.accept(sexpv)
        TRACE_FILE.write( '\n\n- RETURN var (aux var)'+ var.__str__()+'\n')
        TRACE_FILE.write('\n- NB Clauses:' + str(len(cl_ds.list_clauses)))
        TRACE_FILE.write( '\n- Clauses'+'\n')
        for cla in cl_ds.list_clauses:
            TRACE_FILE.write( cla.__str__()+'\n')



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

#    suiteFew = unittest.TestSuite()
    #suiteFew.addTest(TestMCLSigExprVisitor("testCSE2"))
    #suiteFew.addTest(Testgt2Sig("testOneTransCondEvent"))
    #suiteFew.addTest(TestTransitionClauses('testCondEvent'))
    #suiteFew.addTest(TestFull('testModel3'))
    #suiteFew.addTest(TestTransitionList("testSimple"))
    #unittest.TextTestRunner(verbosity=2).run(suiteFew)

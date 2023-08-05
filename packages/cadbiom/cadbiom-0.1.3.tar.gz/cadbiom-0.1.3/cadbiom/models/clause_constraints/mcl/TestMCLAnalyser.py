## Filename    : TestMCLAnalyser.py
## Author(s)   : Michel Le Borgne
## Created     : 03/2012
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
## Contributor(s): Geoffroy Andrieux - IRISA/IRSET
##
"""
Unitary Tests for the MCLAnalyser
"""

import unittest
import sys, os

from cadbiom.models.clause_constraints.mcl.MCLAnalyser import MCLAnalyser
from cadbiom.models.guard_transitions.simulator.chart_simul import ChartSimulator
from cadbiom.models.guard_transitions.chart_model import ChartModel
from cadbiom.models.clause_constraints.mcl.MCLQuery import MCLSimpleQuery
from cadbiom.models.clause_constraints.mcl.MCLSolutions import FrontierSolution

TRACE_FILE = sys.stdout
#TRACE_FILE = open("/tmp/testMCLAnalyzer.txt",'w')

# helper fonctions for test automation
def lit_subsol_equal(ssol1, ssol2):
    """
    @param ssol1,ssol2: list<string>
    CAREFULL: change order in lists
    """
    if len(ssol1) != len(ssol2):
        return False
    else:
        ssol1.sort()
        ssol2.sort()
        for i in range(len(ssol1)):
            if ssol1[i] != ssol2[i]:
                return False
        return True

def lit_sol_equal(sol1, sol2):
    """
    @param sol1,sol2: list<list<string>>
    CAREFULL: change order in lists
    """
    if len(sol1) != len(sol2):
        return False
    else:
        for i in range(len(sol1)):
            if not lit_subsol_equal(sol1[i], sol2[i]):
                return False
        return True


# simple reporter
class ErrorRep(object):
    """
    error reporter of the compil type
    """
    def __init__(self):
        self.context = ""
        self.error = False
        pass

    def display(self, mess):
        """
        just printing
        """
        self.error = True
        print '\n>> '+self.context+"  "+mess

    def display_info(self, mess):
        """
        just printing
        """
        print '\n-- '+mess

    def set_context(self, cont):
        """
        for transition compiling
        """
        self.context = cont



class TestMCLAnaLyzer(unittest.TestCase):
    """
    Unit tests for MCLAnalyser
    """

    def test_lit_sol_equal(self):
        """
        Test the test helper function
        """
        sol1 = [['-_lit2', '-C4', 'h2', '-A1', '-C3', '-A3', '-A2', '-A4'], \
                ['-_lit2', '-C4', '-h2', '-A1', '-C3', '-A3', '-A2', '-A4'],\
                ['-_lit2', '-C4', '-h2', '-A1', '-C3', '-A3', '-A2', '-A4']]
        sol2 = [['-_lit2', '-C4', 'h2', '-A1', '-C3', '-A3', '-A2', '-A4'], \
                ['-_lit2', '-C4', '-h2', '-A1', '-C3', '-A3', '-A2', '-A4'],\
                ['-_lit2', '-C4', '-h2', '-A1', '-C3', '-A3', '-A2', '-A4']]
        res = lit_sol_equal(sol1, sol2)
        self.assert_(res, 'Error in lit_sol equality')
        sol2 = [['-_lit2', '-C4', 'h2', '-A1', '-C3', '-A3', '-A2', '-A4'], \
                ['-_lit2', '-C4', '-h2', '-A1', '-C3', '-A3', '-A2', '-A4'],\
                ['-_lit2', 'C4', '-h2', '-A1', '-C3', '-A3', '-A2', '-A4']]
        res = lit_sol_equal(sol1, sol2)
        self.assert_(not res, 'Error in lit_sol inequality')
        # test on numbers
        sol1 = [[], [3], [], [5]]
        sol2 = [[], [3], [], [5]]
        res = lit_sol_equal(sol1, sol2)
        self.assert_(res, 'Error in lit_sol equality: number case')
        sol2 = [[], [3], [2], []]
        res = lit_sol_equal(sol1, sol2)
        self.assert_(not res, 'Error in lit_sol inequality: number case')

    def test_load1(self):
        """
        Load from a bcx file
        """
        rep = ErrorRep()
        mcla = MCLAnalyser(rep)
        mcla.build_from_chart_file("../ucl/examples/test_tgfb_ref_300511.bcx")
        res = rep.error
        self.assert_(not res, 'Error in load1')

    def test_load2(self):
        """
        Load from a cadlang file
        """
        rep = ErrorRep()
        mcla = MCLAnalyser(rep)
        file_name = "../../guard_transitions/translators/tests/tgf_cano_cmp.cal"
        mcla.build_from_cadlang(file_name)
        res = rep.error
        self.assert_(not res, 'Error in load2')

    def test_load3(self):
        """
        Load from a PID file
        """
        rep = ErrorRep()
        mcla = MCLAnalyser(rep)
        mcla.build_from_pid_file("../ucl/examples/test_plk3_pathway.xml")
        res = rep.error
        self.assert_(not res, 'Error in load3')

    def test_delay1(self):
        """
        simple delay computation
        """
        rep = ErrorRep()
        mcla = MCLAnalyser(rep)
        mcla.build_from_cadlang("examples/delay1.cal")

        f_prop =  "C3 and not C4"
        query = MCLSimpleQuery(None, None, f_prop)

        lsol = mcla.sq_solutions(query,
                                 4, 1, mcla.unfolder.get_frontier())

#        if len(lsol) > 0:
#            print 'C3 ALONE'
#            print lsol[0] #first solution _ we have two
#        else:
#            print 'NO SOLUTION C4'

        res =  len(lsol) == 2
        expected_sol = [['-_lit2', '-C4', 'h2', '-A1', '-C3', '-A3', '-A2', '-A4', '-B2', '-B3', '-_lit3', '-C2', 'C1', '_lit0', '-_lit1', 'B1'], ['-_lit2', '-C4', '-h2', '-A1', '-C3', '-A3', '-A2', '-A4', 'B2', '-B3', '-_lit3', 'C2', '-C1', '-_lit0', '-_lit1', '-B1'], ['-_lit2', '-C4', '-h2', '-A1', '-C3', '-A3', '-A2', '-A4', '-B2', 'B3', '_lit3', 'C2', '-C1', '-_lit0', '_lit1', '-B1']]
        res = res and lit_sol_equal(lsol[0].__str__(), expected_sol)
        self.assert_(not res, 'Error in C3 alone')

        f_prop = "C4 and not C3"
        query = MCLSimpleQuery(None, None, f_prop)

        lsol = mcla.sq_solutions(query,
                                 4, 1, mcla.unfolder.get_frontier())

#        if len(lsol)>0:
#            print 'C4 ALONE', len(lsol)
#            print lsol[0]
#        else:
#            print 'NO SOLUTION C4'

        res =  len(lsol) == 1
        expected_sol = [['-_lit2', '-C4', '-h2', 'A1', '-C3', '-A3', '-A2', '-A4', '-B2', '-B3', '-_lit3', '-C2', 'C1', '-_lit0', '-_lit1', 'B1'], ['-_lit2', '-C4', '-h2', '-A1', '-C3', '-A3', 'A2', '-A4', '-B2', '-B3', '-_lit3', 'C2', '-C1', '-_lit0', '-_lit1', 'B1'], ['-_lit2', '-C4', '-h2', '-A1', '-C3', 'A3', '-A2', '-A4', '-B2', '-B3', '-_lit3', 'C2', '-C1', '-_lit0', '-_lit1', 'B1'], ['_lit2', '-C4', 'h2', '-A1', '-C3', '-A3', '-A2', 'A4', '-B2', '-B3', '_lit3', 'C2', '-C1', '_lit0', '-_lit1', 'B1']]
        res = res and lit_sol_equal(lsol[0].__str__(), expected_sol)
        self.assert_(not res, 'Error in C4 alone')

        f_prop = "C3 and C4"
        query = MCLSimpleQuery(None, None, f_prop)

        lsol = mcla.sq_solutions(query,
                                 4, 1, mcla.unfolder.get_frontier())

#        if len(lsol)>0:
#            print 'C3 and C4'
#            print lsol[0]
#        else:
#            print 'NO SOLUTION'

        res =  len(lsol) == 1
        expected_sol =  [['-_lit2', '-C4', '-h2', 'A1', '-C3', '-A3', '-A2', '-A4', '-B2', '-B3', '-_lit3', '-C2', 'C1', '-_lit0', '-_lit1', 'B1'], ['-_lit2', '-C4', 'h2', '-A1', '-C3', '-A3', 'A2', '-A4', '-B2', '-B3', '-_lit3', 'C2', '-C1', '_lit0', '-_lit1', 'B1'], ['-_lit2', '-C4', '-h2', '-A1', '-C3', 'A3', '-A2', '-A4', 'B2', '-B3', '-_lit3', 'C2', '-C1', '-_lit0', '-_lit1', '-B1'], ['_lit2', '-C4', '-h2', '-A1', '-C3', '-A3', '-A2', 'A4', '-B2', 'B3', '_lit3', 'C2', '-C1', '-_lit0', '_lit1', '-B1']]
        res = res and lit_sol_equal(lsol[0].__str__(), expected_sol)
        self.assert_(not res, 'Error in C3 and C4')

    def test_delay1_w_ic(self):
        """
        simple delay computation with clock sequence
        """
        rep = ErrorRep()
        mcla = MCLAnalyser(rep)
        mcla.build_from_cadlang("examples/delay1.cal")

        st_prop = None
        inv_prop = None
        f_prop =  "C4"
        query = MCLSimpleQuery(st_prop, inv_prop, f_prop)
        lsol = mcla.sq_solutions(query, 4, 1, mcla.unfolder.get_frontier())
        sol = lsol[0]
        ic_seq = sol.extract_act_input_clock_seq()
        #print ic_seq
        expected_sol = [[], [], [], [3]]
        res =  len(lsol) != 0
        res = res and lit_sol_equal(expected_sol, ic_seq)
        self.assert_(res, 'Error clock sequence for C4')

        f_prop = "C4 and not C3"
        query = MCLSimpleQuery(None, None, f_prop)
        lsol = mcla.sq_solutions(query, 4, 1, mcla.unfolder.get_frontier())
        sol = lsol[0]
        ic_seq = sol.extract_act_input_clock_seq()
        #print ic_seq
        expected_sol = [[], [], [], [3]]
        res =  len(lsol) != 0
        res = res and lit_sol_equal(expected_sol, ic_seq)
        self.assert_(res, 'Error clock sequence for C4 and not C3')

        f_prop = "C3 and C4"
        query = MCLSimpleQuery(None, None, f_prop)
        lsol = mcla.sq_solutions(query, 4, 1, mcla.unfolder.get_frontier())
        sol = lsol[0]
        ic_seq = sol.extract_act_input_clock_seq()
        #print ic_seq
        expected_sol = [[], [3], [], []]
        res =  len(lsol) != 0
        res = res and lit_sol_equal(expected_sol, ic_seq)
        self.assert_(res, 'Error clock sequence for C4')


    def test_input1(self):
        """
        simple input computation
        """
        rep = ErrorRep()
        mcla = MCLAnalyser(rep)
        mcla.build_from_cadlang("examples/input1.cal")

        st_prop = None
        inv_prop = None
        f_prop =  "C3 and not C4"
        query = MCLSimpleQuery(st_prop, inv_prop, f_prop)
        lsol = mcla.sq_solutions(query, 4, 1, mcla.unfolder.get_frontier())
        sol = lsol[0]
        res = len(lsol) == 2
        ic_seq = sol.extract_act_input_clock_seq()
        #print ic_seq
        expected_sol = [[2], [], []]
        res = res and lit_sol_equal(expected_sol, ic_seq)
        self.assert_(res, 'Error clock/input sequence for C3 and not C4')

        f_prop = "C4 and C3"
        query = MCLSimpleQuery(None, None, f_prop)
        lsol = mcla.sq_solutions(query, 4, 1, mcla.unfolder.get_frontier())
        sol = lsol[0]
        res = len(lsol) == 1
        ic_seq = sol.extract_act_input_clock_seq()
        #print ic_seq
        expected_sol = [[], [2], [], []]
        res = res and lit_sol_equal(expected_sol, ic_seq)
        self.assert_(res, 'Error clock/input sequence for C3 and C4')


    def test_unflatten(self):
        """
        Test unflatten trajectory
        """
        rep = ErrorRep()
        mcla = MCLAnalyser(rep)
        mcla.build_from_cadlang("examples/delay1.cal")

        st_prop = None
        inv_prop = None
        f_prop = "C3"
        query = MCLSimpleQuery(st_prop, inv_prop, f_prop)
        lsol = mcla.sq_solutions(query, 4, 1, mcla.unfolder.get_frontier())
        ufl = lsol[0].unflatten()
        expected_ufl = [[-1, -2, 3, -4, -5, -6, -7, -8, -9, -10, -11, -12, 13, 14, -15, 16], [-1, -2, -3, -4, -5, -6, -7, -8, 9, -10, -11, 12, -13, -14, -15, -16], [-1, -2, -3, -4, -5, -6, -7, -8, -9, 10, 11, 12, -13, -14, 15, -16]]
        res = lit_sol_equal(expected_ufl, ufl)
        self.assert_(res, 'Error unflatten')


    def test_dimacs_frontier(self):
        """
        frontier solution in DIMACS form
        """
        rep = ErrorRep()
        mcla = MCLAnalyser(rep)
        prop = 'p15INK4b and p21CIP1'
        query = MCLSimpleQuery(None, None, prop)

        mcla.build_from_chart_file("../ucl/examples/tgf_211011_man.bcx")
        # lsol: list<dimacs frontier solution>
        lsol = mcla.test_dimacs_frontier_sol(query, 8, 1)
        lforbidden = []
        for sol in lsol:
            forbid = []
            for varcod in sol.frontier_values:
                if varcod > 0:
                    forbid.append(-varcod)
            lforbidden.append(forbid)
        # try another solution
        query.set_dim_start(lforbidden)
        lsol2 = mcla.test_dimacs_frontier_sol(query, 8, 1)
        # comparison: solution are ordered and must be different
        sol = lsol[0]
        sol2 = lsol2[0]
        res = True
        # remains true if all components are equal (equal solutions)
        for i in range(sol.get_solution_size()):
            res = res and (sol.get_solution()[i] == sol2.get_solution()[i])
        self.assert_(not res, 'Error dimacs_frontier: solutions not different')

    def test_prune(self):
        """
        pruning a solution
        """
        rep = ErrorRep()
        mcla = MCLAnalyser(rep)
        prop = 'p15INK4b and p21CIP1'
        query = MCLSimpleQuery(None, None, prop)

        mcla.build_from_chart_file("../ucl/examples/tgf_211011_man.bcx")
        # lsol: list<dimacs frontier solution>
        lsol = mcla.test_dimacs_frontier_sol(query, 8, 10)
        small_sol = mcla.less_activated_solution(lsol)
        cpt1 = 0
        for varcod in small_sol.get_solution():
            if varcod > 0:
                cpt1 += 1
        # check solution
        start = []
        for ssol in small_sol.frontier_values:
            start.append([ssol])
        query.set_dim_start(start)
        res = mcla.sq_is_satisfiable(query, 8)
        self.assert_(res, 'Small sol is not a solution')
        # find if there are solutions with same unactivated places
        for ssol in small_sol.frontier_values:
            if ssol < 0:
                start.append([ssol])
        query.set_dim_start(start)
        res = mcla.sq_is_satisfiable(query, 8)
        self.assert_(res, 'No solution with same unactivated places')
        prune = mcla.test_prune_frontier_solution(small_sol, query, 8)
        # compare sizes
        cpt2 = 0
        for varcod in prune.get_solution():
            if varcod > 0:
                cpt2 += 1
        res = (cpt2 <= cpt1)
        self.assert_(res, 'Prune do not reduce nb of activated places')




    def test_cam_no_clock(self):
        """
        test cam without clocks
        """
        # solving
        rep = ErrorRep()
        mcla = MCLAnalyser(rep)
        prop = 'p15INK4b and p21CIP1'
        dir_n = "../../guard_transitions/translators/tests/"
        f_name = dir_n + "tgf_cano_noclock_cmp.cal"
        mcla.build_from_cadlang(f_name)
        mcla.unfolder.set_stats()
        query = MCLSimpleQuery(None, None, prop)
        cam_list = mcla.mac_search(query, 10)
        res = len(cam_list) == 8
        self.assert_(res, 'Incorrect number of cam')
        list_expected = [['SP1', 'betaglycan__dimer___intToMb', 'SMAD4_nucl', 'importinbeta', 'MIZ_1', 'DAB2', 'TGFBfamily__dimer___active_exCellRegion', 'TGFBR2__dimer___active_intToMb', 'Axin_SMAD3', 'SMAD4_cy', 'SMAD2_3', 'FKBP12_TGFBR1__dimer___inactive_intToMb', 'CTGF'],
                         ['SP1', 'betaglycan__dimer___intToMb', 'SMAD4_nucl', 'MIZ_1', 'DAB2', 'TGFBfamily__dimer___active_exCellRegion', 'TGFBR2__dimer___active_intToMb', 'Axin_SMAD3', 'SMAD4_cy', 'importinalpha', 'SMAD2_3', 'FKBP12_TGFBR1__dimer___inactive_intToMb', 'CTGF'],
                         ['SP1', 'betaglycan__dimer___intToMb', 'SMAD4_nucl', 'MIZ_1', 'DAB2', 'TGFBfamily__dimer___active_exCellRegion', 'NUP214', 'TGFBR2__dimer___active_intToMb', 'Axin_SMAD3', 'SMAD4_cy', 'SMAD2_3', 'FKBP12_TGFBR1__dimer___inactive_intToMb', 'CTGF'],
                         ['SP1', 'betaglycan__dimer___intToMb', 'SMAD4_nucl', 'MIZ_1', 'DAB2', 'TGFBfamily__dimer___active_exCellRegion', 'TGFBR2__dimer___active_intToMb', 'Axin_SMAD3', 'SMAD4_cy', 'SMAD2_3', 'NUP153', 'FKBP12_TGFBR1__dimer___inactive_intToMb', 'CTGF'],
                         ['SP1', 'betaglycan__dimer___intToMb', 'SMAD4_nucl', 'importinbeta', 'FOXO1_3a_4_active_nucl', 'DAB2', 'CEBPB', 'TGFBfamily__dimer___active_exCellRegion', 'TGFBR2__dimer___active_intToMb', 'Axin_SMAD3', 'SMAD4_cy', 'SMAD2_3', 'FKBP12_TGFBR1__dimer___inactive_intToMb', 'CTGF', 'FOXG1'],
                         ['SP1', 'betaglycan__dimer___intToMb', 'SMAD4_nucl', 'FOXO1_3a_4_active_nucl', 'DAB2', 'CEBPB', 'TGFBfamily__dimer___active_exCellRegion', 'TGFBR2__dimer___active_intToMb', 'Axin_SMAD3', 'SMAD4_cy', 'importinalpha', 'SMAD2_3', 'FKBP12_TGFBR1__dimer___inactive_intToMb', 'CTGF', 'FOXG1'],
                         ['SP1', 'betaglycan__dimer___intToMb', 'SMAD4_nucl', 'FOXO1_3a_4_active_nucl', 'DAB2', 'CEBPB', 'TGFBfamily__dimer___active_exCellRegion', 'NUP214', 'TGFBR2__dimer___active_intToMb', 'Axin_SMAD3', 'SMAD4_cy', 'SMAD2_3', 'FKBP12_TGFBR1__dimer___inactive_intToMb', 'CTGF', 'FOXG1'],
                         ['SP1', 'betaglycan__dimer___intToMb', 'SMAD4_nucl', 'FOXO1_3a_4_active_nucl', 'DAB2', 'CEBPB', 'TGFBfamily__dimer___active_exCellRegion', 'TGFBR2__dimer___active_intToMb', 'Axin_SMAD3', 'SMAD4_cy', 'SMAD2_3', 'NUP153', 'FKBP12_TGFBR1__dimer___inactive_intToMb', 'CTGF', 'FOXG1']
                         ]
        list_obtained = []
        for cam in cam_list:
            list_obtained.append(cam.activated_frontier)
        res = lit_sol_equal(list_expected, list_obtained)
        self.assert_(res, 'Incorrect list of MAC (no clock)')


    def test_cam_clock(self):
        """
        cam with clocks
        """
        # solving
        rep = ErrorRep()
        mcla = MCLAnalyser(rep)
        prop = 'p15INK4b'
        #p = "C3"
        f_name = "../../guard_transitions/translators/tests/tgf_cano_cmp.cal"
        mcla.build_from_cadlang(f_name)
        #mcla.build_from_cadlang("examples/delay2.cal")
        #mcla.unfolder.set_stats()
        query = MCLSimpleQuery(None, None, prop)
        cam_list = mcla.mac_search(query, 10)
        list_expected = [['SMAD4_nucl', 'FOXO1_3a_4_active_nucl', 'CEBPB', 'TGFB_TGFBR2_TGFBR1_DAB2_active_intToMb', 'SMAD2_3', 'FOXG1'],
                         ['SP1', 'SMAD4_nucl', 'MIZ_1', 'TGFB_TGFBR2_TGFBR1_DAB2_active_intToMb', 'SMAD2_3'],
                         ['SP1', 'betaglycan__dimer___intToMb', 'SMAD4_nucl', 'Caveolin_1', 'MIZ_1', 'TRAP_1_TGFBR1__dimer___inactive_intToMb', 'AP2B2', 'TGFBR2__dimer___active_intToMb', 'PML_SARA_SMAD2_3_earlyendosome', 'TGFBfamily__dimer___active_exCellRegion', 'SMAD7_SMURF1_2_nucl', 'CTGF'],
                         ['betaglycan__dimer___intToMb', 'SMAD4_nucl', 'Caveolin_1', 'FOXO1_3a_4_active_nucl', 'TRAP_1_TGFBR1__dimer___inactive_intToMb', 'AP2B2', 'CEBPB', 'TGFBR2__dimer___active_intToMb', 'PML_SARA_SMAD2_3_earlyendosome', 'TGFBfamily__dimer___active_exCellRegion', 'SMAD7_SMURF1_2_nucl', 'CTGF', 'FOXG1']
                         ]
        list_obtained = []
        for cam in cam_list:
            list_obtained.append(cam.activated_frontier)
        res = lit_sol_equal(list_expected, list_obtained)
        self.assert_(res, 'Incorrect list of MAC (clock)')




    def test_valid_simul_delay(self):
        """
        Test simulation of the delay example
        """
        rep = ErrorRep()
        mcla = MCLAnalyser(rep)
        mcla.build_from_cadlang("examples/delay1.cal")

        st_prop = None
        inv_prop = None
        f_prop =  "C3 and  C4"
        query = MCLSimpleQuery(st_prop, inv_prop, f_prop)
        # lsol: list<RawSolution>
        lsol = mcla.sq_solutions(query, 4, 1, mcla.unfolder.get_frontier())
        sol = lsol[0]
        f_sol = FrontierSolution.from_raw(sol)

        # independant simulation
        chm = ChartModel(" ")
        chm.build_from_cadlang("examples/delay1.cal", rep)
        sim = ChartSimulator()
        sim.build(chm, True, rep)
        sim.simul_init_places(f_sol.activated_frontier)
        sim.set_act_input_stream(f_sol.ic_sequence)
        sim.set_reachable_prop(f_prop)

        while True:
            try:
                sim.simul_step()
            except Exception, exc:
                exc_txt = exc.__str__()
                self.assert_(exc_txt == 'STOP', "Error: " + exc_txt)
                break
        # test if property reached
        res = sim.check_reachable_property()
        self.assert_(res, "Property not reached")


    def test_valid_simul_input(self):
        """
        Test simulation of the input example
        """
        rep = ErrorRep()
        mcla = MCLAnalyser(rep)
        mcla.build_from_cadlang("examples/input1.cal")

        st_prop = None
        inv_prop = None
        f_prop =  "C3 and  C4"
        query = MCLSimpleQuery(st_prop, inv_prop, f_prop)
        lsol = mcla.sq_solutions(query, 4, 1, mcla.unfolder.get_frontier())
        sol = lsol[0]
        f_sol = FrontierSolution.from_raw(sol)

        # independant simulation
        chm = ChartModel(" ")
        chm.build_from_cadlang("examples/input1.cal", rep)
        sim = ChartSimulator()
        sim.build(chm, True, rep)
        sim.simul_init_places(f_sol.activated_frontier)
        sim.set_act_input_stream(f_sol.ic_sequence)
        sim.set_reachable_prop(f_prop)

        while True:
            try:
                sim.simul_step()
            except Exception, exc:
                exc_txt = exc.__str__()
                self.assert_(exc_txt == 'STOP', "Error: " + exc_txt)
                break
        # test if property reached
        res = sim.check_reachable_property()
        self.assert_(res, "Property not reached")


    def test_cam_delay_save(self):
        """
        Test save on the delay example
        """
        rep = ErrorRep()
        mcla = MCLAnalyser(rep)
        mcla.build_from_cadlang("examples/delay1.cal")

        f_prop =  "C3 and C4"
        query = MCLSimpleQuery(None, None, f_prop)
        macwic = mcla.mac_search(query, 10)

        f_out = file("x_file", 'w')
#        print macwic[0].activated_frontier
#        print macwic[0].ic_sequence
#        print '---------------'

        macwic[0].save(f_out)
        r_front = FrontierSolution.from_file("x_file")
#        print r_front.activated_frontier
#        print r_front.ic_sequence
        res = r_front.has_same_frontier(macwic[0])
        self.assert_(res, "Frontier solutions differ after read")
        os.remove("x_file")


    def test_cam_inhibitor(self):
        """
        test
        """
        rep = ErrorRep()
        mcla = MCLAnalyser(rep)
        mcla.build_from_cadlang("examples/delay3.cal")

        f_prop =  "C3 and C4"
        query = MCLSimpleQuery(None, None, f_prop)
        macwic = mcla.mac_search(query, 10)
        exp_act_front = ['A1', 'C1', 'B1']
        res = lit_subsol_equal(exp_act_front, macwic[0].activated_frontier)
        self.assert_(res, "Bad cam frontier solution")
        exp_timing = ["%", "% h2", "%", "%"]
        obt_timing = []
        obt_timing.extend(macwic[0].ic_sequence)
        res = lit_subsol_equal(exp_timing, obt_timing)
        self.assert_(res, "Bad cam timing solution")
        res = mcla.is_strong_activator(macwic[0], query)
        # it is not a strong activator
        self.assert_(not res, "Not a strong activator")
        inhib = mcla.mac_inhibitor_search(macwic[0], query, 10)
#        print 'INHIB:'
#        for isol in inhib:
#            print isol

        exp_act_front1 = ['D', 'A1', 'C1', 'B1']
        obt_act_front = inhib[0].activated_frontier
        obt_timing = []
        obt_timing.extend(inhib[0].ic_sequence)
        res = lit_subsol_equal(exp_act_front1, obt_act_front)
        if res:
            exp_timing = ["%", "% h2", "%", "%"]
            res = res and lit_subsol_equal(exp_timing, obt_timing)
            self.assert_(res, "Bad inhib timing solution")
        else:
            res = lit_subsol_equal(exp_act_front, obt_act_front)
            exp_timing = ["% h2", "% h2", "%", "%"]
            res = res and lit_subsol_equal(exp_timing, obt_timing)
            self.assert_(res, "Bad inhib timing solution")

        obt_act_front = inhib[1].activated_frontier
        obt_timing = []
        obt_timing.extend(inhib[1].ic_sequence)
        res = lit_subsol_equal(exp_act_front, obt_act_front)
        if res:
            exp_timing = ["% h2", "% h2", "%", "%"]
            res = res and lit_subsol_equal(exp_timing, obt_timing)
            self.assert_(res, "Bad inhib timing solution")
        else:
            res = lit_subsol_equal(exp_act_front1, obt_act_front)
            exp_timing = ["%", "% h2", "%", "%"]
            res = res and lit_subsol_equal(exp_timing, obt_timing)
            self.assert_(res, "Bad inhib timing solution")

        res = mcla.is_strong_inhibitor(inhib[0], query)
        # it is a strong inhibitor
        self.assert_(res, "Bad answer - strong inhibitor")



## Filename    : MCLAnalyser.py
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
Main class to perform dynamic analysis of Cadbiom chart models.
"""
from cadbiom.antlr3 import ANTLRFileStream, CommonTokenStream

from cadbiom.models.guard_transitions.translators.chart_xml import \
        MakeModelFromXmlFile

from cadbiom.models.guard_transitions.translators.chart_xml_pid import \
        MakeModelFromPidFile

from cadbiom.models.guard_transitions.analyser.ana_visitors import TableVisitor
from cadbiom.models.clause_constraints.mcl.MCLTranslators import  GT2Clauses
from cadbiom.models.clause_constraints.mcl.CLUnfolder import CLUnfolder
from cadbiom.models.clause_constraints.mcl.MCLSolutions import \
        extract_dimacs_init_frontier, MCLException

from cadbiom.models.clause_constraints.CLDynSys import CLDynSys
from cadbiom.models.guard_transitions.translators.cadlangLexer import cadlangLexer
from cadbiom.models.guard_transitions.translators.cadlangParser import cadlangParser
from cadbiom.models.guard_transitions.chart_model import ChartModel
from cadbiom.models.clause_constraints.mcl.MCLSolutions import FrontierSolution
from cadbiom.models.clause_constraints.mcl.MCLQuery import MCLSimpleQuery

#import random
import sys
TRACEFILE = sys.stdout

class MCLAnalyser(object):
    """
    query a UCL dynamical system and analyses solutions
    """
    NB_SOL = 10  # for mac search - to be optimized??

    def __init__(self, report):
        """
        Constructor - the built analyser is void
        @param report: a standard reporter
        """
        self.cl_dyn_sys = None     # dynamical system in clause constraint form
        self.unfolder = None       # computation management: unfolding
        self.reporter = report     # for generic error display
        self.opti = True           # turn on optimizations for translation

    # building
    def build_from_chart_model(self, model):
        """
        Build an MCLAnalyser from a chartmodel object
        @param model: object - ChartModel
        """
        # reloading a MCLAnalyser is forbidden - create a new one
        if self.unfolder:
            raise MCLException("This MCLAnalyser is already initialized")
        # building CLsys
        vtab = TableVisitor(self.reporter)
        model.accept(vtab)
        if self.reporter.error:
            return
        clds = CLDynSys( vtab.tab_symb, self.reporter)
        if self.reporter.error:
            return
        comp_visitor = GT2Clauses(clds, self.reporter, self.opti)
        model.accept(comp_visitor)
        if self.reporter.error:
            return
        self.cl_dyn_sys = clds

        # build unfolder
        self.unfolder = CLUnfolder(clds)

    def build_from_chart_file(self, file_name):
        """
        Build an MCLAnalyser from a .bcx file
        @param file_name: str - path of the .bcx file
        """
        parsing = MakeModelFromXmlFile(file_name)
        # chart model
        cmodel = parsing.get_model()
        self.build_from_chart_model(cmodel)

    def build_from_pid_file(self,
                            file_name, has_clock=True, ai_interpretation=0):
        """
        Build an MCLAnalyser from a .xml file of PID database
        @param file_name: str - path of .xml file
        """
        parsing = MakeModelFromPidFile(file_name,
                                    self.reporter, has_clock, ai_interpretation)
        # chart model
        cmodel = parsing.get_model()
        self.build_from_chart_model(cmodel)

    def build_from_cadlang(self, file_name):
        """
        Build an MCLAnalyser from a .cal file of PID database
        @param file_name: str - path of .cal file
        """
        creporter = self.reporter
        fstream = ANTLRFileStream(file_name)
        lexer = cadlangLexer(fstream)
        lexer.set_error_reporter(creporter)
        parser = cadlangParser(CommonTokenStream(lexer))
        parser.set_error_reporter(creporter)
        model = ChartModel(file_name)
        parser.cad_model(model)
        # chart model
        cmodel = parser.model
        self.build_from_chart_model(cmodel)



    # solution processing
    def less_activated_solution(self, dimacs_solution_list):
        """
        return the solution with the less activated  states
        @param dimacs_solution_list: either a DimacsFrontierSol or DimacsActFrontSol list
        @return: a solution object of the type in the list
        """
        if not dimacs_solution_list:
            self.reporter.display(
                    "Trying to find a smallest solution without solution list")
            return None

        smallest_sol = dimacs_solution_list[0]
        la_number = smallest_sol.nb_activated()

        for sol in dimacs_solution_list[1:]:
            if sol.nb_activated() < la_number:
                smallest_sol = sol
                la_number = sol.nb_activated()
        return smallest_sol

    def __prune_frontier_solution(self, fsol, query, max_step):
        """
        take a frontier condition  which induces property prop and reduce the
        number of activated variables from this solution while inducing prop,
        @param fsol: a DimacsFrontierSol
        @param query: MCLQuery
        @return: a DimacsfrontierSol

        ASSERT: fsol is a frontier condition implying sq satisfiability
        """

#        # for debug - too expansive to be activated anytime
#        start = []
#        for s in fsol.frontier_values:
#            start.append([s])
#        assert(self.sq_is_satisfiable(query, max_step))
        to_prune = fsol
        current_len = fsol.nb_activated() # number of act. places in solution
        next_len = 0
        is_pruned = True

        while is_pruned:
            # find at most 10 ic frontier solutions with same no activated
            # frontier place - return current_small if no more sol
            dimacs_solutions = self.__solve_with_inact_fsolution(
                                                                 to_prune,
                                                                 query,
                                                                 max_step)
            if len(dimacs_solutions) == 1:
                return dimacs_solutions[0]  # found no new solutions
            # seach for less activated solutions
            next_small = self.less_activated_solution(dimacs_solutions)
            next_len = next_small.nb_activated()
            is_pruned = current_len > next_len
            if is_pruned:
                to_prune = next_small
                current_len = next_len
        # never reach this point
        raise MCLException("_prune_frontier_solution: what happened??")

    # for unit test
    def test_prune_frontier_solution(self, fsol, query, max_step):
        """
        For tests only
        """
        return self.__prune_frontier_solution(fsol, query, max_step)


    # generic solver for simple queries
    def sq_is_satisfiable(self, query, max_step):
        """
        @param query: MCLQuery
        @param max_step: int - length of unfolding

        @return: boolean

        @warning: no_frontier places are initialized to False in simple queries
        """
        # setting parameters
        self.unfolder.reset()
        self.unfolder.set_initial_property(query.start_prop)
        self.unfolder.set_dim_initial_property(query.dim_start)
        self.unfolder.set_current_property(query.inv_prop)
        self.unfolder.set_dim_current_property(query.dim_inv)
        self.unfolder.set_final_property(query.final_prop)
        self.unfolder.set_dim_final_property(query.dim_final)
        self.unfolder.set_variant_property(query.variant_prop)
        self.unfolder.set_dim_variant_property(query.dim_variant_prop)

        self.unfolder.set_minimal_steps(query.steps_before_reach)
        # go
        return self.unfolder.squery_is_satisfied(max_step)


    def sq_solutions(self, query, max_step, max_sol, vvars):
        """
        @param query: MCLQuery
        @param max_step: int - length of unfolding
        @param vvars: variables for which solutions must differ:
                    list<int> Dimacs code
        @return: a list of RawSolution objects

        @warning:  no_frontier places are initialized to False in simple queries
            except if initial condition.

        @warning: if the query includes variant constraints, the horizon (max_step) is
            automatically adjusted to min(max_step, len(variant_constraints)).
        """
        # setting parameters
        self.unfolder.reset()
        self.unfolder.set_initial_property(query.start_prop)
        self.unfolder.set_dim_initial_property(query.dim_start)
        self.unfolder.set_current_property(query.inv_prop)
        self.unfolder.set_dim_current_property(query.dim_inv)
        self.unfolder.set_final_property(query.final_prop)
        self.unfolder.set_dim_final_property(query.dim_final)
        self.unfolder.set_variant_property(query.variant_prop)
        self.unfolder.set_dim_variant_property(query.dim_variant_prop)

        self.unfolder.set_minimal_steps(query.steps_before_reach)
        # go
        return self.unfolder.squery_solve(vvars, max_step, max_sol)


    def sq_frontier_solutions(self, query, max_step, max_sol):
        """
        Compute active frontier places and timing
        @param query: MCLQuery
        @param max_step: int - length of unfolding
        @param max_sol: max number of solutions
        @return:  list<FrontierSolution>  set of frontier place names which
                                      must be activated for implying query satisfaction
        @warning:  no_frontier places are initialized to False

        """
        vvars = self.unfolder.get_frontier()
        l_sol = self.sq_solutions(query, max_step, max_sol, vvars)
        out = []
        for sol in l_sol:
            fsol = FrontierSolution.from_raw(sol)
            out.append(fsol)
        return out

    def __sq_dimacs_frontier_solutions(self, query, max_step, max_sol):
        """
        @param query: MCLQuery
        @param max_step: int - length of unfolding
        @param max_sol:int - max number of solutions for each solve
        @return:  list<DimacsFrontierSol>

        """
        frontier = self.unfolder.get_frontier()
        lsol = self.sq_solutions(query, max_step, max_sol, frontier)
        return extract_dimacs_init_frontier(lsol)


    # only for unit test
    def test_dimacs_frontier_sol(self, query, max_step, max_sol):
        """ for test only """
        return self.__sq_dimacs_frontier_solutions(query, max_step, max_sol)



    def __solve_with_inact_fsolution(self, fsolution, query, max_step):
        """
        frontier states not activated in  fsolution (frontier solution) forced
        to be False at start solve and return frontier solution list with this constraint
        @param fsolution: list<DimacsFrontierSol> -  one solution to obtain the property in dimacs
        @param query: current query
        @param max_step: int - horizon

        @precondition: fsolution is a frontier solution for the query
        """

        # collect inactivated places
        final_dsol = \
            [[var] for var in fsolution.frontier_values if var < 0]
        if query.dim_start:
            query.set_dim_start(final_dsol + query.dim_start)
        else:
            query.set_dim_start(final_dsol)
        # must return fsol if no more solution
        return self.__sq_dimacs_frontier_solutions(query, max_step,
                                                   MCLAnalyser.NB_SOL)


    # only for unit test
    def test_solve_with_inact_fsolution(self, fsolution, query, max_step):
        """
        unit test accessible
        """
        self.__solve_with_inact_fsolution(fsolution, query, max_step)



    def __mac_exhaustive_search(self, query, nb_step):
        """
        @param query: MCLQuery
        @param nb_step: int - number of dynamical step
        @return list<DimacsFrontierSol>
        """
        # list of timed minimal activation conditions on frontier (dimacs code)
        # i.e list<DimacsFrontierSol>
        mac_list = []

        reachable = self.sq_is_satisfiable(query, nb_step)
        # get the minimum number of steps for reachability
        min_step = self.unfolder.get_current_step() - 1
        query.set_steps_before_reach(min_step)

        while reachable :
            # compute forbidden solutions: already discovered macs
            forbidden_sol = []
            for dsol in mac_list:
                dimacs_clause = []
                for var in dsol.frontier_values:
                    if var > 0:
                        dimacs_clause.append(-var)       # OR( not var)
                forbidden_sol.append(dimacs_clause)

            # reachable - solutions differ on frontier: 2 different solutions
            # to avoid a all activated solution - lfsol:list<DimacsFrontierSol>
            query.set_dim_start(forbidden_sol)
            lfsol = self.__sq_dimacs_frontier_solutions(query, nb_step, 2)
            if len(lfsol)>0:
                small_sol = self.less_activated_solution(lfsol)
                start = []
                for ssol in small_sol.frontier_values:
                    start.append([ssol])
                #assert(self.sq_is_satisfiable(query, nb_step))
            else:
                reachable = False
                break

            current_mac = self.__prune_frontier_solution(small_sol,
                                                         query, nb_step)
            if current_mac.nb_activated() == 0:
                reachable = False
            else :
                mac_list.append(current_mac)
        return mac_list



    def next_mac(self, query, nb_step):
        """
        if st_prop contains negation of mac conditions,
        return a different mac if any
        same parameters as __mac_exhaustive_search
        Used for search on cluster

        @param query: MCLQuery
        @param nb_step: int - number of dynamical step
        @return: a list of variables (list<string>)
        """
        lfsol = self.__sq_dimacs_frontier_solutions(query, nb_step, 2)
        if len(lfsol)>0:
            small_fsol = self.less_activated_solution(lfsol)
        else:
            return None

        current_mac = self.__prune_frontier_solution(small_fsol,
                                                     query,
                                                     nb_step)
        vmac = FrontierSolution.from_dimacs_front_sol(current_mac)
        return vmac

    def mac_search(self, query, nb_step):
        """
        @param query: MCLQuery
        @param nb_step: int - number of dynamical step
        @return: list<FrontierSolution>
        """
        mac_list = self.__mac_exhaustive_search(query, nb_step)
        # convert to FrontierSolution list
        vmac_list = []
        for mac in mac_list:
            vmac = FrontierSolution.from_dimacs_front_sol(mac)
            vmac_list.append(vmac)
        return vmac_list

    def is_strong_activator(self, act_sol, query):
        """
        test if an activation condition is a strong one (independent of timing)
        @param act_sol: FrontierSolution with activation condition
        @param query: the query used for act_sol condition
        """
        nb_step = len(act_sol.ic_sequence) - 1
        query_1 = MCLSimpleQuery.from_frontier_sol_same_timing(act_sol,
                                                              self.unfolder)
        inv_prop = 'not('+query.final_prop+')'
        query_2 = MCLSimpleQuery(None, inv_prop, None)
        query_1 = query_2.merge(query_1)
        return not(self.sq_is_satisfiable(query_1, nb_step))

    def next_inhibitor(self, mac, query):
        """
        if st_prop contains negation of mac conditions,
        return a different mac if any
        same parameters as __mac_exhaustive_search
        Used for search on cluster

        @param mac: FrontierSolution
        @param query: MCLQuery
        @param nb_step: int - number of dynamical step
        @return: a list of variables (list<string>)
        """
        # query with mac init frontier places and  timing
        inh_query1 = MCLSimpleQuery.from_frontier_sol_same_timing(mac,
                                                                  self.unfolder)
        # query with negation of final prop as invariant property
        if not query.final_prop:
            raise MCLException("Query must have a final property")
        if not query.inv_prop:
            inv_prop = "not (" + query.final_prop + ")"
        else:
            inv_prop = query.inv_prop + "and (not (" + query.final_prop +"))"
        inh_query2 = MCLSimpleQuery(None, inv_prop, None)
        # init + timing + final property not reachable
        inh_query = inh_query1.merge(inh_query2)
        nb_step = len(inh_query.variant_prop)
        assert(nb_step == len(mac.ic_sequence))

        # search solutions - diseable aux clauses
        self.unfolder.set_include_aux_clauses(False)
        next_inhib = self.next_mac(inh_query, nb_step)
        self.unfolder.set_include_aux_clauses(True)
        return next_inhib


    def mac_inhibitor_search(self, mac, query, max_sol):
        """
        Search inhibitors for a mac scenario

        @param mac: the mac
        @param query: the property enforced by the mac
        @param max_sol: limit on the number of solutions
        @param max_sol: maximum number of solutions

        @return: a list of frontier solution
        """
        # query with mac init frontier places and  timing
        inh_query1 = MCLSimpleQuery.from_frontier_sol(mac)
        # query with negation of final prop as invariant property
        if not query.final_prop:
            raise MCLException("Query must have a final property")
        if not query.inv_prop:
            inv_prop = "not (" + query.final_prop + ")"
        else:
            inv_prop = query.inv_prop + "and (not (" + query.final_prop +"))"
        inh_query2 = MCLSimpleQuery(None, inv_prop, None)
        # init + timing + final property not reachable
        inh_query = inh_query1.merge(inh_query2)

        nb_step = len(inh_query.variant_prop)
        assert(nb_step == len(mac.ic_sequence))
        # search solutions - diseable aux clauses
        self.unfolder.set_include_aux_clauses(False)
#        lsol = self.sq_frontier_solutions(inh_query, nb_step, max_sol)
        lsol = self.mac_search(inh_query, nb_step)
        self.unfolder.set_include_aux_clauses(True)
        return lsol

    def is_strong_inhibitor(self, in_sol, query):
        """
        test if an activation condition inhibitor is a trong one
        (i.e independent of timing)
        @param in_sol: FrontierSolution with activation condition and inhibition
        @param query: the property which is inhibed
        """
        nb_step = len(in_sol.ic_sequence) - 1
        query_1 = MCLSimpleQuery.from_frontier_sol_new_timing(in_sol,
                                                              self.unfolder)
        # negation of the query
        if not query.final_prop:
            raise MCLException("Query must have a final property")
        if not query.inv_prop:
            inv_prop = "not (" + query.final_prop + ")"
        else:
            inv_prop = query.inv_prop + "and (not (" + query.final_prop +"))"
        inh_query = MCLSimpleQuery(None, inv_prop, None)
        query_1 = inh_query.merge(query_1)
        return not self.sq_is_satisfiable(query_1, nb_step)


# helper functions
def only_in_l1(ll1, ll2):
    """
    @param ll1: list<any> - list of element
    @param ll2: list<any> - list of element
    @return: only_l1 list<any> - list of element that are only in the first list (l1\l2)
    """
    only_l1 = []
    for el1 in ll1:
        if el1 not in ll2:
            only_l1.append(el1)
    only_l1.sort()
    return only_l1

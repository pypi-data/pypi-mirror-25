## Filename    : CLUnfolder.py
## Author(s)   : Michel Le Borgne
## Created     : 22 mars 2012
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
## Contributor(s): Geoffroy Andrieux IRSET
##
"""
Main engine for constraint unfolding and solving
"""
#from pyCryptoMS import CryptoMS
from pycryptosat import Solver as CryptoMS
from cadbiom.models.biosignal.translators.gt_visitors import compile_cond, compile_event
from cadbiom.models.clause_constraints.CLDynSys import Clause, Literal
from cadbiom.models.clause_constraints.mcl.MCLSolutions import RawSolution, MCLException
from cadbiom import commons as cm

# C++ API
from _cadbiom import shift_clause, shift_dynamic, forward_code, \
                     forward_init_dynamic

# Standard imports
from logging import DEBUG
import itertools as it

LOGGER = cm.logger()

class CLUnfolder(object):
    """
    Dynamic constraints unfolding management
    ========================================
    Each variable is coded as an integer (in var_code_table and var_list).
    Each clause is represented as a list of signed integers (DIMACS coding).
    During unfolding, clauses are shifted either to the future (forward) or
    to the past (backward). The shift operator is a simple addition
    of self.__shift_step. The shift direction depends only on initializations.
    self.__shift_step depends on the number of variables so it is impossible
    to add variables while generating a trajectory unfolding.

    Glossary
    ========
    - ground variables/ground dimacs code: variables at time 0/their encoding.
    - solution: a solution of the logical dynamic constraint from SAT solver
    - state vector: list of DIMACS code of original (not shifted) variables
      corresponding to a step.
    - trajectory: list of state_vectors
    """

    def __init__(self, sys):
        self.__dyn_sys = sys # symbolic clause dynamic system

        # shift_step equal to the total number of coded variables
        self.__shift_step_init = sys.get_var_number() # shift step of system
        self.__shift_step = self.__shift_step_init    #  current shift/step
        self.__locked = False
        self.__current_step = 1
        self.__steps_before_check = 0
        self.__include_aux_clauses = True

        # assign a DIMACS code number to each variable (invariant)
        self.__lit_cpt = self.__shift_step +1 # counter for aux. var. coding
        self.__var_code_table = dict()            # name -> DIMACS code
        self.__var_list = ['##']                  # DIMACS code -> name - != 0
        cpt = 1
        for svar in sys.base_var_set:
            self.__var_list.append(svar)
            self.__var_code_table[svar] = cpt
            cpt += 1
        assert(cpt == self.__shift_step + 1)

        # same tools for auxiliary variables from property compilation
        self.__aux_code_table = dict()            # name 2 code
        self.__aux_list = []                      # code to name

        # list  no_frontier place DIMACS codes
        self.__no_frontier_init = []
        for nfp in self.__dyn_sys.no_frontier:
            self.__no_frontier_init.append([- self.__var_code_table[nfp]])

        # ordered list of frontier place DIMACS codes for extraction (inv)
        self.__frontier = []
        for frp in self.__dyn_sys.frontier:
            self.__frontier.append(self.__var_code_table[frp])
        self.__frontier.sort()

        # ordered list of input places DIMACS code for extraction (inv)
        self.__inputs = []
        for inp in self.__dyn_sys.inputs:
            self.__inputs.append(self.__var_code_table[inp])
        self.__inputs.sort()

        # ordered list of free clocks DIMACS code for extraction (invariant)
        self.__free_clocks = []
        for fcl in self.__dyn_sys.free_clocks:
            self.__free_clocks.append(self.__var_code_table[fcl])
        self.__free_clocks.sort()

        # properties to be checked
        self.__initial_property = None            # string
        self.__dim_initial = None                 # list of dimacs clauses
        self.__final_property = None              # idem
        self.__dim_final = None
        self.__invariant_property = None          # idem
        self.__dim_invariant = None
        self.__variant_property = None            # list<logic formulas>
        self.__dim_variant = None                 # list<list<dimacs clauses>>
        # list of variant temporal constraints in Dimacs ground code
        self.__list_variant_constraints = None    # list<list<dimacs clauses>>

        # constraints - logical constraints
        # result from unfolding of base constraints
        self.__dynamic_constraints = []        # DIMACS clauses: X' = f(X,H,I)
        self.__initial_constraints = []        # DIMACS clauses: C(X_0)
        self.__final_constraints   = []        # idem: C(X_n)
        self.__invariant_constraints = []      # DIMACS clauses: C(X_i))
        self.__variant_constraints = []        # variant constraints along traj.
        self.__shift_direction = None          # forward or backward

        # statistics on solver
        self.__stats = False
        self.__nb_vars = 0
        self.__nb_clauses = 0



    def reset(self):
        """
        Reset the unfolder before a new query
        """
        self.__initial_property = None
        self.__dim_initial = None
        self.__final_property = None
        self.__dim_final = None
        self.__invariant_property = None
        self.__dim_invariant = None
        self.__variant_property = None
        self.__dim_variant = None
        self.list_variant_constraints = None
        self.__steps_before_check = 0
        self.__shift_direction = None
        self.__locked = False

    def set_stats(self):
        """
        Enable solver statistics
        """
        self.__stats = True
        self.__nb_vars = 0
        self.__nb_clauses = 0

    def unset_stats(self):
        """
        disable solver statistics
        """
        self.__stats = False

    def _stats(self):
        """
        print solver statistics
        """
        print "\n NB Variables in solver: ", self.__nb_vars
        print "NB Clauses in solver: ", self.__nb_clauses

    def set_minimal_steps(self, nb_steps):
        """
        For reachability optimisation. number of shift before checking
        """
        self.__steps_before_check = nb_steps

    def set_include_aux_clauses(self, val):
        """
        Include auxiliary clause to eliminate undesirable solutions
        If A->B has clock h an aux constraint added is h included in h when A
        Must be set to False for inhibitors computations
        """
        self.__include_aux_clauses = val

    # internal variable access for tests
    def get_dynamic_constraints(self):
        """
        For tests: returns coded dynamic constraints
        """
        return self.__dynamic_constraints

    def get_initial_constraints(self):
        """
        For tests: returns coded initial constraints
        """
        return self.__initial_constraints

    def get_invariant_constraints(self):
        """
        For tests: returns coded invariant constraints
        """
        return self.__invariant_constraints

    def get_variant_constraints(self):
        """
        For tests: returns coded variant constraints
        """
        return self.__variant_constraints

    def get_final_constraints(self):
        """
        For tests: returns coded final constraints
        """
        self.__final_constraints

    # variables management
    def var_dimacs_code(self, var_name):
        """
        returns dimacs code of (string) var_name variable
        """
        return self.__var_code_table[var_name]

    def get_system_var_number(self):
        """
        number of variables in the clause constraint dynamical system
        """
        return self.__dyn_sys.get_var_number()

    def get_var_number(self):
        """
        number of principal variables (properties excluded) in the unfolder
        """
        return len(self.__var_list) -1

    def get_var_name(self, var_num):
        """
        @param var_num: DIMACS literal coding of an initial variable
        @return: name of the variable
        """
        if var_num < 0:
            varnum1 = -var_num
        else: varnum1 = var_num
        var_code = (varnum1 - 1) % self.__shift_step + 1
        if var_code <= self.__shift_step_init: # variable from initial system
            return self.__var_list[var_code]
        else: # auxiliary variable introduced by properties compilation
            return self.__aux_list[var_code - self.__shift_step_init -1]
            #raise MCLException("Not a DIMACS code of an initial variable")

    def get_var_indexed_name(self, var_num):
        """
        @param var_num: DIMACS literal coding
        @return: name of the variable with time index
        """
        if var_num < 0:
            varnum1 = -var_num
        else: varnum1 = var_num
        var_code = (varnum1 - 1) % self.__shift_step + 1
        var_step = (varnum1 - var_code)/self.__shift_step
        if var_code <= self.__shift_step_init:
            return self.__var_list[var_code] + '_%s'% var_step
        else:
            index = var_code - self.__shift_step_init -1
            return self.__aux_list[index] + '_%s'% var_step

    def get_frontier(self):
        """
        @return: the DIMACS code of the frontier variables
        """
        return self.__frontier

    def get_free_clocks(self):
        """
        @return: the DIMACS code of the free_clocks variables
        """
        return self.__free_clocks

    def get_inputs(self):
        """
        @return: the DIMACS code of the input variables
        """
        return self.__inputs

    def get_shift_direction(self):
        """
        @return: string "FORWARD" or "BACKWARD"
        """
        return self.__shift_direction

    def get_shift_step(self):
        """
        @return: the shift step ss (if n is X_0 code, n+ss is X_1 code)
        """
        return self.__shift_step

    def get_shift_step_init(self):
        """
        @return: the shift step ss (if n is X_0 code, n+ss is X_1 code)
        """
        return self.__shift_step_init

    def get_current_step(self):
        """
        @return: the current number of unfolding
        """
        return self.__current_step



    # translation from names to num codes
    # the translation depends on the shift direction
    def __forward_code(self, clause):
        """
        numerically code a clause with the numeric code found in self.__var_code_table for
        a base variable x and numeric_code + shift_step for x'
        variable integer coding increases in futur steps
        @param clause: a Clause object
        @return: the DIMACS coding of the forward shifted clause
        """

        # Old API
        # num_clause = []
        # for lit in clause.list_of_literals:
        #     if lit.name[-1] == '`': # t+1 variable
        #         num_clause.append(
        #             -(self.__var_code_table[lit.name[:-1]] + self.__shift_step) \
        #             if not lit.sign \
        #             else (self.__var_code_table[lit.name[:-1]] + self.__shift_step)
        #         )
        #     else: # t variable
        #         num_clause.append(
        #             -self.__var_code_table[lit.name] \
        #             if not lit.sign else self.__var_code_table[lit.name]
        #         )
        # return num_clause

        # New API via C++ module
        #print(forward_code(clause, self.__var_code_table, self.__shift_step))
        return forward_code(clause, self.__var_code_table, self.__shift_step)


    def __backward_code(self, clause):
        """
        numerically code a clause with the numeric code found in self.__var_code_table+ shift_step for
        a base variable x and numeric_code for x'
        variable integer coding increases in past steps
        @param clause: a Clause object
        @return: the DIMACS coding of the backward shifted clause
        """
        num_clause = []
        for lit in clause.list_of_literals:
            if not lit.name[-1] == '`': # t variable
                num_clause.append(-(self.__var_code_table[lit.name] + self.__shift_step) \
                if not lit.sign \
                else (self.__var_code_table[lit.name] + self.__shift_step))
            else:  # t+1 variable
                num_clause.append(-self.__var_code_table[lit.name[:-1]] \
                if not lit.sign \
                else self.__var_code_table[lit.name[:-1]])
        return num_clause

    def __code_clause(self, clause):
        """
        numerically code a clause with the numeric code found in
        self.__var_code_table for variables in the dynamic system and
        self.__aux_code_table for other variables assume all variables
        are basic variables (t=0)
        @warning: MODIFIES SHIFT_STEP if auxiliary variables are present (numeric code)
        """
        num_clause = []
        for lit in clause.list_of_literals:
            name = lit.name
            if self.__var_code_table.has_key(name):
                var_cod = self.__var_code_table[name]
            elif self.__aux_code_table.has_key(name):
                var_cod = self.__aux_code_table[name]
            else: # create an auxiliary variable - modifies shift_step
                self.__shift_step += 1
                self.__aux_code_table[name] = self.__shift_step
                var_cod = self.__shift_step
                self.__aux_list.append(name)
            if lit.sign:
                lit_code = var_cod
            else:
                lit_code = - var_cod
            num_clause.append(lit_code)
        return num_clause

    # dynamics initialisations
    def __forward_init_dynamic(self):
        """
        set dynamic constraints for a forward one step: X1 = f(X0)
        """

        # Old API
        # self.__dynamic_constraints = []

        # num_clause_list = \
        #     [self.__forward_code(clause)
        #      for clause in self.__dyn_sys.list_clauses]
        #
        # if self.__include_aux_clauses:
        #     num_clause_list += \
        #         [self.__forward_code(clause)
        #          for clause in self.__dyn_sys.aux_list_clauses]
        #
        # self.__dynamic_constraints.append(num_clause_list)

        # New API via C++ module
        # TODO: take a look at __backward_init_dynamic & __backward_code
        if self.__include_aux_clauses:
            self.__dynamic_constraints = \
                forward_init_dynamic(self.__dyn_sys.list_clauses,
                                     self.__var_code_table,
                                     self.__shift_step,
                                     self.__dyn_sys.aux_list_clauses)
        else:
            self.__dynamic_constraints = \
                forward_init_dynamic(self.__dyn_sys.list_clauses,
                                     self.__var_code_table,
                                     self.__shift_step)

    def __backward_init_dynamic(self):
        """
        set dynamic constraints for a forward one step: X0 = f(X1)
        """
        self.__dynamic_constraints = []

        num_clause_list = \
            [self.__backward_code(clause)
             for clause in self.__dyn_sys.list_clauses]

        if self.__include_aux_clauses:
            num_clause_list += \
                [self.__backward_code(clause)
                 for clause in self.__dyn_sys.aux_list_clauses]

        self.__dynamic_constraints.append(num_clause_list)

    # shifting: implementation of the shift operator
    def __shift_clause(self, ncl):
        """
        shift a clause one step
        @param ncl: DIMACS clause
        @warning: lock the unfolder
        """
        self.__locked = True  # shift_step must be frozen

        # Old API
        # Less efficient with abs()
        # return [(abs(lit) + self.__shift_step) * (-1 if lit < 0 else 1) for lit in ncl]
        # More efficient with ternary assignment
        # return [(lit + self.__shift_step) if lit > 0 else (lit - self.__shift_step)
        #         for lit in ncl]

        # New API via C++ module
        return shift_clause(ncl, self.__shift_step)

    def __m_shift_clause(self, ncl, nb_steps):
        """
        shift a clause many step
        @param ncl: DIMACS clause
        @param nb_steps: number of shifts
        @warning: lock the unfolder
        """
        self.__locked = True  # shift_step must be frozen

        return [(lit + self.__shift_step * nb_steps) if lit > 0
                else (lit - self.__shift_step * nb_steps) for lit in ncl]

    def __shift_dynamic(self):
        """
        Shift clauses representing the dynamics X' = f(X,I,C)
        """

        # Old API
        # self.__dynamic_constraints.append(
        #   [self.__shift_clause(clause)
        #    for clause in self.__dynamic_constraints[-1]]
        # )

        # New API via C++ module
        self.__dynamic_constraints.append(
            shift_dynamic(
                self.__dynamic_constraints[-1],
                self.__shift_step
            )
        )

    def __shift_initial(self):
        """
        Shift initialisation condition
        """

        self.__initial_constraints = \
            [self.__shift_clause(clause)
             for clause in self.__initial_constraints]

    def __shift_final(self):
        """
        Shift final property
        """

        self.__final_constraints = \
            [self.__shift_clause(clause)
             for clause in self.__final_constraints]


    def __shift_invariant(self):
        """
        Shift invariant property
        """
        if not self.__invariant_constraints == []:

            # Old API
            # self.__invariant_constraints.append(
            #     [self.__shift_clause(clause)
            #      for clause in self.__invariant_constraints[-1]]
            # )

            # New API via C++ module
            self.__invariant_constraints.append(
                shift_dynamic(
                    self.__invariant_constraints[-1],
                    self.__shift_step
                )
            )

    def __shift_variant(self):
        """
        shift variant property - depends on unfolding direction
        """
        if not self.__list_variant_constraints:
            return
        if self.__shift_direction == "FORWARD":
            index = self.__current_step # constraint t0 already included
            current_constraint = self.__list_variant_constraints[index]
            # shift constraint at current step and add to var_constraints
            for clause in current_constraint:
                s_clause = self.__m_shift_clause(clause, index)
                self.__variant_constraints.append(s_clause)
                return
        elif self.__shift_direction == 'BACKWARD':
            raise MCLException("Not yet implemented")
        else:
            raise MCLException("Shift incoherent data: "+self.__shift_direction)


    def shift(self):
        """
        assume shift direction is set - shift one step
        """
        self.__shift_dynamic()
        self.__shift_invariant()
        self.__shift_variant()
        if self.__shift_direction == 'FORWARD':
            self.__shift_final()
        elif self.__shift_direction == 'BACKWARD':
            self.__shift_initial()
        else:
            raise MCLException("Shift incoherent data: "+self.__shift_direction)
        self.__current_step += 1

    # coding of properties
    def __compile_property(self, property_text):
        """
        compile a property (logical formula) into clauses
        type checking uses the symbol table of dyn_sys
        error reporting through the dyn_sys reporter
        MODIFIES __lit_cpt for numbering of auxiliary variables (not coding)
        """
        if self.__locked:
            raise MCLException("Trying to compile property while unfolder is locked")

        # syntax analyser and type checker
        # property_text, symb_t, reporter
        tree_prop = compile_cond(property_text,
                                 self.__dyn_sys.symb_tab,
                                 self.__dyn_sys.report)
        # avoid name collisions of aux var
        prop_visitor = CLPropertyVisitor(self.__lit_cpt)
        tree_prop.accept(prop_visitor)
        self.__lit_cpt = prop_visitor.cpt # avoid name collisions of aux var
        return prop_visitor.clauses

        # coding of properties

    def __compile_event(self, property_text):
        """
        compile an event (biosignal expression) into clauses
        type checking uses the symbol table of dyn_sys
        error reporting through the dyn_sys reporter
        MODIFIES __lit_cpt for numbering of auxiliary variables (not coding)
        """
        if self.__locked:
            mess = "Trying to compile property while unfolder is locked"
            raise MCLException(mess)
        reporter = self.__dyn_sys.report
        symb_t = self.__dyn_sys.symb_tab
        # syntax analyser and type checker
        (tree_prop, ste, fcl) = compile_event(property_text, symb_t,
                                              True,  reporter)
        # avoid name collisions of aux var
        prop_visitor = CLPropertyVisitor(self.__lit_cpt)
        tree_prop.accept(prop_visitor)
        self.__lit_cpt = prop_visitor.cpt # avoid name collisions of aux var
        return prop_visitor.clauses

    def set_initial_property(self, property_text):
        """
        @param property_text: string - litteral boolean expression
        """
        self.__initial_property = property_text

    def set_dim_initial_property(self, dimacs_clause_list):
        """
        set initial property with a DIMACS representation
        @param dimacs_clause_list:
        """
        self.__dim_initial = dimacs_clause_list

    def __init_initial_constraint_0(self, no_frontier_init=True):
        """
        if initial property is set, generate constraints clauses in numeric form
        base variable form - we have to wait until all variables are num coded
        before shifting anything!!
        """
# OLD
#        self.__initial_constraints = []
#        if no_frontier_init:
#            # initialize no frontier places to False
#            for nfp in self.__no_frontier_init:
#                self.__initial_constraints.append(nfp)
#        if self.__initial_property:
#            # compile initial property
#            l_clauses = self.__compile_property(self.__initial_property)
#            # compile numeric form
#            for clause in l_clauses:
#                self.__initial_constraints.append(self.__code_clause(clause))
#        # dimacs aux initial properties
#        dim_init = self.__dim_initial
#        if dim_init:
#            self.__initial_constraints = self.__initial_constraints + dim_init

        self.__initial_constraints = list()

        # initialize no frontier places to False
        if no_frontier_init:
            self.__initial_constraints += [elem for elem in self.__no_frontier_init]

        if self.__initial_property:
            # compile initial property
            # compile numeric form
            self.__initial_constraints += [self.__code_clause(clause) for clause in self.__compile_property(self.__initial_property)]

        # dimacs aux initial properties
        if self.__dim_initial:
            self.__initial_constraints += self.__dim_initial

    def set_final_property(self, property_text):
        """
        @param property_text: string - litteral boolean expression
        """
        self.__final_property = property_text

    def set_dim_final_property(self, dimacs_clause_list):
        """
        set final property with a DIMACS representation
        @param dimacs_clause_list:
        """
        self.__dim_final = dimacs_clause_list

    def __init_final_constraint_0(self):
        """
        if final property is set, generate constraints clauses in numeric form
        base variable used - we have to wait until all variables are num coded
        before shifting anything!!
        """

        self.__final_constraints = []
        if self.__final_property:
            # compile initial (X0) property
            l_clauses = self.__compile_property(self.__final_property)
            # compile numeric form
            for clause in l_clauses:
                self.__final_constraints.append(self.__code_clause(clause))
        dim_fin = self.__dim_final
        if dim_fin:
            self.__final_constraints = self.__final_constraints + dim_fin

    def set_current_property(self, property_text):
        """
        @param property_text: string - litteral boolean expression
        """

        self.__invariant_property = property_text

    def set_dim_current_property(self, dimacs_clause_list):
        """
        set final property with a DIMACS representation
        @param dimacs_clause_list:
        """

        self.__dim_invariant = dimacs_clause_list

    def __init_invariant_constraint_0(self):
        """
        if trajectory property is set, generate constraints clauses in numeric form
        base variable used - we have to wait until all variables are num coded
        before shifting anything!!
        """
        self.__invariant_constraints = []
        if self.__invariant_property:
            # compile initial (X0) property
            l_clauses = self.__compile_property(self.__invariant_property)
            # compile numeric form
            init_const = []
            for clause in l_clauses:
                init_const.append(self.__code_clause(clause))
            self.__invariant_constraints.append(init_const)
        d_inv = self.__dim_invariant
        if d_inv:
            self.__invariant_constraints = self.__invariant_constraints + d_inv

    def set_variant_property(self, var_prop):
        """
        @param var_prop: a list of logical formulas representing time varying
        constraints. Each constraint uses ground (not shifted) variables.
        The order of the list of constraints is always time increasing.
        """
        self.__variant_property = var_prop

    def set_dim_variant_property(self, dim_var_prop):
        """
        @param dim_var_prop: a list list of dimacs clauses representing time
        varying constraints. Each constraint uses ground (not shifted)
        variable codes.
        """
        self.__dim_variant = dim_var_prop

    def __init_variant_constraints_0(self):
        """
        if variant_property is set, compile each property into clauses and
        encode these clauses. Clauses already in dimacs form are added.
        The two variant constraint forms must be compatible (same length)
        """
        # coding of variant properties
        if self.__variant_property:
            self.__list_variant_constraints = []
            for prop in self.__variant_property:
                # compile initial (X0) property
                l_clauses = self.__compile_event(prop)
                # encode the clauses
                dim_cl = []
                for clause in l_clauses:
                    dim_cl.append(self.__code_clause(clause))
                self.__list_variant_constraints.append(dim_cl)

            # add variant properties in dimacs form
            if self.__dim_variant:
                vp_length = len(self.__variant_property)
                if vp_length != len(self.__dim_variant):
                    mess = "Incoherent variant properties"
                    raise MCLException(mess)

                for i in range(vp_length):
                    c_var = self.__list_variant_constraints[i]
                    c_var = c_var + self.__dim_variant[i]
                    self.__list_variant_constraints[i] = c_var
        else:
            if self.__dim_variant:
                self.__list_variant_constraints = self.__dim_variant
        # initialisation
        if self.__list_variant_constraints:
            if self.__shift_direction == "FORWARD":
                self.__variant_constraints = self.__list_variant_constraints[0]
            elif  self.__shift_direction == "BACKWARD":
                raise MCLException("Not yet implemented")
            else:
                raise MCLException("Shift incoherent data: "
                                   + self.__shift_direction)

    # whole initialisations
    def init_forward_unfolding(self):
        """
        initialisation before generating constraints - forward trajectory
        """
        self.__shift_direction = 'FORWARD'
        self.__current_step = 1
        self.__shift_step = self.__shift_step_init  # back to basic!
        self.__aux_code_table = dict()              # flush auxiliary variables
        self.__aux_list = []                        # idem

        # init properties to generate all variable num codes
        self.__init_initial_constraint_0()
        self.__init_final_constraint_0()
        self.__init_invariant_constraint_0()
        self.__init_variant_constraints_0()

        # now shifting is possible
        self.__forward_init_dynamic()
        self.__shift_final()
        self.__shift_invariant()


    def init_backward_unfolding(self):
        """
        initialisation before generating constraints - backward trajectory
        """
        self.__shift_direction = 'BACKWARD'
        self.__current_step = 0
        self.__shift_step = self.__shift_step_init  # back to basic!
        self.__aux_code_table = dict()              # flush auxiliary variables
        self.__aux_list = []                        # idem

        # init properties to generate all variable num codes
        self.__init_initial_constraint_0()
        self.__init_final_constraint_0()
        self.__init_invariant_constraint_0()
        self.__init_variant_constraints_0()

        # now shifting is possible
        self.__backward_init_dynamic()
        self.__shift_initial()
        self.__shift_invariant()

    # for debug
    def vars_in_clause(self, clause):
        """
        DEBUG
        """
        lvar = []
        for var in clause:
            lvar.append(self.get_var_indexed_name(var))
        return lvar


    # solver interface
    def __load_solver(self, solv):
        """
        add all the current clauses in solver solv
        """

        # New API via C++ module
        solv.add_clauses(self.__final_constraints)
        solv.add_clauses(it.chain(*self.__invariant_constraints))
        solv.add_clauses(self.__variant_constraints)
        solv.add_clauses(it.chain(*self.__dynamic_constraints))
        solv.add_clauses(self.__initial_constraints)

        # Less efficient alternative
        # solv.add_clauses([clause for lcl in self.__invariant_constraints
        #                   for clause in lcl])
        # solv.add_clauses([clause for lcl in self.__dynamic_constraints
        #                   for clause in lcl])

        # Old API
        # Clauses are added one by one
        # final
        #[solv.add_clause(clause) for clause in self.__final_constraints]

        # trajectory invariant
        #[solv.add_clause(clause) for lcl in self.__invariant_constraints
        # for clause in lcl]

        # trajectory variant
        #[solv.add_clause(clause) for clause in self.__variant_constraints]

        # dynamics
        #[solv.add_clause(clause) for lcl in self.__dynamic_constraints
        # for clause in lcl]

        # initial
        #[solv.add_clause(clause) for clause in self.__initial_constraints]

        # LOGGING
        if LOGGER.getEffectiveLevel() == DEBUG:
            # final
            LOGGER.debug("Load new solver !!")
            LOGGER.debug(">> final: " + str(len(self.__final_constraints)))
            LOGGER.debug(str(self.__final_constraints))

            # trajectory invariant
            LOGGER.debug(">> trajectory inv: " + str(len(self.__invariant_constraints)))
            LOGGER.debug(str(self.__invariant_constraints))

            # trajectory variant
            LOGGER.debug(">> trajectory var: " + str(len(self.__variant_constraints)))
            LOGGER.debug(str(self.__variant_constraints))

            # dynamics
            LOGGER.debug(">> dynamics: " + str(len(self.__dynamic_constraints)))
            LOGGER.debug(str(self.__dynamic_constraints))

            # initial
            LOGGER.debug(">> initial: " + str(len(self.__initial_constraints)))
            LOGGER.debug(str(self.__initial_constraints))


    def __constraints_satisfied(self):
        """
        @return: boolean
        """
        LOGGER.debug("__constraints_satisfied ?")
        solver = CryptoMS()
        # Load Solver and all clauses
        self.__load_solver(solver)
        # If stats are activated (never besides in test environment):
        # sync local data (nb vars, nb clauses with solver state)
        if self.__stats:
            if solver.nb_vars() > self.__nb_vars:
                self.__nb_vars = solver.nb_vars()
            if solver.nb_clauses() > self.__nb_clauses:
                self.__nb_clauses = solver.nb_clauses()
        # Is problem satisfiable ?
        return solver.is_satisfiable()


    def __msolve_constraints(self, max_sol, vvars):
        """
        @param max_sol: int - the max number of solution returned
        @param vvars: variables for which the solver must find different solutions(dimacs code)
        @return: a list of RawSolution
        """
        solver = CryptoMS()
        self.__load_solver(solver)

        if self.__stats:
            if solver.nb_vars() > self.__nb_vars:
                self.__nb_vars = solver.nb_vars()
            if solver.nb_clauses() > self.__nb_clauses:
                self.__nb_clauses = solver.nb_clauses()

        if LOGGER.getEffectiveLevel() == DEBUG:
            LOGGER.debug("__msolve_constraints :: vvars : " + str(vvars))
            LOGGER.debug("__msolve_constraints :: max_sol : " + str(max_sol))
            lintsol = solver.msolve_selected(max_sol, vvars)
            LOGGER.debug("__msolve_constraints :: lintsol : " + str(lintsol))
            return [RawSolution(solint, self) for solint in lintsol]

        return [RawSolution(solint, self)
                for solint in solver.msolve_selected(max_sol, vvars)]

    # dynamic properties
    def squery_is_satisfied(self, max_step):
        """
        Ask the SAT solver
        @param max_step: int - the horizon
        """
        # initialization
        self.init_forward_unfolding()
        # horizon adjustment
        if self.__list_variant_constraints:
            max_step = min(max_step, len(self.__list_variant_constraints)-1)
        # loop
        if self.__invariant_property and not self.__final_property :
            while self.__current_step <= max_step:
                self.shift()
            return self.__constraints_satisfied()
        else :
            while self.__current_step <= max_step:
                if self.__constraints_satisfied():
                    return True
                self.shift()
            return self.__constraints_satisfied()



    def squery_solve(self, vvars, max_step, max_sol):
        """
        Assert a query is loaded (start_condition, inv_condition, final_condition)
        @param vvars: variables on which different solutions must differ
        @param max_step: bounded horizon for computations
        @param max_sol: max number of solutions to be computed

        @return: list of RawSolution objects
        """
        if LOGGER.getEffectiveLevel() == DEBUG:
            LOGGER.debug("squery_solve :: vvars : " + str(vvars))
        # initialization
        self.init_forward_unfolding()
        # horizon adjustment
        if self.__list_variant_constraints:
            max_step = min(max_step, len(self.__list_variant_constraints)-1)
        # loop
        if self.__invariant_property and not self.__final_property :
            while self.__current_step <= max_step:
                self.shift()
            # return l_rawsol
            return self.__msolve_constraints(max_sol, vvars)

        else : # reachability
            l_rawsol = []
            # check and correct for incoherent data on step number
            if self.__steps_before_check > max_step:
                self.__steps_before_check = max_step - 1
            # shift without checking (optimization)
            while self.__current_step <= self.__steps_before_check:
                self.shift()
            # search for solutions at each step
            while self.__current_step <= max_step:
                lsol = self.__msolve_constraints(max_sol, vvars)
                if len(lsol)>0:
                    l_rawsol = l_rawsol + lsol
                self.shift()
            return l_rawsol


###############################################################################
class CLPropertyVisitor(object):
    """
    SigExpression on states and events into a set of clauses
    Type checking must be done.
    """

    def __init__(self, aux_cpt=0):
        self.cpt = aux_cpt         # for auxiliary variable naming
        self.clauses = []          # generated clauses
        self.top = True            # root of the formula?

    def visit_sig_ident(self, tnode):
        """
        ident -> literal
        """
        name = tnode.name
        new_lit = Literal(name, True)
        if self.top:
            self.clauses.append(Clause([new_lit]))
            return None
        return new_lit

    def visit_sig_not(self, node):
        """
        translate a not
        """
        top = self.top
        self.top = False
        # compile operand to nl <=> formula
        newl = node.operand.accept(self)
        notnl = newl.lit_not()
        if top: # we are at the root
            self.clauses.append(Clause([notnl]))
            return None
        return notnl # if we are not at the root

    def visit_sig_sync(self, binnode):
        """
        translate a binary (or/and) expression
        """
        top = self.top
        self.top = False
        # the internal nodes will be affected with the name '_lit'
        name = '_lit'+str(self.cpt)
        self.cpt += 1
        newl = Literal(name, True)
        notnl = Literal(name, False)
        # recursive visits
        operator = binnode.operator
        nl1 = binnode.left_h.accept(self)
        notnl1 = nl1.lit_not()
        nl2 = binnode.right_h.accept(self)
        notnl2 = nl2.lit_not()
        # clauses generation
        if operator == 'and':   # x = lh and rh
            self.clauses.append(Clause([nl1, notnl]))           # not x or not lh
            self.clauses.append(Clause([nl2, notnl]))           # not x or not rh
            self.clauses.append(Clause([notnl1, notnl2, newl])) # x or not lh or not rh

        if operator == 'or':    # x = lh or rh
            self.clauses.append(Clause([notnl1, newl]))        # x or not lh
            self.clauses.append(Clause([notnl2, newl]))        # x or not rh
            self.clauses.append(Clause([nl1, nl2, notnl]))     # not x or not lh or not rh

#        self.clauses.append(cl1)
#        self.clauses.append(cl2)
#        self.clauses.append(cl3)
        if top:
            self.clauses.append(Clause([newl]))
            return None
        return newl

    def visit_sig_const(self, exp):
        """
        translate a constant expression
        """
        top = self.top
        if top:
            if exp.is_const_false():
                raise TypeError("No constant False property allowed")
            else: # always present or satisfied
                return None
        # the internal nodes will be affected with the name '_lit'
        name = '_lit'+str(self.cpt)
        self.cpt += 1
        newl = Literal(name, True)

        # clause generation
        if exp.value:
            clause = newl  # x = True
        else:
            clause = newl.lit_not()
        self.clauses.append(Clause([clause]))
        return newl

    # time operators
    def visit_sig_default(self, exp):
        """
        default translation
        """
        top = self.top
        self.top = False
        # the internal nodes will be affected the name '_lit'
        name = '_lit'+str(self.cpt)
        self.cpt += 1
        newl = Literal(name, True)
        notnl = Literal(name, False)
        # recursive visits
        nl1 = exp.left_h.accept(self)
        notnl1 = nl1.lit_not()
        nl2 = exp.right_h.accept(self)
        notnl2 = nl2.lit_not()
        # clause generation: x = lh or rh
        cl1 = Clause([notnl1, newl])        # x or not lh
        cl2 = Clause([notnl2, newl])        # x or not rh
        cl3 = Clause([nl1, nl2, notnl])     # not x or not lh or not rh

        self.clauses.append(cl1)
        self.clauses.append(cl2)
        self.clauses.append(cl3)
        if top:
            self.clauses.append(Clause([newl]))
            return None
        return newl

    def visit_sig_when(self, exp):
        """
        when translation
        """
        top = self.top
        self.top = False
        # the internal nodes will be affected the name '_lit'
        name = '_lit'+str(self.cpt)
        self.cpt += 1
        newl = Literal(name, True)
        notnl = Literal(name, False)
        # recursive visits
        nl1 = exp.left_h.accept(self)
        notnl1 = nl1.lit_not()
        nl2 = exp.right_h.accept(self)
        notnl2 = nl2.lit_not()
        # clause generation: x = lh and rh
        cl1 = Clause([nl1, notnl])           # not x or not lh
        cl2 = Clause([nl2, notnl])           # not x or not rh
        cl3 = Clause([notnl1, notnl2, newl]) # x or not lh or not rh

        self.clauses.append(cl1)
        self.clauses.append(cl2)
        self.clauses.append(cl3)
        if top:
            self.clauses.append(Clause([newl]))
            return None
        return newl


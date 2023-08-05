## Filename    : MCLSolutions.py
## Author(s)   : Michel Le Borgne
## Created     : 03/9/2012
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
Various solution representations
"""

# C++ API
from _cadbiom import get_unshift_code, unflatten

class MCLException(Exception):
    """
    Exception for MCLAnalyser
    """
    def __init__(self, mess):
        self.message = mess

    def __str__(self):
        return self.message

class RawSolution(object):
    """
    RawSolution objects contain a solution got from SAT solver with all
    variable parameters from the unfolder. This permit different extractions.
    IMPORTANT: the solution MUST correspond to the properties registered
    for its computation. Any change in these properties will give incorrect
    results.
    """
    def __init__(self, sol, cl_unfolder):
        """
        @param sol: DIMACS encoded solution
        @param cl_unfolder: the cl_unfolder (to be used for invariant constants)
        """
        self.__solution = sol
        self.__unfolder = cl_unfolder
        self.__nb_steps = cl_unfolder.get_current_step()
        self.__shift_step = cl_unfolder.get_shift_step() # dependant on the run
        self.__current_step = cl_unfolder.get_current_step()
        self.__shift_direction = cl_unfolder.get_shift_direction()

    def get_unshift_code(self, var_num):
        """
        @param var_num: DIMACS literal coding of a shifted variable x_i
        @return: DIMACS literal coding of  x_0 with same value
        """

        # Old API
        # var_code = (abs(var_num) - 1) % self.__shift_step + 1
        #
        # if var_code <= self.__shift_step:
        #     return var_code * (-1 if var_num < 0 else 1)
        # else:
        #     raise MCLException("Not a DIMACS code of an initial variable")

        # New API via C++ module
        get_unshift_code(var_num, self.__shift_step)

    def get_var_name(self, var_num):
        """
        For translation to symbolic representation
        """
        return self.__unfolder.get_var_name(var_num)

    def get_solution_size(self):
        """
        @return: int
        """
        return len(self.__solution)

    def get_solution(self):
        """
        DIMACS encoding of the solution from the solver
        """
        return self.__solution

    def get_nbsteps(self):
        """
        @return: int
        """
        return self.__nb_steps

    def get_unfolder(self):
        """
        @return: a clunfolder
        """
        return self.__unfolder

    def unflatten(self):
        """
        Transform a flat DIMACS representation of a trajectory into a list<list<int>>
        each sublist represents a state vector. Auxiliary variables introduced by properties
        compiling are ignored.
        @return: a list of state vectors (list<int>) in DIMACS format
        """

        # Old API
        # lv_traj = []
        # step = 0
        # dec = 0
        # len_shift_step_init = self.__unfolder.get_shift_step_init()
        # # n steps means h0, ..., h(n-1) in constraints for clocks and inputs
        # while dec + self.__shift_step <  len(self.__solution):
        #     #assert [self.get_unshift_code(self.__solution[i+dec]) for i in range(len_shift_step_init)] == [get_unshift_code(self.__solution[i+dec], self.__shift_step) for i in range(len_shift_step_init)]
        #     lv_traj.append(
        #         [get_unshift_code(self.__solution[i+dec], self.__shift_step)
        #          for i in range(len_shift_step_init)]
        #     )
        #     step += 1
        #     dec = step * self.__shift_step # first index of time step
        # return lv_traj # list of lists

        # New API via C++ module
        return unflatten(
            self.__solution,
            self.__unfolder.get_shift_step_init(),
            self.__shift_step
        )


    def extract_frontier_values(self):
        """
        Extract values of the init frontier variables from a whole solution vector
        Assert: sol is sorted by variable code

        @return: a dimacs code list of the activation state on the frontier for sol
        """

        # Old API
        # jmax = len(self.__unfolder.get_frontier())
        # fsol = []
        # j = 0
        # dec = self.__shift_step * self.__current_step
        # sol = self.__solution
        # for i in range(len(sol)):
        #     # the variable is frontier var:
        #     if abs(sol[i]) == self.__unfolder.get_frontier()[j]:
        #         if self.__shift_direction == "FORWARD":
        #             fsol.append(sol[i])
        #         else:
        #             fsol.append(sol[i+dec])     # look for initial values
        #         j += 1
        #         if j == jmax:
        #             return fsol
        # return fsol # never reach this point

        frontiers = self.__unfolder.get_frontier()
        jmax = len(frontiers)
        fsol = list()
        j = 0
        dec = self.__shift_step * self.__current_step
        for i, sol in enumerate(self.__solution):
            # the variable is frontier var:
            if abs(sol) == frontiers[j]:
                if self.__shift_direction == "FORWARD":
                    fsol.append(sol)
                else:
                    fsol.append(self.__solution[i+dec])# look for initial values
                j += 1
                if j == jmax:
                    return fsol
        return fsol # never reach this point

    def extract_act_frontier_values(self, sol):
        """
        frontier variables which are active at the beginning of  whole solution vector
        Assert: sol is sorted by variable code
        @param sol:  a dimacs solution
        @return: a dimacs code list of the activation state on the frontier for sol
        """
        frontiers = self.__unfolder.get_frontier()
        jmax = len(frontiers)
        fsol = list()
        j = 0
        dec = self.__shift_step * self.__current_step
        for i, sol in enumerate(self.__solution):
            # the variable is frontier var:
            if abs(sol) == frontiers[j]:
                if self.__shift_direction == "FORWARD":
                    if sol > 0:
                        fsol.append(sol)
                else:
                    if self.__solution[i+dec] > 0:
                        fsol.append(self.__solution[i+dec])# look for initial values
                j += 1
                if j == jmax:
                    return fsol
        return fsol # never reach this point


    def extract_act_inputs_clocks(self, s_vector):
        """
        extract active __inputs and clocks from a state vector
        """

        inputs      = frozenset(self.__unfolder.get_inputs())
        free_clocks = frozenset(self.__unfolder.get_free_clocks())

        return [s_varcode for s_varcode in s_vector
                if (s_varcode > 0)
                and ((s_varcode in inputs)
                    or (s_varcode in free_clocks))]


    def extract_act_input_clock_seq(self):
        """
        Extract the sequence of activated __inputs and clocks in the solution sol
        @return: list<list<int>> list of input vector
        """

        return [] \
            if (len(self.__unfolder.get_inputs()) == 0) and (len(self.__unfolder.get_free_clocks()) == 0) \
            else [self.extract_act_inputs_clocks(xic)
                  for xic in self.unflatten()] # list of lists

    def __str__(self):
        """
        For debug purpose
        """
        unfl = self.unflatten()
        stn = []
        for vect in unfl:
            vect_n = []
            for dcod in vect:
                if dcod > 0:
                    vect_n.append(self.get_var_name(dcod))
                else:
                    vect_n.append("-"+self.get_var_name(dcod))
            stn.append(vect_n)
        return stn.__str__()

    def display_activ_sol(self):
        """
        for debug
        """
        unfl = self.unflatten()
        stn = []
        for vect in unfl:
            vect_n = []
            for dcod in vect:
                if dcod > 0:
                    v_name = self.get_var_name(dcod)
                    if not v_name[0] == "_":
                        vect_n.append(v_name)
            vect_n.sort()
            stn.append(vect_n)
        print stn



class FrontierSolution(object):
    """
    class for symbolic frontier and timing representation (built from a raw solution)
    """

    def __init__(self, act_frontier, ic_seq, horizon):
        """
        Build a symbolic representation of frontier values and timing from
        a raw solution
        """
        # attributes
        self.activated_frontier = act_frontier   # list<string>
        self.ic_sequence = ic_seq                # list<string> (format % h1 h2)
        self.horizon = horizon                   # int



    @classmethod
    def from_raw(cls, raws):
        """
        Build a symbolic representation of frontier values and timing from
        a raw solution
        @param raws: a raw solution
        """
        # activated frontier places
        dim_front = raws.extract_frontier_values()
        out = []
        for dcod in dim_front:
            if dcod > 0:
                out.append(raws.get_var_name(dcod))
        activated_frontier = out

        # activated input/clocks
        ic_seq = raws.extract_act_input_clock_seq()
        lic = []
        for icv in ic_seq:
            ic_act = "%"
            for iii in icv:
                ic_act = ic_act + " " + raws.get_var_name(iii)
            lic.append(ic_act)
        ic_sequence = lic
        horizon = raws.get_nbsteps()
        return cls(activated_frontier, ic_sequence, horizon)

    @classmethod
    def from_dimacs_front_sol(cls, fds):
        """
        Build a symbolic representation of frontier values and timing from
        a DimacsFrontierSolution solution
        @param fds: a raw solution
        """
        # activated frontier places
        dim_front = fds.frontier_values
        out = []
        for dcod in dim_front:
            if dcod > 0:
                out.append(fds.get_var_name(dcod))
        activated_frontier = out

        # activated input/clocks
        ic_seq = fds.ic_sequence
        lic = []
        for icv in ic_seq:
            ic_act = "%"
            for iii in icv:
                ic_act = ic_act + " " + fds.get_var_name(iii)
            lic.append(ic_act)
        ic_sequence = lic
        horizon = fds.get_nbsteps()
        return cls(activated_frontier, ic_sequence, horizon)

    @classmethod
    def from_file(cls, file_name):
        """
        Build a symbolic representation of frontier values and timing from
        a DimacsFrontierSolution solution
        """
        try:
            fr_f = open(file_name)
        except:
            raise MCLException("Impossible to open file: "+file_name)
        act_front = fr_f.readline().split()
        ic_seq = []
        step = fr_f.readline()
        horizon = 0
        while step:
            horizon += 1
            ic_seq.append(step[:-1])
            step = fr_f.readline()
        return cls(act_front, ic_seq, horizon)

    def __str__(self):
        """
        give a string representation of a Frontier solution
        """
        stro = "\nActivated front.:"
        stro = stro + self.activated_frontier.__str__()
        stro = stro + "\nTiming:"
        for icc in self.ic_sequence:
            stro =  stro + "\n   " + icc
        return stro

    def has_same_frontier(self, other):
        """
        Check if two FrontierSol have same frontier
        @param other: a DimacsFrontierSol
        @return bool
        """
        return set(self.frontier_values) == set(other.frontier_values)

    def save(self, outfile):
        """
        Save a symbolic solution in a file
        The format is readable by the simulator
        @param outfile: writable file
        """
        outfile.write(' '.join(sorted(self.activated_frontier, key=lambda s: s.lower())) + '\n')
        outfile.write('\n'.join(self.ic_sequence) + '\n')
        outfile.flush()


class DimacsFrontierSol(object):
    """
    class for solution frontier and timing representation
    (built from a raw solution) in Dimacs code
    """
    def __init__(self, raws):
        """
        Build a numeric representation of frontier values and timing from
        a raw solution
        @param raws: a raw solution
        """
        # attributes
        # self.frontier_values : list<int>
        # self.ic_sequence     : list<list<int>>
        # self.horizon         : int

        # frontier places
        self.frontier_values = raws.extract_frontier_values()

        # activated input/clocks (may be empty if data-flow model without input)
        self.ic_sequence = raws.extract_act_input_clock_seq()
        self.horizon = raws.get_nbsteps()

        # CLUnfolder
        self.__unfolder = raws.get_unfolder()

    def get_var_name(self, var_num):
        """
        For translation to symbolic representation
        """
        return self.__unfolder.get_var_name(var_num)

    def get_solution_size(self):
        """
        @return: int
        """
        return len(self.frontier_values)

    def get_solution(self):
        """
        @return: list<int>
        """
        return self.frontier_values

    def get_nbsteps(self):
        """
        @return: int
        """
        return self.horizon

    def has_same_frontier(self, other):
        """
        Check if two DimacsFrontierSol have same frontier
        @param other: a DimacsFrontierSol
        @return bool
        """
        return set(self.frontier_values) == set(other.frontier_values)

    def front_is_in(self, ldfs):
        """
        Check if an object of ldfs has the same frontier list
        @param ldfs: list of  DimacsFrontierSol
        @return bool
        """
        for dfs in ldfs:
            #if self.has_same_frontier(dfs):
            if set(self.frontier_values) == set(dfs.frontier_values):
                return True
        return False

    def nb_activated(self):
        """
        Count the number of activated places in solution
        @return: int
        """
        cpt = 0
        for vcod in self.frontier_values:
            if vcod > 0:
                cpt += 1
        return cpt

    def nb_timed(self):
        """
        Count the number of events in solution
        @return: int
        """
        cpt = 0
        for ic_act in self.ic_sequence:
            cpt += len(ic_act)
        return cpt

    def display(self):
        """
        For tests and debug
        """
        print 'Frontier solution:'
        print self.frontier_values

# useful functions for solution lists
def extract_dimacs_init_frontier(lsol):
    """
    Extract init values of the frontier variables from a whole solution vector for
    a list of solution vectors.
    Eliminate double frontier level
    @param lsol: list of raw solutions
    @return: a list of DimacsFrontierSol
    """
    ext1 = []
    for sol in lsol:
        esol = DimacsFrontierSol(sol)
        if not esol.front_is_in(ext1):
            ext1.append(esol)
    return ext1


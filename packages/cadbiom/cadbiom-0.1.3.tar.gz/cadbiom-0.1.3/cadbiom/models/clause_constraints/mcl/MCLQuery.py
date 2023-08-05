## Filename    : MCLQuery.py
## Author(s)   : Michel Le Borgne
## Created     : 10 sept. 2012
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
Query internal representation
"""

from cadbiom.models.clause_constraints.mcl.MCLSolutions import MCLException
from cadbiom import commons as cm
from logging import DEBUG

LOGGER = cm.logger()

class MCLSimpleQuery(object):
    """
    Class packaging the elements of a query:
        - start property (string)
        - invariant property (string)
        - final property (sting)
        - dim_start: a start property in DIMACS form - optional - default None
        - dim_invariant: idem for invariant property
        - dim_final: idem for final property
        - steps_before _reach: number of shift before testing the final property
                               optional - default value 1000 000
    NB: DClause: a clause coded as a list of DIMACS coded literals
    """

    def __init__(self, start_prop, inv_prop, final_prop):
        """
        @param start_prop: init property - None is allowed
        @param inv_prop: invariant property - None allowed
        @param final_prop: final property - None is allowed
        """
        if LOGGER.getEffectiveLevel() == DEBUG:
            LOGGER.debug("MCLSimpleQuery params:: " + \
                         str(start_prop) + '; ' + \
                         str(inv_prop) + '; ' + \
                         str(final_prop))
        self.start_prop = start_prop  # logical formula or None
        self.inv_prop = inv_prop      # logical formula or None
        self.variant_prop = []        # list<logical formula>
        self.final_prop = final_prop  # logical formula or None
        # dimacs form of preceding
        self.dim_start = []         # list<DClause>
        self.dim_inv = []           # list<DClause>
        self.dim_final = []         # list<DClause>
        self.dim_variant_prop = []  # list<list<DClause>>

        self.steps_before_reach = 0

    @classmethod
    def from_frontier_sol(cls, f_sol):
        """
        build a query from a frontier solution
        start condition activate the activated frontier places
        variant property enforce same timing
        """
        # start condition enforce activation of solution places
        st_prop = None
        if f_sol.activated_frontier:
            st_prop = f_sol.activated_frontier[0]
            for fcond in f_sol.activated_frontier[1:]:
                st_prop = st_prop + " and " + fcond
        # no invariant property
        inv_prop = None
        # variant property enforce same timing
        var_prop = None
        if f_sol.ic_sequence:
            var_prop = []
            for ic_act in f_sol.ic_sequence:
                l_ic = ic_act[1:].split()
                if len(l_ic)>0:
                    ic_prop = l_ic[0]
                    for icp in l_ic[1:]:
                        ic_prop = ic_prop + " and " + icp
                else:
                    ic_prop = ""
                var_prop.append(ic_prop)
        fin_prop = None
        n_query = MCLSimpleQuery(st_prop, inv_prop, fin_prop)
        n_query.set_variant_property(var_prop)
        return n_query


    @classmethod
    def from_frontier_sol_new_timing(cls, f_sol, unfolder):
        """
        @param f_sol: the FrontierSolution
        @param unfolder: unfolder in use
        build a query from a frontier solution
        start condition activate the activated frontier places
        and force others to be inactivate.
        variant property enforce new timing
        """
        # activation part of start condition
        st_prop = None
        if f_sol.activated_frontier:
            st_prop = f_sol.activated_frontier[0]
            for fcond in f_sol.activated_frontier[1:]:
                st_prop = st_prop + " and " + fcond
        # no invariant property
        inv_prop = None
        # variant property enforce new timing
        var_prop = None
        if f_sol.ic_sequence:
            var_prop = []
            for ic_act in f_sol.ic_sequence:
                l_ic = ic_act[1:].split()
                if len(l_ic)>0:
                    ic_prop = "not (" + l_ic[0]+ ")" # step constraint
                    for icp in l_ic[1:]:
                        n_icp = "not (" + icp + ")"
                        ic_prop = ic_prop + " or " + n_icp
                else:
                    ic_prop = ""
                var_prop.append(ic_prop)
        fin_prop = None
        # inactivation of other frontier places at start (dimacs form)
        frontier = unfolder.get_frontier()
        l_dstart = []
        for i_fr in frontier:
            name = unfolder.get_var_name(i_fr)
            if not name in f_sol.activated_frontier:
                l_dstart.append([- i_fr])

        n_query = MCLSimpleQuery(st_prop, inv_prop, fin_prop)
        n_query.set_variant_property(var_prop)
        n_query.set_dim_start(l_dstart)
        return n_query

    @classmethod
    def from_frontier_sol_same_timing(cls, f_sol, unfolder):
        """
        @param f_sol: the FrontierSolution
        @param unfolder: unfolder in use
        build a query from a frontier solution
        start condition activate the activated frontier places
        and force others to be inactivate.
        variant property enforce same timing on activated events,
        and others are free
        """
        # activation part of start condition
        st_prop = None
        if f_sol.activated_frontier:
            st_prop = f_sol.activated_frontier[0]
            for fcond in f_sol.activated_frontier[1:]:
                st_prop = st_prop + " and " + fcond
        # no invariant property
        inv_prop = None
        # make event dictionary
        event_dict = dict()
        step_cpt = 0
        for ic_act in f_sol.ic_sequence:
            l_ic = ic_act[1:].split()
            for icp in l_ic:
                if not event_dict.has_key(icp):
                    event_dict[icp]=[step_cpt]
                else :
                    event_dict[icp].append(step_cpt)
            step_cpt += 1
        # variant property enforce same timing on activated events
        var_prop = None
        if f_sol.ic_sequence:
            var_prop = []
            step_cpt = 0
            for ic_act in f_sol.ic_sequence:
                l_ic = ic_act[1:].split()
                if len(l_ic)>0:
                    if event_dict.has_key(l_ic[0]):
                        if step_cpt in event_dict[l_ic[0]]:
                            ic_prop = l_ic[0]
                        else :
                            ic_prop = "not (" + l_ic[0]+ ")"
                    for icp in l_ic[1:]:
                        if event_dict.has_key(icp):
                            if step_cpt in event_dict[icp]:
                                n_icp = icp
                            else :
                                n_icp = "not (" + icp + ")"
                        ic_prop = ic_prop + " and " + n_icp
                else:
                    ic_prop = ""
                var_prop.append(ic_prop)
                step_cpt += 1
        fin_prop = None
        # inactivation of other frontier places at start (dimacs form)
        frontier = unfolder.get_frontier()
        l_dstart = []
        for i_fr in frontier:
            name = unfolder.get_var_name(i_fr)
            if not name in f_sol.activated_frontier:
                l_dstart.append([- i_fr])

        n_query = MCLSimpleQuery(st_prop, inv_prop, fin_prop)
        n_query.set_variant_property(var_prop)
        n_query.set_dim_start(l_dstart)
        return n_query

    def set_variant_property(self, var_prop):
        """
        @param var_prop: list<string> - list of logical formulas
        """
        self.variant_prop = var_prop

    def set_dim_variant_prop(self, d_var_prop):
        """
        @param d_var_prop: list<list<list<int>>> - list-list of dimacs clauses
        """
        self.dim_variant_prop = d_var_prop

    def set_dim_start(self, dim_start):
        """
        @param dim_start: start property in DIMACS format
        """
        self.dim_start = dim_start

    def set_dim_inv(self, dim_inv):
        """
        Similar to set_dim_start
        """
        self.dim_inv = dim_inv

    def set_dim_final(self, dim_final):
        """
        Similar to set_dim_final
        """
        self.dim_final = dim_final

    def set_steps_before_reach(self, nb_steps):
        """
        @param nb_steps: int - number of shifts before testing final prop
        """
        self.steps_before_reach = nb_steps

    def merge(self, quer):
        """
        Merge two queries into one. start, inv and final properties are
        the and of the corresponding properties in each query.
        If both queries have variant properties, they must be on the same horizon.
        steps before reach is set to zero.

        @param quer: a MCLSimpleQuery
        @raise MCLException: if the queries have variant properties on
        different horizons.
        """
        # merge of start properties
        if not self.start_prop:
            st_prop = quer.start_prop
        elif not quer.start_prop:
            st_prop = self.start_prop
        else:
            st_prop = "(" + self.start_prop + ") and (" + quer.start_prop + ")"
        # merge of invariant properties
        if not self.inv_prop:
            i_prop = quer.inv_prop
        elif not quer.inv_prop:
            i_prop = self.inv_prop
        else:
            i_prop = "(" + self.inv_prop + ") and (" + quer.inv_prop + ")"
        # merge of final properties
        if not self.final_prop:
            f_prop = quer.final_prop
        elif not quer.final_prop:
            f_prop = self.final_prop
        else:
            f_prop = "(" + self.final_prop + ") and (" + quer.final_prop + ")"

        n_query = MCLSimpleQuery(st_prop, i_prop, f_prop)
        # merge of variant prop
        v_prop = None
        if not self.variant_prop:
            v_prop = quer.variant_prop
        elif not quer.variant_prop:
            v_prop = self.variant_prop
        else:
            ll1 = len(self.variant_prop)
            ll2 = len(quer.variant_prop)
            if ll1 != ll2:
                mess = "Tempting to merge two queries with variant prop "
                mess = mess + "of different length"
                raise MCLException(mess)
            else:
                v_prop = []
                for i in range(ll1):
                    loc = self.variant_prop[i] + " and "+ quer.variant_prop[i]
                    v_prop.append(loc)
        n_query.set_variant_property(v_prop)
        # merge of dim properties
        dim_start = self.dim_start + quer.dim_start
        n_query.set_dim_start(dim_start)
        dim_inv = self.dim_inv + quer.dim_inv
        n_query.set_dim_inv(dim_inv)
        dim_final = self.dim_final + quer.dim_final
        n_query.set_dim_final(dim_final)

        return n_query

    def __str__(self):
        """
        Print logical formulas in query
        """
        str_out = "Start_property: "
        if self.start_prop:
            str_out = str_out + self.start_prop
        str_out = str_out + "\nInv property: "
        if self.inv_prop:
            str_out = str_out + self.inv_prop
        str_out = str_out + "\nFinal property: "
        if self.final_prop:
            str_out = str_out + self.final_prop
        str_out = str_out + "\nVariant property: "
        if self.variant_prop:
#            str_out = str_out + self.variant_prop[0]
#            for prop in self.variant_prop[1:]:
#                str_out = str_out + ", " + prop
            str_out = str_out + self.variant_prop.__str__()
        return str_out

## Filename    : static_analysis.py
## Author(s)   : Michel Le Borgne
## Created     : 02/2012
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
##     IRISA/IRISA
##     Symbiose team
##     IRISA  Campus de Beaulieu
##     35042 RENNES Cedex, FRANCE
##
##
## Contributor(s): Geoffroy Andrieux
##
"""
Classes for static analysis
"""
import string
import networkx as nx
import copy
from collections import OrderedDict

from cadbiom.antlr3 import ANTLRFileStream, CommonTokenStream


from cadbiom.models.biosignal.translators.gt_visitors import compile_cond, compile_event
from cadbiom.models.guard_transitions.translators.cadlangLexer import cadlangLexer
from cadbiom.models.guard_transitions.translators.cadlangParser import cadlangParser
from cadbiom.models.guard_transitions.translators.chart_xml import MakeModelFromXmlFile
from cadbiom.models.guard_transitions.translators.chart_xml_pid import \
                                          MakeModelFromPidFile
from cadbiom.models.guard_transitions.chart_model import ChartModel
from cadbiom.models.guard_transitions.analyser.ana_visitors import EstimExpVisitor, \
                       TableVisitor,  FrontierVisitor, SigExpIdCollectVisitor
import cadbiom.commons as cm

LOGGER = cm.logger()

class StaticAnalyzer(object):
    """
    Main class for static analysis
    """

    def __init__(self, reporter):
        self.reporter = reporter
        self.model = None
        self.influence_dict = dict()

    def build_from_chart_model(self, chart_model):
        """
        For technical purpose
        """
        self.model = chart_model

    def build_from_cadlang(self, file_name):
        """
        Build a StaticAnalyser from a .cal file of PID database
        @param file_name: str - path of .cal file
        """

        crep = self.reporter
        fstream = ANTLRFileStream(file_name)
        lexer = cadlangLexer(fstream)
        lexer.set_error_reporter(crep)
        parser = cadlangParser(CommonTokenStream(lexer))
        parser.set_error_reporter(crep)
        model = ChartModel(file_name)
        parser.cad_model(model)
        # chart model
        self.model = parser.model

    def build_from_chart_file(self, file_name):
        """
        Build a StaticAnalyser from a .bcx file
        @param file_name: str - path of the .bcx file
        """
        parsing = MakeModelFromXmlFile(file_name)
        # chart model
        self.model = parsing.get_model()

    def build_from_pid_file(self, file_name, has_clock=True,
                            ai_interpretation=0):
        """
        Build an StaticAnalyser from a .xml file of PID database
        @param file_name: str - path of .xml file
        """
        parser = MakeModelFromPidFile(file_name, self.reporter,
                                       has_clock, ai_interpretation)
        # chart model
        self.model = parser.get_model()

    def get_frontier_node_names(self):
        """
        returns a (list<string>) list of frontier place names
        """
        fvi = FrontierVisitor()
        self.model.accept(fvi)
        return fvi.frontier

    def get_gene_places(self):
        """
        We assume that all places representing a gene contain the 'gene' string in the name
        """
        lpname = []
        node_dict = self.model.node_dict
        for pname in node_dict.keys():
            if string.find(pname, 'gene') > 0:
                lpname.append(pname)
        return lpname


    def get_statistics(self, sfile=False):
        """
        Compute various informations on the model (assume PID encoding)

        .. warning:: Start nodes (__start__0) are counted here in 'other'
            locations.

        :param arg1: Opened file (optional).
        :type arg1: <open file>
        :return: Informations (status of nodes and their cellular locations).
        :rtype: <str>
        """

        input_cpt = 0
        front_cpt = 0
        final_cpt = 0
        isolated_cpt = 0
        locations = (
            '_gene', '_transMb', '_nucl', '_intToMb', '_cy', '_plasmaMb',
            '_exCellRegion', '_ccJct', '_en', '_siteofdouble_strandbreak',
            '_membraneraft', 'other',
        )
        # Init counter of locations
        location_dict = OrderedDict({location: 0 for location in locations})

        # Iterate on model nodes
        for node_name, node in self.model.node_dict.iteritems():
            loc_found = False
            for location in locations:
                if location in node_name:
                    if loc_found:
                        LOGGER.warning(
                            "get_statistics::Multiple locations: {}, {}".format(
                                node_name, location))
                    location_dict[location] += 1
                    loc_found = True


            # Warning: this line also counts "virtual" "start nodes"
            # like __start__0
            if not loc_found:
                location_dict['other'] += 1

            # Check node status
            nb_outgoing_trans = len(node.outgoing_trans)
            nb_incoming_trans = len(node.incoming_trans)

            if node.is_input():
                input_cpt += 1
            if nb_outgoing_trans == 0:
                final_cpt += 1
            if nb_incoming_trans == 0:
                front_cpt += 1
            if nb_outgoing_trans == 0 and nb_incoming_trans == 0:
                isolated_cpt += 1

        # Forge data header
        data = OrderedDict({
            "Model name": self.model.name,
            "Nb places": len(self.model.node_dict),
            "Nb transitions": len(self.model.transition_list),
            "Nb inputs": input_cpt,
            "Nb frontier (no incoming transitions)": front_cpt,
            "Nb terminal (no outgoing transitions)": final_cpt,
            "Nb isolated (frontier places in conditions/not used)":isolated_cpt,
        })
        # Forge data locations
        for k, v in location_dict.iteritems():
            data['Nb ' + k] = v

        # Forge text
        text = "\n".join([k + ': ' + str(v) for k, v in data.iteritems()])

        # Dump text if an opened file is given
        if sfile != False:
            sfile.write(text)

        return text


    def get_frontier_scc(self):
        """
        Find initial strongly connected components in the transition graph
        @return:   list<list<string>> - list of list of node names in frontier
        strongly connected components

        .. warning:: If the model is modified but not reloaded, KeyError is
            raised (see below); we inform the user of that...
        """
        # Get directed graph
        directed_graph = self.make_transition_dg()
        # generator on the strongly connectec components
        scc_list = nx.strongly_connected_components(directed_graph)

        frontier_list = []
        tvi = TableVisitor(self.reporter)
        self.model.accept(tvi)

        for scc in scc_list:
            # eliminate isolated frontier nodes
            if len(scc) > 1:
                frontier = True
                # generate symbol table for partial evaluation
                # all places in scc are inactivated (-1)
                symbol_table = dict.fromkeys(scc, -1)
                pe_visitor = EstimExpVisitor(symbol_table)

                # find all incoming transitions for each node in scc
                LOGGER.debug("scc: " + str(scc))
                for node_name in scc:

                    try:
                        # raises keyerror if the model isn't reloaded manually..
                        chart_node = self.model.node_dict[node_name]
                    except KeyError:
                        return list([[
                            "Error: Please try by \
                            saving & reloading the model manually"]])

                    for in_trans in chart_node.incoming_trans:
                        LOGGER.debug(
                            "Node {}, trans: {}".format(
                                node_name,
                                (in_trans.ori.name, in_trans.ext.name)
                            )
                        )

                        # if the transition comes from outside scc,
                        # we try to detect if scc may be reached with this trans
                        if in_trans.ori.name not in scc :
                            cond = self.__tr_estim(in_trans, pe_visitor,
                                                   tvi.tab_symb)

                            LOGGER.debug(
                                "scc validated as a cyle ?: " + str(cond)
                            )
                            # Guard of the transition is True
                            # (not False or indeterminate),
                            # so scc may be reached from other part of the model
                            # => switch to next scc
                            if cond >= 0:
                                frontier = False
                                break
                if frontier:
                    LOGGER.debug("frontier found")
                    frontier_list.append(scc)

        LOGGER.debug("SCC found: " + str(frontier_list))

        # Nothing found => return empty result
        if len(frontier_list) == 0:
            return [[]]
        return frontier_list

    def get_basal_activated_genes(self):
        """
        Basal activated genes are genes which are activated even if all the places present
        in activation condition, are inactivate
        """
        node_dict = self.model.node_dict
        tvi = TableVisitor(self.reporter)
        self.model.accept(tvi)
        lg_n = self.get_gene_places()
        lgene = []
        for gen in lg_n:
            lgene.append(node_dict[gen])
        lbag = []

        for gep in lgene:
            pe_visitor = EstimExpVisitor(None) # all variables set to False
            assert(len(gep.outgoing_trans)==1)
            trans = gep.outgoing_trans[0] # assume only one transition
            trans_val = self.__tr_estim(trans, pe_visitor, tvi.tab_symb)
            if trans_val == 1:
                lbag.append(gep.name)
        lbag.sort()
        return lbag

    def get_why_basal_genes(self):
        """
        More complete than get_basal_activated_genes. Returns a list of pairs (g,lpv) where
        g is a basal activated gene and lpv are the principal variables (isolated_inhib., dominant_inhib,
        essential_act, dominant activator)
        """
        res = []
        node_dict = self.model.node_dict
        lbag = self.get_basal_activated_genes()
        for gep in lbag:
            gnode = node_dict[gep]
            trans = gnode.outgoing_trans[0]
            pva = self.get_tr_principal_variables(trans)
            res.append((gep, pva))

        # Nothing found => return empty result
        if len(res) == 0:
            return [[]]
        return res

    def __tr_estim(self, trans, e_visitor, tab_symb):
        """
        Given a partial assignation of variables implemented in tab_symb, estimate if
        the guard of a transition is True, False or indeterminate. The variables not present
        in the symbol table are considered as indeterminates

        If tab_symb is None, all variables are assigned the value False and the condition of the
        guard is estimated alone.
        """
        ev_estim = 1
        cond_estim = 1

        if trans.condition:
            cond_sexpr = compile_cond(trans.condition, tab_symb, self.reporter)
            cond_estim = cond_sexpr.accept(e_visitor)

        if not e_visitor.symb_table:
            return cond_estim

        if trans.event:
            ev_sexpr = compile_event(trans.event, tab_symb,
                                        True, self.reporter)[0]
            ev_estim = ev_sexpr.accept(e_visitor)

        return min(ev_estim, cond_estim)

    def __get_tr_node_variables(self, cond_sexpr, ev_sexpr):
        """
        Get the node idents in the guard expression of
        the transition condition and event
        """
        lst1 = []
        lst2 = []
        lcl = []
        icv = SigExpIdCollectVisitor()
        if cond_sexpr:
            # condition expressions contains only node ident
            lst1 = cond_sexpr.accept(icv)
        if ev_sexpr:
            ll2 = ev_sexpr.accept(icv)
            for ident in ll2:
                if self.model.node_dict.has_key(ident): # state
                    lst2.append(ident)
                else: # clock
                    lcl.append(ident)
        lst = lst1 + lst2
        lst.sort()
        # eliminate doubles
        if len(lst)>0:
            nres = [lst[0]]
            for i in range(len(lst)-1):
                if lst[i+1] != lst[i]:
                    nres.append(lst[i+1])
        else:
            nres = []

        if len(lcl)>0:
            cres = [lcl[0]]
            for i in range(len(lcl)-1):
                if lcl[i+1] != lcl[i]:
                    cres.append(lcl[i+1])
        else:
            cres = []

        return nres , cres

    # for test
    def test_get_tr_node_variables(self, trans):
        """
        externalize a private method for test only
        """
        tvi = TableVisitor(self.reporter)
        self.model.accept(tvi)

        if trans.condition:
            cond_sexpr = compile_cond(trans.condition, tvi.tab_symb,
                                      self.reporter)
        else:
            cond_sexpr = None
        if trans.event:
            ev_sexpr, see, free_clocks = compile_event(trans.event,
                                                       tvi.tab_symb,
                                                       True, self.reporter)
        else:
            ev_sexpr = None

        lvar = self.__get_tr_node_variables(cond_sexpr, ev_sexpr)
        return lvar


    def get_tr_principal_variables(self, trans):
        """
        Compute the essentiel, inhibitors, dominant inhibitors,
        essential activators and dominant activators of a transition tr.
        """
        ein = [] # essential inhibitors
        din = [] # dominant inhibitors
        eac = [] # essentiel activators
        dac = [] # dominant activators
        tvi = TableVisitor(self.reporter)
        self.model.accept(tvi)
        # compile guard expression
        if trans.condition:
            cond_sexpr = compile_cond(trans.condition, tvi.tab_symb,
                                      self.reporter)
        else:
            cond_sexpr = None
        if trans.event:
            ev_sexpr, see, free_clocks = compile_event(trans.event,
                                                      tvi.tab_symb,
                                                      True, self.reporter)
        else:
            ev_sexpr = None

        lvar , lcl = self.__get_tr_node_variables(cond_sexpr, ev_sexpr)

        for ident in lvar:
            # essential inhibitor (F => (guard=T))
            assign_table = dict()
            assign_table[ident] = -1
            for clo in lcl:
                assign_table[clo] = 1 # clocks are assigned to Present
            pe_visitor = EstimExpVisitor(assign_table)

            if cond_sexpr:
                cpe = cond_sexpr.accept(pe_visitor)
            else:
                cpe = 1
            if ev_sexpr:
                epe = ev_sexpr.accept(pe_visitor)
            else:
                epe = 1
            if min(cpe, epe) == 1:
                ein.append(ident)
            # dominant inhibitor (T => (guard=F))
            assign_table = dict()
            assign_table[ident] = 1
            for clo in lcl:
                assign_table[clo] = 1 # clocks are assigned to Present
            pe_visitor = EstimExpVisitor(assign_table)

            if cond_sexpr:
                cpe = cond_sexpr.accept(pe_visitor)
            else:
                cpe = 1
            if ev_sexpr:
                epe = ev_sexpr.accept(pe_visitor)
            else:
                epe = 1
            if min(cpe, epe) == -1:
                din.append(ident)
            # essential activator (F => (guard=F))
            assign_table = dict()
            assign_table[ident] = -1
            for clo in lcl:
                assign_table[clo] = 1 # clocks are assigned to Present
            pe_visitor = EstimExpVisitor(assign_table)

            if cond_sexpr:
                cpe = cond_sexpr.accept(pe_visitor)
            else:
                cpe = 1
            if ev_sexpr:
                epe = ev_sexpr.accept(pe_visitor)
            else:
                epe = 1
            if min(cpe, epe) == -1:
                eac.append(ident)
            # dominant activator (T => (guard=T))
            assign_table = dict()
            assign_table[ident] = 1
            for clo in lcl:
                assign_table[clo] = 1 # clocks are assigned to Present
            pe_visitor = EstimExpVisitor(assign_table)

            if cond_sexpr:
                cpe = cond_sexpr.accept(pe_visitor)
            else:
                cpe = 1
            if ev_sexpr:
                epe = ev_sexpr.accept(pe_visitor)
            else:
                epe = 1
            if min(cpe, epe) == 1:
                dac.append(ident)
        return [ein, din, eac, dac]


    def make_transition_dg(self):
        """
        Build the directed graph of transitions (flow graph)
        @return: a Networkx digraph
        """
        graph = nx.DiGraph()

        edges = [(trans.ori.name, trans.ext.name)
            for trans in self.model.transition_list]

        graph.add_edges_from(edges)
        graph.add_nodes_from(self.model.node_dict.keys())

        return graph

    def make_dependence_dg(self, weight = False):
        """
        Build the directed graph of transitions and conditions (dependence graph)
        if weight : dependencies from transitions have a weight of 2, dependencies from conditions have a weight of 1
        else : all dependencies have a weight of 1
        @return: a Networkx digraph
        """
        graph = nx.DiGraph()
        for trans in self.model.transition_list :
            ori_name = trans.ori.name
            ext_name = trans.ext.name

            lno , lcl = self.test_get_tr_node_variables(trans)
            for cond in lno :
                graph.add_edges_from([(cond, ext_name)], weight=1)
            if weight :
                graph.add_edges_from([(ori_name, ext_name)], weight=2)
            else :
                graph.add_edges_from([(ori_name, ext_name)], weight=1)
        return graph


    def make_full_dependence_dg(self, weight = False):
        """
        Build the directed graph of transitions and conditions (dependence graph)
        Conditions also influence input
        @return: a Networkx digraph
        """
        graph = nx.DiGraph()
        for trans in self.model.transition_list :
            ori_name = trans.ori.name
            ext_name = trans.ext.name

            lno , lcl = self.test_get_tr_node_variables(trans)
            for cond in lno :
                graph.add_edges_from([(cond, ext_name)], weight=1)
                # conditions influence input
                graph.add_edges_from([(cond, ori_name)], weight=1)

            if weight :
                graph.add_edges_from([(ori_name, ext_name)], weight=2)
            else :
                graph.add_edges_from([(ori_name, ext_name)], weight=1)
        return graph

#    def make_full_dependence_weighted_dg(self):
#        """
#        Build the directed graph of transitions and conditions
#        (dependence graph)
#        Dependences from transitions have a weight of 2
#        Dependences from conditions have a weight of 1
#        Conditions also influence input
#        @return: a Networkx digraph
#        """
#        G=nx.DiGraph()
#        for trans in self.model.transition_list :
#            ori_name = trans.ori.name
#            ext_name = trans.ext.name
#
#            ln , lh = self.test_get_tr_node_variables(trans)
#            for cond in ln :
#                G.add_edges_from([(cond,ext_name)], weight=1)
#                # conditions influence input
#                G.add_edges_from([(cond,ori_name)], weight=1)
#
#            G.add_edges_from([(ori_name,ext_name)], weight=2)
#        return G

#    def condition_count(self):
#        cond_dict=dict()
#        for trans in self.model.transition_list :
#            if trans.condition != '':
#                cond_name_list = get_property_places(trans.condition)
#                for cond in cond_name_list :
#                    if cond_dict.has_key(cond) :
#                        cond_dict[cond]+=1
#                    else :
#                        cond_dict[cond]=1
#        cond_items = cond_dict.items()
#        cond_items.sort(cmpval)
#
#        cond_moy=0.0
#        for cond_couple in cond_items :
#            cond_moy+=cond_couple[1]
#        print 'cond moy : ',cond_moy/len(cond_dict.keys())
#        print 'cond median : ',cond_items[len(cond_dict.keys())/2][1]
#        print 'cond count : ',cond_items[:10]
#        return cond_items

    def get_predecessors(self, dgraph, node, rank=None):
        """
        return all node predecessors if rank=None, predecessors under the rank else
        @return: a list of str predecessor name
        """
        if not rank :
            pred_list = dgraph.predecessors(node)
            pred_list.append(node)
            for pred in pred_list:
                sec_pred_list = dgraph.predecessors(pred)
                for sec_p in sec_pred_list:
                    if sec_p not in pred_list:
                        pred_list.append(sec_p)
#            print len(pred_list), pred_list
        else :
            self.ranked_list = []
            pred_list = [node]
            already_visited = []
            for i in range(rank):
                new_pred_list = []
                for node in pred_list:
                    if node not in already_visited:
                        new_pred_list.extend(dgraph.predecessors(node))
                        already_visited.append(node)
                self.ranked_list.append(new_pred_list)
                pred_list.extend(new_pred_list)
#                print i, len(list(set(new_pred_list)))
#                print i,len(new_pred_list),new_pred_list
        return list(set(pred_list))

    def get_successors(self, dgraph, node, rank=None):
        """
        return all node successors if rank=None, successors under the rank else
        @return: a list of str successor name
        """
        if not rank :
            suc_list = dgraph.successors(node)
            suc_list.append(node)
            for suc in suc_list:
                sec_suc_list = dgraph.successors(suc)
                for sec_s in sec_suc_list:
                    if sec_s not in suc_list:
                        suc_list.append(sec_s)
    #        print len(pred_list), pred_list
        else :
            self.ranked_list = []
            suc_list = [node]
            already_visited = []
            for i in range(rank):
                new_suc_list = []
                for node in suc_list:
                    if node not in already_visited:
                        new_suc_list.extend(dgraph.successors(node))
                        already_visited.append(node)
                self.ranked_list.append(new_suc_list)
                suc_list.extend(new_suc_list)
#                print i,len(new_pred_list),new_pred_list
        return list(set(suc_list))


    def get_local_neighbors(self, dgraph, node):
        """
        return node direct neighbors (successors and predecessors) in a same list
        @return: a list of str neighbor name
        """
        neighbor_list = []
        neighbor_list.extend(dgraph.predecessors(node))
        neighbor_list.extend(dgraph.successors(node))
        return list(set(neighbor_list))

#    def get_list_neighbors(self, dgraph, node_list):
#        neighbor_list = []
#        for node in node_list :
#            neighbor_list.extend(self.get_node_neighbors(dgraph, node))
#        final_list = []
#        final_list.extend(neighbor_list)
#        final_list.extend(node_list)
#        return list(set(final_list))

#    def change_node_att(self, g, node_list, att, value):
#        for node in node_list:
#            g.node[node].size = value
#        return g

    def get_propagated_places(self, frontier_places, property_places):

        final_list = []
        already_visited = []
        condition = []
        new_frontier = frontier_places

        while len(new_frontier) != 0 :
            save_frontier = new_frontier
            new_frontier = []

            for place in save_frontier :
                node = self.model.node_dict[place]
                for trans in node.outgoing_trans :
                    ext_place = trans.ext.name
                    if  ext_place not in already_visited :
                        already_visited.append(ext_place)
                        new_frontier.append(ext_place)

                    lno , lcl = self.test_get_tr_node_variables(trans)
                    condition.extend(lno)
            final_list.extend(new_frontier)

        new_frontier = property_places

        while len(new_frontier) != 0 :
            save_frontier = new_frontier
            new_frontier = []

            for place in save_frontier :
                node = self.model.node_dict[place]
                for trans in node.incoming_trans :
                    ori_place = trans.ori.name
                    if  ori_place not in already_visited :
                        already_visited.append(ori_place)
                        new_frontier.append(ori_place)

                    lno , lcl = self.test_get_tr_node_variables(trans)
                    condition.extend(lno)
            final_list.extend(new_frontier)

        new_frontier = property_places

        while len(new_frontier) != 0 :
            save_frontier = new_frontier
            new_frontier = []

            for place in save_frontier :
                node = self.model.node_dict[place]
                for trans in node.outgoing_trans :
                    ext_place = trans.ext.name
                    if  ext_place not in already_visited :
                        already_visited.append(ext_place)
                        new_frontier.append(ext_place)

                    lno , lcl = self.test_get_tr_node_variables(trans)
                    condition.extend(lno)
            final_list.extend(new_frontier)


        tr_graph = self.make_transition_dg()
        to_check_for_perm = []
        to_check_for_perm.extend(final_list)
        to_check_for_perm.extend(condition)
        to_check_for_perm.extend(property_places)
        to_check_for_perm = list(set(to_check_for_perm))

        perm_list = []
        for place in to_check_for_perm :
            predecessors = self.get_predecessors(tr_graph, place, None)
            for pred in predecessors :
                if self.model.node_dict[pred].is_perm():
                    if pred not in perm_list :
                        perm_list.append(pred)

        for place in perm_list :
            successors = self.get_successors(tr_graph, place, None)
            final_list.extend(successors)

        final_list = list(set(final_list))
        print len(final_list)
        return final_list


    def get_frontier_successors(self, tr_graph, frontier_places, property_places, perm = True):
        final_list = []
        to_check = frontier_places

        #Add permanent nodes
#        if perm :
#            for node in self.model.node_dict.keys():
#                if self.model.node_dict[node].is_perm():
#                    to_check.append(node)

        final_list.extend(frontier_places)
        final_list.extend(to_check)

        for place in to_check :
            successors = self.get_successors(tr_graph, place, None)
            final_list.extend(successors)

        final_list = list(set(final_list))


        perm_list = []
        important_places = []
        act_graph = self.make_dependence_dg()
        for place in to_check :
            successors = self.get_successors(act_graph, place, None)
            important_places.extend(successors)

        important_places.extend(property_places)
        important_places = list(set(important_places))

        for place in important_places :
            predecessors = self.get_predecessors(tr_graph, place, None)
            for pred in predecessors :
                if self.model.node_dict[pred].is_perm():
                    perm_list.append(pred)
        perm_list = list(set(perm_list))

        for place in perm_list :
            successors = self.get_successors(tr_graph, place, None)
            final_list.extend(successors)

        print len(list(set(final_list)))
        print list(set(final_list))
        return list(set(final_list))

    def get_submodel(self, node_list):
        new_model = copy.deepcopy(self.model)
        new_model_nodes = new_model.node_dict.keys()


    def remove_nodes_not_in_list(self, graph, node_list):
        """
        @return: a Networkx graph (or digraph) without nodes NOT in the input list
        """
        to_remove = graph.nodes()
        for node in to_remove :
            if node not in node_list:
                graph.remove_node(node)
        return graph

    def remove_nodes_in_list(self, graph, node_list):
        """
        @return: a Networkx graph (or digraph) without nodes in the input list
        """
        to_remove = graph.nodes()
        for node in to_remove :
            if node in node_list:
                graph.remove_node(node)
        return graph

    def in_degree_cut_off(self, dgraph, degree):
        """
        @return: a Networkx digraph without nodes with input degree upper than degree parameter
        """
        in_degree = dgraph.in_degree()
        node_list = dgraph.nodes()
        for node in node_list :
            if in_degree[node] > degree :
                dgraph.remove_node(node)
        return dgraph

    def out_degree_cut_off(self, dgraph, degree):
        """
        @return: a Networkx digraph without nodes with output degree upper than degree parameter
        """
        out_degree = dgraph.out_degree()
        node_list = dgraph.nodes()
        for node in node_list :
            if out_degree[node] > degree :
                dgraph.remove_node(node)
        return dgraph


    def export_2_graphml(self, graph, graphml_file):
        """
        As it says
        @param graph: the graph to export
        @param graphml_file: filename
        """
        nx.write_graphml(graph, graphml_file)

    def export_2_dot(self, graph, dot_file):
        """
        As it says
        @param graph: the graph to export
        @param dot_file: filename
        """
        nx.write_dot(graph, dot_file)



def stat_on_graph(graph):
    """
    ???
    """
    print 'number of nodes : ', graph.order()
    print 'number of edges : ', graph.number_of_edges()

    print 'number of connected components : ', \
           nx.number_connected_components(graph)

    if nx.is_connected(graph):
        print 'diameter : ', nx.diameter(graph) # max of shortest length
        print 'average path length : ', nx.average_shortest_path_length(graph)
        print 'density : ', nx.density(graph)
        print 'clustering : ', nx.clustering(graph)

    degree = graph.degree().items()
    degree.sort(cmpval)
    degree_moy = 0.0
    for degree_couple in degree :
        degree_moy += degree_couple[1]
    print 'degree moy : ', degree_moy / graph.order()

    print 'degree median : ', degree[len(degree) / 2][1]
    print 'degree : ', degree[:10]


def stat_on_dgraph(dgraph):
    """
    ???
    """
    print 'number of nodes : ', dgraph.order()
    print 'number of edges : ', dgraph.number_of_edges()
    nscc = nx.number_strongly_connected_components(dgraph)
    print 'number of strongly connected components : ', nscc

    in_degree = dgraph.in_degree().items()
    in_degree.sort(cmpval)
    print 'in degree : ', in_degree[:10]

    out_degree = dgraph.out_degree().items()
    out_degree.sort(cmpval)
    print 'out degree : ', out_degree[:10]


def view_graph(graph):
    """
    draw interaction graph with matplotlib
    """
    import matplotlib.pyplot as plt

    pos = nx.spring_layout(graph, iterations=5)
    low = []
    medium = []
    high = []
    hyper_high = []
    for node in graph:
        neighbors = graph.neighbors(node)
        if len(neighbors) <= 2:
            low.append(node)
        elif len(neighbors) > 2 and len(neighbors) <= 5:
            medium.append(node)
        elif len(neighbors) > 5 and len(neighbors) <= 10:
            high.append(node)
        else:
            hyper_high.append(node)

    nx.draw_networkx_nodes(graph, pos, nodelist=low, node_color='blue')
    nx.draw_networkx_nodes(graph, pos, nodelist=medium,
                           node_color='deepskyblue')
    nx.draw_networkx_nodes(graph, pos, nodelist=high, node_color='hotpink')
    nx.draw_networkx_nodes(graph, pos, nodelist=hyper_high,
                           node_color='crimson')
    nx.draw_networkx_edges(graph, pos)
#        nx.draw_networkx_labels(graph,pos)
    plt.show()


def view_weighted_graph(graph, rank):
    """
    ???
    """
    import matplotlib.pyplot as plt

    pos = nx.spring_layout(graph, iterations=10)
    edges = graph.edges(data=True)
    elarge = [(u, v) for (u, v, d) in edges if d['weight'] > 1]
    esmall = [(u, v) for (u, v, d) in edges if d['weight'] <= 1]

    # nodes

    nx.draw_networkx_nodes(graph, pos, node_size=100, nodelist=rank[0],
                           node_color='crimson')
    nx.draw_networkx_nodes(graph, pos, node_size=75, nodelist=rank[1],
                           node_color='hotpink')
    nx.draw_networkx_nodes(graph, pos, node_size=50, nodelist=rank[2],
                           node_color='deepskyblue')
    nx.draw_networkx_nodes(graph, pos, node_size=25, nodelist=rank[3],
                           node_color='blue')
    # edges
    nx.draw_networkx_edges(graph, pos, edgelist=elarge,
                        width=0.5, alpha=0.5)
    nx.draw_networkx_edges(graph, pos, edgelist=esmall,
                           width=0.5, alpha=0.5,
                           edge_color='dodgerblue', style='dashed')

    # labels
    nx.draw_networkx_labels(graph, pos, font_size=10, font_family='sans-serif')

    plt.axis('off')
#    plt.savefig("weighted_graph.png") # save as png

    plt.show() # display

def cmpval(xxx, yyy):
    """
    utility
    """
    if xxx[1] > yyy[1]:
        return -1
    elif xxx[1] == yyy[1]:
        return 0
    else:
        return 1

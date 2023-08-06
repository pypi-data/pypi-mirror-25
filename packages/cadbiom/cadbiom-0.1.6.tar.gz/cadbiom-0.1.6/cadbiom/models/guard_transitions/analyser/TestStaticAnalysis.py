
## Filename    : TestStaticAnalysis.py
## Author(s)   : Michel Le Borgne
## Created     : 14 may. 2012
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

import unittest
import sys
import networkx as nx

from cadbiom.models.guard_transitions.translators.chart_xml_pid import PidXmlParser
from cadbiom.models.guard_transitions.analyser.ana_visitors import \
                                     DirectFlowGraphBuilder
from cadbiom.models.guard_transitions.analyser.static_analysis import \
                                     StaticAnalyzer
from cadbiom.models.guard_transitions.translators.chart_lang import LangVisitor
from cadbiom.models.guard_transitions.chart_model import ChartModel

from cadbiom.models.guard_transitions.translators.chart_xml import \
                                     MakeModelFromXmlFile


TRACEFILE = sys.stdout
#TRACEFILE = open("/tmp/testMCLTranslator.txt",'w')


class Reporter(object):
    """
    Simple reporter for tests
    """
    def __init__(self):
        self.error = False
        self.mess = ""
        pass

    def display(self,  mes):
        """
        print message
        """
        self.error = True
        mess = self.mess + "ERROR -> "+mes
        TRACEFILE.write("\n\n"+ mess)

class TestAnaVisitors(unittest.TestCase):
    """
    Test visitor for static analysis
    """
    def test_frontier(self):
        """
        frontier visitor test
        """
        file_name = '../translators/tests/tgf_cano.xml'
        reporter = Reporter()
        parser = PidXmlParser(file_name, reporter)
        if reporter.error:
            print 'ERsROR IN READING FILE'

        cmodel = parser.model
        nx_graph = nx.DiGraph()
        gvi = DirectFlowGraphBuilder(nx_graph, False)
        cmodel.accept(gvi)

        aco = nx.attracting_components(nx_graph)
        scc = []
        for elem in aco:
            if len(elem)>1:
                scc.append(elem)
        print 'SCC FRONTIER  ', scc
        print aco



class TestStaticAnalysis(unittest.TestCase):
    """
    Test static analysis
    """
    def test_frontier1(self):
        """
        frontier computation
        """
        file_name = '../translators/tests/tgf_cano.xml'
        reporter = Reporter()
        parser = PidXmlParser(file_name, reporter)
        if reporter.error:
            print 'ERROR IN READING FILE'
        report = Reporter()
        sta = StaticAnalyzer(parser.model, report)
        print 'FRONTIER'
        ftr = sta.get_frontier_scc()
        print ftr
        # add a start transition on ft[0][1] (betaglycan__dimer___intToMb)
        parser.model.mark_as_frontier(ftr[0][1])
        out = open(file_name[:-4]+'_cmp.cal',"w")
        # decompiler visitor
        lvi = LangVisitor(out)
        parser.model.accept(lvi)
        out.close()

    def test_frontier1_no_clock(self):
        """
        test with a rather big clockless model
        """
        file_name = '../translators/tests/tgf_cano.xml'
        reporter = Reporter()
        parser = PidXmlParser(file_name, reporter, has_clock=False)
        if reporter.error:
            print 'ERROR IN READING FILE'
        report = Reporter()
        sta = StaticAnalyzer(parser.model, report)
        print 'FRONTIER'
        ftr = sta.get_frontier_scc()
        print ftr
        # add a start transition on ft[0][1] (betaglycan__dimer___intToMb)
        parser.model.mark_as_frontier(ftr[0][1])
        out = open(file_name[:-4]+'_noclock_cmp.cal',"w")
        # decompiler visitor
        lvi = LangVisitor(out)
        parser.model.accept(lvi)
        out.close()


    def test_frontier2(self):
        """
        frontier computation on all database
        """
        # test on all the database
        file_name = '../translators/tests/tgf_cano.xml'
        reporter = Reporter()
        parser = PidXmlParser(file_name, reporter)
        if reporter.error:
            print 'ERROR IN READING FILE'
        report = Reporter()
        sta = StaticAnalyzer(parser.model, report)
        print 'FRONTIER'
        print sta.get_frontier_scc()

    def test_get_tr_node_variables(self):
        """
        n1 --> n2; h1 when n2 default h2 when n3[not n4]
        n1 --> n3; h2 when n4[]
        n4 --> n1; h3[]
        """
        model = ChartModel("Test")
        root = model.get_root()
        node1 = root.add_simple_node('n1', 0, 0)
        node2 = root.add_simple_node('n2', 0, 0)
        node3 = root.add_simple_node('n3', 0, 0)
        node4 = root.add_simple_node('n4', 0, 0)
        tr1 = root.add_transition(node1, node2)
        tr1.set_condition("not n4")
        tr1.set_event('h1 when n2 default h2 when n3')
        tr2 = root.add_transition(node1, node3)
        tr2.set_event('h2 when n4')
        tr3 = root.add_transition(node4, node1)
        tr3.set_event('h3')

        report = Reporter()
        sta = StaticAnalyzer(report)
        sta.build_from_chart_model(model)
        lnn, lhh = sta.test_get_tr_node_variables(tr1)
        print lnn, lhh

    def test_principal_variables(self):
        """
        n1 --> n2; h1 when n2 default h2 when n3[not n4]
        n1 --> n3; h2 when n4[n1 or (not n4)]
        n4 --> n1; h3[n3 or not n4]
        """
        model = ChartModel("Test")
        root = model.get_root()
        node1 = root.add_simple_node('n1', 0, 0)
        node2 = root.add_simple_node('n2', 0, 0)
        node3 = root.add_simple_node('n3', 0, 0)
        node4 = root.add_simple_node('n4', 0, 0)
        tr1 = root.add_transition(node1, node2)
        tr1.set_condition("not n4")
        tr1.set_event('h1 when n2 default h2 when n3')
        tr2 = root.add_transition(node1, node3)
        tr2.set_event('h2 when n4')
        tr2.set_condition('n1 or (not n4)')
        tr3 = root.add_transition(node4, node1)
        tr3.set_condition('n3 or (not n4)')
        tr3.set_event('h3')

        report = Reporter()
        sta = StaticAnalyzer(model, report)
        pva = sta.get_tr_principal_variables(tr1)
        print pva

    def test_cadbiom_2_graphml(self):
        """
        test export in GML
        """
        file_name = '../translators/tests/pid0512.xml'
        report = Reporter()
        sta = StaticAnalyzer(report)
        sta.build_from_pid_file(file_name, has_clock=True, ai_interpretation=0)
        mgraph = sta.make_dependence_dg()
        fname = '../translators/tests/pid0512_dependenceGraph.graphml'
        sta.export_2_graphml(mgraph, fname)

    def test_get_pred_and_succ(self):
        """
        test predecessors and successors
        """
        file_name = '../../../bio_models/whole_pid_curated.bcx'
        report = Reporter()
        sta = StaticAnalyzer(report)
        sta.build_from_chart_file(file_name)
        graph = sta.make_dependence_dg()

        target = 'SNAIL'
        # PREDECESSORS
        pred = sta.get_predecessors(graph, target)
        print target, ' has  ', len(pred), ' predecessors'

        # SUCCESSORS
        succ = sta.get_successors(graph, target)
        print target, ' has  ', len(succ), ' successors'

    def test_pred_dependence_graph(self):
        """
        As it says
        """
        file_name = '../../../bio_models/tgf/tgf_canonical.bcx'
        report = Reporter()
        sta = StaticAnalyzer(report)
        sta.build_from_chart_file(file_name)
        graph = sta.make_dependence_dg()

        target = 'p15INK4b'
        # PREDECESSORS
        pred = sta.get_predecessors(graph, target)
        graph = sta.remove_nodes_not_in_list(graph, pred)
        fname = '../translators/tests/tgf_cano_p15_pred.graphml'
        sta.export_2_graphml(graph, fname)

    def test_pred_graph_extraction(self):
        """
        As it says
        """
        file_name = '../../../bio_models/tgf/tgf_canonical.bcx'
        report = Reporter()
        sta = StaticAnalyzer(report)
        sta.build_from_chart_file(file_name)
        graph = sta.make_dependence_dg()

        target = 'p15INK4b'
        # PREDECESSORS
        pred = sta.get_predecessors(graph, target)
        graph = sta.remove_nodes_not_in_list(graph, pred)

        #sta.extract_node_in_list(pred)


    def test_gene_signal_dependent(self):
        """
        As it says
        """
        file_name = '/home/gandrieu/these/cadbiom model/fevrier2012_newParser/whole_pid_man_noInhib_modif.bcx'
        parser = MakeModelFromXmlFile(file_name)
        report = Reporter()
        model = parser.get_model()
        sta = StaticAnalyzer(model, report)
        graph = sta.make_dependence_dg()
        # GENE RESEARCH
        gene_dict = dict() # key : gene, value : list of exCellRegion
        for node in graph.nodes():
            if len(node)>5:
                if node[-5:] == "_gene":
                    prot = node[:-5]
                    gene_dict[prot] = []
        # PREDECESSORS
        for gene in gene_dict.keys():
            gene_pred = sta.get_predecessors(graph, gene)
            for pred in gene_pred :
                if len(pred) > 13:
                    if pred[-13:] == "_exCellRegion":
                        gene_dict[gene].append(pred)
        print gene_dict['p15INK4b']
        print gene_dict['p21CIP1']
        # COUNTER
        dpt_dict = dict()
        for gene in gene_dict.keys():
            gene_dict[gene].sort()
            number_of_ex_cell_region = len(gene_dict[gene])
            if dpt_dict.has_key(number_of_ex_cell_region):
                dpt_dict[number_of_ex_cell_region] += 1
            else :
                dpt_dict[number_of_ex_cell_region] = 1
        dpt_items = dpt_dict.items()
        dpt_items.sort()
        for couple in dpt_items :
            print couple[1], ' genes(s) that depends on ', \
                    couple[0], ' signal(s)'



    def test_signal_gene_influent(self):
        """
        ???
        """
        file_name = '/home/gandrieu/these/cadbiom model/fevrier2012_newParser/whole_pid_man_noInhib_modif.bcx'
        parser = MakeModelFromXmlFile(file_name)

        report = Reporter()
        model = parser.get_model()
        sta = StaticAnalyzer(model, report)
        graph = sta.make_dependence_dg()
        # SIGNAL RESEARCH
        signal_dict = dict() # key : gene, value : list of exCellRegion
        for node in graph.nodes():
            if len(node)>13:
                if node[-13:] == "_exCellRegion":
                    signal_dict[node] = []
        # GENE RESEARCH
        gene_list = []
        for node in graph.nodes():
            if len(node)>5:
                if node[-5:] == "_gene":
                    prot = node[:-5]
                    gene_list.append(prot)
        # SUCCESSORS
        for signal in signal_dict.keys():
            signal_suc = sta.get_successors(graph, signal)
            for suc in signal_suc :
                if suc in gene_list :
                    signal_dict[signal].append(suc)
        # COUNTER
        dpt_dict = dict()
        for signal in signal_dict.keys():
            signal_dict[signal].sort()
            number_of_genes = len(signal_dict[signal])
            if dpt_dict.has_key(number_of_genes):
                dpt_dict[number_of_genes] += 1
            else :
                dpt_dict[number_of_genes] = 1
        dpt_items = dpt_dict.items()
        dpt_items.sort()
        for couple in dpt_items :
            print couple[1],' signal(s) regulates ', couple[0],' gene(s)'

    def test_ordering_pred(self):
        """
        write a predecessor file
        clustering predecessors into 10 class in fact of the distance of the shortest path to a given target
        Each line of the output file is a tab separated list of predecessors of the same class
        """

        file_name = '/home/gandrieu/these/models/cadbiom model/fevrier2012_newParser/whole_pid_man.bcx'
        parser = MakeModelFromXmlFile(file_name)

        report = Reporter()
        model = parser.get_model()
        sta = StaticAnalyzer(model, report)
        graph = sta.make_dependence_dg()
        prop = 'SNAIL'
        pred_list = sta.get_predecessors(graph, prop)
        max_dist = 0
        for pred in pred_list:
            dist = nx.shortest_path_length(graph, source=pred, target=prop)
            if dist > max_dist :
                max_dist = dist


        ordering_pred_list = [[], [], [], [], [], [], [], [], [], []]
        for pred in pred_list :
            dist = nx.shortest_path_length(graph, source=pred, target=prop)
            new_dist = dist * 100 / max_dist

            if new_dist <= 10 :
                ordering_pred_list[0].append(pred)
            elif new_dist <= 20 :
                ordering_pred_list[1].append(pred)
            elif new_dist <= 30 :
                ordering_pred_list[2].append(pred)
            elif new_dist <= 40 :
                ordering_pred_list[3].append(pred)
            elif new_dist <= 50 :
                ordering_pred_list[4].append(pred)
            elif new_dist <= 60 :
                ordering_pred_list[5].append(pred)
            elif new_dist <= 70 :
                ordering_pred_list[6].append(pred)
            elif new_dist <= 80 :
                ordering_pred_list[7].append(pred)
            elif new_dist <= 90 :
                ordering_pred_list[8].append(pred)
            else :
                ordering_pred_list[9].append(pred)

        fileOut='/home/gandrieu/these/gephi/script/snailOrderingPred.txt'
        fih = open(fileOut,'w')
        for pred_list in ordering_pred_list:
            for pred in pred_list:
                fih.write(pred + '\t')
            fih.write('\n')
        fih.close()

    def testStaticExtraction(self):
#        file_name = '../../../bio_models/whole_pid_man_noInhib_modif.bcx' # model without inhibitor
        file_name = '/home/gandrieu/these/processHitting/snail/whole_pid_man.bcx'
        parser = MakeModel_from_xml_file(file_name)

        report = Reporter()
        model = parser.get_model()
        sa = StaticAnalyzer(model, report)
        graph=sa.make_dependence_dg()

        # PREDECESSORS
#        pred = sa.get_predecessors(graph,'SNAIL')
#        pred=list(set(pred))
#        print len(pred)

        # LOAD FILE
        pred =[]
        f = open('/home/gandrieu/these/processHitting/snail/whole_pid_man_SNAIL_processes_nameList.txt','r')
        for line in f :
            line=line[:-1]
            pred.append(line)
        f.close()
        pred = list(set(pred))

#        f=open('/home/gandrieu/tmp/snail_pred_all_dependences.txt','w')
#        for node in pred:
#            f.write(node)
#            f.write('\n')
#        f.close()

#        pred = sa.get_list_neighbors(graph, pred)
#        print len(pred)
        # EXTRACTION
#        file_name = '../../../bio_models/whole_pid_curated.bcx'
#        parser = Make_model_from_xml_file(file_name)
        ex = SubModelExtraction(model,None,None)
        new_model = ex.extract_sub_model3(pred)
        new_model = perm_node_filter(new_model)
        xml = Xml_visitor(new_model)
        file = open("/home/gandrieu/tmp/whole_pid_man_extraction_SNAIL_PH_with_local_env.bcx",'w')
        file.write(xml.return_xml())
        file.close()

    def test_statistics(self):
        file_name = '../../../bio_models/pid_or_clock.bcx'
        report = Reporter()
        sta = StaticAnalyzer(report)
        sta.build_from_chart_file(file_name)
        stat_file = open('../../../bio_models/stat.txt','w')
        sta.get_statistics(stat_file)

    def test_model_extraction(self):
        file_name = '../../../bio_models/pid_or_clock.bcx'
        report = Reporter()
        sta = StaticAnalyzer(report)
        sta.build_from_chart_file(file_name)
#        graph = sta.make_dependence_dg()
        graph = sta.make_transition_dg()
        cam = ['ADAM10','HIF1A_cy','GammaSecretase_plasmaMb','ARNT_nucl','Jagged1_intToMb','SMAD2_3','SP1','IPAS','NOTCH1_golgiAp','MIZ_1','SHARP_RBPJ_CtIP_CtBP_LSD1_nucl','TGFB_TGFBR2_TGFBR1_DAB2_active_intToMb','SMAD4_nucl']
        prop = ['p15INK4b','p21CIP1']
#        sta.get_frontier_successors(graph, cam, prop, True)
        sta.get_propagated_places(cam, prop)

if __name__ == '__main__':

    import sys
    sys.setrecursionlimit(10000)

    suiteFew = unittest.TestSuite()
    suiteFew.addTest(TestStaticAnalysis('test_statistics'))
    unittest.TextTestRunner(verbosity=2).run(suiteFew)



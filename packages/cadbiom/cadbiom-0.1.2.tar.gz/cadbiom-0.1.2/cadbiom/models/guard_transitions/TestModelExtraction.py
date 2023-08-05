##
## Filename    : extract_visitor.py
## Author(s)   : Michel Le Borgne
## Created     : 5 nov. 2012
## Revision    :
## Source      :
##
## Copyright 2009 - 2012 : IRISA/IRSET
##
## This library is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published
## by the Free Software Foundation; either version 2.1 of the License, or
## any later version.
##
## This library is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY, WITHOUT EVEN THE IMPLIED WARRANTY OF
## MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.  The software and
## documentation provided hereunder is on an "as is" basis, and IRISA has
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
##     http:
##     mailto:
##
## Contributor(s): Geoffroy Andrieux
##
"""
Test Visitors for extracting submodels.
PathExtractor : abstract a trajectory as a set of path in the transition graph
"""

import unittest
import sys
from cadbiom.antlr3 import ANTLRFileStream, CommonTokenStream

from cadbiom.models.guard_transitions.translators.chart_xml_pid import PidXmlParser
from cadbiom.models.guard_transitions.translators.chart_lang import LangVisitor
#from models.guard_transitions.chart_model import ChartModel

#from models.guard_transitions.translators.chart_xml import \
#                                     MakeModelFromXmlFile
from cadbiom.models.guard_transitions.extract_visitor import PathExtractor
from cadbiom.models.guard_transitions.analyser.ana_visitors import EstimExpVisitor, \
                       TableVisitor,  FrontierVisitor, SigExpIdCollectVisitor
from cadbiom.models.guard_transitions.translators.cadlangLexer import cadlangLexer
from cadbiom.models.guard_transitions.translators.cadlangParser import cadlangParser
from cadbiom.models.guard_transitions.chart_model import ChartModel

class Reporter(object):
    """
    Simple reporter for tests
    """
    def __init__(self):
        self.error = False
        self.mess = ""

    def display(self,  mes):
        """
        print message
        """
        self.error = True
        mess = self.mess + "ERROR -> "+mes
        print "\n\n"+ mess

class TestExtractVisitors(unittest.TestCase):
    """
    Test visitor for model extraction
    """
    def test_exec1(self):
        """
        Test on simple exp
        """
        file_name = 'translators/tests/ext1.cal'
        reporter = Reporter()
        readf = ANTLRFileStream(file_name)
        lexer = cadlangLexer(readf)
        lexer.set_error_reporter(reporter)
        parser = cadlangParser(CommonTokenStream(lexer))
        parser.set_error_reporter(reporter)
        model = ChartModel('test1')
        parser.cad_model(model)
        model = parser.model

        target = ['C_D']
        frontier = ['F1', 'F2','F3']
        pex = PathExtractor(model, target, frontier, reporter)
        model.accept(pex)
        # decompiler visitor
        lvi = LangVisitor(sys.stdout)
        pex.extract_model.accept(lvi)

#    def test_exec2(self):
#        """
#        test visitor execution
#        """
#        file_name = 'translators/tests/tgf_cano.xml'
#        reporter = Reporter()
#        parser = PidXmlParser(file_name, reporter)
#        if reporter.error:
#            print 'ERROR IN READING FILE'
#        model = parser.model
#
#        tvi = TableVisitor(reporter)
#        model.accept(tvi)
#
#        target = ['TRAP_1']
#        frontier = ['TGFBR2__dimer___active_intToMb',
#                    'TGFBfamily__dimer___active_exCellRegion', 'CTGF']
#        pex = PathExtractor(model, target, frontier, reporter)
#        model.accept(pex)
#        # decompiler visitor
#        lvi = LangVisitor(sys.stdout)
#        pex.extract_model.accept(lvi)

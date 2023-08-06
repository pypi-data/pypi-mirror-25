##
## Filename    : TestCadlangCompiler.py
## Author(s)   : Michel Le Borgne
## Created     : 18/4/2012
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

import sys
import unittest
from cadbiom.antlr3 import ANTLRFileStream, CommonTokenStream

from cadbiom.models.guard_transitions.translators.pintlangLexer import pintlangLexer
from cadbiom.models.guard_transitions.translators.pintlangParser import pintlangParser
from cadbiom.models.guard_transitions.translators.chart_lang import LangVisitor

class Reporter(object):
    def __init__(self):
        self.error = False
        self.mess = ""
        pass

    def display(self, hdr, mes):
        self.error = True
        mess = self.mess + "ERROR -> "+hdr+' '+mes
        print mess



class PintlangTest(unittest.TestCase):

    def testSimple(self):
        """
        model with processes and actions only
        """
        err = Reporter()
        r = ANTLRFileStream("tests/test1.ph")
        lexer = pintlangLexer(r)
        lexer.set_error_reporter(err)
        parser = pintlangParser(CommonTokenStream(lexer))
        parser.set_error_reporter(err)
        parser.pintspec('test1')
        dc = LangVisitor(sys.stdout)
        parser.model.accept(dc)

    def testCoop1(self):
        """
        model with processes and actions only
        """
        err = Reporter()
        r = ANTLRFileStream("tests/test2.ph")
        lexer = pintlangLexer(r)
        lexer.set_error_reporter(err)
        parser = pintlangParser(CommonTokenStream(lexer))
        parser.set_error_reporter(err)
        parser.pintspec('test1')
        dc = LangVisitor(sys.stdout)
        parser.model.accept(dc)

    def testCoop2(self):
        """
        model with processes and actions only
        """
        err = Reporter()
        r = ANTLRFileStream("tests/test3.ph")
        lexer = pintlangLexer(r)
        lexer.set_error_reporter(err)
        parser = pintlangParser(CommonTokenStream(lexer))
        parser.set_error_reporter(err)
        parser.pintspec('test1')
        dc = LangVisitor(sys.stdout)
        parser.model.accept(dc)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()

    suiteFew = unittest.TestSuite()
    suiteFew.addTest(PintlangTest("testCoop2"))
    unittest.TextTestRunner(verbosity=2).run(suiteFew)

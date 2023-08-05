
## Filename    : TestExprCompiler.py
## Author(s)   : Michel Le Borgne
## Created     : 04/2010
## Revision    :
## Source      :
##
## Copyright 2010 : IRISA/IRSET
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
## Contributor(s): Geoffroy Andrieux, Nolwenn Le Meur
##
"""
Tests for the biosignal expression compiler
"""

import unittest
from cadbiom.models.biosignal.sig_expr import SigDefaultExpr, SigIdentExpr, \
                SigConstExpr, SigDiffExpr, SigEqualExpr, SigNotExpr, \
                SigEventExpr, SigWhenExpr, SigSyncBinExpr
from cadbiom.models.biosignal.translators.sigexpr_compiler import sigexpr_compiler
from cadbiom.models.biosignal.translators.sigexpr_lexer import sigexpr_lexer
from cadbiom.antlr3 import ANTLRStringStream, CommonTokenStream, RecognitionException


class Reporter(object):
    """
    Simple reporter
    """
    def __init__(self):
        self.mem = ">>>>>>>>"
        self.error = False
        pass

    def display(self, mess):
        """
        Just register messages
        """
        self.error = True
        print '--->' + mess
        self.mem = self.mem + "\n" + mess



class TestExpressionAnalyzer(unittest.TestCase):
    """
    The setup generates a collection of biosignal  expressions
    Test all elementary operators
    """

    def setUp(self):
        self.exp1 = SigIdentExpr('X1')
        self.exp2 = SigIdentExpr('X2')
        self.exp3 = SigIdentExpr('X3')
        self.exp4 = SigIdentExpr('X4')
        self.exp5 = SigConstExpr(True)
        self.exp6 = SigConstExpr(False)

        self.exp10 = SigDefaultExpr(self.exp1, self.exp2)    # X1 default X2
        self.exp11 = SigWhenExpr(self.exp3, self.exp4)       # X3 when X4
        self.exp12 = SigDiffExpr(self.exp1, self.exp4)       # X1 != X4
        self.exp13 = SigEqualExpr(self.exp2, self.exp4)      # X2 == X4
        self.exp14 = SigNotExpr(self.exp1)          # not X1
        self.exp15 = SigEventExpr(self.exp10)       # event (X1 default X2)
        self.exp16 = SigNotExpr(self.exp10)         # not (X1 default X2)
#        #(X1 != X4) + not (X1 default X2)
#        self.exp17 = SigPolyBinExpr('+', self.exp12, self.exp16)
#        # (not X1)*(not (X1 default X2))
#        self.exp18 = SigPolyBinExpr('*', self.exp14, self.exp16)
#        # (not X1)-(not (X1 default X2))
#        self.exp19 = SigPolyBinExpr('-', self.exp14, self.exp16)
#        # ((not X1)-(not (X1 default X2)))^2
#        self.exp20 = SigPolyPowExpr(self.exp19, 2)
#        self.exp21 = SigPolyPowExpr(self.exp19, 1)
#        # (event (X1 default X2))^2
#        self.exp22 = SigPolyPowExpr(self.exp15, 2)

        self.st1 = SigIdentExpr('S1')
        self.st2 = SigIdentExpr('S2')
        self.st3 = SigIdentExpr('S3')

        self.err_rep = Reporter()
        self.tab = {}
        self.tab['X1'] = "emit", 1
        self.tab['X2'] = "input", 1
        self.tab['X3'] = "emit", 1
        self.tab['X4'] = "emit", 1
        self.tab['S1'] = "state", 1
        self.tab['S2'] = "state", 1
        self.tab['S3'] = "state", 1

        self.err_rep = Reporter()

    def tearDown(self):
        """
        Nothing to do
        """
        pass

    def test_equal(self):
        """
        test expression equality (necessary for tests!!)
        """
        # ident
        res = self.exp1.test_equal(self.exp1)
        self.assert_(res, "Error in Expression equality Test01")

        res = self.exp1.test_equal(self.exp2)
        self.assert_(not res, "Error in Expression equality Test02")
        # default
        exp10 = SigDefaultExpr(self.exp1, self.exp2) # X1 default X2
        exp101 = SigDefaultExpr(exp10, self.exp3) #( X1 default X2) default X3
        res = exp101.test_equal(exp101)
        self.assert_(res, "Error in Expression equality Test1")
        # when
        exp11 = SigWhenExpr(self.exp3, self.exp4) # X3 when X4
        exp111 = SigWhenExpr(exp11, self.exp2) # (X3 when X4) when X2
        res = exp111.test_equal(exp111)
        self.assert_(res, "Error in Expression equality Test2")

        res = exp111.test_equal(exp101)
        self.assert_(not res, "Error in Expression equality Test3")
        # when and default
        exp112 = SigDefaultExpr(self.exp1, exp11)  # X1 default (X3 when X4)
        res = exp112.test_equal(exp112)
        self.assert_(res, "Error in Expression equality Test4")

        res = exp112.test_equal(exp101)
        self.assert_(not res, "Error in Expression equality Test5")

        # binary bool exp
        exp12 = SigSyncBinExpr('or', self.exp1, self.exp2)
        exp121 = SigWhenExpr(self.exp3, exp12)
        res = exp121.test_equal(exp121)
        self.assert_(res, "Error in Expression equality Test6")

        exp13 = SigSyncBinExpr('and', self.exp1, self.exp2)
        exp131 = SigWhenExpr(self.exp3, exp13)
        res = exp131.test_equal(exp131)
        self.assert_(res, "Error in Expression equality Test7")

        res = exp121.test_equal(exp131)
        self.assert_(not res, "Error in Expression equality Test8")
        # binary bool exp whith constants
        exp14 = SigSyncBinExpr('or', self.exp1, SigConstExpr(True))
        exp141 = SigSyncBinExpr('or', self.exp1, SigConstExpr(False))
        res = exp141.test_equal(exp141)
        self.assert_(res, "Error in Expression equality Test9")

        res = exp141.test_equal(exp14)
        self.assert_(not res, "Error in Expression equality Test10")


    def test_default(self):
        """
        default left associativity
        """
        sig_str = "X1 default X2 default X3 $"
        reader = ANTLRStringStream(sig_str)
        lexer = sigexpr_lexer(reader)
        parser = sigexpr_compiler(CommonTokenStream(lexer))
        parser.set_error_reporter(self.err_rep)
        try:
            exp_obj = parser.sig_expression(self.tab)
        except RecognitionException , exc:
            parser.displayExceptionMessage(exc)
            self.assert_(True, "Compiler error for default")

        exp10 = SigDefaultExpr(self.exp1, self.exp2) # X1 default X2
        exp101 = SigDefaultExpr(exp10, self.exp3) #( X1 default X2) default X3
        res = exp101.test_equal(exp_obj.exp)
        self.assert_(res, "Error in Expression analyzer for default")

    def test_when(self):
        """
        when left associativity
        """
        reader = ANTLRStringStream("X3 when X4 when X2 $")
        lexer = sigexpr_lexer(reader)
        parser = sigexpr_compiler(CommonTokenStream(lexer))
        parser.set_error_reporter(self.err_rep)
        try:
            exp_obj = parser.sig_expression(self.tab)
        except RecognitionException , exc:
            #parser.displayExceptionMessage(exc)
            self.assert_(True, "Compiler error for when")
        exp11 = SigWhenExpr(self.exp3, self.exp4) # X3 when X4
        exp111 = SigWhenExpr(exp11, self.exp2) # (X3 when X4) when X2
        res = exp111.test_equal(exp_obj.exp)
        self.assert_(res, "Error in Expression analyzer for when")

    def test_default_when(self):
        """
        priority of when over default
        """
        reader = ANTLRStringStream("(X1 default X3 when X4)$")
        lexer = sigexpr_lexer(reader)
        parser = sigexpr_compiler(CommonTokenStream(lexer))
        parser.set_error_reporter(self.err_rep)
        try:
            exp_obj = parser.sig_expression(self.tab)
        except RecognitionException , exc:
            #parser.displayExceptionMessage(exc)
            self.assert_(True, "Compiler error for default_when")
        exp11 = SigWhenExpr(self.exp3, self.exp4) # X3 when X4
        exp112 = SigDefaultExpr(self.exp1, exp11)  # X1 default (X3 when X4)
        res = exp112.test_equal(exp_obj.exp)
        mess = "Error in Expression analyzer for X1 default X3 when X4"
        self.assert_(res, mess)

    def test_void(self):
        """
        void string : default value True
        """
        reader = ANTLRStringStream("  $")
        lexer = sigexpr_lexer(reader)
        parser = sigexpr_compiler(CommonTokenStream(lexer))
        parser.set_error_reporter(self.err_rep)
        try:
            exp_obj = parser.sig_expression(self.tab)
        except RecognitionException , exc:
            #parser.displayExceptionMessage(exc)
            self.assert_(True, "Compiler error for void")
        expv = SigConstExpr(True)
        res = expv.test_equal(exp_obj.exp)
        mess = "Error in void expression - must default to True"
        self.assert_(res, mess)


#        exp11 = SigWhenExpr(self.exp3,self.exp4)  # X3 when X4
#        exp112 = SigDefaultExpr(self.exp1, exp11) # X1 default (X3 when X4)
#        res = exp112.test_equal(exp_obj.exp)
#        mess = "Error in Expression analyzer for (X1 and X3 and X4)"
#        self.assert_(res, mess)

    def test_when_or(self):
        """
        boolean operator precedence on when operators
        """
        reader = ANTLRStringStream("X3 when X4 or X2 $")
        lexer = sigexpr_lexer(reader)
        parser = sigexpr_compiler(CommonTokenStream(lexer))
        parser.set_error_reporter(self.err_rep)
        try:
            exp_obj = parser.sig_expression(self.tab)
        except RecognitionException , exc:
            #parser.displayExceptionMessage(exc)
            self.assert_(True, "Compiler error for when")
        exp11 = SigSyncBinExpr('or', self.exp4, self.exp2) # X4 or X2
        exp111 = SigWhenExpr(self.exp3, exp11) # X3 when (X4 or X2)
        res = exp111.test_equal(exp_obj.exp)
        self.assert_(res, "Error in Expression analyzer for when_or")

    def test_type_error1(self):
        """
        boolean expr on states in default
        """
        reader = ANTLRStringStream("X3 default (S3 or S2) $")
        lexer = sigexpr_lexer(reader)
        parser = sigexpr_compiler(CommonTokenStream(lexer))
        parser.set_error_reporter(self.err_rep)
        #parser.state_only = True
        try:
            exp_obj = parser.sig_expression(self.tab)
        except RecognitionException , exc:
            #parser.displayExceptionMessage(exc)
            self.assert_(True, "Compiler error for when")

        res = self.err_rep.error
        #print self.err_rep.mem
        self.assert_(res, "Type checking error in test_type_error1")

    def test_type_error2(self):
        """
        signal in when  with state_only option
        """
        reader = ANTLRStringStream("X3 when (S3 or X2) $")
        lexer = sigexpr_lexer(reader)
        parser = sigexpr_compiler(CommonTokenStream(lexer))
        parser.set_error_reporter(self.err_rep)
        parser.state_only = True
        try:
            exp_obj = parser.sig_expression(self.tab)
        except RecognitionException , exc:
            #parser.displayExceptionMessage(exc)
            self.assert_(True, "Compiler error for when")

        res = self.err_rep.error
        print self.err_rep.mem
        self.assert_(res, "Type checking error in test_type_error1")


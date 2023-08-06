##
## Filename    : SysExpr.py
## Author(s)   : Michel Le Borgne
## Created     : 11-12/2008
## Revision    : 
## Source      : 
##
## Copyright 2008 - 2009 : IRISA/IRSET
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
Standard representation of biosignal expressions as trees.
In addition to standard logical operator, we introduce the default
and when operators.
"""
# representation of signal expressions as trees

class SigExpression(object):
    """
    Generic abstract class
    """
    def __init__(self):
        pass
    def __str__(self):
        pass
    def get_signals(self):
        """
        Gives the set of idents used in the expression
        """
        return set([])
    
    def get_ultimate_signals(self, mcsystem):
        """
        Gives the set of signals used in the expression
        """
        return set([])
    
    def is_clock(self, symb_table, method=None):
        """
         Check if an expression always give a clock 
        """
        return False
    
    def is_ident(self):
        """
        As it says
        """
        return False
    
    def is_bot(self):
        """
        As it says
        """
        return False
    
    def is_const(self):
        """
        As it says
        """
        return False
    
    def is_const_false(self):
        """
        As it says
        """
        return False
    
    def accept(self, visitor):
        """
        Method for all kind of visitors - raise exception if not implemented
        """
        raise TypeError(self.__class__.__name__+": Not implemented")
    
    def test_equal(self, model):
        """
        test if the expression tree is equal to model tree (for TESTS)
        """
        pass
     
class SigIdentExpr(SigExpression):
    """
    Ident expressions are represented by their name. So we need a symbol
    table for type checking
    """
    def __init__(self, name):
        """
        @param name: the identifier 
        """
        self.name = name
        
    def __str__(self):
        return self.name
    
    def is_ident(self):
        return True
    
    def get_signals(self):
        return set([self.name])
    
    def get_ultimate_signals(self, mcsystem):
        try:
            scg = mcsystem.symbol_table[self.name]
        except:  # undefined component considered as ultimate
            return set([self.name])
        if scg.is_state():
            return set([self.name])
        elif scg.is_signal():
            sce = scg.expression
            if not sce: # undefined signal
                return set([self.name])
            else:
                return sce.get_ultimate_signals(mcsystem)
        else: # ???
            return set([self.name])
        
    def is_clock(self, symb_table, method=None):
        try:
            scg = symb_table[self.name]
            if not method:
                return scg.is_clock()
            else:
                return method(scg)
        except KeyError:
            return False

    def accept(self, visitor):
        return visitor.visit_sig_ident(self)
        
    def test_equal(self, model):
        if not isinstance(model, SigIdentExpr):
            return False
        else:
            return (self.name == model.name)
        
        
class SigConstExpr(SigExpression):
    """
    Constant signals: True, False
    """
    def __init__(self, val):
        """
        @param val: boll - the value 
        """
        self.value = val # boolean
        
    def __str__(self):
        return self.value.__str__()

    def get_signals(self):
        return set([])
    
    def is_clock(self, symb_table, method=None):
        """
        Tick and true are considered as similar
        """
        return self.value
    
    def is_const(self):
        return True
    
    def is_const_false(self):
        return not self.value
    
    def accept(self, visitor):
        return visitor.visit_sig_const(self)
        
    def test_equal(self, model):
        if not isinstance(model, SigConstExpr):
            return False
        else:
            return (self.value == model.value)
        
class SigBotExpr(SigExpression):
    """
    Usefull signal for initialisations - should not appear in normal signal expressions
    """
    def __init__(self):
        pass
        
    def __str__(self):
        return '%b'

    def get_signals(self):
        return set([])
    
    def is_bot(self):
        return True
    
    def accept(self, visitor):
        return visitor.visit_sig_bot(self)
        
    def test_equal(self, model):
        return isinstance(model, SigBotExpr)

class SigBinExpr(SigExpression):
    """
    Binary expression - abstract class
    """
    def __init__(self, exp1, exp2):
        """
        @param exp1,exp2: SigExpression - the two operands 
        """
        self.left_h = exp1
        self.right_h = exp2

    def __str__(self):
        pass
    
    def get_signals(self):
        sig1 = self.left_h.get_signals()
        sig2 = self.right_h.get_signals()
        sig1.update(sig2) #union of sets
        return sig1

    def get_ultimate_signals(self, mcsys):
        sig1 = self.left_h.get_ultimate_signals(mcsys)
        sig2 = self.right_h.get_ultimate_signals(mcsys)
        return sig1 | sig2 #union of sets
    
    
class SigDefaultExpr(SigBinExpr):
    """
    Implements the default operator
    """
    def __str__(self):
        if self.left_h.is_bot():
            return self.right_h.__str__()
        elif self.right_h.is_bot():
            return self.left_h.__str__()
        else:
            str = '('+self.left_h.__str__() + ' default '
            str = str  + self.right_h.__str__() + ')'
            return  str
    
    def is_clock(self, symb_table, method = None):
        cond = self.left_h.is_clock(symb_table, method)
        cond = cond and self.right_h.is_clock(symb_table, method)
        return  cond

    def accept(self, visitor):
        return visitor.visit_sig_default(self)

    def test_equal(self, model):
        if not isinstance(model, SigDefaultExpr):
            return False
        else:
            cond = self.left_h.test_equal(model.left_h)
            cond = cond and (self.right_h.test_equal(model.right_h))
            return cond
                    
class SigWhenExpr(SigBinExpr):
    """
    Implements when expression
    """
    def __str__(self):
        return '('+self.left_h.__str__()+' when '+self.right_h.__str__()+')'
    
    def is_clock(self, symb_table, method=None):
        return self.left_h.is_clock(symb_table, method)
    
    def accept(self, visitor):
        return visitor.visit_sig_when(self)
   
    def test_equal(self, model):
        if not isinstance(model, SigWhenExpr):
            return False
        else:
            cond = self.left_h.test_equal(model.left_h)
            cond = cond and (self.right_h.test_equal(model.right_h))
            return cond
        
class SigEqualExpr(SigBinExpr):
    """
    Implement the equality test: sig1 == sig2 when both present
    """
    def __str__(self):
        return '('+self.left_h.__str__()+' == '+self.right_h.__str__()+')'
    
    def is_clock(self, symb_table, method=None):
        cond = self.left_h.is_clock(symb_table, method)
        cond = cond and self.right_h.is_clock(symb_table, method)
        return  cond
    
    def accept(self, visitor):
        return visitor.visit_sig_equal(self)

    def test_equal(self, model):
        if not isinstance(model, SigEqualExpr):
            return False
        else:
            cond = self.left_h.test_equal(model.left_h)
            cond = cond and (self.right_h.test_equal(model.right_h))
            return cond
                    
class SigDiffExpr(SigBinExpr):
    """
    Implement the different test: sig1 != sig2 when both present
    """
    def __str__(self):    
        return '('+self.left_h.__str__()+' != '+self.right_h.__str__()+')'
    
    def is_clock(self, symb_table, method=None):
        return False
    
    def accept(self, visitor):
        return visitor.visit_sig_diff(self)

    def test_equal(self, model):
        if not isinstance(model, SigDiffExpr):
            return False
        else:
            cond = self.left_h.test_equal(model.left_h)
            cond = cond and (self.right_h.test_equal(model.right_h))
            return cond
        
class SigNotExpr(SigExpression):
    """
    Boolean not on a signal
    """
    def __init__(self, exp):
        self.operand = exp
        
    def __str__(self):
        return '( not '+self.operand.__str__()+')'

    def get_signals(self):
        return self.operand.get_signals()

    def get_ultimate_signals(self, mcsys):
        return self.operand.get_ultimate_signals(mcsys)

    def is_clock(self, symb_table, method=None):
        return False

    def accept(self, visitor):
        return visitor.visit_sig_not(self)

    def test_equal(self, model):
        if not isinstance(model, SigNotExpr):
            return False
        else:
            return (self.operand.test_equal(model.operand))
        
class SigEventExpr(SigExpression):
    """
    Event operand creates a clock
    """
    def __init__(self, exp):
        self.operand = exp
        
    def __str__(self):
        return 'event('+self.operand.__str__()+')'

    def get_signals(self):
        return self.operand.get_signals()
    
    def get_ultimate_signals(self, mcsys):
        return self.operand.get_ultimate_signals(mcsys)

    def is_clock(self, symb_table, method=None):
        return True

    def accept(self, visitor):
        return visitor.visit_sig_event(self)

    def test_equal(self, model):
        if not isinstance(model, SigEventExpr):
            return False
        else:
            return (self.operand.test_equal(model.operand))
                    
                    
class SigSyncBinExpr(SigBinExpr):
    """
    Generic class for boolean operation on signals
    A boolean operator emits a signal when both operand are present
    """
    def __init__(self, operator, exp1, exp2):
        self.left_h = exp1
        self.right_h = exp2
        self.operator = operator

    def __str__(self):
        lhs = self.left_h.__str__()
        rhs = self.right_h.__str__()
        return '('+ lhs +' '+self.operator+' '+rhs+')'
    
    def is_clock(self, symb_table, method=None):
        """
        Clocks are assimilated to boolean signals with true value
        And and or give true in this case, so its a clock!!
        """
        cond = self.left_h.is_clock(symb_table, method)
        cond = cond and self.right_h.is_clock(symb_table, method)
        return  cond

    def accept(self, visitor):
        return visitor.visit_sig_sync(self)

    def test_equal(self, model):
        if not isinstance(model, SigSyncBinExpr):
            return False
        else:
            cond = self.left_h.test_equal(model.left_h)
            cond = cond and (self.right_h.test_equal(model.right_h))
            cond = cond and self.operator == model.operator
            return cond

#class SigPolyBinExpr(SigBinExpr):
#    def __init__(self, op, exp1, exp2):
#        self.left_h = exp1
#        self.right_h = exp2
#        self.operator = op
#        
#    def __str__(self):
#        lhs = self.left_h.__str__()
#        rhs = self.right_h.__str__()
#        return '('+ lhs +' '+self.operator+' '+rhs+')'
#    
#    def is_clock(self, ts, method=None):
#        """
#        Clocks are assimilated to boolean signals with true value
#        In general a polynomial expression doesn't deliver a clock
#        """
#        return False
#    
#    def accept(self, visitor):
#        return visitor.visitSigPolyBinExpr(self)
#
#    def test_equal(self, model):
#        if not isinstance(model, SigPolyBinExpr):
#            return False
#        else:
#            cond = self.operator==model.operator
#            cond = cond and (self.left_h.test_equal(model.left_h)
#            cond = cond and (self.right_h.test_equal()))
#            return cond
#                            
#class SigPolyPowExpr(SigExpression):
#    def __init__(self, exp, pow):
#        self.operand = exp
#        self.power = pow%3
#        
#    def __str__(self):
#        op=self.operand.__str__()
#        return '('+ op +'^'+"%d"%(self.power)+')'
#
#    def get_signals(self):
#        return self.operand.get_signals()
#
#    def get_ultimate_signals(self, mcsys):
#        return self.operand.get_ultimate_signals(mcsys)
#
#    def is_clock(self, ts, method=None):
#        if self.power == 2:
#            return True
#        else:
#            return False
#        
#    def test_equal(self, model):
#        if not isinstance(model, SigPolyPowExpr):
#            return False
#        else:
#            cond = self.power==model.power
#            cond = cond and (self.operand.test_equal(model.operand))
#            return  cond
#                    
#    def accept(self, visitor):
#        return visitor.visitSigPowExpr(self)

class SigConstraintExpr(SigExpression):
    """
    Implements constraints on events
    """
    SYNCHRO = 'synchro'
    EXCLU = 'exclus'
    INCL = 'included'
    
    def __init__(self, name, explist=[]):
        self.constraint_name = name
        self.arg = explist
        
    def add_arg(self, arg):
        """
        Constraints are n-ary operators - this method add an operand
        """
        self.arg.append(arg)
        
    def __str__(self):
        str_out = self.constraint_name + '('
        if len(self.arg)>0:
            str_out = str_out + self.arg[0].__str__()
        for arg in self.arg[1:]:
            str_out = str_out +', '+arg.__str__()
        str_out = str_out+')'
        return str_out
    
    def accept(self, visitor):
        return visitor.visit_sig_constraint(self)



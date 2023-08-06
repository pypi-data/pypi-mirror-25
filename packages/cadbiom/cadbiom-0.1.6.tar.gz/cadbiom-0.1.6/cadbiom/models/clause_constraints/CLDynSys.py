
## Filename    : CLDynSys.py
## Author(s)   : Michel Le Borgne
## Created     : 05/2011
## Revision    : 
## Source      : 
##
## Copyright 2011 : IRISA/IRSET
##
## This library is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published
## by the Free Software Foundation; either version 2.1 of the License, or
## any later version.
##
## This library is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY, WITHOUT EVEN THE IMPLIED WARRANTY OF
## MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.  The software and
## documentation provided here under is on an "as is" basis, and  has
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
## Contributor(s): Geoffroy Andrieux
##
"""
Classes for building clause constraint models
"""
class Clause():
    """
    Objects representing logical clauses
    a clause is represented as a list of literals.
    """
    def __init__(self, list_lit=[]):
        self.list_of_literals = list_lit
        
    def add_lit(self, lit):
        """
        add a literal to the clause
        @param lit: Literal object
        """
        self.list_of_literals.append(lit)
        
    def __str__(self):
        """
        To print
        """
        clause_string = '$'
        for lit in self.list_of_literals[:-1]:
            clause_string += lit.__str__()+', '
        clause_string = clause_string + self.list_of_literals[-1].__str__()+'$'
        return clause_string
        
    def __repr__(self):
        return self.__str__()
    
    def equal(self, cl2):
        """
        test if two clauses have the same literals
        """
        if len(self.list_of_literals) != len(cl2.list_of_literals):
            return  False       
        sc1 = sorted(self.list_of_literals, cmp=lit_cmp)
        sc2 = sorted(cl2.list_of_literals, cmp=lit_cmp)
        for i in range(len(sc1)):
            if not lit_cmp(sc1[i], sc2[i]) == 0:
                return False
        return True
    
# helper functions mainly for tests    
def clause_cmp(cl1, cl2):
    """
    lexicographic order on ordered list of literals
    """
    sc1 = sorted(cl1.list_of_literals, cmp=lit_cmp)
    sc2 = sorted(cl2.list_of_literals, cmp=lit_cmp) 
    len1 = len(sc1)
    len2 = len(sc2)
    rlen = min(len1, len2)
    for i in range(rlen):
        cmp = lit_cmp(sc1[i], sc2[i])
        # if not equal - clauses ordered as literals   
        if cmp != 0:
            return cmp
    # the shorter clause is a prefix of the longuest one
    if len1 < len2:
        return -1
    elif len2 < len1:
        return 1
    else:
        return 0
    
def clause_list_equal(lc1, lc2):
    """
    compare two clause lists
    """
    if len(lc1) != len(lc2):
        return False
    slc1 = sorted(lc1, cmp=clause_cmp)
    slc2 = sorted(lc2, cmp=clause_cmp)
    for i in range(len(slc1)):
        if not slc1[i].equal(slc2[i]):
            return False
    return True
    
    
class Literal():
    """
    Object representing literals.
    A literal is a pair (string, boolean). The string is the variable name 
    and the boolean the sign of the literal. 
    """
    
    def __init__(self, name, sign):
        self.name = name
        self.sign = sign
        
    def lit_not(self):
        """
        returns the negation of the literal
        """
        return Literal(self.name, not self.sign)
    
    def equal(self, lit):
        """
        literal equality
        """
        return (lit.name == self.name) and (lit.sign == self.sign) 
    
    def opposite(self, lit):
        """
        true if one literal is the negation of the other
        """
        return (lit.name == self.name) and (lit.sign ==  (not self.sign)) 
                 
    def __str__(self):
        """
        For printing
        """
        if self.sign:
            return self.name
        else:
            return 'not '+self.name
        
    def code_name(self):
        """
        returns a string representing the literal
        """
        if self.sign:
            return self.name
        else:
            return '_' + self.name
        
    def __repr__(self):
        return self.__str__()

def lit_cmp(lit1, lit2):
    """
    for sorting clauses
    @param lit1, lit2: Literal
    @return:  1 if l1>l2, 0 if equal, -1 if l1<l2
    """
    if lit1.equal(lit2):
        return 0
    if lit1.name == lit2.name:
        if lit2.sign:  # l1 > l2
            return 1
        else:
            return -1 # l1 < l2
    else:
        if lit1.name < lit2.name:
            return -1
        else:
            return 1
    
    
        
class CLDynSys(object):
    """
    This class describe a dynamic system in clause form.
    @param symb_tab: name (string) -> type
    @param report: reporter for error reporting
    
    The frontier, free_clock, place_clock list are used for extractiong informations
    from solutions. The place_cock list is used for generating the structural constraint
    OR(P and h) implying that at least one clock transition must be activated at each step.
    """
    
    def __init__(self, symb_tab, report):
        # symbol table of charter model produced by Table_visitor
        # completed by add_free_clock
        self.symb_tab = symb_tab             
        self.report = report           # reporter for errors
        # set of variables of the dynamic system (including aux vars)
        self.base_var_set = set()      
        self.list_clauses = []         # clause form of the dynamic
        # structural constraints valid if there is no timing constraints
        self.aux_list_clauses = []     
        self.frontier = []             # frontier of the model 
        # complement of the frontier in the set of variables
        self.no_frontier = []          
        
        self.free_clocks = []          # free clocks inputs
        # dictionary clock h -> [place P] where P is the place 
        # preceding free clock h 
        self.place_clocks = dict()    
        self.inputs = []               # other inputs
        
        self.lit_compt = 0             # for auxiliary variables generation
        
    def add_var(self, name):
        """
        add a logical variable to the dynamic system
        @param name: the name of the variable (string)
        """
        if name in self.base_var_set: 
            return
        else:
            self.base_var_set.add(name)
    
    def add_aux_var(self):
        """
        create an auxiliary variable for compiler purpose
        """
        name = '_lit' + str(self.lit_compt)
        self.lit_compt += 1
        self.base_var_set.add(name)
        return name
    
    def add_free_clock(self, hname):
        """
        add a free clock variable
        @param hname: the name of the clock variable (string)
        """
        if hname in self.base_var_set: 
            return
        else:
            self.base_var_set.add(hname)
            self.free_clocks.append(hname)
            self.symb_tab[hname] = ('clock', -1)
            
    def add_place_clock(self, pname, hname):
        """
        add an association hname --> pname between a clock and an inductive place
        """
        try:
            lpn = self.place_clocks[hname]
            lpn.append(pname)
        except:
            # clock not registered
            self.place_clocks[hname] = [pname]
            
    def add_input(self, name):
        """
        add a variable representing an input
        @param name: name of the input 
        """
        if not name in self.base_var_set:
            self.base_var_set.add(name)
        self.inputs.append(name)
            
    def add_clause(self, cla):
        """
        add a clause constraint
        """
        #TODO: do not add satisfied clauses (n or not n)
        self.list_clauses.append(cla)
        
    def add_aux_clause(self, cla):
        """
        add an auxiliary clause constraint
        """
        self.aux_list_clauses.append(cla)
            
    def get_var_number(self):
        """
        returns the number of variables used in the system (including aux vars)
        """
        return len(self.base_var_set)
    
            

    
## Filename    : ana_visitors.py
## Author(s)   : Michel Le Borgne
## Created     : 04/2010
## Revision    : 03/2012
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
##     IRISA  Campus de Beaulieu
##     35042 RENNES Cedex, FRANCE 
##     
##
## Contributor(s): Geoffroy Andrieux, Nolwenn Le Meur
##
"""
Visitors for guarded transition model analysis
"""

class TableVisitor(object):
    """
    Visitor used to collect action and place declarations.
    Events and conditions are not considered so implicit free clocks are 
    not registered.
    The name of a place must be unique in a whole chart (no scope implemented).
    The same holds for an event declared in an action.
    Pseudo places used for inputs can be declared several time
    
    TYPES: state, input, emit 
    OTHER TYPES: clock (used when free clocks are found)
    """
    def __init__(self, erdisplay):
        # place name -> (type, deepness) 
        # type is state or input or emit (emitted events)
        self.tab_symb = dict()             
        self.error_reporter = erdisplay     # reporter to display errors
        self.error = False                  # True if an error is found
        self.deep = 0                       # imbrication level of macro states
        
    def declare(self, name, stype):
        """
        Register an identifier with its type
        """
        try:
            stype, deep = self.tab_symb[name]
            # error double declaration except for input
            self.error_reporter.display("Double declaration: "+name)
            self.error = True
        except KeyError:
            self.tab_symb[name] = (stype, self.deep)
        return
    
    def visit_chart_model(self, model):
        """
        first step in the visit
        """
        model.get_root().accept(self)
        
    def visit_cstart_node(self, node):
        """
        nothing to declare
        """
        return
    
    def visit_ctrap_node(self, node):
        """
        nothing to declare
        """
        return
    
    def visit_csimple_node(self, node):
        """
        register the node as a state
        """
        self.declare(node.name, "state")
        return
    
    def visit_cinput_node(self, node):
        """
        register the ident as input
        """
        try:
            ntype, deep = self.tab_symb[node.name]
            # double declaration allowed for input so we don't use declare
            # must be of the right type!
            if not (ntype == 'input'):
                self.error_reporter.display("Double declaration: " + node.name)
                self.error = True
            return
        except KeyError:
            # input places are put at level zero and are made unique
            self.tab_symb[node.name] = ('input', 0)
        return

    def visit_cperm_node(self, node):
        """
        register the node as a state
        """
        self.declare(node.name, "state")
        return
    
    def visit_cmacro_node(self, node):
        """
        register the node as a state
        deepness is updated
        """
        self.declare(node.name, "state")
        deepnest = self.deep
        self.deep = self.deep+1
        # sub states
        for sst in node.sub_nodes:
            sst.accept(self)
        self.deep = deepnest
        # transitions
        for gtr in node.transitions:
            for trans in gtr:
                trans.accept(self)
        return
    
    def visit_ctop_node(self, node):
        """
        after registering the node, visit subnodes and transitions
        """
        self.declare(node.name, "state")
        # sub states
        for sst in node.sub_nodes:
            sst.accept(self)
        # transitions
        for gtr in node.transitions:
            for trans in gtr:
                trans.accept(self)
    
    def visit_ctransition(self, trans):
        """
        visit transition
        """
        # transition actions are the only declared events at this level
        eve = trans.action # ident syntax to be checked later!!
        if eve != "":
            try:
                ntype, deep = self.tab_symb[eve]
                # error bad type
                if ntype != "emit":
                    mess = "Double declaration - different type: " + eve
                    self.error_reporter.display(mess)
                    self.error = True
            except KeyError:
                self.tab_symb[eve] = ("emit", self.deep)
        return

class FrontierVisitor(object):
    """
    Simple frontier computation for editor
    """
    def __init__(self):
        self.frontier = []
        
    def is_frontier(self, node):
        """
        Find if a node is a frontier node
        """
        itr = node.incoming_trans
        if itr == []:
            return True
        else:
            for trans in itr:
                if trans.ori.is_start():
                    return True
        return False
    
    def visit_chart_model(self, model):
        """
        Entrance for the visitor
        """
        model.get_root().accept(self)
        
    def visit_csimple_node(self, node):
        """
        check if it is a frontier node
        """
        if self.is_frontier(node):
            self.frontier.append(node.name)

    def visit_cstart_node(self, node):
        """
        Nothing to do
        """
        pass
    
    def visit_ctrap_node(self, node):
        """
        Nothing to do
        """
        pass  
    
    def visit_cinput_node(self, node):
        """
        Nothing to do
        """
        pass
    
    def visit_cmacro_node(self, node):
        """
        macros are not on the frontier
        """
        pass
    
    def visit_cperm_node(self, node):
        """
        Nothing to do
        """
        pass
    
    def visit_ctop_node(self, node):
        """
        visit subnodes
        """
        # sub states
        for sst in node.sub_nodes:
            sst.accept(self)
    
class IndirectFlowGraphBuilder(object):
    """
    build a networkx indirect graph of transitions
    """
    def __init__(self, nwx_graph):
        """
        @param nwx_graph:  networkx graph        
        nwx_graph is populated by place nodes and transition edges
        """
        self.graph = nwx_graph
        
    def visit_chart_model(self, model):
        """
        entrance through top node
        """
        model.get_root().accept(self)
        
    def visit_csimple_node(self, node):
        """
        Nothing to do
        """
        pass

    def visit_cstart_node(self, node):
        """
        Nothing to do
        """
        pass
    
    def visit_ctrap_node(self, node):
        """
        Nothing to do
        """
        pass  
    
    def visit_cinput_node(self, node):
        """
        Nothing to do
        """
        pass
    
    def visit_cmacro_node(self, node):
        """
        visit sub elements
        """
        for ltr in node.transitions:
            for trans in ltr:
                self.graph.add_edge(trans.ori.name, trans.ext.name)
        # sub states
        for sst in node.sub_nodes:
            sst.accept(self)
    
    def visit_cperm_node(self, node):
        """
        Nothing to do
        """
        pass
    
    def visit_ctop_node(self, node):
        """
        same as macro
        """
        self.visit_cmacro_node(node)
 
class DirectFlowGraphBuilder(object):
    """
    build a networkx graph of transitions
    """
    def __init__(self, nwx_graph, direct=True):
        """
        @param nwx_graph:  networkx Digraph 
        @param direct: true if direct graph is built (default), false for the inverse graph        
        nwx_graph is populated by place nodes and transition edges
        """
        self.graph = nwx_graph 
        self.direction = direct 
        
    def visit_chart_model(self, model):
        """
        entrance through top node
        """
        model.get_root().accept(self)
        
    def visit_csimple_node(self, node):
        """
        Nothing to do
        """
        pass

    def visit_cstart_node(self, node):
        """
        Nothing to dot
        """
        pass
    
    def visit_ctrap_node(self, node):
        """
        Nothing to do
        """
        pass  
    
    def visit_cinput_node(self, node):
        """
        Nothing to do
        """
        pass
    
    def visit_cmacro_node(self, node):
        """
        collect edges from transitions
        """
        for ltr in node.transitions:
            for trans in ltr:
                if self.direction:
                    self.graph.add_edge(trans.ori.name, trans.ext.name)
                else:
                    self.graph.add_edge(trans.ext.name, trans.ori.name)
        # sub states
        for sst in node.sub_nodes:
            sst.accept(self)
    
    def visit_cperm_node(self, node):
        """
        Nothing to do
        """
        pass
    
    def visit_ctop_node(self, node):
        """t
        same as macro
        """
        self.visit_cmacro_node(node)
 
 
class EstimExpVisitor(object):
    """
    Partial Evaluator of event and condition expressions (subset of sig expressions)
    The value of an expression is either True (1) or False (-1) or Indeterminate (0)
    If no symbol table, all variables are evaluated to False
    """
    def __init__(self, symb_t):
        """
        @param symb_t: symbol table associating values to SOME places 
        """
        self.symb_table = symb_t # this symbol table must contains name-> value

    def visit_sig_ident(self, iex):
        """
        @param iex: the biosignal ident expression
        """
        if not self.symb_table:
            return -1
        try:
            val = self.symb_table[iex.name] # 1 or -1
        except KeyError:
            val = 0 # indeterminate
        return val
    
    def visit_sig_const(self, cex):
        """
        coding of the constant on 1,-1
        """
        if cex.value:
            return 1
        else:
            return -1
    
    def visit_sig_default(self, dex):
        """
        this evaluation is valid for clocks only
        """
        cv1 = dex.left_h.accept(self)
        cv2 = dex.right_h.accept(self)
        return max(cv1 , cv2)

    def visit_sig_when(self, wex):
        """
        left operand is a clock and right operand a condition
        """
        cv1 = wex.left_h.accept(self)
        cv2 = wex.right_h.accept(self)
        return min(cv1 , cv2)

    def visit_sig_equal(self, eex):
        """
        not yet implemented
        """
        pass

    def visit_sig_sync(self, sex):
        """
        estimation depends on the operator
        """
        cv1 = sex.left_h.accept(self)
        cv2 = sex.right_h.accept(self)
        if sex.operator == 'or':
            return max(cv1 , cv2)
        if sex.operator == 'and':
            return min(cv1 , cv2)

    def visit_sig_not(self, nex):
        """
        opposite in our coding
        """
        cv1 = nex.operand.accept(self)
        return -cv1


class SigExpIdCollectVisitor(object):
    """
    Collect idents in a sig expression
    """
    def __init__(self):
        """
        simple walker 
        """
        pass

    def visit_sig_ident(self, iexp):
        """
        @param iexp: the expression
        """
        return [iexp.name]
    
    def visit_sig_const(self, cexp):
        """
        no id
        """
        return []
    
    def visit_sig_default(self, dexp):
        """
        ids come from both operands
        """
        ll1 = dexp.left_h.accept(self)
        ll2 = dexp.right_h.accept(self)
        return ll1 + ll2

    def visit_sig_when(self, wexp):
        """
        ids come from both operands
        """
        ll1 = wexp.left_h.accept(self)
        ll2 = wexp.right_h.accept(self)
        return ll1 + ll2

    def visit_sig_equal(self, eex):
        """
        not implemented
        """
        pass

    def visit_sig_sync(self, sex):
        """
        ids come from both operands
        """
        ll1 = sex.left_h.accept(self)
        ll2 = sex.right_h.accept(self)
        return ll1 + ll2

    def visit_sig_not(self, nex):
        """
        same as operand
        """
        ll1 = nex.operand.accept(self)
        return ll1
 

    
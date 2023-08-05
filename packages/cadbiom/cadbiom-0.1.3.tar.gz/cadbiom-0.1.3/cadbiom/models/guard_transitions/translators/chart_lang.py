
##
## Filename    : chart_lang.py
## Author(s)   : Michel Le Borgne
## Created     : 2/1/2012
## Revision    : 
## Source      : 
##
## Copyright 2009 - 2012 : IRISA
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
##  have been advised of the possibility of such damage.  See
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


class LangVisitor(object):
    '''
    Decompiler from chart model to chart language description.
    '''
    PERM_N = '/p'
    INPUT_N = '/i'
    MACRO_N = '/m'
    
    MACRO = '/macro'
    ENDMACRO = '/endmacro'
    INDENT = "    "
    TARROW = " --> "
    
    def __init__(self, outfile):
        '''
        Constructor
        '''
        self.file = outfile
        self.indent = ""
        
    def visit_chart_model(self, mod):
        """
        Entry point in the model
        """
        if not mod.name == "":
            self.file.write("/name  "+ mod.name +"\n")
        mod.get_root().accept(self)
        if len(mod.constraints)>0: 
            self.file.write("/constraints\n")
            self.file.write(mod.constraints)
            self.file.write("\n/endconstraints\n")
        
    def visit_cstart_node(self, node):
        """
        Nothing to do
        """
        return ""
    
    def visit_ctrap_node(self, node):
        """
        Nothing to do
        """
        return ""
    
    def visit_csimple_node(self, node):
        """
        create an ident
        """
        return node.name
    
    def visit_cperm_node(self, node): 
        """
        return the mangled name
        """
        return node.name + self.PERM_N
    
    def visit_cinput_node(self, node): 
        """
        return the mangled name
        """
        return node.name + self.INPUT_N
    
    def visit_cmacro_node(self, mnode):
        """
        Generate the textual description of a macro
        """
        self.file.write("\n"+self.indent + self.MACRO + " "+ mnode.name + "\n")
        old_indent = self.indent
        self.indent = self.indent + self.INDENT
        # nodes
        for snode in mnode.sub_nodes:
            if not snode.is_macro(): 
                cond = (snode.incoming_trans == []) 
                cond = cond and (snode.outgoing_trans == [])
                if cond: # isolated nodes
                    dec = snode.accept(self)
                    if not dec == "":
                        self.file.write(self.indent + dec + " ;\n")
                # nodes used in transitions are not declared
            else:
                snode.accept(self)
        # transitions
        for trg in mnode.transitions:
            for trans in trg:
                trans.accept(self)
        # end
        self.indent = old_indent
        self.file.write(self.indent + self.ENDMACRO + "\n\n")
        return mnode.name
    
    def visit_ctop_node(self, tnode):    
        """
        Same as macro node except for indentation and constraints
        """
        # nodes
        self.file.write("// =============== macros nodes================\n\n")
        for snode in tnode.sub_nodes:
            if snode.is_macro():
                snode.accept(self)
        out_str = "// =============== isolated nodes ================\n\n"
        self.file.write(out_str)
        for snode in tnode.sub_nodes:
            if not snode.is_macro(): 
                cond = (snode.incoming_trans == []) 
                cond = cond and (snode.outgoing_trans == [])
                if cond: # isolated nodes
                    dec = snode.accept(self)
                    if not dec == "":
                        self.file.write(self.indent + dec + " ;\n")
        # transitions
        out_str = "\n\n// =============== transitions ================\n\n"
        self.file.write(out_str)
        for trg in tnode.transitions:
            for trans in trg:
                trans.accept(self)
        
        # constraints
        #TODO
        
    
    def visit_ctransition(self, trans): 
        """
        compile a transition
        """
        # macro nodes must be defined before use in transitions
        if not trans.ori.is_macro():   
            ori_txt = trans.ori.accept(self)
        else:
            ori_txt = trans.ori.name
        if not trans.ext.is_macro():
            target_txt = trans.ext.accept(self)
        else:
            target_txt = trans.ext.name
        event_expr = trans.event
        cond_expr = trans.condition
        action_expr = trans.action
        if event_expr and not trans.ori.is_start():
            guard = event_expr + "[" + cond_expr + "]"
        elif not trans.ori.is_start():
            guard = "[" + cond_expr + "]"
        else:
            guard = ""
        if action_expr:
            guard = guard + action_expr + " "
        else:
            guard = guard + " "
        out_str = self.indent + ori_txt + self.TARROW + target_txt + ";\n"
        self.file.write(out_str)
        self.file.write(self.indent + self.INDENT + guard)
        if not trans.note == "":
            note = "{" + trans.note + "}"
            self.file.write("\n"+ self.indent + self.INDENT + note)
        self.file.write(";\n\n")

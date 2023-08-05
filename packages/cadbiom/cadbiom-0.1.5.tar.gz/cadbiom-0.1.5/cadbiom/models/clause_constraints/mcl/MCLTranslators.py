## Filename    : MCLTranslators.py
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
##     IRISA  Campus de Beaulieu
##     35042 RENNES Cedex, FRANCE
##
##
## Contributor(s):
##
"""
Translators from guarded transition models to clause constraint models
"""
from cadbiom.models.biosignal.sig_expr import SigIdentExpr, SigSyncBinExpr, \
                            SigConstraintExpr

from cadbiom.models.biosignal.translators.gt_visitors import compile_cond, \
                            compile_event, compile_constraint

from cadbiom.models.clause_constraints.CLDynSys import Literal, Clause


class MCLNoImplemented(Exception):
    """
    Exception for non implemented features
    """
    def __init__(self, mess):
        self.message = mess


class MCLSigExprVisitor(object):
    """
    visit a restricted SigExpression (type restrictions on default operands (both clocks)
    and when operands (clock, logical condition on states) and add clauses
    to logical dynamic system to encode y = f(X). SigExpressions are restricted.
    The variable y is represented as a literal for optimization reasons. It can be
    given as a parameter or generated as an intermediate literal.
    The generated clauses enforce the constraint y <=> f(X).
    All the expressions are memorized to implement common subexpression elimination.

    @param cldyn_sys: the dynamical system to be generated in clause form
    @param output: the variable name y or None for intermediate expressions)
    @param subexpressions: dictionary op#x#y -> literal for subexpressions memorization
    """
    def __init__(self, cldyn_sys, output, subexpressions = None):
        """
        @param cldyn_sys: clause constraint dynamical system to pupulate
        """
        self.reporter = cldyn_sys.report
        self.cldyn_sys = cldyn_sys
        # cannot test optimisation "turn on" on dictionary: empty dict => False
        if subexpressions == None:
            self.sub_dict = None
            self.opti = False
        else:
            self.sub_dict = subexpressions
            self.opti = True

        if output:
            # added because it may not appear in evolution
            self.cldyn_sys.add_var(output)
            self.output_lit = Literal(output, True) # output literal y
        else:
            self.output_lit = None

    def visit_sig_ident(self, sexpr):
        """
        if self.output(y) we have either y = x or (not y) = x - the y variable disappears
        either we are in an intermediate sexpr: returns the corresponding literal
        """
        # register variable names
        name = sexpr.name
        self.cldyn_sys.add_var(name)
        nlit = Literal(name, True)
        notnl = nlit.lit_not()
        # y = x : sexpr is top node of an expression
        if self.output_lit:
            if self.output_lit.sign:
                return nlit
            else:
                return notnl
        else:
            return nlit  # return the ident (Literal) if no output_var


    def visit_sig_not(self, sexpr):
        """
        if y is given and the expression is not f(X) we generate not y <=> f(X)
        """
        if self.output_lit: # y = not exp or (not y) = not expr
            slit = self.output_lit
            self.output_lit = self.output_lit.lit_not()
            notnl = sexpr.operand.accept(self)
            self.output_lit = slit # restore preceding value
        else :
            nlit = sexpr.operand.accept(self)
            notnl = nlit.lit_not()
        # don't generate more clauses than operand
        return notnl


    def visit_sig_sync(self, binsexpr):
        """
         the output_var is the next variable, the root of the tree
         we affect this name to the root and change output_var to None for the other BinExpression
        """
        # case y = f(X)
        if self.output_lit:
            nlit = self.output_lit
            notnl = nlit.lit_not()
        # sub expression: an auxiliary literal is introduced (nlit = f(X))
        else:
            name = self.cldyn_sys.add_aux_var()
            nlit = Literal(name, True)
            notnl = Literal(name, False)

        # recursive visits of operands
        olit = self.output_lit
        self.output_lit = None
        nlit1 = binsexpr.left_h.accept(self)
        notnl1 = nlit1.lit_not()
        nlit2 = binsexpr.right_h.accept(self)
        notnl2 = nlit2.lit_not()
        self.output_lit = olit

        # is a similar expression already visited?
        operator = binsexpr.operator
        if self.opti:
            var = search_sub_exp(operator, nlit1, nlit2, True, self.sub_dict)
            if var:
                if self.output_lit: # y = var
                    notnvar = var.lit_not()
                    cl1 = Clause([notnl, var])
                    cl2 = Clause([nlit, notnvar])
                    self.cldyn_sys.add_clause(cl1)
                    self.cldyn_sys.add_clause(cl2)
                    return self.output_lit
                return var

        # no sub expression: clauses generation for nlit = f(X)
        if operator == 'and': # nlit = lh and rh
            cl1 = Clause([nlit1, notnl])         # not nlit or not lh
            cl2 = Clause([nlit2, notnl])         # not nlit or not rh
            cl3 = Clause([notnl1, notnl2, nlit]) # nlit or not lh or not rh

        if operator == 'or':    # nlit =  or rh
            cl1 = Clause([notnl1, nlit])        # nlit or not lh
            cl2 = Clause([notnl2, nlit])        # nlit or not rh
            cl3 = Clause([nlit1, nlit2, notnl])   # not nlit or not lh or not rh

        self.cldyn_sys.add_clause(cl1)
        self.cldyn_sys.add_clause(cl2)
        self.cldyn_sys.add_clause(cl3)

        # sub expression memorization
        if self.opti:
            key = operator + '#' + nlit1.code_name() + '#' + nlit2.code_name()
            self.sub_dict[key] = nlit
        return nlit

    def visit_sig_const(self, exp):
        """
        compile a constant signal
        """
        if self.output_lit:
            nlit = self.output_lit
            notnl = nlit.lit_not()

            if exp.value:
                cla = nlit  # y = True
            else:
                cla = notnl  # y = False

        # the internal nodes will be affected with the name '_lit'
        else:
            name = self.cldyn_sys.add_aux_var()
            nlit = Literal(name, True)
            notnl = Literal(name, False)
        # clause generation
        if exp.value:
            cla = nlit  # x = True
        else:
            cla = nlit.lit_not()
        self.cldyn_sys.add_clause(Clause([cla]))
        return nlit

    def visit_sig_bot(self, bex):
        """
        The always absent clock
        """
        raise MCLNoImplemented("SigBotVisitor: Not yet implemented")

    def visit_sig_default(self, dex):
        """
        @param dex: default expression: lhs default rhs

        default is restricted to clocks
        """
        # case y = f(X)
        if self.output_lit:
            nlit = self.output_lit
            notnl = nlit.lit_not()
        # sub expression: an auxiliary literal is introduced (nlit = f(X))
        else:
            name = self.cldyn_sys.add_aux_var()
            nlit = Literal(name, True)
            notnl = Literal(name, False)

        # check if both operands are clocks
        if not dex.is_clock(self.cldyn_sys.symb_tab, check_clock):
            mess = "Default signal:"+dex.__str__()+" is not a clock"
            self.reporter.display(mess)
            return nlit # no meaning

        # visit recursively each operand
        olit = self.output_lit
        self.output_lit = None
        nl1 = dex.left_h.accept(self)
        notnl1 = nl1.lit_not()
        nl2 = dex.right_h.accept(self)
        notnl2 = nl2.lit_not()
        self.output_lit = olit

        # is a similar expression already visited?
        operator = 'default'
        if self.opti:
            var = search_sub_exp(operator, nl1, nl2, True, self.sub_dict)
            if var:
                if self.output_lit: # y = var
                    notnvar = var.lit_not()
                    cl1 = Clause([notnl, var])
                    cl2 = Clause([nlit, notnvar])
                    self.cldyn_sys.add_clause(cl1)
                    self.cldyn_sys.add_clause(cl2)
                    return self.output_lit
                return var

        # generate nlit = nl1 or nl2
        self.cldyn_sys.add_clause(Clause([notnl, nl1, nl2]))  # nl => nl1 or nl2
        self.cldyn_sys.add_clause(Clause([notnl1, nlit]))     # nl1 => nlit
        self.cldyn_sys.add_clause(Clause([notnl2, nlit]))     # nl2 => nlit

        # sub expression memorization
        if self.opti:
            key = operator + '#' + nl1.code_name() + '#' + nl2.code_name()
            self.sub_dict[key] = nlit
        return nlit

    def visit_sig_when(self, wex):
        """
        When expression
        @param wex: when expression

        the left operand must be a clock and the right one must be
        a boolean exp on states and inputs (checked on syntax analysis)
        """
        # case y = f(X)
        if self.output_lit:
            nlit = self.output_lit
            notnl = nlit.lit_not()
        # sub expression: an auxiliary literal is introduced (nlit = f(X))
        else:
            name = self.cldyn_sys.add_aux_var()
            nlit = Literal(name, True)
            notnl = Literal(name, False)

        # check if left operand is clock
        if not wex.left_h.is_clock(self.cldyn_sys.symb_tab, check_clock):
            mess = "Default signal:"+wex.__str__()+" is not a clock"
            self.reporter.display(mess)
            return nlit # no meaning

        # visit recursively each operand
        olit = self.output_lit
        self.output_lit = None
        nl1 = wex.left_h.accept(self)
        notnl1 = nl1.lit_not()
        nl2 = wex.right_h.accept(self)
        notnl2 = nl2.lit_not()
        self.output_lit = olit

        # is a similar expression already visited?
        operator = 'when'
        if self.opti:
            var = search_sub_exp(operator, nl1, nl2, False, self.sub_dict)
            if var:
                if self.output_lit: # y = var
                    notnvar = var.lit_not()
                    cl1 = Clause([notnl, var])
                    cl2 = Clause([nlit, notnvar])
                    self.cldyn_sys.add_clause(cl1)
                    self.cldyn_sys.add_clause(cl2)
                    return self.output_lit
                return var
        # generate nlit = nl1 and nl2
        #  nl1 and nl2 => nlit
        self.cldyn_sys.add_clause(Clause([notnl1, notnl2, nlit]))
        self.cldyn_sys.add_clause(Clause([notnl, nl1]))     # nlit => nl1
        self.cldyn_sys.add_clause(Clause([notnl, nl2]))     # nlit => nl2

        # sub expression memorization
        if self.opti:
            key = operator + '#' + nl1.code_name() + '#' + nl2.code_name()
            self.sub_dict[key] = nlit
        return nlit

    def visit_sig_constraint(self, cex):
        """
        generate clause constraints for clock constraints
        """
        if cex.constraint_name == SigConstraintExpr.SYNCHRO:
            gen_code_synchro(cex, self)
        elif cex.constraint_name == SigConstraintExpr.EXCLU:
            gen_code_exclu(cex, self)
        elif cex.constraint_name == SigConstraintExpr.INCL:
            gen_code_included(cex, self)
        else:
            self.reporter.display("Unknown constraint type: " + cex.name)

    def visit_sig_equa(self, eex):
        """
        TODO
        """
        raise MCLNoImplemented("MCLSigExprVisitor: Not yet implemented")

    def visit_sig_diff(self, dix):
        """
        TODO
        """
        raise MCLNoImplemented("MCLSigExprVisitor: Not yet implemented")

# helper fonctions
def gen_code_synchro(cex, visit):
    """
    code generator for a synchro constraint
    """
    if len(cex.arg) <2:
        visit.reporter.display("Incorrect clock synchro")
        return None
    exp = cex.arg[0]
    lit1 = exp.accept(visit)
    for exp in cex.arg[1:]:
        lit = exp.accept(visit)
        visit.cldyn_sys.add_clause(Clause([lit1.lit_not(), lit]))
        visit.cldyn_sys.add_clause(Clause([lit1, lit.lit_not()]))
        lit1 = lit

def gen_code_exclu(cex, visit):
    """
    code generator for an exclusion constraint
    """
    if len(cex.arg) <2:
        visit.reporter.display("Incorrect clock exclusion")
        return None
    llit = []
    for exp in cex.arg:
        lit = exp.accept(visit)
        llit.append(lit)
    for i in range(len(llit)):
        for j in range(i+1, len(llit)):
            visit.cldyn_sys.add_clause(Clause([llit[i].lit_not(),
                                               llit[j].lit_not()]))

def gen_code_included(cex, visit):
    """
    code generator for an inclusion constraint
    """
    if len(cex.arg) !=2:
        visit.reporter.display("Incorrect clock inclusion")
        return None
    lit1 = cex.arg[0].accept(visit)
    lit2 = cex.arg[1].accept(visit)
    visit.cldyn_sys.add_clause(Clause([lit1.lit_not(), lit2]))

def search_sub_exp(ope, op1, op2, com, sub_dict):
    """
    search if an expression a op b was already translated to clause constraints
    @param ope: operator (string)
    @param op1: left operand (literal)
    @param op2: right operand (literal)
    @param com: bool - true if operator is commutative
    @param sub_dict:directory of sub expressions
    """
    key = ope + '#' + op1.code_name() + '#' + op2.code_name()
    try:
        val_var = sub_dict[key]
        return val_var
    except KeyError:
        if com:
            key = ope + '#' + op2.code_name() + '#' + op1.code_name()
            try:
                val_var = sub_dict[key]
                return val_var
            except KeyError:
                return None
        else:
            return None

class GT2Clauses(object):
    """
    visit a charter_model based on guarded transitions and populate the associated
    CLSysDyn with clauses implementing the evolution constraints X' = f(X).
    Compute the frontier of the charter model. Frontier places are places without
    incoming transition or with a start incoming transition. In the later case,
    other transitions may exist.
    """

    def __init__(self, cldyn_sys, reporter, opti):
        """
        @param cldyn_sys: a new dynamic system in clause constraints.
        """
        self.cl_ds = cldyn_sys              # CLSysDyn to be populated
        self.reporter = reporter  # for error reporting
        if opti:
            self.sub_exp = dict()     # for subexpression elimination
        else:
            self.sub_exp = None


    def visit_chart_model(self, model):
        """
        Enter a model - after traversal, clock constraints are compiled
        """
        model.clean_code()
        model.get_root().accept(self)
        gen_aux_clock_constraints(self.cl_ds)
        gen_clock_constraints(model.constraints, self.cl_ds,
                              self.sub_exp, self.reporter)

    def visit_csimple_node(self, node):
        """
        simple node compilation
        """
        # register variable
        self.cl_ds.add_var(node.name)
        # frontier - registered for solution extraction
        if is_frontier(node):
            self.cl_ds.frontier.append(node.name)
        else:
            self.cl_ds.no_frontier.append(node.name)
        gen_simple_evolution(node, self.cl_ds, self.sub_exp, self.reporter)
        return

    def visit_cstart_node(self, node):
        """
        start node: nothing to do. Start nodes are frontier marks
        """
        pass

    def visit_ctrap_node(self, node):
        """
        trap node: compilation is done in transitions
        """
        pass

    def visit_cinput_node(self, node):
        """
        Input nodes generate free variables as free clocks
        We just have to register them for solution extraction
        """
        # register input variable
        self.cl_ds.add_input(node.name)

    def visit_cmacro_node(self, node):
        """
        Macro nodes are treated as simple nodes
        They must be empty!!
        """
        if len(node.sub_nodes) > 0:
            mess = "gt2Clause ==> ", "Macronodes not yet implemented!"
            self.reporter.display(mess)
        self.visit_csimple_node(node)

    def visit_cperm_node(self, node):
        """
        perm nodes are always activated - they do not appear in code
        """
        pass

    def visit_ctop_node(self, node):
        """
        visit all sub nodes
        """
        # sub states
        for sst in node.sub_nodes:
            sst.accept(self)

# helper functions

def check_clock(vva):
    """
    simple check
    """
    return vva[0] == 'clock'

def gen_transition_clock(trans, cl_ds, sub_exp, reporter):
    """
    @param trans: a transition
    @param cl_ds: logical (clauses) dynamic system to generate
    @param sub_exp: expression
    @param reporter: reporter for error reporting

    @return:  a literal representing the transition clock
    @warning: The clause constraint dynamic system cl_ds is modified
    """
    # condition compiling in SigExpr
    node_exp = SigIdentExpr(trans.ori.name)
    if trans.condition:
        cond_sexp = compile_cond(trans.condition, cl_ds.symb_tab, reporter)
        if trans.ori.is_perm():
            log_sexp = cond_sexp
        else:
            log_sexp = SigSyncBinExpr('and', node_exp, cond_sexp)
    else : # no condition on incoming transition
#        if trans.ori.is_perm():
#            log_sexp = None # stand for True!!
#        else:
        log_sexp = node_exp
    # condition compiling to clauses
    #temp_cond = cl_ds.add_aux_var()
    if log_sexp:
        sexpv = MCLSigExprVisitor(cl_ds, None, sub_exp)
        v_cond = log_sexp.accept(sexpv)
        notv_cond = v_cond.lit_not()

    # event compiling
    if trans.event:
        ev_sexpr, sex, free_clocks = compile_event(trans.event,
                                                   cl_ds.symb_tab,
                                                   True, reporter)
        for hne in free_clocks:
            cl_ds.add_free_clock(hne)
        if ev_sexpr.is_ident():
            h_event = Literal(trans.event, True)
        else:
            sexpv = MCLSigExprVisitor(cl_ds, None, sub_exp)
            h_event = ev_sexpr.accept(sexpv)

        if not log_sexp: # trans_h = ev because cond = True
            return h_event
        # register (trans.ori, h_event) since trans.ori is an
        # induction place of h_event
        if not trans.ori.is_perm():
            cl_ds.add_place_clock(trans.ori.name, h_event.name)
        nh_event = h_event.lit_not()
        nnn = cl_ds.add_aux_var() # name of the transition clock
        h_tr = Literal(nnn, True)
        noth_tr = Literal(nnn, False)
        cl1 = Clause([noth_tr, h_event])           # not tr_h or  ev
        cl_ds.add_clause(cl1)
        cl2 = Clause([noth_tr, v_cond])            #  not tr_h or  cond
        cl_ds.add_clause(cl2)
        # tr_h or (not cond) or (not ev)
        cl3 = Clause([nh_event, notv_cond, h_tr])
        cl_ds.add_clause(cl3)
        return h_tr

    else:
        return v_cond

def gen_transition_list_clock(ltr, cl_ds, sub_exp, reporter):
    """
    @param ltr: a list of transitions - must be non_empty
    @param cl_ds: logical (clauses) dynamic system to generate
    @param sub_exp: expression
    @param reporter: reporter for error reporting
    @return  a literal representing the default of the transition clocks or None if empty list
    The clause constraint dynamic system cl_ds is modified
    """
    if ltr == []:
         return None
    ltr_h = []
    for trans in ltr:
        if trans.ori.is_start():
            continue # trans is a pseudo transition
        if not trans.clock: # avoid multiple transition compilation
            tr_h = gen_transition_clock(trans, cl_ds, sub_exp, reporter)
            trans.clock = tr_h
        else:
            tr_h = trans.clock
        ltr_h.append(tr_h)
    if len(ltr_h) == 1:
        return ltr_h[0]
    h_name = cl_ds.add_aux_var() # name of the default clock
    h_def = Literal(h_name, True)
    nh_def = Literal(h_name, False)
    # add all the clauses h_def or not h_i
    for fcl in ltr_h:
        cl0 = Clause([h_def, fcl.lit_not()])
        cl_ds.add_clause(cl0)
    # add the clause (not h_def) or h1 or ...or hp
    ltr_h.append(nh_def)
    cl0 = Clause(ltr_h)
    cl_ds.add_clause(cl0)

    return h_def

def gen_simple_evolution(splace, cl_ds, sub_exp, reporter):
    """
    generate evolution equation of a place as clauses constraints
    @param splace: a simple place
    @param cl_ds: logical (clauses) dynamic system to generate
    @param sub_exp: expression
    @param reporter: reporter for error reporting
    @return  nothing
    The clause constraint dynamic system cl_ds is modified
    """
    pname = splace.name
    p_lit = Literal(pname, True)
    np_lit = Literal(pname, False)
    pnext = pname+"`"
    pnext_lit = Literal(pnext, True)
    npnext_lit = Literal(pnext, False)
    h_in = gen_transition_list_clock(splace.incoming_trans,
                                      cl_ds, sub_exp, reporter)
    h_out = gen_transition_list_clock(splace.outgoing_trans,
                                      cl_ds, sub_exp, reporter)
    # clauses for evolution equation
    if h_in and h_out:
        # not X' or h_in or X
        cla = Clause([npnext_lit, h_in, p_lit])
        cl_ds.add_clause(cla)
        # not X' or h_in or not h_out
        cla = Clause([npnext_lit, h_in, h_out.lit_not()])
        cl_ds.add_clause(cla)
        # X' or not h_in
        cla = Clause([pnext_lit, h_in.lit_not()])
        cl_ds.add_clause(cla)
        # X' or not X or h_out
        cla = Clause([pnext_lit, np_lit, h_out])
        cl_ds.add_clause(cla)

    elif h_in:
        # not X' or h_in or X
        cla = Clause([npnext_lit, h_in, p_lit])
        cl_ds.add_clause(cla)
        # X' or not h_in
        cla = Clause([pnext_lit, h_in.lit_not()])
        cl_ds.add_clause(cla)
        # X' or not X
        cla = Clause([pnext_lit, np_lit])
        cl_ds.add_clause(cla)

    elif h_out:
        # not X' or X
        cla = Clause([npnext_lit, p_lit])
        cl_ds.add_clause(cla)
        # not X' or not h_out
        cla = Clause([npnext_lit, h_out.lit_not()])
        cl_ds.add_clause(cla)
        # X' or not X or h_out
        cla = Clause([pnext_lit, np_lit, h_out])
        cl_ds.add_clause(cla)

    else:
        # not X' or X
        cla = Clause([npnext_lit, p_lit])
        cl_ds.add_clause(cla)
        # X' or not X
        cla = Clause([pnext_lit, np_lit])
        cl_ds.add_clause(cla)

def gen_aux_clock_constraints(cl_ds):
    """
    generate structural clock constraints:
    not h or A1 or A2 ... or Ap
    for all couples (A,h) where A is an induction place of h
    """
    # first constraint: a clock depends on its inductive places
    for hname in cl_ds.place_clocks.keys():
        hlit = Literal(hname, False)
        llit = [hlit]
        for pname in cl_ds.place_clocks[hname]:
            plit = Literal(pname, True)
            llit.append(plit)
        cl_ds.add_aux_clause(Clause(llit))

def gen_clock_constraints(constraints_txt, cl_ds, sub_exp, reporter):
    """
    cleaning clock constraints
    """
    text_const = ""
    for cha in constraints_txt:
        if  cha != ';' and cha != '\n':
            text_const += cha
        else:
            if cha == ';':
                gen_code_clock_const(text_const, cl_ds, sub_exp, reporter)
            text_const = ""


def gen_code_clock_const(const_txt, cl_ds, sub_exp, reporter):
    """
    code generator for clock constraints
    """
    ctexpr = compile_constraint(const_txt, cl_ds.symb_tab, reporter)
    ctexpv = MCLSigExprVisitor(cl_ds, None, sub_exp)
    ctexpr.accept(ctexpv)


def is_frontier(node):
    """
    Find if a node is a frontier node
    """
    itrans = node.incoming_trans
    if itrans == []:
        return True
    else:
        for trans in itrans:
            if trans.ori.is_start():
                return True
    return False


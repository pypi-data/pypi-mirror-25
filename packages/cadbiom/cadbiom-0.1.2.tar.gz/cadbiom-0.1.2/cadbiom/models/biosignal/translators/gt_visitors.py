## Filename    : gt_visitors
## Author(s)   : Michel Le Borgne
## Created     : 01/2012
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
Utilities for compiling conditions, event and constraints
"""
#import sys
from cadbiom.antlr3 import ANTLRStringStream, CommonTokenStream, RecognitionException

from cadbiom.models.biosignal.translators.sigexpr_lexer import sigexpr_lexer
from cadbiom.models.biosignal.translators.sigexpr_compiler import sigexpr_compiler


# GT2MCSysVisitor compile a MC model from a guarded transition model
# mangling constants
ENVAC = "_envac"
ENVINAC = "_envinac"
ACT = "_activ"
INACT = "_inac"
UPDAT = "_update"



def compile_cond(text, symb_table, error_reporter, deep = -1, message = ""):
    """
    Compile a condition expression to a tree representation
    @param text: string to be compiled
    @param symb_table: symbol table of the compiler
    @param error_reporter: use a CompilReporter for full information!!
    @param deep: optional - if >0 the compiler doesn't accept states
                declared inside macro
    """
    text_c = text+" $"
    reader = ANTLRStringStream(text_c)
    lexer = sigexpr_lexer(reader)
    parser = sigexpr_compiler(CommonTokenStream(lexer))
    parser.deep = deep
    parser.message = message
    if error_reporter:
        # default options (state_only = False)
        parser.set_error_reporter(error_reporter)
    # ident checking option: only state and input names are allowed
    parser.state_only = True
    try:
        tree = parser.sig_bool(symb_table)
    except RecognitionException , exc:
        if error_reporter:
            error_reporter.display( 'Error in condition: %s'%exc)
            parser.displayExceptionMessage(exc)
            return None
        else:
            raise exc
    return tree.exp

def compile_constraint(const_txt, symb_table, error_reporter):
    """
    Compile a constraint expression to a tree representation
    @param const_txt: string to be compiled
    @param symb_table: symbol table of the compiler
    @param error_reporter: output error messages
    @return: a tree representing the expression
    """
    text_c = const_txt+" $"
    reader = ANTLRStringStream(text_c)
    lexer = sigexpr_lexer(reader)
    parser = sigexpr_compiler(CommonTokenStream(lexer))
    parser.set_error_reporter(error_reporter)
    try:
        tree = parser.sig_expression(symb_table)
    except RecognitionException , exc:
        error_reporter.display('Error in constraints: %s'%exc)
        parser.displayExceptionMessage(exc)
        return None
    return tree.exp

def compile_event(text, symb_table, free_clocks, error_reporter):
    """
    Compile an event expression to a tree representation
    @param text: string to be compiled
    @param symb_table: symbol table of the compiler
    @param free_clocks: boolean if true free clocks are collected
    @param error_reporter: output error messages
    @return: a triple exp, se, fc where exp is the event expression,
            se the state events (s#> ..) used and
            fc is the free clocks used in the event expression.
    """
    text_c = text+' $'
    reader = ANTLRStringStream(text_c)
    lexer = sigexpr_lexer(reader)
    # default options on compiler (state_only = False)
    parser = sigexpr_compiler(CommonTokenStream(lexer))
    parser.set_error_reporter(error_reporter)
    parser.catch_free_clocks = free_clocks
    # ident checking option: only state and input names are allowed in bool op
    parser.state_only_in_bool = True
    try:
        tree = parser.sig_expression(symb_table)
    except RecognitionException , exc:
        error_reporter.display('Error in event: %s'%exc)
        parser.displayExceptionMessage(exc)
        return None
    return tree.exp, parser.state_events, parser.free_clocks


# $ANTLR 3.1.2 /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g 2012-10-23 16:08:43

import sys
from cadbiom.antlr3 import *
from cadbiom.antlr3.compat import set, frozenset

from cadbiom.antlr3.tree import *


from cadbiom.models.biosignal.sig_expr import *
import string



# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
F=17
DEF=19
SYNC=9
LETTER=32
DEFAULT=6
T=16
CHG=26
NOT=15
MINUS=29
EVENT=8
AND=13
EOF=-1
MUL=30
CONSTR=18
INC=11
SCOL=27
WS=4
EXC=10
EXP=31
SEQ=12
NOTEG=21
WHEN=7
COM=25
OR=14
DOL=24
IDENT=34
PLUS=28
DIGIT=33
COMMENT=5
PD=23
EG=20
PG=22

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>",
    "WS", "COMMENT", "DEFAULT", "WHEN", "EVENT", "SYNC", "EXC", "INC", "SEQ",
    "AND", "OR", "NOT", "T", "F", "CONSTR", "DEF", "EG", "NOTEG", "PG",
    "PD", "DOL", "COM", "CHG", "SCOL", "PLUS", "MINUS", "MUL", "EXP", "LETTER",
    "DIGIT", "IDENT"
]




class sigexpr_compiler(Parser):
    grammarFileName = "/home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g"
    antlr_version = version_str_to_tuple("3.1.2")
    antlr_version_str = "3.1.2"
    tokenNames = tokenNames

    def __init__(self, input, state=None):
        if state is None:
            state = RecognizerSharedState()

        Parser.__init__(self, input, state)


        self.dfa1 = self.DFA1(
            self, 1,
            eot = self.DFA1_eot,
            eof = self.DFA1_eof,
            min = self.DFA1_min,
            max = self.DFA1_max,
            accept = self.DFA1_accept,
            special = self.DFA1_special,
            transition = self.DFA1_transition
            )

        self.dfa3 = self.DFA3(
            self, 3,
            eot = self.DFA3_eot,
            eof = self.DFA3_eof,
            min = self.DFA3_min,
            max = self.DFA3_max,
            accept = self.DFA3_accept,
            special = self.DFA3_special,
            transition = self.DFA3_transition
            )

        self.dfa7 = self.DFA7(
            self, 7,
            eot = self.DFA7_eot,
            eof = self.DFA7_eof,
            min = self.DFA7_min,
            max = self.DFA7_max,
            accept = self.DFA7_accept,
            special = self.DFA7_special,
            transition = self.DFA7_transition
            )




        self.state_events = []
        self.free_clocks = []
        self.state_only = False
        self.state_only_in_bool = False
        self.catch_free_clocks = False
        self.deep = -1
        self.message = ""
        self.error_reporter = None





        self._adaptor = CommonTreeAdaptor()



    def getTreeAdaptor(self):
        return self._adaptor

    def setTreeAdaptor(self, adaptor):
        self._adaptor = adaptor

    adaptor = property(getTreeAdaptor, setTreeAdaptor)


    def set_error_reporter(self, err):
        self.error_reporter = err

    def displayRecognitionError(self, tokenNames, re):
           hdr = self.getErrorHeader(re)
           msg = self.getErrorMessage(re, tokenNames)
           self.error_reporter.display('sig_exp ->'+hdr+msg+self.message)


    def displayExceptionMessage(self, e):
      msg = self.getErrorMessage(self, e, tokenNames)
      self.error_reporter.display('sig_exp ->'+msg)

    # semantic checks for compilers
    def check_ident(self, symbol_table, st_only, free_clock, deep, message, name):
        """
        Check if  name  is declared  (with state/input type if st_only = True)
        @return: a SigIdentExpr
        """
        try:
          name = name.encode("utf-8")
          type, s_deep = symbol_table[name]
          # for condition compiler
          if st_only:
            if (not (type == "state" or type=="input")):
              self.error_reporter.display("type error -> " + name + " is not a state (" +type+")"+ message)
          else:
            if deep >= 0:
              if s_deep >= deep:
                 self.error_reporter.display("type error -> " + name + " not declared in a surrounding macro state"+ message)
        except KeyError:
          if free_clock and not st_only:
            self.free_clocks.append(name)
          else:
            self.error_reporter.display("dec -> Undeclared event or state:" + name + message)
        return SigIdentExpr(name)

    def check_updown(self, symbol_table, id, mode):
        """
        This function introduce new signals: state> or state<
        """
        id  = id.encode("utf-8")
        try:
            att = symbol_table[id]
            type = att[0]
            s_deep = att[1]
        except KeyError:
            self.error_reporter.display('dec -> Undeclared state in variation:' + id)
            type = "error"
        if type == "state":
            if mode == 1: #up
                name = id+">"
            else: #down
                name = id+"<"
            self.state_events.append(name)
            return SigIdentExpr(name)
        else:
            self.error_reporter.display('type error -> Up and Down can only be derived from a state: '+id)

    def  check_change(self, symbol_table, id):
        id  = id.encode("utf-8")
        try:
            att = symbol_table[id]
            type = att[0]
            s_deep = att[1]
        except KeyError:
            self.error_reporter.display('dec -> Undeclared signal in variation:' + id)
            type = "error"
        if type == "state":
            refresh_expr = SigIdentExpr(id)
            st_expr = SigIdentExpr(id)
            return SigWhenExpr(SigConstExpr(True),SigDiffExpr(st_expr, refresh_expr))
        else:
            self.error_reporter.display('type error -> Change can only be derived  from a state: '+id)

    def check_sync(self, lexp):
        # type checking is done in expressions
        return SigConstraintExpr(SigConstraintExpr.SYNCHRO, lexp)

    def check_exclus(self, lexp):
        return SigConstraintExpr(SigConstraintExpr.EXCLU, lexp)


    def check_included(self, exp1,exp2):
        return SigConstraintExpr(SigConstraintExpr.INCL, [exp1,exp2])



    class sig_expression_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.exp = None
            self.tree = None




    # $ANTLR start "sig_expression"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:163:1: sig_expression[tab_symb] returns [exp] : (exp1= sig_expression1[tab_symb] DOL | exp2= sig_constraint[tab_symb] DOL );
    def sig_expression(self, tab_symb):

        retval = self.sig_expression_return()
        retval.start = self.input.LT(1)

        root_0 = None

        DOL1 = None
        DOL2 = None
        exp1 = None

        exp2 = None


        DOL1_tree = None
        DOL2_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:164:9: (exp1= sig_expression1[tab_symb] DOL | exp2= sig_constraint[tab_symb] DOL )
                alt1 = 2
                alt1 = self.dfa1.predict(self.input)
                if alt1 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:164:11: exp1= sig_expression1[tab_symb] DOL
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_sig_expression1_in_sig_expression148)
                    exp1 = self.sig_expression1(tab_symb)

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, exp1.tree)
                    DOL1=self.match(self.input, DOL, self.FOLLOW_DOL_in_sig_expression151)

                    DOL1_tree = self._adaptor.createWithPayload(DOL1)
                    self._adaptor.addChild(root_0, DOL1_tree)

                    #action start
                    retval.exp = ((exp1 is not None) and [exp1.exp] or [None])[0]
                    #action end


                elif alt1 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:166:11: exp2= sig_constraint[tab_symb] DOL
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_sig_constraint_in_sig_expression181)
                    exp2 = self.sig_constraint(tab_symb)

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, exp2.tree)
                    DOL2=self.match(self.input, DOL, self.FOLLOW_DOL_in_sig_expression184)

                    DOL2_tree = self._adaptor.createWithPayload(DOL2)
                    self._adaptor.addChild(root_0, DOL2_tree)

                    #action start
                    retval.exp = ((exp2 is not None) and [exp2.exp] or [None])[0]
                    #action end


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass

        return retval

    # $ANTLR end "sig_expression"

    class sig_expression1_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.exp = None
            self.tree = None




    # $ANTLR start "sig_expression1"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:170:1: sig_expression1[tab_symb] returns [exp] : (exp1= sig_exp[tab_symb] ( DEFAULT exp2= sig_exp[tab_symb] )* | );
    def sig_expression1(self, tab_symb):

        retval = self.sig_expression1_return()
        retval.start = self.input.LT(1)

        root_0 = None

        DEFAULT3 = None
        exp1 = None

        exp2 = None


        DEFAULT3_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:171:9: (exp1= sig_exp[tab_symb] ( DEFAULT exp2= sig_exp[tab_symb] )* | )
                alt3 = 2
                alt3 = self.dfa3.predict(self.input)
                if alt3 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:171:11: exp1= sig_exp[tab_symb] ( DEFAULT exp2= sig_exp[tab_symb] )*
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_sig_exp_in_sig_expression1230)
                    exp1 = self.sig_exp(tab_symb)

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, exp1.tree)
                    #action start
                    retval.exp = ((exp1 is not None) and [exp1.exp] or [None])[0]
                    #action end
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:172:11: ( DEFAULT exp2= sig_exp[tab_symb] )*
                    while True: #loop2
                        alt2 = 2
                        LA2_0 = self.input.LA(1)

                        if (LA2_0 == DEFAULT) :
                            alt2 = 1


                        if alt2 == 1:
                            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:172:12: DEFAULT exp2= sig_exp[tab_symb]
                            pass
                            DEFAULT3=self.match(self.input, DEFAULT, self.FOLLOW_DEFAULT_in_sig_expression1247)

                            DEFAULT3_tree = self._adaptor.createWithPayload(DEFAULT3)
                            root_0 = self._adaptor.becomeRoot(DEFAULT3_tree, root_0)

                            self._state.following.append(self.FOLLOW_sig_exp_in_sig_expression1252)
                            exp2 = self.sig_exp(tab_symb)

                            self._state.following.pop()
                            self._adaptor.addChild(root_0, exp2.tree)
                            #action start
                            retval.exp = SigDefaultExpr(retval.exp, ((exp2 is not None) and [exp2.exp] or [None])[0])
                            #action end


                        else:
                            break #loop2




                elif alt3 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:176:11:
                    pass
                    root_0 = self._adaptor.nil()

                    #action start
                    retval.exp = SigConstExpr(True)
                    #action end


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass

        return retval

    # $ANTLR end "sig_expression1"

    class sig_exp_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.exp = None
            self.tree = None




    # $ANTLR start "sig_exp"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:179:1: sig_exp[tab_symb] returns [exp] : exp1= sig_bool[tab_symb] ( WHEN exp2= sig_bool[tab_symb] )* ;
    def sig_exp(self, tab_symb):

        retval = self.sig_exp_return()
        retval.start = self.input.LT(1)

        root_0 = None

        WHEN4 = None
        exp1 = None

        exp2 = None


        WHEN4_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:180:9: (exp1= sig_bool[tab_symb] ( WHEN exp2= sig_bool[tab_symb] )* )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:180:12: exp1= sig_bool[tab_symb] ( WHEN exp2= sig_bool[tab_symb] )*
                pass
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_sig_bool_in_sig_exp338)
                exp1 = self.sig_bool(tab_symb)

                self._state.following.pop()
                self._adaptor.addChild(root_0, exp1.tree)
                #action start
                retval.exp = ((exp1 is not None) and [exp1.exp] or [None])[0]
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:181:11: ( WHEN exp2= sig_bool[tab_symb] )*
                while True: #loop4
                    alt4 = 2
                    LA4_0 = self.input.LA(1)

                    if (LA4_0 == WHEN) :
                        alt4 = 1


                    if alt4 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:181:12: WHEN exp2= sig_bool[tab_symb]
                        pass
                        WHEN4=self.match(self.input, WHEN, self.FOLLOW_WHEN_in_sig_exp355)

                        WHEN4_tree = self._adaptor.createWithPayload(WHEN4)
                        root_0 = self._adaptor.becomeRoot(WHEN4_tree, root_0)

                        #action start
                        st_only_save = self.state_only; self.state_only = self.state_only_in_bool
                        #action end
                        self._state.following.append(self.FOLLOW_sig_bool_in_sig_exp389)
                        exp2 = self.sig_bool(tab_symb)

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, exp2.tree)
                        #action start
                        retval.exp = SigWhenExpr(retval.exp, ((exp2 is not None) and [exp2.exp] or [None])[0])
                        self.state_only = st_only_save
                        #action end


                    else:
                        break #loop4





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass

        return retval

    # $ANTLR end "sig_exp"

    class sig_bool_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.exp = None
            self.tree = None




    # $ANTLR start "sig_bool"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:190:1: sig_bool[tab_symb] returns [exp] : exp1= sig_bool_and[tab_symb] ( OR exp2= sig_bool_and[tab_symb] )* ;
    def sig_bool(self, tab_symb):

        retval = self.sig_bool_return()
        retval.start = self.input.LT(1)

        root_0 = None

        OR5 = None
        exp1 = None

        exp2 = None


        OR5_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:191:9: (exp1= sig_bool_and[tab_symb] ( OR exp2= sig_bool_and[tab_symb] )* )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:191:11: exp1= sig_bool_and[tab_symb] ( OR exp2= sig_bool_and[tab_symb] )*
                pass
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_sig_bool_and_in_sig_bool471)
                exp1 = self.sig_bool_and(tab_symb)

                self._state.following.pop()
                self._adaptor.addChild(root_0, exp1.tree)
                #action start
                retval.exp = ((exp1 is not None) and [exp1.exp] or [None])[0]
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:192:11: ( OR exp2= sig_bool_and[tab_symb] )*
                while True: #loop5
                    alt5 = 2
                    LA5_0 = self.input.LA(1)

                    if (LA5_0 == OR) :
                        alt5 = 1


                    if alt5 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:192:12: OR exp2= sig_bool_and[tab_symb]
                        pass
                        OR5=self.match(self.input, OR, self.FOLLOW_OR_in_sig_bool487)

                        OR5_tree = self._adaptor.createWithPayload(OR5)
                        root_0 = self._adaptor.becomeRoot(OR5_tree, root_0)

                        self._state.following.append(self.FOLLOW_sig_bool_and_in_sig_bool492)
                        exp2 = self.sig_bool_and(tab_symb)

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, exp2.tree)
                        #action start
                        retval.exp = SigSyncBinExpr("or", retval.exp, ((exp2 is not None) and [exp2.exp] or [None])[0])
                        #action end


                    else:
                        break #loop5





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass

        return retval

    # $ANTLR end "sig_bool"

    class sig_bool_and_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.exp = None
            self.tree = None




    # $ANTLR start "sig_bool_and"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:197:1: sig_bool_and[tab_symb] returns [exp] : exp1= sig_primary[tab_symb] ( AND exp2= sig_primary[tab_symb] )* ;
    def sig_bool_and(self, tab_symb):

        retval = self.sig_bool_and_return()
        retval.start = self.input.LT(1)

        root_0 = None

        AND6 = None
        exp1 = None

        exp2 = None


        AND6_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:198:9: (exp1= sig_primary[tab_symb] ( AND exp2= sig_primary[tab_symb] )* )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:198:11: exp1= sig_primary[tab_symb] ( AND exp2= sig_primary[tab_symb] )*
                pass
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_sig_primary_in_sig_bool_and561)
                exp1 = self.sig_primary(tab_symb)

                self._state.following.pop()
                self._adaptor.addChild(root_0, exp1.tree)
                #action start
                retval.exp = ((exp1 is not None) and [exp1.exp] or [None])[0]
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:199:11: ( AND exp2= sig_primary[tab_symb] )*
                while True: #loop6
                    alt6 = 2
                    LA6_0 = self.input.LA(1)

                    if (LA6_0 == AND) :
                        alt6 = 1


                    if alt6 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:199:12: AND exp2= sig_primary[tab_symb]
                        pass
                        AND6=self.match(self.input, AND, self.FOLLOW_AND_in_sig_bool_and577)

                        AND6_tree = self._adaptor.createWithPayload(AND6)
                        root_0 = self._adaptor.becomeRoot(AND6_tree, root_0)

                        self._state.following.append(self.FOLLOW_sig_primary_in_sig_bool_and582)
                        exp2 = self.sig_primary(tab_symb)

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, exp2.tree)
                        #action start
                        retval.exp = SigSyncBinExpr("and",retval.exp, ((exp2 is not None) and [exp2.exp] or [None])[0])
                        #action end


                    else:
                        break #loop6





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass

        return retval

    # $ANTLR end "sig_bool_and"

    class sig_primary_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.exp = None
            self.tree = None




    # $ANTLR start "sig_primary"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:204:1: sig_primary[tab_symb] returns [exp] : ( NOT nexp= sig_primary[tab_symb] | cexp= sig_constant | EVENT PG exps= sig_expression1[tab_symb] PD | WHEN PG expw= sig_expression1[tab_symb] PD | i7= IDENT UP | i8= IDENT DOWN | id2= IDENT | PG expse= sig_expression1[tab_symb] PD );
    def sig_primary(self, tab_symb):

        retval = self.sig_primary_return()
        retval.start = self.input.LT(1)

        root_0 = None

        i7 = None
        i8 = None
        id2 = None
        NOT7 = None
        EVENT8 = None
        PG9 = None
        PD10 = None
        WHEN11 = None
        PG12 = None
        PD13 = None
        UP14 = None
        DOWN15 = None
        PG16 = None
        PD17 = None
        nexp = None

        cexp = None

        exps = None

        expw = None

        expse = None


        i7_tree = None
        i8_tree = None
        id2_tree = None
        NOT7_tree = None
        EVENT8_tree = None
        PG9_tree = None
        PD10_tree = None
        WHEN11_tree = None
        PG12_tree = None
        PD13_tree = None
        UP14_tree = None
        DOWN15_tree = None
        PG16_tree = None
        PD17_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:205:9: ( NOT nexp= sig_primary[tab_symb] | cexp= sig_constant | EVENT PG exps= sig_expression1[tab_symb] PD | WHEN PG expw= sig_expression1[tab_symb] PD | i7= IDENT UP | i8= IDENT DOWN | id2= IDENT | PG expse= sig_expression1[tab_symb] PD )
                alt7 = 8
                alt7 = self.dfa7.predict(self.input)
                if alt7 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:205:11: NOT nexp= sig_primary[tab_symb]
                    pass
                    root_0 = self._adaptor.nil()

                    NOT7=self.match(self.input, NOT, self.FOLLOW_NOT_in_sig_primary656)

                    NOT7_tree = self._adaptor.createWithPayload(NOT7)
                    root_0 = self._adaptor.becomeRoot(NOT7_tree, root_0)

                    self._state.following.append(self.FOLLOW_sig_primary_in_sig_primary661)
                    nexp = self.sig_primary(tab_symb)

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, nexp.tree)
                    #action start
                    retval.exp = SigNotExpr(((nexp is not None) and [nexp.exp] or [None])[0])
                    #action end


                elif alt7 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:208:11: cexp= sig_constant
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_sig_constant_in_sig_primary704)
                    cexp = self.sig_constant()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, cexp.tree)
                    #action start
                    retval.exp = ((cexp is not None) and [cexp.exp] or [None])[0]
                    #action end


                elif alt7 == 3:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:211:11: EVENT PG exps= sig_expression1[tab_symb] PD
                    pass
                    root_0 = self._adaptor.nil()

                    EVENT8=self.match(self.input, EVENT, self.FOLLOW_EVENT_in_sig_primary751)

                    EVENT8_tree = self._adaptor.createWithPayload(EVENT8)
                    self._adaptor.addChild(root_0, EVENT8_tree)

                    PG9=self.match(self.input, PG, self.FOLLOW_PG_in_sig_primary753)
                    self._state.following.append(self.FOLLOW_sig_expression1_in_sig_primary758)
                    exps = self.sig_expression1(tab_symb)

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, exps.tree)
                    PD10=self.match(self.input, PD, self.FOLLOW_PD_in_sig_primary761)
                    #action start
                    retval.exp = SigEventExpr(((exps is not None) and [exps.exp] or [None])[0])
                    #action end


                elif alt7 == 4:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:214:11: WHEN PG expw= sig_expression1[tab_symb] PD
                    pass
                    root_0 = self._adaptor.nil()

                    WHEN11=self.match(self.input, WHEN, self.FOLLOW_WHEN_in_sig_primary798)

                    WHEN11_tree = self._adaptor.createWithPayload(WHEN11)
                    self._adaptor.addChild(root_0, WHEN11_tree)

                    PG12=self.match(self.input, PG, self.FOLLOW_PG_in_sig_primary800)
                    self._state.following.append(self.FOLLOW_sig_expression1_in_sig_primary805)
                    expw = self.sig_expression1(tab_symb)

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, expw.tree)
                    PD13=self.match(self.input, PD, self.FOLLOW_PD_in_sig_primary808)
                    #action start
                    retval.exp = SigWhenExpr(SigConstExpr(True),((expw is not None) and [expw.exp] or [None])[0])
                    #action end


                elif alt7 == 5:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:217:11: i7= IDENT UP
                    pass
                    root_0 = self._adaptor.nil()

                    i7=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_sig_primary838)

                    i7_tree = self._adaptor.createWithPayload(i7)
                    self._adaptor.addChild(root_0, i7_tree)

                    UP14=self.match(self.input, 3, self.FOLLOW_3_in_sig_primary840)

                    UP14_tree = self._adaptor.createWithPayload(UP14)
                    self._adaptor.addChild(root_0, UP14_tree)

                    #action start
                    retval.exp = self.check_updown(tab_symb, i7.text, 1)
                    #action end


                elif alt7 == 6:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:220:11: i8= IDENT DOWN
                    pass
                    root_0 = self._adaptor.nil()

                    i8=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_sig_primary870)

                    i8_tree = self._adaptor.createWithPayload(i8)
                    self._adaptor.addChild(root_0, i8_tree)

                    DOWN15=self.match(self.input, 2, self.FOLLOW_2_in_sig_primary872)

                    DOWN15_tree = self._adaptor.createWithPayload(DOWN15)
                    self._adaptor.addChild(root_0, DOWN15_tree)

                    #action start
                    retval.exp = self.check_updown(tab_symb, i8.text, 2)
                    #action end


                elif alt7 == 7:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:225:11: id2= IDENT
                    pass
                    root_0 = self._adaptor.nil()

                    id2=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_sig_primary915)

                    id2_tree = self._adaptor.createWithPayload(id2)
                    self._adaptor.addChild(root_0, id2_tree)

                    #action start
                    retval.exp = self.check_ident(tab_symb, self.state_only, self.catch_free_clocks, self.deep, self.message, id2.text)
                    #action end


                elif alt7 == 8:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:228:11: PG expse= sig_expression1[tab_symb] PD
                    pass
                    root_0 = self._adaptor.nil()

                    PG16=self.match(self.input, PG, self.FOLLOW_PG_in_sig_primary956)

                    PG16_tree = self._adaptor.createWithPayload(PG16)
                    self._adaptor.addChild(root_0, PG16_tree)

                    self._state.following.append(self.FOLLOW_sig_expression1_in_sig_primary960)
                    expse = self.sig_expression1(tab_symb)

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, expse.tree)
                    PD17=self.match(self.input, PD, self.FOLLOW_PD_in_sig_primary963)

                    PD17_tree = self._adaptor.createWithPayload(PD17)
                    self._adaptor.addChild(root_0, PD17_tree)

                    #action start
                    retval.exp = ((expse is not None) and [expse.exp] or [None])[0]
                    #action end


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass

        return retval

    # $ANTLR end "sig_primary"

    class sig_constant_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.exp = None
            self.tree = None




    # $ANTLR start "sig_constant"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:232:1: sig_constant returns [exp] : ( T | F );
    def sig_constant(self, ):

        retval = self.sig_constant_return()
        retval.start = self.input.LT(1)

        root_0 = None

        T18 = None
        F19 = None

        T18_tree = None
        F19_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:233:10: ( T | F )
                alt8 = 2
                LA8_0 = self.input.LA(1)

                if (LA8_0 == T) :
                    alt8 = 1
                elif (LA8_0 == F) :
                    alt8 = 2
                else:
                    nvae = NoViableAltException("", 8, 0, self.input)

                    raise nvae

                if alt8 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:233:12: T
                    pass
                    root_0 = self._adaptor.nil()

                    T18=self.match(self.input, T, self.FOLLOW_T_in_sig_constant1008)

                    T18_tree = self._adaptor.createWithPayload(T18)
                    self._adaptor.addChild(root_0, T18_tree)

                    #action start
                    retval.exp = SigConstExpr(True)
                    #action end


                elif alt8 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:234:12: F
                    pass
                    root_0 = self._adaptor.nil()

                    F19=self.match(self.input, F, self.FOLLOW_F_in_sig_constant1023)

                    F19_tree = self._adaptor.createWithPayload(F19)
                    self._adaptor.addChild(root_0, F19_tree)

                    #action start
                    retval.exp = SigConstExpr(False)
                    #action end


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass

        return retval

    # $ANTLR end "sig_constant"

    class sig_constraint_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.exp = None
            self.tree = None




    # $ANTLR start "sig_constraint"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:237:1: sig_constraint[tab_symb] returns [exp] : ( SYNC PG el= exp_list[tab_symb] PD | EXC PG el= exp_list[tab_symb] PD | INC PG e3= sig_expression1[tab_symb] COM e4= sig_exp[tab_symb] PD );
    def sig_constraint(self, tab_symb):

        retval = self.sig_constraint_return()
        retval.start = self.input.LT(1)

        root_0 = None

        SYNC20 = None
        PG21 = None
        PD22 = None
        EXC23 = None
        PG24 = None
        PD25 = None
        INC26 = None
        PG27 = None
        COM28 = None
        PD29 = None
        el = None

        e3 = None

        e4 = None


        SYNC20_tree = None
        PG21_tree = None
        PD22_tree = None
        EXC23_tree = None
        PG24_tree = None
        PD25_tree = None
        INC26_tree = None
        PG27_tree = None
        COM28_tree = None
        PD29_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:238:10: ( SYNC PG el= exp_list[tab_symb] PD | EXC PG el= exp_list[tab_symb] PD | INC PG e3= sig_expression1[tab_symb] COM e4= sig_exp[tab_symb] PD )
                alt9 = 3
                LA9 = self.input.LA(1)
                if LA9 == SYNC:
                    alt9 = 1
                elif LA9 == EXC:
                    alt9 = 2
                elif LA9 == INC:
                    alt9 = 3
                else:
                    nvae = NoViableAltException("", 9, 0, self.input)

                    raise nvae

                if alt9 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:238:12: SYNC PG el= exp_list[tab_symb] PD
                    pass
                    root_0 = self._adaptor.nil()

                    SYNC20=self.match(self.input, SYNC, self.FOLLOW_SYNC_in_sig_constraint1075)

                    SYNC20_tree = self._adaptor.createWithPayload(SYNC20)
                    root_0 = self._adaptor.becomeRoot(SYNC20_tree, root_0)

                    PG21=self.match(self.input, PG, self.FOLLOW_PG_in_sig_constraint1078)
                    self._state.following.append(self.FOLLOW_exp_list_in_sig_constraint1083)
                    el = self.exp_list(tab_symb)

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, el.tree)
                    PD22=self.match(self.input, PD, self.FOLLOW_PD_in_sig_constraint1087)
                    #action start
                    retval.exp = self.check_sync(((el is not None) and [el.expl] or [None])[0])
                    #action end


                elif alt9 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:241:12: EXC PG el= exp_list[tab_symb] PD
                    pass
                    root_0 = self._adaptor.nil()

                    EXC23=self.match(self.input, EXC, self.FOLLOW_EXC_in_sig_constraint1138)

                    EXC23_tree = self._adaptor.createWithPayload(EXC23)
                    root_0 = self._adaptor.becomeRoot(EXC23_tree, root_0)

                    PG24=self.match(self.input, PG, self.FOLLOW_PG_in_sig_constraint1142)
                    self._state.following.append(self.FOLLOW_exp_list_in_sig_constraint1149)
                    el = self.exp_list(tab_symb)

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, el.tree)
                    PD25=self.match(self.input, PD, self.FOLLOW_PD_in_sig_constraint1152)
                    #action start
                    retval.exp = self.check_exclus(((el is not None) and [el.expl] or [None])[0])
                    #action end


                elif alt9 == 3:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:244:12: INC PG e3= sig_expression1[tab_symb] COM e4= sig_exp[tab_symb] PD
                    pass
                    root_0 = self._adaptor.nil()

                    INC26=self.match(self.input, INC, self.FOLLOW_INC_in_sig_constraint1181)

                    INC26_tree = self._adaptor.createWithPayload(INC26)
                    root_0 = self._adaptor.becomeRoot(INC26_tree, root_0)

                    PG27=self.match(self.input, PG, self.FOLLOW_PG_in_sig_constraint1184)
                    self._state.following.append(self.FOLLOW_sig_expression1_in_sig_constraint1189)
                    e3 = self.sig_expression1(tab_symb)

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, e3.tree)
                    COM28=self.match(self.input, COM, self.FOLLOW_COM_in_sig_constraint1192)
                    self._state.following.append(self.FOLLOW_sig_exp_in_sig_constraint1197)
                    e4 = self.sig_exp(tab_symb)

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, e4.tree)
                    PD29=self.match(self.input, PD, self.FOLLOW_PD_in_sig_constraint1200)
                    #action start
                    retval.exp = self.check_included(((e3 is not None) and [e3.exp] or [None])[0], ((e4 is not None) and [e4.exp] or [None])[0])
                    #action end


                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass

        return retval

    # $ANTLR end "sig_constraint"

    class exp_list_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.expl = None
            self.tree = None




    # $ANTLR start "exp_list"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:248:1: exp_list[tab_symb] returns [expl] : exp1= sig_expression1[tab_symb] ( COM exp2= sig_expression1[tab_symb] )* ;
    def exp_list(self, tab_symb):

        retval = self.exp_list_return()
        retval.start = self.input.LT(1)

        root_0 = None

        COM30 = None
        exp1 = None

        exp2 = None


        COM30_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:249:10: (exp1= sig_expression1[tab_symb] ( COM exp2= sig_expression1[tab_symb] )* )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:249:12: exp1= sig_expression1[tab_symb] ( COM exp2= sig_expression1[tab_symb] )*
                pass
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_sig_expression1_in_exp_list1257)
                exp1 = self.sig_expression1(tab_symb)

                self._state.following.pop()
                self._adaptor.addChild(root_0, exp1.tree)
                #action start
                retval.expl = [((exp1 is not None) and [exp1.exp] or [None])[0]]
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:250:13: ( COM exp2= sig_expression1[tab_symb] )*
                while True: #loop10
                    alt10 = 2
                    LA10_0 = self.input.LA(1)

                    if (LA10_0 == COM) :
                        alt10 = 1


                    if alt10 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_compiler.g:250:14: COM exp2= sig_expression1[tab_symb]
                        pass
                        COM30=self.match(self.input, COM, self.FOLLOW_COM_in_exp_list1275)

                        COM30_tree = self._adaptor.createWithPayload(COM30)
                        self._adaptor.addChild(root_0, COM30_tree)

                        self._state.following.append(self.FOLLOW_sig_expression1_in_exp_list1279)
                        exp2 = self.sig_expression1(tab_symb)

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, exp2.tree)
                        #action start
                        retval.expl.append(((exp2 is not None) and [exp2.exp] or [None])[0])
                        #action end


                    else:
                        break #loop10





                retval.stop = self.input.LT(-1)


                retval.tree = self._adaptor.rulePostProcessing(root_0)
                self._adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
                retval.tree = self._adaptor.errorNode(self.input, retval.start, self.input.LT(-1), re)
        finally:

            pass

        return retval

    # $ANTLR end "exp_list"


    # Delegated rules


    # lookup tables for DFA #1

    DFA1_eot = DFA.unpack(
        u"\14\uffff"
        )

    DFA1_eof = DFA.unpack(
        u"\14\uffff"
        )

    DFA1_min = DFA.unpack(
        u"\1\7\13\uffff"
        )

    DFA1_max = DFA.unpack(
        u"\1\42\13\uffff"
        )

    DFA1_accept = DFA.unpack(
        u"\1\uffff\1\1\7\uffff\1\2\2\uffff"
        )

    DFA1_special = DFA.unpack(
        u"\14\uffff"
        )


    DFA1_transition = [
        DFA.unpack(u"\2\1\3\11\3\uffff\3\1\4\uffff\1\1\1\uffff\1\1\11\uffff"
        u"\1\1"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"")
    ]

    # class definition for DFA #1

    DFA1 = DFA
    # lookup tables for DFA #3

    DFA3_eot = DFA.unpack(
        u"\13\uffff"
        )

    DFA3_eof = DFA.unpack(
        u"\13\uffff"
        )

    DFA3_min = DFA.unpack(
        u"\1\7\12\uffff"
        )

    DFA3_max = DFA.unpack(
        u"\1\42\12\uffff"
        )

    DFA3_accept = DFA.unpack(
        u"\1\uffff\1\1\6\uffff\1\2\2\uffff"
        )

    DFA3_special = DFA.unpack(
        u"\13\uffff"
        )


    DFA3_transition = [
        DFA.unpack(u"\2\1\6\uffff\3\1\4\uffff\1\1\3\10\10\uffff\1\1"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"")
    ]

    # class definition for DFA #3

    DFA3 = DFA
    # lookup tables for DFA #7

    DFA7_eot = DFA.unpack(
        u"\21\uffff"
        )

    DFA7_eof = DFA.unpack(
        u"\21\uffff"
        )

    DFA7_min = DFA.unpack(
        u"\1\7\5\uffff\1\2\12\uffff"
        )

    DFA7_max = DFA.unpack(
        u"\1\42\5\uffff\1\31\12\uffff"
        )

    DFA7_accept = DFA.unpack(
        u"\1\uffff\1\1\1\2\1\uffff\1\3\1\4\1\uffff\1\10\1\5\1\6\1\7\6\uffff"
        )

    DFA7_special = DFA.unpack(
        u"\21\uffff"
        )


    DFA7_transition = [
        DFA.unpack(u"\1\5\1\4\6\uffff\1\1\2\2\4\uffff\1\7\13\uffff\1\6"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\11\1\10\2\uffff\2\12\5\uffff\2\12\10\uffff\3\12"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"")
    ]

    # class definition for DFA #7

    DFA7 = DFA


    FOLLOW_sig_expression1_in_sig_expression148 = frozenset([24])
    FOLLOW_DOL_in_sig_expression151 = frozenset([1])
    FOLLOW_sig_constraint_in_sig_expression181 = frozenset([24])
    FOLLOW_DOL_in_sig_expression184 = frozenset([1])
    FOLLOW_sig_exp_in_sig_expression1230 = frozenset([1, 6])
    FOLLOW_DEFAULT_in_sig_expression1247 = frozenset([7, 8, 15, 16, 17, 22, 34])
    FOLLOW_sig_exp_in_sig_expression1252 = frozenset([1, 6])
    FOLLOW_sig_bool_in_sig_exp338 = frozenset([1, 7])
    FOLLOW_WHEN_in_sig_exp355 = frozenset([7, 8, 15, 16, 17, 22, 34])
    FOLLOW_sig_bool_in_sig_exp389 = frozenset([1, 7])
    FOLLOW_sig_bool_and_in_sig_bool471 = frozenset([1, 14])
    FOLLOW_OR_in_sig_bool487 = frozenset([7, 8, 15, 16, 17, 22, 34])
    FOLLOW_sig_bool_and_in_sig_bool492 = frozenset([1, 14])
    FOLLOW_sig_primary_in_sig_bool_and561 = frozenset([1, 13])
    FOLLOW_AND_in_sig_bool_and577 = frozenset([7, 8, 15, 16, 17, 22, 34])
    FOLLOW_sig_primary_in_sig_bool_and582 = frozenset([1, 13])
    FOLLOW_NOT_in_sig_primary656 = frozenset([7, 8, 15, 16, 17, 22, 34])
    FOLLOW_sig_primary_in_sig_primary661 = frozenset([1])
    FOLLOW_sig_constant_in_sig_primary704 = frozenset([1])
    FOLLOW_EVENT_in_sig_primary751 = frozenset([22])
    FOLLOW_PG_in_sig_primary753 = frozenset([7, 8, 15, 16, 17, 22, 23, 34])
    FOLLOW_sig_expression1_in_sig_primary758 = frozenset([23])
    FOLLOW_PD_in_sig_primary761 = frozenset([1])
    FOLLOW_WHEN_in_sig_primary798 = frozenset([22])
    FOLLOW_PG_in_sig_primary800 = frozenset([7, 8, 15, 16, 17, 22, 23, 34])
    FOLLOW_sig_expression1_in_sig_primary805 = frozenset([23])
    FOLLOW_PD_in_sig_primary808 = frozenset([1])
    FOLLOW_IDENT_in_sig_primary838 = frozenset([3])
    FOLLOW_3_in_sig_primary840 = frozenset([1])
    FOLLOW_IDENT_in_sig_primary870 = frozenset([2])
    FOLLOW_2_in_sig_primary872 = frozenset([1])
    FOLLOW_IDENT_in_sig_primary915 = frozenset([1])
    FOLLOW_PG_in_sig_primary956 = frozenset([7, 8, 15, 16, 17, 22, 23, 34])
    FOLLOW_sig_expression1_in_sig_primary960 = frozenset([23])
    FOLLOW_PD_in_sig_primary963 = frozenset([1])
    FOLLOW_T_in_sig_constant1008 = frozenset([1])
    FOLLOW_F_in_sig_constant1023 = frozenset([1])
    FOLLOW_SYNC_in_sig_constraint1075 = frozenset([22])
    FOLLOW_PG_in_sig_constraint1078 = frozenset([7, 8, 15, 16, 17, 22, 25, 34])
    FOLLOW_exp_list_in_sig_constraint1083 = frozenset([23])
    FOLLOW_PD_in_sig_constraint1087 = frozenset([1])
    FOLLOW_EXC_in_sig_constraint1138 = frozenset([22])
    FOLLOW_PG_in_sig_constraint1142 = frozenset([7, 8, 15, 16, 17, 22, 25, 34])
    FOLLOW_exp_list_in_sig_constraint1149 = frozenset([23])
    FOLLOW_PD_in_sig_constraint1152 = frozenset([1])
    FOLLOW_INC_in_sig_constraint1181 = frozenset([22])
    FOLLOW_PG_in_sig_constraint1184 = frozenset([7, 8, 15, 16, 17, 22, 25, 34])
    FOLLOW_sig_expression1_in_sig_constraint1189 = frozenset([25])
    FOLLOW_COM_in_sig_constraint1192 = frozenset([7, 8, 15, 16, 17, 22, 34])
    FOLLOW_sig_exp_in_sig_constraint1197 = frozenset([23])
    FOLLOW_PD_in_sig_constraint1200 = frozenset([1])
    FOLLOW_sig_expression1_in_exp_list1257 = frozenset([1, 25])
    FOLLOW_COM_in_exp_list1275 = frozenset([7, 8, 15, 16, 17, 22, 25, 34])
    FOLLOW_sig_expression1_in_exp_list1279 = frozenset([1, 25])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("sigexpr_compilerLexer", sigexpr_compiler)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)

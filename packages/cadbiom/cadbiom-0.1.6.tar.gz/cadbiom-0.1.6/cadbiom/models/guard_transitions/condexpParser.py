# $ANTLR 3.1.2 /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g 2012-09-11 14:55:48

import sys
from cadbiom.antlr3 import *
from cadbiom.antlr3.compat import set, frozenset




# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
F=12
WS=13
LETTER=15
OR=5
DOL=4
T=11
IDENT=8
DIGIT=16
NOT=7
COMMENT=14
PD=10
AND=6
EOF=-1
PG=9

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>",
    "DOL", "OR", "AND", "NOT", "IDENT", "PG", "PD", "T", "F", "WS", "COMMENT",
    "LETTER", "DIGIT"
]




class condexpParser(Parser):
    grammarFileName = "/home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g"
    antlr_version = version_str_to_tuple("3.1.2")
    antlr_version_str = "3.1.2"
    tokenNames = tokenNames

    def __init__(self, input, state=None):
        if state is None:
            state = RecognizerSharedState()

        Parser.__init__(self, input, state)














    # $ANTLR start "sig_bool"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:13:1: sig_bool returns [idents] : (id1= sig_bool1 DOL | DOL );
    def sig_bool(self, ):

        idents = None

        id1 = None


        idents = set([])
        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:15:9: (id1= sig_bool1 DOL | DOL )
                alt1 = 2
                LA1_0 = self.input.LA(1)

                if ((NOT <= LA1_0 <= PG) or (T <= LA1_0 <= F)) :
                    alt1 = 1
                elif (LA1_0 == DOL) :
                    alt1 = 2
                else:
                    nvae = NoViableAltException("", 1, 0, self.input)

                    raise nvae

                if alt1 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:15:11: id1= sig_bool1 DOL
                    pass
                    self._state.following.append(self.FOLLOW_sig_bool1_in_sig_bool65)
                    id1 = self.sig_bool1()

                    self._state.following.pop()
                    self.match(self.input, DOL, self.FOLLOW_DOL_in_sig_bool67)
                    #action start
                    idents = id1
                    #action end


                elif alt1 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:16:11: DOL
                    pass
                    self.match(self.input, DOL, self.FOLLOW_DOL_in_sig_bool81)



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return idents

    # $ANTLR end "sig_bool"


    # $ANTLR start "sig_bool1"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:19:1: sig_bool1 returns [idents] : id1= sig_bool_and ( OR id2= sig_bool_and )* ;
    def sig_bool1(self, ):

        idents = None

        id1 = None

        id2 = None


        idents = set([])
        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:21:9: (id1= sig_bool_and ( OR id2= sig_bool_and )* )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:21:11: id1= sig_bool_and ( OR id2= sig_bool_and )*
                pass
                self._state.following.append(self.FOLLOW_sig_bool_and_in_sig_bool1146)
                id1 = self.sig_bool_and()

                self._state.following.pop()
                #action start
                idents = id1
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:22:11: ( OR id2= sig_bool_and )*
                while True: #loop2
                    alt2 = 2
                    LA2_0 = self.input.LA(1)

                    if (LA2_0 == OR) :
                        alt2 = 1


                    if alt2 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:22:12: OR id2= sig_bool_and
                        pass
                        self.match(self.input, OR, self.FOLLOW_OR_in_sig_bool1161)
                        self._state.following.append(self.FOLLOW_sig_bool_and_in_sig_bool1165)
                        id2 = self.sig_bool_and()

                        self._state.following.pop()
                        #action start
                        idents = idents | id2
                        #action end


                    else:
                        break #loop2






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return idents

    # $ANTLR end "sig_bool1"


    # $ANTLR start "sig_bool_and"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:26:1: sig_bool_and returns [idents] : id1= sig_primary ( AND id2= sig_primary )* ;
    def sig_bool_and(self, ):

        idents = None

        id1 = None

        id2 = None


        idents = set([])
        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:28:9: (id1= sig_primary ( AND id2= sig_primary )* )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:28:11: id1= sig_primary ( AND id2= sig_primary )*
                pass
                self._state.following.append(self.FOLLOW_sig_primary_in_sig_bool_and229)
                id1 = self.sig_primary()

                self._state.following.pop()
                #action start
                idents = id1
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:29:11: ( AND id2= sig_primary )*
                while True: #loop3
                    alt3 = 2
                    LA3_0 = self.input.LA(1)

                    if (LA3_0 == AND) :
                        alt3 = 1


                    if alt3 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:29:12: AND id2= sig_primary
                        pass
                        self.match(self.input, AND, self.FOLLOW_AND_in_sig_bool_and244)
                        self._state.following.append(self.FOLLOW_sig_primary_in_sig_bool_and248)
                        id2 = self.sig_primary()

                        self._state.following.pop()
                        #action start
                        idents =  idents | id2
                        #action end


                    else:
                        break #loop3






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return idents

    # $ANTLR end "sig_bool_and"


    # $ANTLR start "sig_primary"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:33:1: sig_primary returns [idents] : ( NOT id1= sig_primary | id4= sig_constant | id2= IDENT | PG id3= sig_bool1 PD );
    def sig_primary(self, ):

        idents = None

        id2 = None
        id1 = None

        id4 = None

        id3 = None


        idents = set([])
        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:35:9: ( NOT id1= sig_primary | id4= sig_constant | id2= IDENT | PG id3= sig_bool1 PD )
                alt4 = 4
                LA4 = self.input.LA(1)
                if LA4 == NOT:
                    alt4 = 1
                elif LA4 == T or LA4 == F:
                    alt4 = 2
                elif LA4 == IDENT:
                    alt4 = 3
                elif LA4 == PG:
                    alt4 = 4
                else:
                    nvae = NoViableAltException("", 4, 0, self.input)

                    raise nvae

                if alt4 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:35:11: NOT id1= sig_primary
                    pass
                    self.match(self.input, NOT, self.FOLLOW_NOT_in_sig_primary310)
                    self._state.following.append(self.FOLLOW_sig_primary_in_sig_primary314)
                    id1 = self.sig_primary()

                    self._state.following.pop()
                    #action start
                    idents = id1
                    #action end


                elif alt4 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:38:11: id4= sig_constant
                    pass
                    self._state.following.append(self.FOLLOW_sig_constant_in_sig_primary356)
                    id4 = self.sig_constant()

                    self._state.following.pop()
                    #action start
                    idents = id4
                    #action end


                elif alt4 == 3:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:41:11: id2= IDENT
                    pass
                    id2=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_sig_primary388)
                    #action start
                    idents = set([id2.text.encode("utf8")])
                    #action end


                elif alt4 == 4:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:44:11: PG id3= sig_bool1 PD
                    pass
                    self.match(self.input, PG, self.FOLLOW_PG_in_sig_primary429)
                    self._state.following.append(self.FOLLOW_sig_bool1_in_sig_primary434)
                    id3 = self.sig_bool1()

                    self._state.following.pop()
                    self.match(self.input, PD, self.FOLLOW_PD_in_sig_primary436)
                    #action start
                    idents = id3
                    #action end



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return idents

    # $ANTLR end "sig_primary"


    # $ANTLR start "sig_constant"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:48:1: sig_constant returns [idents] : ( T | F );
    def sig_constant(self, ):

        idents = None

        idents = set([])
        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:50:10: ( T | F )
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if (LA5_0 == T) :
                    alt5 = 1
                elif (LA5_0 == F) :
                    alt5 = 2
                else:
                    nvae = NoViableAltException("", 5, 0, self.input)

                    raise nvae

                if alt5 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:50:12: T
                    pass
                    self.match(self.input, T, self.FOLLOW_T_in_sig_constant491)
                    #action start
                    idents = set([])
                    #action end


                elif alt5 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:51:12: F
                    pass
                    self.match(self.input, F, self.FOLLOW_F_in_sig_constant506)
                    #action start
                    idents = set([])
                    #action end



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return idents

    # $ANTLR end "sig_constant"


    # Delegated rules




    FOLLOW_sig_bool1_in_sig_bool65 = frozenset([4])
    FOLLOW_DOL_in_sig_bool67 = frozenset([1])
    FOLLOW_DOL_in_sig_bool81 = frozenset([1])
    FOLLOW_sig_bool_and_in_sig_bool1146 = frozenset([1, 5])
    FOLLOW_OR_in_sig_bool1161 = frozenset([7, 8, 9, 11, 12])
    FOLLOW_sig_bool_and_in_sig_bool1165 = frozenset([1, 5])
    FOLLOW_sig_primary_in_sig_bool_and229 = frozenset([1, 6])
    FOLLOW_AND_in_sig_bool_and244 = frozenset([7, 8, 9, 11, 12])
    FOLLOW_sig_primary_in_sig_bool_and248 = frozenset([1, 6])
    FOLLOW_NOT_in_sig_primary310 = frozenset([7, 8, 9, 11, 12])
    FOLLOW_sig_primary_in_sig_primary314 = frozenset([1])
    FOLLOW_sig_constant_in_sig_primary356 = frozenset([1])
    FOLLOW_IDENT_in_sig_primary388 = frozenset([1])
    FOLLOW_PG_in_sig_primary429 = frozenset([7, 8, 9, 11, 12])
    FOLLOW_sig_bool1_in_sig_primary434 = frozenset([10])
    FOLLOW_PD_in_sig_primary436 = frozenset([1])
    FOLLOW_T_in_sig_constant491 = frozenset([1])
    FOLLOW_F_in_sig_constant506 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("condexpLexer", condexpParser)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)

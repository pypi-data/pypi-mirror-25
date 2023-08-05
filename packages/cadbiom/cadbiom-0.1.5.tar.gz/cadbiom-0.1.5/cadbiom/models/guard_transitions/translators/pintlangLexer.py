# $ANTLR 3.1.2 /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g 2012-09-11 14:55:44

import sys
from cadbiom.antlr3 import *
from cadbiom.antlr3.compat import set, frozenset


# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
RB=15
RP=11
LETTER=21
LP=9
COOP=8
INT=6
NOT=18
AND=16
EOF=-1
SC=14
WS=19
COM=10
OR=17
PROC=4
ARROW=7
IDENT=5
LB=13
IN_KW=12
DIGIT=22
COMMENT=20


class pintlangLexer(Lexer):

    grammarFileName = "/home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g"
    antlr_version = version_str_to_tuple("3.1.2")
    antlr_version_str = "3.1.2"

    def __init__(self, input=None, state=None):
        if state is None:
            state = RecognizerSharedState()
        Lexer.__init__(self, input, state)

        self.dfa4 = self.DFA4(
            self, 4,
            eot = self.DFA4_eot,
            eof = self.DFA4_eof,
            min = self.DFA4_min,
            max = self.DFA4_max,
            accept = self.DFA4_accept,
            special = self.DFA4_special,
            transition = self.DFA4_transition
            )





    def set_error_reporter(self, err):
        self.error_reporter = err

    def displayRecognitionError(self, tokenNames, re):
        hdr = self.getErrorHeader(re)
        msg = self.getErrorMessage(re, tokenNames)
        self.error_reporter.display(hdr,msg)


    def displayExceptionMessage(self, e):
        msg = self.getErrorMessage(self, e, tokenNames)
        self.error_reporter.display('',msg)



    # $ANTLR start "WS"
    def mWS(self, ):

        try:
            _type = WS
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:251:13: ( ( ' ' | '\\t' | '\\n' ) )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:251:16: ( ' ' | '\\t' | '\\n' )
            pass
            if (9 <= self.input.LA(1) <= 10) or self.input.LA(1) == 32:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse

            #action start
            _channel = HIDDEN;
            #action end



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "WS"



    # $ANTLR start "COMMENT"
    def mCOMMENT(self, ):

        try:
            _type = COMMENT
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:253:13: ( '//' (~ '\\n' )* '\\n' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:253:15: '//' (~ '\\n' )* '\\n'
            pass
            self.match("//")
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:253:19: (~ '\\n' )*
            while True: #loop1
                alt1 = 2
                LA1_0 = self.input.LA(1)

                if ((0 <= LA1_0 <= 9) or (11 <= LA1_0 <= 65535)) :
                    alt1 = 1


                if alt1 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:253:20: ~ '\\n'
                    pass
                    if (0 <= self.input.LA(1) <= 9) or (11 <= self.input.LA(1) <= 65535):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse



                else:
                    break #loop1


            self.match(10)
            #action start
            _channel = HIDDEN;
            #action end



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "COMMENT"



    # $ANTLR start "PROC"
    def mPROC(self, ):

        try:
            _type = PROC
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:256:9: ( 'process' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:256:11: 'process'
            pass
            self.match("process")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "PROC"



    # $ANTLR start "ARROW"
    def mARROW(self, ):

        try:
            _type = ARROW
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:257:9: ( '->' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:257:11: '->'
            pass
            self.match("->")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ARROW"



    # $ANTLR start "COOP"
    def mCOOP(self, ):

        try:
            _type = COOP
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:258:9: ( 'COOPERATIVITY' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:258:11: 'COOPERATIVITY'
            pass
            self.match("COOPERATIVITY")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "COOP"



    # $ANTLR start "IN_KW"
    def mIN_KW(self, ):

        try:
            _type = IN_KW
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:259:9: ( 'in' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:259:11: 'in'
            pass
            self.match("in")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "IN_KW"



    # $ANTLR start "LP"
    def mLP(self, ):

        try:
            _type = LP
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:261:9: ( '(' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:261:11: '('
            pass
            self.match(40)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LP"



    # $ANTLR start "RP"
    def mRP(self, ):

        try:
            _type = RP
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:262:9: ( ')' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:262:11: ')'
            pass
            self.match(41)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "RP"



    # $ANTLR start "LB"
    def mLB(self, ):

        try:
            _type = LB
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:263:9: ( '[' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:263:11: '['
            pass
            self.match(91)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LB"



    # $ANTLR start "RB"
    def mRB(self, ):

        try:
            _type = RB
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:264:9: ( ']' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:264:11: ']'
            pass
            self.match(93)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "RB"



    # $ANTLR start "SC"
    def mSC(self, ):

        try:
            _type = SC
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:265:9: ( ';' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:265:11: ';'
            pass
            self.match(59)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "SC"



    # $ANTLR start "COM"
    def mCOM(self, ):

        try:
            _type = COM
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:266:9: ( ',' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:266:11: ','
            pass
            self.match(44)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "COM"



    # $ANTLR start "AND"
    def mAND(self, ):

        try:
            _type = AND
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:268:9: ( 'and' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:268:11: 'and'
            pass
            self.match("and")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "AND"



    # $ANTLR start "OR"
    def mOR(self, ):

        try:
            _type = OR
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:269:9: ( 'or' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:269:11: 'or'
            pass
            self.match("or")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "OR"



    # $ANTLR start "NOT"
    def mNOT(self, ):

        try:
            _type = NOT
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:270:9: ( 'not' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:270:11: 'not'
            pass
            self.match("not")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "NOT"



    # $ANTLR start "LETTER"
    def mLETTER(self, ):

        try:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:272:19: ( 'a' .. 'z' | 'A' .. 'Z' | '_' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:
            pass
            if (65 <= self.input.LA(1) <= 90) or self.input.LA(1) == 95 or (97 <= self.input.LA(1) <= 122):
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "LETTER"



    # $ANTLR start "DIGIT"
    def mDIGIT(self, ):

        try:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:274:19: ( '0' .. '9' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:274:21: '0' .. '9'
            pass
            self.matchRange(48, 57)




        finally:

            pass

    # $ANTLR end "DIGIT"



    # $ANTLR start "IDENT"
    def mIDENT(self, ):

        try:
            _type = IDENT
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:276:9: ( LETTER ( LETTER | DIGIT )* )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:276:11: LETTER ( LETTER | DIGIT )*
            pass
            self.mLETTER()
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:276:17: ( LETTER | DIGIT )*
            while True: #loop2
                alt2 = 2
                LA2_0 = self.input.LA(1)

                if ((48 <= LA2_0 <= 57) or (65 <= LA2_0 <= 90) or LA2_0 == 95 or (97 <= LA2_0 <= 122)) :
                    alt2 = 1


                if alt2 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:
                    pass
                    if (48 <= self.input.LA(1) <= 57) or (65 <= self.input.LA(1) <= 90) or self.input.LA(1) == 95 or (97 <= self.input.LA(1) <= 122):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse



                else:
                    break #loop2





            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "IDENT"



    # $ANTLR start "INT"
    def mINT(self, ):

        try:
            _type = INT
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:278:9: ( ( DIGIT )+ )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:278:11: ( DIGIT )+
            pass
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:278:11: ( DIGIT )+
            cnt3 = 0
            while True: #loop3
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if ((48 <= LA3_0 <= 57)) :
                    alt3 = 1


                if alt3 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:278:11: DIGIT
                    pass
                    self.mDIGIT()


                else:
                    if cnt3 >= 1:
                        break #loop3

                    eee = EarlyExitException(3, self.input)
                    raise eee

                cnt3 += 1





            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "INT"



    def mTokens(self):
        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:8: ( WS | COMMENT | PROC | ARROW | COOP | IN_KW | LP | RP | LB | RB | SC | COM | AND | OR | NOT | IDENT | INT )
        alt4 = 17
        alt4 = self.dfa4.predict(self.input)
        if alt4 == 1:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:10: WS
            pass
            self.mWS()


        elif alt4 == 2:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:13: COMMENT
            pass
            self.mCOMMENT()


        elif alt4 == 3:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:21: PROC
            pass
            self.mPROC()


        elif alt4 == 4:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:26: ARROW
            pass
            self.mARROW()


        elif alt4 == 5:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:32: COOP
            pass
            self.mCOOP()


        elif alt4 == 6:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:37: IN_KW
            pass
            self.mIN_KW()


        elif alt4 == 7:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:43: LP
            pass
            self.mLP()


        elif alt4 == 8:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:46: RP
            pass
            self.mRP()


        elif alt4 == 9:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:49: LB
            pass
            self.mLB()


        elif alt4 == 10:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:52: RB
            pass
            self.mRB()


        elif alt4 == 11:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:55: SC
            pass
            self.mSC()


        elif alt4 == 12:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:58: COM
            pass
            self.mCOM()


        elif alt4 == 13:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:62: AND
            pass
            self.mAND()


        elif alt4 == 14:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:66: OR
            pass
            self.mOR()


        elif alt4 == 15:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:69: NOT
            pass
            self.mNOT()


        elif alt4 == 16:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:73: IDENT
            pass
            self.mIDENT()


        elif alt4 == 17:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:1:79: INT
            pass
            self.mINT()







    # lookup tables for DFA #4

    DFA4_eot = DFA.unpack(
        u"\3\uffff\1\20\1\uffff\2\20\6\uffff\3\20\2\uffff\2\20\1\32\1\20"
        u"\1\34\3\20\1\uffff\1\40\1\uffff\1\41\2\20\2\uffff\4\20\1\50\1\20"
        u"\1\uffff\5\20\1\57\1\uffff"
        )

    DFA4_eof = DFA.unpack(
        u"\60\uffff"
        )

    DFA4_min = DFA.unpack(
        u"\1\11\2\uffff\1\162\1\uffff\1\117\1\156\6\uffff\1\156\1\162\1\157"
        u"\2\uffff\1\157\1\117\1\60\1\144\1\60\1\164\1\143\1\120\1\uffff"
        u"\1\60\1\uffff\1\60\1\145\1\105\2\uffff\1\163\1\122\1\163\1\101"
        u"\1\60\1\124\1\uffff\1\111\1\126\1\111\1\124\1\131\1\60\1\uffff"
        )

    DFA4_max = DFA.unpack(
        u"\1\172\2\uffff\1\162\1\uffff\1\117\1\156\6\uffff\1\156\1\162\1"
        u"\157\2\uffff\1\157\1\117\1\172\1\144\1\172\1\164\1\143\1\120\1"
        u"\uffff\1\172\1\uffff\1\172\1\145\1\105\2\uffff\1\163\1\122\1\163"
        u"\1\101\1\172\1\124\1\uffff\1\111\1\126\1\111\1\124\1\131\1\172"
        u"\1\uffff"
        )

    DFA4_accept = DFA.unpack(
        u"\1\uffff\1\1\1\2\1\uffff\1\4\2\uffff\1\7\1\10\1\11\1\12\1\13\1"
        u"\14\3\uffff\1\20\1\21\10\uffff\1\6\1\uffff\1\16\3\uffff\1\15\1"
        u"\17\6\uffff\1\3\6\uffff\1\5"
        )

    DFA4_special = DFA.unpack(
        u"\60\uffff"
        )


    DFA4_transition = [
        DFA.unpack(u"\2\1\25\uffff\1\1\7\uffff\1\7\1\10\2\uffff\1\14\1\4"
        u"\1\uffff\1\2\12\21\1\uffff\1\13\5\uffff\2\20\1\5\27\20\1\11\1\uffff"
        u"\1\12\1\uffff\1\20\1\uffff\1\15\7\20\1\6\4\20\1\17\1\16\1\3\12"
        u"\20"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\22"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\23"),
        DFA.unpack(u"\1\24"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\25"),
        DFA.unpack(u"\1\26"),
        DFA.unpack(u"\1\27"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\30"),
        DFA.unpack(u"\1\31"),
        DFA.unpack(u"\12\20\7\uffff\32\20\4\uffff\1\20\1\uffff\32\20"),
        DFA.unpack(u"\1\33"),
        DFA.unpack(u"\12\20\7\uffff\32\20\4\uffff\1\20\1\uffff\32\20"),
        DFA.unpack(u"\1\35"),
        DFA.unpack(u"\1\36"),
        DFA.unpack(u"\1\37"),
        DFA.unpack(u""),
        DFA.unpack(u"\12\20\7\uffff\32\20\4\uffff\1\20\1\uffff\32\20"),
        DFA.unpack(u""),
        DFA.unpack(u"\12\20\7\uffff\32\20\4\uffff\1\20\1\uffff\32\20"),
        DFA.unpack(u"\1\42"),
        DFA.unpack(u"\1\43"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\44"),
        DFA.unpack(u"\1\45"),
        DFA.unpack(u"\1\46"),
        DFA.unpack(u"\1\47"),
        DFA.unpack(u"\12\20\7\uffff\32\20\4\uffff\1\20\1\uffff\32\20"),
        DFA.unpack(u"\1\51"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\52"),
        DFA.unpack(u"\1\53"),
        DFA.unpack(u"\1\54"),
        DFA.unpack(u"\1\55"),
        DFA.unpack(u"\1\56"),
        DFA.unpack(u"\12\20\7\uffff\32\20\4\uffff\1\20\1\uffff\32\20"),
        DFA.unpack(u"")
    ]

    # class definition for DFA #4

    DFA4 = DFA




def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import LexerMain
    main = LexerMain(pintlangLexer)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)

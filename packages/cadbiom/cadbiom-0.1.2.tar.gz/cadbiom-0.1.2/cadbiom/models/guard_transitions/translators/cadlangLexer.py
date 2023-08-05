# $ANTLR 3.1.2 /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g 2012-09-12 14:02:23

import sys
from cadbiom.antlr3 import *
from cadbiom.antlr3.compat import set, frozenset


# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
ENDCONST=25
F=23
RB=11
SYNC=26
RP=18
LETTER=32
CONST=24
DEFAULT=15
LP=17
INPUT=9
T=22
ENDMACRO=14
EXCL=27
NOT=21
TEXT=12
AND=20
EOF=-1
SC=6
INC=28
NAME=4
WS=30
WHEN=16
COM=29
OR=19
TARROW=7
IDENT=5
LB=10
DIGIT=33
COMMENT=31
MACRO=13
PERM=8


class cadlangLexer(Lexer):

    grammarFileName = "/home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g"
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
        self.error_reporter.display(hdr+' '+msg)


    def displayExceptionMessage(self, e):
        msg = self.getErrorMessage(self, e, tokenNames)
        self.error_reporter.display(msg)



    # $ANTLR start "WS"
    def mWS(self, ):

        try:
            _type = WS
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:345:13: ( ( ' ' | '\\t' | '\\n' ) )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:345:16: ( ' ' | '\\t' | '\\n' )
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:347:13: ( '//' (~ '\\n' )* '\\n' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:347:15: '//' (~ '\\n' )* '\\n'
            pass
            self.match("//")
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:347:19: (~ '\\n' )*
            while True: #loop1
                alt1 = 2
                LA1_0 = self.input.LA(1)

                if ((0 <= LA1_0 <= 9) or (11 <= LA1_0 <= 65535)) :
                    alt1 = 1


                if alt1 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:347:20: ~ '\\n'
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



    # $ANTLR start "AND"
    def mAND(self, ):

        try:
            _type = AND
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:350:9: ( 'and' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:350:11: 'and'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:351:9: ( 'or' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:351:11: 'or'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:352:9: ( 'not' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:352:11: 'not'
            pass
            self.match("not")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "NOT"



    # $ANTLR start "T"
    def mT(self, ):

        try:
            _type = T
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:353:9: ( 'true' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:353:11: 'true'
            pass
            self.match("true")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "T"



    # $ANTLR start "F"
    def mF(self, ):

        try:
            _type = F
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:354:9: ( 'false' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:354:11: 'false'
            pass
            self.match("false")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "F"



    # $ANTLR start "LP"
    def mLP(self, ):

        try:
            _type = LP
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:356:9: ( '(' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:356:11: '('
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:357:9: ( ')' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:357:11: ')'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:358:9: ( '[' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:358:11: '['
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:359:9: ( ']' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:359:11: ']'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:360:9: ( ';' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:360:11: ';'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:361:9: ( ',' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:361:11: ','
            pass
            self.match(44)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "COM"



    # $ANTLR start "TARROW"
    def mTARROW(self, ):

        try:
            _type = TARROW
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:364:9: ( '-->' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:364:11: '-->'
            pass
            self.match("-->")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "TARROW"



    # $ANTLR start "PERM"
    def mPERM(self, ):

        try:
            _type = PERM
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:365:9: ( '/p' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:365:11: '/p'
            pass
            self.match("/p")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "PERM"



    # $ANTLR start "INPUT"
    def mINPUT(self, ):

        try:
            _type = INPUT
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:366:9: ( '/i' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:366:11: '/i'
            pass
            self.match("/i")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "INPUT"



    # $ANTLR start "MACRO"
    def mMACRO(self, ):

        try:
            _type = MACRO
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:367:9: ( '/macro' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:367:11: '/macro'
            pass
            self.match("/macro")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "MACRO"



    # $ANTLR start "ENDMACRO"
    def mENDMACRO(self, ):

        try:
            _type = ENDMACRO
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:368:9: ( '/endmacro' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:368:11: '/endmacro'
            pass
            self.match("/endmacro")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ENDMACRO"



    # $ANTLR start "NAME"
    def mNAME(self, ):

        try:
            _type = NAME
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:369:9: ( '/name' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:369:11: '/name'
            pass
            self.match("/name")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "NAME"



    # $ANTLR start "DEFAULT"
    def mDEFAULT(self, ):

        try:
            _type = DEFAULT
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:370:9: ( 'default' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:370:11: 'default'
            pass
            self.match("default")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DEFAULT"



    # $ANTLR start "WHEN"
    def mWHEN(self, ):

        try:
            _type = WHEN
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:371:9: ( 'when' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:371:11: 'when'
            pass
            self.match("when")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "WHEN"



    # $ANTLR start "CONST"
    def mCONST(self, ):

        try:
            _type = CONST
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:372:9: ( '/constraints' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:372:11: '/constraints'
            pass
            self.match("/constraints")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "CONST"



    # $ANTLR start "ENDCONST"
    def mENDCONST(self, ):

        try:
            _type = ENDCONST
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:373:9: ( '/endconstraints' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:373:11: '/endconstraints'
            pass
            self.match("/endconstraints")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ENDCONST"



    # $ANTLR start "SYNC"
    def mSYNC(self, ):

        try:
            _type = SYNC
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:374:9: ( 'synchro' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:374:11: 'synchro'
            pass
            self.match("synchro")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "SYNC"



    # $ANTLR start "EXCL"
    def mEXCL(self, ):

        try:
            _type = EXCL
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:375:9: ( 'exclus' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:375:11: 'exclus'
            pass
            self.match("exclus")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "EXCL"



    # $ANTLR start "INC"
    def mINC(self, ):

        try:
            _type = INC
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:376:9: ( 'included' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:376:11: 'included'
            pass
            self.match("included")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "INC"



    # $ANTLR start "LETTER"
    def mLETTER(self, ):

        try:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:378:19: ( 'a' .. 'z' | 'A' .. 'Z' | '_' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:
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
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:380:19: ( '0' .. '9' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:380:21: '0' .. '9'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:382:9: ( ( LETTER | DIGIT )+ )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:382:11: ( LETTER | DIGIT )+
            pass
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:382:11: ( LETTER | DIGIT )+
            cnt2 = 0
            while True: #loop2
                alt2 = 2
                LA2_0 = self.input.LA(1)

                if ((48 <= LA2_0 <= 57) or (65 <= LA2_0 <= 90) or LA2_0 == 95 or (97 <= LA2_0 <= 122)) :
                    alt2 = 1


                if alt2 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:
                    pass
                    if (48 <= self.input.LA(1) <= 57) or (65 <= self.input.LA(1) <= 90) or self.input.LA(1) == 95 or (97 <= self.input.LA(1) <= 122):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse



                else:
                    if cnt2 >= 1:
                        break #loop2

                    eee = EarlyExitException(2, self.input)
                    raise eee

                cnt2 += 1





            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "IDENT"



    # $ANTLR start "TEXT"
    def mTEXT(self, ):

        try:
            _type = TEXT
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:384:9: ( '{' (~ '}' )* '}' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:384:11: '{' (~ '}' )* '}'
            pass
            self.match(123)
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:384:14: (~ '}' )*
            while True: #loop3
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if ((0 <= LA3_0 <= 124) or (126 <= LA3_0 <= 65535)) :
                    alt3 = 1


                if alt3 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:384:15: ~ '}'
                    pass
                    if (0 <= self.input.LA(1) <= 124) or (126 <= self.input.LA(1) <= 65535):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse



                else:
                    break #loop3


            self.match(125)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "TEXT"



    def mTokens(self):
        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:8: ( WS | COMMENT | AND | OR | NOT | T | F | LP | RP | LB | RB | SC | COM | TARROW | PERM | INPUT | MACRO | ENDMACRO | NAME | DEFAULT | WHEN | CONST | ENDCONST | SYNC | EXCL | INC | IDENT | TEXT )
        alt4 = 28
        alt4 = self.dfa4.predict(self.input)
        if alt4 == 1:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:10: WS
            pass
            self.mWS()


        elif alt4 == 2:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:13: COMMENT
            pass
            self.mCOMMENT()


        elif alt4 == 3:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:21: AND
            pass
            self.mAND()


        elif alt4 == 4:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:25: OR
            pass
            self.mOR()


        elif alt4 == 5:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:28: NOT
            pass
            self.mNOT()


        elif alt4 == 6:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:32: T
            pass
            self.mT()


        elif alt4 == 7:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:34: F
            pass
            self.mF()


        elif alt4 == 8:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:36: LP
            pass
            self.mLP()


        elif alt4 == 9:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:39: RP
            pass
            self.mRP()


        elif alt4 == 10:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:42: LB
            pass
            self.mLB()


        elif alt4 == 11:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:45: RB
            pass
            self.mRB()


        elif alt4 == 12:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:48: SC
            pass
            self.mSC()


        elif alt4 == 13:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:51: COM
            pass
            self.mCOM()


        elif alt4 == 14:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:55: TARROW
            pass
            self.mTARROW()


        elif alt4 == 15:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:62: PERM
            pass
            self.mPERM()


        elif alt4 == 16:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:67: INPUT
            pass
            self.mINPUT()


        elif alt4 == 17:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:73: MACRO
            pass
            self.mMACRO()


        elif alt4 == 18:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:79: ENDMACRO
            pass
            self.mENDMACRO()


        elif alt4 == 19:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:88: NAME
            pass
            self.mNAME()


        elif alt4 == 20:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:93: DEFAULT
            pass
            self.mDEFAULT()


        elif alt4 == 21:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:101: WHEN
            pass
            self.mWHEN()


        elif alt4 == 22:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:106: CONST
            pass
            self.mCONST()


        elif alt4 == 23:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:112: ENDCONST
            pass
            self.mENDCONST()


        elif alt4 == 24:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:121: SYNC
            pass
            self.mSYNC()


        elif alt4 == 25:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:126: EXCL
            pass
            self.mEXCL()


        elif alt4 == 26:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:131: INC
            pass
            self.mINC()


        elif alt4 == 27:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:135: IDENT
            pass
            self.mIDENT()


        elif alt4 == 28:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:1:141: TEXT
            pass
            self.mTEXT()







    # lookup tables for DFA #4

    DFA4_eot = DFA.unpack(
        u"\3\uffff\5\24\7\uffff\5\24\11\uffff\1\24\1\51\10\24\1\uffff\1\63"
        u"\1\uffff\1\64\7\24\3\uffff\1\76\2\24\1\101\3\24\3\uffff\1\105\1"
        u"\24\1\uffff\3\24\1\uffff\2\24\1\114\1\24\1\116\1\117\1\uffff\1"
        u"\24\2\uffff\1\121\1\uffff"
        )

    DFA4_eof = DFA.unpack(
        u"\122\uffff"
        )

    DFA4_min = DFA.unpack(
        u"\1\11\1\uffff\1\57\1\156\1\162\1\157\1\162\1\141\7\uffff\1\145"
        u"\1\150\1\171\1\170\1\156\6\uffff\1\156\2\uffff\1\144\1\60\1\164"
        u"\1\165\1\154\1\146\1\145\1\156\2\143\1\144\1\60\1\uffff\1\60\1"
        u"\145\1\163\1\141\1\156\1\143\2\154\1\143\2\uffff\1\60\1\145\1\165"
        u"\1\60\1\150\2\165\3\uffff\1\60\1\154\1\uffff\1\162\1\163\1\144"
        u"\1\uffff\1\164\1\157\1\60\1\145\2\60\1\uffff\1\144\2\uffff\1\60"
        u"\1\uffff"
        )

    DFA4_max = DFA.unpack(
        u"\1\173\1\uffff\1\160\1\156\1\162\1\157\1\162\1\141\7\uffff\1\145"
        u"\1\150\1\171\1\170\1\156\6\uffff\1\156\2\uffff\1\144\1\172\1\164"
        u"\1\165\1\154\1\146\1\145\1\156\2\143\1\144\1\172\1\uffff\1\172"
        u"\1\145\1\163\1\141\1\156\1\143\2\154\1\155\2\uffff\1\172\1\145"
        u"\1\165\1\172\1\150\2\165\3\uffff\1\172\1\154\1\uffff\1\162\1\163"
        u"\1\144\1\uffff\1\164\1\157\1\172\1\145\2\172\1\uffff\1\144\2\uffff"
        u"\1\172\1\uffff"
        )

    DFA4_accept = DFA.unpack(
        u"\1\uffff\1\1\6\uffff\1\10\1\11\1\12\1\13\1\14\1\15\1\16\5\uffff"
        u"\1\33\1\34\1\2\1\17\1\20\1\21\1\uffff\1\23\1\26\14\uffff\1\4\11"
        u"\uffff\1\3\1\5\7\uffff\1\22\1\27\1\6\2\uffff\1\25\3\uffff\1\7\6"
        u"\uffff\1\31\1\uffff\1\24\1\30\1\uffff\1\32"
        )

    DFA4_special = DFA.unpack(
        u"\122\uffff"
        )


    DFA4_transition = [
        DFA.unpack(u"\2\1\25\uffff\1\1\7\uffff\1\10\1\11\2\uffff\1\15\1\16"
        u"\1\uffff\1\2\12\24\1\uffff\1\14\5\uffff\32\24\1\12\1\uffff\1\13"
        u"\1\uffff\1\24\1\uffff\1\3\2\24\1\17\1\22\1\7\2\24\1\23\4\24\1\5"
        u"\1\4\3\24\1\21\1\6\2\24\1\20\3\24\1\25"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\26\63\uffff\1\34\1\uffff\1\32\3\uffff\1\30\3\uffff"
        u"\1\31\1\33\1\uffff\1\27"),
        DFA.unpack(u"\1\35"),
        DFA.unpack(u"\1\36"),
        DFA.unpack(u"\1\37"),
        DFA.unpack(u"\1\40"),
        DFA.unpack(u"\1\41"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\42"),
        DFA.unpack(u"\1\43"),
        DFA.unpack(u"\1\44"),
        DFA.unpack(u"\1\45"),
        DFA.unpack(u"\1\46"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\47"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\50"),
        DFA.unpack(u"\12\24\7\uffff\32\24\4\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(u"\1\52"),
        DFA.unpack(u"\1\53"),
        DFA.unpack(u"\1\54"),
        DFA.unpack(u"\1\55"),
        DFA.unpack(u"\1\56"),
        DFA.unpack(u"\1\57"),
        DFA.unpack(u"\1\60"),
        DFA.unpack(u"\1\61"),
        DFA.unpack(u"\1\62"),
        DFA.unpack(u"\12\24\7\uffff\32\24\4\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(u""),
        DFA.unpack(u"\12\24\7\uffff\32\24\4\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(u"\1\65"),
        DFA.unpack(u"\1\66"),
        DFA.unpack(u"\1\67"),
        DFA.unpack(u"\1\70"),
        DFA.unpack(u"\1\71"),
        DFA.unpack(u"\1\72"),
        DFA.unpack(u"\1\73"),
        DFA.unpack(u"\1\75\11\uffff\1\74"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\12\24\7\uffff\32\24\4\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(u"\1\77"),
        DFA.unpack(u"\1\100"),
        DFA.unpack(u"\12\24\7\uffff\32\24\4\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(u"\1\102"),
        DFA.unpack(u"\1\103"),
        DFA.unpack(u"\1\104"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\12\24\7\uffff\32\24\4\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(u"\1\106"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\107"),
        DFA.unpack(u"\1\110"),
        DFA.unpack(u"\1\111"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\112"),
        DFA.unpack(u"\1\113"),
        DFA.unpack(u"\12\24\7\uffff\32\24\4\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(u"\1\115"),
        DFA.unpack(u"\12\24\7\uffff\32\24\4\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(u"\12\24\7\uffff\32\24\4\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\120"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\12\24\7\uffff\32\24\4\uffff\1\24\1\uffff\32\24"),
        DFA.unpack(u"")
    ]

    # class definition for DFA #4

    DFA4 = DFA




def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import LexerMain
    main = LexerMain(cadlangLexer)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)

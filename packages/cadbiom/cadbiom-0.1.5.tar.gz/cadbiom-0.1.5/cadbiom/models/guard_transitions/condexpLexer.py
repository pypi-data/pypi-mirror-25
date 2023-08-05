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
NOT=7
DIGIT=16
AND=6
PD=10
COMMENT=14
EOF=-1
PG=9


class condexpLexer(Lexer):

    grammarFileName = "/home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g"
    antlr_version = version_str_to_tuple("3.1.2")
    antlr_version_str = "3.1.2"

    def __init__(self, input=None, state=None):
        if state is None:
            state = RecognizerSharedState()
        Lexer.__init__(self, input, state)

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






    # $ANTLR start "WS"
    def mWS(self, ):

        try:
            _type = WS
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:55:13: ( ( ' ' | '\\t' | '\\n' ) )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:55:16: ( ' ' | '\\t' | '\\n' )
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:57:13: ( '//' (~ '\\n' )* '\\n' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:57:15: '//' (~ '\\n' )* '\\n'
            pass
            self.match("//")
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:57:19: (~ '\\n' )*
            while True: #loop1
                alt1 = 2
                LA1_0 = self.input.LA(1)

                if ((0 <= LA1_0 <= 9) or (11 <= LA1_0 <= 65535)) :
                    alt1 = 1


                if alt1 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:57:20: ~ '\\n'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:60:9: ( 'and' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:60:11: 'and'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:61:9: ( 'or' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:61:11: 'or'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:62:9: ( 'not' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:62:11: 'not'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:63:9: ( 'true' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:63:11: 'true'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:64:9: ( 'false' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:64:11: 'false'
            pass
            self.match("false")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "F"



    # $ANTLR start "PG"
    def mPG(self, ):

        try:
            _type = PG
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:66:9: ( '(' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:66:11: '('
            pass
            self.match(40)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "PG"



    # $ANTLR start "PD"
    def mPD(self, ):

        try:
            _type = PD
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:67:9: ( ')' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:67:11: ')'
            pass
            self.match(41)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "PD"



    # $ANTLR start "DOL"
    def mDOL(self, ):

        try:
            _type = DOL
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:68:9: ( '$' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:68:11: '$'
            pass
            self.match(36)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DOL"



    # $ANTLR start "LETTER"
    def mLETTER(self, ):

        try:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:71:19: ( 'a' .. 'z' | 'A' .. 'Z' | '_' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:
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
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:73:19: ( '0' .. '9' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:73:21: '0' .. '9'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:75:9: ( ( LETTER | DIGIT )+ )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:75:11: ( LETTER | DIGIT )+
            pass
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:75:11: ( LETTER | DIGIT )+
            cnt2 = 0
            while True: #loop2
                alt2 = 2
                LA2_0 = self.input.LA(1)

                if ((48 <= LA2_0 <= 57) or (65 <= LA2_0 <= 90) or LA2_0 == 95 or (97 <= LA2_0 <= 122)) :
                    alt2 = 1


                if alt2 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:
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



    def mTokens(self):
        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:1:8: ( WS | COMMENT | AND | OR | NOT | T | F | PG | PD | DOL | IDENT )
        alt3 = 11
        alt3 = self.dfa3.predict(self.input)
        if alt3 == 1:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:1:10: WS
            pass
            self.mWS()


        elif alt3 == 2:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:1:13: COMMENT
            pass
            self.mCOMMENT()


        elif alt3 == 3:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:1:21: AND
            pass
            self.mAND()


        elif alt3 == 4:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:1:25: OR
            pass
            self.mOR()


        elif alt3 == 5:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:1:28: NOT
            pass
            self.mNOT()


        elif alt3 == 6:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:1:32: T
            pass
            self.mT()


        elif alt3 == 7:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:1:34: F
            pass
            self.mF()


        elif alt3 == 8:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:1:36: PG
            pass
            self.mPG()


        elif alt3 == 9:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:1:39: PD
            pass
            self.mPD()


        elif alt3 == 10:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:1:42: DOL
            pass
            self.mDOL()


        elif alt3 == 11:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/condexp.g:1:46: IDENT
            pass
            self.mIDENT()







    # lookup tables for DFA #3

    DFA3_eot = DFA.unpack(
        u"\3\uffff\5\13\4\uffff\1\13\1\22\3\13\1\26\1\uffff\1\27\2\13\2\uffff"
        u"\1\32\1\13\1\uffff\1\34\1\uffff"
        )

    DFA3_eof = DFA.unpack(
        u"\35\uffff"
        )

    DFA3_min = DFA.unpack(
        u"\1\11\2\uffff\1\156\1\162\1\157\1\162\1\141\4\uffff\1\144\1\60"
        u"\1\164\1\165\1\154\1\60\1\uffff\1\60\1\145\1\163\2\uffff\1\60\1"
        u"\145\1\uffff\1\60\1\uffff"
        )

    DFA3_max = DFA.unpack(
        u"\1\172\2\uffff\1\156\1\162\1\157\1\162\1\141\4\uffff\1\144\1\172"
        u"\1\164\1\165\1\154\1\172\1\uffff\1\172\1\145\1\163\2\uffff\1\172"
        u"\1\145\1\uffff\1\172\1\uffff"
        )

    DFA3_accept = DFA.unpack(
        u"\1\uffff\1\1\1\2\5\uffff\1\10\1\11\1\12\1\13\6\uffff\1\4\3\uffff"
        u"\1\3\1\5\2\uffff\1\6\1\uffff\1\7"
        )

    DFA3_special = DFA.unpack(
        u"\35\uffff"
        )


    DFA3_transition = [
        DFA.unpack(u"\2\1\25\uffff\1\1\3\uffff\1\12\3\uffff\1\10\1\11\5\uffff"
        u"\1\2\12\13\7\uffff\32\13\4\uffff\1\13\1\uffff\1\3\4\13\1\7\7\13"
        u"\1\5\1\4\4\13\1\6\6\13"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\14"),
        DFA.unpack(u"\1\15"),
        DFA.unpack(u"\1\16"),
        DFA.unpack(u"\1\17"),
        DFA.unpack(u"\1\20"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\21"),
        DFA.unpack(u"\12\13\7\uffff\32\13\4\uffff\1\13\1\uffff\32\13"),
        DFA.unpack(u"\1\23"),
        DFA.unpack(u"\1\24"),
        DFA.unpack(u"\1\25"),
        DFA.unpack(u"\12\13\7\uffff\32\13\4\uffff\1\13\1\uffff\32\13"),
        DFA.unpack(u""),
        DFA.unpack(u"\12\13\7\uffff\32\13\4\uffff\1\13\1\uffff\32\13"),
        DFA.unpack(u"\1\30"),
        DFA.unpack(u"\1\31"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\12\13\7\uffff\32\13\4\uffff\1\13\1\uffff\32\13"),
        DFA.unpack(u"\1\33"),
        DFA.unpack(u""),
        DFA.unpack(u"\12\13\7\uffff\32\13\4\uffff\1\13\1\uffff\32\13"),
        DFA.unpack(u"")
    ]

    # class definition for DFA #3

    DFA3 = DFA




def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import LexerMain
    main = LexerMain(condexpLexer)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)

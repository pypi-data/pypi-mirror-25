# $ANTLR 3.1.2 /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g 2012-10-23 16:08:41

import sys
from cadbiom.antlr3 import *
from cadbiom.antlr3.compat import set, frozenset


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
NOTEG=21
SEQ=12
WHEN=7
COM=25
OR=14
DOL=24
IDENT=34
PLUS=28
DIGIT=33
PD=23
COMMENT=5
EG=20
PG=22


class sigexpr_lexer(Lexer):

    grammarFileName = "/home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g"
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:53:13: ( ( ' ' | '\\t' | '\\n' ) )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:53:16: ( ' ' | '\\t' | '\\n' )
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:55:13: ( '//' (~ '\\n' )* '\\n' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:55:15: '//' (~ '\\n' )* '\\n'
            pass
            self.match("//")
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:55:19: (~ '\\n' )*
            while True: #loop1
                alt1 = 2
                LA1_0 = self.input.LA(1)

                if ((0 <= LA1_0 <= 9) or (11 <= LA1_0 <= 65535)) :
                    alt1 = 1


                if alt1 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:55:20: ~ '\\n'
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



    # $ANTLR start "DEFAULT"
    def mDEFAULT(self, ):

        try:
            _type = DEFAULT
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:58:11: ( 'default' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:58:13: 'default'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:59:9: ( 'when' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:59:11: 'when'
            pass
            self.match("when")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "WHEN"



    # $ANTLR start "EVENT"
    def mEVENT(self, ):

        try:
            _type = EVENT
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:60:9: ( 'event' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:60:11: 'event'
            pass
            self.match("event")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "EVENT"



    # $ANTLR start "SYNC"
    def mSYNC(self, ):

        try:
            _type = SYNC
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:61:9: ( 'synchro' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:61:11: 'synchro'
            pass
            self.match("synchro")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "SYNC"



    # $ANTLR start "EXC"
    def mEXC(self, ):

        try:
            _type = EXC
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:62:9: ( 'exclus' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:62:11: 'exclus'
            pass
            self.match("exclus")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "EXC"



    # $ANTLR start "INC"
    def mINC(self, ):

        try:
            _type = INC
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:63:9: ( 'included' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:63:13: 'included'
            pass
            self.match("included")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "INC"



    # $ANTLR start "SEQ"
    def mSEQ(self, ):

        try:
            _type = SEQ
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:64:9: ( 'sequence' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:64:13: 'sequence'
            pass
            self.match("sequence")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "SEQ"



    # $ANTLR start "AND"
    def mAND(self, ):

        try:
            _type = AND
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:65:9: ( 'and' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:65:11: 'and'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:66:9: ( 'or' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:66:11: 'or'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:67:9: ( 'not' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:67:11: 'not'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:68:9: ( 'true' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:68:11: 'true'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:69:9: ( 'false' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:69:11: 'false'
            pass
            self.match("false")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "F"



    # $ANTLR start "CONSTR"
    def mCONSTR(self, ):

        try:
            _type = CONSTR
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:70:9: ( 'constraint' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:70:13: 'constraint'
            pass
            self.match("constraint")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "CONSTR"



    # $ANTLR start "DEF"
    def mDEF(self, ):

        try:
            _type = DEF
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:72:9: ( ':=' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:72:13: ':='
            pass
            self.match(":=")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DEF"



    # $ANTLR start "EG"
    def mEG(self, ):

        try:
            _type = EG
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:73:9: ( '=' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:73:13: '='
            pass
            self.match(61)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "EG"



    # $ANTLR start "NOTEG"
    def mNOTEG(self, ):

        try:
            _type = NOTEG
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:74:9: ( '!=' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:74:11: '!='
            pass
            self.match("!=")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "NOTEG"



    # $ANTLR start "PG"
    def mPG(self, ):

        try:
            _type = PG
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:75:9: ( '(' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:75:11: '('
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:76:9: ( ')' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:76:11: ')'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:77:9: ( '$' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:77:11: '$'
            pass
            self.match(36)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DOL"



    # $ANTLR start "COM"
    def mCOM(self, ):

        try:
            _type = COM
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:78:9: ( ',' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:78:11: ','
            pass
            self.match(44)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "COM"



    # $ANTLR start "UP"
    def mUP(self, ):

        try:
            _type = UP
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:79:9: ( '>' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:79:13: '>'
            pass
            self.match(62)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "UP"



    # $ANTLR start "DOWN"
    def mDOWN(self, ):

        try:
            _type = DOWN
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:80:9: ( '<' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:80:13: '<'
            pass
            self.match(60)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DOWN"



    # $ANTLR start "CHG"
    def mCHG(self, ):

        try:
            _type = CHG
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:81:9: ( '!' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:81:13: '!'
            pass
            self.match(33)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "CHG"



    # $ANTLR start "SCOL"
    def mSCOL(self, ):

        try:
            _type = SCOL
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:82:9: ( ';' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:82:13: ';'
            pass
            self.match(59)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "SCOL"



    # $ANTLR start "PLUS"
    def mPLUS(self, ):

        try:
            _type = PLUS
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:83:9: ( '+' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:83:13: '+'
            pass
            self.match(43)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "PLUS"



    # $ANTLR start "MINUS"
    def mMINUS(self, ):

        try:
            _type = MINUS
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:84:9: ( '-' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:84:13: '-'
            pass
            self.match(45)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "MINUS"



    # $ANTLR start "MUL"
    def mMUL(self, ):

        try:
            _type = MUL
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:85:9: ( '*' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:85:13: '*'
            pass
            self.match(42)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "MUL"



    # $ANTLR start "EXP"
    def mEXP(self, ):

        try:
            _type = EXP
            _channel = DEFAULT_CHANNEL

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:86:9: ( '^' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:86:13: '^'
            pass
            self.match(94)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "EXP"



    # $ANTLR start "LETTER"
    def mLETTER(self, ):

        try:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:89:19: ( 'a' .. 'z' | 'A' .. 'Z' | '_' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:
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
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:91:19: ( '0' .. '9' )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:91:21: '0' .. '9'
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

            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:95:9: ( ( LETTER | DIGIT )+ )
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:95:11: ( LETTER | DIGIT )+
            pass
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:95:11: ( LETTER | DIGIT )+
            cnt2 = 0
            while True: #loop2
                alt2 = 2
                LA2_0 = self.input.LA(1)

                if ((48 <= LA2_0 <= 57) or (65 <= LA2_0 <= 90) or LA2_0 == 95 or (97 <= LA2_0 <= 122)) :
                    alt2 = 1


                if alt2 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:
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
        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:8: ( WS | COMMENT | DEFAULT | WHEN | EVENT | SYNC | EXC | INC | SEQ | AND | OR | NOT | T | F | CONSTR | DEF | EG | NOTEG | PG | PD | DOL | COM | UP | DOWN | CHG | SCOL | PLUS | MINUS | MUL | EXP | IDENT )
        alt3 = 31
        alt3 = self.dfa3.predict(self.input)
        if alt3 == 1:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:10: WS
            pass
            self.mWS()


        elif alt3 == 2:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:13: COMMENT
            pass
            self.mCOMMENT()


        elif alt3 == 3:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:21: DEFAULT
            pass
            self.mDEFAULT()


        elif alt3 == 4:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:29: WHEN
            pass
            self.mWHEN()


        elif alt3 == 5:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:34: EVENT
            pass
            self.mEVENT()


        elif alt3 == 6:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:40: SYNC
            pass
            self.mSYNC()


        elif alt3 == 7:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:45: EXC
            pass
            self.mEXC()


        elif alt3 == 8:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:49: INC
            pass
            self.mINC()


        elif alt3 == 9:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:53: SEQ
            pass
            self.mSEQ()


        elif alt3 == 10:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:57: AND
            pass
            self.mAND()


        elif alt3 == 11:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:61: OR
            pass
            self.mOR()


        elif alt3 == 12:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:64: NOT
            pass
            self.mNOT()


        elif alt3 == 13:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:68: T
            pass
            self.mT()


        elif alt3 == 14:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:70: F
            pass
            self.mF()


        elif alt3 == 15:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:72: CONSTR
            pass
            self.mCONSTR()


        elif alt3 == 16:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:79: DEF
            pass
            self.mDEF()


        elif alt3 == 17:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:83: EG
            pass
            self.mEG()


        elif alt3 == 18:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:86: NOTEG
            pass
            self.mNOTEG()


        elif alt3 == 19:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:92: PG
            pass
            self.mPG()


        elif alt3 == 20:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:95: PD
            pass
            self.mPD()


        elif alt3 == 21:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:98: DOL
            pass
            self.mDOL()


        elif alt3 == 22:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:102: COM
            pass
            self.mCOM()


        elif alt3 == 23:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:106: UP
            pass
            self.mUP()


        elif alt3 == 24:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:109: DOWN
            pass
            self.mDOWN()


        elif alt3 == 25:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:114: CHG
            pass
            self.mCHG()


        elif alt3 == 26:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:118: SCOL
            pass
            self.mSCOL()


        elif alt3 == 27:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:123: PLUS
            pass
            self.mPLUS()


        elif alt3 == 28:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:128: MINUS
            pass
            self.mMINUS()


        elif alt3 == 29:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:134: MUL
            pass
            self.mMUL()


        elif alt3 == 30:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:138: EXP
            pass
            self.mEXP()


        elif alt3 == 31:
            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/biosignal/translators/sigexpr_lexer.g:1:142: IDENT
            pass
            self.mIDENT()







    # lookup tables for DFA #3

    DFA3_eot = DFA.unpack(
        u"\3\uffff\13\34\2\uffff\1\101\14\uffff\1\34\2\uffff\1\34\2\uffff"
        u"\2\34\2\uffff\2\34\2\uffff\1\34\2\uffff\1\34\2\uffff\1\132\2\uffff"
        u"\1\34\2\uffff\1\34\2\uffff\1\34\2\uffff\1\34\52\uffff"
        )

    DFA3_eof = DFA.unpack(
        u"\150\uffff"
        )

    DFA3_min = DFA.unpack(
        u"\1\11\2\uffff\1\145\1\150\1\166\1\145\2\156\1\162\1\157\1\162\1"
        u"\141\1\157\2\uffff\1\75\14\uffff\1\146\2\uffff\1\145\2\uffff\1"
        u"\145\1\143\2\uffff\1\156\1\161\2\uffff\1\143\2\uffff\1\144\2\uffff"
        u"\1\60\2\uffff\1\164\2\uffff\1\165\2\uffff\1\154\2\uffff\1\156\52"
        u"\uffff"
        )

    DFA3_max = DFA.unpack(
        u"\1\172\2\uffff\1\145\1\150\1\170\1\171\2\156\1\162\1\157\1\162"
        u"\1\141\1\157\2\uffff\1\75\14\uffff\1\146\2\uffff\1\145\2\uffff"
        u"\1\145\1\143\2\uffff\1\156\1\161\2\uffff\1\143\2\uffff\1\144\2"
        u"\uffff\1\172\2\uffff\1\164\2\uffff\1\165\2\uffff\1\154\2\uffff"
        u"\1\156\52\uffff"
        )

    DFA3_accept = DFA.unpack(
        u"\1\uffff\1\1\1\2\13\uffff\1\20\1\21\1\uffff\1\23\1\24\1\25\1\26"
        u"\1\27\1\30\1\32\1\33\1\34\1\35\1\36\1\37\43\uffff\1\22\1\31\1\3"
        u"\2\uffff\1\4\2\uffff\1\5\2\uffff\1\7\2\uffff\1\6\2\uffff\1\11\2"
        u"\uffff\1\10\2\uffff\1\12\2\uffff\1\13\1\uffff\1\14\2\uffff\1\15"
        u"\2\uffff\1\16\2\uffff\1\17\2\uffff"
        )

    DFA3_special = DFA.unpack(
        u"\150\uffff"
        )


    DFA3_transition = [
        DFA.unpack(u"\2\1\25\uffff\1\1\1\20\2\uffff\1\23\3\uffff\1\21\1\22"
        u"\1\32\1\30\1\24\1\31\1\uffff\1\2\12\34\1\16\1\27\1\26\1\17\1\25"
        u"\2\uffff\32\34\3\uffff\1\33\1\34\1\uffff\1\10\1\34\1\15\1\3\1\5"
        u"\1\14\2\34\1\7\4\34\1\12\1\11\3\34\1\6\1\13\2\34\1\4\3\34"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\35"),
        DFA.unpack(u"\1\40"),
        DFA.unpack(u"\1\43\1\uffff\1\44"),
        DFA.unpack(u"\1\50\23\uffff\1\47"),
        DFA.unpack(u"\1\53"),
        DFA.unpack(u"\1\56"),
        DFA.unpack(u"\1\61"),
        DFA.unpack(u"\1\64"),
        DFA.unpack(u"\1\67"),
        DFA.unpack(u"\1\72"),
        DFA.unpack(u"\1\75"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\100"),
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
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\102"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\105"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\110"),
        DFA.unpack(u"\1\113"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\116"),
        DFA.unpack(u"\1\121"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\124"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\127"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\12\34\7\uffff\32\34\4\uffff\1\34\1\uffff\32\34"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\134"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\137"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\142"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\145"),
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
        DFA.unpack(u""),
        DFA.unpack(u"")
    ]

    # class definition for DFA #3

    DFA3 = DFA




def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import LexerMain
    main = LexerMain(sigexpr_lexer)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)

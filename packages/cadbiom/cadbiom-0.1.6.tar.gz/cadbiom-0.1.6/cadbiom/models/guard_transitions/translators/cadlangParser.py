# $ANTLR 3.1.2 /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g 2012-09-12 14:02:23

import sys
from cadbiom.antlr3 import *
from cadbiom.antlr3.compat import set, frozenset

from cadbiom.antlr3.tree import *






# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
ENDCONST=25
F=23
SYNC=26
RB=11
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
TARROW=7
OR=19
IDENT=5
LB=10
DIGIT=33
COMMENT=31
MACRO=13
PERM=8

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>",
    "NAME", "IDENT", "SC", "TARROW", "PERM", "INPUT", "LB", "RB", "TEXT",
    "MACRO", "ENDMACRO", "DEFAULT", "WHEN", "LP", "RP", "OR", "AND", "NOT",
    "T", "F", "CONST", "ENDCONST", "SYNC", "EXCL", "INC", "COM", "WS", "COMMENT",
    "LETTER", "DIGIT"
]




class cadlangParser(Parser):
    grammarFileName = "/home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g"
    antlr_version = version_str_to_tuple("3.1.2")
    antlr_version_str = "3.1.2"
    tokenNames = tokenNames

    def __init__(self, input, state=None):
        if state is None:
            state = RecognizerSharedState()

        Parser.__init__(self, input, state)








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
        self.error_reporter.display(hdr+' '+msg)


    def displayExceptionMessage(self, e):
        msg = self.getErrorMessage(self, e, tokenNames)
        self.error_reporter.display(msg)

    def check_ident_dec(self, id, type, line):
        """
        @param id : string
        """
        line_txt = 'line '+str(line)+':'
        try:
          place = self.symb_tab[id]
          self.error_reporter.display(line_txt+" Node double declaration:"+id)

        except KeyError:
          if type == 'S':
            node = self.current_macro.add_simple_node(id, 0,0)
          elif type == 'P':
            node = self.current_macro.add_perm_node(id, 0,0)
          elif type == 'I':
            node = self.current_macro.add_input_node(id, 0,0)
          else:
            self.error_reporter.display(line_txt+ " Unknown type - bug?")
          self.symb_tab[id] = node


    def check_ident_trans(self, id, type, line):
        """
        @param id : string
        """
        line_txt = 'line '+str(line)+':'
        try:
          # already used node
          node = self.symb_tab[id]
          tok = (node.is_input() and type == 'I') or (node.is_perm() and type == 'P') or (type == 'N')
          if (not tok)  :
            self.error_reporter.display(line_txt + " Type error in transition: "+id)
        except KeyError:
          if type == 'N':
            node = self.current_macro.add_simple_node(id, 0,0)
          elif type == 'P':
            node = self.current_macro.add_perm_node(id, 0,0)
          elif type == 'I':
            node = self.current_macro.add_input_node(id, 0,0)
          else:
            self.error_reporter.display(line_txt+ " Unknown type - bug?")
          self.symb_tab[id] = node
        return node

    def check_ident_start(self, id, line):
        """
        @param id : string
        """
        line_txt = 'line '+str(line)+':'
        try:
          # already used node, must be simple or macro
          node = self.symb_tab[id]
          tnok = node.is_input() or node.is_perm()
          if tnok:
            self.error_reporter.display(line_txt+ " Type error in start transition: "+id)
        except KeyError:
          node = self.current_macro.add_simple_node(id, 0,0)
          self.symb_tab[id] = node
        return node

    def check_ident_deg(self, id, line):
        """
        @param id : string
        """
        line_txt = 'line '+str(line)+':'
        try:
          # already used node, must be simple
          node = self.symb_tab[id]
          if not (node.is_simple() or node.is_macro()):
            # degradation allowed from macro nodes - TO MODIFY??
            self.error_reporter.display(line_txt+" Type error in degradation transition: "+id)
        except KeyError:
          node = self.current_macro.add_simple_node(id, 0,0)
          self.symb_tab[id] = node
        return node

    def build_transition(self, id1, modif, id2, modif2, gc, note, line):
        line_txt = 'line '+str(line)+':'
        if modif:
          type = self.modif_code(modif)
        else:
          type = 'N'
        ori = self.check_ident_trans(id1, type, line)
        if modif2:
          type2 = self.modif_code(modif)
        else:
          type2 = 'N'
        target = self.check_ident_trans(id2, type2, line)
        # check if origin and target are in the same macro
        if not ori.father == target.father:
          self.error_reporter.display(line_txt+" Node:"+id1+ " and node:"+id2 + " are not in the same macro")
        if gc[0]:
          event = gc[0]
        else:
          event = ''
        if gc[1]:
          cond = gc[1]
        else:
          cond = ''
        note_txt = self.clean_note(note)
        t = self.current_macro.add_transition(ori, target)
        if event:
          t.set_event(event)
        t.set_condition(cond)
        if len(note_txt)>0:
          t.note = note_txt

    def build_start_transition(self, id, note, line):
        ori = self.current_macro.add_start_node(0,0)
        target = self.check_ident_start(id, line)
        t = self.current_macro.add_transition(ori, target)
        if note:
          note_txt = self.clean_note(note)
          t.set_note(note_txt)

    def build_deg_transition(self, id, gc, note, line):
        target = self.current_macro.add_trap_node(0,0)
        ori = self.check_ident_deg(id, line)
        event = gc[0]
        cond = gc[1]
        note_txt = self.clean_note(note)
        t = self.current_macro.add_transition(ori, target)
        if event:
          t.set_event(event)
        t.set_condition(cond)

    def enter_macro(self, id, line):
        line_txt = 'line '+str(line)+':'
        self.macro_pile.append(self.current_macro)
        try:
          node = self.symb_tab[id]
          if not node.is_macro():
            self.error_reporter.display(line_txt+ " Not macro node used as macro:"+id)
            return
          else:
            self.error_reporter.display(line_txt+ " Macro double definition:"+id)

        except KeyError:
          node = self.current_macro.add_macro_subnode(id,0,0, 0.25, 0.25)
          self.symb_tab[id] = node
        self.current_macro = node


    def leave_macro(self, id=None):
        self.current_macro = self.macro_pile.pop()

    def clean_note(self, note):
        return note[1:-1]

    def modif_code(self, modif):
        if modif == '/p':
          return 'P'
        elif modif == '/i':
          return 'I'

    def check_end(self):
        if len(self.macro_pile)>0:
          self.error_reporter.display("Bad macro imbrication - missing \endmacro?")


    class cad_model_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.tree = None




    # $ANTLR start "cad_model"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:207:1: cad_model[model] : ( NAME id= IDENT )? ( macro | transition | dec )+ (txt= constraints )? EOF ;
    def cad_model(self, model):

        retval = self.cad_model_return()
        retval.start = self.input.LT(1)

        root_0 = None

        id = None
        NAME1 = None
        EOF5 = None
        txt = None

        macro2 = None

        transition3 = None

        dec4 = None


        id_tree = None
        NAME1_tree = None
        EOF5_tree = None


        self.model = model
        self.macro_pile = []
        self.symb_tab = dict()
        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:212:12: ( ( NAME id= IDENT )? ( macro | transition | dec )+ (txt= constraints )? EOF )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:213:17: ( NAME id= IDENT )? ( macro | transition | dec )+ (txt= constraints )? EOF
                pass
                root_0 = self._adaptor.nil()

                #action start
                self.current_macro = self.model.get_root()
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:215:13: ( NAME id= IDENT )?
                alt1 = 2
                LA1_0 = self.input.LA(1)

                if (LA1_0 == NAME) :
                    alt1 = 1
                if alt1 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:215:14: NAME id= IDENT
                    pass
                    NAME1=self.match(self.input, NAME, self.FOLLOW_NAME_in_cad_model139)

                    NAME1_tree = self._adaptor.createWithPayload(NAME1)
                    self._adaptor.addChild(root_0, NAME1_tree)

                    id=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_cad_model143)

                    id_tree = self._adaptor.createWithPayload(id)
                    self._adaptor.addChild(root_0, id_tree)

                    #action start
                    self.model.name = id.text
                    #action end



                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:216:13: ( macro | transition | dec )+
                cnt2 = 0
                while True: #loop2
                    alt2 = 4
                    LA2 = self.input.LA(1)
                    if LA2 == MACRO:
                        alt2 = 1
                    elif LA2 == IDENT:
                        LA2 = self.input.LA(2)
                        if LA2 == TARROW:
                            alt2 = 2
                        elif LA2 == PERM or LA2 == INPUT:
                            LA2_5 = self.input.LA(3)

                            if (LA2_5 == SC) :
                                alt2 = 3
                            elif (LA2_5 == TARROW) :
                                alt2 = 2


                        elif LA2 == SC:
                            alt2 = 3

                    elif LA2 == TARROW:
                        alt2 = 2

                    if alt2 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:216:14: macro
                        pass
                        self._state.following.append(self.FOLLOW_macro_in_cad_model162)
                        macro2 = self.macro()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, macro2.tree)


                    elif alt2 == 2:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:216:20: transition
                        pass
                        self._state.following.append(self.FOLLOW_transition_in_cad_model164)
                        transition3 = self.transition()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, transition3.tree)


                    elif alt2 == 3:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:216:31: dec
                        pass
                        self._state.following.append(self.FOLLOW_dec_in_cad_model166)
                        dec4 = self.dec()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, dec4.tree)


                    else:
                        if cnt2 >= 1:
                            break #loop2

                        eee = EarlyExitException(2, self.input)
                        raise eee

                    cnt2 += 1


                #action start
                self.check_end()
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:218:13: (txt= constraints )?
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if (LA3_0 == CONST) :
                    alt3 = 1
                if alt3 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:218:14: txt= constraints
                    pass
                    self._state.following.append(self.FOLLOW_constraints_in_cad_model203)
                    txt = self.constraints()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, txt.tree)
                    #action start
                    self.model.constraints = ((txt is not None) and [txt.text] or [None])[0]
                    #action end



                EOF5=self.match(self.input, EOF, self.FOLLOW_EOF_in_cad_model222)

                EOF5_tree = self._adaptor.createWithPayload(EOF5)
                self._adaptor.addChild(root_0, EOF5_tree)




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

    # $ANTLR end "cad_model"

    class dec_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.tree = None




    # $ANTLR start "dec"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:222:1: dec : id= IDENT (m= modifier )? SC ;
    def dec(self, ):

        retval = self.dec_return()
        retval.start = self.input.LT(1)

        root_0 = None

        id = None
        SC6 = None
        m = None


        id_tree = None
        SC6_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:222:12: (id= IDENT (m= modifier )? SC )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:222:13: id= IDENT (m= modifier )? SC
                pass
                root_0 = self._adaptor.nil()

                #action start
                type = 'S'
                #action end
                id=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_dec270)

                id_tree = self._adaptor.createWithPayload(id)
                self._adaptor.addChild(root_0, id_tree)

                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:224:22: (m= modifier )?
                alt4 = 2
                LA4_0 = self.input.LA(1)

                if ((PERM <= LA4_0 <= INPUT)) :
                    alt4 = 1
                if alt4 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:224:23: m= modifier
                    pass
                    self._state.following.append(self.FOLLOW_modifier_in_dec275)
                    m = self.modifier()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, m.tree)
                    #action start
                    type = self.modif_code(((m is not None) and [self.input.toString(m.start,m.stop)] or [None])[0])
                    #action end



                SC6=self.match(self.input, SC, self.FOLLOW_SC_in_dec281)

                SC6_tree = self._adaptor.createWithPayload(SC6)
                self._adaptor.addChild(root_0, SC6_tree)

                #action start
                self.check_ident_dec(id.text, type, id.line)
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

    # $ANTLR end "dec"

    class transition_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.tree = None




    # $ANTLR start "transition"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:228:1: transition : (id1= IDENT (m= modifier )? TARROW id2= IDENT SC gc= guard (m2= modifier )? ntext= note SC | id3= IDENT TARROW SC gc1= guard ntext1= note SC | TARROW id4= IDENT SC (ntext2= note SC )? );
    def transition(self, ):

        retval = self.transition_return()
        retval.start = self.input.LT(1)

        root_0 = None

        id1 = None
        id2 = None
        id3 = None
        id4 = None
        TARROW7 = None
        SC8 = None
        SC9 = None
        TARROW10 = None
        SC11 = None
        SC12 = None
        TARROW13 = None
        SC14 = None
        SC15 = None
        m = None

        gc = None

        m2 = None

        ntext = None

        gc1 = None

        ntext1 = None

        ntext2 = None


        id1_tree = None
        id2_tree = None
        id3_tree = None
        id4_tree = None
        TARROW7_tree = None
        SC8_tree = None
        SC9_tree = None
        TARROW10_tree = None
        SC11_tree = None
        SC12_tree = None
        TARROW13_tree = None
        SC14_tree = None
        SC15_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:228:12: (id1= IDENT (m= modifier )? TARROW id2= IDENT SC gc= guard (m2= modifier )? ntext= note SC | id3= IDENT TARROW SC gc1= guard ntext1= note SC | TARROW id4= IDENT SC (ntext2= note SC )? )
                alt8 = 3
                LA8_0 = self.input.LA(1)

                if (LA8_0 == IDENT) :
                    LA8_1 = self.input.LA(2)

                    if (LA8_1 == TARROW) :
                        LA8_3 = self.input.LA(3)

                        if (LA8_3 == SC) :
                            alt8 = 2
                        elif (LA8_3 == IDENT) :
                            alt8 = 1
                        else:
                            nvae = NoViableAltException("", 8, 3, self.input)

                            raise nvae

                    elif ((PERM <= LA8_1 <= INPUT)) :
                        alt8 = 1
                    else:
                        nvae = NoViableAltException("", 8, 1, self.input)

                        raise nvae

                elif (LA8_0 == TARROW) :
                    alt8 = 3
                else:
                    nvae = NoViableAltException("", 8, 0, self.input)

                    raise nvae

                if alt8 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:229:13: id1= IDENT (m= modifier )? TARROW id2= IDENT SC gc= guard (m2= modifier )? ntext= note SC
                    pass
                    root_0 = self._adaptor.nil()

                    id1=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_transition340)

                    id1_tree = self._adaptor.createWithPayload(id1)
                    self._adaptor.addChild(root_0, id1_tree)

                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:229:23: (m= modifier )?
                    alt5 = 2
                    LA5_0 = self.input.LA(1)

                    if ((PERM <= LA5_0 <= INPUT)) :
                        alt5 = 1
                    if alt5 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:229:24: m= modifier
                        pass
                        self._state.following.append(self.FOLLOW_modifier_in_transition345)
                        m = self.modifier()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, m.tree)



                    TARROW7=self.match(self.input, TARROW, self.FOLLOW_TARROW_in_transition349)

                    TARROW7_tree = self._adaptor.createWithPayload(TARROW7)
                    self._adaptor.addChild(root_0, TARROW7_tree)

                    id2=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_transition353)

                    id2_tree = self._adaptor.createWithPayload(id2)
                    self._adaptor.addChild(root_0, id2_tree)

                    SC8=self.match(self.input, SC, self.FOLLOW_SC_in_transition355)

                    SC8_tree = self._adaptor.createWithPayload(SC8)
                    self._adaptor.addChild(root_0, SC8_tree)

                    self._state.following.append(self.FOLLOW_guard_in_transition359)
                    gc = self.guard()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, gc.tree)
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:229:66: (m2= modifier )?
                    alt6 = 2
                    LA6_0 = self.input.LA(1)

                    if ((PERM <= LA6_0 <= INPUT)) :
                        alt6 = 1
                    if alt6 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:229:67: m2= modifier
                        pass
                        self._state.following.append(self.FOLLOW_modifier_in_transition364)
                        m2 = self.modifier()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, m2.tree)



                    self._state.following.append(self.FOLLOW_note_in_transition370)
                    ntext = self.note()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, ntext.tree)
                    SC9=self.match(self.input, SC, self.FOLLOW_SC_in_transition372)

                    SC9_tree = self._adaptor.createWithPayload(SC9)
                    self._adaptor.addChild(root_0, SC9_tree)

                    #action start
                    self.build_transition(id1.text, ((m is not None) and [self.input.toString(m.start,m.stop)] or [None])[0], id2.text, ((m2 is not None) and [self.input.toString(m2.start,m2.stop)] or [None])[0], ((gc is not None) and [gc.guard_component] or [None])[0], ((ntext is not None) and [self.input.toString(ntext.start,ntext.stop)] or [None])[0], id1.line)
                    #action end


                elif alt8 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:232:14: id3= IDENT TARROW SC gc1= guard ntext1= note SC
                    pass
                    root_0 = self._adaptor.nil()

                    id3=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_transition416)

                    id3_tree = self._adaptor.createWithPayload(id3)
                    self._adaptor.addChild(root_0, id3_tree)

                    TARROW10=self.match(self.input, TARROW, self.FOLLOW_TARROW_in_transition418)

                    TARROW10_tree = self._adaptor.createWithPayload(TARROW10)
                    self._adaptor.addChild(root_0, TARROW10_tree)

                    SC11=self.match(self.input, SC, self.FOLLOW_SC_in_transition421)

                    SC11_tree = self._adaptor.createWithPayload(SC11)
                    self._adaptor.addChild(root_0, SC11_tree)

                    self._state.following.append(self.FOLLOW_guard_in_transition425)
                    gc1 = self.guard()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, gc1.tree)
                    self._state.following.append(self.FOLLOW_note_in_transition429)
                    ntext1 = self.note()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, ntext1.tree)
                    SC12=self.match(self.input, SC, self.FOLLOW_SC_in_transition431)

                    SC12_tree = self._adaptor.createWithPayload(SC12)
                    self._adaptor.addChild(root_0, SC12_tree)

                    #action start
                    self.build_deg_transition(id3.text, ((gc1 is not None) and [gc1.guard_component] or [None])[0], ((ntext1 is not None) and [self.input.toString(ntext1.start,ntext1.stop)] or [None])[0], id3.line)
                    #action end


                elif alt8 == 3:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:235:14: TARROW id4= IDENT SC (ntext2= note SC )?
                    pass
                    root_0 = self._adaptor.nil()

                    TARROW13=self.match(self.input, TARROW, self.FOLLOW_TARROW_in_transition474)

                    TARROW13_tree = self._adaptor.createWithPayload(TARROW13)
                    self._adaptor.addChild(root_0, TARROW13_tree)

                    id4=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_transition478)

                    id4_tree = self._adaptor.createWithPayload(id4)
                    self._adaptor.addChild(root_0, id4_tree)

                    SC14=self.match(self.input, SC, self.FOLLOW_SC_in_transition481)

                    SC14_tree = self._adaptor.createWithPayload(SC14)
                    self._adaptor.addChild(root_0, SC14_tree)

                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:235:35: (ntext2= note SC )?
                    alt7 = 2
                    LA7_0 = self.input.LA(1)

                    if (LA7_0 == SC or LA7_0 == TEXT) :
                        alt7 = 1
                    if alt7 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:235:36: ntext2= note SC
                        pass
                        self._state.following.append(self.FOLLOW_note_in_transition486)
                        ntext2 = self.note()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, ntext2.tree)
                        SC15=self.match(self.input, SC, self.FOLLOW_SC_in_transition488)

                        SC15_tree = self._adaptor.createWithPayload(SC15)
                        self._adaptor.addChild(root_0, SC15_tree)




                    #action start
                    self.build_start_transition(id4.text, ((ntext2 is not None) and [self.input.toString(ntext2.start,ntext2.stop)] or [None])[0], id4.line)
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

    # $ANTLR end "transition"

    class modifier_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.tree = None




    # $ANTLR start "modifier"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:239:1: modifier : ( PERM | INPUT );
    def modifier(self, ):

        retval = self.modifier_return()
        retval.start = self.input.LT(1)

        root_0 = None

        set16 = None

        set16_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:239:12: ( PERM | INPUT )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:
                pass
                root_0 = self._adaptor.nil()

                set16 = self.input.LT(1)
                if (PERM <= self.input.LA(1) <= INPUT):
                    self.input.consume()
                    self._adaptor.addChild(root_0, self._adaptor.createWithPayload(set16))
                    self._state.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    raise mse





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

    # $ANTLR end "modifier"

    class guard_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.guard_component = None
            self.tree = None




    # $ANTLR start "guard"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:245:1: guard returns [guard_component] : (h= sig_expression )? LB (bt= bool_exp ) RB (id2= IDENT )? ;
    def guard(self, ):

        retval = self.guard_return()
        retval.start = self.input.LT(1)

        root_0 = None

        id2 = None
        LB17 = None
        RB18 = None
        h = None

        bt = None


        id2_tree = None
        LB17_tree = None
        RB18_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:246:12: ( (h= sig_expression )? LB (bt= bool_exp ) RB (id2= IDENT )? )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:247:13: (h= sig_expression )? LB (bt= bool_exp ) RB (id2= IDENT )?
                pass
                root_0 = self._adaptor.nil()

                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:247:13: (h= sig_expression )?
                alt9 = 2
                LA9_0 = self.input.LA(1)

                if (LA9_0 == IDENT or LA9_0 == LP) :
                    alt9 = 1
                if alt9 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:247:14: h= sig_expression
                    pass
                    self._state.following.append(self.FOLLOW_sig_expression_in_guard634)
                    h = self.sig_expression()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, h.tree)



                LB17=self.match(self.input, LB, self.FOLLOW_LB_in_guard638)

                LB17_tree = self._adaptor.createWithPayload(LB17)
                self._adaptor.addChild(root_0, LB17_tree)

                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:247:36: (bt= bool_exp )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:247:37: bt= bool_exp
                pass
                self._state.following.append(self.FOLLOW_bool_exp_in_guard643)
                bt = self.bool_exp()

                self._state.following.pop()
                self._adaptor.addChild(root_0, bt.tree)



                RB18=self.match(self.input, RB, self.FOLLOW_RB_in_guard646)

                RB18_tree = self._adaptor.createWithPayload(RB18)
                self._adaptor.addChild(root_0, RB18_tree)

                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:247:53: (id2= IDENT )?
                alt10 = 2
                LA10_0 = self.input.LA(1)

                if (LA10_0 == IDENT) :
                    alt10 = 1
                if alt10 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:247:54: id2= IDENT
                    pass
                    id2=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_guard651)

                    id2_tree = self._adaptor.createWithPayload(id2)
                    self._adaptor.addChild(root_0, id2_tree)




                #action start
                if h and id2: retval.guard_component = (((h is not None) and [h.text] or [None])[0], ((bt is not None) and [bt.text] or [None])[0], id2.text)
                elif h: retval.guard_component = (((h is not None) and [h.text] or [None])[0], ((bt is not None) and [bt.text] or [None])[0], None)
                elif id2: retval.guard_component = (None, ((bt is not None) and [bt.text] or [None])[0], id2.text)
                else:  retval.guard_component = (None, ((bt is not None) and [bt.text] or [None])[0], None)
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

    # $ANTLR end "guard"

    class note_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.tree = None




    # $ANTLR start "note"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:254:1: note : ( TEXT | );
    def note(self, ):

        retval = self.note_return()
        retval.start = self.input.LT(1)

        root_0 = None

        TEXT19 = None

        TEXT19_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:254:12: ( TEXT | )
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if (LA11_0 == TEXT) :
                    alt11 = 1
                elif (LA11_0 == SC) :
                    alt11 = 2
                else:
                    nvae = NoViableAltException("", 11, 0, self.input)

                    raise nvae

                if alt11 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:255:13: TEXT
                    pass
                    root_0 = self._adaptor.nil()

                    TEXT19=self.match(self.input, TEXT, self.FOLLOW_TEXT_in_note717)

                    TEXT19_tree = self._adaptor.createWithPayload(TEXT19)
                    self._adaptor.addChild(root_0, TEXT19_tree)



                elif alt11 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:257:12:
                    pass
                    root_0 = self._adaptor.nil()


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

    # $ANTLR end "note"

    class macro_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.tree = None




    # $ANTLR start "macro"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:259:1: macro : MACRO id1= IDENT ( macro | transition | dec )* ENDMACRO ;
    def macro(self, ):

        retval = self.macro_return()
        retval.start = self.input.LT(1)

        root_0 = None

        id1 = None
        MACRO20 = None
        ENDMACRO24 = None
        macro21 = None

        transition22 = None

        dec23 = None


        id1_tree = None
        MACRO20_tree = None
        ENDMACRO24_tree = None

        id2 = None
        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:260:12: ( MACRO id1= IDENT ( macro | transition | dec )* ENDMACRO )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:261:13: MACRO id1= IDENT ( macro | transition | dec )* ENDMACRO
                pass
                root_0 = self._adaptor.nil()

                MACRO20=self.match(self.input, MACRO, self.FOLLOW_MACRO_in_macro795)

                MACRO20_tree = self._adaptor.createWithPayload(MACRO20)
                self._adaptor.addChild(root_0, MACRO20_tree)

                id1=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_macro799)

                id1_tree = self._adaptor.createWithPayload(id1)
                self._adaptor.addChild(root_0, id1_tree)

                #action start
                self.enter_macro(id1.text, id1.line)
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:263:13: ( macro | transition | dec )*
                while True: #loop12
                    alt12 = 4
                    LA12 = self.input.LA(1)
                    if LA12 == MACRO:
                        alt12 = 1
                    elif LA12 == IDENT:
                        LA12 = self.input.LA(2)
                        if LA12 == TARROW:
                            alt12 = 2
                        elif LA12 == PERM or LA12 == INPUT:
                            LA12_5 = self.input.LA(3)

                            if (LA12_5 == TARROW) :
                                alt12 = 2
                            elif (LA12_5 == SC) :
                                alt12 = 3


                        elif LA12 == SC:
                            alt12 = 3

                    elif LA12 == TARROW:
                        alt12 = 2

                    if alt12 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:263:14: macro
                        pass
                        self._state.following.append(self.FOLLOW_macro_in_macro829)
                        macro21 = self.macro()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, macro21.tree)


                    elif alt12 == 2:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:263:20: transition
                        pass
                        self._state.following.append(self.FOLLOW_transition_in_macro831)
                        transition22 = self.transition()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, transition22.tree)


                    elif alt12 == 3:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:263:31: dec
                        pass
                        self._state.following.append(self.FOLLOW_dec_in_macro833)
                        dec23 = self.dec()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, dec23.tree)


                    else:
                        break #loop12


                ENDMACRO24=self.match(self.input, ENDMACRO, self.FOLLOW_ENDMACRO_in_macro849)

                ENDMACRO24_tree = self._adaptor.createWithPayload(ENDMACRO24)
                self._adaptor.addChild(root_0, ENDMACRO24_tree)

                #action start
                self.leave_macro()
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

    # $ANTLR end "macro"

    class sig_expression_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.text = None
            self.tree = None




    # $ANTLR start "sig_expression"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:269:1: sig_expression returns [text] : exp1= sig_exp ( DEFAULT exp2= sig_exp )* ;
    def sig_expression(self, ):

        retval = self.sig_expression_return()
        retval.start = self.input.LT(1)

        root_0 = None

        DEFAULT25 = None
        exp1 = None

        exp2 = None


        DEFAULT25_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:270:9: (exp1= sig_exp ( DEFAULT exp2= sig_exp )* )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:270:11: exp1= sig_exp ( DEFAULT exp2= sig_exp )*
                pass
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_sig_exp_in_sig_expression923)
                exp1 = self.sig_exp()

                self._state.following.pop()
                self._adaptor.addChild(root_0, exp1.tree)
                #action start
                retval.text = ((exp1 is not None) and [exp1.text] or [None])[0]
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:271:11: ( DEFAULT exp2= sig_exp )*
                while True: #loop13
                    alt13 = 2
                    LA13_0 = self.input.LA(1)

                    if (LA13_0 == DEFAULT) :
                        alt13 = 1


                    if alt13 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:271:12: DEFAULT exp2= sig_exp
                        pass
                        DEFAULT25=self.match(self.input, DEFAULT, self.FOLLOW_DEFAULT_in_sig_expression939)

                        DEFAULT25_tree = self._adaptor.createWithPayload(DEFAULT25)
                        root_0 = self._adaptor.becomeRoot(DEFAULT25_tree, root_0)

                        self._state.following.append(self.FOLLOW_sig_exp_in_sig_expression944)
                        exp2 = self.sig_exp()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, exp2.tree)
                        #action start
                        retval.text = retval.text + ' default '+ ((exp2 is not None) and [exp2.text] or [None])[0]
                        #action end


                    else:
                        break #loop13





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

    class sig_exp_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.text = None
            self.tree = None




    # $ANTLR start "sig_exp"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:276:1: sig_exp returns [text] : exp1= sig_exp_primary ( WHEN exp2= bool_exp )* ;
    def sig_exp(self, ):

        retval = self.sig_exp_return()
        retval.start = self.input.LT(1)

        root_0 = None

        WHEN26 = None
        exp1 = None

        exp2 = None


        WHEN26_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:277:9: (exp1= sig_exp_primary ( WHEN exp2= bool_exp )* )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:277:12: exp1= sig_exp_primary ( WHEN exp2= bool_exp )*
                pass
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_sig_exp_primary_in_sig_exp1014)
                exp1 = self.sig_exp_primary()

                self._state.following.pop()
                self._adaptor.addChild(root_0, exp1.tree)
                #action start
                retval.text = ((exp1 is not None) and [exp1.text] or [None])[0]
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:278:11: ( WHEN exp2= bool_exp )*
                while True: #loop14
                    alt14 = 2
                    LA14_0 = self.input.LA(1)

                    if (LA14_0 == WHEN) :
                        alt14 = 1


                    if alt14 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:278:12: WHEN exp2= bool_exp
                        pass
                        WHEN26=self.match(self.input, WHEN, self.FOLLOW_WHEN_in_sig_exp1029)

                        WHEN26_tree = self._adaptor.createWithPayload(WHEN26)
                        root_0 = self._adaptor.becomeRoot(WHEN26_tree, root_0)

                        self._state.following.append(self.FOLLOW_bool_exp_in_sig_exp1034)
                        exp2 = self.bool_exp()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, exp2.tree)
                        #action start
                        retval.text = retval.text + ' when '+ ((exp2 is not None) and [exp2.text] or [None])[0]
                        #action end


                    else:
                        break #loop14





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

    class sig_exp_primary_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.text = None
            self.tree = None




    # $ANTLR start "sig_exp_primary"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:283:1: sig_exp_primary returns [text] : (id= IDENT | LP se= sig_expression RP );
    def sig_exp_primary(self, ):

        retval = self.sig_exp_primary_return()
        retval.start = self.input.LT(1)

        root_0 = None

        id = None
        LP27 = None
        RP28 = None
        se = None


        id_tree = None
        LP27_tree = None
        RP28_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:284:9: (id= IDENT | LP se= sig_expression RP )
                alt15 = 2
                LA15_0 = self.input.LA(1)

                if (LA15_0 == IDENT) :
                    alt15 = 1
                elif (LA15_0 == LP) :
                    alt15 = 2
                else:
                    nvae = NoViableAltException("", 15, 0, self.input)

                    raise nvae

                if alt15 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:284:11: id= IDENT
                    pass
                    root_0 = self._adaptor.nil()

                    id=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_sig_exp_primary1101)

                    id_tree = self._adaptor.createWithPayload(id)
                    self._adaptor.addChild(root_0, id_tree)

                    #action start
                    retval.text = id.text
                    #action end


                elif alt15 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:286:11: LP se= sig_expression RP
                    pass
                    root_0 = self._adaptor.nil()

                    LP27=self.match(self.input, LP, self.FOLLOW_LP_in_sig_exp_primary1125)

                    LP27_tree = self._adaptor.createWithPayload(LP27)
                    self._adaptor.addChild(root_0, LP27_tree)

                    self._state.following.append(self.FOLLOW_sig_expression_in_sig_exp_primary1129)
                    se = self.sig_expression()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, se.tree)
                    RP28=self.match(self.input, RP, self.FOLLOW_RP_in_sig_exp_primary1131)

                    RP28_tree = self._adaptor.createWithPayload(RP28)
                    self._adaptor.addChild(root_0, RP28_tree)

                    #action start
                    retval.text = '('+((se is not None) and [se.text] or [None])[0]+')'
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

    # $ANTLR end "sig_exp_primary"

    class bool_exp_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.text = None
            self.tree = None




    # $ANTLR start "bool_exp"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:290:1: bool_exp returns [text] : (b1= bool_and ( OR b2= bool_and )* | );
    def bool_exp(self, ):

        retval = self.bool_exp_return()
        retval.start = self.input.LT(1)

        root_0 = None

        OR29 = None
        b1 = None

        b2 = None


        OR29_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:291:12: (b1= bool_and ( OR b2= bool_and )* | )
                alt17 = 2
                LA17_0 = self.input.LA(1)

                if (LA17_0 == IDENT or LA17_0 == LP or (NOT <= LA17_0 <= F)) :
                    alt17 = 1
                elif ((LB <= LA17_0 <= RB) or (DEFAULT <= LA17_0 <= WHEN) or LA17_0 == RP or LA17_0 == COM) :
                    alt17 = 2
                else:
                    nvae = NoViableAltException("", 17, 0, self.input)

                    raise nvae

                if alt17 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:292:13: b1= bool_and ( OR b2= bool_and )*
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_bool_and_in_bool_exp1225)
                    b1 = self.bool_and()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, b1.tree)
                    #action start
                    retval.text = ((b1 is not None) and [b1.text] or [None])[0]
                    #action end
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:293:13: ( OR b2= bool_and )*
                    while True: #loop16
                        alt16 = 2
                        LA16_0 = self.input.LA(1)

                        if (LA16_0 == OR) :
                            alt16 = 1


                        if alt16 == 1:
                            # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:293:14: OR b2= bool_and
                            pass
                            OR29=self.match(self.input, OR, self.FOLLOW_OR_in_bool_exp1242)

                            OR29_tree = self._adaptor.createWithPayload(OR29)
                            self._adaptor.addChild(root_0, OR29_tree)

                            self._state.following.append(self.FOLLOW_bool_and_in_bool_exp1246)
                            b2 = self.bool_and()

                            self._state.following.pop()
                            self._adaptor.addChild(root_0, b2.tree)
                            #action start
                            retval.text = retval.text + ' '+'or '+((b2 is not None) and [b2.text] or [None])[0]
                            #action end


                        else:
                            break #loop16




                elif alt17 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:294:14:
                    pass
                    root_0 = self._adaptor.nil()

                    #action start
                    retval.text = ""
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

    # $ANTLR end "bool_exp"

    class bool_and_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.text = None
            self.tree = None




    # $ANTLR start "bool_and"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:297:1: bool_and returns [text] : b1= bool_primary ( AND b2= bool_primary )* ;
    def bool_and(self, ):

        retval = self.bool_and_return()
        retval.start = self.input.LT(1)

        root_0 = None

        AND30 = None
        b1 = None

        b2 = None


        AND30_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:298:12: (b1= bool_primary ( AND b2= bool_primary )* )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:298:14: b1= bool_primary ( AND b2= bool_primary )*
                pass
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_bool_primary_in_bool_and1311)
                b1 = self.bool_primary()

                self._state.following.pop()
                self._adaptor.addChild(root_0, b1.tree)
                #action start
                retval.text = ((b1 is not None) and [b1.text] or [None])[0]
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:299:13: ( AND b2= bool_primary )*
                while True: #loop18
                    alt18 = 2
                    LA18_0 = self.input.LA(1)

                    if (LA18_0 == AND) :
                        alt18 = 1


                    if alt18 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:299:14: AND b2= bool_primary
                        pass
                        AND30=self.match(self.input, AND, self.FOLLOW_AND_in_bool_and1328)

                        AND30_tree = self._adaptor.createWithPayload(AND30)
                        self._adaptor.addChild(root_0, AND30_tree)

                        self._state.following.append(self.FOLLOW_bool_primary_in_bool_and1332)
                        b2 = self.bool_primary()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, b2.tree)
                        #action start
                        retval.text = retval.text + ' '+'and '+((b2 is not None) and [b2.text] or [None])[0]
                        #action end


                    else:
                        break #loop18





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

    # $ANTLR end "bool_and"

    class bool_primary_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.text = None
            self.tree = None




    # $ANTLR start "bool_primary"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:302:1: bool_primary returns [text] : ( NOT b1= bool_primary | b2= bool_constant | id= IDENT | LP b3= bool_exp RP );
    def bool_primary(self, ):

        retval = self.bool_primary_return()
        retval.start = self.input.LT(1)

        root_0 = None

        id = None
        NOT31 = None
        LP32 = None
        RP33 = None
        b1 = None

        b2 = None

        b3 = None


        id_tree = None
        NOT31_tree = None
        LP32_tree = None
        RP33_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:303:12: ( NOT b1= bool_primary | b2= bool_constant | id= IDENT | LP b3= bool_exp RP )
                alt19 = 4
                LA19 = self.input.LA(1)
                if LA19 == NOT:
                    alt19 = 1
                elif LA19 == T or LA19 == F:
                    alt19 = 2
                elif LA19 == IDENT:
                    alt19 = 3
                elif LA19 == LP:
                    alt19 = 4
                else:
                    nvae = NoViableAltException("", 19, 0, self.input)

                    raise nvae

                if alt19 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:303:14: NOT b1= bool_primary
                    pass
                    root_0 = self._adaptor.nil()

                    NOT31=self.match(self.input, NOT, self.FOLLOW_NOT_in_bool_primary1379)

                    NOT31_tree = self._adaptor.createWithPayload(NOT31)
                    self._adaptor.addChild(root_0, NOT31_tree)

                    self._state.following.append(self.FOLLOW_bool_primary_in_bool_primary1383)
                    b1 = self.bool_primary()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, b1.tree)
                    #action start
                    retval.text = 'not '+((b1 is not None) and [b1.text] or [None])[0]
                    #action end


                elif alt19 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:305:14: b2= bool_constant
                    pass
                    root_0 = self._adaptor.nil()

                    self._state.following.append(self.FOLLOW_bool_constant_in_bool_primary1415)
                    b2 = self.bool_constant()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, b2.tree)
                    #action start
                    retval.text = ((b2 is not None) and [b2.text] or [None])[0]
                    #action end


                elif alt19 == 3:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:307:14: id= IDENT
                    pass
                    root_0 = self._adaptor.nil()

                    id=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_bool_primary1438)

                    id_tree = self._adaptor.createWithPayload(id)
                    self._adaptor.addChild(root_0, id_tree)

                    #action start
                    retval.text = id.text
                    #action end


                elif alt19 == 4:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:309:14: LP b3= bool_exp RP
                    pass
                    root_0 = self._adaptor.nil()

                    LP32=self.match(self.input, LP, self.FOLLOW_LP_in_bool_primary1470)

                    LP32_tree = self._adaptor.createWithPayload(LP32)
                    self._adaptor.addChild(root_0, LP32_tree)

                    self._state.following.append(self.FOLLOW_bool_exp_in_bool_primary1474)
                    b3 = self.bool_exp()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, b3.tree)
                    RP33=self.match(self.input, RP, self.FOLLOW_RP_in_bool_primary1476)

                    RP33_tree = self._adaptor.createWithPayload(RP33)
                    self._adaptor.addChild(root_0, RP33_tree)

                    #action start
                    retval.text = '('+((b3 is not None) and [b3.text] or [None])[0]+')'
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

    # $ANTLR end "bool_primary"

    class bool_constant_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.text = None
            self.tree = None




    # $ANTLR start "bool_constant"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:313:1: bool_constant returns [text] : ( T | F );
    def bool_constant(self, ):

        retval = self.bool_constant_return()
        retval.start = self.input.LT(1)

        root_0 = None

        T34 = None
        F35 = None

        T34_tree = None
        F35_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:314:12: ( T | F )
                alt20 = 2
                LA20_0 = self.input.LA(1)

                if (LA20_0 == T) :
                    alt20 = 1
                elif (LA20_0 == F) :
                    alt20 = 2
                else:
                    nvae = NoViableAltException("", 20, 0, self.input)

                    raise nvae

                if alt20 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:314:14: T
                    pass
                    root_0 = self._adaptor.nil()

                    T34=self.match(self.input, T, self.FOLLOW_T_in_bool_constant1514)

                    T34_tree = self._adaptor.createWithPayload(T34)
                    self._adaptor.addChild(root_0, T34_tree)

                    #action start
                    retval.text = 'true'
                    #action end


                elif alt20 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:315:14: F
                    pass
                    root_0 = self._adaptor.nil()

                    F35=self.match(self.input, F, self.FOLLOW_F_in_bool_constant1532)

                    F35_tree = self._adaptor.createWithPayload(F35)
                    self._adaptor.addChild(root_0, F35_tree)

                    #action start
                    retval.text = 'false'
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

    # $ANTLR end "bool_constant"

    class constraints_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.text = None
            self.tree = None




    # $ANTLR start "constraints"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:318:1: constraints returns [text] : CONST t1= const_exp (t2= const_exp )* ENDCONST ;
    def constraints(self, ):

        retval = self.constraints_return()
        retval.start = self.input.LT(1)

        root_0 = None

        CONST36 = None
        ENDCONST37 = None
        t1 = None

        t2 = None


        CONST36_tree = None
        ENDCONST37_tree = None


        SEP = ';'

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:322:12: ( CONST t1= const_exp (t2= const_exp )* ENDCONST )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:322:14: CONST t1= const_exp (t2= const_exp )* ENDCONST
                pass
                root_0 = self._adaptor.nil()

                CONST36=self.match(self.input, CONST, self.FOLLOW_CONST_in_constraints1595)

                CONST36_tree = self._adaptor.createWithPayload(CONST36)
                self._adaptor.addChild(root_0, CONST36_tree)

                self._state.following.append(self.FOLLOW_const_exp_in_constraints1599)
                t1 = self.const_exp()

                self._state.following.pop()
                self._adaptor.addChild(root_0, t1.tree)
                #action start
                retval.text = ((t1 is not None) and [t1.text] or [None])[0]+SEP
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:323:14: (t2= const_exp )*
                while True: #loop21
                    alt21 = 2
                    LA21_0 = self.input.LA(1)

                    if ((SYNC <= LA21_0 <= INC)) :
                        alt21 = 1


                    if alt21 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:323:15: t2= const_exp
                        pass
                        self._state.following.append(self.FOLLOW_const_exp_in_constraints1619)
                        t2 = self.const_exp()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, t2.tree)
                        #action start
                        retval.text = retval.text+'\n'+((t2 is not None) and [t2.text] or [None])[0]+SEP
                        #action end


                    else:
                        break #loop21


                ENDCONST37=self.match(self.input, ENDCONST, self.FOLLOW_ENDCONST_in_constraints1625)

                ENDCONST37_tree = self._adaptor.createWithPayload(ENDCONST37)
                self._adaptor.addChild(root_0, ENDCONST37_tree)




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

    # $ANTLR end "constraints"

    class const_exp_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.text = None
            self.tree = None




    # $ANTLR start "const_exp"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:326:1: const_exp returns [text] : ( SYNC LP t1= exp_list RP | EXCL LP t2= exp_list RP | INC LP t3= sig_expression COM t4= sig_expression RP );
    def const_exp(self, ):

        retval = self.const_exp_return()
        retval.start = self.input.LT(1)

        root_0 = None

        SYNC38 = None
        LP39 = None
        RP40 = None
        EXCL41 = None
        LP42 = None
        RP43 = None
        INC44 = None
        LP45 = None
        COM46 = None
        RP47 = None
        t1 = None

        t2 = None

        t3 = None

        t4 = None


        SYNC38_tree = None
        LP39_tree = None
        RP40_tree = None
        EXCL41_tree = None
        LP42_tree = None
        RP43_tree = None
        INC44_tree = None
        LP45_tree = None
        COM46_tree = None
        RP47_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:327:12: ( SYNC LP t1= exp_list RP | EXCL LP t2= exp_list RP | INC LP t3= sig_expression COM t4= sig_expression RP )
                alt22 = 3
                LA22 = self.input.LA(1)
                if LA22 == SYNC:
                    alt22 = 1
                elif LA22 == EXCL:
                    alt22 = 2
                elif LA22 == INC:
                    alt22 = 3
                else:
                    nvae = NoViableAltException("", 22, 0, self.input)

                    raise nvae

                if alt22 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:327:14: SYNC LP t1= exp_list RP
                    pass
                    root_0 = self._adaptor.nil()

                    SYNC38=self.match(self.input, SYNC, self.FOLLOW_SYNC_in_const_exp1669)

                    SYNC38_tree = self._adaptor.createWithPayload(SYNC38)
                    self._adaptor.addChild(root_0, SYNC38_tree)

                    LP39=self.match(self.input, LP, self.FOLLOW_LP_in_const_exp1671)

                    LP39_tree = self._adaptor.createWithPayload(LP39)
                    self._adaptor.addChild(root_0, LP39_tree)

                    self._state.following.append(self.FOLLOW_exp_list_in_const_exp1675)
                    t1 = self.exp_list()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, t1.tree)
                    RP40=self.match(self.input, RP, self.FOLLOW_RP_in_const_exp1677)

                    RP40_tree = self._adaptor.createWithPayload(RP40)
                    self._adaptor.addChild(root_0, RP40_tree)

                    #action start
                    retval.text = 'synchro('+((t1 is not None) and [t1.text] or [None])[0]+')'
                    #action end


                elif alt22 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:329:14: EXCL LP t2= exp_list RP
                    pass
                    root_0 = self._adaptor.nil()

                    EXCL41=self.match(self.input, EXCL, self.FOLLOW_EXCL_in_const_exp1707)

                    EXCL41_tree = self._adaptor.createWithPayload(EXCL41)
                    self._adaptor.addChild(root_0, EXCL41_tree)

                    LP42=self.match(self.input, LP, self.FOLLOW_LP_in_const_exp1709)

                    LP42_tree = self._adaptor.createWithPayload(LP42)
                    self._adaptor.addChild(root_0, LP42_tree)

                    self._state.following.append(self.FOLLOW_exp_list_in_const_exp1713)
                    t2 = self.exp_list()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, t2.tree)
                    RP43=self.match(self.input, RP, self.FOLLOW_RP_in_const_exp1715)

                    RP43_tree = self._adaptor.createWithPayload(RP43)
                    self._adaptor.addChild(root_0, RP43_tree)

                    #action start
                    retval.text = 'exclus('+((t2 is not None) and [t2.text] or [None])[0]+')'
                    #action end


                elif alt22 == 3:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:331:14: INC LP t3= sig_expression COM t4= sig_expression RP
                    pass
                    root_0 = self._adaptor.nil()

                    INC44=self.match(self.input, INC, self.FOLLOW_INC_in_const_exp1745)

                    INC44_tree = self._adaptor.createWithPayload(INC44)
                    self._adaptor.addChild(root_0, INC44_tree)

                    LP45=self.match(self.input, LP, self.FOLLOW_LP_in_const_exp1747)

                    LP45_tree = self._adaptor.createWithPayload(LP45)
                    self._adaptor.addChild(root_0, LP45_tree)

                    self._state.following.append(self.FOLLOW_sig_expression_in_const_exp1751)
                    t3 = self.sig_expression()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, t3.tree)
                    COM46=self.match(self.input, COM, self.FOLLOW_COM_in_const_exp1753)

                    COM46_tree = self._adaptor.createWithPayload(COM46)
                    self._adaptor.addChild(root_0, COM46_tree)

                    self._state.following.append(self.FOLLOW_sig_expression_in_const_exp1757)
                    t4 = self.sig_expression()

                    self._state.following.pop()
                    self._adaptor.addChild(root_0, t4.tree)
                    RP47=self.match(self.input, RP, self.FOLLOW_RP_in_const_exp1759)

                    RP47_tree = self._adaptor.createWithPayload(RP47)
                    self._adaptor.addChild(root_0, RP47_tree)

                    #action start
                    retval.text = 'included('+((t3 is not None) and [t3.text] or [None])[0]+', '+ ((t4 is not None) and [t4.text] or [None])[0]+')'
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

    # $ANTLR end "const_exp"

    class exp_list_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.text = None
            self.tree = None




    # $ANTLR start "exp_list"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:335:1: exp_list returns [text] : t1= sig_expression ( COM t2= sig_expression )* ;
    def exp_list(self, ):

        retval = self.exp_list_return()
        retval.start = self.input.LT(1)

        root_0 = None

        COM48 = None
        t1 = None

        t2 = None


        COM48_tree = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:336:12: (t1= sig_expression ( COM t2= sig_expression )* )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:336:14: t1= sig_expression ( COM t2= sig_expression )*
                pass
                root_0 = self._adaptor.nil()

                self._state.following.append(self.FOLLOW_sig_expression_in_exp_list1823)
                t1 = self.sig_expression()

                self._state.following.pop()
                self._adaptor.addChild(root_0, t1.tree)
                #action start
                retval.text = ((t1 is not None) and [t1.text] or [None])[0]
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:337:12: ( COM t2= sig_expression )*
                while True: #loop23
                    alt23 = 2
                    LA23_0 = self.input.LA(1)

                    if (LA23_0 == COM) :
                        alt23 = 1


                    if alt23 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/cadlang.g:337:13: COM t2= sig_expression
                        pass
                        COM48=self.match(self.input, COM, self.FOLLOW_COM_in_exp_list1839)

                        COM48_tree = self._adaptor.createWithPayload(COM48)
                        self._adaptor.addChild(root_0, COM48_tree)

                        self._state.following.append(self.FOLLOW_sig_expression_in_exp_list1843)
                        t2 = self.sig_expression()

                        self._state.following.pop()
                        self._adaptor.addChild(root_0, t2.tree)
                        #action start
                        retval.text = retval.text +', '+((t2 is not None) and [t2.text] or [None])[0]
                        #action end


                    else:
                        break #loop23





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




    FOLLOW_NAME_in_cad_model139 = frozenset([5])
    FOLLOW_IDENT_in_cad_model143 = frozenset([5, 7, 13])
    FOLLOW_macro_in_cad_model162 = frozenset([5, 7, 13, 24])
    FOLLOW_transition_in_cad_model164 = frozenset([5, 7, 13, 24])
    FOLLOW_dec_in_cad_model166 = frozenset([5, 7, 13, 24])
    FOLLOW_constraints_in_cad_model203 = frozenset([])
    FOLLOW_EOF_in_cad_model222 = frozenset([1])
    FOLLOW_IDENT_in_dec270 = frozenset([6, 8, 9])
    FOLLOW_modifier_in_dec275 = frozenset([6])
    FOLLOW_SC_in_dec281 = frozenset([1])
    FOLLOW_IDENT_in_transition340 = frozenset([7, 8, 9])
    FOLLOW_modifier_in_transition345 = frozenset([7])
    FOLLOW_TARROW_in_transition349 = frozenset([5])
    FOLLOW_IDENT_in_transition353 = frozenset([6])
    FOLLOW_SC_in_transition355 = frozenset([5, 10, 17])
    FOLLOW_guard_in_transition359 = frozenset([6, 8, 9, 12])
    FOLLOW_modifier_in_transition364 = frozenset([6, 12])
    FOLLOW_note_in_transition370 = frozenset([6])
    FOLLOW_SC_in_transition372 = frozenset([1])
    FOLLOW_IDENT_in_transition416 = frozenset([7])
    FOLLOW_TARROW_in_transition418 = frozenset([6])
    FOLLOW_SC_in_transition421 = frozenset([5, 10, 17])
    FOLLOW_guard_in_transition425 = frozenset([6, 12])
    FOLLOW_note_in_transition429 = frozenset([6])
    FOLLOW_SC_in_transition431 = frozenset([1])
    FOLLOW_TARROW_in_transition474 = frozenset([5])
    FOLLOW_IDENT_in_transition478 = frozenset([6])
    FOLLOW_SC_in_transition481 = frozenset([1, 6, 12])
    FOLLOW_note_in_transition486 = frozenset([6])
    FOLLOW_SC_in_transition488 = frozenset([1])
    FOLLOW_set_in_modifier0 = frozenset([1])
    FOLLOW_sig_expression_in_guard634 = frozenset([10])
    FOLLOW_LB_in_guard638 = frozenset([5, 11, 17, 21, 22, 23])
    FOLLOW_bool_exp_in_guard643 = frozenset([11])
    FOLLOW_RB_in_guard646 = frozenset([1, 5])
    FOLLOW_IDENT_in_guard651 = frozenset([1])
    FOLLOW_TEXT_in_note717 = frozenset([1])
    FOLLOW_MACRO_in_macro795 = frozenset([5])
    FOLLOW_IDENT_in_macro799 = frozenset([5, 7, 13, 14])
    FOLLOW_macro_in_macro829 = frozenset([5, 7, 13, 14])
    FOLLOW_transition_in_macro831 = frozenset([5, 7, 13, 14])
    FOLLOW_dec_in_macro833 = frozenset([5, 7, 13, 14])
    FOLLOW_ENDMACRO_in_macro849 = frozenset([1])
    FOLLOW_sig_exp_in_sig_expression923 = frozenset([1, 15])
    FOLLOW_DEFAULT_in_sig_expression939 = frozenset([5, 17])
    FOLLOW_sig_exp_in_sig_expression944 = frozenset([1, 15])
    FOLLOW_sig_exp_primary_in_sig_exp1014 = frozenset([1, 16])
    FOLLOW_WHEN_in_sig_exp1029 = frozenset([5, 16, 17, 21, 22, 23])
    FOLLOW_bool_exp_in_sig_exp1034 = frozenset([1, 16])
    FOLLOW_IDENT_in_sig_exp_primary1101 = frozenset([1])
    FOLLOW_LP_in_sig_exp_primary1125 = frozenset([5, 17])
    FOLLOW_sig_expression_in_sig_exp_primary1129 = frozenset([18])
    FOLLOW_RP_in_sig_exp_primary1131 = frozenset([1])
    FOLLOW_bool_and_in_bool_exp1225 = frozenset([1, 19])
    FOLLOW_OR_in_bool_exp1242 = frozenset([5, 17, 21, 22, 23])
    FOLLOW_bool_and_in_bool_exp1246 = frozenset([1, 19])
    FOLLOW_bool_primary_in_bool_and1311 = frozenset([1, 20])
    FOLLOW_AND_in_bool_and1328 = frozenset([5, 17, 21, 22, 23])
    FOLLOW_bool_primary_in_bool_and1332 = frozenset([1, 20])
    FOLLOW_NOT_in_bool_primary1379 = frozenset([5, 17, 21, 22, 23])
    FOLLOW_bool_primary_in_bool_primary1383 = frozenset([1])
    FOLLOW_bool_constant_in_bool_primary1415 = frozenset([1])
    FOLLOW_IDENT_in_bool_primary1438 = frozenset([1])
    FOLLOW_LP_in_bool_primary1470 = frozenset([5, 17, 18, 21, 22, 23])
    FOLLOW_bool_exp_in_bool_primary1474 = frozenset([18])
    FOLLOW_RP_in_bool_primary1476 = frozenset([1])
    FOLLOW_T_in_bool_constant1514 = frozenset([1])
    FOLLOW_F_in_bool_constant1532 = frozenset([1])
    FOLLOW_CONST_in_constraints1595 = frozenset([26, 27, 28])
    FOLLOW_const_exp_in_constraints1599 = frozenset([25, 26, 27, 28])
    FOLLOW_const_exp_in_constraints1619 = frozenset([25, 26, 27, 28])
    FOLLOW_ENDCONST_in_constraints1625 = frozenset([1])
    FOLLOW_SYNC_in_const_exp1669 = frozenset([17])
    FOLLOW_LP_in_const_exp1671 = frozenset([5, 17])
    FOLLOW_exp_list_in_const_exp1675 = frozenset([18])
    FOLLOW_RP_in_const_exp1677 = frozenset([1])
    FOLLOW_EXCL_in_const_exp1707 = frozenset([17])
    FOLLOW_LP_in_const_exp1709 = frozenset([5, 17])
    FOLLOW_exp_list_in_const_exp1713 = frozenset([18])
    FOLLOW_RP_in_const_exp1715 = frozenset([1])
    FOLLOW_INC_in_const_exp1745 = frozenset([17])
    FOLLOW_LP_in_const_exp1747 = frozenset([5, 17])
    FOLLOW_sig_expression_in_const_exp1751 = frozenset([29])
    FOLLOW_COM_in_const_exp1753 = frozenset([5, 17])
    FOLLOW_sig_expression_in_const_exp1757 = frozenset([18])
    FOLLOW_RP_in_const_exp1759 = frozenset([1])
    FOLLOW_sig_expression_in_exp_list1823 = frozenset([1, 29])
    FOLLOW_COM_in_exp_list1839 = frozenset([5, 17])
    FOLLOW_sig_expression_in_exp_list1843 = frozenset([1, 29])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("cadlangLexer", cadlangParser)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)

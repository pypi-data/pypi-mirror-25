# $ANTLR 3.1.2 /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g 2012-09-11 14:55:44

import sys
from cadbiom.antlr3 import *
from cadbiom.antlr3.compat import set, frozenset

from cadbiom.models.guard_transitions.chart_model import ChartModel



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

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>",
    "PROC", "IDENT", "INT", "ARROW", "COOP", "LP", "COM", "RP", "IN_KW",
    "LB", "SC", "RB", "AND", "OR", "NOT", "WS", "COMMENT", "LETTER", "DIGIT"
]




class pintlangParser(Parser):
    grammarFileName = "/home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g"
    antlr_version = version_str_to_tuple("3.1.2")
    antlr_version_str = "3.1.2"
    tokenNames = tokenNames

    def __init__(self, input, state=None):
        if state is None:
            state = RecognizerSharedState()

        Parser.__init__(self, input, state)













    def set_error_reporter(self, err):
        self.error_reporter = err

    def displayRecognitionError(self, tokenNames, re):
        hdr = self.getErrorHeader(re)
        msg = self.getErrorMessage(re, tokenNames)
        self.error_reporter.display(hdr,msg)


    def displayExceptionMessage(self, e):
        msg = self.getErrorMessage(self, e, tokenNames)
        self.error_reporter.display('',msg)

    def check_process(self, name, level, line):
        line_txt = 'line '+str(line)+':'
        try:
            lev = self.symb_tab[name]
            self.error_reporter.display(line_txt, "Process double declaration: "+id)

        except KeyError:
            self.symb_tab[name] = level
            for ii in range(level+1):
                pname = name + '_' + str(ii)
                self.model.get_root().add_simple_node(pname, 0.0, 0.0)

    def check_action(self, fname, flevel, cname, clevel1, clevel2, line):
        line_txt = 'line '+str(line)+':'
        try:
            lev = self.symb_tab[fname]
            if flevel>lev:
                self.error_reporter(line_txt, "Incorrect level for:"+fname)
                return
        except KeyError:
            self.error_reporter.display(line_txt, "Undeclared process: "+fname)
            return
        try:
            lev = self.symb_tab[cname]
            if clevel1>lev or clevel2>lev:
                self.error_reporter(line_txt, "Incorrect level for:"+cname)
                return
        except KeyError:
            self.error_reporter.display(line_txt, "Undeclared process: "+cname)
            return

        n1 = self.model.get_simple_node(cname+'_'+str(clevel1))
        n2 = self.model.get_simple_node(cname+'_'+str(clevel2))
        tr=self.model.get_root().add_transition(n1, n2)
        tr.set_condition(fname+'_'+str(flevel))
        h_name = 'hh_'+str(self.clock_cpt)
        self.clock_cpt +=1
        tr.set_event(h_name)
        self.clock_list.append(h_name)
        return

    def check_transition(self, cname, clevel1, clevel2, line):
        line_txt = 'line '+str(line)+':'
        try:
            lev = self.symb_tab[cname]
            if clevel1>lev or clevel2>lev:
                self.error_reporter(line_txt, "Incorrect level for:"+cname)
                return
        except KeyError:
            self.error_reporter.display(line_txt, "Undeclared process: "+cname)
            return

        n1 = self.model.get_simple_node(cname+'_'+str(clevel1))
        n2 = self.model.get_simple_node(cname+'_'+str(clevel2))
        tr=self.model.get_root().add_transition(n1, n2)
        return tr

    def check_tt_rhs(self, tr, il ,l_cond):
        line_txt = 'line '+'? :'
        cond = self.tt_translate_lcond(il, l_cond, line_txt)
        tr.set_condition(cond)
        h_name = 'hh_'+str(self.clock_cpt)
        self.clock_cpt +=1
        tr.set_event(h_name)
        self.clock_list.append(h_name)

    def check_tr_rhs(self, cond, cname, clevel1, clevel2, line):
        line_txt = 'line '+str(line)+':'
        try:
            lev = self.symb_tab[cname]
            if clevel1>lev or clevel2>lev:
                self.error_reporter(line_txt, "Incorrect level for:"+cname)
                return
        except KeyError:
            self.error_reporter.display(line_txt, "Undeclared process: "+cname)
            return

        n1 = self.model.get_simple_node(cname+'_'+str(clevel1))
        n2 = self.model.get_simple_node(cname+'_'+str(clevel2))
        tr=self.model.get_root().add_transition(n1, n2)
        tr.set_condition(cond)
        h_name = 'hh_'+str(self.clock_cpt)
        self.clock_cpt +=1
        tr.set_event(h_name)
        self.clock_list.append(h_name)


    def tt_translate_cond(self, id_list, val_list, line_txt):
        if len(id_list) != len(val_list):
            self.error_reporter.display(line_txt, "Bad condition specification"+id_list.__str__())
            return None
        cond = id_list[0] + "_"+str(val_list[0])
        for i in range(1, len(id_list)):
            cond_el = id_list[i] + "_" + str(val_list[i])
            cond = cond + " and "+ cond_el
        return cond


    def tt_translate_lcond(self, id_list, lval_list, line_txt):
        cond_el = self.tt_translate_cond(id_list, lval_list[0], line_txt)
        if cond_el:
            cond = '(' + cond_el + ')'
        else:
            return ""
        for i in range(1,len(lval_list)):
            cond_el = self.tt_translate_cond(id_list, lval_list[i], line_txt)
            if cond_el:
                cond = cond + ' or (' + cond_el + ')'
            else:
                return ""
        return cond





    # $ANTLR start "pintspec"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:158:1: pintspec[model_name] : ( process | action | cooper )* EOF ;
    def pintspec(self, model_name):


        self.model = ChartModel(model_name)
        self.symb_tab = dict()
        self.clock_cpt = 0
        self.clock_list = []
        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:163:12: ( ( process | action | cooper )* EOF )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:163:14: ( process | action | cooper )* EOF
                pass
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:163:14: ( process | action | cooper )*
                while True: #loop1
                    alt1 = 4
                    LA1 = self.input.LA(1)
                    if LA1 == PROC:
                        alt1 = 1
                    elif LA1 == IDENT:
                        alt1 = 2
                    elif LA1 == COOP:
                        alt1 = 3

                    if alt1 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:163:15: process
                        pass
                        self._state.following.append(self.FOLLOW_process_in_pintspec72)
                        self.process()

                        self._state.following.pop()


                    elif alt1 == 2:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:163:23: action
                        pass
                        self._state.following.append(self.FOLLOW_action_in_pintspec74)
                        self.action()

                        self._state.following.pop()


                    elif alt1 == 3:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:163:30: cooper
                        pass
                        self._state.following.append(self.FOLLOW_cooper_in_pintspec76)
                        self.cooper()

                        self._state.following.pop()


                    else:
                        break #loop1


                self.match(self.input, EOF, self.FOLLOW_EOF_in_pintspec81)




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "pintspec"


    # $ANTLR start "process"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:166:1: process : PROC id= IDENT i= INT ;
    def process(self, ):

        id = None
        i = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:167:12: ( PROC id= IDENT i= INT )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:167:14: PROC id= IDENT i= INT
                pass
                self.match(self.input, PROC, self.FOLLOW_PROC_in_process123)
                id=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_process127)
                i=self.match(self.input, INT, self.FOLLOW_INT_in_process132)
                #action start
                self.check_process(id.text, int(i.text), id.line)
                #action end




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "process"


    # $ANTLR start "action"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:171:1: action : fid= IDENT flev= INT ARROW cid= IDENT lev1= INT lev2= INT ;
    def action(self, ):

        fid = None
        flev = None
        cid = None
        lev1 = None
        lev2 = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:172:12: (fid= IDENT flev= INT ARROW cid= IDENT lev1= INT lev2= INT )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:172:14: fid= IDENT flev= INT ARROW cid= IDENT lev1= INT lev2= INT
                pass
                fid=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_action194)
                flev=self.match(self.input, INT, self.FOLLOW_INT_in_action198)
                self.match(self.input, ARROW, self.FOLLOW_ARROW_in_action200)
                cid=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_action204)
                lev1=self.match(self.input, INT, self.FOLLOW_INT_in_action208)
                lev2=self.match(self.input, INT, self.FOLLOW_INT_in_action212)
                #action start
                self.check_action(fid.text, int(flev.text), cid.text, int(lev1.text), int(lev2.text), fid.line)
                #action end




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "action"


    # $ANTLR start "cooper"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:176:1: cooper : COOP LP lha= coop_lhs COM coop_rhs[$lha.transition, $lha.id_list, $lha.condition] RP ;
    def cooper(self, ):

        lha = None


        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:177:12: ( COOP LP lha= coop_lhs COM coop_rhs[$lha.transition, $lha.id_list, $lha.condition] RP )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:177:14: COOP LP lha= coop_lhs COM coop_rhs[$lha.transition, $lha.id_list, $lha.condition] RP
                pass
                self.match(self.input, COOP, self.FOLLOW_COOP_in_cooper275)
                self.match(self.input, LP, self.FOLLOW_LP_in_cooper277)
                self._state.following.append(self.FOLLOW_coop_lhs_in_cooper281)
                lha = self.coop_lhs()

                self._state.following.pop()
                self.match(self.input, COM, self.FOLLOW_COM_in_cooper283)
                self._state.following.append(self.FOLLOW_coop_rhs_in_cooper285)
                self.coop_rhs(((lha is not None) and [lha.transition] or [None])[0], ((lha is not None) and [lha.id_list] or [None])[0], ((lha is not None) and [lha.condition] or [None])[0])

                self._state.following.pop()
                self.match(self.input, RP, self.FOLLOW_RP_in_cooper288)




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "cooper"

    class coop_lhs_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.transition = None
            self.id_list = None
            self.condition = None




    # $ANTLR start "coop_lhs"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:180:1: coop_lhs returns [transition, id_list, condition] : il= sort_list rc= rcoop_lhs[il] ;
    def coop_lhs(self, ):

        retval = self.coop_lhs_return()
        retval.start = self.input.LT(1)

        il = None

        rc = None


        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:181:12: (il= sort_list rc= rcoop_lhs[il] )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:181:14: il= sort_list rc= rcoop_lhs[il]
                pass
                self._state.following.append(self.FOLLOW_sort_list_in_coop_lhs338)
                il = self.sort_list()

                self._state.following.pop()
                #action start
                retval.id_list = il
                #action end
                self._state.following.append(self.FOLLOW_rcoop_lhs_in_coop_lhs372)
                rc = self.rcoop_lhs(il)

                self._state.following.pop()
                #action start
                retval.transition = ((rc is not None) and [rc.transition] or [None])[0]
                retval.condition = ((rc is not None) and [rc.condition] or [None])[0]
                #action end



                retval.stop = self.input.LT(-1)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end "coop_lhs"

    class rcoop_lhs_return(ParserRuleReturnScope):
        def __init__(self):
            ParserRuleReturnScope.__init__(self)

            self.transition = None
            self.condition = None




    # $ANTLR start "rcoop_lhs"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:188:1: rcoop_lhs[ids] returns [transition, condition] : (kw= IN_KW tt= tt_condition cond= tail_logexp | ARROW id= IDENT i1= INT i2= INT );
    def rcoop_lhs(self, ids):

        retval = self.rcoop_lhs_return()
        retval.start = self.input.LT(1)

        kw = None
        id = None
        i1 = None
        i2 = None
        tt = None

        cond = None


        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:189:12: (kw= IN_KW tt= tt_condition cond= tail_logexp | ARROW id= IDENT i1= INT i2= INT )
                alt2 = 2
                LA2_0 = self.input.LA(1)

                if (LA2_0 == IN_KW) :
                    alt2 = 1
                elif (LA2_0 == ARROW) :
                    alt2 = 2
                else:
                    nvae = NoViableAltException("", 2, 0, self.input)

                    raise nvae

                if alt2 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:189:14: kw= IN_KW tt= tt_condition cond= tail_logexp
                    pass
                    kw=self.match(self.input, IN_KW, self.FOLLOW_IN_KW_in_rcoop_lhs438)
                    self._state.following.append(self.FOLLOW_tt_condition_in_rcoop_lhs443)
                    tt = self.tt_condition()

                    self._state.following.pop()
                    self._state.following.append(self.FOLLOW_tail_logexp_in_rcoop_lhs447)
                    cond = self.tail_logexp()

                    self._state.following.pop()
                    #action start
                    retval.condition = self.tt_translate_lcond(ids, tt,  'line '+str(kw.line)+':') + cond
                    #action end


                elif alt2 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:191:14: ARROW id= IDENT i1= INT i2= INT
                    pass
                    self.match(self.input, ARROW, self.FOLLOW_ARROW_in_rcoop_lhs478)
                    id=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_rcoop_lhs482)
                    i1=self.match(self.input, INT, self.FOLLOW_INT_in_rcoop_lhs486)
                    i2=self.match(self.input, INT, self.FOLLOW_INT_in_rcoop_lhs490)
                    #action start
                    retval.transition = self.check_transition(id.text, int(i1.text), int(i2.text), id.line)
                    #action end


                retval.stop = self.input.LT(-1)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end "rcoop_lhs"


    # $ANTLR start "coop_rhs"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:195:1: coop_rhs[tr, il, cond] : (tt= tt_condition | id= IDENT cc= COM i1= INT COM i2= INT );
    def coop_rhs(self, tr, il, cond):

        id = None
        cc = None
        i1 = None
        i2 = None
        tt = None


        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:196:12: (tt= tt_condition | id= IDENT cc= COM i1= INT COM i2= INT )
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if (LA3_0 == LB) :
                    alt3 = 1
                elif (LA3_0 == IDENT) :
                    alt3 = 2
                else:
                    nvae = NoViableAltException("", 3, 0, self.input)

                    raise nvae

                if alt3 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:196:14: tt= tt_condition
                    pass
                    self._state.following.append(self.FOLLOW_tt_condition_in_coop_rhs553)
                    tt = self.tt_condition()

                    self._state.following.pop()
                    #action start
                    self.check_tt_rhs(tr,il, tt, )
                    #action end


                elif alt3 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:198:14: id= IDENT cc= COM i1= INT COM i2= INT
                    pass
                    id=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_coop_rhs584)
                    cc=self.match(self.input, COM, self.FOLLOW_COM_in_coop_rhs588)
                    i1=self.match(self.input, INT, self.FOLLOW_INT_in_coop_rhs592)
                    self.match(self.input, COM, self.FOLLOW_COM_in_coop_rhs595)
                    i2=self.match(self.input, INT, self.FOLLOW_INT_in_coop_rhs599)
                    #action start
                    self.check_tr_rhs(cond, id.text, int(i1.text), int(i2.text), cc.line)
                    #action end



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return

    # $ANTLR end "coop_rhs"


    # $ANTLR start "sort_list"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:202:1: sort_list returns [id_list] : LB id1= IDENT ( SC id2= IDENT )* RB ;
    def sort_list(self, ):

        id_list = None

        id1 = None
        id2 = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:203:12: ( LB id1= IDENT ( SC id2= IDENT )* RB )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:203:14: LB id1= IDENT ( SC id2= IDENT )* RB
                pass
                self.match(self.input, LB, self.FOLLOW_LB_in_sort_list660)
                id1=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_sort_list664)
                #action start
                id_list = [id1.text]
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:205:14: ( SC id2= IDENT )*
                while True: #loop4
                    alt4 = 2
                    LA4_0 = self.input.LA(1)

                    if (LA4_0 == SC) :
                        alt4 = 1


                    if alt4 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:205:15: SC id2= IDENT
                        pass
                        self.match(self.input, SC, self.FOLLOW_SC_in_sort_list699)
                        id2=self.match(self.input, IDENT, self.FOLLOW_IDENT_in_sort_list703)
                        #action start
                        id_list.append(id2.text)
                        #action end


                    else:
                        break #loop4


                self.match(self.input, RB, self.FOLLOW_RB_in_sort_list709)




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return id_list

    # $ANTLR end "sort_list"


    # $ANTLR start "tt_condition"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:208:1: tt_condition returns [l_cond] : LB tt1= tt_conjunction ( SC tt2= tt_conjunction )* RB ;
    def tt_condition(self, ):

        l_cond = None

        tt1 = None

        tt2 = None


        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:209:12: ( LB tt1= tt_conjunction ( SC tt2= tt_conjunction )* RB )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:209:14: LB tt1= tt_conjunction ( SC tt2= tt_conjunction )* RB
                pass
                self.match(self.input, LB, self.FOLLOW_LB_in_tt_condition755)
                self._state.following.append(self.FOLLOW_tt_conjunction_in_tt_condition759)
                tt1 = self.tt_conjunction()

                self._state.following.pop()
                #action start
                l_cond = [tt1]
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:210:14: ( SC tt2= tt_conjunction )*
                while True: #loop5
                    alt5 = 2
                    LA5_0 = self.input.LA(1)

                    if (LA5_0 == SC) :
                        alt5 = 1


                    if alt5 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:210:15: SC tt2= tt_conjunction
                        pass
                        self.match(self.input, SC, self.FOLLOW_SC_in_tt_condition777)
                        self._state.following.append(self.FOLLOW_tt_conjunction_in_tt_condition781)
                        tt2 = self.tt_conjunction()

                        self._state.following.pop()
                        #action start
                        l_cond.append(tt2)
                        #action end


                    else:
                        break #loop5


                self.match(self.input, RB, self.FOLLOW_RB_in_tt_condition788)




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return l_cond

    # $ANTLR end "tt_condition"


    # $ANTLR start "tt_conjunction"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:213:1: tt_conjunction returns [lval] : LB i1= INT ( SC i2= INT )* RB ;
    def tt_conjunction(self, ):

        lval = None

        i1 = None
        i2 = None

        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:214:12: ( LB i1= INT ( SC i2= INT )* RB )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:214:15: LB i1= INT ( SC i2= INT )* RB
                pass
                self.match(self.input, LB, self.FOLLOW_LB_in_tt_conjunction835)
                i1=self.match(self.input, INT, self.FOLLOW_INT_in_tt_conjunction839)
                #action start
                lval = [int(i1.text)]
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:215:15: ( SC i2= INT )*
                while True: #loop6
                    alt6 = 2
                    LA6_0 = self.input.LA(1)

                    if (LA6_0 == SC) :
                        alt6 = 1


                    if alt6 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:215:16: SC i2= INT
                        pass
                        self.match(self.input, SC, self.FOLLOW_SC_in_tt_conjunction858)
                        i2=self.match(self.input, INT, self.FOLLOW_INT_in_tt_conjunction862)
                        #action start
                        lval.append(int(i2.text))
                        #action end


                    else:
                        break #loop6


                self.match(self.input, RB, self.FOLLOW_RB_in_tt_conjunction869)




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return lval

    # $ANTLR end "tt_conjunction"


    # $ANTLR start "tail_logexp"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:218:1: tail_logexp returns [cond] : ( | AND tt1= tt_logexp | OR tt2= tt_logexp | tt_primary );
    def tail_logexp(self, ):

        cond = None

        tt1 = None

        tt2 = None


        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:219:12: ( | AND tt1= tt_logexp | OR tt2= tt_logexp | tt_primary )
                alt7 = 4
                LA7 = self.input.LA(1)
                if LA7 == COM:
                    alt7 = 1
                elif LA7 == AND:
                    alt7 = 2
                elif LA7 == OR:
                    alt7 = 3
                elif LA7 == LP or LA7 == LB or LA7 == NOT:
                    alt7 = 4
                else:
                    nvae = NoViableAltException("", 7, 0, self.input)

                    raise nvae

                if alt7 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:219:14:
                    pass
                    #action start
                    cond = ""
                    #action end


                elif alt7 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:220:14: AND tt1= tt_logexp
                    pass
                    self.match(self.input, AND, self.FOLLOW_AND_in_tail_logexp931)
                    self._state.following.append(self.FOLLOW_tt_logexp_in_tail_logexp935)
                    tt1 = self.tt_logexp()

                    self._state.following.pop()
                    #action start
                    cond = ' and ' + tt1
                    #action end


                elif alt7 == 3:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:222:14: OR tt2= tt_logexp
                    pass
                    self.match(self.input, OR, self.FOLLOW_OR_in_tail_logexp966)
                    self._state.following.append(self.FOLLOW_tt_logexp_in_tail_logexp971)
                    tt2 = self.tt_logexp()

                    self._state.following.pop()
                    #action start
                    cond = ' and ' + tt1
                    #action end


                elif alt7 == 4:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:224:14: tt_primary
                    pass
                    self._state.following.append(self.FOLLOW_tt_primary_in_tail_logexp1002)
                    self.tt_primary()

                    self._state.following.pop()
                    #action start
                    cond = tt1
                    #action end



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return cond

    # $ANTLR end "tail_logexp"


    # $ANTLR start "tt_logexp"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:228:1: tt_logexp returns [cond] : tt1= tt_logexp2 ( OR tt2= tt_logexp2 )* ;
    def tt_logexp(self, ):

        cond = None

        tt1 = None

        tt2 = None


        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:229:12: (tt1= tt_logexp2 ( OR tt2= tt_logexp2 )* )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:229:14: tt1= tt_logexp2 ( OR tt2= tt_logexp2 )*
                pass
                self._state.following.append(self.FOLLOW_tt_logexp2_in_tt_logexp1066)
                tt1 = self.tt_logexp2()

                self._state.following.pop()
                #action start
                cond = tt1
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:230:13: ( OR tt2= tt_logexp2 )*
                while True: #loop8
                    alt8 = 2
                    LA8_0 = self.input.LA(1)

                    if (LA8_0 == OR) :
                        alt8 = 1


                    if alt8 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:230:14: OR tt2= tt_logexp2
                        pass
                        self.match(self.input, OR, self.FOLLOW_OR_in_tt_logexp1083)
                        self._state.following.append(self.FOLLOW_tt_logexp2_in_tt_logexp1087)
                        tt2 = self.tt_logexp2()

                        self._state.following.pop()
                        #action start
                        cond = cond + ' or ' + tt2
                        #action end


                    else:
                        break #loop8






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return cond

    # $ANTLR end "tt_logexp"


    # $ANTLR start "tt_logexp2"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:233:1: tt_logexp2 returns [cond] : tt1= tt_primary ( AND tt2= tt_primary )* ;
    def tt_logexp2(self, ):

        cond = None

        tt1 = None

        tt2 = None


        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:234:12: (tt1= tt_primary ( AND tt2= tt_primary )* )
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:234:14: tt1= tt_primary ( AND tt2= tt_primary )*
                pass
                self._state.following.append(self.FOLLOW_tt_primary_in_tt_logexp21139)
                tt1 = self.tt_primary()

                self._state.following.pop()
                #action start
                cond = tt1
                #action end
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:235:14: ( AND tt2= tt_primary )*
                while True: #loop9
                    alt9 = 2
                    LA9_0 = self.input.LA(1)

                    if (LA9_0 == AND) :
                        alt9 = 1


                    if alt9 == 1:
                        # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:235:15: AND tt2= tt_primary
                        pass
                        self.match(self.input, AND, self.FOLLOW_AND_in_tt_logexp21157)
                        self._state.following.append(self.FOLLOW_tt_primary_in_tt_logexp21161)
                        tt2 = self.tt_primary()

                        self._state.following.pop()
                        #action start
                        cond = cond + ' and ' + tt2
                        #action end


                    else:
                        break #loop9






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return cond

    # $ANTLR end "tt_logexp2"


    # $ANTLR start "tt_primary"
    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:238:1: tt_primary returns [cond] : ( NOT tt1= tt_primary | st= sort_list kw= IN_KW tt2= tt_condition | LP tt3= tt_logexp RP );
    def tt_primary(self, ):

        cond = None

        kw = None
        tt1 = None

        st = None

        tt2 = None

        tt3 = None


        try:
            try:
                # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:239:12: ( NOT tt1= tt_primary | st= sort_list kw= IN_KW tt2= tt_condition | LP tt3= tt_logexp RP )
                alt10 = 3
                LA10 = self.input.LA(1)
                if LA10 == NOT:
                    alt10 = 1
                elif LA10 == LB:
                    alt10 = 2
                elif LA10 == LP:
                    alt10 = 3
                else:
                    nvae = NoViableAltException("", 10, 0, self.input)

                    raise nvae

                if alt10 == 1:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:239:14: NOT tt1= tt_primary
                    pass
                    self.match(self.input, NOT, self.FOLLOW_NOT_in_tt_primary1212)
                    self._state.following.append(self.FOLLOW_tt_primary_in_tt_primary1216)
                    tt1 = self.tt_primary()

                    self._state.following.pop()
                    #action start
                    cond = 'not (' + tt1 + ')'
                    #action end


                elif alt10 == 2:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:241:14: st= sort_list kw= IN_KW tt2= tt_condition
                    pass
                    self._state.following.append(self.FOLLOW_sort_list_in_tt_primary1247)
                    st = self.sort_list()

                    self._state.following.pop()
                    kw=self.match(self.input, IN_KW, self.FOLLOW_IN_KW_in_tt_primary1251)
                    self._state.following.append(self.FOLLOW_tt_condition_in_tt_primary1255)
                    tt2 = self.tt_condition()

                    self._state.following.pop()
                    #action start
                    cond = self.tt_translate_lcond(st, tt2, 'line '+str(kw.line)+':')
                    #action end


                elif alt10 == 3:
                    # /home/gandrieu/cadbiomworkspace/Cadbiom_des_new/models/guard_transitions/translators/pintlang.g:243:14: LP tt3= tt_logexp RP
                    pass
                    self.match(self.input, LP, self.FOLLOW_LP_in_tt_primary1284)
                    self._state.following.append(self.FOLLOW_tt_logexp_in_tt_primary1288)
                    tt3 = self.tt_logexp()

                    self._state.following.pop()
                    self.match(self.input, RP, self.FOLLOW_RP_in_tt_primary1290)
                    #action start
                    cond = '('+tt3+')'
                    #action end



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return cond

    # $ANTLR end "tt_primary"


    # Delegated rules




    FOLLOW_process_in_pintspec72 = frozenset([4, 5, 8])
    FOLLOW_action_in_pintspec74 = frozenset([4, 5, 8])
    FOLLOW_cooper_in_pintspec76 = frozenset([4, 5, 8])
    FOLLOW_EOF_in_pintspec81 = frozenset([1])
    FOLLOW_PROC_in_process123 = frozenset([5])
    FOLLOW_IDENT_in_process127 = frozenset([6])
    FOLLOW_INT_in_process132 = frozenset([1])
    FOLLOW_IDENT_in_action194 = frozenset([6])
    FOLLOW_INT_in_action198 = frozenset([7])
    FOLLOW_ARROW_in_action200 = frozenset([5])
    FOLLOW_IDENT_in_action204 = frozenset([6])
    FOLLOW_INT_in_action208 = frozenset([6])
    FOLLOW_INT_in_action212 = frozenset([1])
    FOLLOW_COOP_in_cooper275 = frozenset([9])
    FOLLOW_LP_in_cooper277 = frozenset([13])
    FOLLOW_coop_lhs_in_cooper281 = frozenset([10])
    FOLLOW_COM_in_cooper283 = frozenset([5, 13])
    FOLLOW_coop_rhs_in_cooper285 = frozenset([11])
    FOLLOW_RP_in_cooper288 = frozenset([1])
    FOLLOW_sort_list_in_coop_lhs338 = frozenset([7, 12])
    FOLLOW_rcoop_lhs_in_coop_lhs372 = frozenset([1])
    FOLLOW_IN_KW_in_rcoop_lhs438 = frozenset([13])
    FOLLOW_tt_condition_in_rcoop_lhs443 = frozenset([9, 13, 16, 17, 18])
    FOLLOW_tail_logexp_in_rcoop_lhs447 = frozenset([1])
    FOLLOW_ARROW_in_rcoop_lhs478 = frozenset([5])
    FOLLOW_IDENT_in_rcoop_lhs482 = frozenset([6])
    FOLLOW_INT_in_rcoop_lhs486 = frozenset([6])
    FOLLOW_INT_in_rcoop_lhs490 = frozenset([1])
    FOLLOW_tt_condition_in_coop_rhs553 = frozenset([1])
    FOLLOW_IDENT_in_coop_rhs584 = frozenset([10])
    FOLLOW_COM_in_coop_rhs588 = frozenset([6])
    FOLLOW_INT_in_coop_rhs592 = frozenset([10])
    FOLLOW_COM_in_coop_rhs595 = frozenset([6])
    FOLLOW_INT_in_coop_rhs599 = frozenset([1])
    FOLLOW_LB_in_sort_list660 = frozenset([5])
    FOLLOW_IDENT_in_sort_list664 = frozenset([14, 15])
    FOLLOW_SC_in_sort_list699 = frozenset([5])
    FOLLOW_IDENT_in_sort_list703 = frozenset([14, 15])
    FOLLOW_RB_in_sort_list709 = frozenset([1])
    FOLLOW_LB_in_tt_condition755 = frozenset([13])
    FOLLOW_tt_conjunction_in_tt_condition759 = frozenset([14, 15])
    FOLLOW_SC_in_tt_condition777 = frozenset([13])
    FOLLOW_tt_conjunction_in_tt_condition781 = frozenset([14, 15])
    FOLLOW_RB_in_tt_condition788 = frozenset([1])
    FOLLOW_LB_in_tt_conjunction835 = frozenset([6])
    FOLLOW_INT_in_tt_conjunction839 = frozenset([14, 15])
    FOLLOW_SC_in_tt_conjunction858 = frozenset([6])
    FOLLOW_INT_in_tt_conjunction862 = frozenset([14, 15])
    FOLLOW_RB_in_tt_conjunction869 = frozenset([1])
    FOLLOW_AND_in_tail_logexp931 = frozenset([9, 13, 16, 17, 18])
    FOLLOW_tt_logexp_in_tail_logexp935 = frozenset([1])
    FOLLOW_OR_in_tail_logexp966 = frozenset([9, 13, 16, 17, 18])
    FOLLOW_tt_logexp_in_tail_logexp971 = frozenset([1])
    FOLLOW_tt_primary_in_tail_logexp1002 = frozenset([1])
    FOLLOW_tt_logexp2_in_tt_logexp1066 = frozenset([1, 17])
    FOLLOW_OR_in_tt_logexp1083 = frozenset([9, 13, 16, 17, 18])
    FOLLOW_tt_logexp2_in_tt_logexp1087 = frozenset([1, 17])
    FOLLOW_tt_primary_in_tt_logexp21139 = frozenset([1, 16])
    FOLLOW_AND_in_tt_logexp21157 = frozenset([9, 13, 16, 17, 18])
    FOLLOW_tt_primary_in_tt_logexp21161 = frozenset([1, 16])
    FOLLOW_NOT_in_tt_primary1212 = frozenset([9, 13, 16, 17, 18])
    FOLLOW_tt_primary_in_tt_primary1216 = frozenset([1])
    FOLLOW_sort_list_in_tt_primary1247 = frozenset([12])
    FOLLOW_IN_KW_in_tt_primary1251 = frozenset([13])
    FOLLOW_tt_condition_in_tt_primary1255 = frozenset([1])
    FOLLOW_LP_in_tt_primary1284 = frozenset([9, 13, 16, 17, 18])
    FOLLOW_tt_logexp_in_tt_primary1288 = frozenset([11])
    FOLLOW_RP_in_tt_primary1290 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("pintlangLexer", pintlangParser)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)

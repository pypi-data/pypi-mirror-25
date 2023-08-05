## Filename    : chart_xml_pid.py
## Author(s)   : Geoffroy Andrieux
## Created     : 02/2012
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
##     Geoffroy Andrieux.
##     IRISA/IRSET
##     Symbiose team
##     IRISA  Campus de Beaulieu
##     35042 RENNES Cedex, FRANCE
##
##
## Contributor(s): Michel Le Borgne
##
"""
Guarded transition interpretation of PID data
"""

from cadbiom.models.guard_transitions.chart_model import ChartModel, ChartModelException
from lxml import etree

class MEvent(object):
    """
    Object merging similar events in PID
    """
    clock_count = 0
    def __init__(self, inputs, outputs, act_list, inhib_list, pmid, ai_inter):
        """
        Create a merged event. Similar reactions (same inputs and outputs) exist in PID we merge them.
        @param inputs: list of strings - not void
        @param outputs: list of strings - not void
        @param act_list: list of strings
        @param inhib_list: list of strings
        @param pmid: reference
        @param ai_inter: interpretation of activators and inhibitors (0: one activator no inhib., 1: all activ. inhib if all inhib )
        """
        self.inputs = inputs
        self.inputs.sort()
        self.outputs = outputs
        self.outputs.sort()
        # a unique key corresponds to a combination of inputs - outputs
        self.key = self.inputs[0]
        for input in self.inputs[1:]:
            self.key = self.key + '!' + input
        self.key = self.key + '#'
        for output in self.outputs:
            self.key = self.key + '!' + output

        # compute condition as a logical formula (or or and)
        if ai_inter == 0:
            act_logic = logical_or(act_list)
            inhib_logic = logical_or(inhib_list)
        elif ai_inter == 1:
            act_logic = logical_and(act_list)
            inhib_logic = logical_and(inhib_list)
        else:
            raise ChartModelException("Unknown activator and inhibitor option")

        if inhib_logic is not None :
            inhib_logic = 'not('+inhib_logic+')'
        condition_list = []
        if act_logic is not None :
            condition_list.append(act_logic)
        if inhib_logic is not None :
            condition_list.append(inhib_logic)
        condition = logical_and(condition_list)
        self.condition = condition  # might be None
        self.pmid = pmid

        # clock is set from outside (set_clock)
        self.clock = '_$_' #indeterminate clock


    def set_clock(self):
        """
        Create a clock ident and store it in the object
        """
        self.clock = '_h_%i' % MEvent.clock_count
        MEvent.clock_count += 1

    def merge(self, mev):
        """
        merge two events:
        we take the "or" of the two conditions
        references are concatenated without redondancy check
        """
        if self.condition and mev.condition:
            cond1 = "(" + self.condition + ")"
            cond2 = "(" + mev.condition + ")"
            self.condition = cond1 + 'or' + cond2
        elif mev.condition:
            self.condition = mev.condition
        self.pmid = self.pmid + mev.pmid

    def __str__(self):
        str_out = '\nInputs: '
        for input in self.inputs:
            str_out = str_out + input + ", "
        str_out = str_out+"\nOutput: "
        for output in self.outputs:
            str_out = str_out + output + ", "
        str_out = str_out+"\nCondition: "
        if self.condition:
            str_out = str_out + self.condition
        str_out = str_out+"\nClock: "
        str_out = str_out + self.clock
        str_out = str_out +'\n'
        return str_out




class PidXmlParser:
    """
    Object for parsing a PID xml file
    """
    def __init__(self, xml_file, reporter, has_clock = True,
                 ai_inter=0, model=None, e_loc = []):
        """
        Do everything
        """
        self.reporter = reporter
        self.has_clock = has_clock
        self.ai_interpretation = ai_inter
        # statistics
        self.node_count = 0
        self.transition_count = 0
        self.transcription_count = 0
        self.extern_loc = e_loc # for statistics on "extern" molecules
        self.extern_count = 0

        #day=time.strftime('%d_%m_%y',time.localtime())
        if not model:
            xf_split = xml_file.split('.')
            self.model = ChartModel(xf_split[0])
        else:
            self.model = model
        self.top = self.model.get_root()
        self.dict_node = dict()
        self.dict_transition = dict()

        self.coord_x = 0.01
        self.coord_y = 0.01
        self.compt = 1

        self.dict_id = dict()               # id -> name for molecules
        self.dict_name = dict()             # name -> id for molecules
        self.page = etree.parse(xml_file)
        self.int_cpt = 0
        self.mol_cpt = 0
        self.location_dict = dict()
        self.make_dict()                    # build dict_id and dict_name
        dict_mev = self.make_mev_dict()     # build a temporary dictionary
        print "\n\n\nNB INTERACTIONS: "+str(self.int_cpt)
        print "\n\n\nNB MOLECULES: "+str(self.mol_cpt)
        cpt = 0
        for key in self.location_dict.keys() :
            cpt += self.location_dict[key]
            print key,'\t',self.location_dict[key]
        print cpt
#        for k in dict_mev.keys():
#            print dict_mev[k]
        for kmev in dict_mev:
            self.make_transition(dict_mev[kmev])
        # for statistics
        self.clock_count = MEvent.clock_count


    def get_model(self):
        """
        model accessor
        """
        return self.model

#    def set_extern_localisations(self, l_loc):
#        """
#        Define external localisations in PID
#        """
#        self.extern_loc = l_loc

    def make_dict(self):
        """
        build the two dictionaries dict_id and dict_name - Cadbiom basic names are created.
        Cadbiom names result from a mangling of basic name ('PF' one if any) and various informations
        such that localisation, activity, ptm ...see throught_components
        """
        mol_list = self.page.find('Model/MoleculeList')
        i = 0
        for mol in mol_list:
            mid = mol.get('id')                   # id nb in PID
            mtype = mol.get('molecule_type')
            mol_name_list = mol.findall('Name')     # list of synonyms in PID
            if mtype:
                for name in mol_name_list:
                    if name.get('name_type') == "PF":  # preferred name
                        mol_name = name.get('value')
                        i += 1
                        break
                    else :
                        # last synonym if no preferred name type
                        mol_name = name.get('value')

                if self.dict_id.has_key(mid) and self.dict_id[mid]!=mol_name:
                    mess = 'id error : '+str(mid)
                    mess = mess + ' has two different names : '
                    mess = mess + str(mol_name) + ' and '+str(self.dict_id[mid])
                    self.reporter.display(mess)

                self.dict_id[mid] = mol_name        # id --> name
                if mol_name not in self.dict_name.keys():
                    self.dict_name[mol_name] = [mid]
                # name --> list of ids
                elif mid not in self.dict_name[mol_name]:
                    self.dict_name[mol_name].append(mid)

        #print "dict_name : ",len(self.dict_name.keys())
        #print "dict_id : ",len(self.dict_id.keys())

    def make_mev_dict(self):
        """
        Since several events with same inputs and outputs (and different conditions) may exist in PID, we merge them
        """
        id_list = []
        int_list = self.page.find('Model/InteractionList')
        print len(int_list)
        mev_dict = dict()
        for inter in int_list:
            source = inter.find('Source')
            source_id = source.get('id')
            if source_id == '5': # PID curated : 5, Biocarta : 2, Reactome : 7
                self.int_cpt +=1
                int_id = inter.get('id')
                int_type = inter.get('interaction_type')
                if int_id in id_list :
                    continue # redondancy may happend when PID files are merged

                id_list.append(int_id)
                (ili, oli, acl, inl, pmidl) = self.extract_int(inter)
                mol = len(ili) + len(oli) + len(acl) + len(inl)
                self.mol_cpt += mol
                if len(ili) == 0 or len(oli) == 0: # eliminate macros
                    continue
                mev = MEvent(ili, oli, acl, inl, pmidl, self.ai_interpretation)
                try:
                    mev_p = mev_dict[mev.key]
                    mev_p.merge(mev)
                except KeyError: # new merged event
                    mev.set_clock()
                    mev_dict[mev.key] = mev
        return mev_dict

    def extract_int(self, inter):
        """
        Extract informations from a PID interaction
        """
        input_list = []
        output_list = []
        activator_list = []
        inhibitor_list = []
        pmid_list = []
        int_type = inter.get('interaction_type')

        #PMID part
        int_references = inter.find('ReferenceList')
        if int_references is not None :
            for ref in int_references :
                pmid_list.append(ref.get('pmid'))

        #Component part
        int_components = inter.find('InteractionComponentList')
        for comp in int_components :
            c_role = comp.get('role_type')
            c_name = self.throught_component(comp) # do loc and ptm mangling
            self.make_new_node(c_name, 'simple')
            if c_role == 'input' :
                input_list.append(c_name)
            elif c_role == 'output' :
                output_list.append(c_name)
            elif c_role == 'agent':
                activator_list.append(c_name)
            else :
                inhibitor_list.append(c_name)

        if int_type == 'transcription' :
            if  len(output_list)!=0 :
                gene_name = output_list[0]+'_gene'
                self.make_new_node(gene_name, 'perm')
                self.transcription_count += 1
                input_list.append(gene_name)

        return (input_list, output_list, activator_list,
                inhibitor_list, pmid_list)


    def throught_component(self, component) :
        """
        Cadbiom names result from a mangling of basic name ('PF' one if any) and various informations
        such that localisation, activity, ptm ... This is done here.
        """
        activity_state = ''
        location = ''
        ptm_name = ''

        ident = component.get('molecule_idref')
        name = self.dict_id[ident]
        label_list = component.findall('Label')
        for label in label_list :
            ltype = label.get('label_type')
            lvalue = label.get('value')
            if ltype == 'location' :
                location = self.location_converter(lvalue)
            else :
                activity_state = '_'+lvalue

        ptm_list = component.find('PTMExpression')
        if ptm_list is not None:
            for ptm in ptm_list :
                ptm_current_name = ptm_converter(ptm.get('modification'))
                ptm_name += ptm_current_name

        final_name = make_name(name, activity_state, ptm_name, location)
        final_name = make_new_name(final_name)

        return final_name

    def make_transition(self, mev):
        """
        mev is the current merge event
        """
        in_list = mev.inputs
        out_list = mev.outputs
        # condition from activators and inhibitors (ai)
        ai_condition = mev.condition

        # building guarded transitions
        for input in in_list :
            # transition is conditioned by presence of other inputs
            other_in_list = []
            for input2 in in_list :
                if input2 != input and input2 not in other_in_list :
                    other_in_list.append(input2)
            input_logic_and = logical_and(other_in_list)
            if input_logic_and and ai_condition:
                condition = '('+input_logic_and +') and ('+ ai_condition + ')'
            elif input_logic_and:
                condition = input_logic_and
            else:
                condition = ai_condition
            # generate a guarded transition from input to each output of mev
            for output in out_list :
                if input != output :
                    if not self.has_clock:
                        self.no_clock_trans(mev, input, output, condition)
                    else:
                        self.clock_trans(mev, input, output, condition)
                else:
                    #TODO warn??
                    pass

    def no_clock_trans(self, mev, input, output, condition):
        """
        translation without clock - data flow interpretation
        """
        inout = input + '#' + output
        if self.dict_transition.has_key(inout):
            # a transition already exist input -> output
            prev_transition = self.dict_transition[inout]
            previous_condition = prev_transition.condition
            # both different conditions
            cond2 = previous_condition != ''
            cond2 = cond2 and previous_condition != condition
            if condition is not None and cond2:
                new_condition = previous_condition+' or ('+condition+')'
            # equal conditions
            elif condition is not None and previous_condition != '':
                new_condition = condition
            # first condition only
            elif condition:
                new_condition = condition
            # second condition only ( may be empty chain
            else:
                new_condition = previous_condition
            prev_transition.set_condition(new_condition)
            prev_transition.note += str(mev.pmid)
        else :
            # new transition
            input_node = self.dict_node[input]
            output_node = self.dict_node[output]
            transition = self.top.add_transition(input_node, output_node)
            self.transition_count += 1
            if condition is not None :
                transition.set_condition(condition)
            transition.note = 'PMID ' + str(mev.pmid)
            self.dict_transition[inout] = transition


    def clock_trans(self, mev, input, output, condition):
        """
        translation with clock introduction
        """
        inout = input + '#' + output
        if self.dict_transition.has_key(inout):
            # a transition already exist input -> output
            prev_transition = self.dict_transition[inout]
            previous_condition = prev_transition.condition # might be none
            previous_clock = prev_transition.event

            if mev.clock == previous_clock:
                cond2 = previous_condition != ''
                cond2 = cond2 and previous_condition != condition
                if condition is not None and cond2:
                    new_condition = '(' + previous_condition + ')'
                    new_condition =  new_condition + 'or ('  + condition + ')'
                # equal conditions
                elif condition is not None and previous_condition != '':
                    new_condition = condition
                # first condition only
                elif condition:
                    new_condition = condition
                # second condition only ( may be empty chain
                else:
                    new_condition = previous_condition
                new_clock = mev.clock
            else:
                new_condition = ''
                ncl1 = when_clock(previous_clock, previous_condition)
                ncl2 = when_clock(mev.clock, condition)
                new_clock = default_clock(ncl1, ncl2)
            prev_transition.event = new_clock
            prev_transition.condition = new_condition
            prev_transition.note += str(mev.pmid)
        else:
            # new transition
            input_node = self.dict_node[input]
            output_node = self.dict_node[output]
            transition = self.top.add_transition(input_node, output_node)
            self.transition_count += 1
            if condition is not None :
                transition.set_condition(condition)
            transition.event = mev.clock
            transition.note = 'PMID '+str(mev.pmid)
            self.dict_transition[inout] = transition


    def location_converter(self, location):
        """
        convert PID location coding into cadbiom one
        """
        if self.location_dict.has_key(location) :
            self.location_dict[location] += 1
        else :
            self.location_dict[location] = 1
        # statistics
        if location in self.extern_loc:
            self.extern_count += 1
        # short hands for locations
        if location == 'transmembrane':
            return '_transMb'
        elif location =='cytoplasm' or location == 'cytosol':
            return '_cy'
        elif location == 'mitochondria':
            return  '_mi'
        elif location == 'nucleus':
            return '_nucl'
        elif location == 'extracellular region':
            return '_exCellRegion'
        elif location == 'vesicle':
            return '_v'
        elif location == 'calcium store':
            return '_calciumStore'
        elif location == 'endosome':
            return '_en'
        elif location == 'endoplasmic reticulum':
            return '_endoRetic'
        elif location == 'Golgi apparatus':
            return '_golgiAp'
        elif location == 'lysosome':
            return '_l'
        elif location == 'extracellular matrix':
            return '_exMatrix'
        elif location == 'plasma membrane':
            return '_plasmaMb'
        elif location == 'integral to membrane':
            return '_intToMb'
        elif location == 'cell-cell junction':
            return '_ccJct'
        elif location == 'hemidesmosome':
            return '_hd'
        elif location == 'caveola':
            return '_cav'
    #    elif location =='early endosome':
    #        return 'eend'
    #    elif location =='basement membrane':
    #        return 'bmb'
        else :
    #        print 'location exception : ',location
            return '_'+location




    def make_new_node(self, node_name, node_type):
        """
        add a new node in the model
        """
        if node_name in self.dict_node.keys():
                pass
        else:
            name = node_name
            if name != '':
                xloc = self.coord_x
                yloc = self.coord_y
                if node_type == 'simple':
                    node = self.top.add_simple_node(name, xloc, yloc)
                elif node_type == 'perm':
                    node = self.top.add_perm_node(name, xloc, yloc)
                elif node_type == 'macro':
                    node = self.top.add_macro_subnode(name, xloc, yloc,
                                                       0.20, 0.05)
                elif node_type == 'trap':
                    node = self.top.add_trap_node(xloc, yloc, name)
                else :
                    print 'node type error'
                self.node_count += 1
                self.dict_node[node_name] = node
                self.coord_inc()

    def coord_inc(self):
        """
        increment coordinates of nodes for a rectangular layout
        """
        if self.compt == 19:
            self.compt = 1
            self.coord_x = 0.01
            self.coord_y += 0.03
        else:
            self.compt += 1
            self.coord_x += 0.05

def logical_or(list):
    """
    @return: str - OR of the input list
    """
    if len(list) == 0 :
        return None
    elif len(list) == 1 :
        return list[0]
    else :
        logical_formula = ''
        for elemnt in list :
            logical_formula += elemnt + ' or '
        logical_formula = logical_formula[:-4]
#        print logical_formula
        return '('+logical_formula+')'

def when_clock(clo, cond):
    """
    generate a when literal expression
    """
    if not cond:
        return clo
    if len(cond) > 0:
        return '(' + clo + ') when (' + cond + ')'
    else:
        return clo

def default_clock(cl1, cl2):
    """
    generate a literal default clock
    """
    return '(' + cl1 + ') default (' + cl2 + ')'


def logical_and(lprop):
    """
    @return: str - AND of the input list
    """
    if len(lprop)==0 :
        return None
    elif len(lprop)==1 :
        return lprop[0]
    else :
        logical_formula = ''
        for elemnt in lprop :
            logical_formula += elemnt + ' and '
        logical_formula = logical_formula[:-5]
#        print logical_formula
        return '('+logical_formula+')'



def ptm_converter(ptm_term):
    """
    post transformation convertion from PID to Cadbiom
    """
    if ptm_term == 'phosphorylation':
        return '_p'
    elif ptm_term == 'acetylation':
        return '_ac'
    elif ptm_term == 'methylation':
        return '_meth'
    elif ptm_term == 'sumoylation':
        return '_sumo'
    elif ptm_term == 'ubiquitination':
        return '_ub'
    else:
        return '_' + ptm_term

def make_name(name, act, ptm, loc):
    """
    tgenerate a name
    """
    if len(act)!=0:
        name += act
    if len(ptm)!=0:
        name += ptm
    if len(loc)!=0:
        name += loc
    return name

def make_new_name(name):
    """
    remove unusable characters
    """
    new_name = ''
    for cha in name:
        if cha == ' ' :
            continue
        elif cha == '/' :
            cha = '_'
            new_name += cha
        elif cha == '-':
            cha = '_'
            new_name += cha

        elif cha == '+':
            cha = 'PLUS'
            new_name += cha

        elif cha == '.':
            cha = 'POINT'
            new_name += cha

        elif cha == '(' or cha == ')':
            cha = '__'
            new_name += cha
        else:
            new_name += cha
    return new_name

class MakeModelFromPidFile(PidXmlParser):
    """
    Interface class
    """
    def __init__(self, xml_file, reporter,
                 has_clock=True, ai_inter=0, e_loc=[]):
        PidXmlParser.__init__(self, xml_file, reporter,
                              has_clock, ai_inter, None, e_loc)


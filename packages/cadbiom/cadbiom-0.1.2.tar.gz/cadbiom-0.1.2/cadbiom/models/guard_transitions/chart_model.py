##
## Filename    : chart_model.py
## Author(s)   : Michel Le Borgne
## Created     : 4/3/2010
## Revision    :
## Source      :
##
## Copyright 2009 - 2010 : IRISA/IRSET
##
## This library is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published
## by the Free Software Foundation; either version 2.1 of the License, or
## any later version.
##
## This library is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY, WITHOUT EVEN THE IMPLIED WARRANTY OF
## MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.  The software and
## documentation provided hereunder is on an "as is" basis, and IRISA has
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
##     http:
##     mailto:
##
## Contributor(s): Nolwenn Le Meur, Geoffroy Andrieux
##
"""
Classes for representing a guarded transition model
"""

from math import sqrt
from cadbiom.antlr3 import ANTLRStringStream, ANTLRFileStream, CommonTokenStream

from condexpLexer import condexpLexer
from condexpParser import condexpParser
from cadbiom.models.guard_transitions.translators.cadlangLexer import cadlangLexer
from cadbiom.models.guard_transitions.translators.cadlangParser import cadlangParser

# number of simple nodes before we draw macros as simple nodes
MAX_SIZE_MACRO = 50
MAX_SIZE = 2000 # max number of nodes we draw




class ChartModelException(Exception):
    """
    Exception for chart models
    """
    def __init__(self, mess):
        self.message = mess




class ChartModel(object):
    """
    Model of a chart - implements the observer pattern as subject
    observers must have an update method
    """
    def __init__(self, name):
        self.name = name
        self.simple_node_dict = dict()       # for quick finding - name -> node
        self.node_dict = dict()
        self.transition_list = []            # idem
        # idem - simple node name -> list of influenced transition
        self.signal_transition_dict = dict()
        self.__root = CTopNode(name, self)
        self.constraints = "" # string of biosignal clock constraints
        self.modified = False
        self.show_macro = True
        # default value for max number of nodes for drawing
        self.max_size = MAX_SIZE
        self.__observer_list = [] # for observer pattern

    # observer pattern methods
    def attach(self, obs):
        """
        observer pattern standard attach methods
        """
        if not obs in self.__observer_list:
            self.__observer_list.append(obs)

    def detach(self, obs):
        """
        observer pattern standard detach methods
        """
        self.__observer_list.remove(obs)

    def notify(self):
        """
        observer pattern standard notify methods
        """
        for obs in self.__observer_list:
            obs.update()


    def build_from_cadlang(self, file_name, reporter):
        """
        Build a model from a .cal file of PID database
        @param file_name: str - path of .cal file
        """
        crep = reporter
        fstream = ANTLRFileStream(file_name)
        lexer = cadlangLexer(fstream)
        lexer.set_error_reporter(crep)
        parser = cadlangParser(CommonTokenStream(lexer))
        parser.set_error_reporter(crep)
        parser.cad_model(self)

    # model methods
    def draw(self, view):
        """
        @param view: chart_view
        """
        # we don't update views which are not visible
        if not view.window:
            return

        nb_snodes = len(self.simple_node_dict)
        # if model size two large don't draw
        if  nb_snodes > self.max_size:
            return

        # if model size two large, don't show macros
        if  nb_snodes > MAX_SIZE_MACRO:
            self.show_macro = False
        self.__root.draw(view)

    def get_root(self):
        """
        @return: the root of the hierarchy
        """
        if self.__root.submodel:
            return self.__root.sub_nodes[0]
        else:
            return self.__root

    def find_element(self,  m_v_c, dstyle):
        """
        @param m_v_c :coordinates of the mouse in virtual screen
        @param dstyle: drawing style (gives virtual size of fixed size nodes)

        Given the window mouse coordinates, return (node, handle, center)
        where node is the node the mouse is in,  handle the handle of the node
        the mouse is in and c are the coordinates of the node center in view.
        If no handle, handle = 0, handle are 1,2,3,4 clockwise numbered
        from upper left corner
        If no node found returns (None,0,(0,0))
        """
        return self.__root.find_element(m_v_c[0], m_v_c[1], dstyle)

    def make_submodel(self, mnode):
        """
        make a submodel from a macronode (no check) of another model
        """
        self.__root.sub_nodes = []
        self.__root.add_submodel(mnode)

    def is_submodel(self):
        """
        test if it is a submodel (for macro view)
        """
        return self.__root.submodel

    def is_modified(self):
        """
        Changes occur?
        """
        return self.modified

    def clean(self):
        """
        Clean markers
        """
        self.__root.clean()

    def clean_code(self):
        """
        Clean code attribute
        """
        self.__root.clean_code()

    def accept(self, visitor):
        """
        Visitors entrance
        """
        return visitor.visit_chart_model(self)

    def get_simple_node_names(self):
        """
        @return: list of simple nodes in model
        """
        # refresh transition dictionary
        self.signal_transition_dict = dict()
        for trans in self.transition_list:
            ids = trans.get_influencing_places()
            for ident in ids:
                try:
                    id_tr = self.signal_transition_dict[ident]
                    self.signal_transition_dict[id].append(trans)
                except:
                    self.signal_transition_dict[ident] = [trans]
        return self.simple_node_dict.keys()

    def get_matching_node_names(self, regex_obj):
        """
        @return: return node names with name matching reg. expr.
        """
        lname = []
        for name in self.simple_node_dict.keys():
            if regex_obj.match(name):
                lname.append(name)
        return lname


    def search_unmark(self):
        """
        notify observers after unmarking nodes
        """
        for key in self.simple_node_dict:
            self.simple_node_dict[key].search_mark = False
        for key in self.signal_transition_dict:
            for trans in self.signal_transition_dict[key]:
                trans.search_mark = False
        self.notify()

    def search_mark(self, lnode):
        """
        notify observers after marking nodes from lnode
        """
        # unmark first
        for key in self.simple_node_dict:
            self.simple_node_dict[key].search_mark = False
        for key in self.signal_transition_dict:
            for trans in self.signal_transition_dict[key]:
                trans.search_mark = False
        for name in lnode:
            try:
                self.simple_node_dict[name].search_mark = True
                # do not mark transition if node doesnt exist
                for trans in self.signal_transition_dict[name]:
                    trans.search_mark = True
            except:
                pass
        self.notify()

    def get_simple_node(self, name):
        """
        @param name: string - name of the node
        @return a simple node with given name
        """
        return self.simple_node_dict[name]

    def get_node(self, name):
        """
        @param name: string - name of the node
        @return: a node
        """
        return self.node_dict[name]

    def get_influenced_transition(self, node_name):
        """
        @param node_name: string
        @return: the transitions influenced by the node i.e. when
                 the node name appears in the condition
        """
        try:
            return self.signal_transition_dict[node_name]
        except:
            return []

    # method for model transformations
    def mark_as_frontier(self, node_name):
        """
        @param node_name: string
        Given the name of a simple node, add a start node and a transition
        from the start node to the simple node
        @warning: notify observers
        """
        try:
            snode = self.simple_node_dict[node_name]
            macro = snode.father
            start = macro.add_start_node(0, 0)
            macro.add_transition(start, snode)
        except KeyError:
            raise ChartModelException("Unknown simple node: "+node_name)
        self.notify()

    def __turn_into_other(self, node_name, ntype):
        """
        @param node_name: string
        @param ntype: node type - string
        turn a simple name into a permanent or input node
        The simple name must not have entering transitions
        @warning: notify observer
        """
        try:
            snode = self.simple_node_dict[node_name]
        except KeyError:
            raise ChartModelException("Unknown simple node: "+node_name)
        if len(snode.incoming_trans) != 0:
            raise ChartModelException("Incoming transition on node: "+node_name)
        macro = snode.father
        if ntype == 'perm':
            pnode = macro.add_perm_node(node_name, snode.xloc, snode.yloc)
        else:
            pnode = macro.add_input_node(node_name, snode.xloc, snode.yloc)
        for trans in snode.outgoing_tran:
            macro.add_transition(pnode, trans. ext)
        snode.remove()
        self.notify()

    def turn_into_input(self, node_name):
        """
        Turn a simple node into an input node
        """
        self.__turn_into_other(node_name, 'input')

    def turn_into_perm(self, node_name):
        """
        Turn a simple node into a perm node
        """
        self.__turn_into_other(node_name, 'perm')


class CNode(object):
    """
    Generic node for guarded transition models
    """
    wmin = 0.1
    hmin = 0.1
    depth_max = 3

    """
    Base class for  model components
    """
    def __init__(self, x_coord, y_coord, model):
        """
        The coordinates of a node are always in the space of its father.
        """
        self.model = model
        self.name = '$$'
        self.xloc = x_coord
        self.yloc = y_coord
        self.father = None
        self.selected = False
        self.search_mark = False
        self.incoming_trans = []
        self.outgoing_trans = []

    def is_top_node(self):
        """
        As it says
        """
        return False

    def is_macro(self):
        """
        As it says
        """
        return False

    def is_start(self):
        """
        As it says
        """
        return False

    def is_input(self):
        """
        As it says
        """
        return False

    def is_perm(self):
        """
        As it says
        """
        return False

    def is_trap(self):
        """
        As it says
        """
        return False

    def is_simple(self):
        """
        As it says
        """
        return False

    def set_model(self, model):
        """
        As it says
        """
        self.model = model

    def set_name(self, name):
        """
        As it says
        """
        self.name = name

#    def set_coordinates(self, x, y):
#        """
#        As it says
#        """
#        self.xloc = x
#        self.yloc = y
#        self.model.notify()

    def get_coordinates(self):
        """
        As it says
        """
        return (self.xloc, self.yloc)

    def set_layout_coordinates(self, x_coord, y_coord):
        """
        As it says
        """
        self.xloc = x_coord
        self.yloc = y_coord


    def find_element(self, mox, moy, dstyle):
        """
        The mouse coordinates must be in the same frame than nodes coordinates
        """
        pass


    def remove(self):
        """
        Remove this node from its model - assume it is not a top-node
        """
        if self.father:
            nfath = self.father
            # remove transitions using this node
            to_remove = []
            for gtr in nfath.transitions:
                if gtr[0].ori == self :
                    to_remove.append(gtr)

                elif gtr[0].ext == self :
                    to_remove.append(gtr)

            for gtr in to_remove:
                nfath.transitions.remove(gtr)
                for trans in gtr :
                    trans.remove()

            nfath.sub_nodes.remove(self)
            if self.model.simple_node_dict.has_key(self.name):
                del self.model.simple_node_dict[self.name]
            self.model.modified = True
            self.model.notify()
        else:
            pass

    def clean(self):
        """
        Abstract
        """
        pass


class CStartNode(CNode):
    """
    Start node show macro-states initialisation
    """
    def __init__(self, x_coord, y_coord, model):
        CNode.__init__(self, x_coord, y_coord, model)
        self.name = "__start__"
        self.wloc = 1.0
        self.hloc = 1.0 # for compatibility with find

    def copy(self, model = None):
        """
        As says
        """
        if not model:
            model = self.model
        node = CStartNode(self.xloc, self.yloc, model)
        return node

    def is_start(self):
        """
        As says
        """
        return True

    def is_for_origin(self):
        """
        As says
        """
        return True

    def is_for_extremity(self):
        """
        As says
        """
        return False

    def get_center_loc_coord(self, dstyle, w_ratio, h_ratio):
        """
        @param dstyle: drawing style (not used here)
        @param w_ratio,h_ratio: affinity ratios for virtual screen (not used here)

        Returns center coordinate in surrounding node - here node coordinates
        """
        return (self.xloc, self.yloc)

    def draw(self, view, xfr, yfr, wfr, hfr, depth):
        """
        depth is less than depth_max
        """
        # graphic style
        view.drawing_style.draw_start(self, xfr, yfr, wfr, hfr)

    def find_element(self, mox, moy , dstyle, w_coef, h_coef):
        """
        No handle
        """
        # bounding box in father's frame
        v_bb_size = self.accept(dstyle)
        snw = v_bb_size[0] * w_coef
        snh = v_bb_size[1] * h_coef
        hdec = v_bb_size[2] * h_coef

        # center coordinates in father's frame
        ccx = self.xloc
        ccy = self.yloc + hdec
        in_node = (mox>=ccx-snw) and (mox<=ccx+snw)
        in_node = in_node and  (moy>=ccy-snh) and (moy<=ccy+snh)
        if in_node:
            return (self, 0, (ccx, ccy), None)
        else:
            return (None, 0, (0, 0), None)

    def move(self, v_dx, v_dy, dstyle, top_node):
        """
        Move the node - mx_virt, my virt coordinates of the mouse in virtual screen frame
        click_loc is the location of the clic in node's frame
        """

        # move in reference frame (father's)
        (acx, acy) = self.father.v_affinity_coef(top_node)
        loc_dx = acx*v_dx
        loc_dy = acy*v_dy
        # translation vector in own's frame -> father's frame
        new_xloc = self.xloc + loc_dx
        new_yloc = self.yloc + loc_dy

        # TODO compute limits
        delta = 0.0
        if (new_xloc >= 0) and (new_xloc<1.0):
            self.xloc = new_xloc
        if (new_yloc > delta) and (new_yloc < 1.0):
            self.yloc = new_yloc
        self.model.modified = True
        self.model.notify()

    def intersect(self, node2, dstyle, nb_trans, w_ratio, h_ratio):
        """
        @param dstyle: drawing style
        @param w_ratio, h_ratio: affinity ratios virtual -> local frame
        """
        (xc2, yc2) = node2.get_center_loc_coord(dstyle, w_ratio, h_ratio)
        # local axes size (ellipse because of affinities)
        v_size = self.accept(dstyle)
        rlocx = v_size[0]/w_ratio
        rlocy = v_size[1]/h_ratio
        uux = xc2 - self.xloc
        uuy = yc2 - self.yloc
        norm = sqrt(uux**2 + uuy**2)
        if norm != 0:
            uux = uux / norm
            uuy = uuy / norm
        isx = self.xloc + uux * rlocx
        isy = self.yloc + uuy * rlocy
        return (isx, isy, 0.0, 1)

    def clean(self):
        pass

    def accept(self, visitor):
        """
        Generic visitor acceptor
        """
        return visitor.visit_cstart_node(self)

class CTrapNode(CStartNode):
    """
    Dead end node
    """
    def __init__(self, xcoord, ycoord, model):
        CStartNode.__init__(self, xcoord, ycoord, model)
        self.name = "__trap__"

    def is_trap(self):
        return True

    def is_start(self):
        return False

    def copy(self, model = None):
        if not model:
            model = self.model
        node = CTrapNode(self.xloc, self.yloc, model)
        return node

    def is_for_origin(self):
        return False

    def is_for_extremity(self):
        return True

    def draw(self, view, xfr, yfr, wfr, hfr, depth):
        """
        depth is less than depth_max
        """
        # graphic context
        view.drawing_style.draw_trap(self, xfr, yfr, wfr, hfr)

    def accept(self, visitor):
        """
        Standard acceptor
        """
        return visitor.visit_ctrap_node(self)

class CSimpleNode(CNode):
    """
    A simple node cannot have sub nodes
    Simple nodes have constant screen dimensions
    """
    def __init__(self, xcoord, ycoord, name, model):
        CNode.__init__(self, xcoord, ycoord, model)
        self.name = name.encode('ascii')
        self.father = None # double linkage for coordinate computations
        self.hloc = 1.0
        self.activated = False
        self.was_activated = False

    def copy(self, model = None):
        """
        As says
        """
        if not model:
            model = self.model
        node = CSimpleNode(self.xloc, self.yloc, self.name, model)
        return node

    def is_simple(self):
        return True

    def is_for_origin(self):
        """
        Can be used as transition origin
        """
        return True

    def is_for_extremity(self):
        """
        Can be used as transition extremity
        """
        return True

    def set_name(self, name):
        try:
            del self.model.simple_node_dict[self.name]
        except:
            pass
        self.name = name
        self.model.simple_node_dict[name] = self

    def get_center_loc_coord(self, dstyle, w_ratio, h_ratio):
        """
        Returns center coordinate in surrounding node
        """
        v_size = self.accept(dstyle)
        xco = self.xloc + (v_size[0] / w_ratio) / 2.0
        yco = self.yloc + (v_size[1] / h_ratio) / 2.0
        return (xco, yco)


    def draw(self, view, xfr, yfr, wfr, hfr, depth):
        """
        depth is less than depth_max
        @param xfr: x coordinate of father in view screen
        @param yfr: y coordinate of father in view screen
        @param wfr: width of father in virtual screen
        @param hfr: height of father in virtual screen
        """
        view.drawing_style.draw_simple(self, xfr, yfr, wfr, hfr)


    def find_element(self, mox, moy, dstyle, w_coef, h_coef):
        """
        Simple node - No handle
        """
        # size of the node in father's frame
        v_bb = self.accept(dstyle)
        snw = v_bb[0] * w_coef
        snh = v_bb[1] * h_coef

        # center coordinates in father's frame
        ccx = self.xloc + 0.5 * snw
        ccy = self.yloc + 0.5 * snh
        in_node = (mox >= self.xloc) and (mox <= self.xloc + snw)
        in_node = in_node and (moy >= self.yloc) and (moy <= self.yloc+snh)
        if in_node:
            return (self, 0, (ccx, ccy), None)
        else:
            return (None, 0, (0, 0), None)


    def move(self, v_dx, v_dy, v_size, top_node):
        """
        Move the node - mx_virt, my virt are virtual coordinates of the mouse
        click_loc is the location of the clic in node's frame
        """
        # move in reference frame (father's)
        (ccx, ccy) = self.father.v_affinity_coef(top_node)
        loc_dx = ccx * v_dx
        loc_dy = ccy * v_dy
        # translation vector in reference frame i.e. father's frame
        new_xloc = self.xloc + loc_dx
        new_yloc = self.yloc + loc_dy

        # check limits
        wloc = v_size[0] * ccx
        hloc = v_size[1] * ccy
        delta = v_size[2] * ccy

        move = False
        if (new_xloc >= 0) and (new_xloc+wloc < 1.0):
            self.xloc = new_xloc
            move = True
        if (new_yloc > delta) and (new_yloc+hloc < 1.0):
            self.yloc = new_yloc
            move = True
        if move:
            self.model.modified = True
            self.model.notify()


    def intersect(self, node2, dstyle, nb_trans, w_ratio, h_ratio):
        """
        Gives the the first point where to branch a transition, the gap between two arrows
        and a boolean horizontal true if arrows start from horizontal edge
        Assume wloc and hloc computed (node drawn) - coordinates in container frame

        @param node2: second node of the transition
        @param dstyle: drawing style
        @param nb_trans: number of transitions to be drawn
        @param w_ratio, h_ratio: dimentions of the screen for fixed size nodes
        """
        return intersect_simple(self, node2, dstyle, nb_trans, w_ratio, h_ratio)


    def clean(self):
        self.activated = False
        self.was_activated = False

    def accept(self, visitor):
        """
        standard visitor acceptor
        """
        return visitor.visit_csimple_node(self)

class CPermNode(CSimpleNode):
    """
    permanent node are never unactivated
    """

    def __init__(self,  xcoord, ycoord, name, model):
        CSimpleNode.__init__(self, xcoord, ycoord, name, model)

    def copy(self, model = None):
        if not model:
            model = self.model
        node = CPermNode(self.xloc, self.yloc, self.name, model)
        return node

    def is_perm(self):
        return True

    def is_simple(self):
        return False

    def is_for_extremity(self):
        return False

    def accept(self, visitor):
        return visitor.visit_cperm_node(self)

    def draw(self, view, xfr, yfr, wfr, hfr, depth):
        """
        depth is less than depth_max
        @param xfr, yfr: coordinates of father node (reference frame) in view
        @param wfr,hfr: width and height of father node in view (affinity ratios)
        """
        view.drawing_style.draw_perm(self, xfr, yfr, wfr, hfr)


class CInputNode(CSimpleNode):
    """
    An input node cannot have an in-transition
    """
    def __init__(self, xcoord, ycoord, name, model):
        CSimpleNode.__init__(self, xcoord, ycoord, name, model)
        self.father = None # double linkage for coordinate computations
        self.hloc = 1.0
        self.activated = False

    def is_input(self):
        return True

    def is_simple(self):
        return False

    def copy(self, model = None):
        if not model:
            model = self.model
        node = CInputNode(self.xloc, self.yloc, self.name, model)
        return node

    def is_for_extremity(self):
        return False

    def get_center_loc_coord(self, dstyle, w_ratio, h_ratio):
        """
        Returns center coordinate in surrounding node
        """
        return (self.xloc, self.yloc)

    def draw(self, view, xfr, yfr, wfr, hfr, depth):
        """
        special drawing for diamond
        """
        view.drawing_style.draw_input(self, xfr, yfr, wfr, hfr)

    def find_element(self, mox, moy , dstyle, w_coef, h_coef):
        """
        Simple node - No handle
        """
        # size of the box in father's frame
        v_bb = self.accept(dstyle)
        snw = v_bb[0] * w_coef
        snh = v_bb[1] * h_coef

        # center coordinates in father frame
        ccx = self.xloc + 0.5 * snw
        ccy = self.yloc + 0.5 * snh

        # mouse coordinates in self frame
        mxl = (mox - self.xloc) / snw
        myl = (moy - self.yloc) / snh
        # test
        in_node = (mox >= self.xloc) and (mox <= self.xloc+snw)
        in_node = in_node and (moy >= self.yloc) and (moy <= self.yloc+snh)

        if in_node:
            return (self, 0, (ccx, ccy), None)
        else:
            return (None, 0, (0, 0), None)

    def move(self, v_dx, v_dy, v_size, top_node):
        """
        Move the node - mx_virt, my virt are virtual coordinates of the mouse
        click_loc is the location of the clic in node's frame
        """
        # move in reference frame (father's)
        (ccx, ccy) = self.father.v_affinity_coef(top_node)
        loc_dx = ccx * v_dx
        loc_dy = ccy * v_dy
        # translation vector in reference frame i.e. father's frame
        new_xloc = self.xloc + loc_dx
        new_yloc = self.yloc + loc_dy
        # check limits
        wloc = (v_size[0] * ccx)/2.0
        hloc = (v_size[1] * ccy)/2.0
        hlabel = v_size[2] * ccy

        move = False
        if (new_xloc >= wloc) and (new_xloc+wloc < 1.0):
            self.xloc = new_xloc
            move = True
        if (new_yloc - hloc> hlabel) and (new_yloc+hloc < 1.0):
            self.yloc = new_yloc
            move = True
        if move:
            self.model.modified = True
            self.model.notify()


    def intersect(self, node2, dstyle, nb_trans, w_ratio, h_ratio):
        """
        An input node can be the origin of some transition to a node.
        One transition by node.
        """
        # local coordinates of node2 center
        (xc2, yc2) = node2.get_center_loc_coord(dstyle, w_ratio, h_ratio)
        # simple nodes have constant screen dimensions - convert to local ones
        v_size = self.accept(dstyle)
        wloc = (v_size[0] / w_ratio) / 2.0
        hloc = (v_size[1] / h_ratio) / 2.0
        # coordinates of a diamond are center coordinates
        uux = xc2 - self.xloc
        uuy = yc2 - self.yloc
        if uux != 0.0:
            slope = uuy / uux
            if slope < -1:
                if uux < 0.0:
                    return (self.xloc, self.yloc + hloc, 0, True) # upper corner
                else:
                    return (self.xloc, self.yloc - hloc, 0, True) # low corner
            elif slope >= -1 and slope <= 1:
                if uux < 0.0:
                    return (self.xloc - wloc, self.yloc, 0, True) # left corner
                else:
                    return (self.xloc + wloc, self.yloc, 0, True) # right corner
            else:
                if uux < 0.0:
                    return (self.xloc, self.yloc - hloc, 0, True) # low corner
                else:
                    return (self.xloc, self.yloc + hloc, 0, True) # upper corner
        else:
            if uuy >= 0:
                return (self.xloc, self.yloc + hloc, 0, True) # upper corner
            else:
                return (self.xloc, self.yloc - hloc, 0, True) # low corner

    def accept(self, visitor):
        return visitor.visit_cinput_node(self)

class CMacroNode(CSimpleNode):
    """
    Main building block for charts
    """
    def __init__(self, xcoord, ycoord, width, height, name, model):
        CSimpleNode.__init__(self, xcoord, ycoord, name, model)
        self.count = 0 # for start and trap nodes naming
        self.wloc = width
        self.hloc = height
        self.sub_nodes = []
        # list<list<CTransitions>> Sublists: transitions with common extremities
        self.transitions = []

    def _find_in_subnodes(self, node):
        """
        Find a node in the list of sub nodes.
        assume two nodes have different coordinates
        @param node: node to be found
        """
        for snode in self.sub_nodes:
            if snode.xloc == node.xloc and snode.yloc == node.yloc:
                return snode
        return None

    def copy(self, model = None):
        """
        Duplicate a macronode - performs a deep copy
        """
        if not model:
            model = self.model
        node_c = CMacroNode(self.xloc, self.yloc, self.wloc, self.hloc,
                            self.name, model)
        # copy subnodes
        for snode in self.sub_nodes:
            snc = snode.copy(model)
            node_c.sub_nodes.append(snc)
            snc.father = node_c
        # copy transitions
        for gtr in self.transitions:
            gtr_c = []
            for trans in gtr:
                origin = trans.ori
                origin_c = node_c._find_in_subnodes(origin)
                extremity = trans.ext
                extremity_c = node_c._find_in_subnodes(extremity)
                trc = CTransition(origin_c, extremity_c)
                trc.macro_node = node_c
                trc.event = trans.event
                trc.condition = trans.condition
                trc.action = trans.action
                gtr_c.append(trc)
            node_c.transitions.append(gtr_c)
        return node_c

    def set_model(self, model):
        """
        Set the model for a subtree of nodes - used for copy/paste from one model to another
        """
        for snode in self.sub_nodes:
            snode.set_model(model)
        self.model = model
        self.model.modified = True

    def set_name(self, name):
        self.name = name

    def is_macro(self):
        return True

    def is_simple(self):
        return False

    def is_for_origin(self):
        """
        Legitimate transition origin
        """
        return True

    def is_for_extremity(self):
        """
        Legitimate transition extremity
        """
        return True

    def get_center_loc_coord(self, dstyle, w_ratio, h_ratio):
        """
        Returns center coordinate in surrounding node (father)
        """
        if self.model.show_macro:
            xcc = self.xloc + self.wloc / 2.0
            ycc = self.yloc + self.hloc / 2.0
        else:
            v_size = self.accept(dstyle)
            xcc = self.xloc + (v_size[0] / w_ratio) / 2.0
            ycc = self.yloc + (v_size[1] / h_ratio) / 2.0
        return (xcc, ycc)

    def virt_to_self_frame(self, xcoord, ycoord, s_width, s_height, top_node):
        """
        xcoord,ycoord must be virtual coordinates
        result is the coordinates of (x,y) in self frame
        @param xcoord, ycoord: coordinate in virtual window (screen -> 1.0 x 1.0 window)
        @param s_width, s_height: screen dimensions
        @param  top_node: root of the sub_model
        """

        if self != top_node:
            (xfath, yfath) = self.father.virt_to_self_frame(xcoord,
                                                            ycoord,
                                                            s_width, s_height,
                                                            top_node)
            xloc = (xfath - self.xloc) / self.wloc
            yloc = (yfath - self.yloc) / self.hloc
            return (xloc, yloc)
        else: # top node
            return(xcoord, ycoord)

    def self_to_virtual_frame(self, xcoord, ycoord, top_node):
        """
        Coordinate change
        """
        if self != top_node:
            xfath = self.xloc + xcoord * self.wloc
            yfath = self.yloc + ycoord * self.hloc
            return self.father.self_to_virtual_frame(xfath, yfath, top_node)
        else:
            return (xcoord, ycoord)

    def v_affinity_coef(self, top_node):
        """
        Affinity ratios cw,ch: local_horizontal_length = screen_horizontal_length * cw
        Similar relation for vertical length.
        @param  top_node: root of the sub_model
        """
        if(self!= top_node):
            (acw, ach) = self.father.v_affinity_coef(top_node)
            return (acw / self.wloc, ach / self.hloc)
        else:
            return (1.0, 1.0)

    def add_macro_subnode(self, name, xcoord, ycoord, width, height):
        """
        Add a macro node as subnode with dimensions
        """
        node = CMacroNode(xcoord, ycoord, width, height, name, self.model)
        self.model.node_dict[name] = node
        node.father = self
        self.sub_nodes.append(node)
        self.model.modified = True
        self.model.notify()
        return node

    def add_simple_node(self, name,  xcoord, ycoord):
        """
        Add a simple node
        """
        node = CSimpleNode(xcoord, ycoord, name, self.model)
        self.model.node_dict[name] = node
        node.father = self
        self.sub_nodes.append(node)
        self.model.simple_node_dict[name] = node
        self.model.modified = True
        self.model.notify()
        return node

    def add_input_node(self, name,  xcoord, ycoord):
        """
        Add input node
        """
        node = CInputNode(xcoord, ycoord, name, self.model)
        self.model.node_dict[name] = node
        node.father = self
        self.sub_nodes.append(node)
        self.model.modified = True
        self.model.notify()
        return node

    def add_copy(self, node):
        """
        add a node of the same type
        """
        nnode = node.copy(self.model)
        self.model.node_dict[nnode.name] = nnode
        nnode.father = self
        if nnode.is_simple():
            self.model.simple_node_dict[nnode.name] = nnode
        self.sub_nodes.append(nnode)
        self.model.modified = True
        self.model.notify()
        return nnode

    def add_transition(self, ori, targ):
        """
        Add a transition

        @param ori: a simple node
        @param targ: a simple node
        """
        # transition between a node and itself are forbidden
        if ori == targ:
            return None

        # new code: at most one transition in each direction
        add = False
        for tlist in self.transitions:
            if len(tlist) == 1:
                trans = tlist[0]
                if (trans.ori ==  ori) and (trans.ext == targ):
                    return None
                if (trans.ori ==  targ) and (trans.ext == ori):
                    ntrans = CTransition(ori, targ)
                    ntrans.macro_node = self
                    tlist.append(ntrans)
                    add = True
            else: # len(tl) == 2
                trans = tlist[0]
                if (trans.ori ==  ori) and (trans.ext == targ):
                    return None
                trans = tlist[1]
                if (trans.ori ==  ori) and (trans.ext == targ):
                    return None
        if not add:
            ntrans = CTransition(ori, targ)
            ntrans.macro_node = self
            self.transitions.append([ntrans])

        if ntrans:
            ori.outgoing_trans.append(ntrans)
            targ.incoming_trans.append(ntrans)
            self.model.transition_list.append(ntrans)
            self.model.modified = True
            self.model.notify()
        return ntrans

    def add_start_node(self, xcoord, ycoord, name = None):
        """
        Add a start node
        """
        nnode = CStartNode(xcoord, ycoord, self.model)
        self.model.node_dict[name] = nnode
        nnode.father = self
        if name:
            nnode.name = name
        else:
            # add a number to have different graphic start nodes
            nnode.name = nnode.name + "%s" % self.count
        self.count = self.count + 1
        self.sub_nodes.append(nnode)
        self.model.modified = True
        self.model.notify()
        return nnode

    def add_trap_node(self, xcoord, ycoord, name = None):
        """
        Add a trap node
        """
        nnode = CTrapNode(xcoord, ycoord, self.model)
        self.model.node_dict[name] = nnode
        nnode.father = self
        if name:
            nnode.name = name
        else:
            # add a number to have different graphic trap nodes
            nnode.name = nnode.name + "%s" % self.count
        self.count = self.count + 1
        self.sub_nodes.append(nnode)
        self.model.modified = True
        self.model.notify()
        return nnode

    def add_perm_node(self, name, xcoord, ycoord):
        """
        Add a perm node
        """
        nnode = CPermNode(xcoord, ycoord, name, self.model)
        self.model.node_dict[name] = nnode
        nnode.father = self
        self.sub_nodes.append(nnode)
        self.model.modified = True
        self.model.notify()
        return nnode



    def draw(self, view, xfr, yfr, wfr, hfr, depth):
        """
        depth is less than depth_max
        @param view: drawing area
        @param xfr: x coordinate of father in virtual screen
        @param yfr: y -
        @param wfr: father's width in virtual screen
        @param hfr: father's height in virtual
        @param depth: depth of the node
        """
        dstyle = view.drawing_style
        # draw node
        dstyle.draw_macro(self, xfr, yfr, wfr, hfr)
        # draw sub graph
        if depth < CMacroNode.depth_max and self.model.show_macro:
            xxr = xfr + self.xloc * wfr
            yyr = yfr + self.yloc * hfr
            w_ratio = wfr * self.wloc
            h_ratio = hfr * self.hloc
            # edges
            for tgr in self.transitions:
                dstyle.draw_transition_group(tgr, xxr, yyr, w_ratio, h_ratio)
            # nodes
            for snode in self.sub_nodes:
                snode.draw(view, xxr, yyr, w_ratio, h_ratio, depth + 1)


    def move(self, v_dx, v_dy, v_size, top_node):
        """
        Move the node - mx_virt, my virt are virtual coordinates of the mouse
        click_loc (pair) is the location of the clic in node's frame
        """
        # don't try to move a root node
        if self == top_node:
            return
        # move in reference frame (father's)
        (ccx, ccy) = self.father.v_affinity_coef(top_node)
        loc_dx = ccx * v_dx
        loc_dy = ccy * v_dy
        # translation vector in reference frame i.e. father's frame
        new_xloc = self.xloc + loc_dx
        new_yloc = self.yloc + loc_dy
        # check limits
        wloc = v_size[0] * ccx
        hloc = v_size[1] * ccy
        delta = v_size[2] * ccy

        if self.model.show_macro:
            wloc = self.wloc
            hloc = self.hloc
        else:
            wloc = v_size[0] * ccx
            hloc = v_size[1] * ccy
        move = False
        if (new_xloc >= 0) and (new_xloc + wloc < 1.0):
            self.xloc = new_xloc
            move = True
        if (new_yloc > delta) and (new_yloc + hloc < 1.0):
            self.yloc = new_yloc
            move = True
        if move:
            self.model.modified = True
            self.model.notify()


    def find_element(self, mox, moy, dstyle, w_coef, h_coef):
        """
        @param mox, moy: mouse coordinate in container frame
        @param dstyle: drawing style
        @param w_coef, h_coef: affinity ratios for view -> container frame
        """
        # width and height of the node in container frame
        if self.model.show_macro:
            wloc = self.wloc
            hloc = self.hloc
        else:
            bb_size = self.accept(dstyle)
            wloc = bb_size[0] * w_coef
            hloc = bb_size[1] * h_coef
        in_node = (mox >= self.xloc) and (mox <= self.xloc + wloc)
        in_node = in_node and (moy >= self.yloc) and (moy <= self.yloc + hloc)
        if in_node:
            if not self.model.show_macro:
                ccx = self.xloc + 0.5 * wloc
                ccy = self.yloc + 0.5 * hloc
                return (self, 0, (ccx, ccy), None)

            # change coordinates and affinity ratio for self frame
            w_coefloc = w_coef / wloc
            h_coefloc = h_coef / hloc
            mxloc = (mox - self.xloc) / wloc
            myloc = (moy - self.yloc) / hloc
            # search sub node
            for snode in self.sub_nodes:
                (nnn, hhh, ccc, ttt) = snode.find_element(mxloc, myloc, dstyle,
                                               w_coefloc, h_coefloc)
                if nnn:
                    # n center coordinates in container frame
                    ccx = self.xloc + ccc[0] * self.wloc
                    ccy = self.yloc + ccc[1] * self.hloc
                    return (nnn, hhh, (ccx, ccy), ttt)


            # self center coordinate in container frame
            ccx = self.xloc + 0.5 * self.wloc
            ccy = self.yloc + 0.5 * self.hloc

            # not in a subnode, find a transition at this level
            trans = self.find_transition(mxloc, myloc, dstyle,
                                         w_coefloc, h_coefloc)
            if trans:
                return (self, 0, (ccx, ccy), trans)

            # not in a subnode or transition- find handler
            v_size = self.accept(dstyle)
            ddx = v_size[3]
            ddy = v_size[4]

            if (mox < self.xloc + ddx) and (moy < self.yloc + ddy):
                return (self, 1, (ccx, ccy), None)
            if (mox > self.xloc + wloc - ddx) and (moy < self.yloc + ddy):
                return (self, 2, (ccx, ccy), None)
            cond = (mox > self.xloc + wloc - ddx)
            cond = cond and (moy > self.yloc + hloc - ddy)
            if cond:
                return (self, 3, (ccx, ccy), None)
            if (mox < self.xloc + ddx) and (moy > self.yloc + hloc - ddy):
                return (self, 4, (ccx, ccy), None)
            return (self, 0, (ccx, ccy), None)
        else:
            return (None, 0, (0, 0), None)

    def find_transition(self, mox, moy, dstyle, w_coef, h_coef):
        """
        Look for transitions pointed by mouse
        No recursive search - transitions are in current node

        """
        for gtr in self.transitions:
            for trans in gtr:
                if trans.is_me(mox, moy, dstyle, w_coef, h_coef):
                    return trans
        return None


    def resize(self, mx_virt, my_virt, handle, screen_w, screen_h, top_node):
        """
        @param  mx_virt, my_virt:  mouse coordinates in virtual window
        @param handle: as determined by find_node
        @param screen_w, screen_h: size of the screen in pixels
        @param top_node: root node of the sub model
        """
        # don't try to resize a root node
        if self == top_node:
            return

        (mx_loc, my_loc) = self.father.virt_to_self_frame(mx_virt, my_virt,
                                                          screen_w, screen_h,
                                                          top_node)
        if handle == 1: # top left corner
            change = False
            new_xloc = mx_loc
            new_wloc = self.xloc + self.wloc - mx_loc
            if new_xloc > 0 and new_wloc > CNode.wmin :
                self.xloc = new_xloc
                self.wloc = new_wloc
                change = True
            new_yloc = my_loc
            new_hloc = self.yloc + self.hloc - my_loc
            if new_yloc > 0 and new_hloc > CNode.hmin :
                self.yloc = new_yloc
                self.hloc = new_hloc
                change = True
            if change:
                self.model.modified = True
                self.model.notify()

        elif handle == 2: # top right corner
            change = False
            new_wloc = mx_loc - self.xloc
            if self.xloc + new_wloc < 1.0 and new_wloc > CNode.wmin :
                self.wloc = new_wloc
                change = True
            new_yloc = my_loc
            new_hloc = self.yloc + self.hloc - my_loc
            if new_yloc > 0 and new_hloc > CNode.hmin :
                self.yloc = new_yloc
                self.hloc = new_hloc
                change = True
            if change:
                self.model.modified = True
                self.model.notify()

        elif handle == 3: # bottom right corner
            change = False
            new_wloc = mx_loc - self.xloc
            if self.xloc + new_wloc < 1.0 and new_wloc > CNode.wmin :
                self.wloc = new_wloc
                change = True
            new_hloc = my_loc - self.yloc
            if self.yloc+new_hloc < 1.0 and new_hloc > CNode.hmin :
                self.hloc = new_hloc
                change = True
            if change:
                self.model.modified = True
                self.model.notify()

        elif handle == 4: # bottom left corner
            change = False
            new_xloc = mx_loc
            new_wloc = self.xloc + self.wloc - mx_loc
            if new_xloc > 0 and new_wloc > CNode.wmin :
                self.xloc = new_xloc
                self.wloc = new_wloc
                change = True
            new_hloc = my_loc - self.yloc
            if self.yloc + new_hloc < 1.0 and new_hloc > CNode.hmin :
                self.hloc = new_hloc
                change = True
            if change:
                self.model.modified = True
                self.model.notify()
        else:
            pass

    def intersect(self, node2, dstyle, nb_trans, w_ratio, h_ratio):
        """
        Gives the the first point where to branch a transition, the gap between two arrows
        and a boolean horizontal true if arrows start from horizontal edge
        @param node2: second node of the transition
        @param dstyle: drawing style
        @param nb_trans: number of transitions to be drawn
        @param w_ratio,h_ratio: dimentions of the screen for fixed size nodes
        """
        if not self.model.show_macro:
            return intersect_simple(self, node2, dstyle, nb_trans,
                                    w_ratio, h_ratio)
        (xc2, yc2) = node2.get_center_loc_coord(dstyle, w_ratio, h_ratio)
        uux = xc2 - (self.xloc + self.wloc / 2.0)
        uuy = yc2 - (self.yloc + self.hloc / 2.0)
        wloc = self.wloc
        hloc = self.hloc
        limit_slope = hloc/wloc

        if uux != 0.0:
            slope = uuy / uux
            if slope <= -limit_slope:
                if uux > 0:
                    side = 1
                else:
                    side = 3
            elif slope >= limit_slope:
                if uux < 0:
                    side = 1
                else:
                    side = 3
            else: # -limit_slope < slope < limit_slope
                if uux > 0:
                    side = 2
                else:
                    side = 4
        else:
            if uuy >= 0 :
                side = 3
            else:
                side = 1

        if side == 1:
            horizontal = True
            gap = wloc / (nb_trans+1)
            six = self.xloc + gap
            siy = self.yloc
            return (six, siy, gap, horizontal)
        if side == 3:
            horizontal = True
            gap = wloc / (nb_trans+1)
            six = self.xloc + gap
            siy = self.yloc + hloc
            return (six, siy, gap, horizontal)
        if side == 2:
            horizontal = False
            gap = hloc / (nb_trans + 1)
            six = self.xloc + wloc
            siy = self.yloc + gap
            return (six, siy, gap, horizontal)
        if side == 4:
            horizontal = False
            gap = hloc / (nb_trans+1)
            six = self.xloc
            siy = self.yloc + gap
            return (six, siy, gap, horizontal)



    def clean(self):
        self.activated = False
        for node in self.sub_nodes:
            node.clean()
        for gtr in self.transitions:
            for trans in gtr:
                trans.clean()

    def clean_code(self):
        """
        clean the code
        """
        for ltr in self.transitions:
            for trans in ltr:
                trans.clock = None
        for node in self.sub_nodes:
            if node.is_macro():
                node.clean_code()

    def accept(self, visitor):
        """
        Standard visitor acceptor
        """
        return visitor.visit_cmacro_node(self)



class CTopNode(CMacroNode):
    """
    A virtual macronode on top of the hierarchy. A model can be a list of hierarchy.
    This artificial node group all the hierarchy. From a graphical point of view, it
    represents the virtual drawing window.
    """
    def __init__(self, name, model):
        CMacroNode.__init__(self, 0.0, 0.0, 1.0, 1.0, name, model)
        self.submodel = False
        self.env_node = None  # for environment interaction in tests
        #nb no father node

    def copy(self):
        """
        Duplicate a topnode - performs a deep copy - reduce dimensions
        The top node is changed into a macro node - the env_node (if any) is not copied.
        """
        node_c = CMacroNode(self.xloc, self.yloc, 0.5, 0.30,
                            self.name, self.model)
        # copy subnodes
        for snode in self.sub_nodes:
            snc = snode.copy()
            node_c.sub_nodes.append(snc)
            snc.father = node_c
        # copy transitions
        for gtr in self.transitions:
            gtr_c = []
            for trans in gtr:
                origin = trans.ori
                origin_c = node_c._find_in_subnodes(origin)
                extremity = trans.ext
                extremity_c = node_c._find_in_subnodes(extremity)
                trc = CTransition(origin_c, extremity_c)
                trc.macro_node = node_c
                trc.event = trans.event
                trc.condition = trans.condition
                trc.action = trans.action
                gtr_c.append(trc)
            node_c.transitions.append(gtr_c)
        return node_c

    def is_for_origin(self):
        return False

    def is_for_extremity(self):
        return False

    def is_top_node(self):
        return True

    def draw(self, view):
        # the TOP node is virtual - so no drawing
        # if there is only one subnode which is a macro - draw it full screen
        dstyle = view.drawing_style
        if self.submodel:
            mno = self.sub_nodes[0]
            w_ratio = 1.0 / mno.wloc
            h_ratio = 1.0 / mno.hloc
            xxr = - mno.xloc * w_ratio
            yyr = - mno.yloc * h_ratio
            mno.draw(view, xxr, yyr, w_ratio, h_ratio, 0)
            return
        # top of a full model
        # transitions
        for tgr in self.transitions:
            if self.submodel:
                dstyle.draw_transition_group(tgr, 0.0, 0.0, 1.0, 1.0,
                                             self.sub_nodes[0])
            else:
                dstyle.draw_transition_group(tgr, 0.0, 0.0, 1.0, 1.0)
        # nodes
        for snode in self.sub_nodes:
            snode.draw(view, 0.0, 0.0, 1.0, 1.0, 1)


    def find_element(self, mox, moy, dstyle):
        """
        @param mox,moy :coordinates of the mouse in local frame (own frame for top node)
        @param dstyle: drawing style used in the view

        Given the window mouse coordinates, return (node, handle, center) where node is the
        node the mouse is in,  handle the handle of the node the mouse is in and c are the coordinates
        of the node center in view.
        If no handle, handle = 0, handle are 1,2,3,4 clockwise numbered from upper left corner
        If no node found returns (None,0,(0,0))
        """
        # if model size two large don't draw => don't search
        nb_snodes = len(self.model.simple_node_dict)
        if  nb_snodes > self.model.max_size:
            return (self, 0, (0, 0), None) # no handle for top node

        if self.submodel:
            #TODO check new version with virtual screen
            mno = self.sub_nodes[0]
            # mouse coordinates in father frame
            mox = mox*mno.wloc + mno.xloc
            moy = moy*mno.hloc + mno.yloc
            # top node coefs in father frame
            w_coef = mno.wloc
            h_coef = mno.hloc
            return mno.find_element(mox, moy, dstyle, w_coef, h_coef)
        w_coef = 1.0
        h_coef = 1.0
        for snode in self.sub_nodes:
            (nnn, hhh, ccc, ttt) = snode.find_element(mox, moy, dstyle,
                                                       w_coef, h_coef)
            if nnn:
                # center in  screen
                ccx = ccc[0] / w_coef
                ccy = ccc[1] / h_coef
                return (nnn, hhh, (ccx, ccy), ttt)
        # no subnode found: try to find a transition at top level
        for trg in self.transitions:
            for trans in trg:
                if trans.is_me(mox, moy, dstyle, w_coef, h_coef):
                    ccx = 0.5 / w_coef
                    ccy = 0.5 / h_coef
                    return (self, 0, (ccx, ccy), trans)
        # no subnode and no transition found
        return (self, 0, (0, 0), None) # no handle for top node


#    def aff_coefs(self, top_node):
#        """
#        Affinity coefficients
#        """
#        return (1.0, 1.0)

    def aff_coef(self, swidth, sheight, top_node):
        """
        Affinity coefficients
        """
        return (1.0 / swidth, 1.0 / sheight)

    def move(self, v_dx, v_dy, v_size, top_node):
        pass # no move for top node


    def add_submodel(self, mnode):
        """
        add a submodel (subtree) with root a macro node (no check performed)
        """
        self.submodel = True
        self.sub_nodes.append(mnode)
        self.model.modified = True

    def accept(self, visitor):
        return visitor.visit_ctop_node(self)

class CTransition(object):
    """
    A guarded transition object
    """
    def __init__(self, origin, extremity):
        """
        @param origin : CNode
        @param extremity : CNode
        """
        self.macro_node = None
        self.ori = origin
        self.ext = extremity
        self.name = ""
        self.event = ""
        self.condition = ""
        self.action = ""
        self.selected = False
        self.search_mark = False
        self.activated = False
        self.fact_ids = [] #list of associated facts id
        self.note = ""
        # for compiler (avoid redondant clause generation)
        self.clock = None
        self.ori_coord = 0.0 # to be set by layout
        self.ext_coord = 0.0

    def set_event(self, event):
        """
        @param event: string
        """
        self.event = event
        self.ori.model.modified = True

    def set_condition(self, cond):
        """
        @param cond : string
        """
        self.condition = cond
        self.ori.model.modified = True

    def set_action(self, act):
        """
        @param act: string
        """
        self.action = act
        self.ori.model.modified = True

    def set_name(self, name):
        """
        @param name: string
        """
        self.name = name
        self.ori.model.modified = True

    def set_note(self, note):
        """
        @param note: string
        """
        self.note = note

    def get_key(self):
        """
        key for storing the transition in dictionaries
        """
        key = self.ori.name + self.ext.name + self.event
        key = key + self.condition + self.action
        return key

    def clean(self):
        """
        Unmark
        """
        self.activated = False

    def get_influencing_places(self):
        """
        find places that influence the condition
        """
        if len(self.condition) == 0:
            return []
        text_c = self.condition + "$"
        reader = ANTLRStringStream(text_c)
        lexer = condexpLexer(reader)
        parser = condexpParser(CommonTokenStream(lexer))
        try:
            influ = parser.sig_bool()
        except:
            return []
        return influ

    def is_me(self, mox, moy, dstyle, w_coef, h_coef):
        """
        Tell if mouse position is closed to transition
        @param mox, moy: mouse coordinates in container coord (local coordinates)
        """
        v_size = self.accept(dstyle)
        dist_max = max(v_size[0], v_size[1])
        # extremities
        (x_or, y_or) = self.ori_coord
        (x_tg, y_tg) = self.ext_coord

        # distance from mouse cursor
        llx = x_tg - x_or
        lly = y_tg - y_or
        norm = sqrt(llx * llx + lly * lly)
        if norm == 0:
            return # must not happen
        llx = llx / norm
        lly = lly / norm
        xxx = mox - x_or
        yyy = moy - y_or
        uuu = llx * xxx + lly * yyy
        dist = (xxx - uuu * llx) * (xxx - uuu * llx)
        dist = dist + (yyy - uuu * lly) * (yyy - uuu * lly)
        dist = sqrt(dist)

        if dist < dist_max:
            # are we in the bounds
            ddx = abs(x_or-x_tg)
            ddy = abs(y_or-y_tg)
            if ddx > 0.05:
                condx =  (abs(mox - x_or) <= ddx)  and (abs(mox - x_tg) <= ddx)
            else:
                condx = True
            if ddy > 0.05:
                condy = (abs(moy - y_or) <= ddy) and (abs(moy - y_tg) <= ddy)
            else:
                condy = True
            return condx and condy
        else:
            return False

    def remove(self):
        """
        remove the transition from its macro node
        """
        lgtr = self.macro_node.transitions
        for gtr in self.macro_node.transitions:
            if self in gtr:
                gtr.remove(self)
                if len(gtr) == 0:
                    lgtr.remove(gtr)
        self.ori.outgoing_trans.remove(self)
        self.ext.incoming_trans.remove(self)
        self.ori.model.transition_list.remove(self)
        self.ori.model.modified = True

    def accept(self, visitor):
        """
        standard accept visitor
        """
        return visitor.visit_ctransition(self)



# helper function

def intersect_simple(node1, node2, dstyle, nb_trans, w_ratio, h_ratio):
    """
    Intersection of a node with a transition
    """
    # simple nodes have constant screen dimensions - convert to local ones
    v_size = node1.accept(dstyle)
    wloc_snode = v_size[0] / w_ratio
    hloc_snode = v_size[1] / h_ratio

    (xc2, yc2) = node2.get_center_loc_coord(dstyle, w_ratio, h_ratio)
    uux = xc2 - (node1.xloc + wloc_snode/2.0)
    uuy = yc2 - (node1.yloc + hloc_snode/2.0)
    if uux != 0.0:
        slope = uuy / uux
        u_slope = v_size[1] / v_size[0]
        if slope <= -u_slope:
            if uux > 0:
                side = 1
            else:
                side = 3
        elif slope >= u_slope:
            if uux < 0:
                side = 1
            else:
                side = 3
        else: # -U_SLOPE < slope < U_SLOPE
            if uux > 0:
                side = 2
            else:
                side = 4
    else:
        if uuy >= 0 :
            side = 3
        else:
            side = 1

    if side == 1: # hight horizontal
        horizontal = True
        if nb_trans ==  1:
            six = node1.xloc + 0.5 * wloc_snode
            gap = 0.0
        elif nb_trans == 2:
            gap = wloc_snode * 0.6
            six = node1.xloc + 0.2 * wloc_snode
        siy = node1.yloc
        return (six, siy, gap, horizontal)
    if side == 3: # low horizontal
        horizontal = True
        if nb_trans ==  1:
            six = node1.xloc + 0.5 * wloc_snode
            gap = 0.0
        elif nb_trans == 2:
            gap = wloc_snode * 0.6
            six = node1.xloc + 0.2 * wloc_snode
        siy = node1.yloc + hloc_snode
        return (six, siy, gap, horizontal)
    if side == 2: # right vertical
        horizontal = False
        if nb_trans ==  1:
            siy = node1.yloc + 0.5 * hloc_snode
            gap = 0.0
        elif nb_trans == 2:
            gap = hloc_snode * 0.6
            siy = node1.yloc + 0.2 * hloc_snode
        six = node1.xloc + wloc_snode
        return (six, siy, gap, horizontal)
    if side == 4: # left vertical
        horizontal = False
        if nb_trans ==  1:
            siy = node1.yloc + 0.5 * hloc_snode
            gap = 0.0
        elif nb_trans == 2:
            gap = hloc_snode * 0.6
            siy = node1.yloc + 0.2 * hloc_snode
        six = node1.xloc
        return (six, siy, gap, horizontal)





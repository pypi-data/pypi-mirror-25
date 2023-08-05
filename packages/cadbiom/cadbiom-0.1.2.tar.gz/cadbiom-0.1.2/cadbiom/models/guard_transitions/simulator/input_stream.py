##
## Filename    : input_stream.py
## Author(s)   : Michel Le Borgne
## Created     : 11/2009
## Revision    :
## Source      :
##
## Copyright 2009 : IRISA/IRSET
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
## In no event shall INRIA be liable to any party for direct, indirect,
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
## Contributor(s): Geoffroy Andrieux, Nolwenn Le Meur
##

"""
Stream to manage input/clocks during a simulation
"""

import string
from string import  atoi
from cadbiom.models.guard_transitions.simulator.simul_exceptions import \
                               SimulException, SimulStopException

class InputStream(object):
    """
    General class for all input buffers. Input buffers manage dynamic discrete systems inputs
    It has essentially two methods: next_input which deliver an input as a list of activated inputs
    and rewind which initializes the buffer
    """
    def __init__(self):
        self.current_index = 0    # line pointer in buffer
        self.max_index = 0        # size of input buffer

    def next_input(self):
        """
        returns a list of activated inputs (others are inactivated)
        """
        return []

    def rewind(self):
        """
        rewind the input stream for a new simulation
        """
        self.current_index = 0

    def is_all_read(self):
        """
        test end of buffer
        """
        return self.current_index == self.max_index



class CodedStream(InputStream):
    """
    InputStream where inputs are described with a language
    """
    def __init__(self):
        self.current_index = 0    # line pointer in buffer
        self.max_index = 0        # size of input buffer
        self.input_buffer = []    # main buffer
        self.nb_inputs = 0        # number of inputs per line
        self.input_names = []     # list of input names ordered as in first line
        self.label_table = dict() # label name -> address
        self.block_count = None


    def next_input(self):
        """
        Produce the next input as a list of activated inputs (including clocks)
        """
        # end of buffer
        if self.current_index >= self.max_index:
            self.__load_input_buffer()

        line_split = self.input_buffer[self.current_index].split()

        # line analysis: command
        while line_split[0][0] == '$':
            self.__execute_command(line_split) # may change current index
            line_split = self.input_buffer[self.current_index].split()

        # ordinary input
        if len(line_split) != self.nb_inputs:
            mess = "Number of inputs different from nb of declared inputs"
            raise SimulException(mess)
        out = []
        for i in range(self.nb_inputs):
            val = int(line_split[i])
            if val == 1:
                out.append(self.input_names[i])
        self.current_index = self.current_index + 1
        return out

    def __execute_command(self, line_split):
        """
        implements command execution for coded steam
        """
        command = line_split[0][1:]
        if command == 'label':
            self.label_table[line_split[1]] = (self.current_index, 0)
            self.current_index = self.current_index + 1
            return

        elif command == 'repeat':
            label = line_split[1]
            if not self.label_table.has_key(label): # label doesn't exist
                raise SimulException("Unknown label line %s"%self.current_index)
            (index, count) = self.label_table[label]
            time = atoi(line_split[2]) # number of loops
            if count < time:
                self.current_index = index+1
                self.label_table[label] = (index, count+1)
            else:
                self.current_index = self.current_index + 1
                self.label_table[label] = (index, 0)
            return

        elif command == 'block':
            if self.current_index == 1:
                mess = "Input Syntax error line %$: Block on first line,"
                mess = mess + " value must be before" % self.current_index
                raise SimulException(mess)
            if self.block_count == None:
                self.block_count = atoi(line_split[1])
            if self.block_count == 0: # end of block
                self.block_count = None
                self.current_index = self.current_index + 1
            elif self.block_count == -1: # continuous block
                self.current_index = self.current_index - 1
            else: # limited block continues
                self.current_index = self.current_index - 1
                self.block_count = self.block_count - 1

        elif command == 'stop':
            raise SimulStopException()

        else:
            raise SimulException("Unknown command line %s"%self.current_index)

    def __load_input_buffer(self):
        """
        not implemented - for partial loading ??
        """
        raise SimulStopException()

    def rewind(self):
        """
        as it says
        """
        self.current_index = 1
        self.block_count = None

    def is_all_read(self):
        """
        test end of buffer
        """
        return self.current_index == self.max_index



class CFileInput(CodedStream):
    """
    Input buffer with input description in file
    """
    def __init__(self, filename):
        self.file = open(filename, 'r')
        self.input_buffer = self.file.readlines() # read all the lines
        self.max_index = len(self.input_buffer)
        self.current_index = 1               # line 0 is for input description
        line = string.strip(self.input_buffer[0]) # get line 0
        line_split = string.split(line)
        if line_split[0] != "$inputs":
            raise SimulException()
        else:
            self.input_names = []            # collect input names
            for name in line_split[1:]:
                self.input_names.append(name)
            self.nb_inputs = len(self.input_names)
        self.label_table = dict()
        self.block_count = None



class ActInput(InputStream):
    """
    Input buffer where input names are enumerated in a file (pure input or scenario)
    or
    """
    def __init__(self, filename = None, inlist = []):
        if filename:
            ifile = open(filename, 'r')
            self.input_buffer = ifile.readlines() # read all the lines
            ifile.close()
        else:
            self.input_buffer = inlist
        self.max_index = len(self.input_buffer)
        if self.input_buffer[0][0] == '%': # pure input file
            self.current_index = 0
            self.init_index = 0
        else: # scenario
            self.current_index = 1
            self.init_index = 1

    def next_input(self):
        """
        Produce the next input as a list of activated inputs (including clocks)
        coded in file as "% h1 i2 h3"
        """
        # end of buffer
        if self.current_index >= self.max_index:
            raise SimulStopException()
        cin =  self.input_buffer[self.current_index]
        self.current_index += 1
        return cin.split()[1:]

    def rewind(self):
        self.current_index = self.init_index


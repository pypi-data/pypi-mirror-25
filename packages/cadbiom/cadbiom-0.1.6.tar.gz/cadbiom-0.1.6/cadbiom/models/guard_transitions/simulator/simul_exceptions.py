## Filename    : simul_exceptions.py
## Author(s)   : Michel Le Borgne
## Created     : 04/2010
## Revision    : 
## Source      : 
##
## Copyright 2010 : IRISA/INRIA
##
## This library is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published
## by the Free Software Foundation; either version 2.1 of the License, or
## any later version.
##
## This library is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY, WITHOUT EVEN THE IMPLIED WARRANTY OF
## MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.  The software and
## documentation provided here under is on an "as is" basis, and INRIA has
## no obligations to provide maintenance, support, updates, enhancements
## or modifications.
## In no event shall INRIA be liable to any party for direct, indirect,
## special, incidental or consequential damages, including lost profits,
## arising out of the use of this software and its documentation, even if
## INRIA have been advised of the possibility of such damage.  See
## the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this library; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
##
## The original code contained here was initially developed by:
##
##     Michel Le Borgne.
##     IRISA/INRIA
##     Symbiose team
##     IRISA  Campus de Beaulieu
##     35042 RENNES Cedex, FRANCE 
##     
##
## Contributor(s): Geoffroy Andrieux, Nolwenn Le Meur
##
"""
Simulator exceptions
"""

class SimulException(Exception):
    """
    Exceptions for simulation management
    """
    def __init__(self, mess):
        self.message = mess
        
    def __str__(self):
        return self.message

class SimulStopException(SimulException):
    """
    End of a simulation (mostly end of input)
    """
    def __init__(self):
        self.message = 'STOP'
    
    def __str__(self):
        return self.message
    
class SimulPropViolation(SimulException):
    """
    Used when an invariant property or a variant one if violated
    """
    def __init__(self, mess, prop):
        self.message = mess + " : "+prop
    
    def __str__(self):
        return self.message


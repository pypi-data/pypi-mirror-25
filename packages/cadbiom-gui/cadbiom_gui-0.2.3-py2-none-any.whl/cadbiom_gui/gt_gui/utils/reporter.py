##
## Filename    : reporter.py
## Author(s)   : Michel Le Borgne
## Created     : 10/2009
## Revision    : 
## Source      : 
##
## Copyright 2012 : IRISA/IRSET
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
## Contributor(s): Geoffroy Andrieux, Nolwenn Le Meur
##

"""
To adapt message handling to different environment we use reporters
"""

# simple reporter
class SimpleErrorReporter(object):
    """
    Minimum reporter
    """
    def __init__(self):
        self.error = False
        
    
    def display(self, mess):
        """
        Set the error attribute and print the message
        """
        self.error = True
        print '\n>> '+mess



class ErrorReporter(object):
    """
    Usefull for some tests where a header message is informative
    display messages in a textviewer
    """
    def __init__(self, tview, model):
        self.display_window = tview # must be a textviewer
        self.mod_identifier = model
        self.text = ""
        self.err_msg = False
        
    def display(self, hdr, mes = ""):
        """
        build the message from mess and hdr
        """
        buf = self.display_window.get_buffer()
        iter_end = buf.get_end_iter()
        msg = self.mod_identifier+ ':: '+ hdr +'  ' + mes + '\n'
        buf.insert(iter_end, msg)
        self.text = msg
        self.err_msg = True
        
class CompilReporter(object):
    """
    register errors and info - must be checked after compilation
    memory contains all the messages
    """
    def __init__(self):
        self.error = False
        self.info = False
        self.use_context = True
        self.context = ""
        self.memory = ""
        self.indent = "       "
    
    def set_context(self, mess):
        """
        Context message: describe the context (transition for exp.)
        """
        self.context = mess
        self.use_context = False
        
    def display(self, mess, supl = ""):
        """
        Combine the message with context information
        """
        if not self.use_context:
            self.memory = self.memory+'\n\n'+self.context
            self.use_context = True
        self.error = True
        self.memory = self.memory+'\n'+ self.indent + mess +'  '+supl
        
    def display_info(self, mess, supl = ""):
        """
        For information
        """
        if not self.use_context:
            self.memory = self.memory+'\n\n'+self.context
            self.use_context = True
        self.info = True
        self.memory = self.memory+'\n'+ self.indent + mess +'  '+supl   

    def reset(self):
        """
        RAZ
        """
        self.error = False
        self.info = False
        self.use_context = True
        self.context = ""
        self.memory = ""



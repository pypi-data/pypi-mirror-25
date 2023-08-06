##
## Filename    : fileHandling.py
## Author(s)   : Michel Le Borgne
## Created     : 2/2/2012
## Revision    : 
## Source      : 
##
## Copyright 2009 - 2012 : IRISA/IRSET
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
##FILE_CHOOSER_ACTION_SAVE
## Contributor(s): Geoffroy Andrieux
##

from gtk import FileChooserDialog, FileFilter, \
    STOCK_CANCEL, RESPONSE_CANCEL, RESPONSE_OK, \
    FILE_CHOOSER_ACTION_SAVE, STOCK_SAVE, \
    FILE_CHOOSER_ACTION_OPEN, STOCK_OPEN


class FileChooser(FileChooserDialog):
    """
    Create a customed file chooser
    """
    def __init__(self, title, filter_name, filter_pattern, save_window=True):
        """Open a custom file chooser.

        if save_window is False, an open window will be initialized
        """
        if save_window:
            FileChooserDialog.__init__(
                self, title, None, FILE_CHOOSER_ACTION_SAVE,
                (STOCK_CANCEL, RESPONSE_CANCEL, STOCK_SAVE, RESPONSE_OK)
            )
        else:
            FileChooserDialog.__init__(
                self, title, None, FILE_CHOOSER_ACTION_OPEN,
                (STOCK_CANCEL, RESPONSE_CANCEL, STOCK_OPEN, RESPONSE_OK)
            )

        self.set_default_response(RESPONSE_OK)
                       
        #add a filter to see only files for BioSignal (*.sig)
        filter = FileFilter()
        filter.set_name(filter_name)
        filter.add_pattern(filter_pattern)
        self.add_filter(filter)
        
        #add a filter to see all
        no_filter = FileFilter()
        no_filter.set_name("all")
        no_filter.add_pattern("*")
        self.add_filter(no_filter)
        
    def do_action(self, action):
        """
        Action following file selection
        """
        response = self.run()
        if response == RESPONSE_OK:
            action(self.get_filename())
        elif response == RESPONSE_CANCEL:
            pass
        self.destroy()

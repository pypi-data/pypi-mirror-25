##
## Filename    : notebookUtils.py
## Author(s)   : Michel Le Borgne
## Created     : 4/2010
## Revision    : 
## Source      : 
##
## Copyright 2009-2012 : IRISA/IRSET
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
Utilities for notebooks
"""
import gtk

def add_icon_to_button(button):
    """
    add a close buttpn to tab
    """
    #hbox
    iconBox = gtk.HBox(False, 0)
    #empty image
    image = gtk.Image()
    #get close button icon
    image.set_from_stock(gtk.STOCK_CLOSE,gtk.ICON_SIZE_MENU)
    #remove relief
    gtk.Button.set_relief(button,gtk.RELIEF_NONE)
    #get button properties
    settings = gtk.Widget.get_settings(button)
    # w and h = dimensions
    (w,h) = gtk.icon_size_lookup_for_settings(settings,gtk.ICON_SIZE_MENU)
    #we modify dimensions
    gtk.Widget.set_size_request(button, w + 4, h + 4)
    image.show()
    #put the image in the box
    iconBox.pack_start(image, True, False, 0)
    #put the box in the button
    button.add(iconBox)
    iconBox.show()
    return 

def create_custom_tab(text):
    """
    Customized tab with label and close button
    """
    #event box creation
    eventBox = gtk.EventBox()
    #hbox
    tab_box = gtk.HBox(False, 2)
    #label "text"
    tab_label = gtk.Label(text)
    #buton
    tab_button=gtk.Button()

    #add the close icon to button
    add_icon_to_button(tab_button)

    eventBox.show()
    tab_button.show()
    tab_label.show()
    #connect label and button to the box
    tab_box.pack_start(tab_label, False)
    tab_box.pack_start(tab_button, False)

    tab_box.show_all()
    #add the box to eventbox
    eventBox.add(tab_box)
    return (eventBox, tab_button)


## Filename    : charter_info.py
## Author(s)   : Geoffroy Andrieux
## Created     : 03/2010
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
##     IRISA
##     Symbiose team
##     IRISA  Campus de Beaulieu
##     35042 RENNES Cedex, FRANCE
##
##
## Contributor(s): Michel Le Borgne, Nolwenn Le Meur
##
"""
Widget for displaying informations on the elements of the model
"""
import gtk

from utils.text_page import TextEditConfig, TextPage

import pkg_resources

class CharterInfo(gtk.Frame):
    """
    windows of charter_info
    """
    def __init__(self, frame):
        self.frame = frame
        self.controler = None
        self.fact_window = None
        self.model_info = ModelInfo(self)
        self.node_info = NodeInfo(self)
        self.trans_info = TransInfo(self)

        self.current_info = self.model_info

    def set_controler(self, new_controler):
        """
        Associate a controler in a MVC pattern
        """
        if self.controler:
            self.controler.detach("current_change", self)
        self.controler = new_controler
        self.controler.attach("current_change", self)

    def display(self):
        """
        Show all
        """
        chi = self.frame.get_child()
        if chi:
            self.frame.remove(chi)

        self.frame.add(self.current_info.frame)
        self.frame.show()


    def switch_to(self, new_info):
        """
        callback when info change
        """
        if self.current_info == None:
            self.current_info = new_info
            self.display()
        else:
            self.current_info.warn_change()
            self.current_info = new_info
            self.display()


    def update(self, node, transition):
        """
        Used if registered as an observer
        """
        if (node == None and transition == None):
            self.model_info.update(self.controler)
            self.switch_to(self.model_info)

        elif node != None and transition == None:
            if node.is_top_node():
                self.model_info.update(self.controler)
                self.switch_to(self.model_info)
            else:
                self.node_info.update(node)
                self.switch_to(self.node_info)

        else :
            self.trans_info.update(transition)
            self.switch_to(self.trans_info)



    def enter_callback(self, widget, entry):
        """
        return the entry
        """
        entry_text = entry.get_text()
        print "Entry contents: %s\n" % entry_text

    def has_transition(self):
        """
        As it says
        """
        return self.current_info.has_transition()


class ModelInfo(object):
    """
    Object used as a model - store informations
    """
    def __init__(self, cin):
        template = pkg_resources.resource_filename(
            __name__,
            "chart_glade/model_info.glade"
        )
        self.page = gtk.glade.XML(template)
        wid = self.page.get_widget("model_frame")
        self.frame = wid.get_child()
        wid.remove(self.frame)
        self.info = cin

        self.name = self.page.get_widget("model_entry")
        self.name.connect("changed", self.set_model)
        self.name.set_editable(True)

        self.nb_nodes = self.page.get_widget("node_entry")
        self.nb_nodes.set_editable(False)
        self.nb_nodes.set_sensitive(False)

        self.nb_trans = self.page.get_widget("trans_entry")
        self.nb_trans.set_editable(False)
        self.nb_trans.set_sensitive(False)

    def set_model(self, widget):
        """
        As it says
        """
        self.model.name = self.name.get_text()
        self.model.notify()

    def warn_change(self):
        """
        As it says
        """
        pass

    def update(self, controler):
        """
        when used as an observer
        """
        self.model = controler.model
        self.name.set_text(controler.model.name)
        nodes = str(len(self.model.simple_node_dict.keys()))
        trans = str(len(self.model.transition_list))
        self.nb_nodes.set_text(nodes)
        self.nb_trans.set_text(trans)

    def has_transition(self):
        """
        As it says
        """
        return None



class NodeInfo(object):
    """
    A componant of ModelInfo used for nodes
    """
    def __init__(self, cin):
        template = pkg_resources.resource_filename(
            __name__,
            "chart_glade/node_info.glade"
        )
        self.page = gtk.glade.XML(template)
        wid = self.page.get_widget("node_frame")
        self.frame = wid.get_child()
        wid.remove(self.frame)
        self.info = cin

        self.name = self.page.get_widget("node_entry")
        self.name.connect("changed", self.set_node)

    def set_node(self, widget):
        """
        As it says
        """
        self.node.set_name(self.name.get_text())
        self.node.model.notify()

    def warn_change(self):
        """
        As it says
        """
        pass

    def update(self, node):
        """
        Used when registered as an observer
        """
        if node:
            self.node = node
            self.name.set_text(node.name)

    def has_transition(self):
        """
        As it says
        """
        return None

class TransInfo(object):
    """
    A component of ModelInfo used for transitions
    """
    def __init__(self, cin):

        template = pkg_resources.resource_filename(
            __name__,
            "chart_glade/trans_info.glade"
        )
        self.page = gtk.glade.XML(template)
        wid = self.page.get_widget("trans_frame")
        self.frame = wid.get_child()
        wid.remove(self.frame)
        self.info = cin # owner
        self.note_window = None

        self.name = self.page.get_widget("trans_entry")
        self.name.set_editable(False)
        self.evt = self.page.get_widget("evt_entry")
        self.cond = self.page.get_widget("cond_entry")
        self.noteb = self.page.get_widget("note")
        self.show = self.page.get_widget("butshow")

        self.name.connect("changed", self.set_trans)
        self.evt.connect("changed", self.set_trans)
        self.cond.connect("changed", self.set_trans)
        self.noteb.connect("clicked", self.set_note)

    def set_trans(self, widget):
        """
        As it says
        """
        if self.lock:
            return
        else:
            self.trans.set_name(self.name.get_text())
            self.trans.set_event(self.evt.get_text())
            self.trans.set_condition(self.cond.get_text())
            self.trans.ori.model.notify()

    def warn_change(self):
        """
        As it says
        """
        self.save_note(None)

    def update(self, trans):
        """
        When registered as an observer
        """
        if trans:
            self.lock = True
            self.trans = trans
            self.name.set_text(trans.ori.name+'->'+trans.ext.name)
            self.evt.set_text(trans.event)
            self.cond.set_text(trans.condition)
            self.trans = trans # for fact association management
            self.lock = False

    def has_transition(self):
        """
        As it says
        """
        return self.trans

    def set_note(self, widget):
        """
        Associate a text note to a transition
        """
        trans = self.trans
        self.note_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.note_window.connect("destroy", self.save_note)
        self.note_window.set_title("notes: "+trans.ori.name+"->"+trans.ext.name)
        self.note_window.set_position(gtk.WIN_POS_CENTER)
        self.note_window.set_keep_above(True)
        self.note_window.set_default_size(600, 800)
        ed_conf = TextEditConfig()
        self.note_text_page = TextPage(None, ed_conf)
        self.note_text_page.set_text(trans.note)
        self.note_window.add(self.note_text_page)
        self.note_window.show_all()
        return

    def save_note(self, widget):
        """
        register the note
        """
        if self.note_window:
            text = self.note_text_page.get_text()
            self.trans.note = text
            self.trans.ori.model.modified = True
            self.note_window.destroy()
            self.note_window = None

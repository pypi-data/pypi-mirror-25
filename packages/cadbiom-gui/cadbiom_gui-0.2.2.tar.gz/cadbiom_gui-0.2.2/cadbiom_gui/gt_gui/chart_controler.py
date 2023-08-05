## Filename    : chart_controler.py
## Author(s)   : Michel Le Borgne
## Created     : 4/3/2010
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
##     http:
##     mailto:
##
## Contributor(s): Geoffroy Andrieux, Nolwenn Le Meur
##
"""
Main gui controler with auxiliary classes
"""
import itertools as it
from string import ascii_uppercase
from math import sqrt
from gtk.gdk import Cursor, ARROW, BOTTOM_LEFT_CORNER, BOTTOM_RIGHT_CORNER,\
                    TOP_LEFT_CORNER, TOP_RIGHT_CORNER, LINE_ON_OFF_DASH
from cadbiom_gui.gt_gui.graphics.drawing_style import Arrow


import gtk

LSIGNALS = ["current_change", "edit_node"]

class ChartClipboard(object):
    """
    A clipboard to be shared by different controlers
    """
    def __init__(self):
        self.clip_node = None

    def put_node(self, node):
        """
        register a chart model node in the clipboard
        """
        self.clip_node = node

    def get_node(self):
        """
        retrieve the current node in the clipboard
        """
        node = self.clip_node
        self.clip_node = None
        return node

    def has_element(self):
        """
        test if the clipboard has a registered node
        """
        if self.clip_node:
            return True
        else:
            return False

    def has_macro(self):
        """
        test if the clipboard has a registered macro node
        """
        if  self.clip_node:
            return self.clip_node.is_macro()
        else:
            return False

class ChartControler(object):
    """
    Implement a controler for graphical views
    """

    cursors = []
    cursors.append(Cursor(ARROW))
    cursors.append(Cursor(TOP_LEFT_CORNER))
    cursors.append(Cursor(TOP_RIGHT_CORNER))
    cursors.append(Cursor(BOTTOM_RIGHT_CORNER))
    cursors.append(Cursor(BOTTOM_LEFT_CORNER))

    def __init__(self, model, cli):
        self.model = model
        # mouse role
        self.mouse_role = "select"
        self.current_node = None
        self.current_handle = 0
        # coordinate of last click in virtual screen 1x1
        self.m_vscreen_coord = None
        self.current_transition = None
        self.lastx = 0 # coordinates of last click in view
        self.lasty = 0
        self.clipboard = cli
        self.drawing_style = None
        self.signal_dict = dict()
        for sig in LSIGNALS:
            self.signal_dict[sig] = []
        self.edit_window = None

        self.gen_name = self.nodes_names_generator()

    def attach(self, signal, obs):
        """
        Register an observer on a signal list
        @param signal: name of the signal
        @param obs: the observer
        """
        lobs = self.signal_dict[signal]
        if not obs in lobs:
            lobs.append(obs)

    def detach(self, signal, obs):
        """
        Remove an observer from a signal list
        """
        self.signal_dict[signal].remove(obs)

    def notify(self, signal):
        """
        Emit a signal
        @param signal: name of the signal
        """
        lobs = self.signal_dict[signal]
        if signal == "current_change":
            for obs in lobs:
                obs.update(self.current_node, self.current_transition)
        elif signal == "edit_node":
            for obs in lobs:
                obs.update(self.current_node)
        else:
            raise Exception("Chart_controler: Unknown signal")

    def set_view(self, view):
        """
        As it says
        """
        self.view = view

    def set_mouse_role(self, role):
        """
        As it says
        """
        self.mouse_role = role


    def button_press(self, widget, event):
        """
        Action when a mouse button is pressed
        """
        self.lastx = event.x
        self.lasty = event.y

        # cursor coordinates in virtual screen 1x1
        xloc = event.x/self.view.draw_width
        yloc = event.y/self.view.draw_height
        self.m_vscreen_coord = (xloc, yloc)

        # we are always in a node, which one?
        if self.current_node:
            self.current_node.selected = False
        if self.current_transition:
            self.current_transition.selected = False

        (node, handle, center, trans) = self.model.find_element(
                                            self.m_vscreen_coord,
                                            self.drawing_style)
        # we found the root of the sub_model - no resizing
        if node == self.model.get_root():
            handle = 0
        self.current_handle = handle
        self.current_node = node
        node.selected = True
        self.current_node_center = center
        if trans:
            node.selected = False
            trans.selected = True
            self.current_transition = trans
        else:
            self.current_transition = None

        # notify what we have found (red color for selected element)
        self.notify("current_change")
        self.model.notify()
        # action (depending on button and event type)
        if event.type == gtk.gdk._2BUTTON_PRESS: # double click desactivated
            return
#            self.mouse_role = 'select'
#            if self.current_node:
#                if self.current_node.is_macro():
#                    self.notify("edit_node")

        if event.button == 1:
            if self.mouse_role == 'select':
                if node: # got a node
                    if handle != 0: # we get a handle => resizing
                        self.mouse_role = 'resizing'
                    else:
                        self.mouse_role = 'moving'
            else:
                pass
        elif event.button == 3:
            self.context_menu(event)


    def context_menu(self, event):
        """
        Menu appearing on right click
        """
        menu = gtk.Menu()
        node = self.current_node
        transition = self.current_transition
        # Create menu-item copy for nodes only
        if not transition:
            buf = "Copy"
            menu_items = gtk.MenuItem(buf)
            menu.append(menu_items)
            menu_items.connect("activate", self.menuitem_response,
                               buf, node, transition)
            menu_items.show()
        # Create menu-item cut
        if transition or node != self.model.get_root():
            buf = "Cut"
            menu_items = gtk.MenuItem(buf)
            menu.append(menu_items)
            menu_items.connect("activate", self.menuitem_response,
                               buf, node, transition)
            menu_items.show()
        # Create menu-item paste
        buf = "Paste"
        menu_items = gtk.MenuItem(buf)
        menu.append(menu_items)
        if self.clipboard.has_element():
            menu_items.connect("activate", self.menuitem_response,
                               buf, node, transition)
        else:
            menu_items.set_sensitive(False)
        menu_items.show()
        # Create menu item paste component
        buf = "Paste components"
        menu_items = gtk.MenuItem(buf)
        menu.append(menu_items)
        if self.clipboard.has_macro():
            menu_items.connect("activate", self.menuitem_response,
                                buf, node, transition)
        else:
            menu_items.set_sensitive(False)
        menu_items.show()

        menu.popup(None, None, None, 3, event.time)

    def menuitem_response(self, widget, buf, node, transition):
        """
        Callback for the preceding menu
        """
        if buf == 'Copy':
            if not transition:
                cnode = node.copy()
                self.clipboard.put_node(cnode)
        elif buf == 'Cut':
            if transition:
                transition.remove()
                node.model.notify()
            else:
                node.remove()
                self.clipboard.put_node(node)
        elif buf == 'Paste':
            if self.clipboard.has_element() and node.is_macro():
                pnode = self.clipboard.get_node()
                node.sub_nodes.append(pnode)
                pnode.father = node
                pnode.set_model(node.model)
                # renumber start and trap nodes (add a number)
                if pnode.is_start() or pnode.is_trap():
                    pnode.name = pnode.name+"%s" % node.count
                    node.count = node.count + 1
                # coordinates in new node
                pnode.xloc = self.m_vscreen_coord[0]
                pnode.yloc = self.m_vscreen_coord[1]
                node.model.modified = True
                node.model.notify()
        elif buf == 'Paste components':
            if self.clipboard.has_element() and node.is_macro():
                pnode = self.clipboard.get_node()
                if pnode.is_macro():
                    # add nodes
                    for snode in pnode.sub_nodes:
                        node.sub_nodes.append(snode)
                        snode.father = node
                        snode.set_model(node.model)
                        # renumber start and trap nodes (add a number)
                        if snode.is_start() or snode.is_trap():
                            snode.name =  snode.name+"%s" % node.count
                            node.count = node.count + 1
                    # add transition groups
                    for gtr in pnode.transitions:
                        node.transitions.append(gtr)
                        for trans in gtr:
                            trans.macro_node = node
                    node.model.modified = True
                    node.model.notify()

    def button_release(self, widget, event):
        """
        callback when a mouse button is released
        """
        # rubout last click characteristics
        if self.mouse_role == 'select':
            return

        elif self.mouse_role == "resizing" or self.mouse_role == "moving" :
            self.view.window.set_cursor(ChartControler.cursors[0])
            self.mouse_role = "select"

        elif self.mouse_role == "new_trans":
            if self.current_node:
                self.new_transition(event.x, event.y)

        else: # assume node creation
            if self.current_node:
                if self.current_node.is_macro():
                    self.new_node(self.mouse_role)

    def new_node(self, type):
        """
        creation of a new node
        @param type: type of the node (string)
        """
        xnode = self.m_vscreen_coord[0]
        ynode = self.m_vscreen_coord[1]
        if type == 'simple':
            self.current_node = self.current_node.add_simple_node(
                next(self.gen_name),
                xnode, ynode)
        elif type == 'macro':
            self.current_node = self.current_node.add_macro_subnode(
                next(self.gen_name),
                xnode,
                ynode,
                0.25, 0.25)
        elif type == 'start':
            self.current_node = self.current_node.add_start_node(xnode, ynode)
        elif type == 'trap':
            self.current_node = self.current_node.add_trap_node(xnode, ynode)
        elif type == 'perm':
            self.current_node = self.current_node.add_perm_node(
                next(self.gen_name),
                xnode, ynode)
        elif type == 'input':
            self.current_node = self.current_node.add_input_node(
                next(self.gen_name),
                xnode, ynode)
        elif type == 'env':
            self.current_node = self.current_node.add_env_node(
                next(self.gen_name),
                xnode, ynode,
                0.25, 0.25)
        else: # bug!
            print ' new_node:UNKNOWN TYPE:', type
            return
        self.current_transition = None
        self.current_handle = 0
        self.m_vscreen_coord = (0.0, 0.0)
        self.notify("current_change")
        self.view.window.set_cursor(ChartControler.cursors[0])
        self.mouse_role = "select"

    def nodes_names_generator(self):
        """Return a generator of names for new nodes.

        Names are generated in lexicographic order.
        """
        for size in it.count(start=1):
            for tpl in it.combinations(ascii_uppercase, size):
                yield "".join(tpl)

    def new_transition(self, xmo, ymo):
        """
        @param xmo, ymo: int mouse screen coordinates
        """
        # are we in a node?
        xloc = xmo / self.view.draw_width
        yloc = ymo / self.view.draw_height
#        w_coef = 1.0/self.view.draw_width
#        h_coef = 1.0/self.view.draw_height
        (node, handle, center, trans) = self.model.find_element((xloc, yloc),
                                                            self.drawing_style)
        if not node: # no extremity (never happens)
            self.view.window.set_cursor(ChartControler.cursors[0])
            self.mouse_role = "select"
            self.model.notify() # rubout the draft transition
            return
        # are we in same container
        if self.current_node.father != node.father:
            self.view.window.set_cursor(ChartControler.cursors[0])
            self.mouse_role = "select"
            self.model.notify() # rubout the draft transition
            return
        # we are in extremity node - current node is origin node
        # is origin node correct and extremity node correct
        if self.current_node.is_for_origin() and node.is_for_extremity():
            trans = self.current_node.father.add_transition(self.current_node,
                                                          node)
            if trans:
                self.current_node.selected = False
                self.current_node = None
                self.m_vscreen_coord = (0.0, 0.0)
                self.current_transition = trans
                trans.selected = True
                self.notify("current_change")
                self.model.notify()
                self.view.window.set_cursor(ChartControler.cursors[0])
                self.mouse_role = "select"
            else:
                self.view.window.set_cursor(ChartControler.cursors[0])
                self.mouse_role = "select"
                self.model.notify() # rubout the draft transition
        else:
            self.view.window.set_cursor(ChartControler.cursors[0])
            self.mouse_role = "select"
            if self.current_node:
                self.current_node.selected = False
            self.model.notify() # rubout the draft transition
            return


    def motion_notify(self, widget, event):
        """
        Callback when moving window
        """
        swi = self.view.draw_width
        she = self.view.draw_height

        # transform mouse coordinates to virtual screen 1.0 x 1.0
        xvirt = event.x / swi
        yvirt = event.y / she

        if self.mouse_role == 'select':
            (node, handle, center, trans) = self.model.find_element(
                                                            (xvirt, yvirt),
                                                            self.drawing_style)
            if node == self.model.get_root():
                handle = 0
            # detect a new handle
            if handle != self.current_handle:
                self.current_handle = handle
                self.view.window.set_cursor(ChartControler.cursors[handle])

        elif self.mouse_role == 'resizing':
            self.current_node.resize(xvirt, yvirt, self.current_handle,
                                     swi, she, self.model.get_root())

        elif self.mouse_role == 'moving':
            v_dx = xvirt - self.m_vscreen_coord[0]
            v_dy = yvirt - self.m_vscreen_coord[1]
            v_size = self.current_node.accept(self.drawing_style)
            self.current_node.move(v_dx, v_dy, v_size, self.model.get_root())
            self.m_vscreen_coord = (xvirt, yvirt)
        elif self.mouse_role == 'new_trans':
            if self.current_node:
                self.draft_transition(event.x, event.y)
        else:
            pass


    def draft_transition(self, xmo, ymo):
        """
        draw a transition arrow in dotted line
        @param xmo,ymo: mouse coordinates
        """
        view = self.view
        self.model.notify()
        xr1 = int(self.current_node_center[0]*self.view.draw_width)
        yr1 = int(self.current_node_center[1]*self.view.draw_height)

        # graphic context
        pixmap = view.pixmap
        grc = view.window.new_gc()
        grc.set_line_attributes(1, LINE_ON_OFF_DASH, 0, 0)
        # line
        pixmap.draw_line(grc, xr1, yr1, int(xmo), int(ymo))
        # arrow
        unx = xmo - xr1
        uny = ymo - yr1
        norm = sqrt(unx ** 2 + uny ** 2)
        if norm != 0:
            unx = unx / norm
            uny = uny / norm
            arr = Arrow()
            arr.draw(view, (unx, uny), (xmo, ymo))
        grc = view.window.new_gc()
        view.window.draw_drawable(grc, view.pixmap, 0, 0, 0, 0,
                                  view.draw_width, view.draw_height)

#    def edit_constraints(self):
#        lang = 'biosignal'
#        ed_conf = TextEditConfig()
#        self.edit_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
#        self.edit_window.connect("destroy", self.save_constraints)
#        self.edit_window.set_title("Constraints: "+self.model.name)
#        self.edit_window.set_position(gtk.WIN_POS_CENTER)
#        self.edit_window.set_keep_above(True)
#        self.edit_window.set_default_size(600,800)
#
##        scroll = gtk.ScrolledWindow()
##        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
##        scroll.set_shadow_type(gtk.SHADOW_IN)
##        self.edit_window.add(scroll)
#
#        self.text_page = TextPage(lang, ed_conf)
#        self.text_page.set_text(self.model.constraints)
#        self.edit_window.add(self.text_page)
#        self.edit_window.show_all()
#
#    def save_constraints(self, widget):
#        text = self.text_page.get_text()
#        self.model.constraints = text
#        self.edit_window.destroy()


# API for communication with charter
    def set_action_select(self, widget):
        """
        As it says
        """
        self.mouse_role = "select"

    def set_action_new_simple_node(self, widget):
        """
        As it says
        """
        self.mouse_role = "simple"

    def set_action_new_macro_node(self, widget):
        """
        As it says
        """
        self.mouse_role = "macro"

    def set_action_new_start_node(self, widget):
        """
        As it says
        """
        self.mouse_role = "start"

    def set_action_new_trap_node(self, widget):
        """
        As it says
        """
        self.mouse_role = "trap"

    def set_action_new_input_node(self, widget):
        """
        As it says
        """
        self.mouse_role = "input"

    def set_action_new_transition(self, widget):
        """
        As it says
        """
        if self.current_node:
            self.current_node.selected = False
        self.current_node = None
        self.current_handle = 0
        self.m_vscreen_coord = None
        if self.current_transition:
            self.current_transition.selected = False
        self.current_transition = None
        self.mouse_role = "new_trans"

    def set_action_new_perm_node(self, widget):
        """
        As it says
        """
        self.mouse_role = "perm"


# controler for navigation view

class NavControler(object):
    """
    Implement a controler for navigation views
    """

    def __init__(self):
        self.lastx = 0 # coordinates of last click in view
        self.lasty = 0
        self.in_ret = False
        self.obs = []

    def set_view(self, view):
        """
        As it says
        """
        # attribute view is assigned when a view is created
        self.view = view

    def attach(self, obs):
        """
        observer management
        """
        if not obs in self.obs:
            self.obs.append(obs)

    def detach(self, obs):
        """
        observer management
        """
        self.obs.remove(obs)

    def notify(self, depx, depy):
        """
        observer management
        """
        for obs in self.obs:
            obs.update(depx, depy)

    def button_press(self, widget, event):
        """
        action when a mouse button is pressed
        """
        self.lastx = event.x
        self.lasty = event.y
        cond = self.view.x_ret <= self.lastx
        cond = cond and (self.lastx <= (self.view.x_ret + self.view.w_ret))
        if cond :
            cond2 = (self.view.y_ret <= self.lasty)
            vvv = (self.view.y_ret + self.view.h_ret)
            cond2 = cond2 and (self.lasty <= vvv)
            if cond2:
                self.in_ret = True

    def button_release(self, widget, event):
        """
        action when a mouse button is released
        """
        self.in_ret = False
        return

    def motion_notify(self, widget, event):
        """
        callback
        """
        if self.in_ret:
            depx = event.x - self.lastx
            depy = event.y - self.lasty
            alloc = widget.get_allocation()
            # limits
            vv1 = self.view.x_ret + depx + self.view.w_ret
            vv2 = self.view.x_ret + depx
            if (vv1 > alloc.width) or (vv2 < 0):
                depx = 0
            vv1 = self.view.y_ret + depy + self.view.h_ret
            vv2 = self.view.y_ret + depy
            if (vv1 > alloc.height) or (vv2 < 0):
                depy = 0
            self.lastx = self.lastx + depx
            self.lasty = self.lasty + depy
            # reticule move
            if (not depx == 0) or  (not depy == 0):
                depx = float(depx) / alloc.width
                depy = float(depy) / alloc.height
                self.notify(depx, depy)






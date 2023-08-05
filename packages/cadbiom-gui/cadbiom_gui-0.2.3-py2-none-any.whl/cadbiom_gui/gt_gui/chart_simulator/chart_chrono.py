
## Filename    : chart_chrono.py
## Author(s)   : Michel Le Borgne
## Created     : 05/2010
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
Widget for chronograms
"""
import gtk
from gtk.gdk import color_parse, Pixmap
from cadbiom_gui.gt_gui.utils.warn import cancel_warn
INTERLIGNE = 30
W_STEP = 20
H_STEP = 10
CHAR_PIX = 9

class ChartChrono (object):
    """
    A class for displaying a chronogram
    """
    def __init__(self):
        self.name = None
        self.state_names = []
        self.state_dict = dict()
        self.input_names = []
        self.input_dict = dict()
        self.left_margin = 0
        self.nb_step = 0

        self.window = None

    @classmethod
    def from_simulation_model(cls, sim):
        """
        @param sim: simulator object
        """
        chrono = cls()
        chrono.name = sim.model.name
        # initialisations
        symb_table = sim.get_symb_tab()
        lnam = 0  # max size of a name
        for key in symb_table.keys():
            elem = symb_table[key]
            if elem.is_place():
                chrono.state_names.append(key)
                lnam = max(lnam, len(key))
                chrono.state_dict[key] = []
            if elem.is_input_event():
                chrono.input_names.append(key)
                lnam = max(lnam, len(key))
                chrono.input_dict[key] = []
        chrono.state_names.sort()
        chrono.input_names.sort()
        chrono.h_extend = (len(chrono.input_names)
                           + len(chrono.state_names)) * INTERLIGNE + INTERLIGNE
        chrono.w_extend = 500 # width of the curve area
        chrono.height = min(chrono.h_extend, 1000)
        chrono.width = 500
        chrono.left_margin = lnam * CHAR_PIX
        chrono.set_view()
        return chrono

    @classmethod
    def for_trajectory(cls, sim):
        """
        version of a chronogram for registering a whole trajectory
        @param sim : the simulator
        """
        chrono = cls()
        chrono.name = sim.model.name
        # initialisations
        symb_table = sim.get_symb_tab()
        for key in symb_table.keys():
            elem = symb_table[key]
            if elem.is_place():
                chrono.state_names.append(key)
                chrono.state_dict[key] = []
            if elem.is_input_event():
                chrono.input_names.append(key)
                chrono.input_dict[key] = []
        return chrono

    def set_view(self):
        """
        establish the graphical windows
        """
        # view
        self.window =  gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Chronogram "+self.name)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(500 + self.left_margin, self.height)

        # hbox
        hbox = gtk.HBox()
        hbox.set_homogeneous(False)
        scrw = gtk.ScrolledWindow()
        #sw.set_size_request(self.width,self.height)
        scrw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrw.set_shadow_type(gtk.SHADOW_IN)
        scrw.add_with_viewport(hbox)
        self.window.add(scrw)
        self.scrw = scrw

        # name view
        self.name_view = gtk.DrawingArea()
        self.name_view.set_size_request(self.left_margin, self.h_extend)
        self.name_pixmap = None
        self.name_view.connect("expose_event", self.__expose_event)
        self.name_view.connect("configure_event", self.__configure_event)
        hbox.pack_start(self.name_view, True, True)

        # curve view
        self.view = gtk.DrawingArea()
        #self.name_view.set_size_request(self.w_extend, self.h_extend)
        self.pixmap = None # cannot be initialized before self.window creation
        hbox.pack_start(self.view, True, False)
        self.view.connect("expose_event", self.__expose_event)
        self.view.connect("configure_event", self.__configure_event)

        adj = self.scrw.get_hadjustment()
        adj.connect("value_changed", self.__changed_event)

        self.window.show_all()

    def register(self, sim):
        """
        read the simulation model and register the state of each place
        """
        symb_table = sim.get_symb_tab()
        for key in symb_table.keys():
            elem = symb_table[key]
            if elem.is_place():
                if elem.activated:
                    self.state_dict[key].append(1)
                else:
                    self.state_dict[key].append(0)
            if elem.is_input_event():
                if elem.activated:
                    self.input_dict[key].append(1)
                else:
                    self.input_dict[key].append(0)
        self.nb_step = self.nb_step + 1

    def draw_names(self):
        """
        Write the state names
        """
        # graphic context
        pixmap = self.name_pixmap
        grc = self.name_view.window.new_gc()
        grc.set_rgb_fg_color(color_parse("black"))
        stylepango = self.name_view.create_pango_layout("")
        pixmap.draw_rectangle(self.name_view.get_style().white_gc,
                          True, 0, 0, self.left_margin+5, self.h_extend)
        polyl = [(self.left_margin -1, 0), (self.left_margin-1, self.h_extend)]
        pixmap.draw_lines(grc, polyl)
        y_line = 15   # vertical coordinate of the text line
        grc.set_rgb_fg_color(color_parse("blue"))
        for name in self.input_names:
            # put name
            stylepango.set_text(name)
            pixmap.draw_layout(grc, 2, y_line, stylepango)
            polyl = [(self.left_margin -4, y_line+16),
                     (self.left_margin, y_line+16)]
            pixmap.draw_lines(grc, polyl)
            y_line = y_line + INTERLIGNE

        grc.set_rgb_fg_color(color_parse("black"))
        for name in self.state_names:
            # put name
            stylepango.set_text(name)
            wna =  stylepango.get_pixel_size()[0]
            pixmap.draw_layout(grc, 2, y_line, stylepango)
            polyl = [(wna+2, y_line+16), (self.left_margin, y_line+16)]
            pixmap.draw_lines(grc, polyl)
            y_line = y_line + INTERLIGNE

    def draw_steps(self):
        """
        Draw the chronograms for different states
        """
        pixmap = self.pixmap
        grc = self.view.window.new_gc()
        grc.set_rgb_fg_color(color_parse("#CDFFC6"))
        nb_step = self.w_extend/W_STEP
        i = 0
        while i < nb_step:
            xch = i * W_STEP
            polyl = [(xch, 0), (xch, self.h_extend)]
            if i % 10 == 0:
                grc.set_rgb_fg_color(color_parse("green"))
            pixmap.draw_lines(grc, polyl)
            if i % 10 == 0:
                grc.set_rgb_fg_color(color_parse("#CDFFC6"))
            i = i+1

    def draw(self):
        """
        Draw all
        """
        # graphic context
        pixmap = self.pixmap
        if not pixmap:
            return
        self.view.set_size_request(self.w_extend, self.height)
        grc = self.view.window.new_gc()
        pixmap.draw_rectangle(self.view.get_style().white_gc,
                          True, 0, 0, self.w_extend, self.h_extend)
        # scale
        self.draw_steps()
        # chrono
        y_line = 15
        for name in self.input_names:
            # generate chrono
            chrono = []
            st_log = self.input_dict[name]
            x_step = 0

            for val in st_log:
                step = y_line +15 - val * H_STEP
                chrono.append((x_step, step))
                chrono.append((x_step+W_STEP, step))
                x_step = x_step + W_STEP
            if len(chrono) > 0:
                grc.set_rgb_fg_color(color_parse("blue"))
                pixmap.draw_lines(grc, chrono)
            y_line = y_line + INTERLIGNE

        for name in self.state_names:
            # generate chrono
            chrono = []
            st_log = self.state_dict[name]
            x_step = 0

            for val in st_log:
                step = y_line +15 - val * H_STEP
                chrono.append((x_step, step))
                chrono.append((x_step+W_STEP, step))
                x_step = x_step + W_STEP
            if len(chrono)>0:
                grc.set_rgb_fg_color(color_parse("red"))
                pixmap.draw_lines(grc, chrono)
            y_line = y_line + INTERLIGNE

    def update(self):
        """
        Refresh
        """
        if not self.window or not self.pixmap:
            return
        cwidth = self.nb_step*W_STEP + 10
        if cwidth > self.w_extend:
            self.w_extend = cwidth
            self.pixmap = Pixmap(self.view.window, self.w_extend, self.h_extend)
            adj = self.scrw.get_hadjustment()
            adj.set_value(adj.upper)
        self.draw()
        self.view.set_size_request(self.w_extend, self.h_extend)
        fcgc = self.view.get_style().fg_gc[gtk.STATE_NORMAL]
        self.view.window.draw_drawable(fcgc,
                                       self.pixmap, 0, 0, 0, 0,
                                       self.w_extend, self.h_extend)

    def rewind(self):
        """
        As it says
        """
        for key in self.state_names:
            self.state_dict[key] = []
        for key in self.input_names:
            self.input_dict[key] = []
        self.nb_step = 0
        self.width = 500
        adj = self.scrw.get_hadjustment()
        if adj:
            adj.set_value(adj.lower)

    def select_and_prepare(self):
        """
        Select the places with a change in the activation state
        Prepare the chronogram to be displayed
        """
        old_state_dict = self.state_dict
        old_input_dict = self.input_dict
        self.state_dict = dict()
        self.input_dict = dict()
        old_state_names = self.state_names
        old_input_names = self.input_names
        self.state_names = []
        self.input_names = []
        lnam = 0
        for key in old_state_names:
            if has_changed(old_state_dict[key]):
                self.state_names.append(key)
                self.state_dict[key] = old_state_dict[key]
                lnam = max(lnam, len(key))

        for key in old_input_names:
            if has_changed(old_input_dict[key]):
                self.input_names.append(key)
                self.input_dict[key] = old_input_dict[key]
                lnam = max(lnam, len(key))
        self.state_names.sort()
        self.input_names.sort()

        if lnam == 0:
            cancel_warn("No change in the system!!")
            return False
        n_hextend = len(self.input_names)
        n_hextend = (n_hextend + len(self.state_names)) * INTERLIGNE
        self.h_extend = n_hextend + INTERLIGNE

        self.w_extend = 500
        self.height = min(self.h_extend, 1000)
        self.width = self.w_extend
        self.left_margin = lnam * CHAR_PIX
        return True

    def display_selected_chrono(self):
        """
        As it says
        """
        if self.select_and_prepare():
            self.set_view()
            self.draw()

    # window management
    def destroy(self):
        """
        Used when windows are linked
        """
        if self.window:
            self.window.destroy()

    def on_destroy(self):
        """
        Standard call back
        """
#        if self.parent:
#            self.parent.win_remove(self)
        if self.window:
            self.window.destroy()

    def __expose_event(self, widget, event):
        """
        Redisplay drawing after cover and exposure of the window
        """
        if not self.view.window:
            return True
        if not self.name_pixmap:
            self.name_pixmap = Pixmap(self.name_view.window,
                                      self.left_margin, self.h_extend)
            self.draw_names()
        if not self.pixmap:
            self.pixmap = Pixmap(self.view.window,
                                 self.w_extend, self.h_extend)
            self.draw()
        # expose the drawing  already in the pixmaps
        style = widget.get_style().fg_gc[gtk.STATE_NORMAL]
        self.name_view.window.draw_drawable(style, self.name_pixmap,
                                            0, 0, 0, 0,
                                            self.left_margin, self.h_extend)
        self.view.window.draw_drawable(style, self.pixmap,
                                       0, 0, 0, 0, self.w_extend, self.h_extend)
        return True

    def __configure_event(self, widget, event):
        """
        Initialisation
        """
        if not self.name_pixmap:
            self.name_pixmap = Pixmap(self.name_view.window,
                                       self.left_margin, self.h_extend)
        self.draw_names()
        if not self.pixmap:
            #self.pixmap = Pixmap(self.view.window,
            #                     self.w_extend, self.h_extend)
            pass
        else:
            self.draw()
        return True

    def __changed_event(self, widget):
        """
        change in size
        """
        style = self.view.get_style().fg_gc[gtk.STATE_NORMAL]
        self.view.window.draw_drawable(style, self.pixmap,
                                       0, 0, 0, 0,
                                       self.w_extend, self.h_extend)
        return True


# helper function
def has_changed(lls):
    """
    Test changing from last call
    """
    xxx = lls[0]
    for elem in lls:
        if not xxx == elem:
            return True
    return False




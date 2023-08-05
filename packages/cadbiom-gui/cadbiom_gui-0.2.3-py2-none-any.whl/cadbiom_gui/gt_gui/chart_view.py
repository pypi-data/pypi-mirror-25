## Filename    : chart_view.py
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
## Contributor(s): Geoffroy Andrieux, Nolwenn Le Meur
##
"""
Main views for the Cadbiom gui
"""
import gtk

GRAPH_BG_COLOR = "#FEFAFA"

class ChartView(gtk.DrawingArea):
    """
    Class for the main drawing window of charter
    """
    def __init__(self, width, height, drawing_style, controler, model):
        """
        @param width, height: int - size of the view
        @param drawing_style: a Drawing style associated with the pattern
        @param controler: the controller as in the MVC pattern
        @param model: a ChartModel
        """
        gtk.DrawingArea.__init__(self)
        self.controler = controler
        controler.set_view(self)
        self.model = model

        # attach as model observer
        model.attach(self)

        # signals
        self.set_events(gtk.gdk.EXPOSURE_MASK
                             | gtk.gdk.LEAVE_NOTIFY_MASK
                             | gtk.gdk.BUTTON_PRESS_MASK
                             | gtk.gdk._2BUTTON_PRESS
                             | gtk.gdk.BUTTON_RELEASE_MASK
                             | gtk.gdk.POINTER_MOTION_MASK
                             | gtk.gdk.POINTER_MOTION_HINT_MASK)
        self.connect("expose-event", self.expose_event)
        self.connect("configure_event", self.configure_event)

        # controlled events
        self.connect("button_press_event", controler.button_press)
        self.connect("button_release_event", controler.button_release)
        self.connect("motion_notify_event", controler.motion_notify)

        # drawing stuffs
        drawing_style.view = self
        self.drawing_style = drawing_style
        controler.drawing_style = drawing_style
        self.draw_width = width       # drawing window
        self.min_width = width
        self.draw_height = height
        self.min_height = height
        self.set_size_request(width, height)
        self.stylepango = self.create_pango_layout("")
        self.pixmap = None # cannot be initialized before self.window creation
        self.page = None
        self.zoom_count = 0

    def expose_event(self, widget, event):
        """
        Redisplay drawing after cover and exposure of the window
        """

        self.pixmap.draw_rectangle(self.get_style().white_gc,
                          True, 0, 0, self.draw_width, self.draw_height)
        # draw in the pixmap
        self.model.draw(self)
        # expose the drawing
        self.window.draw_drawable(self.get_style().fg_gc[gtk.STATE_NORMAL],
                                self.pixmap, 0, 0, 0, 0,
                                self.draw_width, self.draw_height)
        if self.page:
            self.page.notify(widget)
        return True

    def configure_event(self, widget, event):
        """
        Initialisation and change in size
        """
        # adjust to visible window
        xor , yor, width, height = widget.get_allocation()
        self.draw_width = max(width, self.min_width)
        self.draw_height = max(height, self.min_height)
        # set pixmap if necesssary
        if not self.pixmap:
            self.pixmap = gtk.gdk.Pixmap(self.window,
                                         self.draw_width, self.draw_height)
        # adjust the pixmap to size
        size = self.pixmap.get_size()
        if size[0] != self.draw_width or size[1] != self.draw_height:
            self.set_size_request(self.draw_width, self.draw_height)
            self.pixmap = gtk.gdk.Pixmap(self.window,
                                         self.draw_width, self.draw_height)
        return True

    def update(self):
        """
        Display a new drawing of the model
        """
        # update only visible views
        if not self.window:
            return

        # resize if virtual drawing window size changed
        size = self.pixmap.get_size()
        if size[0] != self.draw_width or size[1] != self.draw_height:
            self.set_size_request(self.draw_width, self.draw_height)
            self.pixmap = gtk.gdk.Pixmap(self.window,
                                         self.draw_width, self.draw_height)
        self.pixmap.draw_rectangle(self.get_style().white_gc,
                          True, 0, 0, self.draw_width, self.draw_height)
        # draw in the pixmap
        self.model.draw(self)
        # expose the drawing
        self.window.draw_drawable(self.get_style().fg_gc[gtk.STATE_NORMAL],
                                self.pixmap, 0, 0, 0, 0,
                                self.draw_width, self.draw_height)


    def zoom_minus(self):
        """
        Zoom out function
        """
        if self.zoom_count < -10:
            return
        self.min_height = int(self.min_height * 0.9)
        self.draw_height = self.min_height
        self.min_width = int(self.min_width * 0.9)
        self.draw_width = self.min_width
        self.update()
        if self.page:
            self.page.notify(None)
        self.zoom_count = self.zoom_count - 1

    def zoom_plus(self):
        """
        Zoom in function
        """
        if self.zoom_count > 15:
            return
        print "before", self.min_height, self.draw_height, self.min_width, self.draw_width
        self.min_height = int(self.min_height * 1.1)
        self.draw_height = self.min_height
        self.min_width = int(self.min_width * 1.1)
        self.draw_width = self.min_width
        print "after", self.min_height, self.draw_height, self.min_width, self.draw_width
        self.update()
        if self.page:
            self.page.notify(None)
        self.zoom_count += 1

class NavView(ChartView):
    """
    Specialized ChartView for navigator
    """
    def __init__(self, width, height, drst, controler, model):
        """
        same parameters than in upper class constructor
        """
        ChartView.__init__(self, width, height, drst, controler, model)
        self.x_ret = 0
        self.y_ret = 0
        self.w_ret = 1
        self.h_ret = 1
        self.show_all()

    def configure_event(self, widget, event):
        """
        Initialization and change in size
        """
        xor, yor, width, height = widget.get_allocation()
        self.draw_width = width
        self.draw_height = height

        self.pixmap = gtk.gdk.Pixmap(self.window,
                                     self.draw_width, self.draw_height)
        self.pixmap.draw_rectangle(widget.get_style().white_gc,
                          True, 0, 0, self.draw_width, self.draw_height)
        self.ret_gc = self.window.new_gc()
        self.ret_gc.set_rgb_fg_color(gtk.gdk.color_parse('red'))
        return True

    def expose_event(self, widget, event):
        """
        Redisplay drawing after cover and exposure of the window
        """
        self.pixmap.draw_rectangle(self.get_style().white_gc,
                          True, 0, 0, self.draw_width, self.draw_height)
        # draw in the pixmap
        self.model.draw(self)
        # expose the drawing
        self.window.draw_drawable(self.get_style().fg_gc[gtk.STATE_NORMAL],
                                self.pixmap, 0, 0, 0, 0,
                                self.draw_width, self.draw_height)
        # draw reticule
        self.window.draw_rectangle(self.ret_gc,
                          False, self.x_ret, self.y_ret,
                          self.w_ret, self.h_ret)
        return True

    def update(self):
        """
        Display a new drawing of the model
        """
        # update only visible views
        if not self.window:
            return
        # hack for notebook
        if not self.pixmap:
            return
        # draw in the pixmap
        self.pixmap.draw_rectangle(self.get_style().white_gc,
                          True, 0, 0, self.draw_width, self.draw_height)
        self.model.draw(self)
        # expose the drawing
        self.window.draw_drawable(self.get_style().fg_gc[gtk.STATE_NORMAL],
                                self.pixmap, 0, 0, 0, 0,
                                self.draw_width, self.draw_height)
        # draw reticule
        self.window.draw_rectangle(self.ret_gc, False,
                                   self.x_ret, self.y_ret,
                                   self.w_ret, self.h_ret)

    def scroll_update(self, xor, yor, width, height):
        """
        Updating function used when the linked window is scrolled
        """
        if not self.window:
            return
        self.x_ret = int(xor * self.draw_width)
        self.y_ret = int(yor * self.draw_height)
        self.w_ret = int(width * self.draw_width)
        self.h_ret = int(height * self.draw_height)
        # expose the drawing
        self.window.draw_rectangle(self.get_style().white_gc,
                          True, 0, 0, self.draw_width, self.draw_height)
        self.window.draw_drawable(self.get_style().fg_gc[gtk.STATE_NORMAL],
                                self.pixmap, 0, 0, 0, 0,
                                self.draw_width, self.draw_height)
        # draw reticule
        self.window.draw_rectangle(self.ret_gc, False,
                                   self.x_ret, self.y_ret,
                                   self.w_ret, self.h_ret)

    def clear(self):
        """
        As it says
        """
        self.window.draw_rectangle(self.get_style().white_gc,
                          True, 0, 0, self.draw_width, self.draw_height)


class ChartPage(gtk.Frame):
    """
    A simple graph editor for pages: a graph area wrapped in a scroll window
    """
    def __init__(self, width, height, drst, controler, model):
        """

        """
        gtk.Frame.__init__(self)
        # for observers
        self.__observer_list = []
        # chart view and model
        self.draw = ChartView(width, height, drst, controler, model)
        self.draw.page = self

        # wrap in a scroll window
        scr_w = gtk.ScrolledWindow()
        self.scr_w = scr_w
        self.vadj = scr_w.get_vadjustment()
        self.hadj = scr_w.get_hadjustment()
        self.hadj_h_id = self.hadj.connect("value_changed", self.notify)
        self.vadj_h_id = self.vadj.connect("value_changed", self.notify)
        self.allow_adj = True
        scr_w.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_ALWAYS)
        viewport = gtk.Viewport()
        scr_w.add(viewport)
        viewport.add(self.draw)
        self.add(scr_w)
        self.show_all()


    # observer pattern methods
    def attach(self, obs):
        """
        standard in observer pattern
        """
        if not obs in self.__observer_list:
            self.__observer_list.append(obs)

    def detach(self, obs):
        """
        standard in observer pattern
        """
        self.__observer_list.remove(obs)

    def notify(self, widget):
        """
        used when the viewport is moved from inside (hbar and vbar)
        """
        if self.allow_adj:
            x_pos = float(self.hadj.value)/self.draw.draw_width
            y_pos = float(self.vadj.value)/self.draw.draw_height
            width = self.hadj.page_size/self.draw.draw_width
            height = self.vadj.page_size/self.draw.draw_height
            for obs in self.__observer_list:
                obs.scroll_update(x_pos, y_pos, width, height)

    # signal call back
    def update(self, dxx, dyy):
        """
        Used when the viewport is moved from outside (navigator)
        """
        d_hadj = dxx * self.draw.draw_width
        d_vadj = dyy * self.draw.draw_height
        self.allow_adj = False
        self.hadj.value = int(self.hadj.value + d_hadj)
        self.vadj.value = int(self.vadj.value + d_vadj)
        self.scr_w.set_hadjustment(self.hadj)
        self.scr_w.set_vadjustment(self.vadj)
        self.allow_adj = True
        self.notify(None)






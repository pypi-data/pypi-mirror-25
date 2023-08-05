#
## Filename    : text_page.py
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
Collection of widgets for text handling
"""
import gtksourceview2 as gtksourceview
import gtk
import gtk.glade

import pkg_resources

class TextEditConfig:
    """
    Text editors configuration
    """
    def __init__(self):
        self.style = "classical"
        self.show_line_numbers = False
        self.show_line_marks = True



class TextArea(gtksourceview.View):
    """
    GtkSourceView with supplementary attributes
    """
    def __init__(self, language = None):
        gtksourceview.View.__init__(self)
        # create buffer
        buffer = gtksourceview.Buffer()
        mgr = gtksourceview.style_scheme_manager_get_default()
        style_scheme = mgr.get_scheme('classical')
        if style_scheme:
            buffer.set_style_scheme(style_scheme)

        # set language
        if language:
            lma = gtksourceview.LanguageManager()
            spa = lma.get_search_path()
            spa.append("utils/language-specs")
            lma.set_search_path(spa)
            lang = lma.get_language(language)
            buffer.set_language(lang)

        # set buffer
        self.set_buffer(buffer)
        self.buffer = buffer

    def refresh_config(self, edit_config):
        """
        As it says
        """
        self.set_show_line_numbers(edit_config.show_line_numbers)
        self.set_show_line_marks(edit_config.show_line_marks)
        mgr = gtksourceview.style_scheme_manager_get_default()
        style_scheme = mgr.get_scheme(edit_config.style)
        #TODO
        if style_scheme:
            self.get_buffer().set_style_scheme(style_scheme)
        else:
            pass

class TextPage(gtk.Frame):
    """
    A simple text editor for pages
    """
    def __init__(self, language, edit_config = None):
        gtk.Frame.__init__(self)
        # text view and model
        self.write = TextArea(language)
        self.modified = False
        self.not_set = False
        # configuration
        if edit_config:
            self.write.refresh_config(edit_config)

        # page num in notebook (if used in notebook)
        self.page_num = -1

        # wrap in a scroll window
        swin = gtk.ScrolledWindow()
        swin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        swin.set_shadow_type(gtk.SHADOW_IN)
        swin.add_with_viewport(self.write)
        self.add(swin)

        # connect control
        self.write.buffer.connect("changed", self.is_modified)

    def refresh_config(self, edit_config):
        """
        Self explained
        """
        self.write.refresh_config(edit_config)

    def set_text(self, text):
        """
        Put text in the buffer
        """
        self.write.get_buffer().set_text(text)
        self.not_set = False
        self.modified = False

    def get_text(self):
        """
        Retrieve text from the buffer
        """
        wbuf = self.write.get_buffer()
        iter_begin = wbuf.get_start_iter()
        iter_end = wbuf.get_end_iter()
        text = wbuf.get_text(iter_begin, iter_end)
        return text

    def insert_at_end(self, text):
        """
        Insert text at the end of the buffer
        """
        wbuf = self.write.get_buffer()
        iter_end = wbuf.get_end_iter()
        wbuf.insert(iter_end, text)

    def clear(self):
        """
        RAZ of the buffer
        """
        wbuf = self.write.get_buffer()
        iter_start = wbuf.get_start_iter()
        iter_end = wbuf.get_end_iter()
        wbuf.delete(iter_start, iter_end)

    # control
    def is_modified(self, widget):
        """
        Mark as modified
        """
        self.modified = True
        #self.modified = self.not_set
        #self.not_set = True

class BioSignalEditor:
    """
    Biosignal simple editor - can load and save files
    @param on_leave: method to be used when quitting the editor
    """
    def __init__(self, name, master, on_leave):
        self.master = master
        self.what_todo = on_leave
        # gui
        # Set the Glade file
        template = pkg_resources.resource_filename(
            __name__,
            "../chart_glade/biosiged.glade"
        )
        self.wtree = gtk.glade.XML(template)

        # Get the Main Window, and connect the "destroy" event
        self.main_window = self.wtree.get_widget("window1")
        if (self.main_window):
            self.main_window.connect("delete_event", self.on_destroy)
        self.main_window.set_title(name)
        self.main_window.set_default_size(800, 900)
        self.main_window.set_position(gtk.WIN_POS_CENTER)
        # text_area
        econf = TextEditConfig();
        self.page = TextPage("biosignal", econf)
        vbox =  self.wtree.get_widget("vbox1")
        vbox.pack_start(self.page)

        # file menu
        menu_item =  self.wtree.get_widget("new_m")
        menu_item.connect("activate", self.on_new)
        menu_item =  self.wtree.get_widget("open_m")
        menu_item.connect("activate", self.on_open)
        menu_item =  self.wtree.get_widget("save_m")
        menu_item.connect("activate", self.on_save)
        menu_item =  self.wtree.get_widget("save_as_m")
        menu_item.connect("activate", self.on_save_as)
        menu_item =  self.wtree.get_widget("quit_m")
        menu_item.connect("activate", self.on_destroy)

        # style menu
        #TODO

        # internals
        self.file = None

        self.main_window.show_all()

    def on_new(self, widget):
        """
        Clear callback
        """
        self.page.clear()
        pass

    def choose_file(self):
        """
        As it says
        """
        choice = gtk.FileChooserDialog("Biosignal Editor", None ,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        choice.set_default_response(gtk.RESPONSE_OK)

        #add a filter to see only biosig files
        filter = gtk.FileFilter()
        filter.set_name("bsi files")
        filter.add_pattern("*.bsi")
        choice.add_filter(filter)

        #add a filter to see all
        no_filter = gtk.FileFilter()
        no_filter.set_name("all")
        no_filter.add_pattern("*")
        choice.add_filter(no_filter)

        response = choice.run()
        if response == gtk.RESPONSE_OK:
            fname =  choice.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            fname =  None
        choice.destroy()
        return fname

    def on_open(self, widget):
        """
        open a window to search .bsi file
        """
        file_name = self.choose_file()
        if file_name:
            file = open(file_name, 'r+')
            self.file = file
            text = file.read()
            self.page.set_text(text)

    def on_save(self, widget):
        """
        Save callback
        """
        if not self.file:
            file_name = self.choose_file()
            if file_name:
                self.file = open(file_name, 'r+')
            else:
                return
        text = self.page.get_text()
        self.file.write(text)

    def on_save_as(self, widget):
        """
        Save as callback
        """
        file_name = self.choose_file()
        if file_name:
            file = open(file_name, 'r+')
            self.file = file
            text = self.page.get_text()
            print 'SAVE AS', text
            self.file.write(text)

    def on_destroy(self, widget, xxx=None):
        """
        destroy callback
        """
        self.what_todo(self)
        self.main_window.destroy()

    def set_text(self, text):
        """
        As it says
        """
        self.page.set_text(text)

    def get_text(self):
        """
        As it says
        """
        return self.page.get_text()

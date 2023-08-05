## Filename    : charter.py
## Author(s)   : Geoffroy Andrieux
## Created     : 03/2010
## Revision    :
## Source      :
##
## Copyright 2010 : IRISA/IRSET
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
##     IRISA/IRSET
##     Symbiose team
##     IRISA  Campus de Beaulieu
##     35042 RENNES Cedex, FRANCE
##
##
## Contributor(s): Michel Le Borgne, Nolwenn Le Meur
##
"""
Main class for Cadbiom gui
"""

import gtk
import webbrowser

from gtk.gdk import screen_height, screen_width, \
                  COLORSPACE_RGB, colormap_get_system, Pixbuf
from cadbiom.antlr3 import ANTLRFileStream, CommonTokenStream

from charter_info import CharterInfo
from edit_mvc import EditMVC
from utils.warn import  confirm, DialogEntry, cancel_warn
from utils.notebookUtils import create_custom_tab
from utils.text_page import BioSignalEditor
from utils.reporter import CompilReporter
from utils.fileHandling import FileChooser

from chart_controler import ChartClipboard
from chart_simulator.chart_simul_controler import \
                     ChartSimulControler, DisplayError
from chart_checker.chart_checker_controler  import ChartChecker
from chart_misc_widgets import SearchManager, SearchFrontier, \
                      LegendWindow, ImportPIDParam, ImportBioPAXParams
from cadbiom_gui.gt_gui.chart_static.chart_stat_controler import \
    STATWindow, SCCWindow, BAGWindow

from cadbiom.models.guard_transitions.chart_model import ChartModel
from cadbiom.models.guard_transitions.translators.chart_lang import LangVisitor
from cadbiom.models.guard_transitions.translators.chart_xml import \
                  XmlVisitor, MakeModelFromXmlFile, \
                  MakeModelFromXmlString, XmlException
from cadbiom.models.guard_transitions.translators.cadlangLexer import cadlangLexer
from cadbiom.models.guard_transitions.translators.cadlangParser import cadlangParser

# Custom imports
from cadbiom.models.guard_transitions.analyser.static_analysis \
    import StaticAnalyzer

from layout import LayoutVisitor

import pkg_resources

class Charter(object):
    """
    charter main class
    """

    def __init__(self, cad):
        self.ident = "charter"
        self.cad_manager = cad

        # Gestion of the destroy of all subwindows opened from this one
        self.subwindows = set()

        # simul options
        self.simul_strict = True
        self.sim_flat_graph = False

        # common clipboard
        self.clipboard = ChartClipboard()
        # gui
        # Set the Glade file
        template = pkg_resources.resource_filename(
            __name__,
            "chart_glade/charter.glade"
        )
        self.wtree = gtk.glade.XML(template)
        # Get the Main Window, and connect the "destroy" event
        self.main_window = self.wtree.get_widget("TopModel")
        if self.main_window:
            self.main_window.connect("delete_event", self.on_destroy)
        h_scr = screen_height()
        w_scr = screen_width()
        self.h_scr = int(h_scr)
        self.w_scr = int(w_scr)
        self.main_window.resize(int(w_scr * 0.9), int(h_scr * 0.9))
        self.constraint_window = None

        # Accelerators
        self.my_accelerators = gtk.AccelGroup()
        self.main_window.add_accel_group(self.my_accelerators)

        # menu bar
        menu_bar = self.wtree.get_widget("menubar1")
        menu_bar.set_size_request(0, 25)

        menu_item =  self.wtree.get_widget("doc_menu")
        menu_item.connect("activate", self.show_doc)
        menu_item =  self.wtree.get_widget("legend_menu")
        menu_item.connect("activate", self.show_legend)

        menu_item =  self.wtree.get_widget("New_model")
        self.add_accelerator(menu_item, "<Control>n")
        menu_item.connect("activate", self.new_charts)
        menu_item =  self.wtree.get_widget("Import_cadbiom")
        self.add_accelerator(menu_item, "<Control>o")
        menu_item.connect("activate", self.choose_xml_file)
        menu_item =  self.wtree.get_widget("Import_BioPAX")
        self.add_accelerator(menu_item, "<Control>b")
        menu_item.connect("activate", self.choose_BioPAX_file)
        menu_item =  self.wtree.get_widget("Import_PID")
        menu_item.connect("activate", self.choose_pid_file)
        menu_item =  self.wtree.get_widget("Import_CadLang")
        menu_item.connect("activate", self.choose_cadlang_file)
        menu_item =  self.wtree.get_widget("Export_cadbiom")
        self.add_accelerator(menu_item, "<Control>s")
        menu_item.connect("activate", self.export_to_xml)
        menu_item =  self.wtree.get_widget("Export_cadlang")
        menu_item.connect("activate", self.export_to_lang)
        menu_item =  self.wtree.get_widget("Export_picture")
        menu_item.connect("activate", self.export_picture)
        # Add Quit button & shortcuts
        menu =  self.wtree.get_widget("menu2")
        menu.append(gtk.SeparatorMenuItem())
        menu_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.add_accelerator(menu_item, "<Control>q")
        menu_item.connect("activate", self.on_destroy, None)
        menu.append(menu_item)

        menu_item =  self.wtree.get_widget("Hierarchical_TB")
        menu_item.connect("activate", self.do_layout, "hierarchical_TB")
        menu_item =  self.wtree.get_widget("Hierarchical_LR")
        menu_item.connect("activate", self.do_layout, "hierarchical_LR")
        menu_item =  self.wtree.get_widget("neato")
        menu_item.connect("activate", self.do_layout, "neato")
        menu_item =  self.wtree.get_widget("fdp")
        menu_item.connect("activate", self.do_layout, "fdp")
        menu_item =  self.wtree.get_widget("twopi")
        menu_item.connect("activate", self.do_layout, "twopi")
        menu_item =  self.wtree.get_widget("circo")
        menu_item.connect("activate", self.do_layout, "circo")

        menu_item =  self.wtree.get_widget("model_infos")
        menu_item.connect("activate", self.on_stats_info)
        menu_item =  self.wtree.get_widget("scc_search")
        menu_item.connect("activate", self.on_frontier_scc)
        menu_item =  self.wtree.get_widget("basal_activated_genes")
        menu_item.connect("activate", self.on_basal_activated_genes)
        menu_item =  self.wtree.get_widget("dependance_graph")

        menu_item =  self.wtree.get_widget("transitionGraph")
        menu_item.connect("activate", self.on_dependency_graph)
        menu_item =  self.wtree.get_widget("dependencyGraph")
        menu_item.connect("activate", self.on_dependency_graph)
        menu_item =  self.wtree.get_widget("fullDependencyGraph")
        menu_item.connect("activate", self.on_dependency_graph)

        # Model Handling buttons
        button = self.wtree.get_widget("Check_button")
        button.set_label(button.get_label() + " (F8)")
        self.add_accelerator(button, "F8")
        button.connect("clicked", self.on_check)

        button = self.wtree.get_widget("Simu_button")
        button.set_label(button.get_label() + " (F9)")
        self.add_accelerator(button, "F9")
        button.connect("clicked", self.on_simulate)

        # graph drawing controler buttons (not connected)
        self.graph_notebook = self.wtree.get_widget("graph_notebook")
        self.graph_notebook.connect("switch-page",
                                    self.switch_graph_page_callback)
        self.create_drawing_buttons()

        # edit MVC
        self.ei_id = 0
        self.edit_mvc_list = []
        self.current_edit_mvc = None

        # chart info
        chart_info_frame = self.wtree.get_widget("informations_frame")
        self.chart_info = CharterInfo(chart_info_frame)
        self.chart_info.trans_info.show.connect("clicked", self.display_states)
        mtk_notebook = self.wtree.get_widget("MTK_notebook")
        # search
        self.search_area = SearchManager(self, mtk_notebook, "Simple node list")
        self.search_frontier = SearchFrontier(self, mtk_notebook, "Frontier")

        # overview
        self.overview_window = self.wtree.get_widget("Overview")
        self.overview_window.connect('scroll-event',
                                     self.on_button_scroll_event)


    def check_curent_model(function):
        """Decorator that checks if there is a current model.

        It is used before the call of functions that do some processing on
        models.

        If there is no model, the function juste returns None.
        """

        def modified_func(self, *args, **kwargs):
            """Returned modified function"""

            if not self.current_edit_mvc:
                return

            return function(self, *args, **kwargs)
        return modified_func

    def refresh(self):
        """
        TODO
        """
        pass

    def hide(self):
        """
        Useful ?
        """
        self.main_window.hide_all()

    def create_drawing_buttons(self):
        """
        create the buttons to control drawing
        """
        self.button_handlers = dict()
        c_box = self.wtree.get_widget("controler_box")

        but = gtk.Button(label="Select")
        c_box.add(but)
        self.button_handlers["Select"] = (but, -1)

        but = gtk.Button(label="InputNode F1")
        self.add_accelerator(but, "F1")
        self.add_image(but, "input_node")
        c_box.add(but)
        self.button_handlers["InputNode"] = (but, -1)

        but = gtk.Button(label="SimpleNode F2")
        self.add_accelerator(but, "F2")
        self.add_image(but, "simple_node")
        c_box.add(but)
        self.button_handlers["SimpleNode"] = (but, -1)

        but = gtk.Button(label="PermNode F3")
        self.add_accelerator(but, "F3")
        self.add_image(but, "permanent_node")
        c_box.add(but)
        self.button_handlers["PermNode"] = (but, -1)

        but = gtk.Button(label="StartNode F4")
        self.add_accelerator(but, "F4")
        self.add_image(but, "start_node")
        c_box.add(but)
        self.button_handlers["StartNode"] = (but, -1)

        but = gtk.Button(label="TrapNode F5")
        self.add_accelerator(but, "F5")
        self.add_image(but, "trap_node")
        c_box.add(but)
        self.button_handlers["TrapNode"] = (but, -1)

        but = gtk.Button(label="Transition F6")
        self.add_accelerator(but, "F6")
        self.add_image(but, "transition")
        c_box.add(but)
        self.button_handlers["Transition"] = (but, -1)

        but = gtk.Button(label="Constraints F7")
        self.add_accelerator(but, "F7")
        c_box.add(but)
        self.button_handlers["Constraints"] = (but, -1)

        # zoom
        but = self.wtree.get_widget("zoomp")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_ZOOM_IN, 3)
        but.set_image(image)
        self.button_handlers["zoom_p"] = (but, -1)
        but = self.wtree.get_widget("zoomm")
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_ZOOM_OUT, 3)
        but.set_image(image)
        self.button_handlers["zoom_m"] = (but, -1)


    def drawing_button_connect(self):
        """
        Connect the buttons to the controler of the graphic view
        Remember for each button the handler
        """
        (but, bhan) = self.button_handlers["Select"]
        bhan = but.connect("clicked",
                         self.current_edit_mvc.controler.set_action_select)
        self.button_handlers["Select"] = (but, bhan)

        (but, bhan) = self.button_handlers["InputNode"]
        bhan = but.connect("clicked",
                    self.current_edit_mvc.controler.set_action_new_input_node)
        self.button_handlers["InputNode"] = (but, bhan)

        (but, bhan) = self.button_handlers["SimpleNode"]
        bhan = but.connect("clicked",
                    self.current_edit_mvc.controler.set_action_new_simple_node)
        self.button_handlers["SimpleNode"] = (but, bhan)

        (but, bhan) = self.button_handlers["PermNode"]
        bhan = but.connect("clicked",
                    self.current_edit_mvc.controler.set_action_new_perm_node)
        self.button_handlers["PermNode"] = (but, bhan)


        (but, bhan) = self.button_handlers["StartNode"]
        bhan = but.connect("clicked",
                    self.current_edit_mvc.controler.set_action_new_start_node)
        self.button_handlers["StartNode"] = (but, bhan)

        (but, bhan) = self.button_handlers["TrapNode"]
        bhan = but.connect("clicked",
                    self.current_edit_mvc.controler.set_action_new_trap_node)
        self.button_handlers["TrapNode"] = (but, bhan)

        (but, bhan) = self.button_handlers["Transition"]
        bhan = but.connect("clicked",
                    self.current_edit_mvc.controler.set_action_new_transition)
        self.button_handlers["Transition"] = (but, bhan)

        (but, bhan) = self.button_handlers["Constraints"]
        bhan = but.connect("clicked", self.edit_constraints)
        self.button_handlers["Constraints"] = (but, bhan)

        (but, bhan) = self.button_handlers["zoom_p"]
        bhan = but.connect("clicked", self.current_edit_mvc.zoom_plus)
        self.button_handlers["zoom_p"] = (but, bhan)

        (but, bhan) = self.button_handlers["zoom_m"]
        bhan = but.connect("clicked", self.current_edit_mvc.zoom_minus)
        self.button_handlers["zoom_m"] = (but, bhan)

    def on_button_scroll_event(self, widget, event):
        """Handle zoom based on mouse scroll event on the overview"""
        if event.direction == gtk.gdk.SCROLL_UP:
            self.current_edit_mvc.zoom_plus(widget)
        elif event.direction == gtk.gdk.SCROLL_DOWN:
            self.current_edit_mvc.zoom_minus(widget)

    def add_image(self, widget, image_file):
        """Add image to a Button
        from http://www.pygtk.org/docs/pygtk/gtk-stock-items.html
        """
        image = gtk.Image()
        # Get resource
        template = pkg_resources.resource_filename(
            __name__,
            'images/' + image_file + '.png',
        )
        pixbuf = gtk.gdk.pixbuf_new_from_file(template)
        pixbuf = pixbuf.scale_simple(15, 15, gtk.gdk.INTERP_BILINEAR)
        image = gtk.image_new_from_pixbuf(pixbuf)
        # image.set_from_file(template)
        widget.set_image(image)

    def add_accelerator(self, widget, accelerator, signal="activate"):
        """Adds a keyboard shortcut"""
        if accelerator is not None:
            #if DEBUG:
                #print accelerator, widget.get_tooltip_text()
            key, mod = gtk.accelerator_parse(accelerator)
            # VISIBLE: if set, the accelerator is visible in a label
            widget.add_accelerator(signal,
                                   self.my_accelerators,
                                   key, mod,
                                   gtk.ACCEL_VISIBLE,
            )
            # print "The accelerator is well added with the signal " + signal

    def drawing_button_disconnect(self):
        """
        Disconnect graphic editor buttons
        Carefull: do not change value of handler for efficiency reason
        """
        for k in self.button_handlers.keys():
            bhan = self.button_handlers[k]
            bhan[0].disconnect(bhan[1])

    def drawing_button_disable(self):
        """
        Disconnect graphic editor buttons
        Carefull: do not change value of handler for efficiency reason
        """
        for k in self.button_handlers.keys():
            bhan = self.button_handlers[k]
            bhan[0].set_sensitive(False)

    def drawing_button_unable(self):
        """
        Disconnect graphic editor buttons
        Carefull: do not change value of handler for efficiency reason
        """
        for k in self.button_handlers.keys():
            bhan = self.button_handlers[k]
            bhan[0].set_sensitive(True)

    def on_destroy(self, widget, _dummy_event):
        """
        destroy if everything OK
        """
        # check if some models are modified
        for emvc in self.edit_mvc_list:
            if emvc.model.is_modified():
                name = emvc.model.name
                ask = False
                ask = confirm(None, 'Model '+name+' is modified - Quit anyway?')
                if not ask:
                    return True
            emvc.clean_subwin()
        gtk.main_quit()

    def show(self):
        """
        TODO check if useful
        """
        self.main_window.show_all()


    def delete_tab_callback(self, widget):
        """
        Delete current edit_MVC and corresponding view
        """
        self.remove_edit_mvc()



    def add_edit_mvc(self, model_name, model=None, layout=False):
        """
        create, register and display a new edit_mvc - close all windows
        associated with a previous edit_mvc
        """

        # edit MVC
        edm = EditMVC(self, model_name, model, layout)
        (eventbox, button) = create_custom_tab(edm.title)
        button.connect("clicked", self.delete_tab_callback)
        edm.tab_button = button

        # insert in emvc management
        page_index = self.graph_notebook.append_page(edm.viewpage, eventbox)
        self.edit_mvc_list.append(edm)
        self.set_current_edit_mvc(edm)
        self.graph_notebook.set_current_page(page_index)

    def add_display_mvc(self, model_name, model=None, layout=False):
        """
        create, register and display a new edit_mvc
        """
        # edit MVC
        edm = EditMVC(self, model_name, model, layout)
        (eventbox, button) = create_custom_tab(edm.title)
        button.connect("clicked", self.delete_tab_callback)
        edm.tab_button = button

        # insert in emvc management
        page_index = self.graph_notebook.append_page(edm.viewpage, eventbox)
        self.edit_mvc_list.append(edm)
        self.set_current_edit_mvc(edm, False) # do not destroy aux windows
        self.graph_notebook.set_current_page(page_index)

    @check_curent_model
    def remove_edit_mvc(self):
        """
        Remove current edit_MVC
        """
        eimvc = self.current_edit_mvc
        # modified model??
        ask = True
        if not eimvc.model.is_submodel():
            if eimvc.model.is_modified():
                ask = confirm(None, "Modified model. Do you want to delete?")
        if ask:
            # remove from notebook and navigator
            self.search_area.clear()
            self.search_frontier.clear()
            self.overview_window.get_child().get_child().clear()
            # following implies a switch page (thus disconnection)
            self.graph_notebook.remove(eimvc.viewpage)
            # remove from list
            self.edit_mvc_list.remove(eimvc)
            eimvc.clean_subwin()

    def open_macro(self, mnode):
        """
        open a macro state in an other tab
        """
        edm = EditMVC(self, mnode.name)
        edm.model.make_submodel(mnode)
        edm.model.get_root()
        # attach submodel view to whole model
        mnode.model.attach(edm.view)

        (eventbox, button) = create_custom_tab(edm.title)
        button.connect("clicked", self.delete_tab_callback)
        edm.tab_button = button
        page_index = self.graph_notebook.append_page(edm.viewpage, eventbox)
        self.edit_mvc_list.append(edm)
        self.set_current_edit_mvc(edm)
        edm.view.show()
        self.graph_notebook.set_current_page(page_index)

    def set_current_edit_mvc(self, edm, w_destroy=True):
        """
        display a new current edit item
        """
        # disconnect the currrent one if any
        if self.current_edit_mvc:
            self.save_constraints(None)
            self.current_edit_mvc.disconnect(self, w_destroy)

        if edm:
            self.current_edit_mvc = edm
            edm.connect(self)
            # refresh search
            self.search_area.set_model(edm.model)
            self.search_frontier.set_model(edm.model)

    def get_emvc_with_view(self, view):
        """
        Retreive the edit_MVC from the view
        """
        for emvc in self.edit_mvc_list:
            if emvc.view == view:
                return emvc
        return None

    def switch_graph_page_callback(self, widget, page, page_index):
        """
        Standard notebook call back
        """
        if page_index >= 0:
            the_view = self.graph_notebook.get_nth_page(page_index).draw
            edm = self.get_emvc_with_view(the_view)
            if edm: # for the first case
                self.set_current_edit_mvc(edm)
        else: # no more page (in case of delete)
            pass

    def ok_new_text(self, but, dialog):
        """
        Prompt if new model - to give the name
        """
        model_name = dialog.entry.get_text()
        dialog.destroy()
        self.add_edit_mvc(model_name)

    def cancel(self, but, dee):
        """
        what?
        """
        dee.destroy()


    def new_charts(self, widget):
        """
        create a new charts when you click on new
        """

        def on_enter(widget, event):
            """On ESC/Return key_press_event, destroy/valid this window."""
            keyval_name = gtk.gdk.keyval_name(event.keyval)
            if keyval_name == 'Return':
                self.ok_new_text(None, die)

            if keyval_name == 'Escape':
                die.destroy()

        # open an independant gtk.Entry for asking for the name
        die = DialogEntry("Insert a model name")
        die.entry.set_text("default_name")
        die.entry.connect('key_press_event', on_enter)
        die.okb.connect("clicked", self.ok_new_text, die)
        die.cancel.connect("clicked", self.cancel, die)
        die.run()

    def save_choice(self):
        """
        choice of file for save
        """
        dialog = gtk.Dialog("",
                            None,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            ("Yes", 0, "No", 1, "Cancel", 2))
        label = gtk.Label("Do yous want to delete previous xml model?")
        dialog.vbox.pack_start(label, True, False, 0)
        label.show()
        response = dialog.run()
        dialog.destroy()
        return response

    @check_curent_model
    def export_to_xml(self, widget):
        """
        open a window to save as xml file
        """
        fch = FileChooser("Export to xml Cadbiom model", "bcx files", "*.bcx")
        fch.set_current_name(self.current_edit_mvc.model.name + ".bcx")
        fch.do_action(self.create_xml_file)


    def create_xml_file(self, xml_file):
        """
        make a xml file with the current model
        """
        if self.current_edit_mvc.model.is_submodel():
            model = self.current_edit_mvc.controler.current_node.model
        else :
            model = self.current_edit_mvc.model
        try:
            xml = XmlVisitor(model)
            mfile = open(xml_file, 'w')
            mfile.write(xml.return_xml())
            mfile.close()
        except XmlException as xec:
            cancel_warn(xec.message)
            return

    def choose_xml_file(self, widget):
        """
        open a window to search xml file
        """
        fch = FileChooser("Import xml Cadbiom model", "bcx files", "*.bcx",
                          save_window=False)
        fch.do_action(self.import_from_xml_file)

    def import_from_xml_file(self, ffile):
        """
        As it says
        """
        self.import_from_xml(ffile, ffile=True)

    def import_from_xml(self, xml_cont, ffile=False):
        """
        open and parse an xml file or from db
        """
        if ffile:
            parsing = MakeModelFromXmlFile(xml_cont)
        else:
            parsing = MakeModelFromXmlString(xml_cont)
        # chart model
        model = parsing.get_model()
        model.modified = False
        self.add_edit_mvc(model.name, model)


    def choose_cadlang_file(self, widget):
        """
        open a window to search xml file
        """
        fch = FileChooser("Import from Cadbiom-chart lang", "cadbiom-l", "*.cal",
                          save_window=False)
        fch.do_action(self.import_from_cl_file)

    def import_from_cl_file(self, ffile):
        """
        As it says
        """
        crep = CompilReporter()
        fstream = ANTLRFileStream(ffile)
        lexer = cadlangLexer(fstream)
        lexer.set_error_reporter(crep)
        parser = cadlangParser(CommonTokenStream(lexer))
        parser.set_error_reporter(crep)
        model = ChartModel(ffile)
        parser.cad_model(model)
        if crep.error:
            DisplayError(crep, ffile)
            return
        model = parser.model
        self.add_edit_mvc(model.name, model, False)
        self.do_layout(None, "hierarchical_LR")


    def choose_pid_file(self, widget):
        """
        open a window to search xml file coming from PID database
        """
        # Pass the parent window to set modal mode on the child
        ImportPIDParam(self, self.main_window)

    def choose_BioPAX_file(self, widget):
        """
        open a window to import BioPAX data from a triplestore
        """
        # Pass the parent window to set modal mode on the child
        ImportBioPAXParams(self, self.main_window)

    @check_curent_model
    def export_to_lang(self, widget):
        """
        Export to CadLang
        """
        fch = FileChooser("Export to Cadbiom-chart lang", "cadbiom-l", "*.cal")
        fch.set_current_name(self.current_edit_mvc.model.name + ".cal")
        fch.do_action(self.compile_to_lang)

    def compile_to_lang(self, file_name):
        """
        Compile in view of exporting
        """
        out = open(file_name, "w")
        # decompiler visitor
        lvi = LangVisitor(out)
        self.current_edit_mvc.model.accept(lvi)
        out.close()

    def show_doc(self, widget):
        """
        Doc
        """
        url = 'http://cadbiom.genouest.org/cw_support.html'
        webbrowser.open(url)
        return

    def show_legend(self, widget):
        """
        Doc
        """
        self.legend = LegendWindow(self)

    @check_curent_model
    def export_picture(self, widget):
        """
        Export a picture (png,jpg) of the current model
        """
        fch = FileChooser("Export picture", "pictures", "*.png")
        fch.set_current_name(self.current_edit_mvc.model.name + ".png")
        fch.get_filter().add_pattern("*.png")
        fch.do_action(self.export_picture_to_file)

    @check_curent_model
    def export_picture_to_file(self, file_name):
        """
        As it says
        """

        edm = self.current_edit_mvc
        fns = file_name.split('.')
        if len(fns)!= 2:
            cancel_warn("Incorrect picture file name" )
            return
        suff = fns[1]
        pxm = edm.view.pixmap
        pxb = Pixbuf(COLORSPACE_RGB, False, 8,
                    edm.view.draw_width, edm.view.draw_height)
        pxb.get_from_drawable(pxm, colormap_get_system(), 0, 0, 0, 0, -1, -1)
        if suff == 'png':
            pxb.save(file_name, 'png')
        elif suff == 'jpg':
            pxb.save(file_name, "jpeg", {"quality":"100"})
        else:
            cancel_warn("Unknown picture format")

    @check_curent_model
    def do_layout(self, widget, layout_style):
        """
        Compute a layout of the model
        """

        edm = self.current_edit_mvc
        lvi = LayoutVisitor(edm.view, layout_style)
        edm.model.accept(lvi)
        edm.display()

    # Simulation
    @check_curent_model
    def on_simulate(self, widget):
        """
        Call simulation
        """
        reporter = CompilReporter()
        ChartSimulControler(self.current_edit_mvc, True, reporter)

    # Static analysis
    @check_curent_model
    def on_stats_info(self, widget):
        """Static analysis: Fill window with model informations.
        """
        reporter = CompilReporter()
        # get stats from StaticAnalyzer
        stan = StaticAnalyzer(reporter)
        stan.build_from_chart_model(self.current_edit_mvc.model)
        ststat = stan.get_statistics()
        window = STATWindow(ststat, self.current_edit_mvc, reporter, self)
        # Get Main widget and connect its "destroy" event
        window.window.connect("destroy", self.win_remove)

    @check_curent_model
    def on_frontier_scc(self, widget):
        """Static analysis: Compute connected components which are on the frontier
        """
        reporter = CompilReporter()
        stan = StaticAnalyzer(reporter)
        stan.build_from_chart_model(self.current_edit_mvc.model)
        # errors??
        lscc = stan.get_frontier_scc()
        window = SCCWindow(lscc, self.current_edit_mvc, reporter, self)
        # Get Main widget and connect its "destroy" event
        window.window.connect("destroy", self.win_remove)

    @check_curent_model
    def on_basal_activated_genes(self, widget):
        """Static analysis: Compute basal activated genes
        """
        reporter = CompilReporter()
        stan = StaticAnalyzer(reporter)
        stan.build_from_chart_model(self.current_edit_mvc.model)
        lwbag = stan.get_why_basal_genes()
        window = BAGWindow(lwbag, self.current_edit_mvc, reporter, self)
        # Get Main widget and connect its "destroy" event
        window.window.connect("destroy", self.win_remove)

    @check_curent_model
    def on_dependency_graph(self, widget):
        """Static analysis: Computation and export of dependency graphs
        """
        selected_menu = widget.get_name()
        reporter = CompilReporter()
        static_analyser = StaticAnalyzer(reporter)
        static_analyser.build_from_chart_model(self.current_edit_mvc.model)

        # Detect type of selected menu
        if selected_menu == "transitionGraph":
            graph = static_analyser.make_transition_dg()
        elif selected_menu == "dependencyGraph":
            graph = static_analyser.make_dependence_dg(True)
        else:
            graph = static_analyser.make_full_dependence_dg(True)

        # Open Filechooser to export graph file
        ch_opt = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE,
                   gtk.RESPONSE_OK)
        choice = gtk.FileChooserDialog("Save the graph as ...", None,
                                       gtk.FILE_CHOOSER_ACTION_SAVE, ch_opt)
        choice.set_default_response(gtk.RESPONSE_OK)

        choice.set_current_name(
            self.current_edit_mvc.model.name + '_' + \
            selected_menu + ".graphml")

        # add a filter to see only graphml files (*.graphml)
        filter = gtk.FileFilter()
        filter.set_name("graphml files")
        filter.add_pattern("*.graphml")
        choice.add_filter(filter)

        # add a filter to see only dot files (*.dot)
        filter = gtk.FileFilter()
        filter.set_name("dot files")
        filter.add_pattern("*.dot")
        choice.add_filter(filter)

        # add a filter to see all
        no_filter = gtk.FileFilter()
        no_filter.set_name("all")
        no_filter.add_pattern("*")
        choice.add_filter(no_filter)

        response = choice.run()

        if response == gtk.RESPONSE_OK:
            # Export to desired file type
            if 'dot' in choice.get_filter().get_name():
                # Dot
                static_analyser.export_2_dot(graph, choice.get_filename())
            else:
                # Graphml
                static_analyser.export_2_graphml(graph, choice.get_filename())

        elif response == gtk.RESPONSE_CANCEL:
            pass
        choice.destroy()

    def win_register(self, window):
        """Register a sub window
        This window will be destroyed when you connect its main widget
        event "destroy" to subwin_on_destroy()

        used by: STATWindow, SCCWindow, BAGWindow, LegendWindow
        """
        print "register"
        self.subwindows.add(window)

    def win_remove(self, window):
        """Destroy a sub window
        This window will be destroyed when you connect its main widget
        event "destroy" to subwin_on_destroy()

        used by: STATWindow, SCCWindow, BAGWindow, LegendWindow
        """
        print "remove"
        try:
            self.subwindows.remove(window)
        except KeyError:
            pass
        window.destroy()

    # Solve model
    @check_curent_model
    def on_check(self, widget):
        """
        Launch checker
        """
        reporter = CompilReporter()
        ChartChecker(self.current_edit_mvc, reporter, self)

    def get_em_with_model_name(self, name):
        """
        get em in list of edit_MVC
        """
        for edm in self.edit_mvc_list:
            if edm.title == name:
                return edm
        return None

    def update(self, mnode):
        """
        observer method
        """
        if mnode.name != self.current_edit_mvc.title:
            list_model = []
            for edm in self.edit_mvc_list:
                list_model.append(edm.model.name)
            if mnode.name in list_model:
                pass
            else:
                self.open_macro(mnode)
        else :
            pass


    def display_states(self, widget):
        """
        As it says
        """
        cst = self.chart_info.trans_info.trans.get_influencing_places()
        ndic = self.current_edit_mvc.model.simple_node_dict
        for ident in cst:
            try:
                ndic[ident].search_mark = True
            except:
                pass
        self.current_edit_mvc.view.update()

    def edit_constraints(self, widget):
        """
        Constraint editor
        """
        model = self.current_edit_mvc.model
        # what_to_do = save_constraints
        self.constraint_window =  BioSignalEditor('Constraints: '+model.name,
                                                   self, self.save_constraints)
        self.constraint_window.set_text(model.constraints)

    def save_constraints(self, edit):
        """
        For export
        """
        if self.constraint_window:
            model = self.current_edit_mvc.model
            model.constraints = edit.get_text()
            model.modified = True
            self.constraint_window = None


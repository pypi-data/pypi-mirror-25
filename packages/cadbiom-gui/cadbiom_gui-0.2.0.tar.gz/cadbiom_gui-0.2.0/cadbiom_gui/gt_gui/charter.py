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

from gtk.gdk import screen_height, screen_width, color_parse, \
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
from cadbiom_gui.gt_gui.chart_static.chart_stat_controler import ChartStatControler

from cadbiom.models.guard_transitions.chart_model import ChartModel
from cadbiom.models.guard_transitions.translators.chart_lang import LangVisitor
from cadbiom.models.guard_transitions.translators.chart_xml import \
                  XmlVisitor, MakeModelFromXmlFile, \
                  MakeModelFromXmlString, XmlException
from cadbiom.models.guard_transitions.translators.cadlangLexer import cadlangLexer
from cadbiom.models.guard_transitions.translators.cadlangParser import cadlangParser

from layout import LayoutVisitor

import pkg_resources

class Charter(object):
    """
    charter main class
    """
    BG_COLOR = '#edf5ff'
    def __init__(self, cad):
        self.ident = "charter"
        self.cad_manager = cad

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
        if (self.main_window):
            self.main_window.connect("delete_event", self.on_destroy)
        h_scr = screen_height()
        w_scr = screen_width()
        self.h_scr = int(h_scr)
        self.w_scr = int(w_scr)
        self.main_window.resize(int(w_scr * 0.9), int(h_scr * 0.9))
        color = color_parse(Charter.BG_COLOR)
        self.main_window.modify_bg(gtk.STATE_NORMAL, color)
        self.constraint_window = None

        # Accelerators
        self.my_accelerators = gtk.AccelGroup()
        self.main_window.add_accel_group(self.my_accelerators)

        # menu bar
        menu_bar = self.wtree.get_widget("menubar1")
        menu_bar.modify_bg(gtk.STATE_NORMAL, color)

        menu_bar = self.wtree.get_widget("menubar2")
        menu_bar.modify_bg(gtk.STATE_NORMAL, color)
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


        # Model Handling buttons
        button = self.wtree.get_widget("Simu_button")
        button.connect("clicked", self.on_simulate)

        button = self.wtree.get_widget("sa_button")
        button.connect("clicked", self.on_static)

        button = self.wtree.get_widget("Check_button")
        button.connect("clicked", self.check)

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

        but = gtk.Button(label = "Select")
        c_box.add(but)
        self.button_handlers["Select"] = (but, -1)

        but = gtk.Button(label = "InputNode")
        self.add_accelerator(but, "F1")
        c_box.add(but)
        self.button_handlers["InputNode"] = (but, -1)

        but = gtk.Button(label = "SimpleNode")
        self.add_accelerator(but, "F2")
        c_box.add(but)
        self.button_handlers["SimpleNode"] = (but, -1)

        but = gtk.Button(label = "PermNode")
        self.add_accelerator(but, "F3")
        c_box.add(but)
        self.button_handlers["PermNode"] = (but, -1)

        but = gtk.Button(label = "StartNode")
        self.add_accelerator(but, "F4")
        c_box.add(but)
        self.button_handlers["StartNode"] = (but, -1)

        but = gtk.Button(label = "TrapNode")
        self.add_accelerator(but, "F5")
        c_box.add(but)
        self.button_handlers["TrapNode"] = (but, -1)

        but = gtk.Button(label = "Transition")
        self.add_accelerator(but, "F6")
        c_box.add(but)
        self.button_handlers["Transition"] = (but, -1)

        but = gtk.Button(label = "Constraints")
        self.add_accelerator(but, "F7")
        c_box.add(but)
        self.button_handlers["Constraints"] = (but, -1)

        # zoom
        but = self.wtree.get_widget("zoomp")
        self.button_handlers["zoom_p"] = (but, -1)
        but = self.wtree.get_widget("zoomm")
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

    def on_destroy(self, widget, xxx):
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



    def add_edit_mvc(self, model_name, model = None, layout = False):
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

    def add_display_mvc(self, model_name, model = None, layout = False):
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
        self.set_current_edit_mvc(edm , False) # do not destroy aux windows
        self.graph_notebook.set_current_page(page_index)


    def remove_edit_mvc(self):
        """
        Remove current edit_MVC
        """
        if not self.current_edit_mvc:
            return
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
        # open an independant gtk.Entry for asking for the name
        die = DialogEntry("Insert a model name")
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

    def export_to_xml(self, widget):
        """
        open a window to save as xml file
        """
        fch = FileChooser("Export to xml", "bcx files", "*.bcx")
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
            mfile = open(xml_file,'w')
            mfile.write(xml.return_xml())
            mfile.close()
        except XmlException, xec:
            cancel_warn(xec.message)
            return

    def choose_xml_file(self, widget):
        """
        open a window to search xml file
        """
        fch = FileChooser("Import Cadbiom model", "bcx files", "*.bcx")
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
        fch = FileChooser("Import from Cadbiom-chart lang",
                          "cadbiom-l", "*.cal")
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
        self.do_layout(None,"hierarchical_LR")


    def choose_pid_file(self, widget):
        """
        open a window to search xml file coming from PID database
        """
        ImportPIDParam(self)

    def choose_BioPAX_file(self, widget):
        """
        open a window to import BioPAX data from a triplestore
        """
        ImportBioPAXParams(self, self.main_window)

    def export_to_lang(self, widget):
        """
        Export to CadLang
        """
        fch = FileChooser("Export to Cadbiom-chart lang", "cadbiom-l", "*.cal")
        fch.do_action(self.compile_to_lang)

    def compile_to_lang(self, file_name):
        """
        Compile in view of exporting
        """
        out = open(file_name,"w")
        # decompiler visitor
        lvi = LangVisitor(out)
        edm = self.current_edit_mvc
        if edm:
            edm.model.accept(lvi)
            out.close()
        else:
            return


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
        self.legend = LegendWindow(self.current_edit_mvc)

    def export_picture(self, widget):
        """
        Export a picture (png,jpg) of the current model
        """
        fch = FileChooser("Export picture", "pictures", "*.png")
        fch.get_filter().add_pattern("*.png")
        fch.do_action(self.export_picture_to_file)

    def export_picture_to_file(self, file_name):
        """
        As it says
        """
        if self.current_edit_mvc:
            edm = self.current_edit_mvc
        else:
            return

        fns = file_name.split('.')
        if len(fns)!= 2:
            cancel_warn("Incorrect picture file name" )
            return
        suff = fns[1]
        pxm = edm.view.pixmap
        pxb = Pixbuf(COLORSPACE_RGB, False, 8,
                    edm.view.draw_width, edm.view.draw_height)
        pxb.get_from_drawable(pxm, colormap_get_system() , 0, 0, 0, 0, -1, -1)
        if suff == 'png':
            pxb.save(file_name, 'png')
        elif suff == 'jpg':
            pxb.save(file_name, "jpeg", {"quality":"100"})
        else:
            cancel_warn("Unknown picture format")

    def do_layout(self, widget, layout_style):
        """
        Compute a layout of the model
        """
        if self.current_edit_mvc:
            edm = self.current_edit_mvc
        else:
            return
        lvi = LayoutVisitor(edm.view, layout_style)
        edm.model.accept(lvi)
        edm.display()

    # simulation
    def on_simulate(self, widget):
        """
        Call simulation
        """
        reporter = CompilReporter()
        if self.current_edit_mvc:
            chart_simul = ChartSimulControler(self.current_edit_mvc,
                                              True, reporter)


    # static analysis
    def on_static(self, widget):
        """
        Call static analysis
        """
        if self.current_edit_mvc:
            reporter = CompilReporter()
            chart_static = ChartStatControler(self.current_edit_mvc, reporter)

    # solve
    def check(self, widget):
        """
        Launch checker
        """
        if self.current_edit_mvc:
            reporter = CompilReporter()
            chart_check = ChartChecker(self.current_edit_mvc, reporter)


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


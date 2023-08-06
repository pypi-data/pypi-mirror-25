## Filename    : chart_simul_controler.py
## Author(s)   : Michel Le Borgne
## Created     : 04/2010
## Revision    :
## Source      :
##
## Copyright 2012 : IRISA/IRSET
##
## This library is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License  published
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
Controller and auxiliary widgets for simulations with gui.
"""
import gtk
from time import clock


from chart_chrono import ChartChrono
from cadbiom_gui.gt_gui.utils.warn import cancel_warn
from cadbiom.models.guard_transitions.simulator.simul_exceptions import \
                              SimulException, SimulStopException
from cadbiom.models.guard_transitions.simulator.chart_simul import ChartSimulator
from cadbiom.models.guard_transitions.simulator.simul_aux import ModelExtractorVisitor
from cadbiom.models.guard_transitions.analyser.ana_visitors import FrontierVisitor
from cadbiom_gui.gt_gui.utils.listDisplay  import ToggleList
from cadbiom_gui.gt_gui.utils.fileHandling import FileChooser

import pkg_resources

class ChartSimulControler(object):
    """
    Control different parameters of a simulation and display panel
    """
    def __init__(self, emvc, sim_option, reporter,
                 init_places = None, icseq=None, parent = None):
        # loading and initializing the simulator model
        self.edit_mvc = emvc
        self.model = emvc.model                    # chart model
        self.option = sim_option                   # free clock treatment option
        self.reporter = reporter                   # display error messages
        self.sim = ChartSimulator()                # simulation model
        self.__reload = True
        if icseq: # simulation with conditions from checker
            self.sim.set_act_input_stream(icseq)
            self.__reload = False
        if init_places:
            self.__reload = False
        self.sim.build(self.model, sim_option, reporter)
        if reporter.error:
            DisplayError(reporter, self.model.name)
            return

        self.init_places = init_places
        if self.init_places:
            self.sim.simul_init_places(self.init_places)
        else:
            self.sim.simul_init()

        self.max_step = 0
        self.tempo = 0.0
        self.stop = False
        self.selected_chrono = False
        self.main_window = None
        self.selected_window = None

        # graphical interface
        # Set the Glade
        template = pkg_resources.resource_filename(
            __name__,
            "../chart_glade/chart_simulator.glade"
        )
        self.wtree = gtk.glade.XML(template)

        # Get the Main Window, and connect the "destroy" event
        self.main_window = self.wtree.get_widget("window1")
        self.main_window.set_title("Simulation: "+self.model.name)
        if (self.main_window):
            self.main_window.connect("destroy", self.on_destroy)
        self.main_window.set_position(gtk.WIN_POS_CENTER)
        self.main_window.set_keep_above(True)

        # frontier button (disconnected when icseq are computed)
        button = self.wtree.get_widget("frontier_button")
        button.connect("clicked", self.on_select_front)
        if icseq:
            button.set_sensitive(False)

        # whole button (disconnected when ic are computed)
        button = self.wtree.get_widget("whole_button")
        button.connect("clicked", self.on_select_whole)
        if icseq:
            button.set_sensitive(False)

        # start button
        button = self.wtree.get_widget("startbutton")
        button.connect("clicked", self.on_start)

        # chrono nutton
        button = self.wtree.get_widget("chronobutton")
        button.connect("clicked", self.on_chrono)

        # input file choser (disconnected when ic are computed)
        button = self.wtree.get_widget("input_file_button")
        if not self.sim.has_input():
            button.set_sensitive(False)
        button.connect("clicked", self.on_input_file_selected)
        if icseq:
            button.set_sensitive(False)

        # step button
        button = self.wtree.get_widget("stepbutton")
        button.connect("clicked", self.on_step_simul)


        # check button for chronogram
        self.cb_chrono = self.wtree.get_widget("cb_chrono")

        # nb of steps widget
        self.nb_step_entry = self.wtree.get_widget("nbsteps")

        # slider
        self.range = self.wtree.get_widget("hscale1")
        self.range.set_update_policy(gtk.UPDATE_DISCONTINUOUS)
        self.range.connect("value_changed", self.on_delay)

        # init button"
        button = self.wtree.get_widget("initbutton")
        button.connect("clicked", self.on_init)

        # reload button (disconnected when using computed input clocks)
        button = self.wtree.get_widget("reloadbutton")
        button.connect("clicked", self.on_reload)
        if not self.__reload:
            button.set_sensitive(False)

        # extract button
        button = self.wtree.get_widget("extractbutton1")
        button.connect("clicked", self.on_extract, False)
        button = self.wtree.get_widget("extractbutton2")
        button.connect("clicked", self.on_extract, True)

        # register itself for parent or emvc
        if parent:
            parent.win_register(self)
        else:
            self.edit_mvc.win_register(self)
        self.parent = parent

        # display
        self.main_window.show_all()
        #gtk.main()

    def on_destroy(self, widget):
        """
        destroy the windows after all secondary windows
        """
        if self.selected_window:
            self.selected_window.destroy()
        if self.sim.chrono:
            self.sim.chrono.window.destroy()
        self.model.clean()
        self.model.notify()
        if self.parent:
            self.parent.win_remove(self)
        else:
            self.edit_mvc.win_remove(self)
        if self.main_window:
            self.main_window.destroy()

    def destroy(self):
        """
        Used if chart_simul_controller is itself a secondary window
        """
        self.on_destroy(None)

    def on_step_simul(self, widget):
        """
        callback for step by step simulation
        """
        # in case a selected chrono is open"
        if self.selected_chrono:
            self.sim.chrono.destroy()
            self.sim.chrono = None
            self.selected_chrono = False
        if self.sim.has_input() and not self.sim.input_buffer:
            # inputs present and no input file
            cancel_warn("Set input file before simulation")
            return
        try:
            self.sim.simul_step()
            if self.sim.chrono:
                self.sim.chrono.register(self.sim)
                self.sim.chrono.update()
        except SimulStopException:
            cancel_warn("Simulation reached end of input")
        except SimulException , exc:
            cancel_warn("Problem in simulation: " + exc.__str__())


    def on_input_file_selected(self, widget):
        """
        chose an input file
        """
        fch = FileChooser("Input file", "", "*", save_window=False)
        fch.do_action(self.set_input_file)

    def set_input_file(self, filename):
        """
        connect an input file
        """
        inputfile = open(filename, 'r')
        fline = inputfile.readline()
        line_split = fline.split()
        inputfile.close()
        # test type of file on first line
        if line_split[0] == "$inputs": # old coded input
            try:
                self.sim.set_cfile_input_stream(filename)
            except Exception , exc:
                cancel_warn("Error in coded input file loading" + exc.__str__())
            return
        elif  line_split[0] == "%": # activated input
            try:
                self.sim.set_act_file_input_stream(filename)
            except Exception , exc:
                mess = "Error in active input file loading" + exc.__str__()
                cancel_warn(mess)
            return
        else: # assume scenario
            try:
                self.sim.set_sce_file_input_stream(filename)
            except Exception , exc:
                cancel_warn("Error in scenario loading" + exc.__str__())
            return


    def on_init(self, widget):
        """
        initialisation of the simulator
        """
        if self.sim.init_places:
            self.sim.simul_init_places(self.sim.init_places)
        else:
            self.sim.simul_init() # standard init from graphics

        if self.sim.input_buffer:
            self.sim.input_buffer.rewind()
        if self.sim.chrono:
            if self.selected_chrono:
                self.sim.chrono.window.destroy()
                self.sim.chrono = None
                self.selected_chrono = False
            else:
                self.sim.chrono.rewind()
                self.sim.chrono.register(self.sim)
                self.sim.chrono.update()

    def on_start(self, widget):
        """
        start a simulation
        """
        # check inputs
        if self.sim.has_input() and not self.sim.input_buffer:
            # inputs present and no input file
            cancel_warn("Set input file before simulation")
            return
        # read nb of steps
        max_step = self.nb_step_entry.get_text()
        if max_step == "":
            self.max_step = 0
            cancel_warn("Set number of simulation steps")
        else:
            self.max_step = int(max_step)
        self.step_count = 0
        self.stop = False
#        a = threading.Thread(None, self.loop, None, (), None)
#        a.start()
#        return
        # selected chrono
        if self.cb_chrono.get_active():
            if self.sim.chrono:
                self.sim.chrono.destroy()
            self.sim.chrono = ChartChrono.for_trajectory(self.sim)
            self.selected_chrono = True
        self.loop()
        if self.selected_chrono:
            self.sim.chrono.display_selected_chrono()

    def loop(self):
        """
        temporized loop for automatic simulation
        """
        if self.sim.chrono:
            self.sim.chrono.register(self.sim)
        while not self.stop and self.step_count < self.max_step:
            start_time = clock()
            try:
                self.sim.simul_step()
                self.step_count = self.step_count + 1
            except SimulStopException:
                cancel_warn("Simulation reached end of input")
                return
            except SimulException , exc:
                cancel_warn("Problem in simulation:" + exc.__str__())
                return
            self.model.notify()
            if self.sim.chrono:
                self.sim.chrono.register(self.sim)
                self.sim.chrono.update()
            # tempo
            if self.tempo > 0.01:
                time = clock()
                delay = time - start_time
                while delay < self.tempo:
                    time = clock()
                    delay = time - start_time

    def on_chrono(self, widget):
        """
        setup chronogram
        """
        if not self.sim.chrono:
            # logical analyser
            self.sim.chrono = ChartChrono.from_simulation_model(self.sim)
            self.sim.chrono.register(self.sim)
            self.sim.chrono.update()
        else:
            self.sim.chrono.destroy()
            self.sim.chrono = None
            self.selected_chrono = False

    def on_delay(self, widget):
        """
        adjust the simulation timer
        """
        self.tempo = self.range.get_value()/50.0

    def on_reload(self, widget):
        """
        reset the simulator
        """
        if not self.__reload:
            cancel_warn("No reload allowed")
            return
        if self.sim.chrono:
            self.sim.chrono.destroy()
        input_file = self.sim.input_file
        self.sim = ChartSimulator()
        self.reporter.error = False
        self.sim.build(self.model, self.option, self.reporter)
        if self.reporter.error:
            DisplayError(self.reporter, self.model)
            return
        if input_file:
            try:
                self.set_input_file(input_file)
            except SimulException, exc:
                self.sim.input_buffer = None
                cancel_warn ("old input file inadequate - redefine input")
        if self.sim.chrono:
            self.sim.chrono.destroy()
            self.sim.chrono = ChartChrono.from_simulation_model(self.sim)
        if self.init_places:
            self.sim.simul_init_places(self.init_places)
        else:
            self.sim.simul_init() # standard init from graphics
        if self.sim.chrono:
            self.sim.chrono.register(self.sim)
            self.sim.chrono.update()
        self.max_step = 0
        self.tempo = 0.0
        self.stop = False

    def on_extract(self, widget, ex_type):
        """
        extract the part of a model used in last simulation
        """
        if self.sim.get_step() < 2:
            return
        mex = ModelExtractorVisitor('sim_extract', ex_type)
        self.model.accept(mex)
        model = mex.sub_model
        self.edit_mvc.charter.add_display_mvc(model.name, model, False)
        self.edit_mvc.charter.do_layout(None,"hierarchical_LR")

    def on_select_front(self, widget):
        """
        selection of frontier activated places at initialization
        """
        self.selected_window = SelectPlaceWindow(self, True)

    def on_select_whole(self, widget):
        """
        selection of activated places at initialization
        """
        self.selected_window = SelectPlaceWindow(self, False)




class DisplayError(object):
    """
    auxiliary widget for simulator
    """
    def __init__(self, report, model_name, text=None):
        self.main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #self.main_window.connect("destroy", gtk.main_quit)
        self.main_window.set_title("Compiler errors or info: " + model_name)
        self.main_window.set_position(gtk.WIN_POS_CENTER)
        self.main_window.set_keep_above(True)
        self.main_window.set_default_size(500, 300)

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_IN)
        self.main_window.add(scroll)

        write = gtk.TextView()
        if report:
            write.get_buffer().set_text(report.memory)
        else:
            write.get_buffer().set_text(text)
        scroll.add_with_viewport(write)
        self.main_window.show_all()
        #gtk.main()

class SelectPlaceWindow(object):
    """
    Select the activated place for initialization
    """
    def __init__(self,  simulator, frontier_bool):

        self.simulator = simulator
        # graphical interface
        # Set the Glade file
        template = pkg_resources.resource_filename(
            __name__,
            "../chart_glade/simu_places.glade"
        )
        self.wtree = gtk.glade.XML(template)

        # Get the Main Window, and connect the "destroy" event
        self.window = self.wtree.get_widget("window1")
        self.window.set_title("Selected window")
        self.window.set_size_request(250, 400)
        self.window.set_position(gtk.WIN_POS_NONE)
        self.window.set_keep_above(True)

        place_notebook = self.wtree.get_widget("place_notebook")
        # search
        if frontier_bool:
            self.search_area = ToggleFrontier(self.simulator.model,
                                              place_notebook, "Frontier")
        else:
            self.search_area = ToggleWholeModel(self.simulator.model,
                                                place_notebook,
                                                "Simple node list")


        # button
        button = self.wtree.get_widget("select_button")
        button.connect("clicked", self.on_select)
        button = self.wtree.get_widget("unselect_button")
        button.connect("clicked", self.on_unselect)
        button = self.wtree.get_widget("save_button")
        button.connect("clicked", self.on_save)
        button = self.wtree.get_widget("load_button")
        button.connect("clicked", self.on_load)
        button = self.wtree.get_widget("validate_button")
        button.connect("clicked", self.on_validate)

        # display
        self.window.show_all()


    def destroy(self):
        """
        as usual for aux widget
        """
        self.window.destroy()

    def on_select(self, widget):
        """
        ???
        """
        self.search_area.sn_viewer.select_all(widget)

    def on_unselect(self, widget):
        """
        ???
        """
        self.search_area.sn_viewer.clear(widget)

    def on_save(self, widget):
        """
        open a window to save initialization
        """
        choice = gtk.FileChooserDialog("Save initialization", None,
                                       gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        choice.set_default_response(gtk.RESPONSE_OK)

        #add a filter to see only txt files
        filter = gtk.FileFilter()
        filter.set_name("text files")
        filter.add_pattern("*.txt")
        choice.add_filter(filter)

        #add a filter to see all
        no_filter = gtk.FileFilter()
        no_filter.set_name("all")
        no_filter.add_pattern("*")
        choice.add_filter(no_filter)

        response = choice.run()
        if response == gtk.RESPONSE_OK:
            self.create_init_file(choice.get_filename())
        elif response == gtk.RESPONSE_CANCEL:
            pass
            #print 'Closed, no files selected'
        choice.destroy()

    def on_load(self, widget):
        """
        open a window to search xml file coming from PID database
        """
        choice = gtk.FileChooserDialog("Import from xml", None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        choice.set_default_response(gtk.RESPONSE_OK)

        #add a filter to see only xml files
        filter = gtk.FileFilter()
        filter.set_name("text files")
        filter.add_pattern("*.txt")
        choice.add_filter(filter)

        #add a filter to see all
        no_filter = gtk.FileFilter()
        no_filter.set_name("all")
        no_filter.add_pattern("*")
        choice.add_filter(no_filter)

        response = choice.run()
        if response == gtk.RESPONSE_OK:
            self.load_init_file(choice.get_filename())
        elif response == gtk.RESPONSE_CANCEL:
            #print 'Closed, no files selected'
            pass
        choice.destroy()

    def on_validate(self, widget):
        """
        validate the choice of activated places
        """
        self.set_places()
        self.destroy()

    def create_init_file(self, file_name):
        """
        make a txt file with the current selected places
        """
        file = open(file_name,'w')
        list_of_places = self.search_area.get_selected_keywords()
        for place in list_of_places :
            file.write(str(place)+'\n')
        file.close()
        return

    def load_init_file(self, file_name):
        """
        load a file to initialize the simulator
        """
        list_of_places = []
        file = open(file_name,'r')
        for line in file:
            name = line[:-1]
            if name not in self.search_area.list_nodes :
                cancel_warn("Name in the file not in the model")
                return
            list_of_places.append(name)
        self.search_area.sn_viewer.set_selected_items(list_of_places)
#        self.simulator.sim.simul_init_places(list_of_places)
#        self.destroy()

    def set_places(self):
        """
        set the chosen activated places
        """
        self.simulator.init_places = self.search_area.get_selected_keywords()
        skw = self.search_area.get_selected_keywords()
        self.simulator.sim.simul_init_places(skw)

class ToggleWholeModel(object):
    """
    List of simple nodes for searching
    """
    def __init__(self, model, notebook, label):
        self.model = model
        self.model_changed = True
        self.notebook = notebook

        # simple nodes
        sn_frame = gtk.Frame()
        vbox = gtk.VBox(False, 0)
        sn_frame.add(vbox)
        # simple nodes list
        self.sn_viewer = ToggleList()
        label = gtk.Label(label)
        # wrap into scrollwindow
        scroll = gtk.ScrolledWindow()
        scroll.add_with_viewport(self.sn_viewer)
        vbox.pack_start(scroll, True, True, 0)

        notebook.append_page(sn_frame, label)

        # get node names
        lnode = model.get_simple_node_names()
        lnode.sort()
        self.list_nodes = lnode
        # display node names
        self.sn_viewer.refresh(lnode)

    def get_selected_keywords(self):
        """
        retrieve the selected items
        """
        return self.sn_viewer.get_selected_items()

class ToggleFrontier(ToggleWholeModel):
    """
    List of frontier nodes for searching
    """
    def __init__(self, model, notebook, label):
        ToggleWholeModel.__init__(self, model, notebook, label)

        self.model = model
        # get node names
        lnode = self.get_frontier_node_names()
        lnode.sort()
        self.list_nodes = lnode
        # display node names
        self.sn_viewer.refresh(lnode)

    def get_frontier_node_names(self):
        """
        retrieve frontier nodes from the model
        """
        fvi = FrontierVisitor()
        self.model.accept(fvi)
        return fvi.frontier

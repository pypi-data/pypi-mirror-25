## Filename    : chart_checker_controler.py
## Author(s)   : Michel Le Borgne
## Created     : 05/2011
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
Collection of widgets for properties checking
"""
import gtk

from cadbiom.models.clause_constraints.mcl.MCLAnalyser import MCLAnalyser
from cadbiom_gui.gt_gui.chart_simulator.chart_simul_controler import ChartSimulControler
from cadbiom_gui.gt_gui.chart_simulator.chart_chrono import ChartChrono
from cadbiom_gui.gt_gui.utils.warn import ok_warn, cancel_warn, confirm
from cadbiom.models.guard_transitions.simulator.chart_simul import  ChartSimulator
from cadbiom.models.clause_constraints.mcl.MCLQuery import MCLSimpleQuery
from cadbiom import commons as cm

import pkg_resources

LOGGER = cm.logger()


class ChartChecker(object):
    """
    This class provide a gui interface for checking some queries
    """

    def __init__(self, emvc, reporter, parent=None):
        self.__emvc = emvc                    # edit mvc - link with charter
        self.__reporter = reporter
        self.__occ_form = OccurenceForm(emvc, reporter)
        self.__current_form = self.__occ_form

        # graphical interface
        self.__main_window = gtk.Window()
        self.__main_window.set_title("Property check: " +
                                     self.__emvc.model.name)
        if (self.__main_window):
            self.__main_window.connect("destroy", self.__on_destroy)
        self.__main_window.set_position(gtk.WIN_POS_CENTER)
        self.__main_window.resize(600, 300)

        if parent:
            # Set window above all windows
            self.__main_window.set_transient_for(parent.main_window)

        # Event on_escape key pressed
        self.__main_window.connect('key_press_event', self.on_escape)

        # register as auxiliary window
        self.__emvc.win_register(self)

        # display
        self.__main_window.add(self.__current_form.get_frame())
        self.__main_window.show_all()

    def __on_destroy(self, widget):
        """
        delete window and dependant sub widgets
        """
        self.__current_form.clean_subwin()
        if self.__main_window:
            self.__main_window.destroy()

    def destroy(self):
        """
        call back adaptor
        """
        self.__on_destroy(None)

    def on_escape(self, widget, event):
        """On ESC key_press_event, destroy this window."""
        if gtk.gdk.keyval_name(event.keyval) == "Escape":
            self.__main_window.destroy()


class OccurenceForm(object):
    """
    Former class for occurence checking
    Now general simple query checking
    """
    def __init__(self, emvc, er_rep):
        self.__emvc = emvc
        self.__model = emvc.model  # chart model
        self.__mcla = None         # clause constraint model analyser
        self.__error_reporter = er_rep
        template = pkg_resources.resource_filename(
            __name__,
            "../chart_glade/occurence_form.glade"
        )
        self.__wtree = gtk.glade.XML(template)
        self.__window = self.__wtree.get_widget("windowOcc")
        wid = self.__wtree.get_widget("frameOcc")
        self.__frame = wid.get_child()
        wid.remove(self.__frame)

        # information
        possible = self.__wtree.get_widget("possible")
        possible.set_active(True)
        self.possible = True
        possible.connect("toggled", self.rb_callback, 'p')
        impossible = self.__wtree.get_widget("impossible")
        impossible.connect("toggled", self.rb_callback, 'i')

        self.step_entry = self.__wtree.get_widget("max_step")
        self.step_entry.set_text('10')
        self.step_entry.connect("changed", self.on_entry_changed)
        self.property_entry = self.__wtree.get_widget("property_entry")
        self.property_entry.connect("changed", self.on_entry_changed)
        self.inv_prop_entry = self.__wtree.get_widget("property_entry2")
        self.inv_prop_entry.connect("changed", self.on_entry_changed)
        self.start_prop_entry = self.__wtree.get_widget("property_entry3")
        self.start_prop_entry.connect("changed", self.on_entry_changed)

        # yes/no button
        button = self.__wtree.get_widget("button_yn")
        button.connect("clicked", self.on_yn)
        # conditions button
        button = self.__wtree.get_widget("button_cond")
        button.connect("clicked", self.on_cond)

        # condition exploration
        self.max_sol_entry = self.__wtree.get_widget("entry_nbsol")
        self.max_sol_entry.set_text('10')
        self.max_sol_entry.connect("changed", self.on_entry_changed)
        self.but_solutions = self.__wtree.get_widget("but_solutions")
        self.but_solutions.connect("clicked", self.on_solutions)
        self.but_solutions.set_sensitive(False)

        self.but_cam = self.__wtree.get_widget("but_cam")
        self.but_cam.connect("clicked", self.on_cam)
        self.but_cam.connect("clicked", self.on_entry_changed)
        self.but_cam.set_sensitive(False)

        # children
        self.__aux_win = []

    def get_frame(self):
        """
        as name says
        """
        return self.__frame

    def rb_callback(self, widget, idw):
        """
        possible and impossible call back
        """
        if idw == 'p':
            self.possible = True
        else:
            self.possible = False

    def on_entry_changed(self, widget):
        """
        react in cas of change in entries
        """
        #  buttons
        self.but_solutions.set_sensitive(False)
        self.but_cam.set_sensitive(False)

    def on_yn(self, widget):
        """
        lauch a satisfiability test
        """
        # get info
        final_prop = self.property_entry.get_text()
        if len(final_prop) == 0:
            cancel_warn("Void property")
            return
        inv_prop = self.inv_prop_entry.get_text()
        start_prop = self.start_prop_entry.get_text()
        max_step_str = self.step_entry.get_text()
        if len(max_step_str) == 0:
            cancel_warn("Number of steps not specified")
            return
        max_step = int(max_step_str)
        self.mcla = MCLAnalyser(self.__error_reporter)
        self.mcla.build_from_chart_model(self.__model)
        if self.__error_reporter.error:
            cancel_warn(self.__error_reporter.memory)
            self.__error_reporter.reset()
            return
        # solve
        if self.possible:
            if len(inv_prop) == 0:
                inv_prop = None
            else :
                inv_prop = "not ("+inv_prop+")"

            if len(start_prop) == 0:
                start_prop = None
            query = MCLSimpleQuery(start_prop, inv_prop, final_prop)
            reach = self.mcla.sq_is_satisfiable(query, max_step)

            if self.__error_reporter.error:
                cancel_warn(self.__error_reporter.memory)
                self.__error_reporter.reset()
                return
            if reach:
                ok_warn("Yes, we can!","green")
            else:
                ok_warn("NO","red")
        else:
            if len(inv_prop) != 0:
                final_prop = "not ("+final_prop+" and "+inv_prop+")"

            query = MCLSimpleQuery(start_prop, inv_prop, None)
            inv = self.mcla.sq_is_satisfiable(query, max_step)
            if self.__error_reporter.error:
                cancel_warn(self.__error_reporter.memory)
                self.__error_reporter.reset()
                return
            if inv:
                ok_warn("Yes, we can","green")
            else:
                ok_warn("NO","red")

    def on_cond(self, widget):
        """
        launch solution computations
        """
        # desactivate buttons
        self.but_solutions.set_sensitive(False)
        self.but_cam.set_sensitive(False)

        # get info
        final_prop = self.property_entry.get_text()
        if len(final_prop) == 0:
            cancel_warn("Void property")
            return
        inv_prop = self.inv_prop_entry.get_text()
        start_prop = self.start_prop_entry.get_text()
        max_step_str = self.step_entry.get_text()
        if len(max_step_str) == 0:
            cancel_warn("Number of steps not specified")
            return
        max_step = int(max_step_str)
        max_sol_str = self.max_sol_entry.get_text()
        if len(max_sol_str) == 0:
            cancel_warn("Number of solutions not specified")
            return
        max_sol = int(max_sol_str)

        self.mcla = MCLAnalyser(self.__error_reporter)
        self.mcla.build_from_chart_model(self.__model)
        if self.__error_reporter.error:
            cancel_warn(self.__error_reporter.memory)
            self.__error_reporter.reset()
            return

        # solve
        if self.possible:
            LOGGER.debug("OccurenceForm.on_cond:: Solve is possible !")
            if len(inv_prop) == 0:
                inv_prop = None
            else :
                inv_prop = "not ("+inv_prop+")"

            if len(start_prop) == 0:
                start_prop = None

            query = MCLSimpleQuery(start_prop, inv_prop, final_prop)
            self.lsol = self.mcla.sq_frontier_solutions(query ,
                                                        max_step, max_sol)
            LOGGER.debug("OccurenceForm.on_cond:: Solutions: " + \
                         str(len(self.lsol)))
            if self.__error_reporter.error:
                cancel_warn(self.__error_reporter.memory)
                self.__error_reporter.reset()
                return
        else:
            LOGGER.debug("OccurenceForm.on_cond:: Solve is NOT possible !")
            if len(inv_prop) != 0:
                final_prop = "not ("+final_prop+" and "+inv_prop+")"
            query = MCLSimpleQuery(start_prop, inv_prop, None)
            self.lsol = self.mcla.sq_frontier_solutions(query,
                                                        max_step, max_sol)
            LOGGER.debug("OccurenceForm.on_cond:: Solutions: " + \
                         str(len(self.lsol)))
            if self.__error_reporter.error:
                cancel_warn(self.__error_reporter.memory)
                self.__error_reporter.reset()
                return


        # affectation
        self.property = final_prop
        self.inv_prop = inv_prop
        self.start_prop = start_prop
        self.max_step = max_step
        self.max_sol = max_sol

        if len(self.lsol) == 0:
            cancel_warn("No conditions")
            return

        # activate buttons
        self.but_solutions.set_sensitive(True)
        self.but_cam.set_sensitive(True)

    def on_solutions(self, widget):
        """
        display solutions
        """
        SolutionWindow(self.lsol, self.__emvc, self.__error_reporter, self)

    def on_common(self, widget):
        """
        obsolete
        """
#        common_number=self.mcla.get_common_sol(self.mcla.solutions)
#        if len(common_number)!=0 :
#            common_name=self.mcla.get_state_list_from_solution(common_number)
#            common_length=self.mcla.get_nb_activated(common_number)
#            suff=self.mcla.is_sufficient(common_number, self.inv_prop,
#                                         self.property, self.max_step)
#            Common_Window(common_name, common_length, suff, self.emvc,
#                                         self.__error_reporter, self)
#        else :
#            ok_warn("There is no common solution")
        pass

    def on_cam(self, widget):
        """
        launch mac computations
        """
        ask = confirm(None, 'This process takes time' + '\n' +
                    'You will not be able to use cadbiom.'+'\n' +
                    ' Do you want to continue ?')
        if ask:
            query = MCLSimpleQuery(self.start_prop,
                                   self.inv_prop, self.property)
            cam_list = self.mcla.mac_search(query, self.max_step)
            if len(cam_list)==0 :
                ok_warn("The solver returns an empty list" +
                        "\n"+" you should refine your query")
            else :
                CNSWindow(cam_list, self.__emvc,
                          self.__error_reporter, self)

    # sub windows management
    def win_register(self, win):
        """
        register sub window for destroy
        """
        self.__aux_win.append(win)

    def win_remove(self, win):
        """
        used when the sub window destroys itself
        """
        if win in self.__aux_win:
            self.__aux_win.remove(win)

    def clean_subwin(self):
        """
        destroy all registered subwindows
        """
        for win in self.__aux_win:
            win.destroy()

    def destroy(self):
        """
        destroy all
        """
        self.clean_subwin()
        if self.__window:
            self.__window.destroy()


class SolutionWindow(object):
    """
    Class used for displaying solutions
    """
    def __init__(self, l_fsol, emvc, reporter, parent):
        """
        @param l_fsol: list<FrontierSolution>
        @param emvc: edit_mvc
        @param reporter: Classical reporter
        @param parent: parent widget
        """
        self.emvc = emvc
        self.reporter = reporter
        # frontier place list extraction and ic sequence extraction
        self.l_solutions = []
        self.l_icseq = []
        for fsol in l_fsol:
            self.l_solutions.append(fsol.activated_frontier)
            self.l_icseq.append(fsol.ic_sequence)

        self.aux_win = []
        self.simul = None

        self.compt = 0
        self.choice = 0
        self.textview_list = []

        # window creation
        template = pkg_resources.resource_filename(
            __name__,
            "../chart_glade/checker_solutions.glade"
        )
        self.wtree = gtk.glade.XML(template)
        self.window = self.wtree.get_widget("window1")

        self.window.set_resizable(True)
        height = gtk.gdk.screen_height()
        height = int(height * 0.30)
        self.window.set_size_request(700, height)


        # button save choice
        button = self.wtree.get_widget("but_sv_choice")
        button.connect("clicked", self.on_save, False)

        # button save all
        button = self.wtree.get_widget("but_sv_all")
        button.connect("clicked", self.on_save, True)
        if len(self.l_solutions) == 1:
            button.set_sensitive(False)

        # info label
        info = self.wtree.get_widget("label_nbsol")
        info.set_text(str(len(self.l_solutions))+" solutions found")

        self.frame_sol =  self.wtree.get_widget("frame_sol")
        # button frame
        vbox = gtk.VBox(False, 0)
        self.frame_sol.add(vbox)
        vbox.show()

        scroll = gtk.ScrolledWindow()
        vbox.pack_start(scroll)

        vbox2 = gtk.VBox()
        scroll.add_with_viewport(vbox2)
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.button_group = None

        frame = self.build_button_frame(self.l_solutions[0])
        vbox2.pack_start(frame)

        for sol in self.l_solutions[1:]:
            hsep = gtk.HSeparator()
            vbox2.pack_start(hsep, False, False)

            frame = self.build_button_frame(sol, self.button_group)
            vbox2.pack_start(frame)

        # button inhibitor
        button = self.wtree.get_widget("but_inhib")
        button.connect("clicked", self.on_inhib)
        button.set_sensitive(False)

        # button simul
        button = self.wtree.get_widget("but_simul")
        button.connect("clicked", self.on_simul)

        # button chrono
        button = self.wtree.get_widget("but_chrono")
        button.connect("clicked", self.on_chrono)

        # register
        parent.win_register(self)
        self.parent = parent

        # display
        self.window.show_all()
        #gtk.main()

    def on_destroy(self, widget):
        """
        when leaving the window
        """
        self.clean_subwin()
        if self.simul:
            self.simul.on_destroy(None)
        self.win_remove(self)

    def destroy(self):
        """
        when leaving the window
        """
        self.clean_subwin()
        if self.simul:
            self.simul.on_destroy(None)
        if self.window:
            self.window.destroy()

    def build_button_frame(self, state_list, group = None):
        """
        ???
        """
        template = pkg_resources.resource_filename(
            __name__,
            "../chart_glade/button_frame.glade"
        )
        wtree = gtk.glade.XML(template)
        wid = wtree.get_widget("button_frame")
        frame = wid.get_child()
        wid.remove(frame)

        #textview
        tname = 'tw'+str(self.compt)
        text = wtree.get_widget("textview")
        text.set_name(tname)

        text_buffer = text.get_buffer()
        str_state = '\n'
        for state in state_list :
            str_state += state + '\t'
        str_state += '\n'
        text_buffer.set_text(str_state)
        text.set_editable(False)

        self.textview_list.append(state_list)

        #radio button
        rname = 'rb' + str(self.compt)
        rbut = wtree.get_widget("rButton")
        rbut.set_name(rname)

        if group:
            rbut.set_group(group)
        else :
            self.button_group = rbut
            rbut.set_active(True)

        rbut.connect("toggled", self.rb_callback, self.compt)
        self.compt += 1
        return frame

    def rb_callback(self, widget, id_frame):
        """
        radio button call_back
        """
        self.choice = id_frame

    def on_save(self, widget, all_sol=True):
        """
        open a window to save as xml file
        @param all_sol : boolean - True if we take all solutions
        """
        choice = gtk.FileChooserDialog("Save solution", None ,
                                       gtk.FILE_CHOOSER_ACTION_SAVE,
                                       ( gtk.STOCK_CANCEL,
                                         gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_SAVE,
                                         gtk.RESPONSE_OK))
        choice.set_default_response(gtk.RESPONSE_OK)

        #add a filter to see only xml files for biochart (*.txt)
        ffilter = gtk.FileFilter()
        ffilter.set_name("txt files")
        ffilter.add_pattern("*.txt")
        choice.add_filter(ffilter)

        #add a filter to see all
        no_filter = gtk.FileFilter()
        no_filter.set_name("all")
        no_filter.add_pattern("*")
        choice.add_filter(no_filter)

        response = choice.run()
        if response == gtk.RESPONSE_OK:
            self.create_solution_file(choice.get_filename(), all_sol)
        elif response == gtk.RESPONSE_CANCEL:
            pass
            #print 'Closed, no files selected'
        choice.destroy()

    def create_solution_file(self, sol_file, all_bool):
        """
        make a xml file with the current model
        """
        if all_bool:
            init_places = self.l_solutions
            input_clocks = self.l_icseq
        else :
            init_places = [self.l_solutions[self.choice]]
            input_clocks = [self.l_icseq[self.choice]]

        sfile = open(sol_file,'w')
        for i in range(len(init_places)):
            spla = init_places[i]
            icseq = input_clocks[i]
            for elemt in spla :
                sfile.write(str(elemt)+'\t')
            for ica in icseq:
                sfile.write('\n' + ica)
            sfile.write('\n')
        sfile.close()

    def on_inhib(self, widget):
        """
        Compute inhibitors
        """
#
#        start_list = self.l_solutions[self.choice]
#        start_p = logical_and(start_list)
#        inv_p = 'not('+self.parent.property+')'
#        mac_list = self.parent.mcla.mac_search(start_p, inv_p, None,
#                                               self.parent.max_step)
#        inhib_list = []
#        for mac in mac_list:
#            im = []
#            for var in mac:
#                if var in start_list:
#                    continue
#                else:
#                    im.append(var)
#            if im:
#                inhib_list.append(im)
#        if len(inhib_list) == 0:
#            cancel_warn("This solution has not inhibitor")
#        else :
#            Inhib_Window(inhib_list, self.emvc, self.reporter, self)
        pass

    def on_simul(self, widget):
        """
        Launch simulation of a solution
        """
        if self.simul:
            self.simul.on_destroy(None)
        #init_places = self.choice
        init_places = self.l_solutions[self.choice]
        input_clocks = self.l_icseq[self.choice]
        self.simul = ChartSimulControler(self.emvc, True, self.reporter,
                                         init_places, input_clocks)

    def on_chrono(self, widget):
        """
        Show a chronogram of a trajectory initialized with solution
        """
        # stand alone simulator
        sim = ChartSimulator()
        sim.build(self.emvc.model, True, self.reporter)

        chrono = ChartChrono.for_trajectory(sim)
        self.win_register(chrono)

        # simulation
        init_places = self.l_solutions[self.choice]
        input_clocks = self.l_icseq[self.choice]
        sim.simul_init_places(init_places)
        # input buffer is any input
        if input_clocks:
            sim.set_act_input_stream(input_clocks)
        i = 0
        while i <= self.parent.max_step :
            chrono.register(sim)
            try:
                sim.simul_step()
                i += 1
            except Exception:
                break
        # clean model
        self.emvc.model.clean()
        self.emvc.model.notify()
        # display
        chrono.display_selected_chrono()

    # sub windows management
    def win_register(self, win):
        """
        sub windows management
        """
        if win.__class__ == ChartSimulControler:
            self.simul = win
        self.aux_win.append(win)

    def win_remove(self, win):
        """
        sub windows management
        """
        if win in self.aux_win:
            self.aux_win.remove(win)
        if win == self.simul:
            self.simul = None

    def clean_subwin(self):
        """
        sub windows management
        """
        for win in self.aux_win:
            win.destroy()
        self.aux_win = []


class CNSWindow(SolutionWindow):
    """
    ???
    """
    def __init__(self, l_solutions, emvc, reporter, parent):

        SolutionWindow.__init__(self, l_solutions, emvc, reporter, parent)

        # info label
        info = self.wtree.get_widget("label_nbsol")
        info.set_text(str(len(l_solutions))+" Minimal Activation Conditions")


class InhibWindow(SolutionWindow):
    """
    ???
    """
    def __init__(self, l_solutions, emvc, reporter, parent):

        SolutionWindow.__init__(self, l_solutions, emvc, reporter, parent)

        # info label
        info = self.wtree.get_widget("label_nbsol")
        info.set_text(str(len(l_solutions)) + " inhibitors")

        # button inhibitor
        button = self.wtree.get_widget("but_inhib")
        button.connect("clicked", self.on_inhib)
        button.set_sensitive(False)



def logical_and(list):
    """
    @return: logical_formula: str - AND of the input list
    """

    if len(list) == 0 :
        return
    elif len(list) == 1 :
        return list[0]
    else :
        logical_formula = ''
        for elemnt in list :
            logical_formula += elemnt + ' and '
        logical_formula = logical_formula[:-5]
#        print logical_formula
        return '('+logical_formula+')'


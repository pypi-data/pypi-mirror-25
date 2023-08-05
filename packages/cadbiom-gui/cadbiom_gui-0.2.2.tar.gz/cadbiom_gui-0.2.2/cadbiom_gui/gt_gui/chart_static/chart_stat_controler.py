## Filename    : chart_stat_controler.py
## Author(s)   : Michel Le Borgne
## Created     : 08/2012
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
## Contributor(s): Geoffroy Andrieux
##
"""
Collection of widgets and controlers for static analysis
"""
import gtk
from cadbiom.models.guard_transitions.analyser.static_analysis import StaticAnalyzer
from cadbiom_gui.gt_gui.utils.reporter import CompilReporter

import pkg_resources

import sys
sys.setrecursionlimit(10000)

class ChartStatControler(object):
    """
    Control of static analysis

    /!\ This class is fully deprecated and is no longer used /!\
    """
    def __init__(self, emvc, reporter):
        self.edit_mvc = emvc
        self.reporter = reporter                   # display error messages
        # graphical interface
        template = pkg_resources.resource_filename(
            __name__,
            "../chart_glade/static_analysis.glade"
        )
        self.wtree = gtk.glade.XML(template)
        self.main_window = self.wtree.get_widget("window1")
        title = "Static analysis - " + self.edit_mvc.model.name
        self.main_window.set_title(title)
        if (self.main_window):
            self.main_window.connect("destroy", self.on_destroy)
        self.main_window.set_position(gtk.WIN_POS_CENTER)
        #self.main_window.set_keep_above(True)
        self.main_window.resize(150, 300)

        # completion button
#        button = self.wtree.get_widget("completionbutton")
#        button.connect("clicked", self.on_completion)

        # frontier button
        button = self.wtree.get_widget("frontierbutton")
        button.connect("clicked", self.on_frontier)

        #  basal activated genes button
        button = self.wtree.get_widget("bgenebutton")
        button.connect("clicked", self.on_b_gene)

        # dependance graph button
        button = self.wtree.get_widget("depgraphbutton")
        button.connect("clicked", self.on_depgraph)

        # stat button
        button = self.wtree.get_widget("statbutton")
        button.connect("clicked", self.on_stat)

        # register as auxiliary window
        self.edit_mvc.win_register(self)
        self.subwin = []

        # display
        self.main_window.show_all()


#    def on_completion(self, widget):
#        """
#        TODO
#        """
#        pass

    def on_frontier(self, widget):
        """
        Compute connected components which are on the frontier
        """
        reporter = CompilReporter()
        stan = StaticAnalyzer(reporter)
        stan.build_from_chart_model(self.edit_mvc.model)
        # errors??
        lscc = stan.get_frontier_scc()
        display_w =  SCCWindow(lscc, self.edit_mvc, self.reporter, self)


    def on_b_gene(self, widget):
        """
        Compute basal activated genes
        """
        reporter = CompilReporter()
        stan = StaticAnalyzer(reporter)
        stan.build_from_chart_model(self.edit_mvc.model)
        lwbag = stan.get_why_basal_genes()
        display_w =  BAGWindow(lwbag, self.edit_mvc, self.reporter, self)

    def on_depgraph(self, widget):
        """
        Computation and export of the dependance graph
        """
        DependencyGraphWindow(self.edit_mvc, self.reporter, self)

    def on_stat(self, widget):
        """
        Fill window with model informations.
        """
        reporter = CompilReporter()
        # get stats from StaticAnalyzer
        stan = StaticAnalyzer(reporter)
        stan.build_from_chart_model(self.edit_mvc.model)
        ststat = stan.get_statistics()
        display_w = STATWindow(ststat, self.edit_mvc, self.reporter, self)

    def win_register(self, win):
        """
        register a sub wundow
        """
        print "register"
        self.subwin.append(win)

    def win_remove(self, win):
        """
        unregister a sub window
        """
        print "remove"
        self.subwin.remove(win)

    def clean_subwin(self):
        """
        sub windows management
        """
        for win in self.subwin:
            print "clean"
            win.destroy()
        self.subwin = []

    def on_destroy(self, widget):
        """
        Standard call back
        """
        print "on destroy"
        self.clean_subwin()
        if self.main_window:
            self.main_window.destroy()

    def destroy(self):
        """
        Standard call back
        """
        self.on_destroy(None)


class  DependencyGraphWindow(object):
    """
    Dialog for dependency graph analysis and export
    /!\ This class is fully deprecated and is no longer used /!\
    """
    def __init__(self, emvc, reporter, parent):
        self.emvc = emvc
        self.reporter = reporter
        self.parent = parent

        # window creation
        template = pkg_resources.resource_filename(
            __name__,
            "../chart_glade/dependency_graph.glade"
        )
        self.wtree = gtk.glade.XML(template)
        self.main_window = self.wtree.get_widget("window1")
        self.main_window.set_title("Dependency graph - "+self.emvc.model.name)

        self.main_window.set_resizable(True)
        screen_h = gtk.gdk.screen_height()
        screen_h = int(screen_h * 0.20)
        self.main_window.set_size_request(300, screen_h)

        if (self.main_window):
            self.main_window.connect("destroy", self.on_destroy)

        self.main_window.set_position(gtk.WIN_POS_CENTER)

        # transition graph radio button
        rbutton = self.wtree.get_widget("transGraph_rb")
        rb_name = rbutton.get_name()
        rbutton.connect("toggled", self.rb_callback, rb_name)

        # dependency graph radio button
        rbutton = self.wtree.get_widget("dpGraph_rb")
        rb_name = rbutton.get_name()
        rbutton.connect("toggled", self.rb_callback, rb_name)

        # full dependency graph radio button
        rbutton = self.wtree.get_widget("fullDpGraph_rb")
        rb_name = rbutton.get_name()
        rbutton.connect("toggled", self.rb_callback, rb_name)

        # DOT button
        button = self.wtree.get_widget("dotButton")
        button.connect("clicked", self.on_save_dot)

        # graphml button
        button = self.wtree.get_widget("graphmlButton")
        button.connect("clicked", self.on_save_graphml)

        # CREATE STATIC ANALYZER AND LOAD MODEL
        self.stan = StaticAnalyzer(reporter)
        self.stan.build_from_chart_model(self.emvc.model)

        self.graph_type = "transGraph_rb"

        # register as auxiliary window
        self.parent.win_register(self.main_window)

        # display
        self.main_window.show_all()

    def rb_callback(self, widget, name):
        """
        ???
        """
        self.graph_type = name

    def on_save_dot(self, widget):
        """
        compute a dependency graph and open a window to save as dot file
        """
        if self.graph_type == "transGraph_rb":
            graph = self.stan.make_transition_dg()
        elif self.graph_type == "dpGraph_rb":
            graph = self.stan.make_dependence_dg(True)
        else :
            graph = self.stan.make_full_dependence_dg(True)
        ch_opt = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE,
                   gtk.RESPONSE_OK)
        choice = gtk.FileChooserDialog("Save as dot file",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_SAVE, ch_opt)
        choice.set_default_response(gtk.RESPONSE_OK)

        #add a filter to see only dot files (*.dot)
        gfilter = gtk.FileFilter()
        gfilter.set_name("dot files")
        gfilter.add_pattern("*.dot")
        choice.add_filter(gfilter)

        #add a filter to see all
        no_filter = gtk.FileFilter()
        no_filter.set_name("all")
        no_filter.add_pattern("*")
        choice.add_filter(no_filter)

        response = choice.run()
        if response == gtk.RESPONSE_OK:
            self.stan.export_2_dot(graph, choice.get_filename())
        elif response == gtk.RESPONSE_CANCEL:
            pass
            #print 'Closed, no files selected'
        choice.destroy()

    def on_save_graphml(self, widget):
        """
        compute a dependency graph and open a window to save as graphml file
        """
        if self.graph_type == "transGraph_rb":
            graph = self.stan.make_transition_dg()
        elif self.graph_type == "dpGraph_rb":
            graph = self.stan.make_dependence_dg(True)
        else :
            graph = self.stan.make_full_dependence_dg(True)

        ch_opt = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE,
                   gtk.RESPONSE_OK)
        choice = gtk.FileChooserDialog("Save as graphml file", None,
                                       gtk.FILE_CHOOSER_ACTION_SAVE, ch_opt)
        choice.set_default_response(gtk.RESPONSE_OK)

        #add a filter to see only graphml files (*.graphml)
        filter = gtk.FileFilter()
        filter.set_name("graphml files")
        filter.add_pattern("*.graphml")
        choice.add_filter(filter)

        #add a filter to see all
        no_filter = gtk.FileFilter()
        no_filter.set_name("all")
        no_filter.add_pattern("*")
        choice.add_filter(no_filter)

        response = choice.run()
        if response == gtk.RESPONSE_OK:
            self.stan.export_2_graphml(graph, choice.get_filename())
        elif response == gtk.RESPONSE_CANCEL:
            pass
            #print 'Closed, no files selected'
        choice.destroy()

    def on_destroy(self, widget):
        """
        Standard call back
        """
        if self.main_window:
            self.parent.win_remove(self.main_window)
            self.main_window.destroy()

    def destroy(self):
        """
        For linked windows
        """
        self.on_destroy(None)



class SCCWindow(object):
    """
    Class used for displaying frontier isolated components
    """
    def __init__(self, l_fsol, emvc, reporter, parent):
        """
        @param l_fsol: list<list<string>>
        @param emvc: edit_mvc
        @param reporter: Classical reporter
        @param parent: parent widget
        """

        self.emvc = emvc
        self.reporter = reporter

        self.compt = 0
        self.choice = 0
        self.textview_list = []
        self.l_solutions = l_fsol
        self.aux_win = [] # for clean_subwin works properly

        # window creation
        template = pkg_resources.resource_filename(
            __name__,
            "../chart_glade/checker_solutions.glade"
        )
        self.wtree = gtk.glade.XML(template)
        self.window = self.wtree.get_widget("window1")

        self.window.set_resizable(True)
        self.window.set_title("Isolated Strongly Connected Components (SCC) - "\
                              + self.emvc.model.name)
        height = gtk.gdk.screen_height()
        height = int(height * 0.30)
        self.window.set_size_request(700, height)

        # Set window above all windows
        self.window.set_transient_for(parent.main_window)

        # Event on_escape key pressed
        self.window.connect('key_press_event', self.on_escape)

        # button save choice
        button = self.wtree.get_widget("but_sv_choice")
        button.connect("clicked", self.on_save, False)

        # button save all
        button = self.wtree.get_widget("but_sv_all")
        button.connect("clicked", self.on_save, True)
        if len(self.l_solutions) == 1:
            button.set_sensitive(False)

        # display
        self.display_info()

        # remove bottom buttons
        hbbox =  self.wtree.get_widget("hbuttonbox2")
        vbox = self.wtree.get_widget("vbox1")
        vbox.remove(hbbox)

        # register
        parent.win_register(self.window)
        self.parent = parent

        # display
        self.window.show_all()
        #gtk.main()

    def on_destroy(self, widget):
        """
        when leaving the window
        useless ? no sub window is created from this mother class and from
        subclasses...
        """
        self.clean_subwin()
        self.parent.win_remove(self)
        if self.window:
            self.window.destroy()

    def destroy(self):
        """
        when leaving the parent window
        """
        self.on_destroy(None)

    def on_escape(self, widget, event):
        """On ESC key_press_event, destroy this window."""
        if gtk.gdk.keyval_name(event.keyval) == "Escape":
            self.window.destroy()


    def display_info(self):
        """
        Display info on isolated SCC
        """
        SCC_found = (len(self.l_solutions[0]) != 0)

        # info label
        info = self.wtree.get_widget("label_nbsol")
        if not SCC_found:
            info.set_text("No isolated Strongly Connected Components found.")
            return
        else:
            info.set_text(str(len(self.l_solutions)) + \
                          " isolated Strongly Connected Components found.\n"
                          "(Only 1 node of each of them requires an input "
                          "transition with a StartNode)")

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


    def build_button_frame(self, state_list, group = None):
        """
        Display info on each isolated SCC
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
        str_state = str_state + '\n'
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
        Print solutions in a file
        """
        if all_bool:
            scc_places = self.l_solutions
        else :
            scc_places = [self.l_solutions[self.choice]]

        sfile = open(sol_file,'w')
        for i in range(len(scc_places)):
            spla = scc_places[i]
            for elemt in spla :
                sfile.write(str(elemt)+'\t')

            sfile.write('\n-------------------------------------------\n\n\n')
        sfile.close()

    # sub windows management
    def win_register(self, win):
        """
        sub windows management
        """
        print "register subsubwin"
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


class BAGWindow(SCCWindow):
    def __init__(self, l_fsol, emvc, reporter, parent):
        """
        @param l_fsol: list<list<string>>
        @param emvc: edit_mvc
        @param reporter: Classical reporter
        @param parent: parent widget
        """

        SCCWindow.__init__(self, l_fsol, emvc, reporter, parent)
        self.window.set_title("Basal activated genes - "+self.emvc.model.name)

    def display_info(self):
        """
        ???
        """

        SCC_found = (len(self.l_solutions[0]) != 0)

        # info label
        info = self.wtree.get_widget("label_nbsol")
        if not SCC_found:
            info.set_text("No basal activated genes found.")
            return
        else:
            info.set_text(str(len(self.l_solutions)) + \
                          " basal activated genes found.")

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


    def build_button_frame(self, pair, group = None):
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
        mess = '\nGene:'
        mess = mess + '\t' + pair[0]
        why = pair[1]
        mess = mess + "\n" + "Essential Inhib.: "
        for act in why[0]:
            mess = mess + "\t" + act
        mess = mess + "\n" + "Dominant Inhib.: "
        for act in why[1]:
            mess = mess + "\t" + act
        mess = mess + "\n" + "Essential Activ.: "
        for act in why[2]:
            mess = mess + "\t" + act
        mess = mess + "\n" + "Dominant Activ.: "
        for act in why[3]:
            mess = mess + "\t" + act
        mess = mess + '\n'
        text_buffer.set_text(mess)
        text.set_editable(False)

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


    def create_solution_file(self, sol_file, all_bool):
        """
        Print solutions in a file
        """
        if all_bool:
            scc_places = self.l_solutions
        else :
            scc_places = [self.l_solutions[self.choice]]

        sfile = open(sol_file,'w')
        for i in range(len(scc_places)):
            pair = scc_places[i]
            mess = '\nGene:'
            mess = mess + '\t' + pair[0]
            why = pair[1]
            mess = mess + "\n" + "Isolated Inhib.:"
            for act in why[0]:
                mess = mess + "\t" + act
            mess = mess + "\n" + "Dominant Inhib.:"
            for act in why[1]:
                mess = mess + "\t" + act
            mess = mess + "\n" + "Essential Activ.:"
            for act in why[2]:
                mess = mess + "\t" + act
            mess = mess + "\n" + "Dominant Activ.:"
            for act in why[3]:
                mess = mess + "\t" + act
            mess = mess + '\n'
            sfile.write(mess)
            sfile.write('\n-------------------------------------------\n\n\n')
        sfile.close()


class STATWindow(BAGWindow):
    """
    Class for displaying statistics
    """
    def __init__(self, stat, emvc, reporter, parent):
        """
        @param l_fsol: list<list<string>>
        @param emvc: edit_mvc
        @param reporter: Classical reporter
        @param parent: parent widget
        """
        BAGWindow.__init__(self, stat, emvc, reporter, parent)

        self.window.set_title("Statistics - "+self.emvc.model.name)
        button = self.wtree.get_widget("but_sv_choice")
        hbbox = self.wtree.get_widget("hbuttonbox1")
        hbbox.remove(button)

    def display_info(self):
        """
        ???
        """
        # info label
        info = self.wtree.get_widget("label_nbsol")
        info.set_text(
            "Model Informations\n"
            "(Please note that some elements may have more than one locations; "
            "take a look at /tmp/logs/cadbiom*)"
        )

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

        frame = self.build_button_frame(self.l_solutions)
        vbox2.pack_start(frame)

    def build_button_frame(self, stat_str, group = None):
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
        text = wtree.get_widget("textview")

        text_buffer = text.get_buffer()
        mess = str(stat_str) + '\n'
        text_buffer.set_text(mess)
        text.set_editable(False)

        #radio button removed
        rname = 'rb' + str(self.compt)
        rbut = wtree.get_widget("rButton")
        hbox = wtree.get_widget("hbox")
        hbox.remove(rbut)

        return frame


    def create_solution_file(self, sol_file, all_bool):
        """
        Print solutions in a file
        """
        sfile = open(sol_file,'w')
        mess = self.l_solutions
        mess = mess + '\n'
        sfile.write(mess)
        sfile.write('\n-------------------------------------------\n\n\n')
        sfile.close()

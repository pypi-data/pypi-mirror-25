##
## Filename    : chart_model.py
## Author(s)   : Michel Le Borgne
## Created     : 5/12/2011
## Revision    :
## Source      :
##
## Copyright 2009 - 2010  - 2011: IRISA/IRSET
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
##
"""
A drawing style contains all the information to display a chart model.
We use essentially two styles Navigator and Plain corresponding to
the two views displayed on the gui.
"""
from math import sqrt

from gtk.gdk import color_parse
import pango


class DrawingStyle:
    """"
    Generic class for chart model drawing
    """

    def __init__(self):
        pass

    def draw_start(self, node, xfv, yfv, wfv, hfv):
        """
        @param xfv: x coordinate of father in virtual view
        @param yfv: y coordinate of father in virtual view
        @param wfv: width of father in virtual view
        @param hfv: height of father in virtual view
        """
        pass

    def draw_trap(self, node, xfv, yfv, wfv, hfv):
        """
        @param xfv: x coordinate of father in virtual view
        @param yfv: y coordinate of father in virtual view
        @param wfv: width of father in virtual view
        @param hfv: height of father in virtual view
        """
        pass


    def draw_top_node(self, node, xfv, yfv, wfv, hfv):
        """
        @param xfv: x coordinate of father in virtual view
        @param yfv: y coordinate of father in virtual view
        @param wfv: width of father in virtual view
        @param hfv: height of father in virtual view
        """
        pass

    def draw_macro(self, node, xfv, yfv, wfv, hfv):
        """
        @param xfv: x coordinate of father in virtual view
        @param yfv: y coordinate of father in virtual view
        @param wfv: width of father in virtual view
        @param hfv: height of father in virtual view
        """
        pass

    def draw_simple(self, node, xfv, yfv, wfv, hfv):
        """
        @param xfv: x coordinate of father in virtual view
        @param yfv: y coordinate of father in virtual view
        @param wfv: width of father in virtual view
        @param hfv: height of father in virtual view
        """
        pass

    def draw_perm(self, node, xfv, yfv, wfv, hfv):
        """
        @param xfv: x coordinate of father in virtual view
        @param yfv: y coordinate of father in virtual view
        @param wfv: width of father in virtual view
        @param hfv: height of father in virtual view
        """
        pass

    def draw_input(self, node, xfv, yfv, wfv, hfv):
        """
        @param xfv: x coordinate of father in virtual view
        @param yfv: y coordinate of father in virtual view
        @param wfv: width of father in virtual view
        @param hfv: height of father in virtual view
        """
        pass

    def draw_transition(self, node, xfv, yfv, wfv, hfv):
        """
        @param xfv: x coordinate of father in virtual view
        @param yfv: y coordinate of father in virtual view
        @param wfv: width of father in virtual view
        @param hfv: height of father in virtual view
        """
        pass

    def draw_transition_group(self, tgr, xfv, yfv, wfv, hfv):
        """
        Draw transitions with common extremities
        @param tgr: is a list of transitions with same extremities
        @param xfv,yfv: view coordinates of the macro node
        @param wfv,hfv: affinity ratios father node -> virtual screen
        """
        pass



        # visitors give virtual size of the node and limits
    def visit_cstart_node(self, node):
        """
        @return: (v_width, v_height, 0.0)
        """
        return (0.0, 0.0, 0.0)

    def visit_ctrap_node(self, node):
        """
        @return: (v_width, v_height, 0.0)
        """
        return (0.0, 0.0, 0.0)

    def visit_cinput_node(self, node):
        """
        @return: (v_width, v_height, 0.0)
        """
        return (0.0, 0.0, 0.0)

    def visit_csimple_node(self, node):
        """
        @return: (v_width, v_height, v_h_top_limit)
        """
        return (0.0, 0.0, 0.0)

    def visit_cperm_node(self, node):
        """
        @return: (v_width, v_height, v_h_top_limit)
        """
        return (0.0, 0.0, 0.0)


    def visit_cmacro_node(self, node):
        """
        @return: (v_width, v_height, v_h_top_limit, handle_w_limit, handle_h_limit)
        """
        return (0.0, 0.0, 0.0, 0.0, 0.0)

    def visit_ctop_node(self, node):
        """
        @return:(0.0, 0.0, 0.0)
        """
        return (0.0, 0.0, 0.0)

    def visit_ctransition(self, node):
        """
        @return: (v_w_detect_limit, v_h_detect_limit
        """
        return (0.0, 0.0)


# main drawing style

class PlainDrawing(DrawingStyle):
    """
    Main drawing style used in main window of charter
    """
    LABEL_H = 22.0
    W_SNODE = 65.0
    H_SNODE = 20.0
    W_INODE = 60.0
    H_INODE = 30.0
    U_SLOPE = H_SNODE/W_SNODE
    NRADIUS = 4
    SNODE_COLOR = "#EDFFEE"
    MNODE_COLOR = "ivory"
    ENODE_COLOR = "#f9fff9"
    PNODE_COLOR = "#fff7ed"
    INODE_COLOR = "green"

    SELECT_COLOR = "red"
    ACTIV_COLOR = "#FF9F7C"
    SEARCH_COLOR = "#DA70D6"

    DELTA = 7.0  # for handler detection
    DIST = 6.0 # distance for transition detection in pixel

    def __init__(self):
        self.view = None
        pass

    def draw_simple(self, node, xfv, yfv, wfv, hfv):
        """
        @param xfv: x coordinate of father in virtual view
        @param yfv: y coordinate of father in virtual view
        @param wfv: width of father in virtual view
        @param hfv: height of father in virtual view
        """
        view = self.view
        wview = view.draw_width
        hview = view.draw_height
        # coordinates in view
        xxr = int((xfv + node.xloc*wfv) * wview)
        yyr = int((yfv + node.yloc*hfv) * hview)
        # must be included in macro
#        wr = min(self.W_SNODE, (xfv - xr+wfv))
#        her = min(self.H_SNODE, (yfv*hview - yr+hfv))
        wir = self.W_SNODE
        her = self.H_SNODE
        # find colors
        if node.selected:
            line_color = self.SELECT_COLOR
        else:
            line_color = 'black'

        if node.activated:
            node_color = self.ACTIV_COLOR
        elif node.search_mark:
            node_color = self.SEARCH_COLOR
        else:
            node_color = self.SNODE_COLOR

        self.draw_node_gen(view, xxr, yyr, wir, her,
                           node.name, node_color, line_color)


    def draw_macro(self, node, xfv, yfv, wfv, hfv):
        """
        @param xfv: x coordinate of father in virtual view
        @param yfv: y coordinate of father in virtual view
        @param wfv: width of father in virtual view
        @param hfv: height of father in virtual view
        """
        view = self.view
        wview = view.draw_width
        hview = view.draw_height
        # coordinates in drawing window
        xxr = int((xfv + node.xloc*wfv) * wview)
        yyr = int((yfv + node.yloc*hfv) * hview)
        if node.model.show_macro:
            wir = int(node.wloc * wfv * wview)
            her = int(node.hloc * hfv * hview)
        else:
#            wir = min(self.W_SNODE, xfv - xr+wfv)
#            her = min(self.H_SNODE, yfv-yr+hfv)
            wir = self.W_SNODE
            her = self.H_SNODE
        if node.selected:
            line_color = self.SELECT_COLOR
        else:
            line_color = 'black'

        if node.model.show_macro:
            name = node.name
        else:
            name = node.name[0:9]

        if node.model.show_macro:
            self.draw_macro_node_gen(view, xxr, yyr, wir, her,
                                     self.LABEL_H, name,
                                     self.MNODE_COLOR, line_color)
        else:
            self.draw_node_gen(view, xxr, yyr, wir, her, name,
                               self.MNODE_COLOR, line_color)


    def draw_start(self, node, xfv, yfv, wfv, hfv):
        view = self.view
        wview = view.draw_width
        hview = view.draw_height
        # coordinates
        xxr = int((xfv + node.xloc*wfv)*wview)
        yyr = int((yfv + node.yloc*hfv)*hview + self.H_SNODE/2)
        # graphic context
        pixmap = view.pixmap
        grc = view.window.new_gc()
        grc.set_rgb_fg_color(color_parse('black'))
        wid = int(xxr-self.NRADIUS)
        hei = int(yyr-self.NRADIUS)
        pixmap.draw_arc(grc, True, wid, hei,
                        2 * self.NRADIUS, 2 * self.NRADIUS, 0, 360*64)

    def draw_trap(self, node, xfv, yfv, wfv, hfv):
        view = self.view
        wview = view.draw_width
        hview = view.draw_height
        # coordinates
        xxr = int((xfv + node.xloc*wfv)*wview)
        yyr = int((yfv + node.yloc*hfv)*hview)
        # graphic context
        pixmap = view.pixmap
        grc = view.window.new_gc()
        grc.set_rgb_fg_color(color_parse('black'))
        grc.line_width = 2
        wid = int(xxr-self.NRADIUS)
        hei = int(yyr-self.NRADIUS)
        pixmap.draw_arc(grc, False, wid, hei,
                        2 * self.NRADIUS, 2 * self.NRADIUS, 0, 360*64)

    def draw_perm(self, node, xfv, yfv, wfv, hfv):
        """
        @param xfv: x coordinate of father in virtual view
        @param yfv: y coordinate of father in virtual view
        @param wfv: width of father in virtual view
        @param hfv: height of father in virtual view
        """

        view = self.view
        wview = view.draw_width
        hview = view.draw_height
        # coordinates in view
        xxr = int((xfv + node.xloc*wfv)*wview)
        yyr = int((yfv + node.yloc*hfv)*hview)

        # must be included in macro
#        wir = min(self.W_SNODE, xfv - xxr+wfv)
#        her = min(self.H_SNODE, yfv-yyr+hfv)
        wir = self.W_SNODE
        her = self.H_SNODE
        # find colors
        if node.selected:
            line_color = self.SELECT_COLOR
        else:
            line_color = 'black'

        if node.activated:
            node_color = self.ACTIV_COLOR
        elif node.search_mark:
            node_color = self.SEARCH_COLOR
        else:
            node_color = self.PNODE_COLOR

        self.draw_node_gen(view, xxr, yyr, wir, her,
                           node.name, node_color, line_color)


    def draw_input(self, node, xfv, yfv, wfv, hfv):
        view = self.view
        wview = view.draw_width
        hview = view.draw_height
        # coordinates
        xxr = int((xfv + node.xloc*wfv)*wview + self.W_SNODE/2)
        yyr = int((yfv + node.yloc*hfv)*hview + self.H_SNODE/2)
        # color choice (activated or not)
        if node.activated:
            color = self.ACTIV_COLOR
        else:
            color = self.INODE_COLOR
        # graphic context
        pixmap = view.pixmap
        grc = view.window.new_gc()

        # diamond drawing
        rax = int(self.W_INODE/2.0)
        ray = int(self.H_INODE/2.0)

        grc.set_rgb_fg_color(color_parse(color))
        xr1 = xxr - rax
        xr2 = xxr + rax
        yr1 = yyr - ray
        yr2 = yyr + ray
        lpe = [(xr1, yyr), (xxr, yr1), (xr2, yyr), (xxr, yr2)]
        pixmap.draw_polygon(grc, True, lpe)
        if node.selected:
            color = self.SELECT_COLOR
        else:
            color = 'black'
        grc.set_rgb_fg_color(color_parse(color))
        grc.line_width = 2
        pixmap.draw_polygon(grc, False, lpe)
        #name
        view.stylepango.set_text(node.name)
        (xps, yps) = view.stylepango.get_pixel_size()
        xxx = xxr - xps/2.0
        yyy = yyr - yps/2.0
        pixmap.draw_layout(grc, int(xxx), int(yyy), view.stylepango)


    def draw_transition(self, trans, x1v, y1v, x2v, y2v, nnn, hor, xfv, yfv):
        """
        @param trans: the transition
        @param x1v, y1v: origin coordinates in virtual screen
        @param x2v, y2v: extremity coordinates in virtual screen
        @param xfv, yfv: father coordinate in virtual screen
        """
        view = self.view
        wview = view.draw_width
        hview = view.draw_height
        # find colors
        if trans.selected:
            color = self.SELECT_COLOR
        elif trans.search_mark:
            color = self.SEARCH_COLOR
        elif trans.activated:
            color = self.ACTIV_COLOR
        else:
            color = 'black'
        label = trans.event + "["+trans.condition+"]"+ trans.action

        # coordinates in view
        xr1 = int((x1v)*wview)
        yr1 = int((y1v)*hview)
        if trans.ori.is_start():
            yr1 = yr1 + int(self.H_SNODE/2)
        if trans.ori.is_input():
            xr1 = xr1 + int(self.W_SNODE/2)
            yr1 = yr1 + int(self.H_SNODE/2)
        xr2 = int((x2v)*wview)
        yr2 = int((y2v)*hview)
        self.draw_edge_gen(view, xr1, yr1, xr2, yr2, hor, nnn, label, color)

    def draw_transition_group(self, tgr, xfv, yfv, wfv, hfv):
        """
        Draw transitions with common extremities
        @param tgr: is a list of transitions with same extremities
        @param xfv, yfv: view coordinates of the macro node
        @param wfv, hfv: affinity ratios father node -> virtual screen
        """
        trans = tgr[0]
        ori = trans.ori
        ext = trans.ext
        nbtrans = len(tgr)

        # extremities coordinates in local frame
        (xo1, yo1, gap1, hor1) = ori.intersect(ext, self, nbtrans, wfv, hfv)
        (xe2, ye2, gap2, hor2) = ext.intersect(ori, self, nbtrans, wfv, hfv)

        # change to virtual view coordinates
        x1v = xfv + xo1 * wfv
        y1v = yfv + yo1 * hfv
        if hor1:
            gap1v = gap1*wfv
        else:
            gap1v = gap1*hfv

        x2v = xfv + xe2 * wfv
        y2v = yfv + ye2 * hfv
        if hor2:
            gap2v = gap2*wfv
        else:
            gap2v = gap2*hfv

        # draw each transition
        cpt = 1
        for trans in tgr:
            if trans.ori == ori: # same direction as first one
                self.draw_transition(trans, x1v, y1v, x2v, y2v,
                                     cpt, hor1, xfv, yfv)
                # record positions in virtual screen for find -
                # position in local coordinate
                trans.ori_coord = (xo1, yo1)
                trans.ext_coord = (xe2, ye2)
            else:  # opposite direction
                self.draw_transition(trans, x2v, y2v, x1v, y1v,
                                     cpt, hor1, xfv, yfv)
                # record positions in virtual screen for find
                # position in local frame
                trans.ext_coord = (xo1, yo1)
                trans.ori_coord = (xe2, ye2)
            # next position
            if hor1:
                x1v = x1v + gap1v
                xo1 = xo1 + gap1
            else:
                y1v = y1v + gap1v
                yo1 = yo1 + gap1
            if hor2:
                x2v = x2v + gap2v
                xe2 = xe2 + gap2
            else:
                y2v = y2v + gap2v
                ye2 = ye2 + gap2
            cpt += 1


    # visitor method
    # visitors give virtual size of the node and limits
    def visit_cstart_node(self, node):
        wid = float(self.view.draw_width)
        hei = float(self.view.draw_height)
        return (self.NRADIUS/wid, self.NRADIUS/hei, self.H_SNODE/(2 * hei))

    def visit_ctrap_node(self, node):
        wid = float(self.view.draw_width)
        hei = float(self.view.draw_height)
        return (self.NRADIUS/wid, self.NRADIUS/hei, 0.0)

    def visit_cinput_node(self, node):
        wid = float(self.view.draw_width)
        hei = float(self.view.draw_height)
        hlabel  = self.LABEL_H/hei
        return (self.W_INODE/wid, self.H_INODE/hei, hlabel)

    def visit_csimple_node(self, node):
        wid = float(self.view.draw_width)
        hei = float(self.view.draw_height)
        return (self.W_SNODE/wid, self.H_SNODE/hei, self.LABEL_H/hei)

    def visit_cperm_node(self, node):
        wid = float(self.view.draw_width)
        hei = float(self.view.draw_height)
        return (self.W_SNODE/wid, self.H_SNODE/hei, self.LABEL_H/hei)


    def visit_cmacro_node(self, node):
        wid = float(self.view.draw_width)
        hei = float(self.view.draw_height)
        del_x = self.DELTA/wid
        del_y = self.DELTA/hei
        return (self.W_SNODE/wid, self.H_SNODE/hei, self.LABEL_H/hei,
                del_x, del_y)

    def visit_ctop_node(self, node):
        return (0.0, 0.0, 0.0)

    def visit_ctransition(self, node):
        wid = float(self.view.draw_width)
        hei = float(self.view.draw_height)
        return (self.DELTA/wid, self.DELTA/hei)


    # generic drawing
    def draw_macro_node_gen(self, view, xxr, yyr, wir, her, hlabel, name,
                            color, line_color):
        """
        Rectangle with round corners
        """
        # graphic context
        pixmap = view.pixmap
        grc = view.window.new_gc()
        cac = pixmap.cairo_create()

        # rounded rectangle
        #   A****BQ
        #  H      C
        #  *      *
        #  G      D
        #   F****E
        col = color_parse(line_color)
        cac.set_line_width(1.0)

        ray = 12
        # Move to A
        cac.move_to(xxr + ray, yyr)
        # Straight line to B
        cac.line_to(xxr + wir - ray, yyr)
        # Curve to C, Control points are both at Q
        cac.curve_to(xxr + wir, yyr , xxr + wir, yyr, xxr + wir, yyr + ray)
        # Move to D
        cac.line_to(xxr + wir, yyr + her - ray)
        # Curve to E
        cac.curve_to(xxr + wir, yyr + her, xxr + wir, yyr + her,
                    xxr + wir - ray, yyr + her)
        # Line to F
        cac.line_to(xxr + ray, yyr + her)
        # Curve to G
        cac.curve_to(xxr, yyr + her, xxr, yyr + her, xxr, yyr + her - ray)
        # Line to H
        cac.line_to(xxr, yyr+ray)
        # Curve to A
        cac.curve_to(xxr, yyr, xxr, yyr, xxr + ray, yyr)

    #    cac.move_to(xr, yyr+LABEL_H)
    #    cac.line_to(xr+wir, yyr+LABEL_H)
        cac.set_source_rgba(col.red / 65535.0, col.green / 65535.0,
                            col.blue / 65535.0)
        cac.stroke_preserve()
        col = color_parse(color)
        cac.set_source_rgba(col.red / 65535.0, col.green / 65535.0,
                            col.blue / 65535.0)
        cac.fill()
        grc.set_rgb_fg_color(color_parse(line_color))
        pixmap.draw_line(grc, int(xxr), int(yyr + self.LABEL_H),
                         int(xxr + wir), int(yyr + self.LABEL_H))
        # label
        view.stylepango.set_text(name)
        fod = pango.FontDescription("normal 9")
        view.stylepango.set_font_description(fod)
        (xpl, ypl) = view.stylepango.get_pixel_size()
        # center
        xpos = xxr + wir/2 - xpl/2
        ypos = yyr + 4
        pixmap.draw_layout(grc, int(xpos), int(ypos), view.stylepango)


    def draw_node_gen(self, view, xxr, yyr, wir, her, name, color, line_color):
        """
        @param xxr,yyr: coordinates in view
        @param wir, her: size in view
        """
        # graphic context
        pixmap = view.pixmap
        grc = view.window.new_gc()
        cac = pixmap.cairo_create()
        # rounded rectangle
        #   A****BQ
        #  H      C
        #  *      *
        #  G      D
        #   F****E
        col = color_parse(line_color)
        cac.set_line_width(1.5)

        ray = 7
        # Move to A
        cac.move_to(xxr + ray, yyr)
        # Straight line to B
        cac.line_to(xxr + wir - ray, yyr)
        # Curve to C, Control points are both at Q
        cac.curve_to(xxr + wir, yyr, xxr + wir, yyr, xxr + wir, yyr + ray)
        # Move to D
        cac.line_to(xxr + wir, yyr + her - ray)
        # Curve to E
        cac.curve_to(xxr + wir, yyr + her, xxr + wir, yyr + her,
                     xxr + wir - ray, yyr + her)
        # Line to F
        cac.line_to(xxr + ray, yyr + her)
        # Curve to G
        cac.curve_to(xxr, yyr + her, xxr, yyr + her, xxr, yyr + her - ray)
        # Line to H
        cac.line_to(xxr, yyr + ray)
        # Curve to A
        cac.curve_to(xxr, yyr, xxr, yyr, xxr + ray, yyr)
        cac.set_source_rgba(col.red / 65535.0, col.green / 65535.0,
                            col.blue / 65535.0)
        cac.stroke_preserve()
        col = color_parse(color)
        cac.set_source_rgba(col.red / 65535.0, col.green / 65535.0,
                            col.blue / 65535.0)
        cac.fill()

        # label
        view.stylepango.set_text(name[:9])
        fod  = pango.FontDescription("normal 9")
        view.stylepango.set_font_description(fod)
        (xpl, ypl)=view.stylepango.get_pixel_size()
        # center
        xpos = xxr + wir/2 - xpl/2
        ypos = yyr + 4
        pixmap.draw_layout(grc, int(xpos), int(ypos), view.stylepango)

    def draw_edge_gen(self, view, xr1, yr1, xr2, yr2, hor, nnn, label, color):
        """
        draw an edge
        """
        # graphic context
        pixmap = view.pixmap
        grc = view.window.new_gc()
        grc.set_rgb_fg_color(color_parse(color))
        # line
        pixmap.draw_line(grc, xr1, yr1, xr2, yr2)
        # arrow
        vux = xr2 - xr1
        vuy = yr2 - yr1
        norm = sqrt(vux ** 2 + vuy ** 2)
        if norm != 0:
            vux = vux / norm
            vuy = vuy / norm
            arr = Arrow()
            arr.draw(view, (vux, vuy),(xr2, yr2))
        # label
        if len(label)>20:
            label1 = label[0:18]+'...'
        else:
            label1 = label
        old_fd = view.stylepango.get_font_description()
        fod = pango.FontDescription("normal 9")
        view.stylepango.set_font_description(fod)
        view.stylepango.set_text(label1)
        (wpl, hpl) = view.stylepango.get_pixel_size()
        # draw label if enough room
        if wpl < abs(xr2 - xr1) or 2 * hpl < abs(yr2 - yr1):
            if not hor:
                xxl = (xr1 + xr2) / 2 - wpl / 2
                yyl = (yr1 + yr2) / 2 - hpl + 2
                pixmap.draw_layout(grc, xxl, yyl, view.stylepango)
            else:
                xxl = (nnn * xr1 + xr2) / (nnn + 1) - wpl / 2
                yyl = (nnn * yr1 + yr2) / (nnn + 1)
                pixmap.draw_layout(grc, xxl, yyl, view.stylepango)
        view.stylepango.set_font_description(old_fd)


class NavDrawing(DrawingStyle):
    """
    Drawing style for an overview
    """
    W_SNODE = 8.0
    H_SNODE = 6.0
    W_INODE = 6.0
    H_INODE = 3.0
    U_SLOPE = H_SNODE/W_SNODE
    NRADIUS = 3
    SNODE_COLOR = "#EDFFEE"
    MNODE_COLOR = "ivory"
    ENODE_COLOR = "#f9fff9"
    PNODE_COLOR = "#FFC1C1"          #"#ffabab"
    INODE_COLOR = "green"
    TNODE_COLOR = 'black'
    StNODE_COLOR = 'blue'

    SELECT_COLOR = "red"
    ACTIV_COLOR = "#FF9F7C"
    SEARCH_COLOR = "#CB1DC4"

    DELTA = 7.0  # for handler detection
    DIST = 6.0 # distance for transition detection in pixel
    def __init__(self):
        self.view = None
        pass


    def draw_top_node(self, node, xfv, yfv, wfv, hfv):
        pass

    def draw_macro(self, node, xfv, yfv, wfv, hfv):
        """
        @param xfv: x coordinate of father in virtual view
        @param yfv: y coordinate of father in virtual view
        @param wfv: width of father in virtual view
        @param hfv: height of father in virtual view
        """
        if not node.model.show_macro:
            self.draw_rectangle(node, xfv, yfv, wfv, hfv, True,
                                self.MNODE_COLOR)
            return
        view = self.view
        wview = view.draw_width
        hview = view.draw_height
        # coordinates
        xxr = int((xfv + node.xloc * wfv) * wview)
        yyr = int((yfv + node.yloc * hfv) * hview)
        # graphic context
        pixmap = view.pixmap
        grc = view.window.new_gc()
        grc.set_rgb_fg_color(color_parse(self.MNODE_COLOR))
        wid = int(node.wloc * wfv * wview)
        hei = int(node.hloc * hfv * hview)
        pixmap.draw_rectangle(grc, True, xxr, yyr, wid, hei)
        grc.set_rgb_fg_color(color_parse('black'))
        pixmap.draw_rectangle(grc, False, xxr, yyr, wid, hei)

    def draw_start(self, node, xfv, yfv, wfv, hfv):
        self.draw_circle(node, xfv, yfv, wfv, hfv, True, self.StNODE_COLOR)

    def draw_trap(self, node, xfv, yfv, wfv, hfv):
        self.draw_circle(node, xfv, yfv, wfv, hfv, True, self.TNODE_COLOR)

    def draw_simple(self, node, xfv, yfv, wfv, hfv):
        self.draw_rectangle(node, xfv, yfv, wfv, hfv, True, self.SNODE_COLOR)

    def draw_perm(self, node, xfv, yfv, wfv, hfv):
        self.draw_rectangle(node, xfv, yfv, wfv, hfv, True, self.PNODE_COLOR)

    def draw_input(self, node, xfv, yfv, wfv, hfv):
        self.draw_circle(node, xfv, yfv, wfv, hfv, True, self.INODE_COLOR)

    def draw_transition(self, node, xfv, yfv, wfv, hfv):
        pass

    def draw_transition_group(self, tgr, xfv, yfv, wfv, hfv):
        """
        Draw transitions with common extremities
        @param tgr: is a list of transitions with same extremities
        @param xfv,yfv: view coordinates of the macro node
        @param wfv,hfv: affinity ratios father node -> virtual screen
        """
        trans = tgr[0]
        ori = trans.ori
        ext = trans.ext

        # change to virtual view coordinates
        x1v = xfv + ori.xloc * wfv
        y1v = yfv + ori.yloc * hfv
        x2v = xfv + ext.xloc * wfv
        y2v = yfv + ext.yloc * hfv

        view = self.view
        v_size = ori.accept(self)
        if ori.is_macro():
            if ori.model.show_macro:
                xcr = v_size[0] * wfv * view.draw_width
                ycr = v_size[1] * hfv * view.draw_height
            else:
                xcr = (self.W_SNODE / 2.0) / view.draw_width
                ycr = (self.H_SNODE / 2.0) / view.draw_height
        else:
            xcr = v_size[0]
            ycr = v_size[1]
        x1r = int(x1v * view.draw_width + xcr)
        y1r = int(y1v * view.draw_height + ycr)

        v_size = ext.accept(self)
        if ext.is_macro():
            if ext.model.show_macro:
                xcr = v_size[0] * wfv * view.draw_width
                ycr = v_size[1] * hfv * view.draw_height
            else:
                xcr = (self.W_SNODE/2.0)/view.draw_width
                ycr = (self.H_SNODE/2.0)/view.draw_height
        else:
            xcr = v_size[0]
            ycr = v_size[1]
        x2r = int(x2v * view.draw_width + xcr)
        y2r = int(y2v * view.draw_height + ycr)
        pixmap = view.pixmap
        grc = view.window.new_gc()
        grc.set_rgb_fg_color(color_parse('black'))
        # line
        pixmap.draw_line(grc, x1r, y1r, x2r, y2r)


    def draw_circle(self, node, xfv, yfv, wfv, hfv, fill, color):
        """
        As it says
        """
        view = self.view
        wview = view.draw_width
        hview = view.draw_height
        # coordinates
        xxr = int((xfv + node.xloc * wfv) * wview)
        yyr = int((yfv + node.yloc * hfv) * hview)
        # graphic context
        pixmap = view.pixmap
        grc = view.window.new_gc()
        grc.set_rgb_fg_color(color_parse(color))
        wid = int(xxr - self.NRADIUS)
        hei = int(yyr - self.NRADIUS)
        pixmap.draw_arc(grc, True, wid, hei,
                        2 * self.NRADIUS, 2 * self.NRADIUS, 0, 360 * 64)
        grc.set_rgb_fg_color(color_parse('black'))
        pixmap.draw_arc(grc, False, wid, hei, 2 * self.NRADIUS,
                        2 * self.NRADIUS, 0, 360 * 64)

    def draw_rectangle(self, node, xfv, yfv, wfv, hfv, fill, color):
        """
        As it says
        """
        view = self.view
        wview = view.draw_width
        hview = view.draw_height
        # coordinates
        xxr = int((xfv + node.xloc*wfv)*wview)
        yyr = int((yfv + node.yloc*hfv)*hview)
        # color
        if node.activated:
            color = self.ACTIV_COLOR
        elif node.search_mark:
            color = self.SEARCH_COLOR
        # graphic context
        pixmap = view.pixmap
        grc = view.window.new_gc()
        grc.set_rgb_fg_color(color_parse(color))
        wid = int(self.W_SNODE)
        hei = int(self.H_SNODE)
        pixmap.draw_rectangle(grc, True, xxr, yyr, wid, hei)
        grc.set_rgb_fg_color(color_parse('black'))
        pixmap.draw_rectangle(grc, False, xxr, yyr, wid, hei)

    def visit_cstart_node(self, node):
        """
        @return: (v_width, v_height, 0.0)
        """
        return (self.NRADIUS/2, self.NRADIUS/2, 0.0)

    def visit_ctrap_node(self, node):
        """
        @return: (v_width, v_height, 0.0)
        """
        return (self.NRADIUS/2.0, self.NRADIUS/2.0, 0.0)

    def visit_cinput_node(self, node):
        """
        @return: (v_width, v_height, 0.0)
        """
        return (0.0, 0.0, 0.0)

    def visit_csimple_node(self, node):
        """
        @return: (v_width, v_height, v_h_top_limit)
        """
        return (self.W_SNODE/2, self.H_SNODE/2, 0.0)

    def visit_cperm_node(self, node):
        """
        @return: (v_width, v_height, v_h_top_limit)
        """
        return (self.W_SNODE/2, self.H_SNODE/2, 0.0)


    def visit_cmacro_node(self, node):
        """
        @return: (v_width, v_height, v_h_top_limit, handle_w_limit, handle_h_limit)
        """
        return (node.wloc/2.0, node.hloc/2.0, 0.0, 0.0, 0.0)

    def visit_ctop_node(self, node):
        """
        @return:(0.0, 0.0, 0.0)
        """
        return (0.0, 0.0, 0.0)

    def visit_ctransition(self, node):
        """
        @return: (v_w_detect_limit, v_h_detect_limit
        """
        return (0.0, 0.0)





# arrow
ALENGTH = 10
SAANGLE = 0.342020
CAANGLE = 0.939693
ARROWCOLOR = "black"


class Arrow:
    """
    Generic arrow
    """
    def __init__(self):
        pass

    def draw(self, view, direct, pos):
        """
        draw the arrow
        """
        pixmap = view.pixmap
        vux = - direct[0]
        vuy = - direct[1]
        poly = [(int(pos[0]), int(pos[1]))]
        xx0 = pos[0]
        yy0 = pos[1]
        u1x = vux * CAANGLE - vuy * SAANGLE
        u1y = vux * SAANGLE + vuy * CAANGLE
        xxx = int(xx0 + ALENGTH * 1.2 * u1x)
        yyy = int(yy0 + ALENGTH * 1.2 * u1y)
        poly.append((xxx, yyy))
        xxx = int(xx0 + ALENGTH * vux)
        yyy = int(yy0 + ALENGTH * vuy)
        poly.append((xxx, yyy))
        u1x = vux * CAANGLE + vuy * SAANGLE
        u1y = vuy * CAANGLE - vux * SAANGLE
        xxx = int(xx0 + ALENGTH * 1.2 * u1x)
        yyy = int(yy0 + ALENGTH * 1.2 * u1y)
        poly.append((xxx, yyy))
        grc = view.window.new_gc()
        grc.set_rgb_fg_color(color_parse(ARROWCOLOR))
        pixmap.draw_polygon(grc, True, poly)

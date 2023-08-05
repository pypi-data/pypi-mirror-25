# -*- coding: utf-8 -*-
# Copyright (C) 2010-2017  IRISA
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# The original code contained here was initially developed by:
#
#     Geoffroy Andrieux.
#     IRISA/IRSET
#     Symbiose team
#     IRISA  Campus de Beaulieu
#     35042 RENNES Cedex, FRANCE
#
#
# Contributor(s): Michel Le Borgne, Nolwenn Le Meur, Pierre Vignet
"""
Created on Nov 2016

..sectionauthor:: Pierre Vignet <pierre.vignet@irisa.fr>
"""

def main():

    """Launch Cadbiom gui"""
    import gtk
    from cadbiom_gui.gt_gui.charter import Charter

    charter = Charter(None)
    charter.show()
    gtk.main()

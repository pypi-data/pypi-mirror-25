#
# "$Id: counters.py 35 2003-09-29 21:39:48Z andreasheld $"
#
# Counters test program for pyFLTK the Python bindings
# for the Fast Light Tool Kit (FLTK).
#
# FLTK copyright 1998-1999 by Bill Spitzak and others.
# pyFLTK copyright 2003 by Andreas Held and others.
#
# This library is free software you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA.
#
# Please report all bugs and problems to "pyfltk-user@lists.sourceforge.net".
#

from fltk import *


# global object names
anAdjuster = None      # type 'Fl_Adjuster' from '()'
aCounter = None      # type 'Fl_Counter' from '()'
aSimpleCounter = None      # type 'Fl_Simple_Counter' from '()'


def adjusterChanged(dial):
    anAdjuster.value(dial.value())  # code
    aCounter.value(dial.value())  # code
    aSimpleCounter.value(dial.value())  # code


def main():
    global anAdjuster
    global aCounter
    global aSimpleCounter

    o_1_0 = Fl_Window(560, 330, 239, 225)
    o_1_0.pyChildren=[]

    anAdjuster = Fl_Adjuster(20, 15, 195, 25, "Adjuster")
    anAdjuster.pyChildren=[]
    anAdjuster.label('Adjuster')
    anAdjuster.callback(adjusterChanged)
    o_1_0.pyChildren.append(anAdjuster)

    aCounter = Fl_Counter(20, 155, 195, 25, "Counter")
    aCounter.precision(3)
    aCounter.pyChildren=[]
    aCounter.label('Counter')
    aCounter.callback(adjusterChanged)
    o_1_0.pyChildren.append(aCounter)

    aSimpleCounter = Fl_Simple_Counter(20, 85, 195, 25, "Simple Counter")
    aSimpleCounter.pyChildren=[]
    aSimpleCounter.label('Simple Counter')
    aSimpleCounter.callback(adjusterChanged)
    aSimpleCounter.selection_color(1)
    o_1_0.pyChildren.append(aSimpleCounter)
    o_1_0.color(215)
    o_1_0.end()

    return o_1_0



if __name__=='__main__':
    import sys
    window = main()
    window.show(len(sys.argv), sys.argv)
    Fl.run()

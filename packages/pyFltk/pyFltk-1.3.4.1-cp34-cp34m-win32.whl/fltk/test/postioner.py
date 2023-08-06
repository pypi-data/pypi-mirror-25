#
# "$Id: postioner.py 28 2003-07-16 20:00:27Z andreasheld $"
#
# Positioner test program for pyFLTK the Python bindings
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
theDisplay = None      # type 'Fl_Output' from '()'
thePos = None      # type 'Fl_Positioner' from '()'


def onOK(ptr):
    sys.exit(0)  # code


def thePosCallback(ptr):
    theDisplay.value("%3.3f, %3.3f"%(thePos.xvalue(), thePos.yvalue()))  # code


def main():
    global theDisplay
    global thePos

    o_1_0 = Fl_Window(461, 360, 221, 185)
    o_1_0.pyChildren=[]

    o_2_0 = Fl_Return_Button(80, 145, 65, 25, "OK")
    o_2_0.pyChildren=[]
    o_2_0.label('OK')
    o_2_0.callback(onOK)
    o_1_0.pyChildren.append(o_2_0)

    theDisplay = Fl_Output(60, 110, 100, 25)
    theDisplay.pyChildren=[]
    o_1_0.pyChildren.append(theDisplay)

    thePos = Fl_Positioner(10, 10, 200, 90)
    thePos.pyChildren=[]
    thePos.callback(thePosCallback)
    o_1_0.pyChildren.append(thePos)
    o_1_0.end()

    return o_1_0



if __name__=='__main__':
    import sys
    window = main()
    window.show(len(sys.argv), sys.argv)
    Fl.run()

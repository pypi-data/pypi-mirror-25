#
# "$Id: demos.py 493 2012-02-14 21:40:41Z andreasheld $"
#
# Test program for pyFLTK the Python bindings
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
demoList = []      # type 'Fl_Browser' from '()'


import os, glob

def onOK(ptr):
    import sys
    sys.exit(0)


def runDemo(ptr):
    if sys.version < "3.0":
        os.system("python "+demoList.text(demoList.value()))
    else:
        os.system("python3 "+demoList.text(demoList.value()))



def fillList():
    files = glob.glob("*.py")
    files.sort()
    for file in files:
    	if not file in ['fltk.py', 'fltk_pre.py', 'demos.py', 'browserData.py']:      		
    		demoList.add(file)


def main():
    global demoList

    o_1_0 = Fl_Window(451, 190, 192, 231)
    o_1_0.pyChildren=[]

    demoList = Fl_Select_Browser(5, 5, 180, 150, "Click to run a demo")
    demoList.pyChildren=[]
    demoList.label('Click to run a demo')
    demoList.callback(runDemo)
    fillList()   # extra code
    demoList.end()
    o_1_0.pyChildren.append(demoList)

    o_2_1 = Fl_Return_Button(115, 185, 50, 25, "OK")
    o_2_1.pyChildren=[]
    o_2_1.label('OK')
    o_2_1.callback(onOK)
    o_1_0.pyChildren.append(o_2_1)
    o_1_0.end()

    return o_1_0



if __name__=='__main__':
    import sys
    window = main()
    #window.show(len(sys.argv), sys.argv)
    #window.show()
    window.show(sys.argv)
    Fl.run()

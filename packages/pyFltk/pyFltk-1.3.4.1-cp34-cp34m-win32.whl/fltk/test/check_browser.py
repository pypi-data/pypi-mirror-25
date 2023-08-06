#
# "$Id: check_browser.py 495 2013-03-30 09:39:45Z andreasheld $"
#
# Check browser test program for pyFLTK the Python bindings
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
aCheckBrowser = None      # type 'Check_Browser' from '()'


def checkBrowserCallback(ptr):
    #cb = Fl_Check_BrowserPtr(ptr)  # code
    cb = ptr
    print("contains %d items"%cb.nitems())
    for i in range(1, cb.nitems()+1):  # code
    	if cb.checked(i):  # code
    		print(cb.text(i)+" is checked")
    	else:  # code
    		print(cb.text(i)+" is not checked")


def onOK(ptr):
    import sys  # code
    checkBrowserCallback(aCheckBrowser)  # code
    sys.exit(0)  # code


def main():
    global aCheckBrowser

    o_1_0 = Fl_Window(394, 309, 245, 133, "check_browser.py")
    o_1_0.pyChildren=[]

    aCheckBrowser = Fl_Check_Browser(5, 5, 240, 75)
    aCheckBrowser.pyChildren=[]
    aCheckBrowser.callback(checkBrowserCallback)
    aCheckBrowser.end()
    o_1_0.pyChildren.append(aCheckBrowser)

    o_2_1 = Fl_Return_Button(160, 90, 70, 30, "OK")
    o_2_1.pyChildren=[]
    o_2_1.label('OK')
    o_2_1.callback(onOK)
    o_1_0.pyChildren.append(o_2_1)
    o_1_0.label('check_browser.py')
    o_1_0.end()
    aCheckBrowser.add("Guiness", 1)  # code
    aCheckBrowser.add("Bud")  # code
    aCheckBrowser.add("Coors")  # code
    aCheckBrowser.add("Grimbergen", 1)  # code
    aCheckBrowser.add("Burning River", 1)  # code
    aCheckBrowser.add("Little Kings")  # code

    return o_1_0



if __name__=='__main__':
    import sys
    window = main()
    window.show(len(sys.argv), sys.argv)
    Fl.run()

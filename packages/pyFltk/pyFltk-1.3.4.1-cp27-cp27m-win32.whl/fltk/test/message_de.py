#
# "$Id: message.py 201 2006-02-16 07:26:03Z andreasheld $"
#
# Message test program for pyFLTK the Python bindings
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

fl_close_set("Schliessen")
fl_yes_set("Ja")
fl_no_set("Nein")
fl_cancel_set("Abbrechen")

fl_message("Spelling check sucessfull, %d errors found with %f confidence" \
	%(1002, 100*(15/77.0)))

fl_alert("Quantum fluctuations in the space-time continuim detected, "
	   "you have %f seconds to comply."% 10.0)

print("fl_ask returned %d"%fl_ask("Do you really want to %s?"%"continue"))

print("fl_choice returned %d"%fl_choice("Choose one of the following:","choice0","choice1","choice2"))

r = fl_input("Please enter a string for input:", "this is the default value")
print("fl_input returned \"%s\""%str(r))

r = fl_password("Enter password:", "123")
print("fl_password returned \"%s\""%str(r))


print("""
This is a quick hack to check setting and getting browser data 
""")

from fltk import *


# global object names
aBrowser = None	  # type 'Browser' from '()'


def onOK(ptr):
	import sys  # code
	#checkBrowserCallback(aBrowser.this)  # code
	sys.exit(0)  # code


def main():
	global aBrowser

	o_1_0 = Fl_Window(394, 309, 245, 133, "check_browser.py")
	o_1_0.pyChildren=[]
	o_1_0.thisown = 0

	aBrowser = Fl_Browser(5, 5, 240, 75)
	aBrowser.pyChildren=[]
	aBrowser.thisown = 0
	aBrowser.end()
	o_1_0.pyChildren.append(aBrowser)

	o_2_1 = Fl_Return_Button(160, 90, 70, 30, "OK")
	o_2_1.pyChildren=[]
	o_2_1.thisown = 0
	o_2_1.label('OK')
	o_2_1.callback(onOK)
	o_1_0.pyChildren.append(o_2_1)
	o_1_0.label('check_browser.py')
	o_1_0.end()
	aBrowser.add("Guiness", "line 1" )  # code
	aBrowser.add("Bud", "line 2")  # code
	aBrowser.add("Coors", "line 3")
	aBrowser.add("rocky mountain", "line 4")  # code
	aBrowser.add("Grimbergen", "line 5")  # code
	aBrowser.add("Burning River", "line 6")  # code
	aBrowser.add("Little Kings", "line 7")  # code

	return o_1_0



if __name__=='__main__':
	import sys
	window = main()
	window.show(len(sys.argv), sys.argv)
	print(aBrowser)
	d="data for 1"
	print("data(1,"+d+")")
	aBrowser.data(1, d)
	aBrowser.data(2, 123)
	print("data(1):", aBrowser.get_data(1))
	print("data(2):", aBrowser.get_data(2))
	print("data(3):", aBrowser.get_data(3))

	Fl.run()


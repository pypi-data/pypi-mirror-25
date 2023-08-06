from fltk import *
import time, string

window = None
fullscreen = 0
label = ""

def cb(ptr, data):
    print(data)

def full_cb(ptr):
    "toggle fullscreen"
    global fullscreen
    if fullscreen == 0:
        fullscreen = 1
        window.fullscreen()
    else:
        fullscreen = 0
        window.fullscreen_off(100,100,300,300)

def resize_cb(ptr, data):
    "grow/shrink the window"
    window.resize(window.x(), window.y(), window.w()+10*data,
    window.h()+10*data)

def iconize_cb(ptr):
    "iconize the window"
    window.iconize()

def hotspot_cb(ptr):
    "move the window to the hotspot"
    window.hotspot(10,10)

def label_cb(ptr):
    "change the label of the window, variable label must be global"
    global label
    label = "Another "+window.label()
    window.label(label)

window = Fl_Window(300,300)
window.label("Window Test")

window.size_range(100,100,500,500,10,10,1)

b1 = Fl_Button(10,10,80,25,"Fullscreen")
b1.callback(full_cb)

b2 = Fl_Button(100,10,80,25,"Grow")
b2.callback(resize_cb, 1)

b3 = Fl_Button(190,10,80,25,"Shrink")
b3.callback(resize_cb, -1)

b4 = Fl_Button(10,45,80,25,"Iconize")
b4.callback(iconize_cb)

b5 = Fl_Button(100,45,80,25,"Hotspot")
b5.callback(hotspot_cb)

b6 = Fl_Button(100,45,80,25,"Label")
b6.callback(label_cb)

window.show()

window.hotspot(100,100)

Fl.run()

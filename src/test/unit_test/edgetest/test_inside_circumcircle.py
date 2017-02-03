from Tkinter import *
from tkFileDialog import askopenfilename
import Image, ImageTk

import time
from threading import Thread

import tkMessageBox

import numpy
from numpy import matrix

import math

def scale(v, s):
    return [v[0]*s, v[1]*s]

def dot_prodcut(v1, v2):
    return v1[0]*v2[0]+v1[1]*v2[1]

def add(v1, v2):
    return [v1[0]+v2[0], v1[1]+v2[1]]

def subtract(v1, v2):
    return [v1[0]-v2[0], v1[1]-v2[1]]

def cross_product(v1, v2):
    return v1[0]*v2[1]-v1[1]*v2[0]

def get_angle(v1, v2):
    dot = dot_prodcut(v1, v2)
    det = cross_product(v1, v2)
    angle = math.atan2(det, dot)
    angle = int(angle*180/math.pi)
    angle = (angle+360)%360
    return angle

def get_radius_angle(v1, v2):
    dot = dot_prodcut(v1, v2)
    det = cross_product(v1, v2)
    angle = math.atan2(det, dot)
    angle = angle*180/math.pi
    return angle

def sort_into_anticlockwisse(a, b, c):
    o = add(add(a,b), c)
    o = [float(o[0])/3, float(o[1])/3]
    oa = subtract(a, o)
    ob = subtract(b, o)
    oc = subtract(c, o)

    a2b = get_radius_angle(oa, ob)
    a2c = get_radius_angle(oa, oc)

    print oa, ob, oc

    print a2b, a2c

    if a2b < 0:
        a2b += 360

    if a2c < 0:
        a2c += 360

    print oa, ob, oc

    print a2b, a2c

    print a,b,c

    if a2b > a2c:
        return [a, c, b]
    else:
        return [a, b, c]



def inside_circumcircle(a, b, c, d):
    a, b, c = sort_into_anticlockwisse(a, b, c)
    print a,b,c
    Ax = a[0]
    Ay = a[1]
    Bx = b[0]
    By = b[1]
    Cx = c[0]
    Cy = c[1]
    Dx = d[0]
    Dy = d[1]

    m = []
    m.append([Ax-Dx, Ay-Dy, Ax*Ax-Dx*Dx+Ay*Ay-Dy*Dy])
    m.append([Bx-Dx, By-Dy, Bx*Bx-Dx*Dx+By*By-Dy*Dy])
    m.append([Cx-Dx, Cy-Dy, Cx*Cx-Dx*Dx+Cy*Cy-Dy*Dy])

    m = matrix(m)
    print numpy.linalg.det(m)
    return numpy.linalg.det(m) >= 0


src_points = [[227, 333], [190, 382], [21, 620], [173, 321]]

def UI_run():
    root = Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    
    canvas_width = int(root.winfo_screenwidth())*0.9
    canvas_height = int(root.winfo_screenheight())*0.9
    canvas = Canvas(root, width = canvas_width, height=canvas_height)
    canvas.pack()    
    canvas.config(background='black')

    r = 5
    def printcoords(event):
        global src_points

        if len(src_points) == 4:
            return
        src_points.append([event.x, event.y])
    
        canvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill="red")

    canvas.bind("<Button 1>",printcoords)

    def test_inside_circumcircle():
        global src_points
        if len(src_points) != 4:
            return
        print inside_circumcircle(src_points[0], src_points[1], src_points[2], src_points[3])
        
        
    def clear_canvas():
        global src_points
        canvas.delete('all')
        src_points = []


    B_1 = Button(root, text ="inside_circumcircle", command = test_inside_circumcircle)
    B_1.pack()

    B_2 = Button(root, text ="clear_canvas", command = clear_canvas)
    B_2.pack()

    root.mainloop()

if __name__ == "__main__":
    UI_run()
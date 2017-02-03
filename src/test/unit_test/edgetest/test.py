from Tkinter import *
from tkFileDialog import askopenfilename
import Image, ImageTk

import time
from threading import Thread

import tkMessageBox

def dot_prodcut(v1, v2):
    return v1[0]*v2[0]+v1[1]*v2[1]

def add(v1, v2):
    return [v1[0]+v2[0], v1[1]+v2[1]]

def subtract(v1, v2):
    return [v1[0]-v2[0], v1[1]-v2[1]]

def cross_product(v1, v2):
    return v1[0]*v2[1]-v1[1]*v2[0]

def edge_intersect_test(p1, p2, p3, p4):
    p = p1
    r = subtract(p2, p1)

    q = p3
    s = subtract(p4, p3)

    rs = cross_product(r, s)
    qp = subtract(q, p)
    qpr = cross_product(qp, r)

    if rs == 0:
        if qpr == 0:
            rr = dot_prodcut(r, r)
            t0 = float(dot_prodcut(qp, r))/rr
            t1 = t0+float(dot_prodcut(s,r))/rr

            interval = [min(t0, t1), max(t0, t1)]
            if interval[0] <= 0:
                if  interval[1] >= 0:
                    return True
                else:
                    return False
            elif interval[0] <= 1:
                return True
            else:
                return False
        else:
            return False
    else:
        t = float(cross_product(qp, s))/rs
        u = float(cross_product(qp, r))/rs
        if t <= 1 and t >= 0 and u <= 1 and u >= 0:
            return True
        else:
            return False


turn = 0
src_points = []
dst_points = []

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
        global turn, src_points, dst_points

        if turn == 0:
            if len(src_points) == 2:
                return
            src_points.append([event.x, event.y])
            turn = 1
        elif turn == 1:
            if len(dst_points) == 2:
                return
            dst_points.append([event.x, event.y])
            turn = 0
            canvas.create_line(event.x, event.y, src_points[-1][0], src_points[-1][1], fill="red")

        canvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill="red")

    canvas.bind("<Button 1>",printcoords)

    def check_intersect():
        global turn, src_points, dst_points
        print edge_intersect_test(src_points[0], dst_points[0], src_points[1], dst_points[1])

        
        
    def clear_canvas():
        global turn, src_points, dst_points
        canvas.delete('all')
        turn = 0
        src_points = []
        dst_points = []

    B_1 = Button(root, text ="check_intersect", command = check_intersect)
    B_1.pack()

    B_2 = Button(root, text ="clear_canvas", command = clear_canvas)
    B_2.pack()

    root.mainloop()

if __name__ == "__main__":
    UI_run()
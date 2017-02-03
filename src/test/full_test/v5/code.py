from Tkinter import *
from tkFileDialog import askopenfilename
import Image, ImageTk

import time
from threading import Thread

import tkMessageBox

import math

import numpy
from numpy import matrix

from image_morphing_v2 import morph_baby
from Delaunay_triangulation import same_point_test


src_img_file_name = "src.jpg"
dst_img_file_name = "dst.jpg"


src_points = []
dst_points = []

src_event_points = []
dst_event_points = []

turn = 0


def color_point(canvas, p, color):
    r = 5
    canvas.create_oval(p[0]-r, p[1]-r, p[0]+r, p[1]+r, fill=color)
    #raw_input()

def color_edge(canvas, e, color):
    canvas.create_line(e[0][0], e[0][1], e[1][0], e[1][1], fill=color)
    #raw_input()


def draw_trianlge(canvas, t, color):
    p1 = t[0]
    p2 = t[1]
    p3 = t[2]

    center = add(add(p1, p2), p3)
    center = [center[0]/3, center[1]/3]

    color_point(canvas, center, color)

    color_edge(canvas, [p1, p2], color)
    color_edge(canvas, [p2, p3], color)
    color_edge(canvas, [p1, p3], color)

def purge_duplicate_points(point_set):
    to_return = []

    for raw_p in point_set:
        flag = True
        for p in to_return:
            if same_point_test(raw_p, p):
                flag = False
                break
        if flag:
            to_return.append(raw_p)

    return to_return



def UI_run():
    root = Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    
    canvas_width = int(root.winfo_screenwidth())*0.9
    canvas_height = int(root.winfo_screenheight())*0.9


    split = 2
    max_img_width = canvas_width/split
    max_img_height = canvas_height
    
    canvas = Canvas(root, width = canvas_width, height=canvas_height)
    canvas.pack()    

    src_img = Image.open(src_img_file_name)
    src_img_height = src_img.size[1]
    src_img_width = src_img.size[0]
    scale_w = float(src_img_width)/max_img_width
    scale_h = float(src_img_height)/max_img_height
    src_scale_factor = max(scale_w, scale_h)
    

    src_new_height = int(src_img_height/src_scale_factor)
    src_new_width = int(src_img_width/src_scale_factor)
    src_img = src_img.resize((src_new_width, src_new_height), Image.ANTIALIAS)
    src_img = ImageTk.PhotoImage(src_img)

    canvas.create_image(canvas_width/(2*split) , canvas_height/2, image=src_img)
  
    

    dst_img = Image.open(dst_img_file_name)
    dst_img_height = dst_img.size[1]
    dst_img_width = dst_img.size[0]
    scale_w = float(dst_img_width)/max_img_width
    scale_h = float(dst_img_height)/max_img_height
    dst_scale_factor = max(scale_w, scale_h)

    
    dst_new_height = int(dst_img_height/dst_scale_factor)
    dst_new_width = int(dst_img_width/dst_scale_factor)
    dst_img = dst_img.resize((dst_new_width, dst_new_height), Image.ANTIALIAS)
    dst_img = ImageTk.PhotoImage(dst_img)
    canvas.config(background='black')

    canvas.create_image(canvas_width*3/(2*split) , canvas_height/2,image=dst_img)
    

    r = 5
    
    def printcoords(event):

        global turn, src_event_points, dst_event_points, src_points, dst_points
        if event.x < canvas_width/split:
            offset_x = 0+(canvas_width/split - src_new_width)/2
            offset_y = (canvas_height - src_new_height)/2
            scale_factor = src_scale_factor

            x = int((event.x - offset_x)*scale_factor)
            y = int((event.y - offset_y)*scale_factor)

            if turn == 0:
                turn = 1
                src_points.append([x,y])
                src_event_points.append([event.x, event.y])
                canvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill="red")

        elif event.x < canvas_width*2/split: 
            offset_x = canvas_width/split + (canvas_width/split - dst_new_width)/2
            offset_y = (canvas_height - dst_new_height)/2
            scale_factor = dst_scale_factor

            x = int((event.x - offset_x)*scale_factor)
            y = int((event.y - offset_y)*scale_factor)

            if turn == 1:
                turn = 0
                dst_points.append([x,y])
                dst_event_points.append([event.x, event.y])
                canvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill="red")

                print src_event_points[-1][0], src_event_points[-1][1]


                canvas.create_line(src_event_points[-1][0], src_event_points[-1][1], event.x, event.y, fill="red")


        elif event.x < canvas_width*3/split:
            offset_x = 0
            offset_y = 0
            scale_factor = 1


    canvas.bind("<Button 1>",printcoords)



    def helloCallBack():
        tkMessageBox.showinfo( "Hello Python", "Hello World")

    def run_triangulation():
        '''
        global src_points, dst_points, turn

        if turn == 1:
            return

        if len(src_points) == 0:
            return


        #add 4 corners
        src_points.append([0, 0])
        src_points.append([0, src_img_height-1])
        src_points.append([src_img_width-1, src_img_height-1])
        src_points.append([src_img_width-1, 0])

        dst_points.append([0, 0])
        dst_points.append([0, dst_img_height-1])
        dst_points.append([dst_img_width-1, dst_img_height-1])
        dst_points.append([dst_img_width-1, 0])

        
        print '*'*20
        print src_points
        src_points = purge_duplicate_points(src_points)
        print src_points        
        
        print '*'*20
        print dst_points
        dst_points = purge_duplicate_points(dst_points)
        print dst_points

        '''

        src_points = [[303, 445], [436, 447], [350, 531], [384, 527], [328, 583], [378, 582], [426, 580], [368, 487], [365, 457], [368, 279], [236, 487], [523, 467], [378, 673], [267, 599], [494, 601], [264, 347], [485, 334], [369, 347], [368, 407], [298, 407], [435, 395], [469, 530], [291, 540], [313, 654], [469, 645], [251, 546], [516, 537], [243, 398], [515, 390], [448, 300], [297, 309], [617, 673], [728, 703], [749, 787], [759, 903], [273, 682], [199, 712], [156, 774], [122, 865], [103, 982], [415, 865], [279, 805], [523, 779], [566, 950], [249, 946], [0, 0], [0, 1023], [767, 1023], [767, 0]]


        dst_points = [[266, 142], [322, 137], [284, 185], [307, 185], [281, 211], [299, 211], [317, 206], [294, 167], [296, 153], [292, 56], [237, 146], [369, 137], [301, 240], [260, 206], [350, 200], [234, 83], [353, 78], [292, 86], [293, 125], [253, 129], [329, 122], [335, 174], [266, 180], [277, 225], [333, 225], [247, 176], [358, 178], [230, 113], [363, 101], [326, 58], [256, 62], [413, 229], [475, 256], [506, 300], [520, 348], [240, 249], [204, 274], [180, 305], [174, 336], [175, 375], [321, 327], [257, 293], [389, 280], [396, 355], [244, 355], [0, 0], [0, 412], [619, 412], [619, 0]]
 

        src_points_to_pass = [i[:] for i in src_points]
        dst_points_to_pass = [i[:] for i in dst_points]

        src_img = Image.open('src.jpg')
        dst_img = Image.open('dst.jpg')
        
        
        morph_baby(src_img, dst_img, src_points_to_pass, dst_points_to_pass, 0.2)




    def clean_canvas():
        global src_points, dst_points, src_event_points, dst_event_points, turn
        src_points = []
        dst_points = []

        src_event_points = []
        dst_event_points = []

        turn = 0

        canvas.delete('all')
        canvas.create_image(canvas_width/(2*split) , canvas_height/2, image=src_img)
        canvas.create_image(canvas_width*3/(2*split) , canvas_height/2,image=dst_img)
    




    B_1 = Button(root, text ="run_triangulation", command = run_triangulation)
    B_1.pack()

    B_2 = Button(root, text ="clean_canvas", command = clean_canvas)
    B_2.pack()

    root.mainloop()


if __name__ == '__main__':
    UI_run()

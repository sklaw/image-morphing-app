from Tkinter import *
from tkFileDialog import askopenfilename
import Image, ImageTk

import time
from threading import Thread

import tkMessageBox

import math

import numpy
from numpy import matrix

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

def edge_intersect_test(e1, e2):
    p1 = e1[0]
    p2 = e1[1]
    p3 = e2[0]
    p4 = e2[1]
    p = p1
    r = subtract(p2, p1)

    if same_point_test(r, [0, 0]):
        return False

    q = p3
    s = subtract(p4, p3)

    if same_point_test(s, [0, 0]):
        return False

    rs = cross_product(r, s)
    qp = subtract(q, p)
    qpr = cross_product(qp, r)

    if rs == 0:
        if qpr == 0:
            rr = dot_prodcut(r, r)


            t0 = float(dot_prodcut(qp, r))/rr
            t1 = t0+float(dot_prodcut(s,r))/rr

            interval = [min(t0, t1), max(t0, t1)]
            if interval[0] < 0:
                if  interval[1] > 0:
                    return True
                else:
                    return False
            elif interval[0] < 1:
                return True
            else:
                return False
        else:
            return False
    else:
        t = float(cross_product(qp, s))/rs
        u = float(cross_product(qp, r))/rs
        if t < 1 and t > 0 and u < 1 and u > 0:
            return True
        else:
            return False

def show_progress(edges):
    global canvas
    for e in edges:
        a = e[0]
        b = e[1]
        canvas.create_line(a[0], a[1], b[0], b[1], fill="red")
    raw_input()



def get_angle(v1, v2):
    dot = dot_prodcut(v1, v2)
    det = cross_product(v1, v2)
    angle = math.atan2(det, dot)
    angle = angle*180/math.pi

    if angle < 0:
        angle += 360
    if angle >= 360:
        angle -= 360

    return angle

def sort_into_anticlockwisse(a, b, c):
    o = add(add(a,b), c)
    o = [float(o[0])/3, float(o[1])/3]
    oa = subtract(a, o)
    ob = subtract(b, o)
    oc = subtract(c, o)

    a2b = get_angle(oa, ob)
    a2c = get_angle(oa, oc)



    if a2b > a2c:
        return [a, c, b]
    else:
        return [a, b, c]

def get_sorted_candidates(a, b, point_set, merged_edges):
    to_return = []
    v1 = subtract(b, a)
    for p in point_set:
        if same_point_test(a, p):
            continue
        
        edge = [a, p]
        found = False
        for tmp_edge in merged_edges:
            if smae_edge_test(tmp_edge, edge):
                found = True
                break

        if not found:
            continue

        v2 = subtract(p, a)




        angle = get_angle(v1, v2)


        to_return.append([p, angle])

    to_return = sorted(to_return, key=lambda x:x[1])
    return to_return    






def inside_circumcircle(a, b, c, d):
    a, b, c = sort_into_anticlockwisse(a, b, c)
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

    return numpy.linalg.det(m) > 0




def same_point_test(p1, p2):
    return p1[0] == p2[0] and p1[1] == p2[1]

def smae_edge_test(e1, e2):
    if same_point_test(e1[0], e2[0]):
        return same_point_test(e1[1], e2[1])
    elif same_point_test(e1[0], e2[1]):
        return same_point_test(e1[1], e2[0])

    return False

def color_edge(e, color):
    global canvas
    canvas.create_line(e[0][0], e[0][1], e[1][0], e[1][1], fill=color)
    raw_input()
    
def color_point(p, color):
    global canvas
    r = 5
    canvas.create_oval(p[0]-r, p[1]-r, p[0]+r, p[1]+r, fill=color)
    raw_input()


def Delaunay_recursive_actor(point_set):
    if len(point_set) == 2:
        edges = [[point_set[0], point_set[1]]]
        show_progress(edges) 
        return edges

    if len(point_set) == 3:
        edges = [[point_set[0], point_set[1]], [point_set[0], point_set[2]], [point_set[1], point_set[2]]] 
        show_progress(edges)
        return edges

    left_point_set = point_set[:len(point_set)/2]
    right_point_set = point_set[len(point_set)/2:]

    

    left_edges = Delaunay_recursive_actor(left_point_set)
    right_edges = Delaunay_recursive_actor(right_point_set)



    #try to fine bottommost LR edge
    y_sorted_left_points = sorted(left_point_set, key=lambda x:x[1])
    y_sorted_right_points = sorted(right_point_set, key=lambda x:x[1])

    left_idx = right_idx = 0
    lr_edge = None

    print "now we'll try to find bottommost edge."

    while True:
        possible_lr_edge = [y_sorted_left_points[left_idx], y_sorted_right_points[right_idx]]
        
        print "got one possible_lr_edge."
        color_edge(possible_lr_edge, 'green')

        flag = True
        for ll_edge in left_edges:
            print "checking intersection against a ll edge."
            color_edge(ll_edge, 'white')
            color_edge(ll_edge, 'red')


            if edge_intersect_test(ll_edge, possible_lr_edge):
                print "intersection found. we'll stop this checking."
                color_edge(possible_lr_edge, 'black')
                flag = False
                break

        if flag:
            print "ll_edge checking says good. now we'll try rr_edge check."
            for rr_edge in right_edges:
                print "checking intersection against a rr edge."
                color_edge(rr_edge, 'white')
                color_edge(rr_edge, 'red')
                if edge_intersect_test(rr_edge, possible_lr_edge):
                    print "intersection found. we'll stop this checking."
                    color_edge(possible_lr_edge, 'black')
                    flag = False
                    break



        if flag:
            print "rr_edge checking says good, this will be our bottommost edge."
            lr_edge = possible_lr_edge
            break

        print 'we look to bottom X possible_lr_edge now.'

        idx_to_try = []

        left_next_idx = left_idx+1
        right_next_idx = right_idx+1

        if left_next_idx > len(y_sorted_left_points):
            left_next_dist = -1
        else:
            left_next_dist = y_sorted_left_points[left_next_idx][1]-y_sorted_left_points[left_idx][1]

        if right_next_idx > len(y_sorted_right_points):
            right_next_dist = -1
        else:
            right_next_dist = y_sorted_right_points[right_next_idx][1]-y_sorted_right_points[right_idx][1]

        if left_next_dist == -1:
            if right_next_dist == -1:
                pass
            else:
                idx_to_try.append([left_idx, right_idx+1])
        elif right_next_dist == -1:
            idx_to_try.append([left_idx+1, right_idx])
        elif left_next_dist <= right_next_dist:
            idx_to_try.append([left_idx+1, right_idx])
            idx_to_try.append([left_idx, right_idx+1])
        else:
            idx_to_try.append([left_idx, right_idx+1])
            idx_to_try.append([left_idx+1, right_idx])


        edge_to_try = [[y_sorted_left_points[i[0]], y_sorted_right_points[i[1]]] for i in idx_to_try]

        flag = True
        for idx in range(len(edge_to_try)):
            possible_lr_edge = edge_to_try[idx]
            print "got one possible_lr_edge."
            color_edge(possible_lr_edge, 'green')

            for ll_edge in left_edges:
                print "checking intersection against a ll edge."
                color_edge(ll_edge, 'white')
                color_edge(ll_edge, 'red')
                if edge_intersect_test(ll_edge, possible_lr_edge):
                    print "intersection found. we'll stop this checking."
                    color_edge(possible_lr_edge, 'black')
                    flag = False
                    break
                
            if flag:
                for rr_edge in right_edges:
                    print "checking intersection against a rr edge."
                    color_edge(rr_edge, 'white')
                    color_edge(rr_edge, 'red')
                    if edge_intersect_test(rr_edge, possible_lr_edge):
                        print "intersection found. we'll stop this checking."
                        color_edge(possible_lr_edge, 'black')
                        flag = False
                        break
                
            if flag:
                print "checking says good, this will be our bottommost edge."
                color_edge(possible_lr_edge, 'red')
                lr_edge = possible_lr_edge
                left_idx = idx_to_try[idx][0]
                right_idx = idx_to_try[idx][1]
                lr_edge = possible_lr_edge
                break



        if flag:
            print 'bottommost edge found. we will call this off.'
            break
        else:
            print 'bottommost edge NOT found. we will step bottom up 1 unit.'
            left_idx += 1
            right_idx += 1
            if left_idx >= len(y_sorted_left_points) or right_idx >= len(y_sorted_right_points):
                print 'steping failed. we cannot find bottommost edge.'
                break

    print '-'*10

    merged_edges = left_edges+right_edges 

    if lr_edge == None:
        print 'fuck. bottom lr not found.'
        return merged_edges

    merged_edges.append(lr_edge)
    show_progress(merged_edges)

    print "good. we got our bottommost edge yet. now, let try to merge them further."

    print 'now, we try to find next lr_edge'
    while lr_edge != None:
        print 'the current lr_edge is in green'
        color_edge(lr_edge, 'green')

        #try to fine more LR edges
        lr_right_point = lr_edge[1]
        lr_left_point = lr_edge[0]

        print "lr_left_point"        
        color_point(lr_left_point, "yellow")
        print 'lr_right_point'
        color_point(lr_right_point, "blue")

        color_point(lr_left_point, "red")
        color_point(lr_right_point, "red")


        sorted_right_point_set_with_angles = get_sorted_candidates(lr_right_point, lr_left_point, right_point_set, merged_edges)
        sorted_right_point_set_with_angles = sorted_right_point_set_with_angles[::-1]
        sorted_left_point_set_with_angles = get_sorted_candidates(lr_left_point, lr_right_point, left_point_set, merged_edges)
        
        print "let's try to find a right_side_candidate"
        #start from the right side
        right_side_candidate = None
        for p_a_idx in range(len(sorted_right_point_set_with_angles)):
            p_a = sorted_right_point_set_with_angles[p_a_idx]
            p = p_a[0]

            angle = p_a[1]
            
            print "the point we are seeing is in white."
            print "angle in degrees: ", angle
            color_point(p, "white")
            
            if angle <= 180:
                print "it is less than 180 degrees when look upward. we will ignore it"
                color_point(p, "red")
                break

            if p_a_idx+1 >= len(sorted_right_point_set_with_angles):
                print 'this is the last one. we will pick it'
                color_point(p, "red")
                right_side_candidate = p
                break

            next_p_a = sorted_right_point_set_with_angles[p_a_idx+1]
            next_p = next_p_a[0]


            print "the next point we will see is in yellow."
            color_point(next_p, "yellow")
            

            if not inside_circumcircle(lr_left_point, lr_right_point, p, next_p):
                print 'next_p is not an interior of current p. current p is good. we will pick it'
                color_point(p, 'red')
                color_point(next_p, 'red')
                right_side_candidate = p
                break
            else:
                print 'next_p IS an interior of current p. current p is NOT good. we won\'t pick it. and we gonna delete the line between p and lr_right_point'
                color_point(p, 'red')
                color_point(next_p, 'red')
                

                target_edge = [lr_right_point, p]
                to_delete_idx = None
                for rr_idx in range(len(merged_edges)):
                    rr_edge = merged_edges[rr_idx]
                    if smae_edge_test(target_edge, rr_edge):
                        to_delete_idx = rr_idx
                        break
                if to_delete_idx != None:
                    color_edge(merged_edges[to_delete_idx], 'black')
                    del merged_edges[to_delete_idx]



        print "let's try to find a left_side_candidate"
        #then the left side
        left_side_candidate = None
        for p_a_idx in range(len(sorted_left_point_set_with_angles)):
            p_a = sorted_left_point_set_with_angles[p_a_idx]
            p = p_a[0]
            angle = p_a[1]
            
            print "the point we are seeing is in white."
            print "angle in degrees: ", angle
            color_point(p, "white")

            if angle >= 180 or angle == 0:
                print "it is less than 180 degrees when look upward. we will ignore it"
                color_point(p, "red")
                break


            if p_a_idx+1 >= len(sorted_left_point_set_with_angles):
                print 'this is the last one. we will pick it'
                color_point(p, "red")
                left_side_candidate = p
                break

            next_p_a = sorted_left_point_set_with_angles[p_a_idx+1]
            next_p = next_p_a[0]

            print "the next point we will see is in yellow."
            color_point(next_p, "yellow")

            print lr_right_point, lr_left_point, p, next_p
            if not inside_circumcircle(lr_right_point, lr_left_point, p, next_p):
                print 'next_p is not an interior of current p. current p is good. we will pick it'
                color_point(p, 'red')
                color_point(next_p, 'red')
                left_side_candidate = p
                break
            else:
                print 'next_p IS an interior of current p. current p is NOT good. we won\'t pick it. and we gonna delete the line between p and lr_right_point'
                color_point(p, 'red')
                color_point(next_p, 'red')

                target_edge = [lr_left_point, p]
                to_delete_idx = None
                for ll_idx in range(len(merged_edges)):
                    ll_edge = merged_edges[ll_idx]
                    if smae_edge_test(target_edge, ll_edge):
                        to_delete_idx = ll_idx
                        break
                if to_delete_idx != None:
                    color_edge(merged_edges[to_delete_idx], 'black')
                    del merged_edges[to_delete_idx]



        if left_side_candidate != None:
            print "we got a left_side_candidate, and it is in yellow."
            color_point(left_side_candidate, 'yellow')
            color_point(left_side_candidate, 'red')
            
        else:
            print 'we got NO left_side_candidate'

        if right_side_candidate != None:
            print "we got a right_side_candidate, and it is in blue."
            color_point(right_side_candidate, 'blue')
            color_point(right_side_candidate, 'red')
        else:
            print 'we got NO right_side_candidate'


        if left_side_candidate == None:
            if right_side_candidate == None:
                print 'no candidates! merge done!'
                color_edge(lr_edge, 'red')
                break;
            else:
                print 'only right_side_candidate shows up. we will take it.'
                lr_edge = [lr_left_point, right_side_candidate]
                merged_edges.append(lr_edge)
                show_progress(merged_edges)
        elif right_side_candidate == None:
            print 'only left_side_candidate shows up. we will take it.'
            lr_edge = [left_side_candidate, lr_right_point]
            merged_edges.append(lr_edge)
            show_progress(merged_edges)
        else:
            print 'two candidates! yah! lets choose the best!'
            if not inside_circumcircle(lr_left_point, lr_right_point, left_side_candidate, right_side_candidate):
                print 'right_side_candidate is out of the circumcircle by the othrers, so left_side_candidate is a good one. we take left_side_candidate, '
                lr_edge = [left_side_candidate, lr_right_point]
                merged_edges.append(lr_edge)    
                show_progress(merged_edges)
            else:
                print 'right_side_candidate is NOT out of the circumcircle by the othrers, so left_side_candidate is  NOT a good one. we take right_side_candidate, '
                
                lr_edge = [lr_left_point, right_side_candidate]
                merged_edges.append(lr_edge)
                show_progress(merged_edges)
        
    return merged_edges




def Delaunay_triangulation(input_points):
    def cmp_func(a, b):
        if a[0] == b[0]:
            return a[1] - b[1]
        else:
            return a[0] - b[0]

    
    #input_points = [[100, 400], [200, 200], [200, 300], [200, 500], [300, 300], [300, 400], [300, 400], [300, 500], [300, 500], [400, 200], [400, 300], [400, 300], [400, 500], [400, 600], [500, 300], [500, 300], [500, 500], [500, 600], [600, 100], [600, 200], [600, 300], [600, 400]]
    

    input_points = [[311, 415], [325, 403], [340, 415], [322, 425], [381, 424], [402, 408], [421, 423], [404, 433], [320, 465], [337, 445], [364, 463], [338, 479], [314, 497], [336, 489], [377, 499], [337, 511], [380, 335], [353, 563], [468, 473], [277, 468], [301, 376], [470, 383], [299, 535], [436, 535], [510, 567], [553, 639], [264, 594], [217, 681], [392, 611], [385, 686], [202, 744], [558, 754], [78, 219], [78, 802], [688, 802], [688, 219]]

    for idx in range(len(input_points)):
        input_points[idx][0] = int(input_points[idx][0]/0.5)
        input_points[idx][1] = int(input_points[idx][1]/1.3)



    for p in input_points:
        color_point(p, 'red')

    print 'game begins'

    input_points = sorted(input_points, cmp=cmp_func)
    edges = Delaunay_recursive_actor(input_points)
    show_progress(edges)
    print input_points

canvas = None
point_set = []



def UI_run():
    global canvas
    root = Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    
    canvas_width = int(root.winfo_screenwidth())*0.9
    canvas_height = int(root.winfo_screenheight())*0.9
    canvas = Canvas(root, width = canvas_width, height=canvas_height)
    canvas.pack()    
    canvas.config(background='black')

    r = 5
    def printcoords(event):
        global point_set
        print event.x
        print event.y
        event.x = (event.x/100)*100
        event.y = (event.y/100)*100

        print event.x
        print event.y

        point_set.append([event.x, event.y])
        canvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill="red")

    canvas.bind("<Button 1>",printcoords)

    def run_Delaunay_triangulation():
        global point_set
        Delaunay_triangulation(point_set)

    def clear_canvas():
        global point_set
        point_set = []
        canvas.delete('all')
        

    B_1 = Button(root, text ="run_Delaunay_triangulation", command = run_Delaunay_triangulation)
    B_1.pack()

    B_2 = Button(root, text ="clear_canvas", command = clear_canvas)
    B_2.pack()

    root.mainloop()

if __name__ == "__main__":
    UI_run()

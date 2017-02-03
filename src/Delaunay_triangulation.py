from Tkinter import *
from tkFileDialog import askopenfilename
import Image, ImageTk

import time
from threading import Thread

import tkMessageBox

import math

import numpy
from numpy import matrix

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

def show_progress(canvas, edges, color="red"):
    for e in edges:
        a = e[0]
        b = e[1]
        canvas.create_line(a[0], a[1], b[0], b[1], fill=color)

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



    if a2b < 0:
        a2b += 360

    if a2c < 0:
        a2c += 360


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


def Delaunay_recursive_actor(point_set):
    if len(point_set) == 2:
        edges = [[point_set[0], point_set[1]]]
        
        return edges

    if len(point_set) == 3:
        edges = [[point_set[0], point_set[1]], [point_set[0], point_set[2]], [point_set[1], point_set[2]]] 
        
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

    #print "now we'll try to find bottommost edge."

    while True:
        possible_lr_edge = [y_sorted_left_points[left_idx], y_sorted_right_points[right_idx]]
        

        flag = True
        for ll_edge in left_edges:
           


            if edge_intersect_test(ll_edge, possible_lr_edge):
                flag = False
                break

        if flag:
            #print "ll_edge checking says good. now we'll try rr_edge check."
            for rr_edge in right_edges:
   
                if edge_intersect_test(rr_edge, possible_lr_edge):
                    flag = False
                    break



        if flag:
            #print "rr_edge checking says good, this will be our bottommost edge."
            lr_edge = possible_lr_edge
            break

        #print 'we look to bottom X possible_lr_edge now.'

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

            for ll_edge in left_edges:
        
                if edge_intersect_test(ll_edge, possible_lr_edge):
                  
                    flag = False
                    break
                
            if flag:
                for rr_edge in right_edges:
                    if edge_intersect_test(rr_edge, possible_lr_edge):
                        flag = False
                        break
                
            if flag:
                lr_edge = possible_lr_edge
                left_idx = idx_to_try[idx][0]
                right_idx = idx_to_try[idx][1]
                lr_edge = possible_lr_edge
                break



        if flag:
            #print 'bottommost edge found. we will call this off.'
            break
        else:
            #print 'bottommost edge NOT found. we will step bottom up 1 unit.'
            left_idx += 1
            right_idx += 1
            if left_idx >= len(y_sorted_left_points) or right_idx >= len(y_sorted_right_points):
                #print 'steping failed. we cannot find bottommost edge.'
                break

    #print '-'*10

    merged_edges = left_edges+right_edges 

    if lr_edge == None:
        #print 'fuck. bottom lr not found.'
        return merged_edges

    merged_edges.append(lr_edge)

    #print "good. we got our bottommost edge yet. now, let try to merge them further."

    #print 'now, we try to find next lr_edge'
    while lr_edge != None:


        #try to fine more LR edges
        lr_right_point = lr_edge[1]
        lr_left_point = lr_edge[0]




        sorted_right_point_set_with_angles = get_sorted_candidates(lr_right_point, lr_left_point, right_point_set, merged_edges)
        sorted_right_point_set_with_angles = sorted_right_point_set_with_angles[::-1]
        sorted_left_point_set_with_angles = get_sorted_candidates(lr_left_point, lr_right_point, left_point_set, merged_edges)
        
        #print "let's try to find a right_side_candidate"
        #start from the right side
        right_side_candidate = None
        for p_a_idx in range(len(sorted_right_point_set_with_angles)):
            p_a = sorted_right_point_set_with_angles[p_a_idx]
            p = p_a[0]

            angle = p_a[1]
            

            
            if angle <= 180:
                break

            if p_a_idx+1 >= len(sorted_right_point_set_with_angles):

                right_side_candidate = p
                break

            next_p_a = sorted_right_point_set_with_angles[p_a_idx+1]
            next_p = next_p_a[0]



            

            if not inside_circumcircle(lr_left_point, lr_right_point, p, next_p):

                right_side_candidate = p
                break
            else:

                

                target_edge = [lr_right_point, p]
                to_delete_idx = None
                for rr_idx in range(len(merged_edges)):
                    rr_edge = merged_edges[rr_idx]
                    if smae_edge_test(target_edge, rr_edge):
                        to_delete_idx = rr_idx
                        break
                if to_delete_idx != None:
                    del merged_edges[to_delete_idx]



        #print "let's try to find a left_side_candidate"
        #then the left side
        left_side_candidate = None
        for p_a_idx in range(len(sorted_left_point_set_with_angles)):
            p_a = sorted_left_point_set_with_angles[p_a_idx]
            p = p_a[0]
            angle = p_a[1]
            


            if angle >= 180 or angle == 0:

                break


            if p_a_idx+1 >= len(sorted_left_point_set_with_angles):

                left_side_candidate = p
                break

            next_p_a = sorted_left_point_set_with_angles[p_a_idx+1]
            next_p = next_p_a[0]



            if not inside_circumcircle(lr_right_point, lr_left_point, p, next_p):

                left_side_candidate = p
                break
            else:


                target_edge = [lr_left_point, p]
                to_delete_idx = None
                for ll_idx in range(len(merged_edges)):
                    ll_edge = merged_edges[ll_idx]
                    if smae_edge_test(target_edge, ll_edge):
                        to_delete_idx = ll_idx
                        break
                if to_delete_idx != None:
                    del merged_edges[to_delete_idx]






        if left_side_candidate == None:
            if right_side_candidate == None:

                break;
            else:
                #print 'only right_side_candidate shows up. we will take it.'
                lr_edge = [lr_left_point, right_side_candidate]
                merged_edges.append(lr_edge)
        elif right_side_candidate == None:
            #print 'only left_side_candidate shows up. we will take it.'
            lr_edge = [left_side_candidate, lr_right_point]
            merged_edges.append(lr_edge)
        else:
            #print 'two candidates! yah! lets choose the best!'
            if not inside_circumcircle(lr_left_point, lr_right_point, left_side_candidate, right_side_candidate):
                #print 'right_side_candidate is out of the circumcircle by the othrers, so left_side_candidate is a good one. we take left_side_candidate, '
                lr_edge = [left_side_candidate, lr_right_point]
                merged_edges.append(lr_edge)
            else:
                #print 'right_side_candidate is NOT out of the circumcircle by the othrers, so left_side_candidate is  NOT a good one. we take right_side_candidate, '
                
                lr_edge = [lr_left_point, right_side_candidate]
                merged_edges.append(lr_edge)
        
    return merged_edges

def Delaunay_triangulation(input_points):
    def cmp_func(a, b):
        if a[0] == b[0]:
            return a[1] - b[1]
        else:
            return a[0] - b[0]

    input_points = sorted(input_points, cmp=cmp_func)
    

    edges = Delaunay_recursive_actor(input_points)
    #print 'input_points:'
    #print input_points
    return edges


def edges_to_triangels(raw_edges):
    edges = raw_edges[:]
    triangles = []

    while len(edges) != 0:
        now_edge = edges.pop()

        if same_point_test(now_edge[0], now_edge[1]):
            continue

        #color_edge(now_edge, 'green')

        p1 = now_edge[0]
        p2 = now_edge[1]

        for e1 in edges:
            pp1 = None
            if same_point_test(e1[0], p1):
                pp1 = e1[1]
            elif same_point_test(e1[1], p1):
                pp1 = e1[0]

            if pp1 != None:

                #color_edge(e1, 'white')

                for e2 in edges:
                    pp2 = None
                    if same_point_test(e2[0], pp1):
                        pp2 = e2[1]
                    elif same_point_test(e2[1], pp1):
                        pp2 = e2[0]

                    if pp2 != None and same_point_test(pp2, p2):
                        #color_edge(e2, 'yellow')
                        v1 = now_edge[0]
                        v2 = now_edge[1]

                        for vv in e1:
                            if not same_point_test(vv, v1) and not same_point_test(vv, v2):
                                v3 = vv
                                break 
                        triangles.append([v1, v2, v3])

    return triangles

def locate_p_in_a_set(point_set, p):
    for i in range(len(point_set)):
        now_p = point_set[i]
        if same_point_test(p, now_p):
            return i


def assign_triangles_id(triangles, point_set):
    to_return = []
    for t in triangles:
        p1 = t[0]
        p2 = t[1]
        p3 = t[2]

        tid = [0, 0, 0]
        tid[0] = locate_p_in_a_set(point_set, p1)
        tid[1] = locate_p_in_a_set(point_set, p2)
        tid[2] = locate_p_in_a_set(point_set, p3) 


        to_return.append([t, tid])
    return to_return

def get_triangle_pairs(src_triangles, dst_points):
    to_return = []

    for t1 in src_triangles:
        t2 = []
        for idx in t1[1]:
            t2.append(dst_points[idx])

        to_return.append([t1[0], t2[:]])

    return to_return
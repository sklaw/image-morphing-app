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


def check_bottomedge(edge, point_set):
    b = edge[0]
    a = edge[1]

    ab = subtract(b, a)

    flag = True

    for p in point_set:
        if same_point_test(p, a) or same_point_test(p, b):
            continue 

        ap = subtract(p, a)

        angle = get_angle(ab, ap)

        if angle < 180:
            flag = False
            break

    return flag



def Delaunay_recursive_actor(point_set):
    if len(point_set) == 2:
        edges = [[point_set[0], point_set[1]]]
        #show_progress(edges) 
        return edges

    if len(point_set) == 3:
        edges = [[point_set[0], point_set[1]], [point_set[0], point_set[2]], [point_set[1], point_set[2]]] 
        #show_progress(edges)
        return edges


    left_point_set = point_set[:len(point_set)/2]
    right_point_set = point_set[len(point_set)/2:]

    

    left_edges = Delaunay_recursive_actor(left_point_set)
    right_edges = Delaunay_recursive_actor(right_point_set)

    merged_edges = left_edges+right_edges 


    #try to fine bottommost LR edge
    y_sorted_left_points = sorted(left_point_set, key=lambda x:x[1])
    y_sorted_right_points = sorted(right_point_set, key=lambda x:x[1])

    left_idx = right_idx = 0
    lr_edge = None

    #print "now we'll try to find bottommost edge."

    lr_edge_found = False

    for lp in y_sorted_left_points:
        if lr_edge_found:
            break

        for rp in y_sorted_right_points:
            possible_lr_edge = [lp, rp]
            #print "got one possible_lr_edge."
            #color_edge(possible_lr_edge, 'green')

            flag = True
            for edge in merged_edges:
                #print "checking intersection against a merge edge."
                #color_edge(edge, 'white')
                #color_edge(edge, 'red')


                if edge_intersect_test(edge, possible_lr_edge):
                    #print "intersection found. we'll stop this checking."
                    #color_edge(possible_lr_edge, 'black')
                    flag = False
                    break

            if not flag:
                continue

            if check_bottomedge(possible_lr_edge, point_set):
                #print "check_bottomedge checking says good, this will be our bottommost edge."
                lr_edge = possible_lr_edge
                lr_edge_found = True
                break
            else:
                #print 'though no intersection with any edges, this is not a real bottom.'
                #color_edge(possible_lr_edge, 'black')
                pass
        


    #print '-'*10


    
    if lr_edge == None:
        #print 'fuck. bottom lr not found.'
        return merged_edges


    merged_edges.append(lr_edge)
    #show_progress(merged_edges)

    #print "good. we got our bottommost edge yet. now, let try to merge them further."

    #print 'now, we try to find next lr_edge'
    while lr_edge != None:
        #print 'the current lr_edge is in green'
        #color_edge(lr_edge, 'green')

        #try to fine more LR edges
        lr_right_point = lr_edge[1]
        lr_left_point = lr_edge[0]

        #print "lr_left_point"        
        #color_point(lr_left_point, "yellow")
        #print 'lr_right_point'
        #color_point(lr_right_point, "blue")

        #color_point(lr_left_point, "red")
        #color_point(lr_right_point, "red")


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
            
            #print "the point we are seeing is in white."
            #print "angle in degrees: ", angle
            #color_point(p, "white")
            
            if angle <= 180:
                #print "it is less than 180 degrees when look upward. we will ignore it"
                #color_point(p, "red")
                break

            if p_a_idx+1 >= len(sorted_right_point_set_with_angles):
                #print 'this is the last one. we will pick it'
                #color_point(p, "red")
                right_side_candidate = p
                break

            next_p_a = sorted_right_point_set_with_angles[p_a_idx+1]
            next_p = next_p_a[0]


            #print "the next point we will see is in yellow."
            #color_point(next_p, "yellow")
            

            if not inside_circumcircle(lr_left_point, lr_right_point, p, next_p):
                #print 'next_p is not an interior of current p. current p is good. we will pick it'
                #color_point(p, 'red')
                #color_point(next_p, 'red')
                right_side_candidate = p
                break
            else:
                #print 'next_p IS an interior of current p. current p is NOT good. we won\'t pick it. and we gonna delete the line between p and lr_right_point'
                #color_point(p, 'red')
                #color_point(next_p, 'red')
                

                target_edge = [lr_right_point, p]
                to_delete_idx = None
                for rr_idx in range(len(merged_edges)):
                    rr_edge = merged_edges[rr_idx]
                    if smae_edge_test(target_edge, rr_edge):
                        to_delete_idx = rr_idx
                        break
                if to_delete_idx != None:
                    #color_edge(merged_edges[to_delete_idx], 'black')
                    del merged_edges[to_delete_idx]



        #print "let's try to find a left_side_candidate"
        #then the left side
        left_side_candidate = None
        for p_a_idx in range(len(sorted_left_point_set_with_angles)):
            p_a = sorted_left_point_set_with_angles[p_a_idx]
            p = p_a[0]
            angle = p_a[1]
            
            #print "the point we are seeing is in white."
            #print "angle in degrees: ", angle
            #color_point(p, "white")

            if angle >= 180 or angle == 0:

                #print "it is less than 180 degrees when look upward. we will ignore it"
                #color_point(p, "red")
                break


            if p_a_idx+1 >= len(sorted_left_point_set_with_angles):
                #print 'this is the last one. we will pick it'
                #color_point(p, "red")
                left_side_candidate = p
                break

            next_p_a = sorted_left_point_set_with_angles[p_a_idx+1]
            next_p = next_p_a[0]

            #print "the next point we will see is in yellow."
            #color_point(next_p, "yellow")

            #print lr_right_point, lr_left_point, p, next_p
            if not inside_circumcircle(lr_right_point, lr_left_point, p, next_p):
                #print 'next_p is not an interior of current p. current p is good. we will pick it'
                #color_point(p, 'red')
                #color_point(next_p, 'red')
                left_side_candidate = p
                break
            else:
                #print 'next_p IS an interior of current p. current p is NOT good. we won\'t pick it. and we gonna delete the line between p and lr_right_point'
                #color_point(p, 'red')
                #color_point(next_p, 'red')

                target_edge = [lr_left_point, p]
                to_delete_idx = None
                for ll_idx in range(len(merged_edges)):
                    ll_edge = merged_edges[ll_idx]
                    if smae_edge_test(target_edge, ll_edge):
                        to_delete_idx = ll_idx
                        break
                if to_delete_idx != None:
                    #color_edge(merged_edges[to_delete_idx], 'black')
                    del merged_edges[to_delete_idx]





        if left_side_candidate == None:
            if right_side_candidate == None:
                #print 'no candidates! merge done!'
                #color_edge(lr_edge, 'red')
                break;
            else:
                #print 'only right_side_candidate shows up. we will take it.'
                lr_edge = [lr_left_point, right_side_candidate]
                merged_edges.append(lr_edge)
                #show_progress(merged_edges)
        elif right_side_candidate == None:
            #print 'only left_side_candidate shows up. we will take it.'
            lr_edge = [left_side_candidate, lr_right_point]
            merged_edges.append(lr_edge)
            #show_progress(merged_edges)
        else:
            #print 'two candidates! yah! lets choose the best!'
            if not inside_circumcircle(lr_left_point, lr_right_point, left_side_candidate, right_side_candidate):
                #print 'right_side_candidate is out of the circumcircle by the othrers, so left_side_candidate is a good one. we take left_side_candidate, '
                lr_edge = [left_side_candidate, lr_right_point]
                merged_edges.append(lr_edge)    
                #show_progress(merged_edges)
            else:
                #print 'right_side_candidate is NOT out of the circumcircle by the othrers, so left_side_candidate is  NOT a good one. we take right_side_candidate, '
                
                lr_edge = [lr_left_point, right_side_candidate]
                merged_edges.append(lr_edge)
                #show_progress(merged_edges)
        
    return merged_edges



def Delaunay_triangulation(input_points):
    def cmp_func(a, b):
        if a[0] == b[0]:
            return a[1] - b[1]
        else:
            return a[0] - b[0]

    input_points = sorted(input_points, cmp=cmp_func)
    

    edges = Delaunay_recursive_actor(input_points)
    ###print 'input_points:'
    ###print input_points
    return edges


def edges_to_triangels(raw_edges):
    edges = raw_edges[:]
    triangles = []

    while len(edges) != 0:
        now_edge = edges.pop()

        if same_point_test(now_edge[0], now_edge[1]):
            continue

        ##color_edge(now_edge, 'green')

        p1 = now_edge[0]
        p2 = now_edge[1]

        for e1 in edges:
            pp1 = None
            if same_point_test(e1[0], p1):
                pp1 = e1[1]
            elif same_point_test(e1[1], p1):
                pp1 = e1[0]

            if pp1 != None:

                ##color_edge(e1, 'white')

                for e2 in edges:
                    pp2 = None
                    if same_point_test(e2[0], pp1):
                        pp2 = e2[1]
                    elif same_point_test(e2[1], pp1):
                        pp2 = e2[0]

                    if pp2 != None and same_point_test(pp2, p2):
                        ##color_edge(e2, 'yellow')
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


def get_triangle_ids(triangles, point_set):
    to_return = [None]*len(triangles)
    for idx in range(len(triangles)):
        t = triangles[idx]
        p1 = t[0]
        p2 = t[1]
        p3 = t[2]

        tid = [0, 0, 0]
        tid[0] = locate_p_in_a_set(point_set, p1)
        tid[1] = locate_p_in_a_set(point_set, p2)
        tid[2] = locate_p_in_a_set(point_set, p3) 


        to_return[idx] = tid
    return to_return

def ids_2_triangles(triangle_ids, dst_points):
    triangles = [None]*len(triangle_ids)
    for idx in range(len(triangle_ids)):
        ids = triangle_ids[idx]
        t = [None, None, None]
        t[0] = dst_points[ids[0]]
        t[1] = dst_points[ids[1]]
        t[2] = dst_points[ids[2]]
        triangles[idx] = t
    return triangles


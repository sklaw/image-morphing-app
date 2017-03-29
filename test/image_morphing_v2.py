from PIL import Image, ImageSequence
import math
from numpy import matrix

from Delaunay_triangulation import *
src_points = [[305, 444], [434, 443], [352, 527], [387, 529], [354, 585], [391, 581], [374, 274], [245, 504], [515, 488], [384, 681], [277, 607], [496, 602], [483, 332], [258, 356], [307, 403], [429, 399], [374, 465], [0, 0], [0, 1023], [767, 1023], [767, 0]]

dst_points = [[225, 95], [283, 104], [208, 134], [227, 135], [210, 159], [237, 166], [271, 53], [189, 127], [353, 139], [236, 211], [200, 189], [317, 190], [339, 76], [205, 80], [237, 75], [286, 85], [241, 108], [0, 0], [0, 412], [549, 412], [549, 0]]

from BresenhamLineGenerator import BresenhamLineGenerator



def draw_convex_polygon(vertices, input_pixels, input_size, value):
    vertices = sorted(vertices, key=lambda x:x[0])
    vertices = sorted(vertices, key=lambda x:x[1])
    input_height = input_size[1]
    input_width = input_size[0]

    s1 = 0
    d1 = 1

    s2 = 0
    d2 = len(vertices)-1

    line_1 = BresenhamLineGenerator(vertices[s1], vertices[d1])
    line_2 = BresenhamLineGenerator(vertices[s2], vertices[d2])

    point_1 = vertices[0]
    point_2 = vertices[0]

    new_point_1 = point_1
    new_point_2 = point_2

    done = False
    
    while not done:
        while True:
            new_point_1 = line_1.get_next_point()

            if new_point_1 == None:
                #print "line 1 consumed with s1:"+str(s1)+" d1:"+str(d1)
                if d1 == d2:
                    done = True
                    break;
                else:
                    s1 = d1
                    d1 += 1
                    line_1 = BresenhamLineGenerator(vertices[s1], vertices[d1])
                    continue

            input_pixels[new_point_1[1]*input_width+new_point_1[0]] = value

            if new_point_1[1] == point_1[1]:
                prev_point_1 = new_point_1             
                continue
            point_1 = prev_point_1
            prev_point_1 = new_point_1
            break

        while True:
            new_point_2 = line_2.get_next_point()

            if new_point_2 == None:
                #print "line 2 consumed with s2:"+str(s2)+" d2:"+str(d2)
                if d1 == d2:
                    done = True
                    break;
                else:
                    s2 = d2
                    d2 -= 1
                    line_2 = BresenhamLineGenerator(vertices[s2], vertices[d2])
                    continue

            input_pixels[new_point_2[1]*input_width+new_point_2[0]] = value


            if new_point_2[1] == point_2[1]:
                prev_point_2 = new_point_2
                continue

            point_2 = prev_point_2
            prev_point_2 = new_point_2
            break

        y = point_1[1]
        x1 = point_1[0]
        x2 = point_2[0]
        if x1 > x2:
            tmp = x2
            x2 = x1
            x1 = tmp

        #print "scanline y:"+str(y)+" from "+str(x1)+" to "+str(x2)

        for i in range(x1+1, x2):
            input_pixels[y*input_width+i] = value


        point_1 = new_point_1
        point_2 = new_point_2




def draw_line(input_pixels, input_size, value, p1, p2):
    input_width = input_size[0]
    input_height = input_size[1]


    tmp = BresenhamLineGenerator([p1[0], p1[1]], [p2[0], p2[1]])
    while not tmp.done:
        point = tmp.get_next_point()
        col = point[0]
        row = point[1]
        input_pixels[row*input_width+col] = value


def pad_to_center(input_pixels, input_size, output_size, zero_value):
    input_width = input_size[0]
    input_height = input_size[1]

    output_width = output_size[0]
    output_height = output_size[1]

    width_offset = (output_width - input_width)/2
    height_offset = (output_height - input_height)/2

    output_pixels = [zero_value]*(output_width*output_height)

    for h in range(input_height):
        for w in range(input_width):
            new_h = h+height_offset
            new_w = w+width_offset
            output_pixels[new_h*output_width+new_w] = input_pixels[h*input_width+w]

    return output_pixels


def adjust_points_after_padding(src_points, dst_points, src_size, dst_size, output_size):
    input_width = src_size[0]
    input_height = src_size[1]

    output_width = output_size[0]
    output_height = output_size[1]

    width_offset = (output_width - input_width)/2
    height_offset = (output_height - input_height)/2

 
    for p in src_points:
        p[0] += width_offset
        p[1] += height_offset

    input_width = dst_size[0]
    input_height = dst_size[1]

    width_offset = (output_width - input_width)/2
    height_offset = (output_height - input_height)/2

    for p in dst_points:
        p[0] += width_offset
        p[1] += height_offset

def get_warping_matrix(t1, t2):

    t = t1
    src_cor = [[t[0][0], t[1][0], t[2][0]],\
                [t[0][1], t[1][1], t[2][1]],\
                [1,1,1]]

    t = t2
    dst_cor = [[t[0][0], t[1][0], t[2][0]],\
                [t[0][1], t[1][1], t[2][1]],\
                [1,1,1]]

    A = matrix(src_cor)
    B = matrix(dst_cor)

    AT = A.T
    AAT = A*AT
    AATinv = AAT.I

    H = B*AT*AATinv
    return H.tolist()

def warp_one_point(p, raw_m):
    m = raw_m


    x = p[0]*m[0][0]+p[1]*m[0][1]+1*m[0][2]
    y = p[0]*m[1][0]+p[1]*m[1][1]+1*m[1][2]
    return [int(x), int(y)]

def get_transition_point(p1, p2, t):
    #print p1, p2
    ox = p2[0]-p1[0]
    oy = p2[1]-p1[1]
    return [int(p1[0]+ox*t), int(p1[1]+oy*t)] 

def get_transition_point_set(src_points, dst_points, t):
    to_return = []
    for idx in range(len(src_points)):
        p1 = src_points[idx]
        p2 = dst_points[idx]

        
        to_return.append(get_transition_point(p1, p2, t))

    return to_return

def morph_baby(src_img, dst_img, src_points, dst_points, step):
    src_pixels = list(src_img.getdata())
    src_mode = src_img.mode
    src_size = src_img.size
    src_height = src_size[1]
    src_width = src_size[0]

    dst_pixels = list(dst_img.getdata())
    dst_mode = dst_img.mode
    dst_size = dst_img.size
    dst_height = dst_size[1]
    dst_width = dst_size[0]

    output_height = max(src_height, dst_height)
    output_width = max(src_width, dst_width)
    output_size = (output_width, output_height)

    src_pixels = pad_to_center(src_pixels, src_size, output_size, (0,0,0))
    output_img = Image.new(src_mode, output_size)
    output_img.putdata(src_pixels)
    #output_img.save("src padded.jpg")

    dst_pixels = pad_to_center(dst_pixels, dst_size, output_size, (0,0,0))
    output_img = Image.new(dst_mode, output_size)
    output_img.putdata(dst_pixels)
    #output_img.save("dst padded.jpg")


    adjust_points_after_padding(src_points, dst_points, src_size, dst_size, output_size)

    idx_map = [-1]*(output_height*output_width)
    dual_matrix_list = []


    img_list = []
    count = 0
    t = 0.0
    while t <= 1:
        for i in range(len(idx_map)):
            idx_map[i] = -1

        dual_matrix_list = []



        now_points = get_transition_point_set(src_points, dst_points, t)

        now_edges = Delaunay_triangulation(now_points)

        now_triangles = edges_to_triangels(now_edges)

        now_triangles_with_id = assign_triangles_id(now_triangles, now_points)


        now_src_triangle_pairs = get_triangle_pairs(now_triangles_with_id, src_points)
        now_dst_triangle_pairs = get_triangle_pairs(now_triangles_with_id, dst_points)
  
        

        for i in range(len(now_src_triangle_pairs)):
            dual_matrix = []
            dual_matrix.append(get_warping_matrix(now_src_triangle_pairs[i][0], now_src_triangle_pairs[i][1]))
            dual_matrix.append(get_warping_matrix(now_dst_triangle_pairs[i][0], now_dst_triangle_pairs[i][1]))
            dual_matrix_list.append(dual_matrix[:])

            draw_convex_polygon(now_src_triangle_pairs[i][0], idx_map, output_size, i)


        output_pixels = []

        for h in range(output_height):
            for w in range(output_width):
                m_idx = idx_map[h*output_width+w]
                if m_idx == -1:
                    output_pixels.append((0,0,0))
                    continue

                src_cor = warp_one_point([w, h], dual_matrix_list[m_idx][0])
                src_w = src_cor[0]
                src_h = src_cor[1]


                dst_cor = warp_one_point([w, h], dual_matrix_list[m_idx][1])
                dst_w = dst_cor[0]
                dst_h = dst_cor[1]


                src_pixel = src_pixels[src_h*output_width+src_w]
                dst_pixel = dst_pixels[dst_h*output_width+dst_w]

                src_pixel = [(1-t)*i for i in src_pixel]
                dst_pixel = [t*i for i in dst_pixel]

                now_pixel = [int(src_pixel[i]+dst_pixel[i]) for i in range(3)]

                output_pixels.append(tuple(now_pixel))


        output_img = Image.new(src_mode, output_size)
        output_img.putdata(output_pixels)
        
        img_list.append(output_img)

        print t
        t += step

    total_steps = int(1/step)

    last_frame = img_list[-1]
    for i in range(total_steps/5):
        img_list.append(last_frame)

    from images2gif import writeGif
    writeGif("result.gif", img_list, duration=0.1)
        

if __name__ == '__main__':
    src_img = Image.open('src.jpg')
    dst_img = Image.open('dst.jpg')
    morph_baby(src_img, dst_img, src_points, dst_points)
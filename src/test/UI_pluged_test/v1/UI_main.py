from Tkinter import *
from tkFileDialog import askopenfilename
import Image, ImageTk

from UI_select_image import UI_select_image
from UI_feature_point_specification import UI_feature_point_specification

if __name__ == '__main__':
    root = Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    
    img_path = [None, None, None]
    UI_select_image(root, img_path)
    
    #img_path = ['src.jpg', 'dst.jpg', "."]

    root = Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    UI_feature_point_specification(root, img_path[0], img_path[1], img_path[2])
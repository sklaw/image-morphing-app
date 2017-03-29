from Tkinter import *
from tkFileDialog import askopenfilename
import Image, ImageTk

from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory

import pickle


def UI_select_image(root, img_path):


    def path_picker(lable, idx, type=0):
        if type == 0:
            filename = askopenfilename() 
        else:
            filename = askdirectory()

        if filename != "":
            now_text = lable.cget("text")
            title = now_text.split(':')[0]
            lable.config(text=title+":"+filename)
            img_path[idx] = filename
            print filename
            with open('cached_filepaths.pickle', 'wb') as handle:
                pickle.dump(img_path, handle, protocol=pickle.HIGHEST_PROTOCOL)
    def said_pick_finish():
        flag = True
        for p in img_path:
            if p == None:
                flag = False
                break

        if flag:
            root.destroy()

    try:
        with open('cached_filepaths.pickle', 'rb') as handle:
            cached_filepaths = pickle.load(handle)
            print cached_filepaths
    except IOError as e:
        pass

    try:
        si = cached_filepaths[0]
    except Exception as e:
        si = None
    img_path[0] = si
    T_1 = Label(root, text="source image: "+str(si))
    T_1.pack()
    B_1 = Button(root, text="pick source image", command = lambda : path_picker(T_1, 0))
    B_1.pack()

    try:
        di = cached_filepaths[1]
    except Exception as e:
        di = None
    img_path[1] = di
    T_2 = Label(root, text="destination image: "+str(di))
    T_2.pack()
    B_2 = Button(root, text ="pick destination image", command = lambda : path_picker(T_2, 1))
    B_2.pack()

    try:
        resultdir = cached_filepaths[2]
    except Exception as e:
        resultdir = None
    img_path[2] = resultdir
    T_3 = Label(root, text="folder to save the result: "+str(resultdir))
    T_3.pack()
    B_3 = Button(root, text ="pick folder to save the result", command = lambda : path_picker(T_3, 2, 1))
    B_3.pack()

    B_4 = Button(root, text ="go!", command = said_pick_finish)
    B_4.pack()



    root.mainloop()

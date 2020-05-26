#!/usr/bin/env python3

import os
import re
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter

def main():

    # iterate over the files in the current folder and call get_files() to get the data_files
    try:
        os.system("clear")
        pattern = r"Environmental_Data_Deep_Moor_20[0-9]{2}\.txt"

        data_files = get_files(pattern)

    except Exception as e:
        print("Custom error gettin files: ", type(e), e)

    # Once we got the files we start importing the data to numpy arrays
    try:
        import csv
        import pandas as pd
        import numpy as np
        from datetime import datetime

        # we  will initially extract and store the data in 2 lists
        fecha = []
        presion = []

        for file in data_files:
            with open(file) as f:
                reader = csv.reader(f, delimiter='\t')
                next(reader)                            # skipping headers
                for row in reader:
                    # row[0] is the date time column which we transform to a datetime object
                    datetime_object = datetime.strptime(row[0], '%Y_%m_%d %H:%M:%S')
                    fecha.append(datetime_object)

                    # row[2] is the barometric pressure
                    # the y axis of the plot was displayed unordered because it was not float
                    presion.append(float(row[2]))

        #         print("fecha :", fecha[-1])
        #         print("presion :", presion[-1])
        #         print("-------------")
            print("loading data from: ", file)
        nfecha = np.array(fecha)
        npresion = np.array(presion)

        # print("n fecha :", nfecha[-1])
        # print("n presion :", npresion[-1])
        # print("-------------")

    except Exception as e:
        print("Custom error:", type(e), e)



    # now we will pass the numpy arrays to matplotlib
    try:
        from matplotlib import pyplot as plt


        x = nfecha
        y = npresion

        # root = Root()
        MatplotCanvas(x,y)

        # plt.title("Weather Statistics")
        # plt.xlabel("FECHA")
        # plt.ylabel("BAROMETRIC PRESSURE")
        # plt.scatter(x, y)

        # plt.show()
    except tkinter.TclError as e:

        import platform
        print(type(e), e)
        print("The OS is ", platform.platform(), "you may need a Xming like server to be running in Windows")

    except Exception as e:
        print("Custom error Passing data to matplotlib:", type(e), e)

# class Root(tkinter):
#     def __init__(self):
#         super(Root, self).__init__()
#         self.title("Tkinter Matplotlib embedding")
#         self.minsize(640, 400)

#         self.MatplotCanvas()

def MatplotCanvas(x, y):

    root = tkinter.Tk()
    root.wm_title("Embedding in Tk")

    f = Figure(figsize=(5, 5), dpi=100)
    a = f.add_subplot(111)
    a.scatter(x,y)

    canvas = FigureCanvasTkAgg (f, master=root)
    # canvas.show()
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    tkinter.mainloop()


def get_files(regex):
    """ Returns a list of files in the current folder that match pattern in their name.
    The pattern should be a regex (raw preferably)
    """
    dir_files = os.listdir()
    files = []
    for f in dir_files:
        if re.search(regex, f):
            # print(file)
            files.append(f)

    if len(files) == 0:
        raise Exception("ERROR: no Environmental_Data_Deep_Moor_20xx.txt to import in " + str(os.getcwd()))
    else: return files


# the following IF statement is done to identify if the script is being executed or imported as a module
# if it is exec name == main and if it is imported name = moduleName
# this is to avoid being executed when being imported

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import os, platform, re, csv
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import pyplot as plt
import tkinter
from tkinter import ttk, messagebox
from datetime import datetime
import numpy as np


def main():

    # iterate over the files in the current folder and call get_files() to get the data_files
    try:
        os.system("clear")
        pattern = r"Environmental_Data_Deep_Moor_20[0-9]{2}\.txt"

        data_files = get_files(pattern)
        # Returns nfecha and npresion which are 1D numpy arrays containing
        # date and barometric pressure extracted from data_files(list) argument
        x, y = extractData(data_files)

        plot1 = Plot(x, y)
        tkinter.mainloop()

    except tkinter.TclError as e:

        print(type(e), e)
        print("The OS is ", platform.platform(), "you may need a Xming like server to be running in Windows")

    except Exception as e:
        print("Custom error gettin files: ", type(e), e)


class Plot:
    """ it creates a scatter plot embeded in tk Figure with the narrays x and y.

    args x, y type numpy.array
    """
    def __init__(self, x, y):
        # The Axes of the plot are the data boundaries
        # As we display all data in the first plot the Axis are
        # also equal to the Axes

        self.xAxis = x
        self.yAxis = y

        root = tkinter.Tk()
        root.title("PLOT Embedded in Tk")
        m = root.maxsize()
        root.geometry('{}x{}+0+0'.format(*m))

        f = Figure(figsize=(5, 5), dpi=100)
        self.subPlot = f.add_subplot(111)

        self.subPlot.scatter(self.xAxis, self.yAxis)

        self.canvas = FigureCanvasTkAgg (f, root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, root)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        panedWindow = ttk.PanedWindow(root, orient=tkinter.HORIZONTAL)
        panedWindow.pack(fill=tkinter.BOTH, expand=True )

        frame1 = ttk.Frame(panedWindow)
        panedWindow.add(frame1, weight=2)

        labelStart = ttk.Label(frame1, font=("Courier", 16), text= "Start\t: ")
        labelStart.grid(row=0, column=0, padx=10)

        entryStart = ttk.Entry(frame1, width=30, font='Courier 16')
        entryStart.insert(0, str(self.xAxis[0]))
        entryStart.grid(row=0, column=1, padx=10)

        labelEnd = ttk.Label(frame1, font=("Courier", 16), text="End\t: ")
        labelEnd.grid(row=1, column=0, padx=10)

        entryEnd = ttk.Entry(frame1, width=30, font='Courier 16')
        entryEnd.insert(0, str(self.xAxis[-1]))
        entryEnd.grid(row=1, column=1, padx=10)

        # in the update button we call updatePlot
        updateButton = ttk.Button(frame1,
                        command=lambda: self.updatePlot(entryStart.get(), entryEnd.get()),
                        text="UPDATE").grid(row=0, column=2, rowspan=2, padx=10)

    def updatePlot(self, entryStart, entryEnd):
        """
        Function called when the button UPDATE is clicked.

        args entryStart, entryEnd: should be strings in datetime format '%Y-%m-%d %H:%M:%S'
        """
        try:
            s = datetime.strptime(entryStart, '%Y-%m-%d %H:%M:%S')
            e = datetime.strptime(entryEnd, '%Y-%m-%d %H:%M:%S')
            if s < self.xAxis[0] or e > self.xAxis[-1]:
                errMsg = "the date ranges introduced are not between\n{} and\n{}".format(self.xAxis[0], self.xAxis[-1])
                messagebox.showerror("Error", errMsg)
            elif e <= s :
                messagebox.showerror(title='Invalid Input Values',
                                 message='End Date must be after Start Date')
                return
            else:
                # This would return a list with all dates >= s
                # itemindexS = np.where(self.xAxis >= s)

                # searchsorted: Find indices where elements should be inserted
                # to maintain order.
                itemindexS = np.searchsorted(self.xAxis, s)
                itemindexE = np.searchsorted(self.xAxis, e)

                self.subPlot.clear()

                self.subPlot.scatter(self.xAxis[itemindexS:itemindexE] ,
                                    self.yAxis[itemindexS:itemindexE])
                self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", "Error updating plot:\n{}".format(e))


def get_files(regex):
    """ Returns a list of files in the current folder that match pattern in their name.
    The pattern should be a regex (raw preferably)
    """
    dir_files = os.listdir()
    files = []
    for f in dir_files:
        if re.search(regex, f):
            files.append(f)

    if len(files) == 0:
        raise Exception("ERROR: no Environmental_Data_Deep_Moor_20xx.txt to import in " + str(os.getcwd()))
    else: return files

def extractData(data_files):
    """ Returns nfecha and npresion which are 1D numpy arrays containing date and barometric
        pressure extracted from data_files(list) argument
    """
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

        print("loading data from", file, ", total files:", len(fecha))
    nfecha = np.array(fecha)
    npresion = np.array(presion)
    return nfecha, npresion

# the following IF statement is done to identify if the script is being executed or imported as a module
# if it is exec name == main and if it is imported name = moduleName
# this is to avoid being executed when being imported

if __name__ == '__main__':
    main()

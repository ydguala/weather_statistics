This script is to solve the Code Clinic problem of extracting weather statistics from 4 files and present them as a plot graph in a GUI \n
The python internal modules used will be;
- csv       : import tab delimited data files
- re        : regex to parse date/time values
- datetime  : manipulate datetime obj
- tkinter   : build the GUI

The python external modules used will be: numpy:
- numpy     : store weather data in arrays
- matplotlib: plot data within tkinter GUI

The flow of the program is :
- Load data to memory
- Build the GUI
- Plot all the data
- Wait for user input > get input > retrieve data > update plot > start again
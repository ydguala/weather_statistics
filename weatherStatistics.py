#!/usr/bin/env python3

def main():
    # iterate over the files in the current folder and create data_files list with the ones we want
    try:  
        import os
        import re

        os.system("clear")
        dir_files = os.listdir()
        pattern = r"Environmental_Data_Deep_Moor_20[0-9]{2}\.txt" 
        data_files = []
        for file in dir_files:
            if re.search(pattern, file):
                # print(file)
                data_files.append(file)
        
        if len(data_files) == 0:
            raise Exception("ERROR: no Environmental_Data_Deep_Moor_20xx.txt to import in " + str(os.getcwd()))
        
    except Exception as e:
        print("Custom error gettin files: ", e)

    # Once we got the files we start importing the data
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
                next(reader)        # skipping headers
                for row in reader:
                    # row[0] is the date time column which we transform to datetime object
                    datetime_object = datetime.strptime(row[0], '%Y_%m_%d %H:%M:%S')
                    fecha.append(datetime_object)
                    # row[2] is the barometric pressure

                    presion.append(row[2])

                print("fecha :",fecha[-1])
                print("presion :",presion[-1])
                print("-------------")

        nfecha = np.array(fecha)
        npresion = np.array(presion)

        print("n fecha :",nfecha[-1])
        print("n presion :",npresion[-1])
        print("-------------")

            
    except Exception as e:
        print("Custom error:",e)

# the following IF statement is done to identify if the script is being executed or imported as a module
# if it is exec name == main and if it is imported name = moduleName 
# this is to avoid being executed when being imported

if __name__ == '__main__':
    main()



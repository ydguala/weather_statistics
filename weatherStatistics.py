# iterate over the files in the current folder and create data_files list with the ones we want
try:  
    import os
    import re

    os.system("clear -x")
    dir_files = os.listdir()
    pattern = r"Environmental_Data_Deep_Moor_20[0-9]{2}\.txt" 
    data_files = []
    for file in dir_files:
        if re.search(pattern, file):
            # print(file)
            data_files.append(file)
    
    if len(data_files) == 0:
        raise Exception("ERROR: no Environmental_Data_Deep_Moor_20xx.txt to import in resources")
    
except Exception as e:
    print("Custom error", e)

# Once we got the files we start importing the data
try:
    import csv
    import pandas as pd

    li = []

    # for file in data_files:
    #     df=pd.read_csv(file, delim_whitespace=True, header=0)
    #     li.append(df)
    #     frame = pd.concat(li)
    # print(frame)            
    
    df_from_each_file = (pd.read_csv(file, delim_whitespace=True, header=0) for file in data_files)
    concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
    print(concatenated_df)            
    
    
except Exception as e:
    print("error:",e)




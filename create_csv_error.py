import sys
import csv
from tkinter import Tk
from tkinter import filedialog
import pandas as pd

Tk().withdraw()

filename = ""
error = ({})

def generate_original_file():
    original_file = pd.read_csv(filename, encoding = 'ANSI')
    return original_file
  
def generate_error_file(original):
    error_file = pd.DataFrame(data=None, index=None, columns=original.columns)
    error_file.insert(0,column='Error',value=None)
    return error_file





# for r in range(len(original_file)):
#     a = ["error " + str(r), "error " + str(r) + ".1"]
#     error = pd.Series({'Error': '\n'.join(a)})
#     other_columns = error.append(original_file.loc[r])
#     error_file = error_file.append(other_columns,ignore_index=True)


# print(error_file)

# export_csv = error_file.to_csv(filedialog.askdirectory() + "\Error.csv", index = None, header=True)
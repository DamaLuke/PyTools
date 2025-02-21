# %%
import os
import json
import nbformat

# Get the notebook name from the user
notebook_name = input("Enter the desired notebook name: ")

# Get the current directory
current_dir = os.getcwd()

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Construct the full path to the notebook
notebook_path = os.path.join(parent_dir, f'{notebook_name}.ipynb')

# Create a new notebook
nb = nbformat.v4.new_notebook()

# Add code cells
code_cell1 = "from PyTools.ModulesAutoInstall import AutoInstall\
\nAutoInstall('pandas','numpy','openpyxl','rich')\
\nimport pandas as pd\
\nimport re\
\nfrom PyTools.Manage import *\
\nfrom PyTools.xlStylesOut import write_excel\
\nimport PyTools.tkinterGUI as tkGUI\
\nfrom functools import reduce\
\nimport numpy as np\
\nimport tkinter as tk\
\nfrom PyTools.DataCleaningFunc import *"
nb['cells'].append(nbformat.v4.new_code_cell(source=code_cell1))

code_cell2 = ""
nb['cells'].append(nbformat.v4.new_code_cell(source=code_cell2))

code_cell3 = "filepath = f'{rootpath}/output/" + notebook_name + "_{today}.xlsx'\
\ndfs = {\
\n    'sheet1': df_out_1,\
\n    'Sheet2': df_out_2,\
\n    'sheet3': df_out_3,\
\n}\
\n\
write_excel(filepath, dfs, isCompeleted=True)"
nb['cells'].append(nbformat.v4.new_code_cell(source=code_cell3))

# Save the notebook
with open(notebook_path, 'w') as f:
    nbformat.write(nb, f)



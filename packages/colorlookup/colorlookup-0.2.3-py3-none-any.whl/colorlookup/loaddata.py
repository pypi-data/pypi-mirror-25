import os.path
import re
import sqlite3
import numpy as np
import pandas as pd

csv_file = os.path.join(os.path.dirname(__file__), 'colors.db')
db_file = os.path.join(os.path.dirname(__file__), 'data', 'w3c_colors.txt')

conn = sqlite3.connect(db_file)

non_decimal = re.compile(r'[^\d.]+')

def str_to_number(string):
    return non_decimal.sub('', string)

def hex_to_int(hex_string):
    return int(hex_string.lstrip('#'), 16)
    
converters = {'hex': hex_to_int,
              'hue': str_to_number,
              'hsl_sat': str_to_number,
              'hsl_light': str_to_number,
              'hsv_sat': str_to_number,
              'hsv_val': str_to_number}

colors = pd.read_csv(csv_file, 
                     header=0, index_col=0,
                     converters=converters,
                     comment='~')

colors.to_sql('w3c_colors', conn)

conn.close()

print("Success.")
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import tkinter
from tkinter import filedialog

yf.pdr_override()

stock = input("Enter Ticker Symbol: ")
print(stock)

startyear = int(input("Enter Start Year: "))
startmonth = 1
startday = 1

start = dt.datetime(startyear, startmonth, startday)
now = dt.datetime.now()

df = pdr.get_data_yahoo(stock, start, now)
df = df.sort_values('Date')

export = pd.DateFrame(data=df)

root = tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = raised)
canvas1.pack()

def exportCSV ():
    global df

    export_file_path = filedialog.asksaveasfile(defaultextension='.csv')
    df.to_csv(export_file_path, index = False, header=True)

saveAsButton_CSV = tk.Button(text='Export CSV', command=exportCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window = saveAsButton_CSV)

root.mainloop()
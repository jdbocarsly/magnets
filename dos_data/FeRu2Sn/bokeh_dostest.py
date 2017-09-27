#!/usr/bin/env python


import pandas as pd
from bokeh.charts import Scatter, output_file, show, marker, Line
from bokeh.sampledata.autompg import autompg as df

df1 = pd.read_csv("sp_dost.dat", names=["energy", "dos","idos"], sep="  ")
df2 = pd.read_csv("nonsp_dost.dat", names=["energy", "udos","ddos"], sep="  ")


tooltips=[
    ('energy','@energy'),
    ('dos','@dos')

]

p = Line(df1, x="energy", y="dos", tooltips=tooltips)

output_file("scatter.html")

show(p)

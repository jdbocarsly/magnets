#!/usr/bin/env python

import pandas as pd
#from bokeh.charts import output_file, show, Line
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool
from numpy import arange

COMPOUND_NAME="FeRu2Sn"

df1 = pd.read_csv("nonsp_dost.dat", names=["energy", "dos","idos"], sep="  ")
df2 = pd.read_csv("sp_dost.dat", names=["energy", "udos","ddos"], sep="  ")
df2["ddos"] = df2["ddos"].apply(lambda x: -x)
#df3 = pd.concat([df1, df2], ignore_index=True) #puts both sp and nonsp data into one dataframe
#df3["ddos"] = df3["ddos"].apply(lambda x: -x)

hover = HoverTool(
        tooltips=[
            ('Energy','$x'),
            ('DOS','$y')
        ]
    )

TOOLS = "box_zoom, pan, wheel_zoom, undo, redo, save, reset"

#plot = Line(df3, x="energy", y=["dos", "udos", "ddos"], xlabel="Energy (eV)", ylabel="Density of States", tools=TOOLS, active_drag="box_zoom", tooltips=tooltips)
p = figure(title=COMPOUND_NAME, x_axis_label="E - E_F (eV)", y_axis_label="Density of States", tools=[TOOLS, hover], 
    active_drag="box_zoom", x_range=(-10,10), y_range=(-20,20))

line_width=2
p.line(df1["energy"], df1["dos"], legend="No spin polarization", line_color="#A9A9A9", line_dash="solid", line_width=line_width)
p.line(df2["energy"], df2["udos"], legend="Spin-up", line_color="blue", line_dash="solid", line_alpha=0.5, line_width=line_width)
p.line(df2["energy"], df2["ddos"], legend="Spin-down", line_color="red", line_dash="solid", line_alpha=0.5, line_width=line_width)

x = arange(-10, 10, 0.1)
y = 0*x
p.line(x, y, line_color="black", line_dash="solid", line_width=1)

output_file("dostest.html")

show(p)





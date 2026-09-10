#!/usr/bin/env python

import pandas as pd
#from bokeh.charts import output_file, show, Line
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool
from numpy import arange

COMPOUND_NAME="FeRu2Sn"


df1 = pd.read_csv("nonsp_dost.dat", names=["energy", "dos","idos"], sep="  ")
df1["type"] = "nonsp"
df2 = pd.read_csv("sp_dost.dat", names=["energy", "udos","ddos"], sep="  ")
df2["type"] = "sp"
df2["ddos"] = -df2["ddos"]


#todo:
# custom HTML tooltips with title
# fix axis labels (subscripts?)
# add a vertical line through the fermi level
# remove unused data from dataframes before making the column data sources
# remove hovertool from horizontal/vertical liness
# hover highlighting vertically


df3 = pd.concat([df1, df2], ignore_index=True) #puts both sp and nonsp data into one dataframe
#df3["ddos"] = df3["ddos"].apply(lambda x: -x)

hover = HoverTool(
        tooltips=[
            ('type','@type'),
            ('Energy','@energy'),
            ('DOS','$y')
        ]
    )

TOOLS = "box_zoom, pan, wheel_zoom, undo, redo, save, reset"

#plot = Line(df3, x="energy", y=["dos", "udos", "ddos"], xlabel="Energy (eV)", ylabel="Density of States", tools=TOOLS, active_drag="box_zoom", tooltips=tooltips)
p = figure(title=COMPOUND_NAME, x_axis_label=r"$E - E_F (eV)$", y_axis_label="Density of States", tools=[TOOLS, hover], 
    active_drag="box_zoom", x_range=(-10,10), y_range=(-15, 15))

line_width=2
cds1 = ColumnDataSource(df1)
cds2 = ColumnDataSource(df2)
p.line("energy","dos", legend="No spin polarization", line_color="#606060", line_dash="solid", line_width=line_width, source=cds1)
p.line("energy", "udos", legend="Spin-up", line_color="#28A0BA", line_dash="solid", line_alpha=0.8, line_width=line_width, source=cds2)
p.line("energy", "ddos", legend="Spin-down", line_color="#DB7C06", line_dash="solid", line_alpha=0.8, line_width=line_width, source=cds2)

x = arange(-10, 10, 0.1)
y = 0*x
p.line(x, y, line_color="black", line_dash="solid", line_width=1)

output_file("dostest.html")

show(p)





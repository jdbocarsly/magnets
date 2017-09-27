#!/usr/bin/env python

import pandas as pd
#from bokeh.charts import output_file, show, Line
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.models import DataRange1d as bmdr
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
# add a vertical line through the fermi level - DONE
# remove unused data from dataframes before making the column data sources
# remove hovertool from horizontal/vertical liness - DONE
# hover highlighting vertically


#df3 = pd.concat([df1, df2], ignore_index=True) #puts both sp and nonsp data into one dataframe
#df3["ddos"] = df3["ddos"].apply(lambda x: -x)

#hover = HoverTool(
#        tooltips=[
#            ('type','@type'),
#            ('Energy','@energy'),
#            ('DOS','$y')
#        ]
#    )

TOOLS = "box_zoom, pan, wheel_zoom, undo, redo, save, reset"

#plot = Line(df3, x="energy", y=["dos", "udos", "ddos"], xlabel="Energy (eV)", ylabel="Density of States", tools=TOOLS, active_drag="box_zoom", tooltips=tooltips)
p = figure(title=COMPOUND_NAME, x_axis_label=r"$E - E_F (eV)$", y_axis_label="Density of States", tools=[TOOLS], 
    active_drag="box_zoom", x_range=bmdr(start=-10, end=10, bounds=(-10,10)), y_range=bmdr(start=-15, end=15, bounds=(-15,15)))

line_width=2
cds1 = ColumnDataSource(df1)
cds2 = ColumnDataSource(df2)
p_nonsp = p.line("energy","dos", legend="No spin polarization", line_color="#606060", line_dash="solid", line_width=line_width, source=cds1)
p_up = p.line("energy", "udos", legend="Spin-up", line_color="#28A0BA", line_dash="solid", line_alpha=0.8, line_width=line_width, source=cds2)
p_down = p.line("energy", "ddos", legend="Spin-down", line_color="#DB7C06", line_dash="solid", line_alpha=0.8, line_width=line_width, source=cds2)

p_nonsp
p_up
p_down

hover_nonsp = HoverTool(
        tooltips=[
#            ('type','@type'),
            ('Energy','@energy'),
            ('DOS','@dos')
        ],
        renderers=[p_nonsp]
    )

hover_up = HoverTool(
        tooltips=[
#            ('type','@type'),
            ('Energy','@energy'),
            ('Spin-up DOS','@udos')
        ],
        renderers=[p_up]
    )

hover_down = HoverTool(
        tooltips=[
#            ('type','@type'),
            ('Energy','@energy'),
            ('Spin-down DOS','@ddos')
        ],
        renderers=[p_down]
    )
    
p.add_tools(hover_nonsp, hover_up, hover_down)

x_h = arange(-15, 15, 1)
y_h = 0*x_h
p.line(x_h, y_h, line_color="black", line_dash="solid", line_width=1)

y_v = arange(-20, 20, 1)
x_v = 0*y_v
p.line(x_v, y_v, line_color="black", line_dash="solid", line_width=1)

output_file("dostest.html")

show(p)





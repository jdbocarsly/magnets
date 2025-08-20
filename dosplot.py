#!/usr/bin/env python
from os.path import join as j

import pandas as pd
from bokeh.models import CrosshairTool
from bokeh.models import DataRange1d as bmdr
from bokeh.models import HoverTool
#from bokeh.charts import output_file, show, Line
from bokeh.plotting import ColumnDataSource, figure
from numpy import arange

#todo:
# custom HTML tooltips with title
# fix axis labels (subscripts?)
# add a vertical line through the fermi level - DONE
# remove unused data from dataframes before making the column data sources
# remove hovertool from horizontal/vertical liness - DONE
# hover highlighting vertically

TOOLS = "box_zoom, pan, crosshair,undo, redo, save, reset"

def create_dosplot(compound, atoms_per_unit_cell):
   path = j("dos_data",compound)
   df1 = pd.read_csv(j(path,"nonsp_dost.dat"), names=["energy", "dos","idos"], sep="\s+")
   df1["type"] = "nonsp"
   df2 = pd.read_csv(j(path,"sp_dost.dat"), names=["energy", "udos","ddos"], sep="\s+")
   df2["type"] = "sp"
   df2["ddos"] = -df2["ddos"]

   # convert to DOS/atom
   df1["dos"] = df1["dos"]/atoms_per_unit_cell
   df2["udos"] = df2["udos"]/atoms_per_unit_cell
   df2["ddos"] = df2["ddos"]/atoms_per_unit_cell

   p = figure(x_axis_label=r"E - Ef (eV)", y_axis_label="density of states (states/eV atom)", sizing_mode="stretch_width",
      tools=TOOLS,active_drag="box_zoom",
      x_range=bmdr(start=-5, end=5, bounds=(-10,10)),
      y_range=bmdr(start=-4, end=4, bounds=(-10,10))
      )
   p.toolbar.logo = "grey"
   line_width=2
   cds1 = ColumnDataSource(df1)
   cds2 = ColumnDataSource(df2)
   p_nonsp = p.line("energy","dos", legend="No spin polarization", line_color="#606060", line_dash="solid", line_width=line_width, source=cds1)
   p_up = p.line("energy", "udos", legend="Spin-up", line_color="#28A0BA", line_dash="solid", line_alpha=0.8, line_width=line_width, source=cds2)
   p_down = p.line("energy", "ddos", legend="Spin-down", line_color="#DB7C06", line_dash="solid", line_alpha=0.8, line_width=line_width, source=cds2)

   hover_nonsp = HoverTool(
      tooltips=[
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
         ('Energy','@energy'),
         ('Spin-down DOS','@ddos')
        ],
        renderers=[p_down]
    )
    
   p.add_tools(hover_nonsp, hover_up, hover_down)

   c = p.select(type=CrosshairTool)
   c.dimensions = "height"

   x_h = arange(-15, 15, 1)
   y_h = 0*x_h
   p.line(x_h, y_h, line_color="black", line_dash="solid", line_width=1)

   y_v = arange(-50, 50, 1)
   x_v = 0*y_v
   p.line(x_v, y_v, line_color="black", line_dash="solid", line_width=1)

   return p

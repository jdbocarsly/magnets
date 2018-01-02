#!/usr/bin/env python
from os.path import join as j
import pandas as pd
#from bokeh.charts import output_file, show, Line
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool, CrosshairTool
from bokeh.models import DataRange1d as bmdr
from numpy import arange

#todo:
# custom HTML tooltips with title
# fix axis labels (subscripts?)
# add a vertical line through the fermi level - DONE
# remove unused data from dataframes before making the column data sources
# remove hovertool from horizontal/vertical liness - DONE
# hover highlighting vertically

datatable_columns = [
'formula',
'class',
'Curie temperature (K)',
'−ΔSm(H = 2T) (J kg⁻¹ K⁻¹)',
'−ΔSm(H = 5T) (J kg⁻¹ K⁻¹)',
'gravimetric moment (emu/g)',
'moment per atom (µB/atom)',
'largest local moment (µB)',
'volumetric moment (emu/cm³)',
'theoretical density (g/cm³)'
]

def create_datatable(df):
  df = df[] 





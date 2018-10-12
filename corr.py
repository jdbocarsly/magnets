from itertools import product
from matplotlib import cm
import numpy as np
from matplotlib.colors import rgb2hex
from bokeh.plotting import figure, ColumnDataSource
from bokeh.palettes import magma
from bokeh.models import HoverTool, TapTool, OpenURL, ColorBar, LinearColorMapper
from bokeh.io import curdoc
from bokeh.themes import Theme

from bokeh.layouts import gridplot

HOVER_LINE_COLOR = "#b20340"##ffd400"

PI = 3.14159
FONTSIZE="10pt"
corr_style = {'attrs': {

    # apply defaults to Figure properties
    'Figure': {
        'toolbar_location': "right",
        'outline_line_color': None,
        'min_border_right': 10,
    },

    # apply defaults to Axis properties
    'Axis': {
        'axis_label_text_font': 'Helvetica',
        'axis_label_text_font_style':'normal',
        'axis_label_text_font_size': FONTSIZE,
        'major_tick_in': None,
        'minor_tick_out': None,
        'minor_tick_in': None,
        'axis_line_color': '#CAC6B6',
        'major_tick_line_color': '#CAC6B6',
        'major_label_text_font_size': FONTSIZE,
        'axis_label_standoff':15
    },

     # apply defaults to Legend properties
    'Legend': {
        'background_fill_alpha': 0.8,
    }
}}


def test():
   import pandas as pd
   from bokeh.plotting import show
   df = pd.read_pickle("clean_pickle.df")
   p = plot_corr(df)
   show(p)

def plot_corr(df, cmap_name="RdBu", method="pearson"):
   '''Function plots a graphical correlation matrix for each pair of columns in the dataframe.

   Input:
        df: pandas DataFrame
        cmap: string name of matplotlib colormap
        method: method for calculating correlation, one of: (pearson, spearman). Both 
           will be displayed in the tooltip, for now
   '''
   df = df.copy()
   #del df["cid"]
   cmap  = cm.get_cmap(name=cmap_name)
   # cmap takes a value between 0 and 1. We want to make it take a value between -1 and 1
   cmapX = lambda x: rgb2hex(cmap((x+1)/2))

   corrP = df.corr(method="pearson")
   corrS = df.corr(method="spearman")

   cols = list(corrP.columns)
   coordinates = list(product(cols, cols))
   x,y  = zip(*coordinates)
   #print(coordinates)

   pearson  = [corrP[i][j] for i,j in coordinates]
   spearman = [corrS[i][j] for i,j in coordinates]
   selected_corr = pearson if method=="pearson" else spearman

   colors   = [cmapX(x) for x in selected_corr]

   source = ColumnDataSource(dict(x=x,y=y,color=colors,pearson=pearson,spearman=spearman))

   # change plot width to make it look more suqare if changing the number of columns included!
   p = figure(tools="hover, tap", toolbar_location=None,
            x_range=cols, y_range=list(reversed(cols)),plot_height=900, plot_width=1075,
           sizing_mode='scale_height')
   curdoc().theme = Theme(json=corr_style)
   p.toolbar.logo = None
   p.toolbar_location = None

   p.xaxis.major_label_orientation = PI / 4
   p.rect("x", "y", color="color", width=1, height=1,source=source,
      name="rects", line_color=None,line_width=4,
      hover_line_color=HOVER_LINE_COLOR, hover_fill_color="color")
   p.line([2.5,2.5],[0,len(cols)+0.5],line_color="black",line_dash="solid",line_width=2) # vert line
   p.line([0,len(cols)+0.5],[len(cols)-1.5,len(cols)-1.5],line_color="black",line_dash="solid",line_width=2) # vert line


   colors = [cmapX(x) for x in np.linspace(-1,1,256)] 
   cbar_mapper = LinearColorMapper(palette=colors,low=-1,high=1)
   color_bar = ColorBar(color_mapper=cbar_mapper, major_label_text_font_size="12pt",
                     label_standoff=12, border_line_color=None, location=(0,0),
                     title_text_font_style="italic", title_text_font_size="14pt", title="\tr", title_text_align="left")
   p.add_layout(color_bar, 'right')
   hover = p.select(type=HoverTool)
   nums = list(range(len(coordinates)))
   hover.tooltips = [
   ("correlation","$x vs. $y"),
   ("Spearman's r","@spearman"),
   ("Pearson's r", "@pearson")
   ]

   #to avoid weird taptool behavior
   renderer = p.select(name="rects")[0]
   renderer.nonselection_glyph=renderer.glyph
   taptool = p.select(type=TapTool)
   taptool.callback = OpenURL(url="/?x_axis=@x&y_axis=@y&color_axis=@y")

   #plot = gridplot([[p]], sizing_mode='scale_height')
   return p

if __name__ == '__main__':
   test()


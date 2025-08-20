from bokeh.models import HoverTool, OpenURL, TapTool, LinearColorMapper,ColorBar
from bokeh.models import HoverTool, OpenURL, TapTool, CustomJS, LinearColorMapper,ColorBar
from bokeh.palettes import Plasma256, brewer
from bokeh.plotting import curdoc, figure, ColumnDataSource
from bokeh.themes import Theme

import resources

def main_plot(df, x_axis, y_axis,color):
   source = ColumnDataSource(df)

   print(type(x_axis), type(y_axis))
   #xs = df[x.value]
   #ys = df[y.value]

   kw=dict()

   if x_axis in resources.discrete_columns.keys():
      kw['x_range'] = resources.discrete_columns[x_axis]
   if y_axis in resources.discrete_columns:
      kw['y_range'] = resources.discrete_columns[y_axis]

   p = figure(plot_height=600, plot_width=800, sizing_mode="scale_width", tools=resources.TOOLS, 
      **kw)
   #title="{} vs. {}".format(y_axis,x_axis) # add to figure() call to use bokeh title
   curdoc().theme = Theme(json=resources.style)
   #p.toolbar.active_drag = None # no boxzoom: todo: ONLY FOR MOBILE

   p.xaxis.axis_label = x_axis
   p.yaxis.axis_label = y_axis

   print(kw)
   sz = 12
   # if size.value != 'None':
   #    groups = pd.qcut(df[size.value].values, len(SIZES))
   #    sz = [SIZES[xx] for xx in groups.codes]

   #c = "#31AADE"
   #if color != 'None':
   #   groups = pd.qcut(df[color].values, len(COLORS))
   #c = [COLORS[x] for x in groups.codes]



   #for categorical data, 
   if color in resources.discrete_columns.keys():
      items = resources.discrete_columns[color]
      c = brewer['Dark2'][len(items)]
      for i, item in enumerate(items):
         df2 = df[df[color]==item]
         source2 = ColumnDataSource(df2)
         print(df2)
         p.circle(x_axis, y_axis, color=c[i],
            size=sz, line_color=c[i], alpha=0.5, hover_alpha=1, hover_line_color="#ff7044",
            line_width=1.5, name="circs_{}".format(i), line_alpha=1, legend=item,muted_alpha=0.05, source=source2)

         #to avoid weird taptool behavior
         renderer = p.select(name="circs_{}".format(i))[0]
         renderer.nonselection_glyph=renderer.glyph


   else:
      # for non categorical, use a color transform
      colormapper = LinearColorMapper(palette="Plasma256",low=df[color].min(), high=df[color].max())
      color_attr = {'field':color, 'transform': colormapper}
      p.circle(x_axis, y_axis, color=color_attr,
         size=sz, line_color=color_attr, alpha=0.2,
         hover_alpha=1, hover_line_color="#ff7044",source=source,
         line_width=1.5,name="circs",line_alpha=1)
      color_bar = ColorBar(color_mapper=colormapper, major_label_text_font_size=resources.FONTSIZE,
                     label_standoff=12, border_line_color=None, location=(0,0))
      p.add_layout(color_bar,"right")
   
      #to avoid weird taptool behavior
      renderer = p.select(name="circs")[0]
      renderer.nonselection_glyph=renderer.glyph

   hover = p.select(type=HoverTool)
   hover.tooltips = [
   ("compound","@formula"),
   ("class","@class"),
   ("Tc", "@{Curie temperature (K)}")
   ]

   taptool = p.select(type=TapTool)
   taptool.callback = OpenURL(url="/c/@cid")

   p.toolbar.logo = "grey"
   return p
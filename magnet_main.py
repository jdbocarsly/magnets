import numpy as np
import pandas as pd
import resources
from ashby import main_plot
from bokeh.embed import components
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models import (ColorBar, CustomJS, HoverTool, LinearColorMapper,
                          OpenURL, TapTool)
from bokeh.palettes import Magma256, Plasma256, Viridis256, brewer
from bokeh.plotting import ColumnDataSource, curdoc, figure
from bokeh.themes import Theme
from corr import plot_corr
from dosplot import create_dosplot
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

df = pd.read_pickle("clean_pickle2.df")
df["formula_nosubs"] = df["formula"]
df["formula_html"]=[resources.make_html_subscripts(f) for f in df["formula"]]
df["formula"] = [resources.make_unicode_subscripts(name) for name in df["formula"]]
df["class"] = df["class"].fillna("classless")



#print(df["class"])
# cols = sorted(df.columns)


@app.route('/')
@app.route('/ashby')
def ashby():
   xprm = request.args.get("x_axis")
   if xprm == None:
      xprm = "Curie temperature (K)"

   yprm = request.args.get("y_axis")
   if yprm == None:
      yprm = "volumetric moment (emu/cm³)"

   cprm = request.args.get("color_axis")
   if cprm == None:
      cprm = "largest local moment (µB)"

   plot = main_plot(df, xprm, yprm,cprm)
   script, div = components(plot)

   return render_template("ashby.html", script=script, div=div,
      cols=resources.axis_columns, curr_x=xprm, curr_y=yprm, curr_c=cprm, col_groups=resources.axis_columns_groups,
      color_cols=resources.axis_columns_groups)

@app.route('/c/<int:cid>')
def single_compound_view(cid):
   if cid >= len(df): return index()
   c = df.iloc[cid]
   #c = c.dropna()
   # vals = ["{:.2f}".format(c[x]) if isinstance(c[x], (np.floating, float)) else c[x] for x in resources.dos_cols]

   groups_with_vals = []
   for category_name, parameters in resources.dos_columns_groups:
      # sorry about this line. The end is to filter out delta Sm labels from showing up at NaN if the data is not available
      parameters = [x for x in parameters if not (isinstance(c[x], (np.floating, float)) and np.isnan(c[x]))]

      vals = ["{:.2f}".format(c[x]) if isinstance(c[x], (np.floating, float)) else c[x] for x in parameters] 
      print('\n',category_name,'\n')
      [print(g,v) for g,v in zip(parameters,vals)]
      groups_with_vals.append( (category_name, list(zip(parameters, vals))) )

   # [print(x) for x in groups_with_vals]
   plot = create_dosplot(df.iloc[cid]["material_name"], df.iloc[cid]["natoms"])
   script, div = components(plot)
   return render_template("dos.html",script=script, div=div,formula=c["formula_html"],dos_columns_groups=groups_with_vals)

@app.route('/correlations')
def corr_page():
   plot = plot_corr(df[resources.corr_cols])
   script, div = components(plot)
   return render_template("corr.html",script=script, div=div)

@app.route('/about')
def about():
  return render_template("about.html")

@app.route('/datatable')
def table_page():
  df_rounded = df.round(
    {"Curie temperature (K)":0,
    "gravimetric moment (emu/g)":1,
    "largest local moment (µB)":2,
    })

  df_rounded = df_rounded.fillna("")
  print(df_rounded.head())
  return render_template("datatable.html", df=df_rounded.iterrows())

if __name__ == '__main__':
   app.run(debug=True, port=5005)

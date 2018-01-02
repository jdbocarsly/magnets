from flask import Flask, render_template, request, url_for
import numpy as np
import pandas as pd
from bokeh.layouts import row, widgetbox
from bokeh.models import HoverTool, OpenURL, TapTool, CustomJS, LinearColorMapper,ColorBar
from bokeh.palettes import Viridis256, Magma256, Plasma256, brewer
from bokeh.plotting import curdoc, figure, ColumnDataSource
from bokeh.embed import components
from bokeh.io import curdoc
from bokeh.themes import Theme

from dosplot import create_dosplot
from corr import plot_corr

trans = str.maketrans('0123456789.-','₀₁₂₃₄₅₆₇₈₉.₋')

def make_subscripts(string):
   return string.translate(trans)
FONTSIZE="14pt"
TYPEFACE = "Lato"
style = {'attrs': {

    # apply defaults to Figure properties
    'Figure': {
        'toolbar_location': "above",
        'outline_line_color': None,
        'min_border_right': 10,
    },
    'Title': {
    'text_font_size':FONTSIZE,
    'text_font_style':'bold',
    'text_font': TYPEFACE,
    },

    # apply defaults to Axis properties
    'Axis': {
        'axis_label_text_font': TYPEFACE,
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



app = Flask(__name__)

df = pd.read_pickle("clean_pickle.df")
#df = pd.read_csv("magnet_database.csv")
df["formula_nosubs"] = df["formula"]
df["formula"] = [make_subscripts(name) for name in df["formula"]]
df["class"] = df["class"].fillna("classless")

df_rounded = df.round(
    {"Curie temperature (K)":0,
    "gravimetric moment (emu/g)":1,
    "largest local moment (µB)":2,
    })


print(df["class"])
source = ColumnDataSource(df)
cols = sorted(df.columns)

SIZES = list(range(6, 22, 3))
COLORS = Plasma256
TOOLS="box_zoom, reset, hover,tap"

dos_cols = [
"Curie temperature (K)",
"−ΔSm(H = 2T) (J kg⁻¹ K⁻¹)",
"−ΔSm(H = 5T) (J kg⁻¹ K⁻¹)",
"magnetic deformation (Σm), %",
"largest local moment (µB)",
"gravimetric moment (emu/g)",
"volumetric moment (emu/cm³)",
"moment per atom (µB/atom)",
"energy of spin-polarization (eV/atom)",
"theoretical density (g/cm³)",
"source (experimental)",
]
axis_columns = [
"class",
"element carrying largest moment",
"−ΔSm(H = 2T) (J kg⁻¹ K⁻¹)",
"−ΔSm(H = 5T) (J kg⁻¹ K⁻¹)",
"Curie temperature (K)",
"gravimetric moment (emu/g)",
"volumetric moment (emu/cm³)",
"moment per atom (µB/atom)",
"largest local moment (µB)",
"theoretical density (g/cm³)",
"energy of spin-polarization (eV/atom)",
"magnetic volume change (%)",
"magnetic deformation (Σm), %",
"Σm x gravimetric moment",

]

discrete_columns = {
'element carrying largest moment':["Cr","Mn","Fe","Co","Ni"],
'class':["heusler","perovskite","antiperovskite","Co2P","MnAs"],
}


def main_plot(x_axis, y_axis,color):
   print(type(x_axis), type(y_axis))
   #xs = df[x.value]
   #ys = df[y.value]

   kw=dict()

   if x_axis in discrete_columns.keys():
      kw['x_range'] = discrete_columns[x_axis]
   if y_axis in discrete_columns:
      kw['y_range'] = discrete_columns[y_axis]

   p = figure(plot_height=600, plot_width=800, responsive=True, tools=TOOLS,
      title="{} vs. {}".format(y_axis,x_axis), **kw)
   curdoc().theme = Theme(json=style)
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
   if color in discrete_columns.keys():
      items = discrete_columns[color]
      c = brewer['Dark2'][len(items)]
      for i, item in enumerate(items):
         df2 = df[df[color]==item]
         p.circle(df2[x_axis], df2[y_axis], color=c[i],
            size=sz, line_color=c[i], alpha=0.5, hover_alpha=1, hover_line_color="#ff7044",
            line_width=1.5, name="circs_{}".format(i), line_alpha=1, legend=item,muted_alpha=0.05)
      p.legend.click_policy="mute"
   


   else:
      # for non catecorical, use a color transform
      colormapper = LinearColorMapper(palette="Plasma256",low=df[color].min(), high=df[color].max())
      color_attr = {'field':color, 'transform': colormapper}
      p.circle(x_axis, y_axis, color=color_attr,
         size=sz, line_color=color_attr, alpha=0.2,
         hover_alpha=1, hover_line_color="#ff7044",source=source,
         line_width=1.5,name="circs",line_alpha=1)
      color_bar = ColorBar(color_mapper=colormapper, major_label_text_font_size=FONTSIZE,
                     label_standoff=12, border_line_color=None, location=(0,0))
      p.add_layout(color_bar,"right")
   
   #to avoid weird taptool behavior
   #renderer = p.select(name="circs")[0]
   #renderer.nonselection_glyph=renderer.glyph

   hover = p.select(type=HoverTool)
   hover.tooltips = [
   ("compound","@formula"),
   ("class","@class"),
   ("Tc", "@{Curie temperature (K)}")
   ]

   taptool = p.select(type=TapTool)
   taptool.callback = OpenURL(url="/c/@cid")

   p.toolbar.logo = "grey"

#    df["url"] = [url_for("single_compound_view", cid=c) for c in df["cid"]]
#    code = """
#    console.log("pressed ")
# selection = require("core/util/selection")
# indices = selection.get_indices(source)
# for (i = 0; i < indices.length; i++) {
#    ind = indices[i]
#    url = source.data['url'][ind]
#    window.open(url, "_self")
# }
# """
#    callback = CustomJS(args=dict(source=source), code=code)
#    taptool = p.select(type=TapTool)
#    taptool.callback = callback
#    print(callback)
   return p


@app.route('/')
@app.route('/ashby')
def ashby():
   xprm = request.args.get("x_axis")
   if xprm == None:
      xprm = "Curie temperature (K)"

   yprm = request.args.get("y_axis")
   if yprm == None:
      yprm = "magnetic deformation (Σm), %"

   cprm = request.args.get("color_axis")
   if cprm == None:
      cprm = "−ΔSm(H = 5T) (J kg⁻¹ K⁻¹)"

   plot = main_plot(xprm, yprm,cprm)
   script, div = components(plot)

   return render_template("ashby.html", script=script, div=div,
      cols=axis_columns, curr_x=xprm, curr_y=yprm, curr_c=cprm,
      color_cols=axis_columns)

@app.route('/c/<int:cid>')
def single_compound_view(cid):
   if cid >= len(df): return index()
   c = df.iloc[cid]
   #c = c.dropna()
   vals = ["{:.2f}".format(c[x]) if isinstance(c[x], (np.floating, float)) else c[x] for x in dos_cols]
   plot = create_dosplot(df.iloc[cid]["material_name"])
   script, div = components(plot)
   return render_template("dos.html",script=script, div=div,formula=c["formula"],c_atts=zip(dos_cols,vals))

@app.route('/correlations')
def corr_page():
   plot = plot_corr(df[axis_columns])
   script, div = components(plot)
   return render_template("corr.html",script=script, div=div)

@app.route('/about')
def about():
  return render_template("about.html")

@app.route('/datatable')
def table_page():
  #table_page()
  return render_template("datatable.html", df=df_rounded.iterrows())

if __name__ == '__main__':
   app.run(debug=True)


"""Serialize the eight existing Ashby plot structures for browser selection."""
from itertools import product

from bokeh.embed import json_item
from bokeh.models import Circle, LinearColorMapper
from bokeh.themes import Theme

from .ashby import main_plot
from . import resources

DEFAULTS = ['Curie temperature (K)', 'volumetric moment (emu/cm³)',
            'largest local moment (µB)']


def make_payload(df, site_root):
    # Only class is categorical in the existing dropdowns. Other classes and
    # their existing omission when coloring by class are deliberately unchanged.
    fields = list(dict.fromkeys(field for _, group in resources.axis_columns_groups
                                for field in group))
    stats = {field: [float(df[field].min()), float(df[field].max())]
             for field in fields if field not in resources.discrete_columns}
    templates = {}
    for categorical in product((False, True), repeat=3):
        selected = ['class' if cat else default
                    for cat, default in zip(categorical, DEFAULTS)]
        plot = main_plot(df, *selected, compound_url=f'{site_root}c/@cid/')
        entry = {
            # Flask components() created a fresh, default-themed document;
            # curdoc().theme in main_plot never reached the embedded figure.
            'item': json_item(plot, 'ashby-plot', theme=Theme(json={})),
            'axes': [plot.xaxis[0].id, plot.yaxis[0].id],
            'glyphs': [model.id for model in plot.select({'type': Circle})],
            'mappers': [model.id for model in plot.select({'type': LinearColorMapper})],
        }
        templates[''.join('c' if cat else 'n' for cat in categorical)] = entry
    return {'templates': templates, 'defaults': DEFAULTS, 'fields': fields,
            'categories': resources.discrete_columns, 'stats': stats}

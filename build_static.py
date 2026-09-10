"""Build the committed GitHub Pages site: uv run python build_static.py."""
import argparse
import json
import os
import re
from pathlib import Path
from urllib.parse import urlencode

# Avoid an unwritable global font cache in restricted environments.
os.environ.setdefault('MPLCONFIGDIR', str(Path(__file__).resolve().parent / '.mpl-cache'))

import pandas as pd
from bokeh.embed import components
from bokeh.models import CustomJS, TapTool
from bokeh.themes import Theme
from jinja2 import Environment, FileSystemLoader, select_autoescape

from ashby_static import DEFAULTS, make_payload
from corr import plot_corr
from dosplot import create_dosplot
import resources
from site_data import ROOT, counts, display_data, load_data, MISSING_DOS


def property_groups(row):
    groups = []
    for category, fields in resources.dos_columns_groups:
        values = [(field, f'{row[field]:.2f}' if isinstance(row[field], float) else row[field])
                  for field in fields if pd.notna(row[field])]
        groups.append((category, values))
    return groups


def source_links(value):
    """Repair only unambiguous relative DOI hrefs; keep visible citation text."""
    def replace(match):
        href = match.group(1)
        if href.startswith(('dx.doi.org/', 'doi.org/')):
            href = 'https://' + href
        elif href.startswith('10.'):
            href = 'https://doi.org/' + href
        return 'href="' + href + '"'
    return re.sub(r'href="([^"]+)"', replace, value)


def safe_json(value):
    # Prevent embedded source text from closing the containing script element.
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False).replace('<', '\\u003c')


def build(output=ROOT):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    source = load_data()
    df = display_data(source)
    # Repair links only in property-table output; retain original source strings
    # in plot data so scientific input and the original Bokeh documents agree.
    total, magnetocaloric = counts(source)
    env = Environment(loader=FileSystemLoader(ROOT / 'templates'),
                      autoescape=select_autoescape(['html']))
    generated = []

    def write(path, content):
        target = output / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.read_text() != content:
            target.write_text(content, encoding='utf-8')
        generated.append(path)

    def render(path, template, **context):
        depth = len(Path(path).parts) - 1
        site_root = '../' * depth if depth else './'
        html = env.get_template(template).render(
            site_root=site_root, compound_count=total,
            magnetocaloric_count=magnetocaloric,
            url_for=lambda endpoint, filename: site_root + 'static/' + filename,
            **context)
        write(path, html)

    for path, site_root in [('index.html', './'), ('ashby/index.html', '../')]:
        payload = make_payload(df, site_root)
        render(path, 'ashby.html', script='', div='<div id="ashby-plot"></div>',
               col_groups=resources.axis_columns_groups,
               curr_x=DEFAULTS[0], curr_y=DEFAULTS[1], curr_c=DEFAULTS[2],
               swap_query=urlencode(dict(zip(['x_axis', 'y_axis', 'color_axis'],
                                            [DEFAULTS[1], DEFAULTS[0], DEFAULTS[2]]))),
               ashby_payload=safe_json(payload))

    plot = plot_corr(df[resources.corr_cols])
    plot.select_one(TapTool).callback = CustomJS(code="""
        const source = cb_data.source;
        const i = source.selected.indices[0];
        if (i === undefined) return;
        const query = new URLSearchParams({x_axis: source.data.x[i],
            y_axis: source.data.y[i], color_axis: source.data.y[i]});
        window.open('../?' + query.toString(), '_blank');
    """)
    script, div = components(plot, theme=Theme(json={}))
    render('correlations/index.html', 'corr.html', script=script, div=div)
    table = df.round({'Curie temperature (K)': 0, 'gravimetric moment (emu/g)': 1,
                      'largest local moment (µB)': 2}).fillna('')
    render('datatable/index.html', 'datatable.html', df=table.iterrows())
    render('about/index.html', 'about.html')

    for _, row in df.iterrows():
        unavailable = MISSING_DOS.get(row.cid) == row.material_name
        script, div = '', ''
        if not unavailable:
            plot = create_dosplot(row.material_name, row.natoms)
            # Match Flask components(), which embedded an unthemed document.
            script, div = components(plot, theme=Theme(json={}))
        display_row = row.copy()
        display_row['source (experimental)'] = source_links(row['source (experimental)'])
        render(f'c/{row.cid}/index.html', 'dos.html', script=script, div=div,
               formula=row.formula_html, dos_columns_groups=property_groups(display_row),
               dos_unavailable=unavailable)

    write('.nojekyll', '')
    manifest = output / 'generated-pages.json'
    if manifest.exists():
        for stale in set(json.loads(manifest.read_text())) - set(generated):
            # Only the exact former per-compound output is eligible for pruning.
            import re
            if re.fullmatch(r'c/\d+/index\.html', stale):
                (output / stale).unlink(missing_ok=True)
    manifest.write_text(json.dumps(sorted(generated), indent=2) + '\n')
    print(f'Built {len(generated) - 1} HTML pages: {total} compounds, {magnetocaloric} magnetocalorics.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT)
    args = parser.parse_args()
    build(args.output)

"""Run with uv run python -m unittest discover -s tests -v.

The baseline is the preserved working-tree commit, not the migrated plotting
implementation. Node is used only to execute the actual browser transformation.
"""
import base64
import ast
from contextlib import redirect_stdout
from contextlib import redirect_stderr
from html.parser import HTMLParser
from html import unescape
import io
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import types
import unittest
from urllib.parse import unquote, urljoin, urlparse
import warnings

os.environ.setdefault('MPLCONFIGDIR', str(Path(__file__).resolve().parents[1] / '.mpl-cache'))

import numpy as np
import pandas as pd
from bokeh.embed import json_item
from bokeh.models import CustomJS, OpenURL, TapTool
from bokeh.util.warnings import BokehDeprecationWarning
import matplotlib
from matplotlib import cm

from ashby_static import DEFAULTS, make_payload
from build_static import property_groups
from site_data import ROOT, counts, display_data, load_data
from scripts.check_rebuild import canonical_document
import resources

BASELINE = '05720c8'
warnings.filterwarnings('ignore', category=BokehDeprecationWarning)


def baseline_module(filename):
    source = subprocess.check_output(['git', 'show', f'{BASELINE}:{filename}'],
                                     cwd=ROOT, text=True)
    module = types.ModuleType('baseline_' + filename[:-3])
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', DeprecationWarning)
        exec(compile(source, filename, 'exec'), module.__dict__)
    return module


def decode(value):
    if isinstance(value, dict) and '__ndarray__' in value:
        return np.frombuffer(base64.b64decode(value['__ndarray__']),
                             dtype=value['dtype']).reshape(value['shape'])
    return np.asarray(value)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.scripts = {}
        self.script = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('src', 'href'):
            if key in attrs:
                self.links.append(attrs[key])
        if tag == 'script' and attrs.get('type') == 'application/json':
            self.script = attrs['id']
            self.scripts[self.script] = ''

    def handle_data(self, data):
        if self.script:
            self.scripts[self.script] += data

    def handle_endtag(self, tag):
        if tag == 'script':
            self.script = None


class StaticParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = load_data()
        cls.df = display_data(cls.raw)

    def test_data_preservation(self):
        original = pd.read_pickle(ROOT / 'clean_pickle3.df')
        expected = original.loc[original.cid != 7].reset_index(drop=True)
        pd.testing.assert_frame_equal(expected, self.raw, check_exact=True)
        self.assertEqual(counts(self.raw), (165, 33))
        self.assertNotIn(7, set(self.raw.cid))
        self.assertIn(139, set(self.raw.cid))

    def test_every_axis_and_color_against_original_python(self):
        old = baseline_module('ashby.py')
        payload = make_payload(self.df, './')
        cases = set()
        # Every selectable field in each role, plus all eight structures and
        # numeric recoloring with both categorical axes.
        for role in range(3):
            for field in payload['fields']:
                values = DEFAULTS.copy()
                values[role] = field
                cases.add(tuple(values))
        from itertools import product
        for categorical in product((False, True), repeat=3):
            cases.add(tuple('class' if cat else DEFAULTS[i]
                            for i, cat in enumerate(categorical)))
        for field in payload['stats']:
            cases.add(('class', 'class', field))
        fixture = {'payload': payload, 'cases': []}
        for fields in sorted(cases):
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                plot = old.main_plot(self.df, *fields)
            plot.select_one(TapTool).callback = OpenURL(url='./c/@cid/')
            fixture['cases'].append({'fields': fields, 'expected': json_item(plot)})
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'ashby.json'
            path.write_text(json.dumps(fixture))
            subprocess.run(['node', str(ROOT / 'tests/check_ashby.js'), str(path)], check=True)

    def test_browser_event_handlers(self):
        subprocess.run(['node', str(ROOT / 'tests/check_controls.js')], check=True)

    def test_property_precision_and_missing_values(self):
        for _, row in self.df.iterrows():
            groups = property_groups(row)
            for (_, fields), (_, output) in zip(resources.dos_columns_groups, groups):
                self.assertEqual([field for field in fields if pd.notna(row[field])],
                                 [field for field, _ in output])
                for field, value in output:
                    expected = f'{row[field]:.2f}' if isinstance(row[field], float) else row[field]
                    self.assertEqual(value, expected)

    def test_detail_and_correlation_plot_structure(self):
        old_dos = baseline_module('dosplot.py')
        old_corr = baseline_module('corr.py')
        # Restore the removed alias only within the baseline module. The named
        # palette is identical; no plot parameters or data are changed.
        old_corr.cm = types.SimpleNamespace(get_cmap=lambda name: matplotlib.colormaps[name])
        for cid in (None, 0, 8, 139):
            path = ROOT / ('correlations/index.html' if cid is None else f'c/{cid}/index.html')
            literal = re.search(r"const docs_json = ('.*');", path.read_text()).group(1)
            doc = next(iter(json.loads(unescape(ast.literal_eval(literal))).values()))
            with redirect_stderr(io.StringIO()):
                if cid is None:
                    plot = old_corr.plot_corr(self.df[resources.corr_cols])
                    code = next(ref['attributes']['code'] for ref in doc['roots']['references']
                                if ref['type'] == 'CustomJS')
                    plot.select_one(TapTool).callback = CustomJS(code=code)
                else:
                    row = self.df.loc[self.df.cid == cid].iloc[0]
                    plot = old_dos.create_dosplot(row.material_name, row.natoms)
            self.assertEqual(canonical_document(doc), canonical_document(json_item(plot)['doc']))

    def test_generated_pages_assets_and_prefixes(self):
        manifest = json.loads((ROOT / 'generated-pages.json').read_text())
        self.assertEqual(sum(path.endswith('.html') for path in manifest), 170)
        self.assertNotIn('c/7/index.html', manifest)
        self.assertIn('c/139/index.html', manifest)
        for path in manifest:
            if not path.endswith('.html'):
                continue
            parser = PageParser()
            parser.feed((ROOT / path).read_text())
            for prefix in ('/', '/magnets/'):
                base = 'https://example.test' + prefix + path.removesuffix('index.html')
                for link in parser.links:
                    parsed = urlparse(urljoin(base, link))
                    if parsed.netloc != 'example.test':
                        continue
                    # Existing source citations with malformed hrefs must not
                    # accidentally become broken local links.
                    self.assertTrue(parsed.path.startswith(prefix), (path, link))
                    relative = unquote(parsed.path[len(prefix):])
                    target = ROOT / relative
                    if parsed.path.endswith('/'):
                        target = target / 'index.html'
                    self.assertTrue(target.is_file(), (path, link, str(target)))

    def test_generated_correlation_and_dos_values(self):
        for cid in [None] + self.df.cid.tolist():
            page = ROOT / ('correlations/index.html' if cid is None else f'c/{cid}/index.html')
            parser = PageParser()
            parser.feed(page.read_text())
            if cid == 37:
                self.assertFalse(parser.scripts)
                self.assertIn('Density-of-states data unavailable.', page.read_text())
                continue
            literal = re.search(r"const docs_json = ('.*');", page.read_text()).group(1)
            doc = next(iter(json.loads(unescape(ast.literal_eval(literal))).values()))
            sources = [ref['attributes']['data'] for ref in doc['roots']['references']
                       if ref['type'] == 'ColumnDataSource']
            if cid is None:
                source = next(data for data in sources if 'pearson' in data)
                for method in ('pearson', 'spearman'):
                    corr = self.df[resources.corr_cols].corr(method=method)
                    expected = [corr[x][y] for x, y in zip(source['x'], source['y'])]
                    np.testing.assert_allclose(decode(source[method]), expected, rtol=0, atol=0)
                continue
            row = self.df.loc[self.df.cid == cid].iloc[0]
            folder = ROOT / 'dos_data' / row.material_name
            nonsp = np.loadtxt(folder / 'nonsp_dost.dat')
            sp = np.loadtxt(folder / 'sp_dost.dat')
            actual_nonsp = next(data for data in sources if 'idos' in data)
            actual_sp = next(data for data in sources if 'udos' in data)
            for actual, expected in [
                (actual_nonsp['energy'], nonsp[:, 0]),
                (actual_sp['energy'], sp[:, 0]),
                (actual_nonsp['dos'], nonsp[:, 1] / row.natoms),
                (actual_sp['udos'], sp[:, 1] / row.natoms),
                (actual_sp['ddos'], -sp[:, 2] / row.natoms),
            ]:
                np.testing.assert_allclose(decode(actual), expected, rtol=1e-14, atol=1e-14)


if __name__ == '__main__':
    unittest.main()

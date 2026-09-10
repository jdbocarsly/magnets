"""Rebuild in a temporary directory and compare semantic page output."""
import ast
from html import unescape
import json
from pathlib import Path
import re
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from magnet_site.build import build
from magnet_site.paths import ROOT, OUTPUT


def canonical_document(doc):
    refs = {ref['id']: ref for ref in doc['roots']['references']}
    assigned, models = {}, []

    def visit(value):
        if isinstance(value, list):
            return [visit(child) for child in value]
        if isinstance(value, dict):
            if set(value) == {'id'} and value['id'] in refs:
                key = value['id']
                if key not in assigned:
                    assigned[key] = len(models)
                    models.append(None)
                    ref = refs[key]
                    models[assigned[key]] = [ref['type'], visit(ref['attributes'])]
                return {'ref': assigned[key]}
            return {key: visit(value[key]) for key in sorted(value)}
        return value

    roots = [visit({'id': key}) for key in doc['roots']['root_ids']]
    return {'roots': roots, 'models': models, 'version': doc['version']}


def canonical_page(path):
    return canonical_html(path.read_text())


def canonical_html(html):
    documents = []
    pattern = r'(<script type="application/json" id="ashby-data">)(.*?)(</script>)'
    match = re.search(pattern, html, re.S)
    if match:
        payload = json.loads(match[2])
        for key, entry in sorted(payload['templates'].items()):
            documents.append([key, canonical_document(entry['item']['doc'])])
        # Graph IDs in the role metadata vary along with the documents. The
        # main parity suite validates that those role mappings produce exactly
        # the independently generated Python plots.
        payload['templates'] = '<documents>'
        html = html[:match.start(2)] + json.dumps(payload, sort_keys=True) + html[match.end(2):]
    match = re.search(r"const docs_json = ('.*');", html)
    if match:
        for doc in json.loads(unescape(ast.literal_eval(match[1]))).values():
            documents.append(canonical_document(doc))
        html = html[:match.start(1)] + "'<documents>'" + html[match.end(1):]
        html = re.sub(r'const render_items = .*;', 'const render_items = <items>;', html)
        html = re.sub(r'data-root-id="\d+"', 'data-root-id="<root>"', html)
        html = re.sub(r'id="[0-9a-f-]{36}"', 'id="<element>"', html)
    return html, documents


def main():
    manifest = json.loads((OUTPUT / 'generated-pages.json').read_text())
    with tempfile.TemporaryDirectory(prefix='magnets-rebuild-') as temporary:
        output = Path(temporary)
        build(output)
        assert json.loads((output / 'generated-pages.json').read_text()) == manifest
        for name in manifest:
            if name.endswith('.html'):
                assert canonical_page(OUTPUT / name) == canonical_page(output / name), name
            else:
                assert (OUTPUT / name).read_bytes() == (output / name).read_bytes(), name
    print('Rebuild matches all 170 pages and copied assets (ignoring incidental Bokeh identifiers/order).')


if __name__ == '__main__':
    main()

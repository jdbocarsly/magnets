A website for visualizing data from:

 J.D. Bocarsly, E.E. Levin, C.A.C. Garcia, K. Schwennicke, S.D. Wilson, R. Seshadri, A Simple Computational Proxy for Screening Magnetocaloric Compounds, *Chem. Mater.* **29** (2017) 1613−1622. [doi](https://doi.org/10.1021/acs.chemmater.6b04729)


The website is static HTML with standalone Bokeh 2.4.3 plots. Generated pages
are committed, so previewing or hosting does not require Flask or a build.

## Preview

From the repository root:

```sh
python3 -m http.server 8000
```

Open <http://localhost:8000/>. Use an HTTP server rather than opening files
directly. Bokeh, Bootstrap, DataTables, jQuery and fonts retain their existing
CDN versions, so the browser needs an internet connection.

## Rebuild after a source change

Install [uv](https://astral.sh/uv), then run:

```sh
uv run --locked python build_static.py
```

uv installs the locked Python 3.10 build environment on first use. Subsequent
builds use that environment. Commit the changed source and generated pages
together. `generated-pages.json` lists the builder-owned output. Rebuilding
may change incidental Bokeh model IDs even when content is equivalent.

The canonical input is [data/magnets.csv](data/magnets.csv); the cleanup is
documented in [data/README.md](data/README.md). It contains 165 compounds,
including 33 with magnetocaloric measurements. Co5Y retains its property page
but has no DOS source files. Existing IDs are preserved, with ID 7 removed.

Python renders Jinja templates and standalone plots. On the Ashby page,
JavaScript selects one of eight Python-generated plot structures, substitutes
the requested axes/color, and embeds a fresh Bokeh document. This preserves
the original plot structure and reset behavior without a server. DOS data is
embedded only in each compound's detail page.

The original scientific preparation scripts and historical data exports are
retained for reference. Routine builds do not run those scripts or require
their scientific-analysis dependencies. Flask, Gunicorn and Docker deployment
have been removed; their baseline is preserved in commit `05720c8`.

## Verify

With Node.js available for the JavaScript checks:

```sh
uv run --locked python -m unittest discover -s tests -v
uv run --locked python scripts/check_rebuild.py
```

The tests compare browser-side plot documents to the original Python plotting
code at `05720c8`, check retained data and every DOS series, verify controls
with a DOM adapter, and crawl generated links at `/` and `/magnets/`. Keep Git
history available when running these baseline comparisons. The rebuild check
compares all generated pages, ignoring incidental Bokeh identifiers/order.

These automated checks do not replace a live browser comparison. Before
publishing, compare desktop/mobile layout and exercise plot tools, hover,
click-throughs and DataTables in a browser. No browser was available to the
implementation session; screenshot and real-browser interaction QA remain
outstanding. The existing CSS, fonts and UI library versions are retained.
The custom Bokeh themes in the legacy Python files were never applied by
Flask's `components()`; the static renderer preserves its default theme.

## GitHub Pages

After merging the migration, configure repository **Settings → Pages → Deploy
from a branch → master → / (root)**. The empty `.nojekyll` file tells Pages to
serve committed files unchanged. No custom Actions build or Python runtime is
needed on the hosting side. GitHub manages the branch deployment.

For the existing repository, the expected project URL is
<https://jdbocarsly.github.io/magnets/>. Navigation and assets use relative paths.
Do not include local logs, environments, or the raw `all_data/` archive in
commits; branch-root publishing serves committed repository files.

See [MIGRATION_PLAN.md](MIGRATION_PLAN.md) for the agreed scope and findings.

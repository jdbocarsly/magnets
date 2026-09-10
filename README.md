A website for visualizing data from:

 J.D. Bocarsly, E.E. Levin, C.A.C. Garcia, K. Schwennicke, S.D. Wilson, R. Seshadri, A Simple Computational Proxy for Screening Magnetocaloric Compounds, *Chem. Mater.* **29** (2017) 1613−1622. [doi](https://doi.org/10.1021/acs.chemmater.6b04729)


The website is static HTML with standalone Bokeh 2.4.3 plots. The complete
generated site is committed in `docs/`, so previewing or hosting does not
require Flask or a build.

## Directory structure

```text
magnet_site/         Python builder, plotting code and data validation
web/templates/      Active Jinja page templates
web/static/         Source CSS and JavaScript
data/magnets.csv     Canonical curated dataset
data/dos/           DOS inputs used by the builder
data/legacy/        Historical data exports and spreadsheets
scripts/            Data curation and rebuild verification utilities
scripts/legacy/     Historical scientific and experimental scripts
tests/              Data, plot, interaction and link checks
docs/               Generated HTML and copied assets; publish this folder
archive/            Retired templates, experiments and project notes
archive/local/      Ignored local logs, editor files and raw calculation archive
```

Edit `magnet_site/`, `web/` or the canonical data, then rebuild; do not edit
generated files in `docs/` by hand. Archived scripts retain their historical
assumptions and dependencies; they are not part of the site build.

## Preview

From the repository root:

```sh
python3 -m http.server 8000 --directory docs
```

Open <http://localhost:8000/>. Use an HTTP server rather than opening files
directly. Bokeh, Bootstrap, DataTables, jQuery and fonts retain their existing
CDN versions, so the browser needs an internet connection.

## Rebuild after a source change

Install [uv](https://astral.sh/uv), then run:

```sh
uv run --locked python -m magnet_site
```

uv installs the locked Python 3.10 build environment on first use. Subsequent
builds use that environment. Commit the changed source and generated pages
together. `docs/generated-pages.json` lists the builder-owned output. Rebuilding
may change incidental Bokeh model IDs even when content is equivalent.

The output folder contains all local assets needed to serve the site. You can
also build a complete copy elsewhere with
`uv run --locked python -m magnet_site --output /path/to/output`.

The canonical input is [data/magnets.csv](data/magnets.csv); the cleanup is
documented in [data/README.md](data/README.md). It contains 165 compounds,
including 33 with magnetocaloric measurements. Co5Y retains its property page
but has no DOS source files. Existing IDs are preserved, with ID 7 removed.

Python renders Jinja templates and standalone plots. On the Ashby page,
JavaScript selects one of eight Python-generated plot structures, substitutes
the requested axes/color, and embeds a fresh Bokeh document. This preserves
the original plot structure and reset behavior without a server. DOS data is
embedded only in each compound's detail page.

The original scientific preparation scripts in `scripts/legacy/` and historical
data exports in `data/legacy/` are retained for reference. Routine builds do not run those scripts or require
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
compares all generated pages and copied assets, ignoring incidental Bokeh identifiers/order.

These automated checks do not replace a live browser comparison. Before
publishing, compare desktop/mobile layout and exercise plot tools, hover,
click-throughs and DataTables in a browser. No browser was available to the
implementation session; screenshot and real-browser interaction QA remain
outstanding. The existing CSS, fonts and UI library versions are retained.
The custom Bokeh themes in the legacy Python files were never applied by
Flask's `components()`; the static renderer preserves its default theme.

## GitHub Pages

After merging the migration, configure repository **Settings → Pages → Deploy
from a branch → master → /docs**. The empty `docs/.nojekyll` file tells Pages to
serve committed files unchanged. No custom Actions build or Python runtime is
needed on the hosting side. GitHub manages the branch deployment.

For the existing repository, the expected project URL is
<https://jdbocarsly.github.io/magnets/>. Navigation and assets use relative paths.
Only `docs/` is published; Python sources, scientific inputs and archived
material stay outside the site. The raw calculation archive and local logs
are preserved in ignored `archive/local/` and are not added to Git.

GitHub Pages supports `/` or `/docs` for branch-based publishing, so `docs/`
is intentionally the build folder name. Its name does not add `/docs/` to the
public URL. See [GitHub's publishing-source documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

See [the migration notes](archive/notes/MIGRATION_PLAN.md) for the original
scope and findings; the organization above supersedes their original root
publishing layout.

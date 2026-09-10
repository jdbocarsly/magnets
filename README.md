# Magnetocaloric materials

Interactive data from J.D. Bocarsly et al., *A Simple Computational Proxy for
Screening Magnetocaloric Compounds*, Chem. Mater. **29** (2017) 1613–1622.
[Paper](https://doi.org/10.1021/acs.chemmater.6b04729).

Static HTML preserves the original site's Bokeh 2.4.3 plots, fonts and layout,
with [documented data corrections](data/README.md). No Flask server is needed.

## Preview and build

The committed site is ready to serve:

```sh
python3 -m http.server 8000 --directory docs
```

Open <http://localhost:8000/>. Internet access is needed for the existing CDN
libraries and fonts. To rebuild, install [uv](https://astral.sh/uv), then:

```sh
uv sync --locked
uv run --locked python -m magnet_site
```

uv manages the locked Python 3.10 environment. Edit sources, not `docs/`, and
commit regenerated pages with source changes. Use
`uv run --locked python -m magnet_site --output /path/to/output` for another destination.

## Development checks

```sh
uv run --locked pre-commit install
uv run --locked pre-commit run --all-files
uv run --locked python -m unittest discover -s tests -v
uv run --locked python scripts/check_rebuild.py
```

Commit hooks fix Ruff lint/format issues and run fast unit tests. Re-stage any
automatic fixes. Generated output, scientific data and archived scripts are
excluded. Run just the fast tests with
`uv run --locked python -m unittest discover -s tests/unit -v`.

The full suite additionally needs Node.js and Git history (baseline `05720c8`).
It checks original plot parity, data, controls and links. The rebuild check
compares every page and asset while ignoring incidental Bokeh IDs. Live-browser
layout and interaction checks are still needed before publishing.

## Layout and hosting

- `magnet_site/`: Python builder, plotting and validation.
- `web/`: source templates, CSS and JavaScript.
- `data/`: canonical `magnets.csv`, DOS inputs and historical exports.
- `scripts/`: [curation and verification utilities](scripts/README.md).
- `tests/`: fast unit tests and full static-site regression checks.
- `docs/`: generated site and copied assets; the only published folder.
- `archive/` and `scripts/legacy/`: historical material, not build dependencies.

After merging, configure GitHub Pages: **Deploy from a branch → master → /docs**.
No custom build workflow is needed; `docs/.nojekyll` is included. The project
URL is <https://jdbocarsly.github.io/magnets/> (no `/docs/` in the URL).
See the [migration notes](archive/notes/MIGRATION_PLAN.md) for background.

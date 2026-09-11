# Magnetocaloric materials

Interactive data from J.D. Bocarsly et al., *A Simple Computational Proxy for
Screening Magnetocaloric Compounds*, Chem. Mater. **29** (2017) 1613–1622.
[Paper](https://doi.org/10.1021/acs.chemmater.6b04729).

This site was originally configured as a Flask server serving the data. It has 
now been converted to a Static HTML site with the same functionality, served on 
Github Pages.

## Preview and build

The built site is located in `docs/` and can be viewed locally with:

```sh
python3 -m http.server 8000 --directory docs
```

Open <http://localhost:8000/>. Internet access is needed as some libraries
and fonts are loaded via CDN.

The source files used to to build the site are stored in `magnet_site`, `web`, and `data`.

To rebuild the site after editing the data or code, install [uv](https://astral.sh/uv), then:

```sh
uv sync --locked
uv run --locked python -m magnet_site
```

`uv run --locked python -m magnet_site --output /path/to/output` Can be used to build into another destination.

## Development checks

```sh
uv run --locked pre-commit install
uv run --locked pre-commit run --all-files
uv run --locked python -m unittest discover -s tests -v
```

Commit hooks fix Ruff lint/format issues and run python unit tests.

There is also a regression test included that is used to test the new static site layout vs. 
the original Flask site. This test is more extensive and requires Node.js and the 
repository's Git history. This normally does not need to be run now that the migration 
is complete, but if needed it can be run with:
```sh
uv run --locked python scripts/check_rebuild.py #regression test for more detailed 
```

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


This migration was carried out largely by GPT 6 Astra, so results should be checked.
# Utilities

Run these from the repository root:

- `uv run --locked python scripts/check_rebuild.py` builds a temporary copy and
  compares it with `docs/`, including copied CSS/JavaScript.
- `uv run --locked python scripts/curate_data.py` reproduces the original
  one-time cleanup from `data/legacy/` and rewrites `data/magnets.csv`. Do not use
  this to rebuild the site after making new scientific corrections to that CSV.

Build the website with `uv run --locked python -m magnet_site`.

`legacy/` preserves historical data-preparation scripts and exploratory code.
They are not invoked by the website. Their original relative paths, dependency
requirements (including pymatgen and a local molar_mass module), and older
Python/pandas APIs are retained for provenance. Review paths and dependencies
before running them; data exports now live in `data/legacy/` and DOS inputs in
`data/dos/`. The DOS collection helpers and plotting prototypes are grouped in
`legacy/dos/`.

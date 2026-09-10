# Static migration with exact visual and functional parity

> Layout update: generated output now lives in `docs/`, with complete copied
> static assets. GitHub Pages should publish `master` → `/docs`. Active Python
> code is in `magnet_site/`, active templates/assets in `web/`, DOS inputs in
> `data/dos/`, historical exports in `data/legacy/`, and misc scripts in
> `scripts/legacy/`. Build with `uv run --locked python -m magnet_site`.
> The original plan below is retained as historical context.

## Summary

Reproduce the existing templates, CSS, fonts, Bootstrap, DataTables, and Bokeh
2.4.3 plots. Allow differences only for approved data corrections and static URL
mechanics. Build locally with Python/Jinja through uv; commit the generated HTML
and serve master from the GitHub Pages repository root with `.nojekyll`.

## Rendering

- Reuse Python plotting functions and templates; pin Python and CDN Bokeh to
  2.4.3 and lock compatible build dependencies.
- Emit index.html, ashby/index.html, correlations/index.html,
  datatable/index.html, about/index.html, and c/<cid>/index.html.
- Use relative links for localhost and /magnets/ hosting.
- Keep HTML selectors and swap control. Browser Bokeh callbacks must handle
  numeric/categorical axes, ranges, scales, tickers, glyphs, legends and color
  bars, preserving current ordering, filtering, colors, opacity and tools.
- Reset plots on selection changes, as Flask reloads do. Preserve encoded
  x_axis/y_axis/color_axis queries and back/forward restoration. Invalid inputs
  use the existing defaults.
- Build correlation and per-compound DOS plots using existing calculations;
  retain every DOS sample, normalization, signs and tools. Apply themes per
  document explicitly. Retain CDN versions, using HTTPS for assets.

## Data

- Verify latest CSV against active pickle; adopt the 36-column CSV as canonical.
- Remove duplicate MnNi2Ga cid=7; retain cid=139 and all other existing IDs.
- Retain Co5Y cid=37 with properties and a DOS-unavailable message.
- Describe 165 compounds and 33 magnetocalorics (measured at either 2 T or 5 T).
- Preserve numerical values, missingness, distinct variants and source content;
  document cleanup provenance.
- Validate IDs, material identifiers, required fields, positive atom counts,
  and both DOS files except the explicit Co5Y exception.

## Build and cleanup

- Provide `uv run python build_static.py`; preview with
  `python3 -m http.server`. Track generated output and manage only explicit
  generated paths, including stale compound pages.
- Preserve pre-existing user changes and scientific sources. After parity
  checks, remove Flask/Gunicorn entrypoints, Docker and its CI; retain plotting
  functions needed by the builder and scientific preprocessing scripts.
- Exclude logs, environments and the untracked raw archive from commits.
- Document Pages configuration; publishing is a separate deployment step.

## Verification

- Capture original Flask pages with assets loaded, then a cleaned-data Flask
  baseline. Compare static and cleaned Flask in the same browser and viewport,
  allowing only rasterization noise.
- Exercise every property, numeric/categorical transitions, swap, queries,
  back/forward, missing values, hover, navigation and existing plot tools.
- Check table search/sort/pagination/formatting, all correlation values and DOS
  series, and crawl output at root and /magnets/ prefixes.
- Rebuild and verify equivalent data/documents, disregarding incidental Bokeh
  generated identifiers when necessary.

## Commit sequence

1. Record plan and preserve the existing working-tree inputs used as baseline.
2. Add curated canonical data and validation.
3. Implement static rendering and browser interactions.
4. Verify parity, remove server deployment, document build and check in output.

## Implementation findings

- Flask `components()` constructs a default-themed document. The old
  `curdoc().theme` assignments never reached the plots. Preserve that observed
  default theme explicitly; applying the unused theme dictionaries would change
  the site's plot fonts and styling.
- Eight serialized Python plot templates (numeric/categorical x/y/color) are
  re-embedded by JavaScript when selectors change. This preserves the original
  model structure and reload-style reset without an exhaustive combination build.
- Matplotlib's removed `cm.get_cmap` is replaced by the equivalent named colormap
  registry lookup to build the existing correlation palette.
- The browser plugin reported no available browsers during implementation.
  Document/data parity checks can proceed; screenshot and live interaction
  verification remain a separate outstanding check until a browser is available.

## Verification results

- All retained source values match the original latest dataframe exactly.
- 88 JavaScript selections match the independently serialized baseline Python
  plots, covering every selectable field and all eight plot structures.
- Correlation and representative DOS model graphs match the baseline, including
  default fonts, dimensions, tools, glyphs and legends (apart from URL callback
  mechanics). Every correlation coefficient and all 164 available DOS series
  pass numerical checks.
- DOM-adapter tests cover query defaults, axis/color changes, swap, back/forward
  restoration, rapid changes and disposal; callback tests cover encoded
  correlation links and multiple selected cells.
- All local links and assets resolve at both `/` and `/magnets/` prefixes.
- A separate temporary rebuild matches all 170 pages after normalizing
  incidental Bokeh identifiers and reference ordering.
- The preview server returned HTTP 200 for all 171 generated files (170 pages
  plus `.nojekyll`). Browser screenshots, actual canvas interactions and
  DataTables UI checks remain unverified due to the unavailable browser.
- Flask/Gunicorn, Docker, WSGI and Docker CI are removed. Their source is
  recoverable from the baseline commit. Publishing has not been enabled.

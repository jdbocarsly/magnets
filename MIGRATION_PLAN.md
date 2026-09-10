# Static migration with exact visual and functional parity

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

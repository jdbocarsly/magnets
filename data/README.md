# Curated website data

`magnets.csv` is the authoritative build input. It contains all 36 columns of
the latest local `legacy/clean_pickle3.df` / `legacy/clean_df3.csv` exports, verified identical
before conversion. Missing numeric values remain empty CSV cells.

The migration removed only row `cid=7` (MnNi2Ga). Row `cid=139` is retained:
its magnetic deformation (0.7431739485%) and other calculated quantities match
the older `legacy/clean_pickle.df` MnNi2Ga result more closely. The removed row instead
shares calculated values with the separate MnNi2Ga_FM-PM variant. No remaining
IDs were reassigned and no remaining numerical values were changed.

Co5Y (`cid=37`) is retained, but its DOS files are absent. Its detail page reports
this explicitly. The exception is validated by both ID and material identifier.

There are 165 records and 33 with magnetocaloric measurements at either 2 T or
5 T. Fe3GeTe2 has only a 5 T measurement; counting just 2 T would incorrectly
give 32. Distinct structural/transition variants remain separate records.

[scripts/curate_data.py](../scripts/curate_data.py) records the one-time migration. Routine website builds
read this CSV directly and do not require pickle files or scientific reanalysis.

`dos/` contains the original DOS samples, loaded by material identifier. They
are embedded in generated compound pages and are not copied into the published
site as raw files. The legacy exports and spreadsheets in `legacy/` are kept
for provenance; miscellaneous plotting experiments are under `archive/dos/`.

"""One-time, auditable migration from the preserved latest data exports."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main():
    original = pd.read_pickle(ROOT / 'clean_pickle3.df')
    exported = pd.read_csv(ROOT / 'clean_df3.csv', index_col=0,
                           float_precision='round_trip')
    pd.testing.assert_frame_equal(original, exported, check_exact=True)
    assert original.loc[original.cid == 7, 'material_name'].item() == 'MnNi2Ga'
    assert original.loc[original.cid == 139, 'material_name'].item() == 'MnNi2Ga'
    clean = original.loc[original.cid != 7].copy()
    assert clean.material_name.is_unique and len(clean) == 165
    destination = ROOT / 'data' / 'magnets.csv'
    destination.parent.mkdir(exist_ok=True)
    clean.to_csv(destination, index=False)
    roundtrip = pd.read_csv(destination, float_precision='round_trip')
    pd.testing.assert_frame_equal(clean.reset_index(drop=True), roundtrip,
                                  check_exact=True)
    print(f'Wrote {len(clean)} records to {destination}')


if __name__ == '__main__':
    main()

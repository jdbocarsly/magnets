"""Canonical data and validation shared by the builder and checks."""
from pathlib import Path

import numpy as np
import pandas as pd

from . import resources
from .paths import ROOT, DATA, DOS

MISSING_DOS = {37: 'Co5Y'}


def load_data(path=DATA):
    df = pd.read_csv(path, float_precision='round_trip')
    required = {'cid', 'material_name', 'formula', 'natoms'}
    for _, fields in resources.axis_columns_groups + resources.dos_columns_groups:
        required.update(fields)
    required.update(resources.corr_cols)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f'Missing required columns: {sorted(missing)}')
    for key in ('cid', 'material_name'):
        if df[key].isna().any() or df[key].duplicated().any():
            raise ValueError(f'{key} must be present and unique')
    if not ((df.cid >= 0) & (df.cid == df.cid.astype(int))).all():
        raise ValueError('cid must be a nonnegative integer')
    if not (np.isfinite(df.natoms) & (df.natoms > 0)).all():
        raise ValueError('natoms must be finite and positive')
    for row in df.itertuples():
        if Path(row.material_name).name != row.material_name:
            raise ValueError(f'Invalid material identifier: {row.material_name}')
        for filename in ('nonsp_dost.dat', 'sp_dost.dat'):
            if not (DOS / row.material_name / filename).is_file():
                if MISSING_DOS.get(row.cid) != row.material_name:
                    raise ValueError(f'Missing DOS: {row.material_name}/{filename}')
    return df


def display_data(df):
    df = df.copy()
    df['formula_nosubs'] = df.formula
    df['formula_html'] = df.formula.map(resources.make_html_subscripts)
    df['formula'] = df.formula.map(resources.make_unicode_subscripts)
    df['class'] = df['class'].fillna('classless')
    return df


def counts(df):
    fields = ['−ΔSm(H = 2T) (J kg⁻¹ K⁻¹)', '−ΔSm(H = 5T) (J kg⁻¹ K⁻¹)']
    return len(df), int(df[fields].notna().any(axis=1).sum())

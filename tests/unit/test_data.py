"""Validation failures using small, isolated data fixtures."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

from magnet_site.data import counts, display_data, load_data
from magnet_site.paths import DATA


class DataTests(unittest.TestCase):
    def setUp(self):
        self.row = pd.read_csv(DATA).iloc[[0]].copy()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        folder = self.root / self.row.iloc[0].material_name
        folder.mkdir()
        for name in ("nonsp_dost.dat", "sp_dost.dat"):
            (folder / name).touch()
        self.dos_patch = patch("magnet_site.data.DOS", self.root)
        self.dos_patch.start()
        self.addCleanup(self.dos_patch.stop)

    def load(self, frame):
        path = self.root / "input.csv"
        frame.to_csv(path, index=False)
        return load_data(path)

    def test_valid_row(self):
        self.assertEqual(len(self.load(self.row)), 1)

    def test_missing_column(self):
        with self.assertRaisesRegex(ValueError, "Missing required columns.*formula"):
            self.load(self.row.drop(columns="formula"))

    def test_duplicate_and_missing_identifiers(self):
        for key in ("cid", "material_name"):
            for missing in (False, True):
                with self.subTest(key=key, missing=missing):
                    frame = pd.concat([self.row, self.row], ignore_index=True)
                    frame["cid"] = [1000, 1001]
                    frame["material_name"] = ["first", "second"]
                    frame[key] = [None, frame.loc[1, key]] if missing else [1, 1]
                    with self.assertRaisesRegex(
                        ValueError, f"{key} must be present and unique"
                    ):
                        self.load(frame)

    def test_invalid_numeric_values(self):
        for key, values, message in (
            ("cid", [-1, 0.5], "cid must be a nonnegative integer"),
            ("natoms", [0, -1, np.nan, np.inf], "natoms must be finite and positive"),
        ):
            for value in values:
                with self.subTest(key=key, value=value):
                    frame = self.row.copy()
                    frame[key] = value
                    with self.assertRaisesRegex(ValueError, message):
                        self.load(frame)

    def test_material_path_cannot_escape_dos_directory(self):
        self.row["material_name"] = "../outside"
        with self.assertRaisesRegex(ValueError, "Invalid material identifier"):
            self.load(self.row)

    def test_missing_dos_requires_exact_exception(self):
        self.row["material_name"] = "Co5Y"
        self.row["cid"] = 37
        self.assertEqual(len(self.load(self.row)), 1)
        for cid, name in ((38, "Co5Y"), (37, "Other")):
            with self.subTest(cid=cid, name=name):
                self.row["cid"], self.row["material_name"] = cid, name
                with self.assertRaisesRegex(ValueError, "Missing DOS"):
                    self.load(self.row)

    def test_measurements_counted_once_across_fields(self):
        frame = pd.DataFrame(
            {
                "−ΔSm(H = 2T) (J kg⁻¹ K⁻¹)": [1, np.nan, 1, np.nan],
                "−ΔSm(H = 5T) (J kg⁻¹ K⁻¹)": [np.nan, 1, 1, np.nan],
            }
        )
        self.assertEqual(counts(frame), (4, 3))

    def test_display_data_does_not_mutate_input(self):
        self.row["formula"] = "Fe2O3"
        self.row["class"] = np.nan
        original = self.row.copy(deep=True)
        result = display_data(self.row)
        pd.testing.assert_frame_equal(self.row, original)
        self.assertEqual(result.iloc[0].formula, "Fe₂O₃")
        self.assertEqual(result.iloc[0].formula_html, "Fe<sub>2</sub>O<sub>3</sub>")
        self.assertEqual(result.iloc[0].formula_nosubs, "Fe2O3")
        self.assertEqual(result.iloc[0]["class"], "classless")

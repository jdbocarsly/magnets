"""Rendering edge cases."""

import json
import unittest

from magnet_site.build import safe_json, source_links


class RenderingTests(unittest.TestCase):
    def test_embedded_json_cannot_close_script(self):
        value = {"citation": "</script><script>alert('Fe₂')</script>"}
        encoded = safe_json(value)
        self.assertNotIn("<", encoded)
        self.assertEqual(json.loads(encoded), value)

    def test_nonfinite_values_rejected(self):
        for value in (float("nan"), float("inf"), -float("inf")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                safe_json({"value": value})

    def test_doi_repairs_preserve_visible_text(self):
        for href, expected in (
            ("dx.doi.org/10.123/test", "https://dx.doi.org/10.123/test"),
            ("doi.org/10.123/test", "https://doi.org/10.123/test"),
            ("10.123/test", "https://doi.org/10.123/test"),
            ("https://example.org/paper", "https://example.org/paper"),
            ("../paper", "../paper"),
        ):
            with self.subTest(href=href):
                self.assertEqual(
                    source_links(f'<a href="{href}">Original citation</a>'),
                    f'<a href="{expected}">Original citation</a>',
                )

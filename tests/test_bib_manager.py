import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import requests

from ultility_toolkit.bib_manager import (
    BibFetchError,
    append_to_bib_file,
    get_bibtex_from_doi,
    normalize_doi,
)


class BibManagerTests(unittest.TestCase):
    def test_normalize_doi_removes_common_prefixes(self):
        self.assertEqual(
            normalize_doi("https://doi.org/10.1038/s41586-021-03819-2"),
            "10.1038/s41586-021-03819-2",
        )
        self.assertEqual(normalize_doi("doi:10.1000/example"), "10.1000/example")

    @patch("ultility_toolkit.bib_manager.requests.get")
    def test_get_bibtex_from_doi_returns_bibtex(self, mock_get):
        mock_get.return_value = Mock(status_code=200, text="@article{example,\n title={Demo}\n}")

        result = get_bibtex_from_doi("10.1000/example")

        self.assertTrue(result.startswith("@article"))
        mock_get.assert_called_once()

    @patch("ultility_toolkit.bib_manager.requests.get")
    def test_get_bibtex_from_doi_raises_on_network_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("timeout")

        with self.assertRaises(BibFetchError):
            get_bibtex_from_doi("10.1000/example")

    def test_append_to_bib_file_writes_valid_entry(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "refs.bib"

            append_to_bib_file("@article{example,\n title={Demo}\n}", str(path))

            self.assertIn("@article{example", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

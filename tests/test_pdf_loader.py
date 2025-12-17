"""Tests unitaires pour la lecture de tableaux PDF sans dépendances."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from listedetenus.pdf_loader import read_pdf_tables


class PdfLoaderTestCase(unittest.TestCase):
    """Vérifie l'extraction de tables à partir d'un fichier PDF textuel."""

    def test_read_pdf_tables_extracts_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_path = Path(tmp_dir) / "sample.pdf"
            pdf_path.write_text(
                "Nom;Prénom;Date\nABAS;Lena;05/09/1981\nZEE;Mara;1990-12-01",
                encoding="utf-8",
            )

            result = read_pdf_tables(pdf_path)

            expected = [
                ["Nom", "Prénom", "Date"],
                ["ABAS", "Lena", "05/09/1981"],
                ["ZEE", "Mara", "1990-12-01"],
            ]
            self.assertEqual(result.tables, [expected])

    def test_read_pdf_tables_rejects_non_pdf_extension(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            text_path = Path(tmp_dir) / "sample.txt"
            text_path.write_text("content", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_pdf_tables(text_path)


if __name__ == "__main__":
    unittest.main()

"""Tests unitaires pour l'extraction des détenus."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from listedetenus.csv_writer import write_csv
from listedetenus.models import Detainee
from listedetenus.parser import tables_to_detainees


class TablesToDetaineesTestCase(unittest.TestCase):
    """Vérifie la transformation des tables en détenus."""

    def test_tables_to_detainees_extracts_rows(self) -> None:
        table = [
            ["Nom", "Prénom", "Date de naissance"],
            ["ABAS", "Lena", "05/09/1981"],
            ["ZEE", "Mara", "1990-12-01"],
        ]
        detainees = tables_to_detainees([table])
        self.assertEqual(
            detainees,
            [
                Detainee(
                    nom="ABAS", prenom="Lena", date_naissance="1981-09-05"
                ),
                Detainee(
                    nom="ZEE", prenom="Mara", date_naissance="1990-12-01"
                ),
            ],
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "detenus.csv"
            write_csv(csv_path, detainees)
            content = csv_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(content[0], "nom,prenom,date_naissance")
            self.assertIn("ABAS,Lena,1981-09-05", content[1])

    def test_tables_to_detainees_raises_when_no_valid_rows(self) -> None:
        table = [
            ["Nom", "Prénom", "Date de naissance"],
            ["", "", ""],
        ]
        with self.assertRaises(ValueError):
            tables_to_detainees([table])

    def test_tables_to_detainees_ignores_tables_without_headers(self) -> None:
        tables = [
            [["Autre", "Champs"], ["X", "Y"]],
            [
                ["Nom", "Prénom", "Date de naissance"],
                ["AA", "BB", "01/01/90"],
            ],
        ]
        detainees = tables_to_detainees(tables)
        self.assertEqual(
            detainees,
            [
                Detainee(
                    nom="AA", prenom="BB", date_naissance="1990-01-01"
                )
            ],
        )

    def test_tables_to_detainees_detects_headers_below_first_row(self) -> None:
        tables = [
            [
                ["", ""],
                ["NOM", "Prénom", "Date naissance"],
                ["ABERKANE", "Yassine", "10/02/1987"],
            ]
        ]

        detainees = tables_to_detainees(tables)

        self.assertEqual(
            detainees,
            [
                Detainee(
                    nom="ABERKANE",
                    prenom="Yassine",
                    date_naissance="1987-02-10",
                )
            ],
        )


if __name__ == "__main__":
    unittest.main()

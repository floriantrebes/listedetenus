"""Tests du flux de conversion PDF vers CSV."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from listedetenus import workflow
from listedetenus.models import PdfExtractionResult


class WorkflowTestCase(unittest.TestCase):
    """Vérifie l'orchestration de la conversion PDF vers CSV."""

    def test_convert_pdf_to_csv_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_path = Path(tmp_dir) / "source.pdf"
            pdf_path.write_text("Nom;Prenom\nA;B", encoding="utf-8")
            csv_path = Path(tmp_dir) / "export" / "result.csv"

            def fake_read(path: Path) -> PdfExtractionResult:
                self.assertEqual(path, pdf_path.resolve())
                return PdfExtractionResult(source=path, tables=[["table"]])

            def fake_tables_to_detainees(
                tables: list[list[list[str]]]
            ) -> list[str]:
                self.assertEqual(tables, [["table"]])
                return ["payload"]

            captured: dict[str, object] = {}

            def fake_write(path: Path, data: list[str]) -> None:
                captured["path"] = path
                captured["data"] = data

            with mock.patch.object(workflow, "read_pdf_tables", fake_read):
                with mock.patch.object(
                    workflow, "tables_to_detainees", fake_tables_to_detainees
                ):
                    with mock.patch.object(workflow, "write_csv", fake_write):
                        result = workflow.convert_pdf_to_csv(
                            pdf_path, csv_path
                        )

            self.assertEqual(result, csv_path.resolve())
            self.assertEqual(captured["path"], csv_path.resolve())
            self.assertEqual(captured["data"], ["payload"])
            self.assertTrue(csv_path.parent.exists())

    def test_convert_pdf_to_csv_requires_csv_extension(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_path = Path(tmp_dir) / "source.pdf"
            pdf_path.write_text("Nom", encoding="utf-8")
            invalid_csv = Path(tmp_dir) / "export.txt"

            with self.assertRaises(ValueError):
                workflow.convert_pdf_to_csv(pdf_path, invalid_csv)

    def test_convert_pdf_to_csv_rejects_file_as_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_path = Path(tmp_dir) / "source.pdf"
            pdf_path.write_text("Nom", encoding="utf-8")
            parent_file = Path(tmp_dir) / "existing"
            parent_file.write_text("content", encoding="utf-8")
            target_csv = parent_file / "result.csv"

            with self.assertRaises(ValueError):
                workflow.convert_pdf_to_csv(pdf_path, target_csv)


if __name__ == "__main__":
    unittest.main()

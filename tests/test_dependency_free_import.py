"""Garantit l'import sans dépendance externe."""

from __future__ import annotations

import importlib
import sys
import unittest
from pathlib import Path
from unittest import mock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


class DependencyFreeImportTestCase(unittest.TestCase):
    """Vérifie que le module n'exige aucune bibliothèque tierce."""

    def test_pdf_loader_import_succeeds_without_pdfplumber(self) -> None:
        """Assure l'import même si pdfplumber est indisponible."""

        module_name = "listedetenus.pdf_loader"
        with mock.patch.dict(sys.modules, {"pdfplumber": None}):
            sys.modules.pop(module_name, None)
            pdf_loader = importlib.import_module(module_name)

        self.assertIsNotNone(pdf_loader)


if __name__ == "__main__":
    unittest.main()

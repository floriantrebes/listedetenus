"""Lecture sécurisée des tableaux depuis un PDF à l'aide de pdfplumber."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

import pdfplumber

from listedetenus.models import PdfExtractionResult
from listedetenus.constants import MAX_ROW_FIELDS

LOGGER = logging.getLogger(__name__)


def read_pdf_tables(pdf_path: Path) -> PdfExtractionResult:
    """Extrait toutes les tables du fichier PDF fourni.

    Rôle:
        Ouvrir le PDF, extraire les tableaux et retourner leur contenu nettoyé.
    Entrées:
        pdf_path: chemin du fichier PDF existant.
    Sorties:
        PdfExtractionResult contenant les tableaux sous forme de listes.
    Erreurs:
        ValueError: fichier manquant, extension incorrecte ou aucune table.
        RuntimeError: échec de l'extraction du PDF.
    """

    _validate_pdf_path(pdf_path)
    tables: list[list[list[str]]] = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_tables = _extract_page_tables(page.extract_tables())
                tables.extend(page_tables)
    except Exception as error:  # noqa: BLE001
        message = f"Échec de lecture du PDF: {error}."
        LOGGER.error(message)
        raise RuntimeError(message) from error

    if not tables:
        message = "Aucune table détectée dans le PDF."
        raise ValueError(message)

    return PdfExtractionResult(source=pdf_path, tables=tables)


def _validate_pdf_path(pdf_path: Path) -> None:
    """Vérifie l'existence et l'extension du fichier PDF."""

    if pdf_path is None:
        raise ValueError("Le chemin PDF ne peut pas être nul.")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Le fichier doit avoir l'extension .pdf.")
    if not pdf_path.exists():
        raise ValueError("Le fichier PDF fourni est introuvable.")


def _extract_page_tables(
    raw_tables: Iterable[list[list[str]]],
) -> list[list[list[str]]]:
    """Nettoie et normalise les tableaux extraits d'une page."""

    cleaned_tables: list[list[list[str]]] = []
    for raw_table in raw_tables:
        cleaned_rows = [_clean_row(row) for row in raw_table if row]
        if cleaned_rows:
            cleaned_tables.append(cleaned_rows)
    return cleaned_tables


def _clean_row(row: list[str]) -> list[str]:
    """Normalise une ligne en limitant sa taille et en supprimant les None."""

    bounded_row = row[:MAX_ROW_FIELDS]
    cleaned_cells: list[str] = []
    for cell in bounded_row:
        if cell is None:
            cleaned_cells.append("")
        else:
            cleaned_cells.append(cell.strip())
    return cleaned_cells

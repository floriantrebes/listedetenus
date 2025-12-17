"""Lecture sécurisée des tableaux depuis un fichier PDF textuel."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

from listedetenus.constants import MAX_ROW_FIELDS
from listedetenus.models import PdfExtractionResult

LOGGER = logging.getLogger(__name__)

LINE_SEPARATORS: list[str] = [";", ",", "\t", "|"]
FALLBACK_SEPARATOR: str = " "
MIN_COLUMN_COUNT: int = 2


def read_pdf_tables(pdf_path: Path) -> PdfExtractionResult:
    """Extrait les tableaux d'un fichier PDF textuel.

    Rôle:
        Lire le contenu d'un fichier PDF (supposé textuel) et en déduire des
        tableaux structurés à partir des séparateurs présents dans chaque
        ligne.
    Entrées:
        pdf_path: chemin du fichier PDF existant.
    Sorties:
        PdfExtractionResult contenant les tableaux sous forme de listes.
    Erreurs:
        ValueError: fichier manquant, extension incorrecte ou aucune table.
        RuntimeError: échec de lecture du fichier.
    """

    _validate_pdf_path(pdf_path)
    content = _load_pdf_content(pdf_path)
    tables = _extract_tables_from_text(content)
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


def _load_pdf_content(pdf_path: Path) -> str:
    """Lit le fichier en texte en essayant des décodages sûrs."""

    try:
        raw_bytes = pdf_path.read_bytes()
    except Exception as error:  # noqa: BLE001
        message = f"Impossible de lire le PDF: {error}."
        LOGGER.error(message)
        raise RuntimeError(message) from error

    if not raw_bytes:
        raise ValueError("Le fichier PDF est vide.")

    decoders = ["utf-8", "latin-1"]
    for decoder in decoders:
        try:
            return raw_bytes.decode(decoder)
        except UnicodeDecodeError:
            continue
    return raw_bytes.decode("utf-8", errors="replace")


def _extract_tables_from_text(text: str) -> list[list[list[str]]]:
    """Construit des tableaux à partir de lignes textuelles séparées."""

    tables: list[list[list[str]]] = []
    current_table: list[list[str]] = []
    for line in _iter_clean_lines(text):
        if line == "":
            _append_table_if_not_empty(tables, current_table)
            current_table = []
            continue
        row = _split_row(line)
        if row:
            current_table.append(row)
    _append_table_if_not_empty(tables, current_table)
    return tables


def _iter_clean_lines(text: str) -> Iterable[str]:
    """Retourne les lignes nettoyées du texte fourni."""

    for raw_line in text.splitlines():
        yield raw_line.strip()


def _append_table_if_not_empty(
    tables: list[list[list[str]]], table: list[list[str]]
) -> None:
    """Ajoute un tableau s'il contient au moins une ligne."""

    if table:
        tables.append(table)


def _split_row(line: str) -> list[str] | None:
    """Découpe une ligne en cellules en choisissant le meilleur séparateur."""

    separator = _detect_separator(line)
    cells = [cell.strip() for cell in line.split(separator)]
    if len(cells) < MIN_COLUMN_COUNT:
        return None
    return cells[:MAX_ROW_FIELDS]


def _detect_separator(line: str) -> str:
    """Identifie le séparateur le plus probable pour une ligne."""

    for separator in LINE_SEPARATORS:
        if separator in line:
            return separator
    return FALLBACK_SEPARATOR

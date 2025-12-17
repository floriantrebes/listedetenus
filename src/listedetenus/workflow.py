"""Orchestration du flux de conversion PDF vers CSV."""

from __future__ import annotations

import logging
from pathlib import Path

from listedetenus.csv_writer import write_csv
from listedetenus.pdf_loader import read_pdf_tables
from listedetenus.parser import tables_to_detainees

CSV_EXTENSION = ".csv"
LOGGER = logging.getLogger(__name__)


def convert_pdf_to_csv(pdf_path: Path, csv_path: Path) -> Path:
    """Convertit un fichier PDF en CSV.

    Rôle:
        Exécuter l'extraction des détenus et écrire le résultat dans un CSV.
    Entrées:
        pdf_path: chemin du fichier PDF à extraire.
        csv_path: chemin du fichier CSV de sortie souhaité.
    Sorties:
        Chemin absolu du CSV écrit.
    Erreurs:
        ValueError: chemins manquants, extension CSV invalide ou dossier cible
            incorrect.
        RuntimeError: échec de l'extraction ou de l'écriture des données.
    """

    resolved_pdf = _normalize_path(pdf_path)
    resolved_csv = _normalize_path(csv_path)
    _validate_csv_path(resolved_csv)
    _ensure_target_directory(resolved_csv)

    try:
        extraction = read_pdf_tables(resolved_pdf)
        detainees = tables_to_detainees(extraction.tables)
        write_csv(resolved_csv, detainees)
    except Exception as error:  # noqa: BLE001
        message = f"Conversion impossible: {error}."
        LOGGER.error(message)
        raise RuntimeError(message) from error

    return resolved_csv


def _normalize_path(path_value: Path) -> Path:
    """Retourne un chemin absolu validé."""

    if path_value is None:
        raise ValueError("Un chemin de fichier est requis.")
    return Path(path_value).expanduser().resolve()


def _validate_csv_path(csv_path: Path) -> None:
    """Vérifie l'extension et la cible du CSV."""

    if csv_path.suffix.lower() != CSV_EXTENSION:
        message = "Le fichier de sortie doit avoir l'extension .csv."
        raise ValueError(message)
    if csv_path.exists() and csv_path.is_dir():
        message = "Le chemin CSV cible ne peut pas être un dossier."
        raise ValueError(message)


def _ensure_target_directory(csv_path: Path) -> None:
    """Crée le dossier parent du CSV si nécessaire."""

    parent = csv_path.parent
    if parent.exists() and not parent.is_dir():
        message = "Impossible d'écrire le CSV: le dossier parent est un fichier."
        raise ValueError(message)
    parent.mkdir(parents=True, exist_ok=True)

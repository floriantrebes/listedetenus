"""Interface en ligne de commande pour convertir un PDF en CSV."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from listedetenus.csv_writer import write_csv
from listedetenus.pdf_loader import read_pdf_tables
from listedetenus.parser import tables_to_detainees

LOG_FORMAT = "%(levelname)s | %(message)s"
LOGGER = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Construit l'analyseur d'arguments CLI."""

    parser = argparse.ArgumentParser(
        description=(
            "Convertit un tableau PDF de détenus en fichier CSV avec nom, "
            "prenom et date de naissance"
        )
    )
    parser.add_argument(
        "pdf",
        type=Path,
        help="Chemin vers le PDF contenant le tableau à extraire",
    )
    parser.add_argument(
        "csv",
        type=Path,
        help="Chemin du fichier CSV de sortie",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Active les logs détaillés pour le débogage",
    )
    return parser


def configure_logging(is_verbose: bool) -> None:
    """Initialise le logging global selon l'option utilisateur."""

    level = logging.DEBUG if is_verbose else logging.INFO
    logging.basicConfig(level=level, format=LOG_FORMAT)


def main() -> int:
    """Point d'entrée CLI.

    Retourne 0 en cas de succès, 1 en cas d'erreur contrôlée.
    """

    parser = build_parser()
    args = parser.parse_args()
    configure_logging(args.verbose)

    try:
        extraction = read_pdf_tables(args.pdf)
        detainees = tables_to_detainees(extraction.tables)
        write_csv(args.csv, detainees)
    except Exception as error:  # noqa: BLE001
        LOGGER.error("Échec: %s", error)
        return 1

    LOGGER.info("Conversion réussie: %s", args.csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

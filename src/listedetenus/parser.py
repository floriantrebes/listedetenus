"""Conversion des tableaux PDF en données de détenus."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Iterable

from listedetenus.constants import CSV_HEADERS, DATE_FORMATS, HEADER_KEYWORDS
from listedetenus.models import Detainee

LOGGER = logging.getLogger(__name__)


class ColumnMapping:
    """Index des colonnes utiles dans un tableau."""

    def __init__(self, nom: int, prenom: int, date_naissance: int) -> None:
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance


def tables_to_detainees(tables: Iterable[list[list[str]]]) -> list[Detainee]:
    """Transforme les tables en liste de détenus.

    Rôle:
        Parcourir les tables et isoler nom, prénom, date de naissance.
    Entrées:
        tables: séquence de tables issues du PDF.
    Sorties:
        Liste de Detainee prête pour l'écriture CSV.
    Erreurs:
        ValueError si aucune ligne valide n'est trouvée.
    """

    detainees: list[Detainee] = []
    for table in tables:
        mapping = _find_columns(table)
        if mapping is None:
            LOGGER.info("Table ignorée: entêtes introuvables.")
            continue
        detainees.extend(_parse_table_rows(table, mapping))

    if not detainees:
        message = "Aucune ligne exploitable après analyse des tables."
        raise ValueError(message)

    return detainees


def _find_columns(table: list[list[str]]) -> ColumnMapping | None:
    """Localise les indices de colonnes nom, prénom et naissance."""

    if not table:
        return None
    header_row = table[0]
    positions: dict[str, int] = {}
    for index, cell in enumerate(header_row):
        lowered = cell.lower()
        for field, keywords in HEADER_KEYWORDS.items():
            if field in positions:
                continue
            if any(keyword in lowered for keyword in keywords):
                positions[field] = index
    if set(positions) == set(CSV_HEADERS):
        return ColumnMapping(
            nom=positions["nom"],
            prenom=positions["prenom"],
            date_naissance=positions["date_naissance"],
        )
    return None


def _parse_table_rows(
    table: list[list[str]], mapping: ColumnMapping
) -> list[Detainee]:
    """Lit les lignes d'un tableau en appliquant la correspondance d'index."""

    detainees: list[Detainee] = []
    for row in table[1:]:
        if not row:
            continue
        detainee = _row_to_detainee(row, mapping)
        if detainee is not None:
            detainees.append(detainee)
    return detainees


def _row_to_detainee(row: list[str], mapping: ColumnMapping) -> Detainee | None:
    """Convertit une ligne en Detainee si tous les champs sont valides."""

    if len(row) <= max(mapping.nom, mapping.prenom, mapping.date_naissance):
        LOGGER.debug("Ligne ignorée: longueur insuffisante.")
        return None
    nom = row[mapping.nom].strip()
    prenom = row[mapping.prenom].strip()
    birth_raw = row[mapping.date_naissance].strip()
    birth_date = _parse_birth_date(birth_raw)
    if not nom or not prenom or birth_date is None:
        LOGGER.debug("Ligne ignorée: champs manquants ou date invalide.")
        return None
    return Detainee(nom=nom, prenom=prenom, date_naissance=birth_date)


def _parse_birth_date(raw_value: str) -> str | None:
    """Valide et normalise la date de naissance en ISO 8601."""

    cleaned = raw_value.replace(" ", "").replace(".", "/")
    for fmt in DATE_FORMATS:
        try:
            parsed = datetime.strptime(cleaned, fmt)
            return parsed.date().isoformat()
        except ValueError:
            continue
    return None

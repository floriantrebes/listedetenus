"""Constantes pour l'extraction de détenus depuis un PDF.

Toutes les valeurs sont limitées à 80 colonnes pour respecter la lisibilité.
"""

from __future__ import annotations

DATE_FORMATS: list[str] = [
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%Y-%m-%d",
    "%d/%m/%y",
]

CSV_HEADERS: list[str] = ["nom", "prenom", "date_naissance"]

HEADER_KEYWORDS: dict[str, list[str]] = {
    "nom": ["nom"],
    "prenom": ["prénom", "prenom"],
    "date_naissance": ["naissance", "date de naissance", "date"],
}

MAX_ROW_FIELDS: int = 30

"""Structures de données utilisées pour la conversion PDF vers CSV."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Detainee:
    """Représente un détenu extrait d'un tableau PDF.

    Attributs:
        nom: Nom de famille en lettres capitales si disponible.
        prenom: Prénom du détenu.
        date_naissance: Date de naissance au format ISO (YYYY-MM-DD).
    """

    nom: str
    prenom: str
    date_naissance: str


@dataclass(frozen=True)
class PdfExtractionResult:
    """Agrège les lignes extraites d'un PDF.

    Attributs:
        source: Chemin du PDF analysé.
        tables: Tables lues; chaque table est une liste de lignes, et chaque
            ligne est une liste de cellules sous forme de chaîne.
    """

    source: Path
    tables: list[list[list[str]]]

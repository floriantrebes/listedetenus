"""Export des données de détenus vers un fichier CSV."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from listedetenus.constants import CSV_HEADERS
from listedetenus.models import Detainee


def write_csv(output_path: Path, detainees: Iterable[Detainee]) -> None:
    """Écrit les détenus dans un fichier CSV avec des en-têtes explicites.

    Rôle:
        Créer le fichier CSV et y déposer chaque détenu sur une ligne.
    Entrées:
        output_path: chemin du fichier CSV à créer.
        detainees: séquence de Detainee.
    Sorties:
        Aucun retour. Le fichier est créé ou écrasé.
    Erreurs:
        ValueError si le chemin est invalide.
        RuntimeError en cas d'échec d'écriture.
    """

    if output_path is None:
        raise ValueError("Le chemin de sortie ne peut pas être nul.")

    try:
        with output_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_HEADERS)
            writer.writeheader()
            for detainee in detainees:
                writer.writerow(
                    {
                        "nom": detainee.nom,
                        "prenom": detainee.prenom,
                        "date_naissance": detainee.date_naissance,
                    }
                )
    except Exception as error:  # noqa: BLE001
        message = f"Impossible d'écrire le CSV: {error}."
        raise RuntimeError(message) from error

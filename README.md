# listedetenus

Outil en ligne de commande pour extraire depuis un PDF la liste des détenus
(NOM, PRÉNOM, date de naissance) et générer un fichier CSV.

## Prérequis

- Python 3.10 ou supérieur
- Aucune dépendance externe : la bibliothèque standard suffit.

## Utilisation

### Interface graphique sans installation supplémentaire

Tkinter est inclus dans la distribution standard de Python. Lancez l'outil
graphique sans dépendances additionnelles :

```bash
PYTHONPATH=src python -m listedetenus.gui
```

Choisissez le PDF source et l'emplacement du CSV généré via les boîtes de
dialogue.

```bash
PYTHONPATH=src python -m listedetenus.cli chemin/vers/liste.pdf \
    sortie/detenus.csv
```

Options utiles :
- `--verbose` : active les logs détaillés pour diagnostiquer les extractions
  difficiles.

Le fichier CSV généré contient les colonnes `nom`, `prenom` et
`date_naissance` au format ISO AAAA-MM-JJ.

## Tests

Les tests reposent uniquement sur la bibliothèque standard :

```bash
python -m unittest
```

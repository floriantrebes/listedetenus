# listedetenus

Outil en ligne de commande pour extraire depuis un PDF la liste des détenus
(NOM, PRÉNOM, date de naissance) et générer un fichier CSV.

## Prérequis

- Python 3.10 ou supérieur
- Dépendances installées via `pip install -r requirements.txt`

## Utilisation

```bash
python -m listedetenus.cli chemin/vers/liste.pdf sortie/detenus.csv
```

Options utiles :
- `--verbose` : active les logs détaillés pour diagnostiquer les extractions
  difficiles.

Le fichier CSV généré contient les colonnes `nom`, `prenom` et
`date_naissance` au format ISO AAAA-MM-JJ.

## Tests

Installez les dépendances de développement puis lancez Pytest :

```bash
pip install -r requirements-dev.txt
pytest
```

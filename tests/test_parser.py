"""Tests unitaires pour l'extraction des détenus."""

from __future__ import annotations

from pathlib import Path

import pytest

from listedetenus.csv_writer import write_csv
from listedetenus.models import Detainee
from listedetenus.parser import tables_to_detainees


def test_tables_to_detainees_extracts_rows(tmp_path: Path) -> None:
    table = [
        ["Nom", "Prénom", "Date de naissance"],
        ["ABAS", "Lena", "05/09/1981"],
        ["ZEE", "Mara", "1990-12-01"],
    ]
    detainees = tables_to_detainees([table])
    assert detainees == [
        Detainee(nom="ABAS", prenom="Lena", date_naissance="1981-09-05"),
        Detainee(nom="ZEE", prenom="Mara", date_naissance="1990-12-01"),
    ]

    csv_path = tmp_path / "detenus.csv"
    write_csv(csv_path, detainees)
    content = csv_path.read_text(encoding="utf-8").splitlines()
    assert content[0] == "nom,prenom,date_naissance"
    assert "ABAS,Lena,1981-09-05" in content[1]


def test_tables_to_detainees_raises_when_no_valid_rows() -> None:
    table = [
        ["Nom", "Prénom", "Date de naissance"],
        ["", "", ""],
    ]
    with pytest.raises(ValueError):
        tables_to_detainees([table])


def test_tables_to_detainees_ignores_tables_without_headers() -> None:
    tables = [
        [["Autre", "Champs"], ["X", "Y"]],
        [["Nom", "Prénom", "Date de naissance"], ["AA", "BB", "01/01/90"]],
    ]
    detainees = tables_to_detainees(tables)
    assert detainees == [
        Detainee(nom="AA", prenom="BB", date_naissance="1990-01-01")
    ]

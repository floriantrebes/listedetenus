"""Tests du flux de conversion PDF vers CSV."""

from __future__ import annotations

from pathlib import Path

import pytest

from listedetenus import workflow
from listedetenus.models import PdfExtractionResult


def test_convert_pdf_to_csv_success(monkeypatch, tmp_path):
    pdf_path = tmp_path / "source.pdf"
    csv_path = tmp_path / "export" / "result.csv"

    def fake_read(path: Path) -> PdfExtractionResult:
        assert path == pdf_path.resolve()
        return PdfExtractionResult(source=path, tables=[["table"]])

    def fake_tables_to_detainees(tables: list[list[list[str]]]) -> list[str]:
        assert tables == [["table"]]
        return ["payload"]

    captured: dict[str, object] = {}

    def fake_write(path: Path, data: list[str]) -> None:
        captured["path"] = path
        captured["data"] = data

    monkeypatch.setattr(workflow, "read_pdf_tables", fake_read)
    monkeypatch.setattr(
        workflow, "tables_to_detainees", fake_tables_to_detainees
    )
    monkeypatch.setattr(workflow, "write_csv", fake_write)

    result = workflow.convert_pdf_to_csv(pdf_path, csv_path)

    assert result == csv_path.resolve()
    assert captured["path"] == csv_path.resolve()
    assert captured["data"] == ["payload"]
    assert csv_path.parent.exists()


def test_convert_pdf_to_csv_requires_csv_extension(tmp_path):
    pdf_path = tmp_path / "source.pdf"
    invalid_csv = tmp_path / "export.txt"

    with pytest.raises(ValueError):
        workflow.convert_pdf_to_csv(pdf_path, invalid_csv)


def test_convert_pdf_to_csv_rejects_file_as_parent(tmp_path):
    pdf_path = tmp_path / "source.pdf"
    parent_file = tmp_path / "existing"
    parent_file.write_text("content")
    target_csv = parent_file / "result.csv"

    with pytest.raises(ValueError):
        workflow.convert_pdf_to_csv(pdf_path, target_csv)

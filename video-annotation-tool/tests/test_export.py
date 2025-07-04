"""
Teste unitário para validação do módulo de exportação.
"""

import pandas as pd
from core.export import AnnotationExporter

def test_export_csv(tmp_path):
    data = [
        {"frame": 1, "label": "Evento A"},
        {"frame": 2, "label": "Evento B"}
    ]
    filepath = tmp_path / "test_output.csv"
    AnnotationExporter.export_to_csv(data, filepath)

    # Verifica se o arquivo foi criado
    assert filepath.exists(), "Arquivo CSV não foi criado."

    # Verifica conteúdo
    df = pd.read_csv(filepath)
    assert df.shape == (2, 2)
    assert list(df.columns) == ["frame", "label"]

def test_export_excel(tmp_path):
    data = [
        {"frame": 10, "label": "Evento X"},
        {"frame": 20, "label": "Evento Y"}
    ]
    filepath = tmp_path / "test_output.xlsx"
    AnnotationExporter.export_to_excel(data, filepath)

    # Verifica se o arquivo foi criado
    assert filepath.exists(), "Arquivo Excel não foi criado."

    # Verifica conteúdo
    df = pd.read_excel(filepath)
    assert df.shape == (2, 2)
    assert list(df.columns) == ["frame", "label"]

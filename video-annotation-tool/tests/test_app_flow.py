"""
Teste de fluxo básico da aplicação de anotação.
"""

import tkinter as tk
from ui.annotation_table import AnnotationTable
from ui.cell_editor import CellEditor


def test_full_annotation_flow():
    root = tk.Tk()

    params = [("label", "str"), ("valor", "int")]
    table = AnnotationTable(root, parameters=params)

    # Inserir anotações simuladas
    table.insert_annotation(0)
    table.update_annotation(0, "label", "Evento Teste")
    table.update_annotation(0, "valor", 42)

    data = table.export_data()

    assert data[0]["frame"] == 0
    assert data[0]["label"] == "Evento Teste"
    assert data[0]["valor"] == 42

    # Simula edição (teste básico, sem abrir janela real)
    editor = CellEditor(table.tree, table, params)
    assert editor.parameters == {"label": "str", "valor": "int"}

    root.destroy()

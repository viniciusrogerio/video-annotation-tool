"""
Teste unitário para o módulo de tabela de anotação.
"""

from ui.annotation_table import AnnotationTable
import tkinter as tk


def test_annotation_table_insertion():
    root = tk.Tk()
    table = AnnotationTable(root, parameters=[("label", "str")])

    table.insert_annotation(5)
    table.insert_annotation(10)

    data = table.export_data()

    assert len(data) == 2
    assert data[0]["frame"] == 5
    assert data[1]["frame"] == 10

    root.destroy()


def test_annotation_table_update():
    root = tk.Tk()
    table = AnnotationTable(root, parameters=[("label", "str")])

    table.insert_annotation(7)
    table.update_annotation(7, "label", "Teste")

    data = table.export_data()

    assert data[0]["label"] == "Teste"

    root.destroy()

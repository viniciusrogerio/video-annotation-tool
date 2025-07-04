"""
Módulo para exportação de anotações para CSV e Excel.
"""

import pandas as pd

class AnnotationExporter:
    """
    Classe utilitária para exportação de anotações em formatos CSV e Excel.
    """
    @staticmethod
    def export_to_csv(data, filepath):
        """Exporta os dados de anotações para um arquivo CSV."""
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)

    @staticmethod
    def export_to_excel(data, filepath):
        """Exporta os dados de anotações para um arquivo Excel."""
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)


if __name__ == "__main__":

    sample_data = [
        {"frame": 1, "label": "Evento A"},
        {"frame": 5, "label": "Evento B"}
    ]
    AnnotationExporter.export_to_csv(sample_data, "teste_export.csv")
    AnnotationExporter.export_to_excel(sample_data, "teste_export.xlsx")

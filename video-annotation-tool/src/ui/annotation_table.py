"""
Tabela de anotações para inserir e visualizar dados por frame.
"""

import tkinter as tk
from tkinter import ttk

class AnnotationTable(ttk.Frame):
    """Classe para exibir e gerenciar anotações de vídeo.
    Permite inserir, atualizar e exportar dados de anotações.
    """
    def __init__(self, master, parameters, *args, **kwargs):
        """
        Inicializa a tabela de anotações.
        :param master: Janela pai onde a tabela será exibida.
        :param parameters: Lista de tuplas (nome, tipo) para os parâmetros de anotação.
        """
        super().__init__(master, *args, **kwargs)
        self.parameters = parameters
        self.data = []

        self.columns = ["frame"] + [name for name, _ in parameters]
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def insert_annotation(self, frame_index):
        """Insere uma nova anotação para o frame especificado.
        Evita duplicatas para o mesmo frame.
        :param frame_index: Índice do frame onde a anotação será inserida.
        """
        if any(row["frame"] == frame_index for row in self.data):
            return  # evitar duplicatas
        row = {"frame": frame_index}
        for name, _ in self.parameters:
            row[name] = ""
        self.data.append(row)
        values = [row[col] for col in self.columns]
        self.tree.insert("", "end", iid=str(frame_index), values=values)

    def update_annotation(self, frame_index, param_name, value):
        """
        Atualiza o valor de um parâmetro para o frame especificado.
        :param frame_index: Índice do frame a ser atualizado.
        :param param_name: Nome do parâmetro a ser atualizado.
        :param value: Novo valor para o parâmetro.
        """
        for row in self.data:
            if row["frame"] == frame_index:
                row[param_name] = value
                break
        values = [row[col] for col in self.columns if row["frame"] == frame_index]
        self.tree.item(str(frame_index), values=values)

    def export_data(self):
        """
        Exporta os dados de anotações para uma lista de dicionários.
        Cada dicionário representa um frame com seus parâmetros.
        :return: Lista de dicionários com os dados de anotações.
        """
        self.data.sort(key=lambda x: x["frame"])
        return self.data

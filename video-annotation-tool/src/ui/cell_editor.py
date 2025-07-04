
"""
Editor de células para editar valores na tabela de anotação.
"""

from tkinter import simpledialog, messagebox

class CellEditor:
    """
    Classe para editar células na tabela de anotações.
    Permite editar valores de parâmetros específicos ao dar um duplo clique na célula.
    """
    def __init__(self, tree, annotation_table, parameters):
        """
        Inicializa o editor de células.
        :param tree: A árvore (Treeview) onde as anotações são exibidas.
        :param annotation_table: A tabela de anotações que contém os dados.
        :param parameters: Dicionário de parâmetros com seus tipos (int, float, str).
        """
        self.tree = tree
        self.annotation_table = annotation_table
        self.parameters = dict(parameters)

        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        """
        Método chamado ao dar um duplo clique em uma célula da tabela.
        Abre um diálogo para editar o valor do parâmetro correspondente.
        :param event: Evento de clique duplo.
        """
        # Verifica se o clique foi em uma célula válida
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        col_index = int(col.replace("#", "")) - 1

        if col_index == 0:
            return  # não edita coluna de frame

        param_name = self.tree["columns"][col_index]
        frame_index = int(row_id)
        param_type = self.parameters[param_name]

        value = simpledialog.askstring("Editar Valor", f"Novo valor para '{param_name}' (tipo {param_type}):")
        if value is None:
            return

        try:
            if param_type == "int":
                value = int(value)
            elif param_type == "float":
                value = float(value)
            # se for string, não faz nada
        except ValueError:
            messagebox.showerror("Erro", f"Valor inválido para tipo {param_type}.")
            return

        self.annotation_table.update_annotation(frame_index, param_name, value)

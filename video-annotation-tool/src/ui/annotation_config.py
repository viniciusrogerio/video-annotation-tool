"""
Interface para configuração dos parâmetros de anotação.
"""

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class AnnotationConfigDialog(tk.Toplevel):
    """
    Diálogo para configurar os parâmetros de anotação.
    Permite adicionar, remover e confirmar parâmetros de anotação.
    """
    def __init__(self, master, on_confirm):
        """
        Inicializa o diálogo de configuração de anotação.
        :param master: Janela pai do diálogo.
        :param on_confirm: Função a ser chamada ao confirmar os parâmetros.
        """
        super().__init__(master)
        self.title("Configurar Anotação")
        self.geometry("400x400")

        self.on_confirm = on_confirm
        self.parameters = []

        self.create_widgets()

    def create_widgets(self):
        """
        Cria os widgets do diálogo de configuração.
        Inclui uma tabela para exibir os parâmetros e botões para adicionar/remover.
        """
        frame = ttk.LabelFrame(self, text="Parâmetros de Anotação")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame, columns=("Tipo"), show="headings")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        add_button = ttk.Button(button_frame, text="Adicionar", command=self.add_parameter)
        add_button.pack(side=tk.LEFT, padx=5)

        remove_button = ttk.Button(button_frame, text="Remover", command=self.remove_parameter)
        remove_button.pack(side=tk.LEFT, padx=5)

        confirm_button = ttk.Button(self, text="Confirmar", command=self.confirm)
        confirm_button.pack(pady=10)

    def add_parameter(self):
        """
        Abre um diálogo para adicionar um novo parâmetro de anotação.
        Solicita o nome e o tipo do parâmetro (int, float, str).
        """
        name = simpledialog.askstring("Nome do Parâmetro", "Digite o nome:")
        if not name:
            return
        param_type = simpledialog.askstring("Tipo do Parâmetro", "Digite o tipo (int, float, str):")
        if param_type not in ["int", "float", "str"]:
            messagebox.showerror("Erro", "Tipo inválido.")
            return

        self.tree.insert("", "end", iid=name, values=(param_type,))
        self.parameters.append((name, param_type))

    def remove_parameter(self):
        """
        Remove o parâmetro selecionado da tabela.
        Se nenhum parâmetro estiver selecionado, não faz nada.
        """
        selected = self.tree.selection()
        for item in selected:
            self.tree.delete(item)
            self.parameters = [p for p in self.parameters if p[0] != item]

    def confirm(self):
        """
        Confirma os parâmetros de anotação e fecha o diálogo.
        Chama a função on_confirm com os parâmetros configurados.
        """
        self.on_confirm(self.parameters)
        self.destroy()

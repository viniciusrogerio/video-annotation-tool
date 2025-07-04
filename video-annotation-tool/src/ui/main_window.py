import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ui.video_controls import VideoControls
from ui.annotation_config import AnnotationConfigDialog
from ui.annotation_table import AnnotationTable
from ui.cell_editor import CellEditor
from core.export import AnnotationExporter
from PIL import Image, ImageTk
import cv2

class VideoAnnotationApp(tk.Tk):
    """
    Classe principal da aplicação de anotação de vídeo.
    Permite carregar vídeos, navegar entre frames, anotar e exportar dados.
    """
    def __init__(self):
        """
        Inicializa a aplicação e configura a janela principal.
        Cria os widgets necessários para a interface do usuário.
        """
        super().__init__()

        self.title("Video Annotation Tool")
        self.geometry("1280x900")

        self.video_cap = None
        self.video_path = None
        self.current_frame = 0

        self.parameters = []
        self.annotation_table = None

        self.create_widgets()

    def create_widgets(self):
        """
        Cria os widgets da interface do usuário.
        Inclui controles de vídeo, canvas para exibição de frames,
        botões para configuração de anotações, anotação do frame atual e exportação de CSV.
        """
        self.configure(bg="white")
        title_label = ttk.Label(
            self,
            text="Ferramenta de Anotação de Vídeos",
            font=("Helvetica", 18, "bold")
        )
        title_label.pack(pady=10)

        self.video_controls = VideoControls(
            self,
            on_video_loaded=self.on_video_loaded,
            on_frame_change=self.change_frame
        )
        self.video_controls.pack(pady=10)

        self.canvas = tk.Canvas(self, width=960, height=540, bg="black")
        self.canvas.pack(pady=10)

        self.info_label = ttk.Label(self, text="Frame: 0 | Tempo: 0.00 s")
        self.info_label.pack(pady=5)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        config_btn = ttk.Button(btn_frame, text="Configurar Anotação", command=self.open_annotation_config)
        config_btn.pack(side=tk.LEFT, padx=5)

        annotate_btn = ttk.Button(btn_frame, text="Anotar Frame Atual", command=self.annotate_current_frame)
        annotate_btn.pack(side=tk.LEFT, padx=5)

        export_btn = ttk.Button(btn_frame, text="Exportar CSV", command=self.export_csv)
        export_btn.pack(side=tk.LEFT, padx=5)

    def on_video_loaded(self, cap, filepath):
        """
        Método chamado quando um vídeo é carregado.
        Configura o objeto de captura de vídeo e exibe o primeiro frame.
        :param cap: Objeto de captura de vídeo do OpenCV.
        :param filepath: Caminho do arquivo de vídeo carregado.
        """
        self.video_cap = cap
        self.video_path = filepath
        self.current_frame = 0
        self.show_frame()
        self.video_controls.slider.set(0)

    def show_frame(self):
        """
        Exibe o frame atual do vídeo no canvas.
        Atualiza a informação do frame e tempo exibida na label.
        """
        if not self.video_cap:
            return

        self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        ret, frame = self.video_cap.read()

        if not ret:
            messagebox.showerror("Erro", "Não foi possível ler o frame do vídeo.")
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        photo = ImageTk.PhotoImage(image=image)
        self.canvas.config(width=frame.shape[1], height=frame.shape[0])

        self.canvas.image = photo
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)

        fps = self.video_cap.get(cv2.CAP_PROP_FPS) or 30
        seconds = self.current_frame / fps
        self.info_label.config(text=f"Frame: {self.current_frame} | Tempo: {seconds:.2f} s")

    def change_frame(self, direction):
        """
        Muda o frame atual do vídeo.
        Permite navegar para frente ou para trás no vídeo.
        :param direction: Número de frames a serem movidos (positivo para frente, negativo para trás).
        """
        if not self.video_cap:
            return

        total_frames = int(self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        new_frame = self.current_frame + direction

        if 0 <= new_frame < total_frames:
            self.current_frame = new_frame
            self.show_frame()

        self.video_controls.slider.set(self.current_frame)

    def open_annotation_config(self):
        """
        Abre o diálogo de configuração de anotações.
        Permite ao usuário definir os parâmetros de anotação e inicializa a tabela de anotações.
        """
        def on_confirm(params):
            self.parameters = params
            if self.annotation_table:
                self.annotation_table.destroy()
            self.annotation_table = AnnotationTable(self, params)
            self.annotation_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            CellEditor(self.annotation_table.tree, self.annotation_table, params)
        AnnotationConfigDialog(self, on_confirm)

    def annotate_current_frame(self):
        """
        Insere uma anotação para o frame atual.
        Verifica se a tabela de anotações está configurada e insere a anotação.
        Se a tabela não estiver configurada, exibe um aviso.
        """
        if not self.annotation_table:
            messagebox.showwarning("Aviso", "Configuração de anotação não definida.")
            return
        self.annotation_table.insert_annotation(self.current_frame)

    def export_csv(self):
        """
        Exporta os dados de anotações para um arquivo CSV.
        Solicita ao usuário um caminho para salvar o arquivo e exporta os dados da tabela de anotações.
        Se a tabela de anotações não estiver configurada, exibe um aviso.
        """
        if not self.annotation_table:
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filepath:
            data = self.annotation_table.export_data()
            AnnotationExporter.export_to_csv(data, filepath)
            messagebox.showinfo("Exportação", "Arquivo exportado com sucesso.")


if __name__ == "__main__":
    app = VideoAnnotationApp()
    app.mainloop()

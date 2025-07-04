import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2

class VideoControls(ttk.Frame):
    """
    Classe para controles de vídeo.
    Permite carregar vídeos, navegar entre frames e ajustar o slider de frames.
    """
    def __init__(self, master, on_video_loaded, on_frame_change, *args, **kwargs):
        """
        Inicializa os controles de vídeo.
        :param master: Janela pai onde os controles serão exibidos.
        :param on_video_loaded: Função a ser chamada quando um vídeo é carregado.
        :param on_frame_change: Função a ser chamada ao mudar de frame.
        """
        super().__init__(master, *args, **kwargs)
        self.on_video_loaded = on_video_loaded
        self.on_frame_change = on_frame_change
        self.cap = None

        self.create_widgets()

    def create_widgets(self):
        """
        Cria os widgets dos controles de vídeo.
        Inclui botões para carregar vídeo, navegar entre frames e um slider para selecionar frames.
        """
        self.pack(fill=tk.X, padx=5, pady=5)
        load_button = ttk.Button(self, text="Carregar Vídeo", command=self.load_video)
        load_button.pack(side=tk.LEFT, padx=5)

        prev_button = ttk.Button(self, text="Frame Anterior", command=self.prev_frame)
        prev_button.pack(side=tk.LEFT, padx=5)

        next_button = ttk.Button(self, text="Próximo Frame", command=self.next_frame)
        next_button.pack(side=tk.LEFT, padx=5)

        self.slider = ttk.Scale(self, from_=0, to=100, orient="horizontal", command=self.on_slider_move)
        self.slider.pack(fill=tk.X, padx=5)

    def on_slider_move(self, value):
        """
        Método chamado quando o slider é movido.
        Atualiza o frame atual com base no valor do slider.
        :param value: Valor do slider (posição do frame).
        """
        if self.cap:
            frame = int(float(value))
            if frame != self.master.current_frame:
                self.on_frame_change(frame - self.master.current_frame)

    def load_video(self):
        """
        Carrega um vídeo a partir de um arquivo selecionado pelo usuário.
        Abre um diálogo para selecionar o arquivo de vídeo e inicializa o objeto de captura de vídeo.
        """
        self.release_video()
        filepath = filedialog.askopenfilename(filetypes=[("Vídeos", "*.mp4 *.avi *.mov")])
        if not filepath:
            return

        cap = cv2.VideoCapture(filepath)
        if not cap.isOpened():
            messagebox.showerror("Erro", "Não foi possível abrir o vídeo.")
            return

        self.cap = cap
        self.slider.config(to=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1)
        messagebox.showinfo("Sucesso", f"Vídeo carregado com sucesso: {filepath}")
        self.on_video_loaded(cap, filepath)

    def prev_frame(self):
        """
        Muda para o frame anterior do vídeo.
        Chama a função de mudança de frame com -1 para navegar para trás.
        """
        if self.cap:
            self.on_frame_change(-1)

    def next_frame(self):
        """
        Muda para o próximo frame do vídeo.
        Chama a função de mudança de frame com +1 para navegar para frente.
        """
        if self.cap:
            self.on_frame_change(1)

    def release_video(self):
        """
        Libera os recursos do vídeo.
        Fecha o objeto de captura de vídeo se estiver aberto.
        """
        if self.cap:
            self.cap.release()
            self.cap = None

"""
Módulo para abstração de operações com vídeos (controle de frames).
"""

import cv2

class VideoHandler:
    def __init__(self, filepath):
        """Inicializa o manipulador de vídeo.

        :param filepath: Caminho do arquivo de vídeo.
        :raises IOError: Se não for possível abrir o vídeo.
        """
        self.filepath = filepath
        self.cap = cv2.VideoCapture(filepath)

        if not self.cap.isOpened():
            raise IOError(f"Não foi possível abrir o vídeo: {filepath}")

    def get_total_frames(self):
        """Retorna o número total de frames no vídeo."""
        return int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def read_frame(self, frame_index):
        """Lê um frame específico do vídeo.

        :param frame_index: Índice do frame a ser lido (0 baseado).
        :return: Frame lido como uma imagem (numpy array).
        :raises ValueError: Se o frame não puder ser lido.
        """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = self.cap.read()
        if not ret:
            raise ValueError(f"Não foi possível ler o frame {frame_index}.")
        return frame

    def release(self):
        """Libera os recursos do vídeo."""
        self.cap.release()

    def __del__(self):
        """Garante que os recursos sejam liberados ao destruir o objeto."""
        self.release()

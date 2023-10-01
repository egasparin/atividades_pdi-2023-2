#!opencv-headless/bin/python3

import numpy as np
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QSlider, QGridLayout, QHBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtCore import Qt 

# Variáveis globais para os valores dos TrackBars
low_pass_filter = 0
high_pass_filter = 0

class ImageConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Conversor de Imagens")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()

        # Layout da imagem no centro
        central_layout = QVBoxLayout()
        self.image_label = QLabel()
        central_layout.addWidget(self.image_label)
        
        # Layout dos botoes da esquerda
        left_layout = QVBoxLayout()
        left_label = QLabel("Funções disponiveis")
        left_itens = QGridLayout()

        # Lista de botões
        # Botão para carregar a imagem
        self.load_button = QPushButton("Carregar Imagem")
        self.load_button.clicked.connect(self.load_image)
        self.load_button.setMaximumWidth(400)
        left_itens.addWidget(self.load_button, 0, 0)
        # Botão para converter de RGB para HSV
        self.convert_button = QPushButton("Converter para HSV")
        self.convert_button.clicked.connect(self.convert_bgr2hsv)
        self.convert_button.setMaximumWidth(400)
        left_itens.addWidget(self.convert_button, 1, 0)
        # Botão para converter de colorido para escala de cinza
        self.convert_button = QPushButton("Converter para Escala de Cinza")
        self.convert_button.clicked.connect(self.convert_bgr2gray)
        self.convert_button.setMaximumWidth(400)
        left_itens.addWidget(self.convert_button, 2, 0)

        # criando uma trackbar (slidebar) que altera o valor da função trackar_changed
        self.trackbar = QSlider(Qt.Horizontal)
        self.trackbar.setMaximumWidth(400)
        left_itens.addWidget(self.trackbar, 3, 0)
        # Conecte a trackbar ao evento de valor alterado
        self.trackbar.valueChanged.connect(self.trackbar_changed)

        # adicionando o label e os itens da lista da esquerda
        left_layout.addWidget(left_label)
        left_layout.addLayout(left_itens)

        # Adicione os layouts à janela principal
        main_layout.addLayout(left_layout)
        main_layout.addLayout(central_layout)

        central_widget.setLayout(main_layout)

        self.loaded_image = None
        

    def trackbar_changed(self, value):
        # atualiza o titulo do slider para o valor atual do slider
        self.title_label.setText(f"Valor Atual: {value}")

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Imagem", "", "Imagens (*.png *.jpg *.jpeg *.bmp *.gif);;Todos os arquivos (*)", options=options)

        if file_path:
            self.loaded_image = cv2.imread(file_path)
            if self.loaded_image is not None:
                self.display_image(self.loaded_image)

    # a funcao abaixo recebe uma imagem e exibe esta na tela
    def display_image(self, image):
        if image is not None:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # caso a imagem seja colorida (rgb ou hsv) deve-se usar o QImage.Format_RGB888
        if(len(image.shape) == 3):
            height, width, channel = image.shape
            QImageParameter = QImage.Format_RGB888
            bytes_per_line = 3 * width
        # caso a imagem seja em tons de cinza deve-se usar o QImage.Format_Grayscale8
        else:
            height, width = image.shape
            QImageParameter = QImage.Format_Grayscale8
            bytes_per_line = width
        
        # enviado a imatem para o buffer de exibicao
        q_image = QImage(image.data, width, height, bytes_per_line, QImageParameter)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

    def convert_bgr2hsv(self, image):
        if image is not None:
            hsv_image = cv2.cvtColor(self.selected_image, cv2.COLOR_BGR2HSV)
            return hsv_image 
    
    # tem que adaptar as funções para que estas retornem uma imagem util para outra função
    def convert_bgr2gray(self, image):
        if image is not None:
            grayscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            # self.display_image(image=grayscale_image)
            return grayscale_image
        
    
    def filter_gaussian_blur(self, image, kernel_size):
        # verifica se a imagem esta em escala de cinza
        if len(image.shape) != 2:
            image = cv2.cvtColor(self.loaded_image, cv2.COLOR_BGR2GRAY)
        # com a imagem em tons de cinza, realiza a operacao
        blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        return blurred

    # def apply_threshold(self, threshold_value): binarizacao
    def apply_threshold(self, image):

        threshold_value = 127
        # Verifica se a imagem esta em escala de cinza
        if len(image.shape) != 2:
            image = cv2.cvtColor(self.loaded_image, cv2.COLOR_BGR2GRAY)
        
        # com a imagem convertida aplica-se o threshold com o limiar estipulado
        _, thresholded_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
        # retorna a imagem com o threshold aplicado
        return thresholded_image
    
    def aply_erode(self, image):
        kernel = np.ones((3,3), np.uint8) 

        if len(image.shape) != 2:
            image = self.apply_threshold(self, image)

        binary = cv2.erode(image, kernel, iterations=4)
        return binary

    def aply_dilate(self, image):
        kernel = np.ones((3,3), np.uint8) 

        if len(image.shape) != 2:
            image = self.apply_threshold(self, image)

        binary = cv2.dilate(image, kernel, iterations=4)
        return binary
    
    def draw_contours(self, image):
        if len(image.shape) != 2:
            image = cv2.cvtColor(self.loaded_image, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return contours

def main():
    app = QApplication(sys.argv)
    window = ImageConverterApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

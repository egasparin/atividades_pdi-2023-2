#!opencv-headless/bin/python3

## O QUE FALTA FAZER: 
## - APRESENTAR OS VALORES DOS ARGUMENTOS DO METODO: KERNEL, LIMIAR ..
## - ALTERAR OS VALORES AO SELECIONAR NA LISTA


import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QListWidget,
    QSlider,
)
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np


class Operation:
    def __init__(self, nome, *args,):
        self.nome = nome
        self.args = args

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_image = None
        self.selected_elements = []
        self.selected_operation = None
        
        # Variáveis globais para os valores dos TrackBars
        self.atribute_one = 11
        self.atribute_two = 11

        self.default_operations =  [
            Operation("Converter para HSV", 0, 0),
            Operation("Converter para Cinza", 0 , 0),
            Operation("Filtro Gaussian Blur\n\tArg1: Kernel\n\tArg2: SigmaX", 21, 11), 
            Operation("Detectar Bordas Canny\n\tArg1: Limiar Mínimo\n\tArg2: Limiar Máximo", 255, 255), 
            Operation("Binarizar Imagem\n\tArg1: Limiar", 255, 0),  
            Operation("Morfologia Matemática - erosão\n\tArg1: Kernel\n\tArg2: Iterações", 21, 21),
            Operation("Morfologia Matemática - dilatação\n\tArg1: Kernel\n\tArg2: Iterações", 21, 21)
        ]

        self.setWindowTitle("Trabalho Bimestral")
        self.setGeometry(100, 100, 1000, 1000)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # Layout principal
        main_layout = QHBoxLayout()

        # Layout da imagem no centro
        self.central_layout = QVBoxLayout()
        self.image_frame = QLabel()
        self.image_frame.setAlignment(Qt.AlignCenter)
        self.image_frame.setStyleSheet("background-color: white; border: 0.5px solid gray; padding: 5px;")
        self.image_frame.setMaximumWidth(600)
        self.central_layout.addWidget(self.image_frame)

        ######################################################
        #  AREA LATERAL QUE TEM AS OPERAÇÕES E O HISTORICO  ##
        ######################################################

        # Área lateral para escolher elementos
        self.lateral_widget = QWidget()
        self.lateral_layout = QVBoxLayout()

        self.open_button = QPushButton("Abrir Imagem")
        self.open_button.clicked.connect(self.load_image)
        self.lateral_layout.addWidget(self.open_button)

        self.operation_list = QListWidget()
        self.operation_list.itemClicked.connect(self.apply_current_values) 
        # self.operation_list.itemClicked.connect(self.apply_current_operation) 
        self.lateral_layout.addWidget(self.operation_list)
        for operation in self.default_operations:
            self.operation_list.addItem(operation.nome)

        # criando as barras para seleção dos atributos
        # criando uma trackbar (slidebar) que altera o valor da função trackar_changed
        primeiro_selector = QHBoxLayout()
        self.trackbar_atribute_one = QSlider(Qt.Horizontal)
        self.trackbar_atribute_one.setRange(0,255)
        self.trackbar_atribute_one.setMaximumWidth(400)
        # Conecte a trackbar ao evento de valor alterado
        self.trackbar_atribute_one.valueChanged.connect(self.trackbar_changed_atribute_one)
        self.label_name_arg1 = QLabel("Arg1")
        self.label_value_arg1 = QLabel("0")
        primeiro_selector.addWidget(self.label_name_arg1)
        primeiro_selector.addWidget(self.trackbar_atribute_one)
        primeiro_selector.addWidget(self.label_value_arg1)
        self.lateral_layout.addLayout(primeiro_selector)
              
        # criando uma trackbar (slidebar) que altera o valor da função trackar_changed
        segundo_seletor = QHBoxLayout()
        self.trackbar_atribute_two = QSlider(Qt.Horizontal)
        self.trackbar_atribute_two.setRange(0,255)
        self.trackbar_atribute_two.setMaximumWidth(400)
        # Conecte a trackbar ao evento de valor alterado
        self.trackbar_atribute_two.valueChanged.connect(self.trackbar_changed_atribute_two)
        self.label_name_arg2 = QLabel("Arg2")
        self.label_value_arg2 = QLabel("0")
        segundo_seletor.addWidget(self.label_name_arg2)
        segundo_seletor.addWidget(self.trackbar_atribute_two)
        segundo_seletor.addWidget(self.label_value_arg2)
        self.lateral_layout.addLayout(segundo_seletor)

        self.open_button = QPushButton("Aplicar Operação")
        self.open_button.clicked.connect(self.apply_operation)
        self.lateral_layout.addWidget(self.open_button)

        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.remove_item)
        self.lateral_layout.addWidget(self.history_list)

        self.clear_button = QPushButton("Limpar Histórico")
        self.clear_button.clicked.connect(self.clear_history)
        self.lateral_layout.addWidget(self.clear_button)

        self.lateral_widget.setLayout(self.lateral_layout)
        # Definindo o tamanho da janela lateral
        self.lateral_widget.setMaximumWidth(400)
        
        # Adicione os layouts à janela principal
        main_layout.addWidget(self.lateral_widget)      
        main_layout.addLayout(self.central_layout)

        # Widget principal
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def trackbar_changed_atribute_one(self, value):
        # atualiza o titulo do slider para o valor atual do slider
        self.atribute_one = value
        self.label_value_arg1.setText(f"{value}")

    def trackbar_changed_atribute_two(self, value):
        # atualiza o titulo do slider para o valor atual do slider
        self.atribute_two = value
        self.label_value_arg2.setText(f"{value}")
        
    # def apply_current_operation(self, item):

    #     for operation in self.default_operations:
    #         if operation.nome == item.text():
    #             self.selected_operation = operation
    #             self.selected_operation.args  = (atribute_one, atribute_two)
    
    def apply_current_values(self, item):
        for operation in self.default_operations:
            if operation.nome == item.text():
                self.selected_operation = operation
                # atualiza o intervalo do slider
                self.trackbar_atribute_one.setRange(0,self.selected_operation.args[0])
                self.trackbar_atribute_two.setRange(0,self.selected_operation.args[1])
                # atualiza o valor do slider
                self.trackbar_atribute_one.setValue(0)
                self.trackbar_atribute_two.setValue(0)
                print(self.selected_operation.args)


    def apply_operation(self):
        if self.selected_image is not None:
            # if self.selected_operation not in self.selected_elements:
            if self.selected_operation:
                self.selected_operation.args  = (self.atribute_one, self.atribute_two)
                self.selected_elements.append(self.selected_operation)
                # self.history_list.addItem(self.selected_operation.nome)

                nome = self.selected_operation.nome.split('\n')
                if len(nome) == 3:
                    string = nome[0]
                    string += '\n' + nome[1] + ': ' + str(self.atribute_one)
                    string += '\n' + nome[2] + ': ' + str(self.atribute_two)
                if len(nome) == 2:
                    string = nome[0]
                    string += '\n' + nome[1] + ': ' + str(self.atribute_one)
                if len(nome) == 1:
                    string = nome[0]
                
                self.history_list.addItem(string)

                self.operations()

    def remove_item(self, item=None):
        self.history_list.takeItem(self.history_list.row(item))
        
        for operation in self.default_operations:
            if operation.nome.split('\n')[0] == item.text().split('\n')[0]:
                self.selected_operation = operation
                self.selected_elements.remove(operation)
        
        self.operations()

    def clear_history(self):
        self.history_list.clear()
        self.selected_elements.clear()
        self.operations()

    def operations(self):
        image = self.selected_image.copy()

        for element in self.selected_elements:
            if element.nome == "Converter para HSV" and len(image.shape) == 3:
                hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                image = hsv_image

            if element.nome == "Converter para Cinza" and len(image.shape) == 3:
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                image = gray_image
                 
            if element.nome.split('\n')[0] == "Filtro Gaussian Blur":
                # Implemente o método de filtro aqui (por exemplo, filtro de suavização)
                # paramentros: imagem, tamanho do kernel, desvio padrão
                if element.args[0] % 2 == 0: 
                    kernel = (element.args[0] + 1, 
                              element.args[0] + 1)
                else: 
                    kernel = (element.args[0], 
                              element.args[0])
                sigmaX = element.args[1]
                filtered_image = cv2.GaussianBlur(image, kernel, sigmaX)
                image = filtered_image
                 
            if element.nome.split('\n')[0] == "Detectar Bordas Canny":
                # Implemente o método de detector de borda aqui (por exemplo, Canny)
                # parametros: imagem, limiar minimo, limiar maximo
                # if len(image.shape) == 2:
                #     image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                if element.args[0] < element.args[1]:
                    min_limiar = element.args[0]
                    max_limiar = element.args[1]
                else:
                    min_limiar = element.args[1]
                    max_limiar = element.args[0]

                edge_image= cv2.Canny(image, min_limiar, max_limiar)
                image = edge_image
               
            if element.nome.split('\n')[0] == "Binarizar Imagem":
                # Implemente o método de binarização aqui (por exemplo, limiar simples)
                limiar = element.args[0]
                _, binary_image = cv2.threshold(image, limiar, 255, cv2.THRESH_BINARY)
                image = binary_image
                print(f'Binarizar: Limiar - {limiar}')
            
            if element.nome.split('\n')[0] == "Morfologia Matemática - erosão":
                if element.args[0] % 2 == 0: 
                    kernel = (element.args[0] + 1, 
                              element.args[0] + 1)
                else: 
                    kernel = (element.args[0], 
                              element.args[0])
                iterations = element.args[1]
                
                erosion_image = cv2.erode(image, kernel, iterations)
                image = erosion_image
            
            if element.nome.split('\n')[0] == "Morfologia Matemática - dilatação":
                if element.args[0] % 2 == 0: 
                    kernel = (element.args[0] + 1, 
                              element.args[0] + 1)
                else: 
                    kernel = (element.args[0], 
                              element.args[0])
                iterations = element.args[1]

                erosion_image = cv2.dilate(image, kernel, iterations)
                image = erosion_image
              
        self.display_image(image)

     # a funcao abaixo recebe uma imagem e exibe esta na tela
    def display_image(self, image):
        # convertendo a imagem de BGR (padrao do Opencv) para RGB (padrão do Qt)
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
        q_image = q_image.scaledToWidth(600)
        pixmap = QPixmap.fromImage(q_image)
        self.image_frame.setPixmap(pixmap)

    
    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Imagem", "", "Imagens (*.png *.jpg *.jpeg *.bmp *.gif);;Todos os arquivos (*)", options=options)

        if file_path:
            try:
                self.selected_image = cv2.imread(file_path)
                self.display_image(self.selected_image)
            except Exception as e:
                print("Erro ao abrir a imagem:", str(e))
        else:
            print("Nenhuma imagem selecionada.")
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
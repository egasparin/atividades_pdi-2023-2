#!opencv-headless/bin/python
import os
import cv2
import numpy as np

## CARREGANDO OS ARQUIVOS

## CARACTERISTICAS DA IMAGEM ##

# Carregar a imagem
def loadImage(src):
    imagem = cv2.imread(src)
    return imagem

# Converter a imagem para tons de cinza
def convertToGray(img):
    if img is not None:
        if len(img.shape) == 3:
            # Converter a imagem para tons de cinza (escala de cinza)
            img_to_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return img_to_gray
        
        if len(img.shape) == 2:
            # se ja estiver em tons de cinza, retorna a imagem
            return img

## CARACTERISTICAS ESTRUTURAIS

# Binarizar a imagem
def binarization(img, limiar):

    if limiar is None:
        limiar = 127
    
    if img is not None:
        if len(img.shape) == 3:
            # Converter a imagem para tons de cinza (escala de cinza)
            img_to_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = img_to_gray
        
        if len(img.shape) == 2:
            binarized = cv2.threshold(img, limiar, 255, cv2.THRESH_BINARY)[1]
            return binarized

# Calcular o perimetro da imagem
def perimeter(img):
    if img is not None:
        if len(img.shape) == 3:
            # Converter a imagem para tons de cinza (escala de cinza)
            img_to_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = img_to_gray
        
        if len(img.shape) == 2:
            img_to_binary = binarization(img, limiar=127)
            
            # Encontre os contornos dos objetos
            contours, _ = cv2.findContours(
                img_to_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Calcule o perímetro do objeto (do primeiro objeto encontrado)
            perimeter = cv2.arcLength(contours[0], True)

            return perimeter

# Calcular a area da imagem
def area(img):
    if img is not None:
        if len(img.shape) == 3:
            # Converter a imagem para tons de cinza (escala de cinza)
            img_to_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = img_to_gray
        
        if len(img.shape) == 2:
            img_to_binary = binarization(img, limiar=127)
            
            # Encontre os contornos dos objetos
            contours, _ = cv2.findContours(
                img_to_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Calcule o perímetro do objeto (do primeiro objeto encontrado)
            area = cv2.contourArea(contours[0])

            return area

## CARACTERISTICAS ESTATISTICAS ##

# Calcular a média dos valores dos pixels de uma imagem em tons de cinza
def meanImage(img):
    if img is not None:
        if len(img.shape) == 3:
            img = convertToGray(img)
        
        if len(img.shape) == 2:
            mean = np.mean(img)
            return mean

# Calcular o desvio padrão dos valores dos pixels
def standardDeviation(img):
    if img is not None:
        if len(img.shape) == 3:
            img = convertToGray(img)
        
        if len(img.shape) == 2:
            standard_deviation = np.std(img)
            return standard_deviation

# Encontrar o valor mínimo e máximo dos pixels
def minAndMax(img):
    if img is not None:
        if len(img.shape) == 3:
            img = convertToGray(img)
        
        if len(img.shape) == 2:
            min_value = np.min(img)
            max_value = np.max(img)

            return min_value, max_value


# Calcular a uniformidade
def uniformity(img):
    if img is not None:
        if len(img.shape) == 3:
            img = convertToGray(img)
        
        if len(img.shape) == 2:
            unif = np.mean((img - meanImage(img)) ** 2)

            return unif

# Calcular a entropia
def entropy(img):
    if img is not None:
        if len(img.shape) == 3:
            img = convertToGray(img)
        
        if len(img.shape) == 2:
            histogram = cv2.calcHist([img], [0], None, [256], [0, 256])
            probabilities = histogram / np.sum(histogram)
            entropy = -np.sum(probabilities * np.log2(probabilities + np.finfo(float).eps))

            return entropy

## MATRIZ GLCM ##

# Calcule a matriz de co-ocorrência
def coOcorrencyMatrix(img, angle, distance):

    # Se a distancia nao é informada, atribui 1
    if distance is None:
        distance = 1

    # Se o angulo nao é informado, atribui-se 0
    if angle not in (0, 45, 90, 135):
        angle = 0
    # Se o angulo for informado dentro do esperado, 
    # atribui ao angulo o valor em radianos
    else:
        if angle == 0:
            angle = 0
        if angle == 45:
            angle = np.pi/4
        if angle == 90:
            angle = np.pi/2
        if angle == 135:
            angle = 3*np.pi/4

    # Se a imagem passada for colorida, converte para cinza
    if img is not None:
        if len(img.shape) == 3:
            img = convertToGray(img)

    # Recebendo a imagem em cinza, realiza-se as operações
        if len(img.shape) == 2:

            # Calcule a matriz de coocorrência
            height, width = img.shape
            cooccurrence_matrix = np.zeros((256, 256), dtype=np.uint32)

            for y in range(height):
                for x in range(width):
                    if x + distance < width and y - distance >= 0:
                        i = img[y, x]
                        j = img[y - distance, x + distance]
                        cooccurrence_matrix[i, j] += 1

            # Normalize a matriz de co-ocorrência (opcional)
            cooccurrence_matrix = cooccurrence_matrix / np.sum(cooccurrence_matrix)

            # Retorna a matriz de ocorrencia calculada
            return cooccurrence_matrix

# OS 14 DESCRITORES DE HARALICK (1973):
# 
# Contraste Angular: Mede a variação de intensidade entre um pixel e seus vizinhos em diferentes direções.
# Correlação: Mede a correlação linear de intensidades de pixels em diferentes direções.
# Variação de Intensidade: Indica a variação da intensidade dos pixels em diferentes direções.
# Momento Angular: Mede a uniformidade das intensidades dos pixels.
# Entropia: Mede o grau de desordem na distribuição de intensidades dos pixels.
# Informação de Medida: Mede a informação média fornecida pela distribuição de intensidades dos pixels.
# Medida de Homogeneidade: Mede o quão homogênea é a distribuição de intensidades dos pixels.
# Soma Média: A média das entradas da matriz de co-ocorrência.
# Soma das Variâncias: A soma das variações individuais para cada intensidade de pixel.
# Soma de Entropia: A entropia da distribuição de intensidades.
# Soma de Informação de Medida: A informação de medida da distribuição de intensidades.
# Soma de Medida de Homogeneidade: A medida de homogeneidade da distribuição de intensidades.
# Máximo de Probabilidade: O valor máximo da probabilidade de ocorrência de um par de intensidades.
# Contraste de Diferença Máxima: Mede o contraste entre os picos da probabilidade de ocorrência
# 
# Calcula os 14 descritores de Haralick (1973) e retorna em uma lista
def descriptorsGLCM(coocorrency_matrix):
    
    # Define a lista para retornar os descritores
    descritores = []

    if coocorrency_matrix is not None:
        contraste = np.sum(np.square(np.arange(256) - np.arange(256).reshape(-1, 1)) * coocorrency_matrix)
        correlacao = np.sum((np.arange(256) - np.mean(np.arange(256))) * (np.arange(256).reshape(-1, 1) - np.mean(np.arange(256))) * coocorrency_matrix) / (np.std(np.arange(256)) ** 2)
        variancia = np.sum(np.square(np.arange(256) - np.mean(np.arange(256))) * coocorrency_matrix)
        momento_angular = np.sum(np.square(coocorrency_matrix))
        entropia = -np.sum(coocorrency_matrix * np.log(coocorrency_matrix + 1e-10))
        medida_informacao = -np.sum(coocorrency_matrix * np.log(coocorrency_matrix + 1e-10))
        medida_homogeneidade = np.sum(coocorrency_matrix / (1 + np.square(np.arange(256) - np.arange(256).reshape(-1, 1))))
        soma_media = np.sum(coocorrency_matrix * np.arange(256))
        soma_variancias = np.sum(np.square(np.arange(256) - np.mean(np.arange(256))) * coocorrency_matrix)
        soma_entropia = -np.sum(coocorrency_matrix * np.log(coocorrency_matrix + 1e-10))
        soma_medida_informacao = -np.sum(coocorrency_matrix * np.log(coocorrency_matrix + 1e-10))
        soma_medida_homogeneidade = np.sum(coocorrency_matrix / (1 + np.square(np.arange(256) - np.arange(256).reshape(-1, 1))))
        maxima_probabilidade = np.max(coocorrency_matrix)
        contraste_diferenca_maxima = np.sum(coocorrency_matrix * np.square(np.arange(256) - np.arange(256).reshape(-1, 1)))

        descritores.append([contraste, correlacao, variancia, momento_angular, entropia,
                            medida_informacao, medida_homogeneidade, soma_media, soma_variancias,
                            soma_entropia, soma_medida_informacao, soma_medida_homogeneidade,
                            maxima_probabilidade, contraste_diferenca_maxima])

        return descritores
    
## As imagens foram selecionadas e copiadas para uma pasta denominada SELECIONADAS
#
# $ cd ./MAIUSCULAS && cp $(ls . | egrep "[A-Z]000.*" | awk '{print $9}') ~/SELECIONADAS/

if __name__ == "__main__":
    
    # Diretorio onde estao as imagens
    diretorio = './SELECIONADAS'

    # Lista que conterá todos os resultados
    resultados = ["Imagem","Area","Perimetro","Media","Desvio Padrão","Uniformidade","Entropia","Descritores[14]"]
    
    # Seleciona todos os arquivos no diretorio informado
    arquivos = os.listdir(diretorio)

    for arquivo in arquivos:

        with open('resultado.txt', 'a+') as fileTxt:
        # Imprime os elementos da lista
            for elemento in resultados:
                fileTxt.write(str(elemento) + ',')
            # Inicia uma nova linha
            fileTxt.write('\n')
    
        # Carrega a imagem
        img = loadImage(f'{diretorio}/{arquivo}')

        # Salva o nome do arquivo
        resultados[0] = arquivo

        # Caracteristicas estruturais 
        resultados[1] = area(img)
        resultados[2] = perimeter(img)

        # Estatisticas
        resultados[3] = meanImage(img)
        resultados[4] = standardDeviation(img)
        resultados[5] = uniformity(img)
        resultados[6] = entropy(img)

        # GLCM
        matriz_coocorrencia = coOcorrencyMatrix(img = img, angle=0, distance=1)
        descritores = descriptorsGLCM(matriz_coocorrencia)
        
        # Une a lista de resultados dos metodos anteriores e da lista de descritores
        resultados = resultados[0:6] + descritores[0]

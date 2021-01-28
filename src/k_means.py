# Manipulação dos dados
import pandas as pd

# Métrica v_measure_score
from sklearn.metrics.cluster import v_measure_score

# Funções para clustering utilizando PyClustering
# Importante: para realização do TP é imprescindível que seu PyClustering esteja na versão 0.10.1 ou superior
from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.utils.metric import distance_metric, type_metric

# Checa versão da biblioteca PyClustering
import pyclustering

def modelTrain(myFunction, clustersNumber, testData):
    X = testData
    # Instancia a função de distância
    metric = distance_metric(type_metric.USER_DEFINED, func=myFunction)
    # define número de clusters
    k = clustersNumber
    # Inicializa centróides utilizando método K-Means++
    initial_centers = kmeans_plusplus_initializer(X, k).initialize()
    # cria instância do K-Means utilizando sua métrica de distância
    kmeans_instance = kmeans(X, initial_centers, metric=metric)
    # treina o modelo
    kmeans_instance.process()
    # recupera os clusters gerados
    clusters = kmeans_instance.get_clusters()

    return clusters

def modelEvaluation(clusters, completeData, labelName):
    copyCompleteData = completeData[:]
    testData = copyCompleteData.drop([labelName], axis=1)
    """
    Importante: o índice do cluster gerado não é necessariamente
    a classe prevista por aquele cluster.
    """
    for i in range(len(clusters)):
        completeData.loc[clusters[i], 'y_pred'] = i
    
    # comparing with euclidian
    clustersEuclidian = modelTrain(euclidianDistance, 7, testData) # 7 for glass dataset, change it for the other one
    for i in range(len(clustersEuclidian)):
        copyCompleteData.loc[clustersEuclidian[i], 'y_pred'] = i
    
    #print('euclidian v-meausure:', v_measure_score(copyCompleteData[labelName], copyCompleteData.y_pred))

    # Calcula V-measure
    return v_measure_score(completeData[labelName], completeData.y_pred)

import math
def euclidianDistance(point1, point2):
    dimension = len(point1)
    sum = 0.0
    for i in range(dimension):
        sum += (point1[i] - point2[i])**2

    return math.sqrt(sum)
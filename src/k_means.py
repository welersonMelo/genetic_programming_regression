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
    """
    Importante: o índice do cluster gerado não é necessariamente
    a classe prevista por aquele cluster.
    """
    for i in range(len(clusters)):
        # Label prevista pelo cluster i
        completeData.loc[clusters[i], 'y_pred'] = completeData.loc[clusters[i]].groupby(labelName).size().idxmax()

    print('predicted:', completeData.y_pred)

    # Calcula V-measure
    return v_measure_score(completeData[labelName], completeData.y_pred)
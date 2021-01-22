# Manipulação dos dados
import pandas as pd

# Métrica v_measure_score
from sklearn.metrics.cluster import v_measure_score

# Funções para clustering utilizando PyClustering
# Importante: para realização do TP é imprescindível que seu PyClustering esteja na versão 0.10.1 ou superior
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.utils.metric import distance_metric, type_metric

# Checa versão da biblioteca PyClustering
import pyclustering
print(pyclustering.__version__ )

"""
O dataset iris não deve ser utilizado no desenvolvimento do Trabalho Prático
"""
# Leitura dos dados
df = pd.read_csv('iris.csv')
# Seleciona atributos a serem utilizados para clusterizar os dados
X = df.drop(['target'], axis=1)


# Modelo de função de distância aceita pela biblioteca PyClustering
def my_manhattan(point1, point2):
    """
    input:
        point1 e point2 = pontos utilizados no cálculo da distância
    output:
        result = distância entre os dois pontos
    """
    dimension = len(point1)
    result = 0.0
    for i in range(dimension):
        result += abs(point1[i] - point2[i]) * 0.1
    return result

def model_train_manhatan():
    # Instancia a função de distância
    manhattan_metric = distance_metric(type_metric.USER_DEFINED, func=my_manhattan)
    # define número de clusters
    k = 3
    # Inicializa centróides utilizando método K-Means++
    initial_centers = kmeans_plusplus_initializer(X, k).initialize()
    # cria instância do K-Means utilizando sua métrica de distância
    kmeans_instance = kmeans(X, initial_centers, metric=manhattan_metric)
    # treina o modelo
    kmeans_instance.process()
    # recupera os clusters gerados
    clusters = kmeans_instance.get_clusters()

def model_evaluation():
    """
    Importante: o índice do cluster gerado não é necessariamente
    a classe prevista por aquele cluster.
    """
    # Label prevista pelo cluster 0
    df.loc[clusters[0],'y_pred'] = df.loc[clusters[0]].groupby('target').size().idxmax()
    # Label prevista pelo cluster 1
    df.loc[clusters[1],'y_pred'] = df.loc[clusters[1]].groupby('target').size().idxmax()
    # Label prevista pelo cluster 2
    df.loc[clusters[2],'y_pred'] = df.loc[clusters[2]].groupby('target').size().idxmax()

    # Calcula FMI
    fowlkes_mallows_score(df.target, df.y_pred)

def model_train_euclidian():
    # define número de clusters
    k = 3
    # Inicializa centróides utilizando método K-Means++
    initial_centers = kmeans_plusplus_initializer(X, k).initialize()
    # cria instância do K-Means utilizando distância Euclidiana
    kmeans_instance = kmeans(X, initial_centers)
    # run cluster analysis and obtain results
    kmeans_instance.process()
    # recupera os clusters gerados
    clusters = kmeans_instance.get_clusters()

def model_evaluation_euclidian():
    # Label prevista pelo cluster 0
    df.loc[clusters[0],'y_pred'] = df.loc[clusters[0]].groupby('target').size().idxmax()
    # Label prevista pelo cluster 1
    df.loc[clusters[1],'y_pred'] = df.loc[clusters[1]].groupby('target').size().idxmax()
    # Label prevista pelo cluster 2
    df.loc[clusters[2],'y_pred'] = df.loc[clusters[2]].groupby('target').size().idxmax()

    # Calcula FMI
    fowlkes_mallows_score(df.target, df.y_pred)
import pandas as pd

def readCsv(path):
    # Leitura dos dados
    df = pd.read_csv(path)
    return df


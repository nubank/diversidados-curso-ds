import numpy as np
import pandas as pd
from sklearn import datasets

iris = datasets.load_iris()

rows = np.hstack((iris.data, iris.target.reshape((-1, 1))))
cols = iris.feature_names + ['especie']

translated_cols = {
    'sepal length (cm)': 'comprimento_sepala',
    'sepal width (cm)': 'largura_sepala',
    'petal length (cm)': 'comprimento_petala',
    'petal width (cm)': 'largura_petala'
}

species = {i: name for i, name in enumerate(iris.target_names)}

df = (
    pd
    .DataFrame(rows, columns=cols)
    .rename(columns=translated_cols)
    .replace({'especie': species})
)

df.to_csv('iris_pt_br.csv', index=False)

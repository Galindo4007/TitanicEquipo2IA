# -*- coding: utf-8 -*-
"""Titanic.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NFepcb1-8b_vJbMSVfQvapTyhtkZ-AVS

#Importacion de librerias
##import pandas as pd:

pandas es una biblioteca de Python para la manipulación y análisis de datos. Se utiliza para trabajar con estructuras de datos como DataFrames. Aquí se importa con el alias pd para simplificar su uso.
##import numpy as np:

numpy es una biblioteca para operaciones matemáticas y científicas en Python, especialmente para trabajar con arrays y matrices. Se importa con el alias np.
##import matplotlib.pyplot as plt:

matplotlib.pyplot es un módulo de la biblioteca matplotlib que proporciona funciones para crear gráficos y visualizaciones. Se importa con el alias plt.
##import seaborn as sbn:

seaborn es una biblioteca para la visualización de datos basada en matplotlib, que ofrece una interfaz de alto nivel para crear gráficos estadísticos. Se importa con el alias sbn.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

"""Este código carga tres archivos CSV en DataFrames: gender_submission.csv en df_gender, train.csv en df_train, y test.csv en df_test. Luego, imprime la forma (número de filas y columnas) del DataFrame df_gender y muestra las primeras 5 filas de df_gender para inspeccionar su contenido y estructura."""

df_train = pd.read_csv('train.csv')
df_test = pd.read_csv('test.csv')
print(df_train.shape)
df_train.head()

print(df_test.shape)
df_test.head()

count_na = df_train.isna().sum()
print('Cantidad de valores NaN en datos de entrenamiento:\n', count_na)

df_train.shape

"""En la columna de edad, hay 177 valores faltantes de un total de 891, lo que equivale al 19.86% de los datos en esa columna. Se consideraron dos cursos de acción para abordar este problema: imputación de datos o eliminación. Tras evaluar el modelo en ambos escenarios, se escogerá el que tenga mejor precisión. Para la imputación, utilizamos la mediana, agrupando los datos por clase y sexo, y así obtener la mediana de cada grupo. Esta se usó para llenar los datos faltantes, con cerca de seis combinaciones diferentes. Este método se consideró adecuado debido a la menor proporción de información faltante en esta columna.

La columna de cabina se eliminará dado que faltan 687 de 891 datos (77.1%), además de que esta columna no tiene mucha relevancia en los datos como otras columnas como lo son la edad, sexo, clase, etc. Bajo este mismo concepto, se eliminarán las columnas "Ticket" y "PassengerId" (esto dado que el numero de ticket realmente no significa mucho y el numero de pasajero es básicmanete como viene ordenado el dataset, por lo que tampoco aporta mucho).
"""

df_train = df_train.drop(['Ticket', 'Cabin', 'PassengerId'], axis=1)

print(df_train.shape)
df_train.head()

# Mapear los valores de 'Sex' a 0 para 'male' y 1 para 'female'
df_train['Sex bool'] = df_train['Sex'].map({'male': 0, 'female': 1})
df_train.head()

"""Ahora que ya tenemos la columna 'Sex bool' con datos numéricos para categorizar el sexo en solo 0 o 1, se puede proceder a eliminar la columna 'sex' para evitar tener datos redundantes o repetidos, dejando solo lo necesario para que funcione de buena manera nuestro modelo."""

df_train = df_train.drop(['Sex'], axis=1)

"""## Procesamiento de datos

Como muchos modelos de aprendizaje no pueden trabajar directamente con categorias y nuestro feature de Embarked clasifica nuestras instancias dependiendo de la ciudad de embarque, necesitamos un procesamiento que cambie las categorías por un dato más fácil de procesar.

"""

df_train = pd.get_dummies(df_train, columns=['Embarked'], dtype=int)
df_test = pd.get_dummies(df_test, columns=['Embarked'], dtype=int)
df_train.head()

# Uso de mapa de calor de seaborn para ver si hay correlación entre variables del dataset con la variable de supervivencia
sbn.heatmap(df_train.drop('Name', axis=1).corr(), annot=True)

"""Con este mapa de calor se puede ver que casi no hay correlación entre las variables de Embarked y la supervivencia, por lo que se puede decir que la supervivencia no depende mucho de estas variables, por lo que se podría optar por no hacerle mucho caso a esas variables. Sin embargo, hay una correlación lineal positiva con la variable 'Sex bool'que era la que habíamos definido para diferenciar entre hombre y mujer, por lo cual esta es una de las variables más importantes y definitivamente tiene que ser utilizada en el análisis. Dado que era muy común que las mujeres subieran a los botes salvavidas primero, esta correlación con la supervivencia hace sentido. Asimismo, la variable de Pclass que representa la clase económica de los pasajeros, también tiene algo de correlación, por lo que esta también debe ser tomada en cuenta. Lo mismo aplica para otras variables como edad y Fare (precio del ticket)."""

df_test = df_test.drop(['Ticket', 'Cabin', 'PassengerId', 'Embarked_C', 'Embarked_Q', 'Embarked_S'], axis=1)
df_train = df_train.drop(['Embarked_C', 'Embarked_Q', 'Embarked_S'], axis=1)

print(df_test.shape)
df_test.head()

"""Ahora que ya quitamos las columnas con datos redundantes o no relevantes, procedemos a probar el modelo. Como primera opción, lo probamos tras eliminar las instancias que tengan valores faltantes en la columna de edad, y como segunda opción lo probamos tras rellenar los valores faltantes de dicha columna.

Luego de esto, el modelo que demuestre mejor precisión será el que se va a utilizar.
"""

# Eliminación de valores faltantes en la columna "Age"
df_train_limp = df_train.dropna(axis=0)

# Confirmamos que ya no haya valores faltantes
count_na = df_train_limp.isna().sum()
print('Valores faltantes por columna:\n', count_na)

print(df_train_limp.shape)
df_train_limp

"""Como se puede observar, se han eliminado las instancias que tenían valores faltantes, pues las dimensiones del dataseframe se han reduido acorde a ello. Ahora se procede con el desarrollo y entrenamiento del modelo para evaluar su desempeño y decidir si se va a utilizar este modelo o el que se hará a continuación con rellenado de edades faltantes."""

# Antes hay que hacer lo mismo para el test set como lo hicimos para el train set.
df_test_limp = df_test.dropna(axis=0)

"""# Modelos"""

# Hay que actualizar el test set con la nueva columna tal como hicimos con el train set.
df_test['Sex bool'] = df_test['Sex'].apply(lambda x: 0 if x == 'male' else 1)

# Crear columna de 'Survived' en los datos de test para predecir dicha variable con nuestro modelo
df_test['Survived'] = 0

# Ahora sí, se procede con el modelo de regresión logística para predicción tras eliminar valores faltantes de edad
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

"""## Modelo de regresión logística tras eliminar edades faltantes"""

x = df_train_limp.drop(['Name', 'Survived'], axis=1)
y = df_train_limp['Survived']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

"""from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from scipy.stats import uniform

# Definir el espacio de búsqueda para los hiperparámetros
param_distributions = {
    'C': uniform(loc=0.1, scale=10.0),
    'solver': ['liblinear', 'lbfgs'],
    'max_iter': [1000, 1500, 2000]
}

# Crear el modelo
modelo_reg = LogisticRegression()

# Configurar la búsqueda aleatoria
random_search = RandomizedSearchCV(estimator=modelo_reg, param_distributions=param_distributions, n_iter=20, cv=5, scoring='accuracy', random_state=42)

# Ajustar la búsqueda a los datos de entrenamiento
random_search.fit(x_train, y_train)

# Obtener los mejores hiperparámetros
best_params = random_search.best_params_
print("Mejores hiperparámetros:", best_params)"""

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

# Crear el modelo de regresión logística con los mejores hiperparámetros
modelo_reg_best = LogisticRegression(
    C=1.528668179219408,
    max_iter=2000,
    solver='lbfgs'
)

# Entrenar el modelo con los datos de entrenamiento
modelo_reg_best.fit(x_train_scaled, y_train)

# Hacer predicciones en el conjunto de prueba
y_pred = modelo_reg_best.predict(x_test_scaled)

"""### Evaluación de exactitud y precisión del modelo"""

# Métricas
from sklearn import metrics
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score
print('Score de exactitud:', accuracy_score(y_test, y_pred))
print('Score de precisión:', precision_score(y_test, y_pred))
print('Score f1:', f1_score(y_test, y_pred))
print('Score de recall:', recall_score(y_test, y_pred))

# Matriz de confusión
from sklearn.metrics import confusion_matrix
mat = confusion_matrix(y_test, y_pred)
print(f'Confusion Matrix:\n{mat}')

# Reporte de clasificación
from sklearn.metrics import classification_report
reporte = classification_report(y_test, y_pred)
print(f'Classification Report:\n{reporte}')

"""## Modelo de árboles de decisión tras eliminar instancias faltantes"""

from sklearn.tree import DecisionTreeClassifier

"""from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

# Definir el rango de hiperparámetros
param_grid = {
    'max_depth': [3, 5, 7, 10],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 5],
    'criterion': ['gini', 'entropy']
}

# Crear el modelo de árbol de decisión
tree = DecisionTreeClassifier()

# Implementar Grid Search con validación cruzada
grid_search = GridSearchCV(tree, param_grid, cv=5)
grid_search.fit(x_train, y_train)

# Mejor combinación de hiperparámetros encontrada
print(f"Mejores hiperparámetros: {grid_search.best_params_}")"""

modelo_arboles = DecisionTreeClassifier(
    criterion='gini',
    max_depth=5,
    min_samples_leaf=5,
    min_samples_split=2
).fit(x_train, y_train)

# Hacer predicciones
y_pred = modelo_arboles.predict(x_test)

"""### Evaluación de exactitud y precisión del modelo"""

# Métricas
print('Score de exactitud:', accuracy_score(y_test, y_pred))
print('Score de precisión:', precision_score(y_test, y_pred))
print('Score f1:', f1_score(y_test, y_pred))
print('Score de recall:', recall_score(y_test, y_pred))

# Matriz de confusión
mat = confusion_matrix(y_test, y_pred)
print(f'Confusion Matrix:\n{mat}')

# Reporte de clasificación
reporte = classification_report(y_test, y_pred)
print(f'Classification Report:\n{reporte}')

"""## Random Forest tras eliminar las edades faltantes"""

from sklearn.ensemble import RandomForestClassifier
random_forest = RandomForestClassifier().fit(x_train, y_train)
y_pred = random_forest.predict(x_test)

'''
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

# Definir el espacio de hiperparámetros a explorar
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['auto', 'sqrt', 'log2']
}

# Crear el modelo de Random Forest
random_forest = RandomForestClassifier(random_state=42)

# Configurar la búsqueda en rejilla
grid_search = GridSearchCV(estimator=random_forest, param_grid=param_grid, cv=5, n_jobs=-1, scoring='accuracy')

# Ajustar el modelo a los datos
grid_search.fit(x_train, y_train)

# Obtener los mejores hiperparámetros
best_params = grid_search.best_params_
print("Mejores hiperparámetros encontrados:", best_params)'''

# Crear el modelo de Random Forest con los hiperparámetros optimizados
random_forest = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=10,
    min_samples_leaf=4,
    max_features='sqrt',
    random_state=42  # Para asegurar reproducibilidad
)

# Ajustar el modelo a los datos de entrenamiento
random_forest.fit(x_train, y_train)

# Hacer predicciones en el conjunto de prueba
y_pred = random_forest.predict(x_test)

"""### Evaluación de exactitud y precisión del modelo"""

# Métricas
print('Score de exactitud:', accuracy_score(y_test, y_pred))
print('Score de precisión:', precision_score(y_test, y_pred))
print('Score f1:', f1_score(y_test, y_pred))
print('Score de recall:', recall_score(y_test, y_pred))

# Matriz de confusión
mat = confusion_matrix(y_test, y_pred)
print(f'Confusion Matrix:\n{mat}')

# Reporte de clasificación
reporte = classification_report(y_test, y_pred)
print(f'Classification Report:\n{reporte}')

"""## Rellenado de edades faltantes"""

## Rellenado de valores faltantes en la columna "Age":
# Imputación basada en grupos rellenando los valores faltantes de manera condicional (en este caso según la clase o el género) mediante el
# agrupamiento de estas variables consideradas para aplicar el rellenado en base a esto y sea de manera más informada y no tan sesgada ni aleatoria.

#df_train['Age'] = df_train.groupby(['Pclass', 'Sex bool'])['Age'].transform(lambda x: x.fillna(x.median()))
#df_test['Age'] = df_test.groupby(['Pclass', 'Sex bool'])['Age'].transform(lambda x: x.fillna(x.median()))

from sklearn.impute import KNNImputer
# En este segundo intento de imputación de los datos de edad se hará con KNN
imputacion = KNNImputer(n_neighbors=5)
df_train['Age'] = imputacion.fit_transform(df_train[['Age']])

# Imprimimos el dataframe tras el rellenado para confirmar que sus dimensiones se conservaron y que no se eliminaron datos como en la primera solución
print(df_train.shape)
df_train

count_na = df_train['Age'].isna().sum()
print('Valores faltantes en columna "Age":\n', count_na)

"""Como se puede observar, ya no hay valores faltantes, por lo que el rellenado de las edades faltantes fue realizado con éxito. Ahora se procede con el desarrollo y entrenamiento del modelo para evaluar su desempeño y decidir si se va a utilizar este modelo o el que se hizo anteriormente con eliminación de instancias faltantes.

## Modelo de regresión logística tras rellenado de edades faltantes
"""

from sklearn.preprocessing import StandardScaler
x = df_train.drop(['Name', 'Survived'], axis=1)
y = df_train['Survived']

# Crear el modelo de regresión logística con los mejores hiperparámetros
modelo_reg_best = LogisticRegression(
    C=1.528668179219408,
    max_iter=2000,
    solver='lbfgs'
)

# Entrenar el modelo con los datos de entrenamiento
modelo_reg_best.fit(x_train_scaled, y_train)

# Hacer predicciones en el conjunto de prueba
y_pred = modelo_reg_best.predict(x_test_scaled)

"""### Evaluación de exactitud y precisión del modelo"""

# Métricas
print('Score de exactitud:', accuracy_score(y_test, y_pred))
print('Score de precisión:', precision_score(y_test, y_pred))
print('Score f1:', f1_score(y_test, y_pred))
print('Score de recall:', recall_score(y_test, y_pred))

# Matriz de confusión
mat = confusion_matrix(y_test, y_pred)
print(f'Confusion Matrix:\n{mat}')

# Reporte de clasificación
reporte = classification_report(y_test, y_pred)
print(f'Classification Report:\n{reporte}')

"""## Modelo de árboles de decisión tras rellenado de edades"""

from sklearn.tree import DecisionTreeClassifier
modelo_arboles = DecisionTreeClassifier(
    criterion='gini',
    max_depth=5,
    min_samples_leaf=5,
    min_samples_split=2
).fit(x_train, y_train)

# Hacer predicciones
y_pred = modelo_arboles.predict(x_test)

"""### Evaluación de exactitud y precisión del modelo"""

# Métricas
print('Score de exactitud:', accuracy_score(y_test, y_pred))
print('Score de precisión:', precision_score(y_test, y_pred))
print('Score f1:', f1_score(y_test, y_pred))
print('Score de recall:', recall_score(y_test, y_pred))

# Matriz de confusión
mat = confusion_matrix(y_test, y_pred)
print(f'Confusion Matrix:\n{mat}')

# Reporte de clasificación
reporte = classification_report(y_test, y_pred)
print(f'Classification Report:\n{reporte}')

"""## Random Forest con los datos rellenados de la edad"""

from sklearn.ensemble import RandomForestClassifier
random_forest = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=10,
    min_samples_leaf=4,
    max_features='sqrt',
    random_state=42  # Para asegurar reproducibilidad
)

# Ajustar el modelo a los datos de entrenamiento
random_forest.fit(x_train, y_train)

# Hacer predicciones en el conjunto de prueba
y_pred = random_forest.predict(x_test)

"""### Evaluación de exactitud y precisión del modelo"""

# Métricas
print('Score de exactitud:', accuracy_score(y_test, y_pred))
print('Score de precisión:', precision_score(y_test, y_pred))
print('Score f1:', f1_score(y_test, y_pred))
print('Score de recall:', recall_score(y_test, y_pred))

# Matriz de confusión
mat = confusion_matrix(y_test, y_pred)
print(f'Confusion Matrix:\n{mat}')

# Reporte de clasificación
reporte = classification_report(y_test, y_pred)
print(f'Classification Report:\n{reporte}')
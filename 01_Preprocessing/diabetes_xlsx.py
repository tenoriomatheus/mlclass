#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atividade para trabalhar o pré-processamento dos dados.

Criação de modelo preditivo para diabetes e envio para verificação de peformance
no servidor.

@author: Aydano Machado <aydano.machado@gmail.com>
"""

import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import requests
from time import sleep


def fill_zero(data_):
    for col_ in data_:
        data_[col_] = data_[col_].fillna(0)

    return data_


def fill_mean(data_):
    for col_ in data_:
        data_[col_] = data_[col_].fillna(data_[col_].mean())

    return data_


def fill_inf(data_):
    for col_ in data_:
        inf = data_[col_].max() * 100
        data_[col_] = data_[col_].fillna(inf)

    return data_


def fill_median(data_):
    return data_


def drop_na(data_):
    return data_


def fill_avg(data_):
    return data_


def data_pre_processing(filepath, method):
    print('\n - Lendo o arquivo com o dataset sobre diabetes')
    data = pd.read_excel('diabetes_dataset.xlsx')

    data = method(data)

    # Criando X and y par ao algorítmo de aprendizagem de máquina.\
    print(' - Criando X e y para o algoritmo de aprendizagem a partir do arquivo diabetes_dataset')
    # Caso queira modificar as colunas consideradas basta algera o array a seguir.
    feature_cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    X = data[feature_cols]
    y = data.Outcome

    return X, y


def model_creation(X, y):
    # Criando o modelo preditivo para a base trabalhada
    print(' - Criando modelo preditivo')
    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(X, y)

    return neigh


def run_test(model, filepath):
    # realizando previsões com o arquivo de
    print(' - Aplicando modelo e enviando para o servidor')
    data_app = pd.read_excel('diabetes_app.xlsx')
    y_pred = model.predict(data_app)

    # Enviando previsões realizadas com o modelo para o servidor
    URL = "https://aydanomachado.com/mlclass/01_Preprocessing.php"

    DEV_KEY = "Equipe da Engenharia"

    # json para ser enviado para o servidor
    data = {'dev_key': DEV_KEY,
            'predictions': pd.Series(y_pred).to_json(orient='values')}

    # Enviando requisição e salvando o objeto resposta
    r = requests.post(url=URL, data=data)

    return r.text
    # # Extraindo e imprimindo o texto da resposta
    # pastebin_url = r.text
    # print(" - Resposta do servidor:\n", r.text, "\n")


methods = {'fill_zero': fill_zero, 'fill_mean': fill_mean, 'fill_inf': fill_inf}

for name in methods:
    print('----' + name + '----')
    X, y = data_pre_processing('diabetes_dataset.xlsx', methods[name])
    model = model_creation(X, y)
    sleep(5*60)
    response = run_test(model, 'diabetes_app.xlsx')
    print(" - Resposta do servidor:\n", response, "\n")
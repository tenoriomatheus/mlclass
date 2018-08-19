#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from pandas import DataFrame
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_validate
import requests
from termcolor import colored


def rename_sex(data_: DataFrame):
    data_['sex'] = data_['sex'].map({'F': 1, 'I': 2, 'M': 3})

    return data_


print('\n - Lendo o arquivo com o dataset sobre abalone')
data = pd.read_excel('abalone_dataset.xlsx')

clone_ = DataFrame(data)
clone_ = rename_sex(clone_)

models = [MLPClassifier(learning_rate='adaptive')]

x = 1
for model in models:
    print('{} - Criando X e y para o algoritmo de aprendizagem a partir do arquivo abalone_dataset'.format(
        colored(x, 'green')))
    feature_cols = ['sex', 'length', 'diameter', 'height',
                    'whole_weight', 'shucked_weight', 'viscera_weight', 'shell_weight']
    X = clone_[feature_cols]
    y = clone_.type

    print('{} - Treinando e Testando'.format(colored(x, 'green')))
    test_results = cross_validate(model, X, y, cv=5, scoring='accuracy')

    print('{} - test_results: {}'.format(colored(x, 'green'), test_results))
    print('{} -  Accuracy: {} (+/- {})\n'.format(colored(x, 'green'),
                                               colored(test_results['test_score'].mean(), 'green'),
                                               colored(test_results['test_score'].std() * 2, 'green')))
    x += 1

# definitive predictive model


# def run_test(model, filepath):
#     # realizando previsões com o arquivo de
#     print(' - Aplicando modelo e enviando para o servidor')
#     data_app = pd.read_excel('diabetes_app.xlsx')
#     y_pred = model.predict(data_app)
#
#     # Enviando previsões realizadas com o modelo para o servidor
#     URL = "https://aydanomachado.com/mlclass/01_Preprocessing.php"
#
#     DEV_KEY = "Equipe da Engenharia"
#
#     # json para ser enviado para o servidor
#     data = {'dev_key': DEV_KEY,
#             'predictions': pd.Series(y_pred).to_json(orient='values')}
#
#     # Enviando requisição e salvando o objeto resposta
#     r = requests.post(url=URL, data=data)
#
#     return r.text
#     # # Extraindo e imprimindo o texto da resposta
#     # pastebin_url = r.text
#     # print(" - Resposta do servidor:\n", r.text, "\n")
#
#
# for name in methods:
#     print('----' + name + '----')
#     X, y = data_pre_processing('diabetes_dataset.xlsx', methods[name])
#     model = model_creation(X, y)
#     response = run_test(model, 'diabetes_app.xlsx')
#     print(" - Resposta do servidor:\n", response, "\n")
#     sleep(5*60)

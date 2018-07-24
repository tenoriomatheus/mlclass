#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import requests

print('\n - Lendo o arquivo com o dataset sobre diabetes')
data = pd.read_excel('diabetes_dataset.xlsx', encode='iso-8859-1')

# data['Insulin'] = data['Insulin'].fillna(data['Insulin'].mean())
# data = data.sort_values(['Insulin'], ascending=[False])
data = data.dropna(how='any')

print(data)
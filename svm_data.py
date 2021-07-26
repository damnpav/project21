from sklearn.svm import SVC
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd


matrix_df = pd.read_excel('matrix_fx.xlsx')
del matrix_df['Unnamed: 0']
clear_matrix = matrix_df.dropna(axis=1, how='all')
clear_matrix1 = clear_matrix.dropna(axis=0, how='all', subset=['белиз', 'дания', 'индия', 'иран', 'италия', 'кипр', 'китай', 'куба',
       'ливан', 'ливан.1', 'литва', 'нидерланды', 'перу', 'сша', 'тунис',
       'чили', 'юар', 'япония', 'америк', 'фрг'])
fx_true = clear_matrix1.loc[clear_matrix1['FX']==1]
fx_false = clear_matrix1.loc[clear_matrix1['FX']!=1]
fx_true = fx_true.fillna(0)
fx_true = fx_true[:915]
fx_false = fx_false.fillna(0)
fx_false = fx_false[:1877]
target = pd.concat([fx_true['FX'][:915], fx_false['FX'][:1877]]).to_numpy()
del fx_true['File'], fx_true['found'], fx_true['FX']
del fx_false['File'], fx_false['found'], fx_false['FX']

features = pd.concat([fx_true, fx_false]).to_numpy()

scaler = StandardScaler()
features_standardized = scaler.fit_transform(features)

svc = SVC(kernel='rbf', random_state=0, gamma=1, C=1)

model = svc.fit(features_standardized, target)


fx_true_test = clear_matrix1.loc[clear_matrix1['FX']==1]
fx_false_test = clear_matrix1.loc[clear_matrix1['FX']!=1]
fx_true_test = fx_true_test.fillna(0)
fx_true_test = fx_true_test[915:]
fx_false_test = fx_false_test.fillna(0)
fx_false_test = fx_false_test[1877:]
del fx_true_test['File'], fx_true_test['found'], fx_true_test['FX']
del fx_false_test['File'], fx_false_test['found'], fx_false_test['FX']

fx_true_values = fx_true_test.values.tolist()
fx_false_values = fx_false_test.values.tolist()

true_results = []
false_results = []

for el in fx_true_values:
    true_results.append(model.predict([el])[0])


for el in fx_false_values:
    false_results.append(model.predict([el])[0])




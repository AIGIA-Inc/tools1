import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

#必要データの読み込み
shots = pd.read_csv('text2.csv')

#データ整形
user = shots.iloc[:,:1]
user_data = shots.iloc[:,1:]


data = user.values
target= user_data.values
print(type(data))
print(type(target))


data_train, data_test, target_train, target_test = train_test_split(
    data, target, test_size=0.3, random_state=0)


reg = RandomForestClassifier()
reg.fit(data_train, target_train)
"""
pred = reg.predict(data_test)
print(pred)
"""

"""

reg = RandomForestClassifier()
reg.fit(data, target)

result = learn_model.iloc[3,:].values
print(result)
predict_model = reg.predict([result])
print(predict_model)
"""
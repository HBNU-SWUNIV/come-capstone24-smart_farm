# -*- coding: euc-kr -*-
import numpy as np
import pandas as pd

from neuralprophet import NeuralProphet


'''
    * ����:
        https://bigwaveai.tistory.com/28
        
        https://medium.com/@tubelwj/neuralprophet-a-pr-python-library-for-time-series-forcasting-12d40a86abff
        https://stackoverflow.com/questions/70476793/how-to-add-additive-regression-for-multivariate-data-in-neural-prophet-like-in
        https://www.kaggle.com/code/ohseokkim/predicting-future-by-lstm-prophet-neural-prophet
'''

# ���� ���ڵ� ����
ENCODING='euc-kr'


data = pd.read_csv('C:\Users\Desktop\Desktop\Neural Prophet을 활용한 모터 개폐 비율에 따른 실내 온, 습도 예측\source', encoding=ENCODING)

data = data[['�Ͻ�', '���(��C)', '����(%)', '���� �µ� 0%']]

column_list = ['���(��C)', '����(%)']

data = data.rename(columns={'�Ͻ�': 'ds', '���� �µ� 0%': 'y'})

cutoff = '2016-12-31'
train = data[data['ds'] < cutoff]
test = data[data['ds'] >= cutoff]

model = NeuralProphet(
            n_lags=24, 
            n_forecasts=1, 
            yearly_seasonality=True,
            weekly_seasonality=True, 
            daily_seasonality=True, 
            epochs=600 
        )

model = model.add_lagged_regressor(column_list)

metrics = model.fit(df=train, 
                    freq='h', 
                    validation_df=test, 
                    metrics=True, 
                    early_stopping=True, 
                    progress='plot',
                    )

forecast = model.predict(test)

fig_forecast = model.plot(forecast)
fig_components = model.plot_components(forecast)
fig_model = model.plot_parameters()

print(metrics.tail(5))

forecast.to_csv('forecasting.csv', encoding=ENCODING)
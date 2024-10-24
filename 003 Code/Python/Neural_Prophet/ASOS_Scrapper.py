# -*- coding: euc-kr -*-
import numpy as np
import pandas as pd

from neuralprophet import NeuralProphet

# ���� ���ڵ� ����
ENCODING='euc-kr'


# ��ó���� ������ �ҷ�����
data = pd.read_csv('preprocessed_result.csv', encoding=ENCODING)

# �ʿ��� column�� �����ϱ�
data = data[['�Ͻ�', '���(��C)', '����(%)', '���� �µ� 0%']]

# ���� ���� ���
column_list = ['���(��C)', '����(%)']

# ���� ���� �����ϱ�
data = data.rename(columns={'�Ͻ�': 'ds', '���� �µ� 0%': 'y'})

# train, test �����ϱ�
cutoff = '2016-12-31' # ������ ���� ����
train = data[data['ds'] < cutoff]
test = data[data['ds'] >= cutoff]

# �� �����ϱ�
model = NeuralProphet(
            n_lags=24, # 24 �ð�����
            n_forecasts=1, # 1�� ����
            yearly_seasonality=True, # �� ������
            weekly_seasonality=True, # �� ������
            daily_seasonality=True, # �� ������
            epochs=600 # �н� Ƚ��
        )

# ���� ���� �߰��ϱ�
model = model.add_lagged_regressor(column_list)

# �н� �ϱ�
metrics = model.fit(df=train, # �н� ������
                    freq='h', # �ֱ�
                    validation_df=test, # ���� ������
                    metrics=True, # ����ǥ Ȱ��ȭ
                    early_stopping=True, # ������ �߻� �� ����
                    progress='plot',
                    )

# �����ϱ�
forecast = model.predict(test)

# �ð�ȭ �ϱ�
fig_forecast = model.plot(forecast)
fig_components = model.plot_components(forecast)
fig_model = model.plot_parameters()

# ���� �� ��ǥ Ȯ���ϱ�
print(metrics.tail(5))

# ������ ������ �����ϱ�
forecast.to_csv('forecasting.csv', encoding=ENCODING)
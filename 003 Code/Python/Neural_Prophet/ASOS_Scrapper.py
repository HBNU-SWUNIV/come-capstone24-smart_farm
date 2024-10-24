# -*- coding: euc-kr -*-
import numpy as np
import pandas as pd

from neuralprophet import NeuralProphet

# 파일 인코딩 설정
ENCODING='euc-kr'


# 전처리한 데이터 불러오기
data = pd.read_csv('preprocessed_result.csv', encoding=ENCODING)

# 필요한 column만 설정하기
data = data[['일시', '기온(°C)', '습도(%)', '개폐 온도 0%']]

# 독립 변수 목록
column_list = ['기온(°C)', '습도(%)']

# 종속 변수 설정하기
data = data.rename(columns={'일시': 'ds', '개폐 온도 0%': 'y'})

# train, test 분할하기
cutoff = '2016-12-31' # 데이터 분할 기준
train = data[data['ds'] < cutoff]
test = data[data['ds'] >= cutoff]

# 모델 설정하기
model = NeuralProphet(
            n_lags=24, # 24 시간으로
            n_forecasts=1, # 1일 예측
            yearly_seasonality=True, # 년 계절성
            weekly_seasonality=True, # 주 계절성
            daily_seasonality=True, # 일 계절성
            epochs=600 # 학습 횟수
        )

# 독립 변수 추가하기
model = model.add_lagged_regressor(column_list)

# 학습 하기
metrics = model.fit(df=train, # 학습 데이터
                    freq='h', # 주기
                    validation_df=test, # 검증 데이터
                    metrics=True, # 평가지표 활성화
                    early_stopping=True, # 과적합 발생 시 정지
                    progress='plot',
                    )

# 예측하기
forecast = model.predict(test)

# 시각화 하기
fig_forecast = model.plot(forecast)
fig_components = model.plot_components(forecast)
fig_model = model.plot_parameters()

# 성능 평가 지표 확인하기
print(metrics.tail(5))

# 예측한 데이터 저장하기
forecast.to_csv('forecasting.csv', encoding=ENCODING)
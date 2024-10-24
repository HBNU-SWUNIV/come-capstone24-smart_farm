import os
import pandas as pd

from tqdm import tqdm
from utils import get_date_range, zfill_date

# 찾을 결측 데이터 시작날짜 설정
START_YEAR  = 2024
START_MONTH = 1
START_DAY   = 1
START_HOUR  = 0
START_MIN   = 0

# 찾을 결측 데이터 종료날짜 설정
END_YEAR    = 2024
END_MONTH   = 12
END_DAY     = 31
END_HOUR    = 23
END_MIN     = 0

# 찾을 결측 데이터 날짜 범위
start_date = zfill_date(START_YEAR, 
                        START_MONTH, 
                        START_DAY, 
                        START_HOUR, 
                        START_MIN)

end_date = zfill_date(END_YEAR, 
                      END_MONTH, 
                      END_DAY, 
                      END_HOUR, 
                      END_MIN)

STD_MISSING_DATA = get_date_range(start_date, 
                                  end_date, 
                                  hours=1, 
                                  format='%Y%m%d%H%M')

# 전처리 오프셋
PERCENT_0   = 0.0
PERCENT_25  = 0.05
PERCENT_50  = 0.1
PERCENT_75  = 0.2
PERCENT_100 = 0.3

# 인코딩 설정
ENCODING = 'euc-kr'

SAVE_FILE_NAME = 'preprocessed_result.csv'

PATH = os.path.dirname(os.path.abspath(__file__)) + '/weather_dataset'


# 데이터 프레임 병합
def merge_dataframe(path):
    merge_df = pd.DataFrame()   
    for file_name in tqdm(os.listdir(path), desc='데이터 프레임 병합'):
        csv_file_path = path + '/' + file_name
        df = pd.read_csv(csv_file_path, encoding=ENCODING)
        merge_df = pd.concat([merge_df, df], ignore_index=True)

    return merge_df

# 결측 데이터 찾기
def find_missing_data(df1, df2):
    return pd.merge(df1, df2, how='outer', indicator=True) \
            .query("_merge=='right_only'") \
            .drop(columns=['_merge'])

# 결측 데이터 채우기
def fill_missing_data_avg(df):
    row_index_list = df[df['습도(%)'].isnull()].index.tolist()
    df_columns = df.columns

    for row in tqdm(row_index_list, desc='결측 데이터 채우기'):
        date = pd.to_datetime(df.loc[row, ['일시']].values.item())
        date = date.strftime('%Y-%m-%d %H:%M')[5:]

        # 찾은 데이터의 평균으로 결측 값 대체하기
        df2 = round(df[df['일시']
                       .astype(str)
                       .str.contains(date, na=False)]
                       .mean(numeric_only=True), 1) \
                       .to_frame().T

        df.loc[row, ['지점명']] = df['지점명'].mode()[0]

        for i, column in enumerate(df_columns):
            if column in df2.columns:
                df.iloc[row, i] = df2.loc[0, [column]]

    return df

# 데이터 타입 맞추기
def change_data_type(df):
    df['지점명'] = df['지점명'].astype('string')
    df['일시'] = pd.to_datetime(df['일시'])
    
    return df

# 리스트 --> 데이터 프레임
def convert_list_to_df(list, columns):
    df = pd.DataFrame(list)
    df.columns = columns
   
    return df

# 모터 개폐 비율에 따른 데이터 생성
def generate_data(value, percent):
    result = 0.0

    if value <= 0.0:
        if percent <= 0.0:
            result =  value - (value * 0.3)
        else:
            result =  value + (value * percent)
        
    if value >= 0.0:
        if percent <= 0.0:
            result =  value + (value * 0.3)
        else:
            result =  value - (value * percent)
            
    if result >= 100.0:
        result = 100.0
        
    return round(result, 1)


if __name__ == '__main__':
    # 데이터를 한 개의 데이터 프레임에 병합
    merged_df = merge_dataframe(PATH)
    
    # 비교할 두 개의 데이터 프레임 준비
    df1 = change_data_type(merged_df)
    df2 = convert_list_to_df(STD_MISSING_DATA, ['일시'])

    # 데이터 타입 통일
    df2 = pd.to_datetime(df2['일시'])
    
    # 결측 데이터 찾기
    missing_df = find_missing_data(df1, df2)
    
    # 찾은 결측 데이터를 병합
    merged_df = pd.concat([merged_df, missing_df], ignore_index=True)
    
    # '일시' 열을 기준으로 정렬(오름차)
    merged_df = merged_df.sort_values('일시', ascending=True, ignore_index=True)

    merged_df = fill_missing_data_avg(merged_df)

    preprocess_df = merged_df[['지점명', '일시', '기온(°C)', '습도(%)']]

    preprocess_df = preprocess_df.copy()

    # 데이터 전처리 
    preprocess_df['개폐 온도 0%'] = preprocess_df['기온(°C)'].apply(generate_data, percent=PERCENT_0)
    preprocess_df['개폐 온도 25%'] = preprocess_df['기온(°C)'].apply(generate_data, percent=PERCENT_25)
    preprocess_df['개폐 온도 50%'] = preprocess_df['기온(°C)'].apply(generate_data, percent=PERCENT_50)
    preprocess_df['개폐 온도 75%'] = preprocess_df['기온(°C)'].apply(generate_data, percent=PERCENT_75)
    preprocess_df['개폐 온도 100%'] = preprocess_df['기온(°C)'].apply(generate_data, percent=PERCENT_100)
    
    preprocess_df['개폐 습도 0%'] = preprocess_df['습도(%)'].apply(generate_data, percent=PERCENT_0)
    preprocess_df['개폐 습도 25%'] = preprocess_df['습도(%)'].apply(generate_data, percent=PERCENT_25)
    preprocess_df['개폐 습도 50%'] = preprocess_df['습도(%)'].apply(generate_data, percent=PERCENT_50)
    preprocess_df['개폐 습도 75%'] = preprocess_df['습도(%)'].apply(generate_data, percent=PERCENT_75)
    preprocess_df['개폐 습도 100%'] = preprocess_df['습도(%)'].apply(generate_data, percent=PERCENT_100)

    # 데이터 저장
    preprocess_df.to_csv(SAVE_FILE_NAME, index=False, encoding=ENCODING)
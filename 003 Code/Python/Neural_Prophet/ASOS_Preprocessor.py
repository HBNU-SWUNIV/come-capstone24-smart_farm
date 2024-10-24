import os
import pandas as pd

from tqdm import tqdm
from utils import get_date_range, zfill_date

# ã�� ���� ������ ���۳�¥ ����
START_YEAR  = 2024
START_MONTH = 1
START_DAY   = 1
START_HOUR  = 0
START_MIN   = 0

# ã�� ���� ������ ���ᳯ¥ ����
END_YEAR    = 2024
END_MONTH   = 12
END_DAY     = 31
END_HOUR    = 23
END_MIN     = 0

# ã�� ���� ������ ��¥ ����
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

# ��ó�� ������
PERCENT_0   = 0.0
PERCENT_25  = 0.05
PERCENT_50  = 0.1
PERCENT_75  = 0.2
PERCENT_100 = 0.3

# ���ڵ� ����
ENCODING = 'euc-kr'

SAVE_FILE_NAME = 'preprocessed_result.csv'

PATH = os.path.dirname(os.path.abspath(__file__)) + '/weather_dataset'


# ������ ������ ����
def merge_dataframe(path):
    merge_df = pd.DataFrame()   
    for file_name in tqdm(os.listdir(path), desc='������ ������ ����'):
        csv_file_path = path + '/' + file_name
        df = pd.read_csv(csv_file_path, encoding=ENCODING)
        merge_df = pd.concat([merge_df, df], ignore_index=True)

    return merge_df

# ���� ������ ã��
def find_missing_data(df1, df2):
    return pd.merge(df1, df2, how='outer', indicator=True) \
            .query("_merge=='right_only'") \
            .drop(columns=['_merge'])

# ���� ������ ä���
def fill_missing_data_avg(df):
    row_index_list = df[df['����(%)'].isnull()].index.tolist()
    df_columns = df.columns

    for row in tqdm(row_index_list, desc='���� ������ ä���'):
        date = pd.to_datetime(df.loc[row, ['�Ͻ�']].values.item())
        date = date.strftime('%Y-%m-%d %H:%M')[5:]

        # ã�� �������� ������� ���� �� ��ü�ϱ�
        df2 = round(df[df['�Ͻ�']
                       .astype(str)
                       .str.contains(date, na=False)]
                       .mean(numeric_only=True), 1) \
                       .to_frame().T

        df.loc[row, ['������']] = df['������'].mode()[0]

        for i, column in enumerate(df_columns):
            if column in df2.columns:
                df.iloc[row, i] = df2.loc[0, [column]]

    return df

# ������ Ÿ�� ���߱�
def change_data_type(df):
    df['������'] = df['������'].astype('string')
    df['�Ͻ�'] = pd.to_datetime(df['�Ͻ�'])
    
    return df

# ����Ʈ --> ������ ������
def convert_list_to_df(list, columns):
    df = pd.DataFrame(list)
    df.columns = columns
   
    return df

# ���� ���� ������ ���� ������ ����
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
    # �����͸� �� ���� ������ �����ӿ� ����
    merged_df = merge_dataframe(PATH)
    
    # ���� �� ���� ������ ������ �غ�
    df1 = change_data_type(merged_df)
    df2 = convert_list_to_df(STD_MISSING_DATA, ['�Ͻ�'])

    # ������ Ÿ�� ����
    df2 = pd.to_datetime(df2['�Ͻ�'])
    
    # ���� ������ ã��
    missing_df = find_missing_data(df1, df2)
    
    # ã�� ���� �����͸� ����
    merged_df = pd.concat([merged_df, missing_df], ignore_index=True)
    
    # '�Ͻ�' ���� �������� ����(������)
    merged_df = merged_df.sort_values('�Ͻ�', ascending=True, ignore_index=True)

    merged_df = fill_missing_data_avg(merged_df)

    preprocess_df = merged_df[['������', '�Ͻ�', '���(��C)', '����(%)']]

    preprocess_df = preprocess_df.copy()

    # ������ ��ó�� 
    preprocess_df['���� �µ� 0%'] = preprocess_df['���(��C)'].apply(generate_data, percent=PERCENT_0)
    preprocess_df['���� �µ� 25%'] = preprocess_df['���(��C)'].apply(generate_data, percent=PERCENT_25)
    preprocess_df['���� �µ� 50%'] = preprocess_df['���(��C)'].apply(generate_data, percent=PERCENT_50)
    preprocess_df['���� �µ� 75%'] = preprocess_df['���(��C)'].apply(generate_data, percent=PERCENT_75)
    preprocess_df['���� �µ� 100%'] = preprocess_df['���(��C)'].apply(generate_data, percent=PERCENT_100)
    
    preprocess_df['���� ���� 0%'] = preprocess_df['����(%)'].apply(generate_data, percent=PERCENT_0)
    preprocess_df['���� ���� 25%'] = preprocess_df['����(%)'].apply(generate_data, percent=PERCENT_25)
    preprocess_df['���� ���� 50%'] = preprocess_df['����(%)'].apply(generate_data, percent=PERCENT_50)
    preprocess_df['���� ���� 75%'] = preprocess_df['����(%)'].apply(generate_data, percent=PERCENT_75)
    preprocess_df['���� ���� 100%'] = preprocess_df['����(%)'].apply(generate_data, percent=PERCENT_100)

    # ������ ����
    preprocess_df.to_csv(SAVE_FILE_NAME, index=False, encoding=ENCODING)
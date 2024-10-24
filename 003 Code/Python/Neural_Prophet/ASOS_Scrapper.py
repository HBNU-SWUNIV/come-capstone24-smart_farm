import os
import requests

from tqdm import tqdm
from multiprocessing import Pool, Lock
from utils import create_folder, save_to_csv_file, get_date_range, zfill_date

'''
    * ����: 
        https://dev-jacob.tistory.com/entry/Python-Requests-�ѱ�-����-����-�ذ��ϱ�
        https://sopython.com/canon/97/writing-csv-adds-blank-lines-between-rows
        https://stackoverflow.com/questions/41920124/multiprocessing-use-tqdm-to-display-a-progress-bar
        https://stackoverflow.com/questions/25557686/python-sharing-a-lock-between-processes
        https://everywhere-data.tistory.com/52
'''

# ���۳�¥ ����
START_YEAR  = 2010
START_MONTH = 1
START_DAY   = 1

# ���ᳯ¥ ����
END_YEAR    = 2020
END_MONTH   = 12
END_DAY     = 31

# ���� ����
REGION = '�ݻ�'

# ������ ���� ����
CPU_COUNT = os.cpu_count()
   
# �����͸� ������ ��� ����
PATH = os.path.dirname(os.path.abspath(__file__)) + '/weather_dataset'


# csv �������� url ���ϱ�
def get_csv_url(start_date, end_date, region):
    # ����������(ASOS) - 1�ð� �������� ������ ���� ������
    url = 'https://data.kma.go.kr/data/common/downloadDataCVS.do'
    
    data = {
        'fileType': 'csv',
        'cmmnCdList': 'F00501,F00502,F00503,F00512,F00513',
        'upperCmmnCode': 'F005',
        'lrgClssCd': 'SFC',
        'mddlClssCd': 'SFC01',
        'menuNo': '32',
        'pageIndex': '1',
        'stnIds': '164_238',
        'serviceSe': 'F00102',
        'elementCds': 'SFC01012001,SFC01012010,SFC01012002,SFC01012003,SFC01012004,SFC01012005,SFC01011001,SFC01001001,SFC01001002,SFC01002001,SFC01002002,SFC01003001,SFC01003004,SFC01003002,SFC01003003,SFC01004001,SFC01004006,SFC01004002,SFC01004003,SFC01005001,SFC01005004,SFC01005002,SFC01005003,SFC01006001,SFC01006004,SFC01006002,SFC01006003,SFC01007001,SFC01007002,SFC01008001,SFC01008002,SFC01008003,SFC01008004,SFC01009001,SFC01010001',
        'elementGroupSns': '101,337,339,91,92,93,94,95,96,97,98,99',
        'dwldSetupPd': '0',
        'firstLoading': 'N',
        'pageRowCount': '24',
        'schTotalCnt': '10',
        'pgmNo': '36',
        'stnTreeId': 'ztree_111_check',
        'elementTreeId': 'ztree1_3_check,ztree1_4_check,ztree1_5_check,ztree1_6_check,ztree1_7_check,ztree1_8_check,ztree1_10_check,ztree1_12_check,ztree1_13_check,ztree1_15_check,ztree1_16_check,ztree1_18_check,ztree1_19_check,ztree1_20_check,ztree1_21_check,ztree1_23_check,ztree1_24_check,ztree1_25_check,ztree1_26_check,ztree1_28_check,ztree1_29_check,ztree1_30_check,ztree1_31_check,ztree1_33_check,ztree1_34_check,ztree1_35_check,ztree1_36_check,ztree1_38_check,ztree1_39_check,ztree1_41_check,ztree1_42_check,ztree1_43_check,ztree1_44_check,ztree1_46_check,ztree1_48_check',
        'dataFormCd': 'F00502',
        'startDt': start_date,
        'startHh': '00',
        'endDt': end_date,
        'endHh': '23',
        'startMt': '01',
        'endMt': '01',
        'txtStnNm': region,
        'txtElementNm': '����µ�,����µ� QC�÷���,5cm ���߿µ�,10cm ���߿µ�,20cm ���߿µ�,30cm ���߿µ�,�����ȣ,���,��� QC�÷���,������,������ QC�÷���,ǳ��,ǳ�� QC�÷���,ǳ��,ǳ�� QC�÷���,����,���� QC�÷���,�����,�̽����µ�,�������,������� QC�÷���,�ظ���,�ظ��� QC�÷���,����,���� QC�÷���,�ϻ�,�ϻ� QC�÷���,����,3�ð�������,���,�������,����,�������,����,�������}',
        'isSample': 'Y'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    return requests.post(url, data=data, headers=headers).text

# url�� ���� csv ������ ��������
def get_file_from_csv_url(file_url):
    url = 'https://data.kma.go.kr/download/fileDownload.do'
    data = {
        'file': file_url,
        'delYn': 'Y'
    }

    response = requests.post(url, data=data)
    response.encoding = response.apparent_encoding
    
    return response.text

# data ���� Ȯ���ϱ�
def is_data_error(csv_data):
    if '�߸��� �����Դϴ�.' in csv_data:
        return True
    else:
        return False
 
# ��(���� ũ�Ⱑ 0) ������ ���ϸ� ã��
def find_empty_file_name(path):
    empty_file_list = []
    for file in os.listdir(path):
        file_size = os.path.getsize(path + '/' + file)
        if file_size <= 0:
            file_name = file.split('.')[0].strip()
            empty_file_list.append(file_name)
            
    return empty_file_list

# ���۳�¥���� ���ᳯ¥���� csv ���� �����ϴ� ���� ������
def main_thread(date):
    with lock:
        csv_url = get_csv_url(date, date, REGION)
        csv_data = get_file_from_csv_url(csv_url)

        if is_data_error(csv_data):
            return

        save_to_csv_file(PATH, csv_data, date)

# multiprocessing pool lock
def init(l):
    global lock
    lock = l


if __name__ == '__main__':
    # ������ �ߺ� ���� �����ϱ�
    lock = Lock()

    # ���� �����ϱ�
    create_folder(PATH)
    
    # ���۳�¥���� ���ᳯ¥ ���� ���� ���ϱ�
    start_date = zfill_date(START_YEAR, START_MONTH, START_DAY)
    end_date = zfill_date(END_YEAR, END_MONTH, END_DAY)
    range_date_list = get_date_range(start_date, end_date)

    # ������ Ǯ�� ����Ͽ� CPU ���� ��ŭ �۾� �����ϱ�
    with Pool(processes=CPU_COUNT, 
              initializer=init, 
              initargs=(lock,)) as pool:
        with tqdm(total=len(range_date_list), desc='������ ����') as pbar:
            for _ in pool.imap_unordered(main_thread, range_date_list):
                pbar.update()
    
    # ������ �����Ͱ� �����ϸ� �ٿ�ε� �ϱ�
    while True:
        empty_file_name_list = find_empty_file_name(PATH)
        if len(empty_file_name_list) > 0:
            with Pool(processes=CPU_COUNT, 
                      initializer=init, 
                      initargs=(lock,)) as pool:
                with tqdm(total=len(empty_file_name_list), desc='������ ������ ����') as pbar:
                    for _ in pool.imap_unordered(main_thread, empty_file_name_list):
                        pbar.update()                  
        else:
            break
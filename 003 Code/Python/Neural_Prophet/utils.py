# -*- coding: euc-kr -*-
import os

from datetime import datetime, timedelta


def create_folder(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print ('����: ������ ������ �� �����ϴ�. ' +  path)
 
def save_to_csv_file(path, csv_data, date):
    with open(path + '/' + str(date) + '.csv', 'w', newline='') as file:
        file.write(csv_data)

# ��¥ ���� ���ϱ�
def get_date_range(start_date, end_date, hours=24, format='%Y%m%d'):
    range_date_list = []

    start_date = datetime.strptime(start_date, format)
    end_date = datetime.strptime(end_date, format)

    # ���� ��¥���� ���� ��¥���� ����Ʈ�� �����ϱ�
    while start_date <= end_date:
        range_date_list.append(start_date.strftime(format))
        start_date += timedelta(hours=hours)

    return range_date_list

# ��¥ ���� ���߱�
def zfill_date(*dates):
    filled_date = ''
    for date in dates:
        filled_date += str(date).zfill(2)

    return filled_date
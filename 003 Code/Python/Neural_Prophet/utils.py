import os

from datetime import datetime, timedelta


def create_folder(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print ('오류: 폴더를 생성할 수 없습니다. ' +  path)
 
def save_to_csv_file(path, csv_data, date):
    with open(path + '/' + str(date) + '.csv', 'w', newline='') as file:
        file.write(csv_data)

# 날짜 범위 구하기
def get_date_range(start_date, end_date, hours=24, format='%Y%m%d'):
    range_date_list = []

    start_date = datetime.strptime(start_date, format)
    end_date = datetime.strptime(end_date, format)

    # 시작 날짜부터 종료 날짜까지 리스트에 저장하기
    while start_date <= end_date:
        range_date_list.append(start_date.strftime(format))
        start_date += timedelta(hours=hours)

    return range_date_list

# 날짜 형식 맞추기
def zfill_date(*dates):
    filled_date = ''
    for date in dates:
        filled_date += str(date).zfill(2)

    return filled_date
import requests
import re
import datetime
import csv

def get(start_data):
    html = requests.get('http://www.opec.org/basket/basketDayArchives.xml')
    content = html.text

    pattern_date = re.compile(r'\d{4}-\d{2}-\d{2}')
    pattern_val = re.compile(r'\d+\.\d{2}')
    date = pattern_date.findall(content)
    val = pattern_val.findall(content)
    csvfile = open('opec.csv', 'w')
    spamwriter = csv.writer(csvfile, dialect='excel')
    spamwriter.writerow(['日期', '价格'])

    for i in range(0, len(date)):
        start_data_stamp = datetime.datetime.strptime(start_data, '%Y-%m-%d').timestamp()
        date_stamp = datetime.datetime.strptime(date[i], '%Y-%m-%d').timestamp()#转换成datatime格式
        if date_stamp < start_data_stamp:
            continue
        else:
            spamwriter.writerow([date[i], val[i]])
if __name__ == "__main__":
    start_data = input("请输入开始日期（格式：2013-05-15）")
    get(start_data)
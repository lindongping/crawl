# -*- coding: utf-8 -*-
import requests
import re
import datetime
#import csv

def get(start_data):
    html = requests.get('http://www.opec.org/basket/basketDayArchives.xml')
    content = html.text

    pattern_date = re.compile(r'\d{4}-\d{2}-\d{2}')
    pattern_val = re.compile(r'\d+\.\d{2}')
    date = pattern_date.findall(content)
    val = pattern_val.findall(content)
    #csvfile = open('opec.csv', 'w')
    #spamwriter = csv.writer(csvfile, dialect='excel')
    #spamwriter.writerow(['日期', '价格'])

    for i in range(0, len(date)):
        start_data_stamp = datetime.datetime.strptime(start_data, '%Y-%m-%d').timestamp()
        date_stamp = datetime.datetime.strptime(date[i], '%Y-%m-%d').timestamp()#转换成datatime格式
        if date_stamp < start_data_stamp:
            continue
        else:
            save_to_mysql(date[i], val[i])
            #spamwriter.writerow([date[i], val[i]])

import pymysql
# def save_to_mysql(date,val):
#     db = pymysql.connect(host="47.92.25.70", user='root', password='Wfn031641', port=3306, db='cxd_data')
#     cursor = db.cursor()
#     sql = "insert into out_crude_oil_index(name,date,price) values(%s,%s,%s)"
#     try:
#         cursor.execute(sql, ("OPEC", date, val))
#         db.commit()
#     except:
#         db.rollback()
#     db.close()
#通用的数据库存储


def save_to_mysql(date, val):
    db = pymysql.connect(host="47.92.25.70", user='root', password='Wfn031641', port=3306, db='cxd_data')
    cursor = db.cursor()

    data = {
            'name': "OPEC",
            'date': date,
            'price': val
    }
    table = "out_crude_oil_index"
    keys = ','.join(data.keys())
    values = ",".join(['%s']*len(data))

    sql = "insert into {table}({keys}) values({values})".format(table=table, keys=keys, values=values)
    try:
        if cursor.execute(sql, tuple(data.values())):
            print("成功！")
            db.commit()
    except:
        print("失败")
        db.rollback()
    db.close()

if __name__ == "__main__":
    start_data = input("请输入开始日期（格式：2013-05-15）")
    get(start_data)

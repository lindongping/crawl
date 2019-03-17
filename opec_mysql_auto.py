# -*- coding: utf-8 -*-
#requests获取opec数据
import requests
import re
import datetime
import pymysql


def get_time(n):# 获取n天前的时间
    now_time = datetime.datetime.now()  # 获取当前时间
    n_time = now_time + datetime.timedelta(days=-n)  # 获取当前时间的前n天
    n_time_nyr = n_time.strftime('%Y-%m-%d')
    return n_time_nyr


def get(start_data):
    html = requests.get('http://www.opec.org/basket/basketDayArchives.xml')
    content = html.text

    pattern_date = re.compile(r'\d{4}-\d{2}-\d{2}')
    pattern_val = re.compile(r'\d+\.\d{2}')
    date = pattern_date.findall(content)
    val = pattern_val.findall(content)

    for i in range(0, len(date)):
        start_data_stamp = datetime.datetime.strptime(start_data, '%Y-%m-%d').timestamp()
        date_stamp = datetime.datetime.strptime(date[i], '%Y-%m-%d').timestamp()#转换成datatime格式
        if date_stamp < start_data_stamp:
            continue
        else:
            save_to_mysql(date[i], val[i])


def save_to_mysql(date, val):
    db = pymysql.connect(host="39.105.9.20", user='root', password='bigdata_oil', port=3306, db='cxd_data') #生产库
    #db = pymysql.connect(host="47.92.25.70", user='root', password='Wfn031641', port=3306, db='cxd_data')  #测试库
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
        print("已经存在")
        db.rollback()
    db.close()


if __name__ == "__main__":
    start_data = get_time(5)
    get(start_data)

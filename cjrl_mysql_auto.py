# -*- coding: utf-8 -*-
#selenium获取美国钻井数量数据
from selenium import webdriver
import time
import datetime
import pymysql


def get_time(n):# 获取n天前的时间
    now_time = datetime.datetime.now()  # 获取当前时间
    n_time = now_time + datetime.timedelta(days=-n)  # 获取当前时间的前n天
    n_time_nyr = n_time.strftime('%Y-%m-%d')
    return n_time_nyr


def save_to_mysql(pub_date, bgn_date, curr_value, prev_value, pred_value, change):
    db = pymysql.connect(host="39.105.9.20", user='root', password='bigdata_oil', port=3306, db='cxd_data', use_unicode=True, charset="utf8")
    #db = pymysql.connect(host="47.92.25.70", user='root', password='Wfn031641', port=3306, db='cxd_data', use_unicode=True, charset="utf8") #测试库
    cursor = db.cursor()

    sql = "insert into `out_crude_oil_drilling`(`area`,`source`,`pub_date`,`bgn_date`,`stat_period`,`curr_value`," \
          "`prev_value`,`pred_value`,`change`,`source_id`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    try:
        if cursor.execute(sql, ("美国", '财经日历', pub_date, bgn_date, "7d", curr_value, prev_value, pred_value, change, "4")):
            print("成功！")
            db.commit()
    except:
        print("已经存在")
        db.rollback()
    db.close()


start_data = get_time(14)
browser = webdriver.PhantomJS()
browser.get('https://www.cjrl.cn/jiedu/meiguo-337.html')
while True:
    try:
        getmore = browser.find_element_by_xpath('//*[@id="loadmore"]/a')
        getmore.click()
        time.sleep(0.5)
    except:
        break
date = browser.find_elements_by_xpath('//table[@id="datadetail"]//tr/td[1]')#公布日期
prev_value = browser.find_elements_by_xpath('//table[@id="datadetail"]//tr/td[3]')#前值
curr_value = browser.find_elements_by_xpath('//table[@id="datadetail"]//tr/td[5]')#公布值
pred_value = browser.find_elements_by_xpath('//table[@id="datadetail"]//tr/td[4]')#预测值

for i in range(0, len(date)):
    start_data_stamp = datetime.datetime.strptime(start_data, '%Y-%m-%d').timestamp()
    date_stamp = datetime.datetime.strptime(date[i].text.split(',')[0], '%Y-%m-%d').timestamp()
    if date_stamp < start_data_stamp:
        continue
    else:
        pre_data_stamp = date_stamp - 557017 #上周的格林威治时间  557017为6天时间
        pre_data = str(datetime.datetime.fromtimestamp(pre_data_stamp).strftime('%Y-%m-%d'))#把格林威治时间转换成时间格式

        change = str(int(curr_value[i].text) - int(prev_value[i].text))
        if pred_value[i].text == "---":
            save_to_mysql(date[i].text.split(',')[0], pre_data, curr_value[i].text, prev_value[i].text, "0", change)
        else:
            save_to_mysql(date[i].text.split(',')[0], pre_data, curr_value[i].text, prev_value[i].text, pred_value[i].text, change)










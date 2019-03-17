from selenium import webdriver
import time
import pymysql

def save_to_mysql(store_data):
    db = pymysql.connect(host="47.92.25.70", user='root', password='Wfn031641', port=3306, db='cxd_data', use_unicode=True, charset="utf8")
    cursor = db.cursor()

    sql = "insert into `out_oil_cn_production`(`area`,`source`,`bgn_date`,`stat_period`,`curr_value`," \
          "`prev_value`,`accum_value`,`value_unit`,`yoy_ratio`,`accum_ratio`,`province_id`,`source_id`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    try:
        if cursor.execute(sql, (store_data[0],store_data[1],store_data[2],store_data[3],store_data[4],store_data[5],store_data[6],store_data[7],store_data[8],
                                store_data[9],store_data[10],store_data[11],)):
            print("成功！")
            db.commit()
    except:
        print("失败")
        db.rollback()
    db.close()

browser = webdriver.Chrome()
browser.get('http://data.stats.gov.cn/easyquery.htm?cn=E0101')
#数据选择按钮xpath路径
choose_xpath_dir = {
    'energy_b': '//*[@id="treeZhiBiao_5_span"]',
    'energy_pro_b': '//*[@id="treeZhiBiao_9_span"]',
    'crude_oil_b': '//*[@id="treeZhiBiao_11_span"]',
    'date_b': '//*[@id="mySelect_sj"]/div[2]/div[1]',
    'date_36_b': '//*[@id="mySelect_sj"]/div[2]/div[2]/div[2]/ul/li[3]'
}
#城市xpath路径
# cities_xpath_dir = []
# for i in range(2, 33):
#     cities_xpath_dir.append('//*[@id="mySelect_reg"]/div[2]/div[2]/div[2]/ul/li[%d]'%i)
cities_name_xpath = {
    '北京市': '', '天津市': '', '河北省': '', '山西省': '', '内蒙古自治区': '', '辽宁省': '', '吉林省': '', '黑龙江省': '',
    '上海市': '', '江苏省': '', '浙江省': '', '安徽省': '', '福建省': '', '江西省': '', '山东省': '', '河南省': '',
    '湖北省': '', '湖南省': '', '广东省': '', '广西壮族自治区': '', '海南省': '', '重庆市': '', '四川省': '', '贵州省': '',
    '云南省': '', '西藏自治区': '', '陕西省': '', '甘肃省': '', '青海省': '', '宁夏回族自治区': '', '新疆维吾尔自治区': ''
}
i = 2
for key, values in cities_name_xpath.items():
    cities_name_xpath[key] = '//*[@id="mySelect_reg"]/div[2]/div[2]/div[2]/ul/li[%d]'%i
    i = i+1
#各省份数据xpath路径
cities_data_xpath_dir_update = {
    'curr_value': '//*[@id="table_main"]/tbody/tr[1]/td[2]',
    'prev_value': '//*[@id="table_main"]/tbody/tr[1]/td[3]',
    'accum_value': '//*[@id="table_main"]/tbody/tr[2]/td[2]',
    'yoy_ratio': '//*[@id="table_main"]/tbody/tr[3]/td[2]',
    'accum_ratio': '//*[@id="table_main"]/tbody/tr[4]/td[2]'
}
#选择相关数据

for key, values in choose_xpath_dir.items():
    key = browser.find_element_by_xpath(values)
    browser.execute_script("arguments[0].click();", key)
    time.sleep(1)
#选择各省份数据
provence_id = 1
for key, values in cities_name_xpath.items():
    city_b = browser.find_element_by_xpath(values)
    browser.execute_script("arguments[0].click();", city_b)
    time.sleep(1)

    store_data = []
    store_data.append(key)
    store_data.append('国家数据')
    store_data.append('2018-05-01')
    store_data.append('1m')
    for key_data, values_data in cities_data_xpath_dir_update.items():
        va = browser.find_element_by_xpath(values_data).text
        store_data.append(va)
    store_data.insert(7, '万吨')
    store_data.append(str(provence_id))
    provence_id = provence_id + 1
    store_data.append('1')
    #print(store_data)
    save_to_mysql(store_data)




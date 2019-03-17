from selenium import webdriver
import time
import csv
import datetime

start_data = input('请输入开始日期（格式：2013-05-15）')
# CHROME_OPTIONS = webdriver.ChromeOptions()
# CHROME_OPTIONS.binary_location = "/opt/google/chrome/google-chrome" #chrome浏览器所在路径
# CHROME_OPTIONS.add_argument('headless') #不打开浏览器
# browser = webdriver.Chrome(chrome_options=CHROME_OPTIONS)
browser = webdriver.Chrome()
browser.get('https://www.cjrl.cn/jiedu/meiguo-337.html')
while True:
    try:
        getmore = browser.find_element_by_xpath('//*[@id="loadmore"]/a')
        getmore.click()
        time.sleep(1)
    except:
        break
date = browser.find_elements_by_xpath('//table[@id="datadetail"]//tr/td[1]')
f_value = browser.find_elements_by_xpath('//table[@id="datadetail"]//tr/td[3]')
p_value = browser.find_elements_by_xpath('//table[@id="datadetail"]//tr/td[5]')

with open('cjrl.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['日期', '前值', '公布值'])
    for i in range(0, len(date)):
        start_data_stamp = datetime.datetime.strptime(start_data, '%Y-%m-%d').timestamp()
        date_stamp = datetime.datetime.strptime(date[i].text.split(',')[0], '%Y-%m-%d').timestamp()
        if date_stamp < start_data_stamp:
            continue
        else:
            writer.writerow([date[i].text, f_value[i].text, p_value[i].text])







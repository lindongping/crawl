from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get(
    'http://price.sci99.com/view/priceview.aspx?pagename=energyview&classid=921&linkname=%E6%88%90%E5%93%81%E6%B2%B9&RequestId=1602d514c37c110f')
browser.find_element_by_xpath('//*[@id="LogInPart1_SciName"]').send_keys('jusure2016')
browser.find_element_by_xpath('//*[@id="LogInPart1_SciPwd"]').send_keys('jusure2017')
browser.find_element_by_xpath('//*[@id="LogInPart1_IB_Login"]').click()
browser.maximize_window()
time.sleep(5)

table = browser.find_elements_by_tag_name('tr')
# print(table)

oil_id = []
for tr_id in table:
    img_id = tr_id.get_attribute("id")
    if img_id:
        oil_id.append(img_id)
    else:
        pass
#print(len(oil_id))
time.sleep(1)

#所有的数据按每十个一组划分
oil_id_10 = [oil_id[i:i+10] for i in range(0, len(oil_id), 10)]
for lists in oil_id_10:  #对每组进行点击
    for base_id in lists:    #对每个进行点击
        id = 'img' + str(base_id)
        #print(id)
        browser.find_element_by_id(id).click()
        #browser.find_element_by_xpath('//*[@id="{}"]'.format(id)).click()
        time.sleep(0.5)
    #对每组进行处理
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="basket_close"]/a').click() #打开数据及曲线对比超链接
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="txtLineStartDate"]').clear() #清空日期范围
    browser.find_element_by_xpath('//*[@id="txtLineStartDate"]').send_keys('2018-01-01') #设置日期范围
    browser.find_element_by_xpath('//*[@id="boxhistorylink"]/b').click() #点击查看历史数据

    browser.switch_to_window(browser.window_handles[1]) #跳转到历史数据页面
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="lbTOExcel_original"]').click()
    time.sleep(1)
    browser.close()  # 关闭新窗口，节省内存

    browser.switch_to.window(browser.window_handles[0])  # 返回首页重新选取
    browser.find_element_by_xpath('//*[@id="basket_close"]/div/div[1]/div[3]/a[2]/b').click() #清空数据
    browser.find_element_by_xpath('//*[@id="basket_close"]/div/div[1]/div[1]/strong').click()#将点开的界面点掉




from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import csv
import time
import random
import os

project_list = ['踏歌智行','联动科技','魔视智能','安其威','Maxieye','深圳熵智科技','异方科技','探维科技',
                '力策科技','拍字节','撷知教育','哥瑞利软件','钛方科技','安声科技','擎朗科技','SRT软体机器人',
                'MobIQ','旗众智能科技','劲鑫科技','拓深科技']
for i in range(0,len(project_list)):
    fold_name = project_list[i]
    print('%s-----------------开始----------------------'%fold_name)
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'D:/task/%s' % fold_name}

    folder = os.path.exists('D:/task/%s'% fold_name)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs('D:/task/%s' % fold_name)

    options.add_experimental_option('prefs', prefs)

    browser = webdriver.Chrome(chrome_options=options)
    browser.get('http://pm.ecc-capital.com/passport/login.html')

    #登录
    browser.find_element_by_xpath('//*[@id="email"]').send_keys('fengbo.zhou')
    time.sleep(0.5)
    browser.find_element_by_xpath('//*[@id="password"]').send_keys('123456')
    time.sleep(0.5)
    browser.find_element_by_xpath('/html/body/div[1]/div[1]/dl/form/dd[3]/a/span').click()
    time.sleep(4)

    #查看项目列表
    browser.find_element_by_xpath('/html/body/div[2]/ul/li[2]/a/span').click()
    time.sleep(3)

    #获取具体信息
    # name = browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/table/tbody/tr[2]/td[2]/a').text
    browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/table/tbody/tr[%d]/td[2]/a'%(i+2)).click()
    time.sleep(3)

    #基本信息
    basic_message = browser.find_element_by_xpath('//*[@id="main"]/div/dl[4]/dd').text
    basic_message_txt = open('D:/task/%s/basic_message.txt'%fold_name, 'a')
    basic_message_txt.write(basic_message)
    basic_message_txt.close()
    print('基本信息写入完毕')
    #print(basic_message)
    time.sleep(2)

    #下载信息
    for i in range(1,100):
        try:
            browser.find_element_by_xpath('//*[@id="main"]/div/dl[3]/dd/div[%d]/a/span' % i).click()#word
            #browser.find_element_by_xpath('//*[@id="main"]/div/dl[3]/dd/div[%d]/a[2]/span' % i).click()  # word
            time.sleep(1)
        except:
            #break
            try:
                browser.find_element_by_xpath('//*[@id="main"]/div/dl[3]/dd/div[%d]/a[1]/span' % i).click()  # pdf
                time.sleep(1)
            except:
                break

    print('下载信息完毕')

    #会议信息
    browser.switch_to.frame('meeting')
    time.sleep(1)
    for i in range(1,100):
        try:
            meeting = browser.find_element_by_xpath('/html/body/div[1]/dl/dd[%d]' % i).text
            meeting_txt = open('D:/task/%s/meeting.txt' % fold_name, 'a')
            meeting_txt.write(meeting)
            meeting_txt.close()
        except:
            break
    print('会议信息写入完毕')

    #评论信息
    time.sleep(1)
    browser.switch_to.default_content()
    browser.switch_to.frame('comment')
    time.sleep(1)
    for i in range(1,100):
        try:
            comment = browser.find_element_by_xpath('/html/body/div[1]/dl/dd[%d]' % i).text
            if comment == '':
                break
            else:
                comment_txt = open('D:/task/%s/comment.txt' % fold_name, 'a')
                comment_txt.write(comment)
                comment_txt.close()
                print('评论信息写入完毕')
        except:
            break

    print('%s-----------------结束----------------------' % fold_name)
    time.sleep(2)





from selenium import webdriver
import time
import os


start_num = 1   #出问题了，修改这个数字，代表页码
end_num = 95
for kk in range(start_num,end_num):
    print('第%d页开始-----------------------------'%kk)
    browser = webdriver.Chrome()
    browser.get('http://pm.ecc-capital.com/invest/indexState.html?page=%d&state=10'%kk)

    browser.find_element_by_xpath('//*[@id="email"]').send_keys('fengbo.zhou')
    time.sleep(0.5)
    browser.find_element_by_xpath('//*[@id="password"]').send_keys('123456')
    time.sleep(0.5)
    browser.find_element_by_xpath('/html/body/div[1]/div[1]/dl/form/dd[3]/a/span').click()
    time.sleep(4)
    project_list = []
    for i in range(2,22):
        name = browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/table/tbody/tr[%d]/td[2]/a'%i).text
        project_list.append(name)
    print(project_list)
    browser.close()

    for j in range(0,len(project_list)):
        fold_name = project_list[j]
        print('%s--开始'%fold_name)
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'D:/tasks/%s' % fold_name}

        folder = os.path.exists('D:/tasks/%s'% fold_name)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs('D:/tasks/%s' % fold_name)

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

        browser.find_element_by_xpath('/html/body/div[2]/ul/li[2]/a/span').click()
        time.sleep(3)

        browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/table/thead/tr/td/form/div[1]/input[1]').send_keys(fold_name)
        time.sleep(0.5)
        browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/table/thead/tr/td/form/div[1]/a[2]/span').click()
        time.sleep(4)
        browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/table/tbody/tr[2]/td[2]/a').click()
        time.sleep(4)
        #查看项目列表
        # browser.find_element_by_xpath('/html/body/div[2]/ul/li[2]/a/span').click()
        # time.sleep(3)
        # browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/ul/li[10]/a').click()
        # time.sleep(5)
        #获取具体信息
        # name = browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/table/tbody/tr[2]/td[2]/a').text
        #browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/table/tbody/tr[%d]/td[2]/a'%(i+2)).click()
        # browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/table/tbody/tr[%d]/td[2]/a'%(i+2)).click
        #
        # time.sleep(3)

        #基本信息
        basic_message = browser.find_element_by_xpath('//*[@id="main"]/div/dl[4]/dd').text
        basic_message_txt = open('D:/tasks/%s/basic_message.txt'%fold_name, 'a')
        basic_message_txt.write(basic_message)
        basic_message_txt.close()
        #print('基本信息写入完毕')
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

        #print('下载信息完毕')

        #会议信息
        browser.switch_to.frame('meeting')
        time.sleep(1)
        for i in range(1,100):
            try:
                meeting = browser.find_element_by_xpath('/html/body/div[1]/dl/dd[%d]' % i).text
                meeting_txt = open('D:/tasks/%s/meeting.txt' % fold_name, 'a')
                meeting_txt.write(meeting)
                meeting_txt.close()
            except:
                break
        #print('会议信息写入完毕')

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
                    comment_txt = open('D:/tasks/%s/comment.txt' % fold_name, 'a')
                    comment_txt.write(comment)
                    comment_txt.close()
                    #print('评论信息写入完毕')
            except:
                break

        #print('%s----结束' % fold_name)
        time.sleep(2)
    print('第%d页结束-----------------------------' % kk)




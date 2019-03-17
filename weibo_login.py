from selenium import webdriver
import time

#browser = webdriver.Chrome()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

browser.get('https://weibo.com/')
#browser.maximize_window()
time.sleep(8)
qq_button = browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[5]/div/a[1]')  #qq图标
browser.execute_script("arguments[0].click();", qq_button)
time.sleep(8)

browser.switch_to.window(browser.window_handles[-1])
browser.switch_to.frame('ptlogin_iframe')
time.sleep(2)
n_p_login = browser.find_element_by_xpath('//*[@id="switcher_plogin"]') #账号密码登录
browser.execute_script("arguments[0].click();", n_p_login)
time.sleep(3)

browser.find_element_by_xpath('//*[@id="u"]').clear()
browser.find_element_by_xpath('//*[@id="u"]').send_keys('364287604')
time.sleep(3)
browser.find_element_by_xpath('//*[@id="p"]').send_keys('ldp520615$')
time.sleep(3)
login = browser.find_element_by_xpath('//*[@id="login_button"]')#登录成功
browser.execute_script("arguments[0].click();", login)

time.sleep(8)

start = 0
for j in range(1, 4):
    print("-----第%d次爬取开始----" % j)
    weibo_list = browser.find_elements_by_class_name('WB_feed_detail')  #微博用户名列表

    num = len(weibo_list)

    weibo_list = weibo_list[start:num]      #将已搜索完的部分去掉

    time.sleep(2)
    for i in weibo_list:
        title = i.find_element_by_class_name('WB_info').text
        print(title)
        time.sleep(1)
    start = len(weibo_list) * j     #已搜索完的部分长度
    print("-----第%d次爬取长度%d----" % (j, len(weibo_list)))
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 滚动到底端
    time.sleep(8)



from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import requests
import urllib.parse
import time
import csv


class BaiduHeatNum(object):
    User_name = '15524882680'
    User_pwd = 'ldp520615@'  # 使用有效的百度账号，现在是关联手机号了，我用的自己号测试的

    browser = webdriver.Chrome()
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # browser = webdriver.Chrome(chrome_options=chrome_options)

    wait = WebDriverWait(browser, 10)  # 等待的最大时间
    actions = ActionChains(browser)

    def login_baidu(self):  # 登录操作
        #url = 'http://index.baidu.com/baidu-index-mobile/#/'  # 移动版
        url = 'https://passport.baidu.com/v2/?login&u=http%3A%2F%2Findex.baidu.com%2Fbaidu-index-mobile%2F#/ '  #登录页面
        browser = self.browser

        browser.get(url)

        forth_click = browser.find_element_by_xpath('//*[@id="TANGRAM__PSP_3__footerULoginBtn"]')   #用户名登录
        forth_click.click()
        time.sleep(1)
        uin_input = browser.find_element_by_id('TANGRAM__PSP_3__userName')
        uin_input.clear()
        time.sleep(1)
        uin_input.send_keys(self.User_name)
        time.sleep(1)
        pwd_input = browser.find_element_by_id('TANGRAM__PSP_3__password')
        pwd_input.clear()
        pwd_input.send_keys(self.User_pwd)
        time.sleep(10)
        login_submit = browser.find_element_by_xpath('//*[@id="TANGRAM__PSP_3__submit"]')
        browser.execute_script("arguments[0].click();", login_submit)#登录
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="TANGRAM__22__button_send_mobile"]').click()#验证码
        time.sleep(15)
        browser.find_element_by_xpath('//*[@id="TANGRAM__22__button_submit"]').click()

    def get_index_by_selenium(self, theme):  # selenimu模拟鼠标方法获取指数
        browser = self.browser
        self.login_baidu()
        time.sleep(3)
        key_word_input = browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div/form/input')
        key_word_input.clear()
        key_word_input.send_keys(theme)
        time.sleep(2)
        key_word_input.send_keys(Keys.ENTER)
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[2]/div').click() #选取指定天数范围
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[4]').click()#90天
        time.sleep(1)
        browser.maximize_window()
        form_need = browser.find_element_by_xpath('//*[@id="trendChart"]/div[1]/canvas')#趋势图xpath
        #move_to_element_with_offset(to_element, xoffset, yoffset) ——移动到距某个元素（左上角坐标）多少距离的位置
        #perform() ——执行链中的所有动作
        with open('data_%s.csv' % theme, 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(['日期', '搜索指数'])
            start_index = 20  #图片开始索引
            end_index = 1000  #图片结束索引
            length = 8  #索引间隔
            for i in range(start_index, end_index, length):
                self.actions.move_to_element_with_offset(form_need, i, 100).perform()
                #time.sleep(1)
                datas = browser.find_element_by_xpath('//*[@id="trendChart"]/div[2]').text    #数据
                datas_list = datas.strip().split('%s:' % theme)
                date = datas_list[0].strip()
                price = datas_list[1].strip()
                spamwriter.writerow([date, price])


if __name__ == '__main__':
    baidu = BaiduHeatNum()
    baidu.get_index_by_selenium('大闸蟹')


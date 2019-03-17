from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get('https://www.tianyancha.com/')
time.sleep(1)
browser.find_element_by_xpath('//*[@id="web-content"]/div/div[1]/div[1]/div/div/div[2]/div[1]/a').click()
time.sleep(1)
browser.find_element_by_xpath('//*[@id="_modal_container"]/div/div/div[2]/div/div/div[3]/div[2]/div[1]').click()
time.sleep(1)
browser.find_element_by_xpath('//*[@id="_modal_container"]/div/div/div[2]/div/div/div[3]/div[1]/div[2]/input').send_keys('15524882680')
time.sleep(1)
browser.find_element_by_xpath('//*[@id="_modal_container"]/div/div/div[2]/div/div/div[3]/div[1]/div[3]/input').send_keys('ldp520615')
time.sleep(1)
browser.find_element_by_xpath('//*[@id="_modal_container"]/div/div/div[2]/div/div/div[3]/div[1]/div[5]').click()





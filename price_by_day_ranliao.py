
# coding: utf-8

# In[16]:


from selenium import webdriver

import time

def crawler():
    browser = webdriver.Chrome()
    browser.get('http://price.sci99.com/view/priceview.aspx?pagename=energyview&classid=273&linkname=%E7%87%83%E6%96%99%E6%B2%B9&RequestId=8666a32cb031681b')
    browser.find_element_by_xpath('//*[@id="LogInPart1_SciName"]').send_keys('jusure2016')
    browser.find_element_by_xpath('//*[@id="LogInPart1_SciPwd"]').send_keys('jusure2017')
    browser.find_element_by_xpath('//*[@id="LogInPart1_IB_Login"]').click()
    browser.maximize_window() 
    time.sleep(2)

    #table = browser.find_element_by_id('divContents')
    table = browser.find_elements_by_tag_name('tr')
    #print(table)

    oil_id = []
    for tr_id in table:
        img_id = tr_id.get_attribute("id")
        if img_id:
            oil_id.append(img_id)
        else:
            pass

    time.sleep(1)
    #browser.maximize_window() 

    small_list = [oil_id[i:i+10] for i in range(0,len(oil_id),10)]#每10个一选
    for id_list in small_list:
        for id in id_list:
            browser.find_element_by_xpath('//*[@id="img{}"]'.format(id)).click()#选择需下载的信息
            time.sleep(0.5)

        time.sleep(2)

        browser.find_element_by_xpath('//*[@id="basket_close"]/a').click()
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="txtLineStartDate"]').clear()
        browser.find_element_by_xpath('//*[@id="txtLineStartDate"]').send_keys(today)#当天日期
        browser.find_element_by_xpath('//*[@id="boxhistorylink"]/b').click()
        browser.switch_to_window(browser.window_handles[-1])
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="lbTOExcel_original"]').click()
        time.sleep(1)
        browser.close()#关闭新窗口，节省内存

        browser.switch_to_window(browser.window_handles[0])#返回首页重新选取
        browser.find_element_by_xpath('//*[@id="basket_close"]/div/div[1]/div[3]/a[2]/b').click()#清空数据
        browser.find_element_by_xpath('//*[@id="basket_close"]/a').click()#将点开的界面点掉
        
#today = '2018-06-05'
#crawler()


# In[14]:


import xlrd
import xlwt
import glob  
from numpy import * 

def price_today(date,name):
    #date = today
    biaotou=['时间','产品名称','最低价','最高价','平均价','单位','型号','生产企业','市场','区域','省','市','价格条件','备注','发改委零售限价','发改委批发限价']  

    filelocation="C:/Users/Admin/Downloads//"  #搜索多个表格存放处 
    fileform="xls"  #当前文件夹下搜索的文件名后缀  

    filedestination="C:/Users/Admin/Downloads/merge//"  #将合并后的表格存放到的位置  
    file="卓创_价格_{}_{}".format(name,date) #合并后的表格名 

    #首先查找默认文件夹下有多少文档需要整合  
     
    filearray=[]  
    for filename in glob.glob(filelocation+"*."+fileform):  
        filearray.append(filename)  
    #以上是从pythonscripts文件夹下读取所有excel表格，并将所有的名字存储到列表filearray 

    print("在默认文件夹下有%d个文档"%len(filearray))  
    ge=len(filearray)  
    matrix = [None]*ge  
    #实现读写数据  

    #下面是将所有文件读数据到三维列表cell[][][]中（不包含表头）  
    import xlrd  
    for i in range(ge):  
        fname=filearray[i]  
        bk=xlrd.open_workbook(fname)  
        try:  
            sh=bk.sheet_by_name("产品的原始历史数据")  #下载的sheet名字
        except:  
            print ("在文件%s中没有找到sheet1，读取文件数据失败,注意表格sheet的名字" %fname)  
        nrows=sh.nrows   
        matrix[i] = [0]*(nrows-1)  

        ncols=sh.ncols  
        for m in range(nrows-1):    
            matrix[i][m] = ["0"]*ncols  

        for j in range(1,nrows):  
            for k in range(0,ncols):  
                matrix[i][j-1][k]=sh.cell(j,k).value  

    #下面是写数据到新的合并表格中  
    #import xlwt  
    filename=xlwt.Workbook()  
    sheet=filename.add_sheet(date)  #新表格的sheet名（date）

    #下面是把表头写上  
    for i in range(0,len(biaotou)):  
        sheet.write(0,i,biaotou[i])  

    #求和前面的文件一共写了多少行  
    zh=1  
    for i in range(ge):  
        for j in range(len(matrix[i])):  
            for k in range(len(matrix[i][j])):  
                sheet.write(zh,k,matrix[i][j][k])  
            zh=zh+1  
    print("我已经将%d个文件合并成1个文件，并命名为%s.xls."%(ge,file))  
    filename.save(filedestination+file+".xls")  


# In[15]:


from datetime import datetime

def main():
    name = '燃料油'
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    crawler()
    price_today(today,name)
    
if __name__ == "__main__":
    main()


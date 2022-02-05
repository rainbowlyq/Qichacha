# -*- coding = utf-8 -*-
# @Time : 2022-02-04 17:23
# @Author : leeao
# @File : qccspider.py
# @Software : PyCharm

import time
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import xlrd
import xlwt
from urllib import parse


# 参数
run_time = 300
sleep_time = 1.0


def get_companylist(path):
    with xlrd.open_workbook(path) as f:
        sheet = f.sheet_by_index(0)
        # print(sheet.name, sheet.nrows, sheet.ncols)
        infolist = sheet.col_values(1)[1:]
        # print(cols)
    return infolist


def get_data(runtime, sleeptime):
    data = []
    for i in range(runtime):  # to be edited 300
        company = companylist[i]
        tgturl = 'https://www.qcc.com/web/search/trademark?key=' + parse.quote(company) + '&type=zhuanli'
        driver.get(tgturl)
        time.sleep(sleeptime)
        if driver.find_elements(By.CLASS_NAME, 'pills-item'):
            driver.find_elements(By.CLASS_NAME, 'pills-item')[5].click()
            time.sleep(sleeptime*0.5)
            patenttypes = driver.find_elements(By.CLASS_NAME, 'pills-item')[1:]
            patentinfo = {'公司名称': company}  # 单个企业的专利信息
            year = ['']
            publicflag = False
            for pt in patenttypes:
                txt = pt.text
                if len(txt) > 0:
                    left = txt.find('(')
                    right = txt.find(')')
                    name = txt[:left-1]
                    if publicflag:
                        name = 'public' + name
                    elif year[-1] < name < '3000':
                        publicflag = True
                        name = 'public' + name
                    else:
                        year.append(name)
                    num = int(txt[left+1:right])
                    patentinfo[name] = num
                else:
                    pass
            data.append(patentinfo)
            # print(patentinfo)
        else:
            print(company + ' fail')
        print("process status: %d/%d" % (i + 1, runtime))  # to be edited 300

    return data


def save_data(data, path):
    print("saving data...please wait...")
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('patent', cell_overwrite_ok=True)

    stddic = {'公司名称': 0,
              '外观设计': 1, '实用新型': 2, '发明公布': 3, '发明授权': 4,
              '权利终止': 5, '授权': 6, '未缴年费': 7, '实质审查': 8, '期限届满': 9, '驳回': 10, '公开': 11, '撤回': 12,
              '避重授权': 13, '权利恢复': 14, '全部无效': 15, '部分无效': 16, '放弃': 17,
              '2021': 18, '2020': 19, '2019': 20, '2018': 21, '2017': 22, '2016': 23, '2015': 24, '2014': 25,
              '2013': 26, '2012': 27,
              'public2022': 28, 'public2021': 29, 'public2020': 30, 'public2019': 31, 'public2018': 32, 'public2017': 33,
              'public2016': 34, 'public2015': 35, 'public2014': 36, 'public2013': 37}
    for j in range(len(stddic)):
        sheet.write(0, j, list(stddic.keys())[j])

    for i in range(len(data)):
        for j in range(len(stddic)):
            try:
                jkey = list(stddic.keys())[j]
                sheet.write(i+1, j, data[i][jkey])
            except KeyError:
                sheet.write(i+1, j, '')
    book.save(path)


xlsfilepath = 'hs300.xls'
savepath = 'output.xls'

companylist = get_companylist(xlsfilepath)

with selenium.webdriver.Chrome() as driver:
    driver.maximize_window()

    driver.get('https://www.qcc.com/')
    searchbox = driver.find_element(By.ID, 'searchKey')
    searchbox.send_keys("贵州茅台")
    time.sleep(0.1)
    searchbox.send_keys(Keys.ENTER)

    mydata = get_data(run_time, sleep_time)

save_data(mydata, savepath)

print("finish")

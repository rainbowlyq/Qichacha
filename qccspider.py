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
run_time = 300  # 运行次数
sleep_time = 1.0  # 延迟时间
xlsfilepath = 'hs300.xls'  # 读入文件
savepath = 'output.xls'  # 输出文件


def get_companylist(path):
    with xlrd.open_workbook(path) as f:  # 打开excel文件
        sheet = f.sheet_by_index(0)
        infolist = sheet.col_values(1)[1:]  # 读取第二列（公司名称）
    return infolist


def get_data(runtime, sleeptime):
    data = []
    for i in range(runtime):
        company = companylist[i]  # 获取公司名称
        # 用encodeURI编码了一下汉字（其实也可以不编码）
        tgturl = 'https://www.qcc.com/web/search/trademark?key=' + parse.quote(company) + '&type=zhuanli'  # 获取目标网址
        driver.get(tgturl)
        time.sleep(sleeptime)
        if driver.find_elements(By.CLASS_NAME, 'pills-item'):
            driver.find_elements(By.CLASS_NAME, 'pills-item')[5].click()  # 点击筛选申请人
            time.sleep(sleeptime*0.5)
            patenttypes = driver.find_elements(By.CLASS_NAME, 'pills-item')[1:]  # 获取所有专利信息
            patentinfo = {'公司名称': company}  # 单个企业的专利信息
            year = ['']  # 用于判断是否进入“公开年份”
            publicflag = False
            for pt in patenttypes:
                txt = pt.text
                if len(txt) > 0:  # 跳过空项
                    left = txt.find('(')
                    right = txt.find(')')
                    name = txt[:left-1]
                    if publicflag:
                        name = 'public' + name
                    elif year[-1] < name < '3000':
                        publicflag = True
                        year.clear()
                        name = 'public' + name
                    else:
                        year.append(name)
                    num = int(txt[left+1:right])  # 从括号中取数字
                    patentinfo[name] = num  # 以字典形式储存
                else:
                    pass
            data.append(patentinfo)  # 将字典加入总列表
        else:
            print(company + ' fail')
        print("process status: %d/%d" % (i + 1, runtime))  # 进度监视

    return data


def save_data(data, path):
    print("saving data...please wait...")
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('patent', cell_overwrite_ok=True)

    stddic = {'公司名称': 0,
              '外观设计': 1, '实用新型': 2, '发明公布': 3, '发明授权': 4,  # 专利类型
              '权利终止': 5, '授权': 6, '未缴年费': 7, '实质审查': 8, '期限届满': 9, '驳回': 10, '公开': 11, '撤回': 12,
              '避重授权': 13, '权利恢复': 14, '全部无效': 15, '部分无效': 16, '放弃': 17,  # 法律状态
              '2021': 18, '2020': 19, '2019': 20, '2018': 21, '2017': 22, '2016': 23, '2015': 24, '2014': 25,
              '2013': 26, '2012': 27,  # 申请年份
              'public2022': 28, 'public2021': 29, 'public2020': 30, 'public2019': 31, 'public2018': 32, 'public2017': 33,
              'public2016': 34, 'public2015': 35, 'public2014': 36, 'public2013': 37}  # 公开年份
    for j in range(len(stddic)):
        sheet.write(0, j, list(stddic.keys())[j])  # 打印首行

    for i in range(len(data)):
        for j in range(len(stddic)):
            try:
                jkey = list(stddic.keys())[j]  # 获取首行名称
                sheet.write(i+1, j, data[i][jkey])  # 存入字典
            except KeyError:
                sheet.write(i+1, j, '')
    book.save(path)


companylist = get_companylist(xlsfilepath)

with selenium.webdriver.Chrome() as driver:
    driver.maximize_window()  # 最大化窗口
    driver.get('https://www.qcc.com/')
    searchbox = driver.find_element(By.ID, 'searchKey')
    searchbox.send_keys("贵州茅台")  # 向搜索框输入“贵州茅台”
    time.sleep(0.1)
    searchbox.send_keys(Keys.ENTER)  # 按回车
    mydata = get_data(run_time, sleep_time)

save_data(mydata, savepath)

print("finish")

# -*- coding = utf-8 -*-
# @Time : 2022-02-04 21:03
# @Author : leeao
# @File : waste_clicks.py
# @Software : PyCharm

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
print('2000'>'名称')

def waste_clicks():
    tgturl = 'https://www.qcc.com/'
    with selenium.webdriver.Chrome() as driver:
        driver.maximize_window()

        driver.get('https://www.qcc.com/')
        searchbox = driver.find_element(By.ID, 'searchKey')
        searchbox.send_keys("贵州茅台")
        time.sleep(0.1)
        searchbox.send_keys(Keys.ENTER)
        time.sleep(0.1)

        sbzl = driver.find_element(By.XPATH, r'/html/body/div[1]/div[2]/div[1]/div/div/div[5]/a')  # 专利商标
        # WebDriverWait(driver, 3).until(EC.element_to_be_clickable(sbzl))
        sbzl.click()
        time.sleep(0.1)

        tgtlist = driver.find_element(By.XPATH, r'/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div/div')
        tgts = driver.find_elements(By.CLASS_NAME, 'tab-item')
        # for tgt in tgts:
        #     print(tgt.text)
        tgts[1].click()
        time.sleep(3)

# -*- coding = utf-8 -*-
# @Time : 2022-02-05 15:26
# @Author : leeao
# @File : baiten.py
# @Software : PyCharm
from urllib import parse
from selenium import webdriver
import time

b = '%253A%2528%25E5%25B9%25B3%25E5%25AE%2589%25E9%2593%25B6%25E8%25A1%258C%25E8%2582%25A1%25E4%25BB%25BD%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8%2529%2B'
c = parse.unquote(b)
d = parse.unquote(c)
print(c,d)
test = ':(贵州茅台)+'
b = parse.quote(parse.quote(test))
a = 'https://www.baiten.cn/results/s/pa'+b+'/.html?type=s'
with webdriver.Chrome() as driver:
    driver.maximize_window()  # 最大化窗口
    driver.get(a)
    time.sleep(10)


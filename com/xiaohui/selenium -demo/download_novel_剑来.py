#code: utf-8

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import requests

import os
import time

def download(url, filePath):
    '''
    爬去笔趣阁的剑来小说
    :param url: 笔趣阁地址
    :param filePath: 小说写入的文件
    :return:
    '''
    browser = webdriver.Chrome()
    browser.get(url)

    WebDriverWait(browser, 10).until(lambda b: b.find_element_by_css_selector('dt.title:last-of-type').is_displayed())
    titles = browser.find_elements_by_css_selector('dt.title:last-of-type~dd>a')
    # print('url: %s title: %s' % (title.get_attribute('href'), title.text))

    user_agent = R"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
    headers = {"User-Agent": user_agent}

    with open(filepath, "a+", encoding="utf-8") as f:
        for title in titles:
            print('url: %s title: %s' % (title.get_attribute('href'), title.text))
            chapterUrl = title.get_attribute('href')
            chapterTitle = title.text

            f.write(chapterTitle+'\n')
            f.write(chapterUrl+'\n')

            curr_resp = requests.get(url=chapterUrl, headers=headers)
            '''
            time 等待，requests 的状态值验证，selenium 的等待，都无法爬去完全小说
            '''
            while curr_resp.status_code != 200:
                curr_resp = requests.get(url=chapterUrl, headers=headers)
                print('circle url: %s title: %s' % (title.get_attribute('href'), title.text))

            # time.sleep(10)
            curr_soup = BeautifulSoup(str(curr_resp.content.decode(encoding='utf-8')), 'html.parser')
            book = curr_soup.select_one(selector='#BookText')
            book_ps = book.find_all('p')
            for p in book_ps:
                f.write(str(' ' * 4 + p.text + '\n'))

    browser.quit()

url = 'http://www.jianlaixiaoshuo.com/'
filepath = os.getcwd()+u'\剑来.txt'
download(url, filepath)

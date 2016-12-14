#!/usr/bin/python3
# 修改中
import re
import requests
from bs4 import BeautifulSoup
import os

class mzt():
    # 选择下载的图片系列
    def in_url(self, url):
        while True:
            select_img = input("请选择下载的类型('花花公子系列'（h）或'无圣光套图系列'(w)): ")
            if select_img == 'h':
                s_url = url + 'zhainanshe/'
                return s_url
            elif select_img == 'w':
                s_url = url + 'luyilu/'
                return s_url
            else:
                print("输入错误")
                continue
    # 获取网页内容
    def request(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'}
        start_html = requests.get(url, headers=headers)
        start_html.encoding = 'gb18030'
        return start_html
    # 切割url
    def cut_url(self, url):
        cut = re.compile(r'h.*/')
        c_url = re.findall(cut, url)
        return c_url
    # 获取下一页面编号
    def next_url(self, html):
        try:
            next_url = html.find('li', "next-page").find('a')['href']
            return next_url
        except:
            next_url = ''
            return next_url
    # 使用BeautifulSoup解析
    def get_html(self, url):
        html = self.request(url)
        Soup = BeautifulSoup(html.text, 'lxml')
        return Soup
    # 获取图片url
    def get_img(self, url):
        j_url = []
        html = self.get_html(url)
        img_url = html.find('article', "article-content").find_all('p')
        cut = re.compile(r'http.*jpg')
        for i_jpg in img_url:
            jpg_url = re.findall(cut, str(i_jpg))            # 获取图片url
            j_url.extend(jpg_url)
        return j_url

    def get_next_url(self, url_h, url_t):
        a_url = []
        while True:
            next_url = url_h                    # 套图页面url
            urlh = self.cut_url(url_h)          # 切割出url前部分
            urlt = self.next_url(url_t)         # 获取下一页的url尾部
            n_url = urlh[0] + urlt              # 下一页套图url
            url_h = n_url                       # 赋值给下一页，方便转换
            url_t = self.get_html(next_url)     # 获取下一页页面内容
            a_url.append(next_url)
            if n_url == urlh[0]:
                url = list(set(a_url))
                url.sort(key=a_url.index)
                return url
    # 主程序
    def a_url(self, url):
        s_url = self.in_url(url)                # 进行挑选
        url_header = 'http://zhaofuli.xyz'
        html = self.get_html(s_url)             # 获得html
        a_list = html.find('div', "content").find_all('h2')    # 找到套图url的范围
        for a in a_list:
            title = a.get_text()               # 获取该套图名称
            href = url_header + a.find('a')['href']            # 获取套图url
            img_html = self.get_html(href)     # 获取套图的网页内容
            imgL = img_html
            imgh = href
            n_url = self.get_next_url(imgh, imgL)
            for i_url in n_url:
                imgg = self.get_img(i_url)
                for im in imgg:
                    print(im)
                
                        
                        
           

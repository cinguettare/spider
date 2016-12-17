#!/usr/bin/python3

import os
import re
from bs4 import BeautifulSoup
from Myuseragent import myrequest

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
        start_html = myrequest.get(url, 3)
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
            jpg_url = re.findall(cut, str(i_jpg))   # 获取图片url
            j_url.extend(jpg_url)
        return j_url

    # 获取下一页rul
    def get_next_url(self, url, html):
        a_url = []
        while True:
            next_url = url                     # 套图页面url
            c_url = self.cut_url(url)          # 切割出url前部分
            h_url = self.next_url(html)        # 获取下一页的url尾部
            n_url = c_url[0] + h_url           # 下一页套图url
            url = n_url                        # 赋值给下一页，方便转换
            html = self.get_html(next_url)     # 获取下一页页面内容
            a_url.append(next_url)
            if n_url == c_url[0]:
                url_l = list(set(a_url))
                url_l.sort(key=a_url.index)
                return url_l

    # 建立文件夹
    def mkdir(self, path):
        path = str(path).strip()
        isExists = os.path.exists(os.path.join("E:\meizitu", path))
        if not isExists:
            print(u"建立", path, u"文件夹！")
            os.makedirs(os.path.join("E:\meizitu", path))
            os.chdir("E:\meizitu\\" + path)
        else:
            print(path, u"已经存在了！")
            return False

    # 保存图片
    def save(self, img_url):
        name = img_url[-14:-4]
        img = self.request(img_url)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    # 主程序
    def a_url(self, url):
        url_header = 'http://zhaofuli.xyz'
        f_url = self.in_url(url)               # 获得url
        html = self.get_html(f_url)            # 获得html
        all_url = self.get_next_url(f_url, html)
        for f in all_url:
            a_list = f.find('div', "content").find_all('h2')    # 找到套图url的范围
            for a in a_list:
                title = a.get_text()               # 获取该套图名称
                self.mkdir(title)
                href = url_header + a.find('a')['href']         # 获取套图url
                img_html = self.get_html(href)     # 获取套图的网页内容
                n_url = self.get_next_url(href, img_html)       # 获取每一页的套图url
                for i in n_url:
                    a_jpg = self.get_img(i)
                    for jpg_url in a_jpg:
                        self.save(jpg_url)



Mzt = mzt()
Mzt.a_url('http://zhaofuli.xyz/')
                
                        
                        
           

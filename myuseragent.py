#!/usr/bin/python3

import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class ua():

    # 获取代理ip网址
    def Get_url(self, page):
        url = 'http://www.kuaidaili.com/free/inha/'
        url_list = []
        for p in range(page, page+5):
            new_url = url + str(p)
            url_list.append(new_url)
        return url_list

    # 获得代理ip
    def Get_ip(self, page):
        try:
            print(u"获取代理中。。。")
            url_list = self.Get_url(page)
            for u in url_list:
                html = requests.get(u, headers=headers)
                soup = BeautifulSoup(html.text, 'lxml')
                iplist = soup.find('tbody').find_all('tr')
                for i in iplist:
                    iii = i.find_all('td', limit=2)
                    ip = iii[0].string
                    port = iii[1].string
                    proxy = ip+':'+port
                    self.Detect_ip(proxy)
        except:
            print(u"代理已用完！")

    # 检测ip是否能够使用
    def Detect_ip(self, ip):
        ip = ''.join(ip.strip())
        proxy = {'http': ip}
        test_time = 2
        try:
            requests.get(url_test, headers=headers, proxies=proxy, timeout=test_time)
            print(u'%s合格， 保存' % proxy)
            ip_list.append(ip)
        except:
            print(u'%s不合格' % proxy)
            pass

    # 获取后续的代理网址页面
    def Get_proxy(self, page):
        if ip_list:
            self.Get_ip(page+5)
        else:
            proxy = ip_list.pop()
            return proxy

    # 代理
    def get(self, url, proxy_flog=False, n=1):
        if not proxy_flog:
            try:
                img_html = requests.get(url, headers=headers, timeout=10)
                time.sleep(5)
                return img_html
            except:
                print(u"开始使用代理！")
                return self.get(url, proxy_flog=True)
        else:
            try:
                time.sleep(5)
                proxy = {'http': self.Get_proxy(n)}
                img_html = requests.get(url, headers=headers, proxies=proxy, timeout=10)
                print(u"现在使用的代理为：", proxy)
                if img_html.status_code == 200:
                    return img_html
                else:
                    time.sleep(5)
                    return self.get(url, proxy_flog=True)
            except:
                n += 5
                return self.get(url, proxy_flog=True, n=n)







ip_list = []
url_test = 'https://www.baidu.com'
headers = {'User-Agent': UserAgent().random}
myrequest = ua()


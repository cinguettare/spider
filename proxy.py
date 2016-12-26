# ip池半成品
# 有空再改


import requests
import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient
from fake_useragent import UserAgent

class getip():

    def __init__(self):
        client = MongoClient()
        db = client['ipcunfang']
        self.ip_collection = db['iplist']
        self.title = 'proxy'
        self.ip_list = []

    def Get_url(self, url):
        url_list = []
        for p in range(1, 1400):
            new_url = url + str(p)
            url_list.append(new_url)
        return url_list

    def Get_ip(self, url):
        url_list = self.Get_url(url)
        for u in url_list:
            print(u)
            html = requests.get(u, headers=headers)
            soup = BeautifulSoup(html.text, 'lxml')
            iplist = soup.find('tbody').find_all('tr')
            for i in iplist:
                iii = i.find_all('td', limit=2)
                ip = iii[0].string
                port = iii[1].string
                proxy = ip+':'+port
                self.Detect_ip(proxy)


    def Detect_ip(self, ip):
        ip = ''.join(ip.strip())
        proxy = {'http': ip}
        test_time = 3
        try:
            requests.get(url_test, headers=headers, proxies=proxy, timeout=test_time)
            print(u'%s合格， 保存' % proxy)
            self.ip_list.append(ip)
        except:
            print(u'%s不合格' % proxy)
            pass
        if len(self.ip_list) > 80:
            post = {
                '标题': self.title,
                'ip代理': self.ip_list,
                '获取时间': datetime.datetime.now()
            }
            self.ip_collection.save(post)
            print('ip已存入数据库')
        else:
            pass

    def Delete_ip(self, num):

        pass



url = 'http://www.kuaidaili.com/free/inha/'
url_test = 'https://www.baidu.com'
headers = {'User-Agent': UserAgent().random}
getIP = getip()
getIP.Get_ip(url)

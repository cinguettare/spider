import re
import time
import requests
import random
from fake_useragent import UserAgent


class Myheader():

    def __init__(self):
        self.iplist = []                                      # 存放ip
        html = requests.get("http://haoip.cc/tiqu.htm")
        iplistn = re.findall(r'r/>(.*?)<b', html.text, re.S)  # 获取ip
        for ip in iplistn:
            i = re.sub('\n', '', ip)                          # 替换\n
            self.iplist.append(i.strip())

    def get(self, url, timeout, proxy=None, num_retries=5):
        ua = UserAgent().random                              
        headers = {'User-Agent': ua}                          # 获得UA

        if proxy == None:
            try:                       # 先不使用代理
                return requests.get(url, headers=headers, timeout=timeout)
            except:                    # 爬虫被阻止后，进行这一步
                if num_retries > 0:
                    time.sleep(10)
                    print(u'获取网页出错，10s后将获取倒数第', num_retries, u'次')
                    return self.get(url, timeout, num_retries-1)
                else:
                    print(u"开始使用代理")
                    time.sleep(10)
                    IP = ''.join(str(random.choice(self.iplist)).strip())
                    proxy = {'http':IP}
                    return self.get(url, timeout, proxy)
        else:                          # 代理
            try:
                IP = ''.join(str(random.choice(self.iplist)).strip())
                proxy = {'http': IP}
                return requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
            except:
                if num_retries > 0:
                    time.sleep(10)
                    IP = ''.join(str(random.choice(self.iplist)).strip())
                    proxy = {'http': IP}
                    print(u'正在更换代理，10s后将重新获取倒数第', num_retries, u'次')
                    print(u'当前代理是：', proxy)
                    return self.get(url, timeout, proxy, num_retries-1)
                else:
                    print(u'代理出错！ 取消代理！')
                    return self.get(url, 3)

myrequest = Myheader()

# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
import random
import requests
from scrapy.selector import Selector

class ProxyMiddleWare(object):
    # 初始化
    def __init__(self, ip='',IP_NUM=5):
        self.ip_list=[]
        self.IP_NUM=IP_NUM
        self.crawl_ips()
        self.ip = random.choice(self.ip_list)
    # 请求处理
    def process_request(self, request, spider):
        # 使用代理IP
        proxy_url = "http://%s:%s" % self.ip
        request.meta['proxy']=proxy_url
    def crawl_ips(self):
        # 爬取西刺的免费ip代理
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
        flag=False
        for i in range(50):
            re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
            selector = Selector(text=re.text)
            all_trs = selector.css("#ip_list tr")
            for tr in all_trs[1:]:
                all_texts = tr.css("td::text").extract()
                ip = all_texts[0]
                port = all_texts[1]
                if self.judge_ip(ip, port):
                    self.ip_list.append((ip, port))
                if len(self.ip_list)>=self.IP_NUM:
                    flag=True
                    break
            if flag:
                break
        print("--------------爬取西刺代理IP完成-----------------")
    def kuaidaili_crawl_ips(self):
        # 爬取西刺的免费ip代理
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
        flag=False
        for i in range(1,50):
            url = "https://www.kuaidaili.com/free/inha/{0}".format(i)
            re = requests.get(url,headers=headers)
            selector = Selector(text=re.text)
            all_trs = selector.css("#list tr")
            for tr in all_trs[1:]:
                all_texts = tr.css("td::text").extract()
                ip = all_texts[0]
                port = all_texts[1]
                # proxy_type = all_texts[3]
                # speed_str = all_texts[5]
                # if speed_str:
                #     speed = float(speed_str.split("秒")[0])
                if self.judge_ip(ip, port):
                    self.ip_list.append((ip, port))
                if len(self.ip_list)>=self.IP_NUM:
                    flag=True
                    break
            if flag:
                break
        print("--------------爬取快代理IP完成-----------------")
    def judge_ip(self, ip,port):
        #判断ip是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip,port)
        try:
            proxy_dict = {
                "http":proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict,timeout=3)
        except Exception as e:
            print ("invalid ip and port")
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print ("effective ip")
                return True
            else:
                print  ("invalid ip and port")
                return False
    def process_response(self,request, response, spider):
        # 处理代理IP不可用的情况
        print("process_response")
        if response.status != 200:
            #  出现异常对当前request加上新代理
            self.get_random_ip()
            proxy_url = "http://%s:%s" % self.ip
            print("-----原代理IP:%s,--现代理IP:%s-----" % (request.meta['proxy'], proxy_url))
            request.meta['proxy'] = proxy_url
            return request
        return response
    # 超时异常 User timeout caused connection failure    took longer than 180.0 seconds..
    def process_exception(self,request, exception, spider):
        # [<twisted.python.failure.Failure twisted.internet.error.ConnectionLost: Connection to the other side was lost in a non-clean fashion: Connection lost.>]
        # Could not open CONNECT tunnel with proxy 61.135.217.7:80 [{'status': 400, 'reason': b'Bad Request'}]
        print("process_exception")
        print(exception)
        #  出现异常对当前request加上新代理
        # self.get_random_ip()
        self.ip=random.choice(self.ip_list)
        proxy_url = "http://%s:%s" % self.ip
        print("-----原代理IP:%s,--现代理IP:%s-----" % (request.meta['proxy'], proxy_url))
        request.meta['proxy'] = proxy_url
        return request

    def process_spider_exception(self,request, exception, spider):
        print("process_spider_exception")
        print(exception)
        #  出现异常对当前request加上新代理
        self.get_random_ip()
        proxy_url = "http://%s:%s" % self.ip
        print("-----原代理IP:%s,--现代理IP:%s-----" % (request.meta['proxy'],proxy_url))
        request.meta['proxy'] = proxy_url
        return request
    def get_random_ip(self):
        self.ip_list.remove(self.ip)
        while True:
            if len(self.ip_list) > 0:
                thisip = random.choice(self.ip_list)
                ip=thisip[0]
                port=thisip[1]
                if self.judge_ip(ip, port):
                    self.ip = thisip
                    break
                else:
                    self.ip_list.remove(thisip)
            else:
                self.kuaidaili_crawl_ips()
        print("-------------代理IP已更换-------------------")

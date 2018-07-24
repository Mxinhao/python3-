#coding:utf-8
import requests
from bs4 import BeautifulSoup
import json
import os
import warnings
warnings.filterwarnings("ignore")
url="https://172.104.76.138:443"
headers={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}
page_source=requests.get(url,headers=headers,verify=False).text
soup=BeautifulSoup(str(page_source),"html.parser")
datas=soup.find_all(attrs={'class':'hover-text'})
configs=[]
for data in datas:
    shadow={}
    h4s=data.find_all("h4")
    shadow["server"]=h4s[0].span.string
    shadow["server_port"]=h4s[1].span.string.replace("\n","")
    shadow["password"] = h4s[2].span.string.replace("\n","")
    shadow['method']= str(h4s[3].string).split(":")[1]
    shadow['remarks'] = ""
    configs.append(shadow)
shadow_data={}
shadow_data["configs"]=configs
shadow_data["index" ]= 0
shadow_data["global"] = False
shadow_data["enabled"] = True
shadow_data["shareOverLan"] = False
shadow_data["isDefault"] = False
shadow_data["localPort"] = 1080
shadow_data["pacUrl"] = ""
shadow_data["useOnlinePac"] = False
print(shadow_data)
with open("D:\\gui-config.json","w") as file:
    file.write(json.dumps(shadow_data))
os.system("D:\\Shadowsocks.exe")


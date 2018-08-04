#coding:utf-8
from tornado.web import RequestHandler
import requests
from bs4 import BeautifulSoup
import json
class TagHander(RequestHandler):
    def get(self):
        page=requests.get("http://www.dbmeinv.com").text
        soup=BeautifulSoup(page,"html.parser")
        tags=soup.find("div",{"id":"main"}).find("div",{"class":"panel-heading"}).find_all("li")
        items=[]
        for tag in tags[1:]:
            item={}
            item["href"]=tag.find("a").get("href")
            item["cid"]=item["href"].split("?cid=")[-1]
            item["title"]=tag.text
            items.append(item)
        self.write(json.dumps({"code": 0, "msg": "", "data": items},"utf-8"))
class PicHander(RequestHandler):
    def get(self):
        cid=self.get_argument("cid")
        page = int(self.get_argument("p"))
        route = 'cid=' + str(cid) + '&pager_offset=' + str(page)
        url="https://www.dbmeinv.com/index.htm?"+route
        r=requests.get(url).text
        soup = BeautifulSoup(r, "html.parser")
        images=soup.find_all("div",{"class":"img_single"})
        imgs = []
        for image in images:
            img={}
            img["url"]=image.find("a").get("href")
            img["title"]=image.find("img").get("title")
            img["src"] = image.find("img").get("src")
            imgs.append(img)
        self.write(json.dumps({"code": 0, "msg": "success", "data": imgs}, "utf-8"))



# imgs = []
#         start=(page-1)*15
#         end=page*15
#         base_url="http://127.0.0.1:8889/static/image/"
#         fs = os.listdir("static/image")
#         lens=len(fs)
#         if lens<end:
#             imgs = []
#         else:
#             for f1 in fs[start:end]:
#                 imgs.append({
#                     "href":base_url+f1,
#                     "title":f1,
#                     "largeSrc":base_url+f1,
#                     "thumbSrc":base_url+f1,
#                     "smallSrc": base_url + f1
#                 })
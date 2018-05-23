#coding:utf-8
import sys
import io
import requests
import time
import json
import warnings
import hashlib

warnings.filterwarnings('ignore')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
login_name=""
login_pass=""
qr_path="qr.jpg"#二维码保存位置
cookies_path="save_cookies.txt"

headers={
	"Accept":"*/*",
	"Accept-Encoding":"gzip, deflate, br",
	"Accept-Language":"zh-CN,zh;q=0.9",
	"Connection":"keep-alive",
	"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
	"Host":"mp.weixin.qq.com",
	"Origin":"https://mp.weixin.qq.com",
	"Referer":"https://mp.weixin.qq.com/",
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
	"X-Requested-With":"XMLHttpRequest"
}
session=requests.Session()
session.headers=headers
# 获取图文分析数据确认是否已经登录
def tuwen_analysis_data(begin_date,end_date,token):
	analysis_url="https://mp.weixin.qq.com/misc/appmsganalysis?"
	tuwen_params={
		"action":"all",
		"begin_date":begin_date,#"2018-05-14",
		"end_date":end_date,#"2018-05-20",
		"order_by":"1",
		"order_direction":"2",
		"token":token,
		"lang":"zh_CN",
		"f":"json",
		"ajax": "1",
		"random": "0.36745056889158034"
	}
	r = session.get(analysis_url, params=tuwen_params, headers=headers).json()
	return r
# 开始登录
def login(login_name,pass_md5):
	login_data = {
		"username": login_name,
		"pwd": pass_md5,
		"imgcode": "",
		"f": "json",
		"userlang": "zh_CN",
		"token": "",
		"lang": "zh_CN",
		"ajax": "1"
	}
	login_url = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin"
	r = session.post(login_url, data=login_data, verify=False)
	session.headers["Set-Cookie"] = r.headers["Set-Cookie"]
	print("--------已经开始登录------------------")
# 	获取二维码并保存
def get_qr():
	qr_url = "https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=getqrcode&param=4300&rd=120"
	r = session.get(qr_url, verify=False)
	with open(qr_path, "wb") as f:
		f.write(r.content)
	print("---------二维码已生成---"+str(qr_path)+"---------------")
# 	确认是否已扫描二维码
def saomiao_qr():
	while True:
		url="https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=ask&f=json&ajax=1&random=0.72205"
		r = session.get(url,verify=False)
		# print(r.json()["status"])
		time.sleep(10)
		if r.json()["status"] == 1:
			break
		else:
			print("------未扫描二维码-------")
	print("----------已扫描二维码确认登录-------------")
# 	获取token
def get_token():
	token_url = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=login"
	param = {
		"userlang": "zh_CN",
		"token": "",
		"lang": "zh_CN",
		"f": "json",
		"ajax": "1"
	}
	r = session.post(token_url, data=param)
	token = str(r.json()["redirect_url"]).split("&")[-1].split("=")[-1]
	print("-----token已获取-------------")
	return token
# 保存cookie
def save_cookie():
	cookies=""
	for cook in session.cookies:
		cookies=cookies+str(cook.name)+"="+str(cook.value)+";"
	with open(cookies_path,"w") as f:
		f.write(cookies[:-1])
	print('-----cookies已保存至'+str(cookies_path)+"--------------")
# 	对密码进行md5加密
def md5str(str):
	md5_str = hashlib.md5(str.encode("utf-8"))
	return md5_str.hexdigest()
# 主方法
def main(login_name,pass_md5):
	login(login_name,pass_md5)
	get_qr()
	saomiao_qr()
	token=get_token()
	save_cookie()
	data=tuwen_analysis_data("2018-05-14","2018-05-21",token)
	print(data)

# 程序入口
if __name__ == '__main__':
	main(login_name,md5str(login_pass))

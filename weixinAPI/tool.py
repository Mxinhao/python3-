#coding:utf-8
import requests
import time
import datetime
import json
import urllib
import config
from db import WeiXinCorpInfo,dbsession,WeiXinFollowersHistory
# 以@post_request 进行注解的方法，调用方法的参数均为weixin_id:微信ID,post_data:post参数字典，具体参数参照微信API文档
# 以@get_request 进行注解的方法，调用方法的参数均为weixin_id:微信ID,params:get参数字典，具体参数参照微信API文档
# 获取access_token,先从数据库获取，验证是否有效，无效时再从微信获取。每次获取会使之前的失效
def get_access_token(weixin_id):
	weixin_info=dbsession.query(WeiXinCorpInfo).filter(WeiXinCorpInfo.weixin_id == weixin_id)
	if check_access_token(weixin_info[0].access_token):
		ACCESS_TOKEN = weixin_info[0].access_token
	else:
		# 从微信获取access_token
		access_token_url =config.wechat_api["access_token"] + weixin_info[0].appid + "&secret=" + weixin_info[0].appsecret
		r=requests.get(url=access_token_url).json()
		print(r)
		ACCESS_TOKEN = r["access_token"]
		expire_time=r["expires_in"]
		dbsession.query(WeiXinCorpInfo).filter(WeiXinCorpInfo.weixin_id == weixin_id).update({
			"access_token":ACCESS_TOKEN,
			"expire_time":(datetime.datetime.now()+datetime.timedelta(seconds=expire_time)).strftime("%Y-%m-%d %H:%M:%S"),
			"update_time":str(time.strftime("%Y-%m-%d %H:%M:%S"))
		})
		dbsession.commit()
		print("更新access_token")
	return ACCESS_TOKEN
# 检测access_token是否有效，验证方法是调用获取粉丝数的接口，返回结果没有错误代码就表明有效
def check_access_token(access_token):
	count_url = config.wechat_api["getusercumulate"]+"access_token=" + access_token
	today = datetime.date.today()
	end_date = today - datetime.timedelta(days=1)
	post_data = {
		"begin_date": str(end_date),
		"end_date": str(end_date)
	}
	headers = {
		'Content-type': 'application/json'
	}
	count_data = requests.post(url=count_url, data=json.dumps(post_data), headers=headers).json()
	return True if "errcode" not in count_data else False

# GET处理请求，统一使用本方法进行请求。进行处理access_token和发送请求
# get_param格式为{"url":"","params":""}  parmas不包含access_token,在发送请求时再加入access_token
# 使用注解重写
def get_request(url):
	def pro_get_request(func):
		def pro_func(weixin_id,params):
			access_token = get_access_token(weixin_id)
			headers = {'Content-type': 'application/json'}
			params["access_token"] = access_token
			r = requests.get(url=url, params=params,headers=headers)
			func(r)
		return pro_func
	return pro_get_request
# POST处理请求，统一使用本方法进行请求。进行处理access_token和发送请求
# post_data为post请求传递的参数
def post_request(url):
	def pro_post_request(func):
		def pro_func(weixin_id,post_data={}):
			access_token = get_access_token(weixin_id)
			headers = {'Content-type': 'application/json'}
			params = {"access_token": access_token}
			r=requests.post(url=url+urllib.parse.urlencode(params),data=json.dumps(post_data),headers=headers)
			func(r)
		return pro_func
	return pro_post_request

# 获取粉丝总数
# post_data = {
# 		"begin_date": "2018-04-11",
# 		"end_date": "2018-04-11"
# 	}
@post_request(config.wechat_api["getusercumulate"])
def get_user_cumulate(response_data):
	return response_data.json()

# 获取粉丝数的新增和取关数据
# post_data = {
# 		"begin_date": begin_date,
# 		"end_date": end_date
# 	}
@post_request(config.wechat_api["getusersummary"])
def get_user_summary(response_data):
	return response_data.json()

# 获取文章素材的详情，media_id素材ID
# post_data = {"media_id": media_id}
@post_request(config.wechat_api["get_material"])
def get_material_detail(response_data):
	return json.loads(str(response_data.content,"utf-8"))

# 获取粉丝数，进行处理后返回总数和新增、取关的数据。由于测试时出现了总数返回数据为空的情况，使用之前最近数据加上新增减去取关的数据计算得到
def get_fan_data(begin_date,end_date,weixin_id,mp_name):
	post_data = {
			"begin_date": begin_date,
			"end_date": end_date
		}
	summary_data=get_user_summary(weixin_id,post_data)
	count_data= get_user_cumulate(weixin_id,post_data)
	ref_date = end_date
	new_user=0
	cancel_user=0
	if len(summary_data["list"])>0:
		ref_date = summary_data["list"][0]["ref_date"]
		for a in summary_data["list"]:
			if a["ref_date"]==ref_date:
				new_user=new_user+a["new_user"]
				cancel_user = cancel_user+a["cancel_user"]
	if len(count_data["list"])>0:
		cumulate_user = count_data["list"][0]["cumulate_user"]
	else:
		pre_date=datetime.datetime.strptime(end_date, "%Y-%m-%d")-datetime.timedelta(days=1)
		pre_cumulate_user=dbsession.query(WeiXinFollowersHistory.cumulate_user).filter(WeiXinFollowersHistory.ref_date==str(pre_date)[:10],
																		 WeiXinFollowersHistory.name==mp_name).first()
		cumulate_user=pre_cumulate_user[0]+new_user-cancel_user
	fans_data={
		"ref_date":ref_date,
		"new_user":new_user,
		"cancel_user":cancel_user,
		"cumulate_user":cumulate_user
	}
	return fans_data

# 获取文章的数据，以下几个参数相同
# post_data = {
# 		"begin_date": begin_date,
# 		"end_date": end_date
# 	}
@post_request(config.wechat_api["getarticletotal"])
# 获取图文群发总数据
def getarticletotal(response_data):
	return response_data.json()
@post_request(config.wechat_api["getarticlesummary"])
# 获取图文群发每日数据
def getarticlesummary(response_data):
	return response_data.json()
@post_request(config.wechat_api["getuserread"])
# 获取图文统计数据
def getuserread(response_data):
	return response_data.json()
@post_request(config.wechat_api["getuserreadhour"])
# 获取图文统计分时数据
def getuserreadhour(response_data):
	return response_data.json()
@post_request(config.wechat_api["getusershare"])
# 获取图文分享转发数据
def getusershare(response_data):
	return response_data.json()
@post_request(config.wechat_api["getusersharehour"])
# 获取图文分享转发分时数据
def getusersharehour(response_data):
	return response_data.json()
# 获取素材列表
# 	post_data = {
# 		"type": TYPE,
# 		"offset": OFFEST,
# 		"count": COUNT
# 	}
@post_request(config.wechat_api["batchget_material"])
def batchget_material(response_data):
	return json.loads(str(response_data.content,"utf-8"))

# 获取素材总数
# post_data={}
@post_request(config.wechat_api["get_materialcount"])
def get_material_count(response_data):
	return response_data

# 获取用户
# params={"next_openid":""}
@get_request(url=config.wechat_api["get_users"])
def get_users(response_data):
	return response_data
# 获取用户详细信息
# params={"openid":"","lang":"zh_CN"}
@get_request(url=config.wechat_api["user_info"])
def get_user_info(response_data):
	return response_data


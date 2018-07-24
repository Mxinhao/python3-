#coding:utf-8
import sys
from sinaweibopy.weibo import APIClient
import json
import time
import datetime
import re
import requests
from  db import *
# dbsession=_init_db()
# 正则提取微博来源
res_tr = '<a .*?>(.*?)</a>'

def create_date_format(create_date):
	senddate = int(time.mktime(time.strptime(create_date, "%a %b %d %H:%M:%S +%f %Y")))
	senddate = time.localtime(senddate)
	senddate = time.strftime("%Y-%m-%d %H:%M:%S", senddate)
	return senddate

weiboinfos=dbsession.query(WeiBoInfo).filter(WeiBoInfo.enabled==1).all()
for weiboinfo in weiboinfos:
	print("----------账号----------" + weiboinfo.mp_name)
	APP_KEY = weiboinfo.appid  # app key
	APP_SECRET = weiboinfo.appsecrpt      # app secret
	CALLBACK_URL = weiboinfo.callback_url  # callback url  
	ACCESS_TOKEN=weiboinfo.access_token
	EXPITRS=weiboinfo.expitrs
	# 查询token的信息，是否过期
	rate_url="https://api.weibo.com/oauth2/get_token_info"
	param={
		"access_token":ACCESS_TOKEN
	}
	r=requests.post(rate_url,data=param).json()
	print(r)
	
	client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
	client.set_access_token(ACCESS_TOKEN, EXPITRS)
	da = client.account.rate_limit_status.get()
	print(da)
	# exit()
	try:
		follows_data = client.users.counts.get(uids=weiboinfo.uid)
	except Exception as e:
		continue
	# follows_data = client.users.counts.get(uids=weiboinfo.uid)
	print(follows_data)
	followers = WeiBoAPIFollowers()
	followers.weibo_id = follows_data[0]["id"]
	followers.mp_name = weiboinfo.mp_name
	followers.followers_count = follows_data[0]["followers_count"]
	followers.friends_count = follows_data[0]["friends_count"]
	followers.statuses_count = follows_data[0]["statuses_count"]
	followers.update_time = time.strftime("%Y-%m-%d %H:%M:%S")
	dbsession.add(followers)
	try:
		data=client.statuses.user_timeline.get(count=5, page=1)
	except Exception as e:
		continue
	for da in data["statuses"]:
		article=WeiBoArticleList()
		article.mp_name=da["user"]["name"]
		create_date=da["created_at"]
		article.created_at=create_date_format(create_date)
		article.id=da["id"]
		article.idstr=da["idstr"]
		article.mid=da["mid"]
		article.can_edit=1 if da["can_edit"]==True else 0
		article.text = da["text"]
		article.textLength =da["textLength"] if "retweeted_status" not in da else da["retweeted_status"]["textLength"]
		m_tr = re.findall(res_tr, da["source"],re.S | re.M)
		article.source=m_tr[0] if len(m_tr)>0 else ""
		article.favorited=1 if da['favorited']==True else 0
		article.truncated = 1 if da['truncated'] == True else 0
		article.in_reply_to_status_id=da["in_reply_to_status_id"]
		article.in_reply_to_screen_name = da["in_reply_to_screen_name"]
		article.in_reply_to_user_id=da['in_reply_to_user_id']
		article.user=da["user"]["id"]
		article.attitudes_count=da["attitudes_count"]
		article.reposts_count=da['reposts_count']
		article.comments_count=da["comments_count"]
		article.bmiddle_pic= da["bmiddle_pic"] if "bmiddle_pic" in da else ""
		article.thumbnail_pic = da["thumbnail_pic"] if "thumbnail_pic" in da else ""
		article.original_pic = da["original_pic"] if "original_pic" in da else ""
		article.geo=json.dumps(da["geo"]) if da["geo"] !=None else ""
		article.update_at=datetime.datetime.now()
		article.mlevel=da["mlevel"]
		article.pic_ids=json.dumps(da["pic_ids"]) if "pic_ids" in da else ""
		article.retweeted_status=json.dumps(da["retweeted_status"]) if "retweeted_status" in da else ""
		article.visible=json.dumps(da["visible"])
		article.source_type=da["source_type"]
		article.source_allowclick=da["source_allowclick"]
		dbsession.merge(article)
		description=da["user"]["description"]
		dbsession.query(WeiBoInfo).filter(WeiBoInfo.uid==weiboinfo.uid).update({"description":description,
																				"updated":datetime.datetime.now()})
		print("----------微博----------" + article.text+"   评论数："+str(article.comments_count))
		if article.comments_count>0:
			pages=int(article.comments_count/200)+1
			count=200 if article.comments_count >= 200 else article.comments_count
			for i in range(1,pages+1):
				comments=client.comments.show.get(id=article.id,page=i,count=count)
				if "comments" not in comments:
					break
				for comment in comments["comments"]:
					weibo_comment=WeiBoAPIComment()
					weibo_comment.id=comment["id"]
					weibo_comment.weibo_id=article.id
					weibo_comment.user_id=comment["user"]["id"]
					weibo_comment.mid=comment["mid"]
					weibo_comment.idstr=comment["idstr"]
					weibo_comment.reply_comment=comment["reply_comment"]["id"] if "reply_comment" in comment else ""
					weibo_comment.created_at=create_date_format(comment["created_at"])
					weibo_comment.text=comment["text"]
					weibo_comment.source=comment["source"] if "source" in comment else ""
					weibo_comment.rootid=comment["rootid"]
					weibo_comment.floor_number = comment["floor_number"]
					check_result=dbsession.query(WeiBoAPIComment).filter(WeiBoAPIComment.id==weibo_comment.id)
					if check_result.count()<1:
						dbsession.add(weibo_comment)
					userinfo=comment["user"]
					user=WeiBoAPIUserinfo()
					user.id=userinfo["id"]
					user.idstr=userinfo["idstr"]
					user.created_at=create_date_format(userinfo["created_at"])
					user.name=userinfo["name"]
					user.screen_name=userinfo["screen_name"]
					user.url=userinfo["url"]
					user.province=userinfo["province"]
					user.city=userinfo["city"]
					user.location=userinfo["location"]
					user.description=userinfo["description"]
					user.profile_image_url=userinfo["profile_image_url"]
					user.profile_url=userinfo["profile_url"]
					user.domain=userinfo["domain"]
					user.weihao=userinfo["weihao"]
					user.gender=userinfo["gender"]
					user.followers_count=userinfo["followers_count"]
					user.friends_count=userinfo["friends_count"]
					user.statuses_count=userinfo["statuses_count"]
					user.favourites_count=userinfo["favourites_count"]
					user.following=1 if userinfo["following"]==True else 0
					user.allow_all_act_msg=1 if userinfo["allow_all_act_msg"]==True else 0
					user.geo_enabled=1 if userinfo["geo_enabled"]==True else 0
					user.verified=1 if userinfo["verified"]==True else 0
					user.verified_type=userinfo["verified_type"]
					user.verified_reason=userinfo["verified_reason"]
					user.remark=userinfo["remark"]
					user.allow_all_comment=1 if userinfo["allow_all_comment"]==True else 0
					user.avatar_large=userinfo["avatar_large"]
					user.avatar_hd=userinfo["avatar_hd"]
					user.bi_followers_count=userinfo["bi_followers_count"]
					user.online_status=userinfo["online_status"]
					user.lang=userinfo["lang"]
					user.follow_me=1 if userinfo["follow_me"]==True else 0
					user.domain=userinfo["domain"]
					dbsession.merge(user)
		dbsession.commit()
	print("----账号："+weiboinfo.mp_name+"-----------获取完成")
print("----------------执行结束----------------")


# API调用次数限制
#
# 	da=client.account.rate_limit_status.get()
# 	print(da)

# {'api_rate_limits': [
# 	{'api': '/statuses/update', 'limit': 15, 'limit_time_unit': 'HOURS', 'remaining_hits': 15},
# 	{'api': '/comments/create', 'limit': 15, 'limit_time_unit': 'HOURS', 'remaining_hits': 15},
# 	{'api': '/direct_messages/new', 'limit': 15, 'limit_time_unit': 'HOURS', 'remaining_hits': 15},
# 	{'api': '/friendships/create', 'limit': 15, 'limit_time_unit': 'DAYS', 'remaining_hits': 15},
# 	{'api': '/statuses/update', 'limit': 50, 'limit_time_unit': 'DAYS', 'remaining_hits': 50},
# 	{'api': '/comments/create', 'limit': 50, 'limit_time_unit': 'DAYS', 'remaining_hits': 50},
# 	{'api': '/users/query', 'limit': 15, 'limit_time_unit': 'DAYS', 'remaining_hits': 15},
# 	{'api': '/users/query', 'limit': 500, 'limit_time_unit': 'HOURS', 'remaining_hits': 500},
# 	{'api': '/users/query', 'limit': 1000, 'limit_time_unit': 'DAYS', 'remaining_hits': 1000},
# 	{'api': '/users/query', 'limit': 50, 'limit_time_unit': 'MINUTES', 'remaining_hits': 50}
# ],
# 	'ip_limit': 1000,
# 	'limit_time_unit': 'HOURS',
# 	'remaining_ip_hits': 1000,
# 	'remaining_user_hits': 150,
# 	'reset_time': '2018-06-28 16:00:00',
# 	'reset_time_in_seconds': 1316,
# 	'user_limit': 150
# }




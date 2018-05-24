#--coding:utf-8--
from bs4 import BeautifulSoup
import time
import re
import datetime
from weibos.db import _init_db,WeiBoArticleList,WeiBoInfo,WeiBoFollowersHistory
import requests
# 获取连接数据库的session
dbsession=_init_db()
# 设置爬取的微博截止时间，三天以前的不再爬取更新数据库数据
today=datetime.date.today()
pre_three_day=today-datetime.timedelta(days=3)
# 数据日期
now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
# update 更新weibo_info粉丝数
def update_fan(followers,uid):
	print("更新info粉丝数----"+str(uid))
	dbsession.query(WeiBoInfo).filter(WeiBoInfo.uid==uid).update({
		"followers":followers,
		 "updated":now
		 })
	dbsession.commit()
# 	更新粉丝数
def insert_fans(followers,uid,mp_name):
	print("插入history粉丝数----" + str(uid))
	weibo_followers=WeiBoFollowersHistory()
	weibo_followers.uid=uid
	weibo_followers.mp_name=mp_name
	weibo_followers.followers=followers
	weibo_followers.updated=now
	dbsession.add(weibo_followers)
base_url="https://m.weibo.cn/api/container/getIndex?"
def get_fans(containerid):
	fans=requests.get("https://m.weibo.cn/api/container/getIndex?"+"containerid="+str(containerid)).json()
	followers=fans["data"]["userInfo"]["followers_count"]
	return followers

# 定义获取微博数据的方法，解析html代码
def get_data():
	weibo_infos = dbsession.query(WeiBoInfo)
	for weibo_info in weibo_infos:
		flag=False
		follo=get_fans(weibo_info.ucontainerid)
		# 更新到账号信息表里
		update_fan(follo, weibo_info.uid)
		# 插入到微博历史粉丝数表里
		insert_fans(follo, weibo_info.uid, weibo_info.mp_name)
		for i in range(1,10000):
			page = base_url+"containerid="+str(weibo_info.containerid)+"&page="+str(i)
			r=requests.get(page).json()
			print(r)
			if len(r["data"]["cards"])==0:
				break
			for data in r["data"]["cards"]:
				if data["card_type"]!=9:
					continue
				weibo_article=WeiBoArticleList()
				weibo_article.followers=data["mblog"]["user"]["followers_count"]
				# 由于created_at数据有时是几小时前，无法获取详细发布时间，所以打开详情页获取详细的发布时间
				# weibo_article.created_at = data["mblog"]["created_at"]
				created=requests.get(data["scheme"]).text
				try:
					senddate=re.findall("[a-zA-Z]{3} [a-zA-Z]{3} \d{1,2} \d{2}:\d{2}:\d{2} \+0800 \d{4}",created)[0]
					senddate = int(time.mktime(time.strptime(senddate, "%a %b %d %H:%M:%S +%f %Y")))
					senddate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(senddate))
					weibo_article.created_at=senddate
				except Exception as e:
					print(e)
					weibo_article.created_at=data["mblog"]["created_at"]
				print(weibo_article.created_at)
		# 		# 置顶的文章有时为三天之前的文章，不能只根据日期就停止继续爬取博文，flag是终止外层循环即flag为True时结束此账号的爬取，开始下一个账户的爬取
				if weibo_article.created_at < str(pre_three_day) and i>1:
						flag = True
						break
				weibo_article.uid=weibo_info.uid
				weibo_article.id=data["mblog"]["id"]
				weibo_article.url="http://weibo.com/"+str(weibo_info.uid)+"/"+data["mblog"]["bid"]
				weibo_article.murl="https://m.weibo.cn/status/"+str(weibo_article.id)
				weibo_article.mp_name=weibo_info.mp_name
				# weibo_article.text= data["mblog"]["text"] #
				# 去除内容中的html标签
				soup=BeautifulSoup(data["mblog"]["text"],"html.parser")
				weibo_article.text = soup.text.replace(" ","").replace("\n","").replace("\t","")
				weibo_article.source=data["mblog"]["source"]
				weibo_article.reposts= data["mblog"]["reposts_count"]
				weibo_article.comments=data["mblog"]["comments_count"]
				weibo_article.likes = data["mblog"]["attitudes_count"]
				weibo_article.updated=now
				# 发布日期为三天之内才进行数据库更新
				if str(weibo_article.created_at)[:10] >= str(pre_three_day):
					insert_data(weibo_article)
					print(str(weibo_article.reposts)+"----"+str(weibo_article.comments)+"----"+str(weibo_article.likes))
				print("----------------------------------------------")
			if flag:
				break
		print("-------------------" + weibo_info.mp_name + "爬取完毕---------------------------")
	print("-------------------所有账号爬取完毕---------------------------")
# 定义将博文插入到数据库的方法
def insert_data(weibo_article):
	result=dbsession.query(WeiBoArticleList).filter(WeiBoArticleList.id==weibo_article.id)
	if result.count()==0:
		dbsession.add(weibo_article)
	else:
		dbsession.query(WeiBoArticleList).filter(WeiBoArticleList.id == weibo_article.id).update({
			"followers":weibo_article.followers,
			"reposts":weibo_article.reposts,
			"comments":weibo_article.comments,
			"likes":weibo_article.likes,
			"text":weibo_article.text,
			"updated":time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		})
def main():
	try:
		get_data()
		dbsession.commit()
	except Exception as e:
		print(e)
if __name__ == '__main__':
	print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
	main()
	print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
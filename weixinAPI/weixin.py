#--coding:utf-8--
import time
import datetime
from db import *
from tool import getarticletotal,get_access_token,get_fan_data

def main():
	today=datetime.date.today()
	# 粉丝数据日期最大只能为昨日
	end_date=today-datetime.timedelta(days=1)
	weixin_infos=dbsession.query(WeiXinCorpInfo).filter(WeiXinCorpInfo.enabled==1)
	for info in weixin_infos:
		print("---------开始爬取账号："+str(info.name)+"-----------")
		fan_data=get_fan_data(str(end_date),str(end_date),info.weixin_id,info.name)
		print(fan_data)
		weixin_fan=WeiXinFollowersHistory()
		weixin_fan.name=info.name
		weixin_fan.ref_date=fan_data["ref_date"]
		weixin_fan.new_user=fan_data["new_user"]
		weixin_fan.cancel_user=fan_data["cancel_user"]
		weixin_fan.cumulate_user=fan_data["cumulate_user"]
		weixin_fan.update_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
		weixin_fan.ref_date=str(end_date)
		check_result=dbsession.query(WeiXinFollowersHistory).filter(WeiXinFollowersHistory.name==info.name,WeiXinFollowersHistory.ref_date==str(end_date)).count()
		if check_result==0:
			dbsession.add(weixin_fan)
			follows=fan_data["cumulate_user"]
			dbsession.query(WeiXinCorpInfo).filter(WeiXinCorpInfo.weixin_id==info.weixin_id).update({"follows":follows,"update_time":time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())}) #(datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
			dbsession.commit()
		# 爬取最近7日的数据
		for i in range(7,0,-1):
			begin_date = today - datetime.timedelta(days=i)
			print("------文章发布日期："+str(begin_date)+"-------------")
			article_data=getarticletotal(info.weixin_id,{"begin_date":str(begin_date),"end_date":str(begin_date),})
			if "list" in article_data:
				for article in article_data["list"]:
					for data in article["details"]:
						query_result=dbsession.query(WeiXinCropArticle).filter(WeiXinCropArticle.msgid==article["msgid"],WeiXinCropArticle.stat_date==data["stat_date"])
						if query_result.count()>=1:
							continue
						weixin_crop_article = WeiXinCropArticle()
						weixin_crop_article.name=info.name
						weixin_crop_article.title=article["title"]
						weixin_crop_article.msgid=article["msgid"]
						weixin_crop_article.ref_date=article["ref_date"]
						weixin_crop_article.msgid_serial=str(weixin_crop_article.msgid)[:-2]
						weixin_crop_article.msgid_sort = str(weixin_crop_article.msgid)[-1:]
						weixin_crop_article.stat_date=data["stat_date"]
						weixin_crop_article.stat_sort = (datetime.datetime.strptime(weixin_crop_article.stat_date,"%Y-%m-%d")-datetime.datetime.strptime(weixin_crop_article.ref_date,"%Y-%m-%d")).days+1
						weixin_crop_article.target_user=data["target_user"]
						weixin_crop_article.int_page_read_user = data["int_page_read_user"]
						weixin_crop_article.int_page_read_count = data["int_page_read_count"]
						weixin_crop_article.ori_page_read_user = data["ori_page_read_user"]
						weixin_crop_article.ori_page_read_count = data["ori_page_read_count"]
						weixin_crop_article.share_user = data["share_user"]
						weixin_crop_article.share_count = data["share_count"]
						weixin_crop_article.add_to_fav_user = data["add_to_fav_user"]
						weixin_crop_article.add_to_fav_count = data["add_to_fav_count"]
						weixin_crop_article.int_page_from_session_read_user = data["int_page_from_session_read_user"]
						weixin_crop_article.int_page_from_session_read_count = data["int_page_from_session_read_count"]
						weixin_crop_article.int_page_from_hist_msg_read_user = data["int_page_from_hist_msg_read_user"]
						weixin_crop_article.int_page_from_hist_msg_read_count = data["int_page_from_hist_msg_read_count"]
						weixin_crop_article.int_page_from_feed_read_user = data["int_page_from_feed_read_user"]
						weixin_crop_article.int_page_from_feed_read_count = data["int_page_from_feed_read_count"]
						weixin_crop_article.int_page_from_friends_read_user = data["int_page_from_friends_read_user"]
						weixin_crop_article.int_page_from_friends_read_count = data["int_page_from_friends_read_count"]
						weixin_crop_article.int_page_from_other_read_user = data["int_page_from_other_read_user"]
						weixin_crop_article.int_page_from_other_read_count = data["int_page_from_other_read_count"]
						weixin_crop_article.feed_share_from_session_user = data["feed_share_from_session_user"]
						weixin_crop_article.feed_share_from_session_cnt = data["feed_share_from_session_cnt"]
						weixin_crop_article.feed_share_from_feed_user = data["feed_share_from_feed_user"]
						weixin_crop_article.feed_share_from_feed_cnt = data["feed_share_from_feed_cnt"]
						weixin_crop_article.feed_share_from_other_user = data["feed_share_from_other_user"]
						weixin_crop_article.feed_share_from_other_cnt = data["feed_share_from_other_cnt"]
						dbsession.add(weixin_crop_article)
						print("插入数据--"+weixin_crop_article.title)
						dbsession.commit()
			else:
				print("返回字典数据里没有数据")

if __name__=="__main__":
	print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
	main()
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	print("--------------执行结束---------------")
dbhost=""
dbport=3306
dbname=""
dbuser=""
dbpassword=""
dbcharset="utf8"


wechat_api={
	# get方法请求接口
	"access_token":"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=",
	"user_info":"https://api.weixin.qq.com/cgi-bin/user/info?",
	"get_users":"https://api.weixin.qq.com/cgi-bin/user/get?",
	# # post方法请求接口
	"getusercumulate":"https://api.weixin.qq.com/datacube/getusercumulate?",
	"get_material":"https://api.weixin.qq.com/cgi-bin/material/get_material?",
	"getusersummary":'https://api.weixin.qq.com/datacube/getusersummary?',
	"getarticletotal":"https://api.weixin.qq.com/datacube/getarticletotal?",
	"batchget_material":"https://api.weixin.qq.com/cgi-bin/material/batchget_material?",
	"get_materialcount":'https://api.weixin.qq.com/cgi-bin/material/get_materialcount?',
	"getarticlesummary":"https://api.weixin.qq.com/datacube/getarticlesummary?",
	"getuserread":"https://api.weixin.qq.com/datacube/getuserread?",
	"getuserreadhour":"https://api.weixin.qq.com/datacube/getuserreadhour?",
	"getusershare":"https://api.weixin.qq.com/datacube/getusershare?",
	"getusersharehour":"https://api.weixin.qq.com/datacube/getusersharehour?"
}
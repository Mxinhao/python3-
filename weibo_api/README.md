# 
使用python3调用微博开放接口获取数据
官方替供的python SDK是廖雪峰大神的，只基于python2的，sinaweibopy下的weibo.py支持python3的版本调用

本目录下的get_token.py是获取access_token的程序
使用方法如下    
    1、补全程序中的变量信息
    2、将打印出的url复制粘贴到浏览器
    3、使用对应的微博账号进行登录，并点击授权
    4、将浏览器地址栏后面的code，粘贴到程序控制台并回车
    5、得到access_token
将access_token保存到对应数据里，以备后面程序使用

weibo.py文件的使用

本程序流程是获取发布的微博，通过微博的id取获取评论的内容，保存评论信息和评论人信息

    statuses/user_timeline.json 接口获取发布的微博(只能获取最新的5条数据)
    comments/show.json 接口获取微博对应的评论

数据库表信息不再给出，数据库字段和db.py字段保持一致


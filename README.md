# python3-
学习使用python，平时使用到的小代码

email_util.py文件的使用
使用这个工具，收发邮件只需要四步
发邮件
1、导入这个py文件
  from email_util import email_util
2、实例化一个对象
  emailUtil=email_util(server,user,password)
3、构建邮件
    message = MIMEMultipart('related')
    message['From'] = ""
    message['To'] = "" #多个收件人需要 receivers=[] 然后转为字符串 ','.join(receivers)
    message['Subject'] = Header("测试发送", 'utf-8')
    puretext = MIMEText("哈哈哈哈，发送成功", 'html', 'utf-8')
    message.attach(puretext)
    #附件
    filename = 'abc.xls'
    att1 = MIMEApplication(open(filename, 'rb').read())
    att1.add_header('Content-Disposition', 'attachment', filename='abc.xls')
    message.attach(att1)
4、发送邮件
    emailUtil.send_email(message)
 收邮件
 1、2步和发邮件一样，不再重复，需要注意的是server,163邮箱的SMTP server为 smtp.163.com  pop3的地址为pop.163.com
 3、获取邮件
    count=emailUtil.mails_count()#获取邮件个数
    email=emailUtil.get_email(count)#使用索引位置获取邮件，count为最新的一封邮件
 4、获取邮件内容
    receive = emailUtil.get_receive(email)#获取收件人
    sender= emailUtil.get_sender(email)#获取发件人
    subject=emailUtil.get_subject(email)#获取主题
    cc=emailUtil.get_receive_cc(email)#获取抄送收件人
    content=emailUtil.get_mail_content(email)#获取邮件的内容和附件，返回的是字典
    #保存附件
    if "files" in content.keys():
        for file in content["files"]:
            with open("d:\\email_file\\"+file["name"],'wb') as f:
                f.write(file['data'])
